const auth_modal = document.querySelector('.auth_modal');
const auth_modal_open_button = document.querySelector('.auth_modal_open_button');

document.addEventListener('click', (event) => {
    if (!auth_modal.contains(event.target) && event.target !== auth_modal_open_button) {
        auth_modal.classList.remove('auth_modal_active');
    }
});

auth_modal_open_button.addEventListener('click', function() {
    auth_modal.classList.add('auth_modal_active');
});


