const openCartModalButton = document.getElementById('open_cart_modal_button');
const cartModal = document.getElementById('cart_modal');
const cart_items_delete = document.getElementsByClassName('cart_item_delete');


openCartModalButton.addEventListener('click', (event) => {
    event.stopPropagation();
    if (cartModal.style.display === '') {
        cartModal.style.display = 'none';
    } 

    if (cartModal.style.display === 'block') {
        cartModal.style.display = ''
    }
    
    if (cartModal.style.display === 'none') {
        cartModal.style.display = 'block';

        fetch('http://127.0.0.1:8000/get_cart/', {
    method: 'GET'
})
.then(response => {
    if (response.ok) {
        return response.json(); // Возвращаем промис
    } else {
        throw new Error('Server response was not ok');
    }
})
.then(data => {
    console.log(data.total_price)})
.catch(error => {
    // Обработка ошибок
    console.error('There was a problem with the fetch operation:', error);
});
    }
});

window.addEventListener('click', (event) => {
    if (!cartModal.contains(event.target)) {
        cartModal.style.display = 'none';
    }
});



Array.from(cart_items_delete).forEach(cart_item_delete => {
    cart_item_delete.addEventListener('click', function(e) {
        e.stopPropagation()

        let productSlug = cart_item_delete.getAttribute('product_slug')

        fetch(`http://127.0.0.1:8000/remove_from_cart/${productSlug}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => {
            if (response.ok) {
                // Будет создаваться массив из полученных объектов
                console.log(response.json())
            }
        })
    })
})


const cleanCartButton = document.getElementById('clean_cart_button');


cleanCartButton.addEventListener('click', function(e) {
    e.stopPropagation()
    fetch('http://127.0.0.1:8000/clean_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => {
        if (response.ok) {
            // Будет создаваться массив из полученных объектов
            console.log(response.json())
        }
    })
})


const addToCartButtons = document.getElementsByClassName('add_to_cart_button');


Array.from(addToCartButtons).forEach(addToCartButton => {
    addToCartButton.addEventListener('click', function(e) {
        e.stopPropagation()
        let productSlug = addToCartButton.getAttribute('product_slug');

    fetch(`http://127.0.0.1:8000/add_to_cart/${productSlug}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken
            }
    })
    .then(response => {
        if (response.ok) {
        console.log(response.json())
        }
    })
        })

})