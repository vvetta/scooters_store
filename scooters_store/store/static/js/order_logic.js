const order_products_div = document.querySelector('.order-products');
const total_price_div = document.querySelector('.order-total');


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
        let total_order_price_html = '';
        total_price_div.innerHTML = data.total_price;
        let innerHtml = '';
        for (let i = 0; i < data.products.length; i++) {
                innerHtml += `<div class="order-col" product_slug=${data.products[i].slug}>
									<div>${data.products[i].quantity}x ${data.products[i].title}</div>
									<div>${data.products[i].price}</div>
								</div>`
            };
            order_products_div.innerHTML = innerHtml;
    })


// Создание заказа


const order_submit_btn = document.querySelector('.order-submit');

order_submit_btn.addEventListener('click', function () {
    let order_inputs = document.querySelectorAll('input');
    let products_list = document.querySelector('.order-products');
    let order_comment = document.querySelector('textarea');
    let order_total_price = document.querySelector('.order-total');

    let products = Array.from(products_list.children);

    let submit_data = {};

    for (let i = 0; i < order_inputs.length; i++) {
        submit_data[order_inputs[i].getAttribute('name')] = order_inputs[i].value;
    }

    submit_data['products'] = []
    submit_data['comment'] = order_comment.value;
    submit_data['total_price'] = Number(order_total_price.innerHTML);

    for (let i = 0; i < products.length; i++) {
        submit_data['products'].push(products[i].getAttribute('product_slug'))
    }

    console.log(submit_data);

//    let data = new FormData();
//    data.append("json", JSON.stringify(submit_data));

    fetch('http://127.0.0.1:8081/create_order/', {
    method: "POST",
    headers: {
        'Content-Type': 'application/json ',
        'X-CSRFToken': csrftoken
    },
    body: JSON.stringify(submit_data)
    }).then(response => {
        return response.json()
    }).then(data => {
        console.log(data)
        let modal_message = document.querySelector('.modal_message_span');
        let modal_order_id = document.querySelector('.modal_order_id');
        let modal_wrapper = document.querySelector('.modal_wrapper');

        modal_order_id.innerHTML = data.order_id;
        modal_message.innerHTML = data.message;

        modal_wrapper.style.display = 'flex';

        fetch('http://127.0.0.1:8081/clean_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        }
    })

    })



});