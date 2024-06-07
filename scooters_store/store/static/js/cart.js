
// Добавление товара в корзину

const add_to_cart_btns = document.querySelectorAll('.add-to-cart-btn');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

for (let i = 0; i < add_to_cart_btns.length; i++) {
    add_to_cart_btns[i].addEventListener('click', function () {
        let productSlug = add_to_cart_btns[i].getAttribute('product_slug');

        fetch(`http://127.0.0.1:8081/add_to_cart/${productSlug}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken
            }
        })

        const cart_len_div = document.querySelector('.cart_len');
        cart_len_div.innerHTML = Number(cart_len_div.innerHTML) + 1

        // Обновление количества товаров в корзине
        fetch('http://127.0.0.1:8081/get_cart/', {
    method: 'GET',
    headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken
            }
    }).then(
        response => {
            if (response.ok) {
                return response.json()
            } else {
                throw new Error('Server response was not ok');
            }
        }
    ).then(data => {
        const cart_len_div = document.querySelector('.cart_len');
    })

    })
};



// Открытие корзины

const open_modal_cart_button = document.querySelector('.dropdown');
const cart_list = document.querySelector('.cart-list');
const cart_summary = document.querySelector('.cart-summary');

open_modal_cart_button.addEventListener('click', function () {
    fetch('http://127.0.0.1:8081/get_cart/', {
    method: 'GET'
    }).then(
        response => {
            if (response.ok) {
                return response.json()
            } else {
                throw new Error('Server response was not ok');
            }
        }
    ).then(
        data => {
            console.log(data);
            let innerHtml = '';
            let innerHtmlSummary = `<small>${data.product_len} товар</small><h5>Итог: ${data.total_price}</h5>`;
            for (let i = 0; i < data.products.length; i++) {
                innerHtml += `<div class="product-widget"><div class="product-img"><img src="http://127.0.0.1:8081/${data.products[i].photo}" alt=""></div>
							<div class="product-body"><h3 class="product-name"><a href="#">${data.products[i].title}</a></h3>
							<h4 class="product-price"><span class="qty">${data.products[i].quantity}x</span>${data.products[i].price}</h4></div>
							<button class="delete cart_delete_btn" product_slug="${data.products[i].slug}" product_price="${data.products[i].price}" product_count="${data.products[i].quantity}"
                            product_photo_src="http://127.0.0.1:8081/${data.products[i].photo}" product_title="${data.products[i].title}"><i class="fa fa-close"></i></button></div>`
            };
            cart_list.innerHTML = innerHtml;
            cart_summary.innerHTML = innerHtmlSummary;

                // Удаление товаров из корзины
                let remove_product_from_cart_btns = document.querySelectorAll('.cart_delete_btn');

                for (let i = 0; i < remove_product_from_cart_btns.length; i++) {
                    remove_product_from_cart_btns[i].addEventListener('click', function () {

                    let productSlug = remove_product_from_cart_btns[i].getAttribute('product_slug');
                    console.log('click')

                    fetch(`http://127.0.0.1:8081/remove_from_cart/${productSlug}/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-CSRFToken': csrftoken
                        }
                    })
                    fetch('http://127.0.0.1:8081/get_cart/', {
                        method: 'GET'
                    }).then(
                        response => {
                            if (response.ok) {
                                return response.json()
                            } else {
                                throw new Error('Server response was not ok');
                            }
                        }
                    ).then(data => {
                        const cart_len_div = document.querySelector('.cart_len');
                        

                        cart_len_div.innerHTML = Number(cart_len_div.innerHTML) - 1

                        // Визуальное удаление товара из корзины покупок

                        const cart_products = document.querySelectorAll('.product-widget');
                        let cart_summary_count = Number(cart_summary.firstChild.textContent.replace(/[^0-9]/g,""));
                        let cart_summary_total = Number(cart_summary.lastChild.textContent.replace(/[^0-9]/g,""));
                        for (let i = 0; i < cart_products.length; i++) {
                            
                            let product_slug = cart_products[i].lastElementChild.getAttribute('product_slug');
                            let product_price = Number(cart_products[i].lastElementChild.getAttribute('product_price'));
                            let product_count = Number(cart_products[i].lastElementChild.getAttribute('product_count'));
                            

                            if (productSlug === product_slug && product_count === 1) {
                                cart_list.removeChild(cart_products[i]);
                                cart_summary.innerHTML = `<small>${cart_summary_count - 1} товар</small><h5>Итог: ${cart_summary_total - product_price}</h5>`;
                            };
                            if (productSlug === product_slug && product_count > 1) {
                                let qty = cart_products[i].querySelector('.qty');
                                qty.textContent = `${product_count - 1}x`;
                                cart_products[i].lastElementChild.setAttribute('product_count', product_count - 1)
                                cart_summary.innerHTML = `<small>${cart_summary_count - 1} товар</small><h5>Итог: ${cart_summary_total - product_price}</h5>`;
                            }
                        };
                    })
                    })
                }

        }
    )

});


// Получение количества товаров в корзине при заходе на страницу

fetch('http://127.0.0.1:8081/get_cart/', {
    method: 'GET'
    }).then(
        response => {
            if (response.ok) {
                return response.json()
            } else {
                throw new Error('Server response was not ok');
            }
        }
    ).then(data => {
        const cart_len_div = document.querySelector('.cart_len');
        cart_len_div.innerHTML = data.product_len
    })
