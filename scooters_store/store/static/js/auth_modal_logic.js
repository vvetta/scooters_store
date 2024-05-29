const openModalButtons = document.getElementsByClassName('open_auth_modal_button');
const authModal = document.getElementById('auth_modal_tonner');
const closeModalButton = document.getElementById('close_auth_modal_button');

Array.from(openModalButtons).forEach(openModalButton => {
    openModalButton.addEventListener('click', () => {
        authModal.style.display = 'flex';
    });     
});

window.addEventListener('click', (event) => {
    if (event.target === authModal || event.target === cartModal) {
        authModal.style.display = 'none';
    }
});

closeModalButton.addEventListener('click', () => {
    authModal.style.display = 'none';
});



const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const authModalForms = document.getElementsByClassName('auth_modal_form');
let authPath;

Array.from(authModalForms).forEach(authModalForm => {
    authModalForm.addEventListener('submit', function(e) {
        e.preventDefault();
    
        let formData = new FormData(this);

        if (formData.get('privacy_policy')) {
            authPath = 'register'
        } else {
            authPath = 'login'
        }
    
        fetch(`http://127.0.0.1:8000/${authPath}/`, {
            headers: {
//                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': csrftoken
            },
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/';
            }
        })
    })
})


const exitButton = document.getElementById