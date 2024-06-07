const add_to_favorite_btns = document.querySelectorAll('.add-to-wishlist');

for (let i = 0; i < add_to_favorite_btns.length; i++) {
  add_to_favorite_btns[i].addEventListener('click', function () {
    let product_slug = add_to_favorite_btns[i].getAttribute('product_slug')
    fetch(`http://127.0.0.1:8081/add_to_favorite/${product_slug}/`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrftoken
      }
    })
})};

const open_wishlist_button = document.querySelector('.wishlist_open_button');
const wishlist_wrapper = document.querySelector('.wishlist_wrapper');
const wishlist_list = document.querySelector('.wishlist_list');

open_wishlist_button.addEventListener('click', function() {
  wishlist_wrapper.classList.toggle('wishlist_active');

  if (wishlist_wrapper.classList.contains('wishlist_active')) {
    fetch('http://127.0.0.1:8081/wishlist_detail/', {
      method: "GET"
    }).then(response => {
      if (response.ok) {return response.json()}
    }).then(data => {
      let list_innerHtml = '';
      for(let i = 0; i < data.products.length; i++) {
        list_innerHtml += `<div class="product-widget wishlist_product"><div class="product-img"><img src="http://127.0.0.1:8081/${data.products[i].photo}" alt=""></div>
        <div class="product-body"><h3 class="product-name"><a href="http://127.0.0.1:8081/product_detail/${data.products[i].slug}/">${data.products[i].title}</a></h3>
        <h4 class="product-price">${data.products[i].price}</h4></div>
        <button class="delete wishlist_remove_button" product_slug="${data.products[i].slug}" product_price="${data.products[i].price}"
        product_photo_src="http://127.0.0.1:8081/${data.products[i].photo}" product_title="${data.products[i].title}"><i class="fa fa-close"></i></button></div>`
      };
      wishlist_list.innerHTML = list_innerHtml;

      const wishlist_remove_buttons = document.querySelectorAll('.wishlist_remove_button');

      for(let i = 0; i < wishlist_remove_buttons.length; i++) {
        wishlist_remove_buttons[i].addEventListener('click', function() {
          let product_slug =  wishlist_remove_buttons[i].getAttribute('product_slug');
          fetch(`http://127.0.0.1:8081/remove_from_favorite/${product_slug}/`, {
            method: "POST",
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'X-CSRFToken': csrftoken
            }
          }).then(response => {if (response.ok) {
            const wishlist_products = document.querySelectorAll('.wishlist_product');
            for (let i = 0; i < wishlist_products.length; i++) {
              let wishlist_slug = wishlist_products[i].lastElementChild.getAttribute('product_slug');
              if (product_slug === wishlist_slug) {
                wishlist_list.removeChild(wishlist_products[i])
              }
            }
          }})
        })
      };
    })
  }
})

document.addEventListener('click', (event) => {
  if (!wishlist_wrapper.contains(event.target) && event.target !== open_wishlist_button) {
    wishlist_wrapper.classList.remove('wishlist_active');
  }
});