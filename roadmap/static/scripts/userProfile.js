// userProfile.js

document.addEventListener('DOMContentLoaded', function() {
    // Función para manejar la actualización del perfil
    const updateProfileForm = document.getElementById('updateProfileForm');
    if (updateProfileForm) {
        updateProfileForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Evita el envío del formulario por defecto

            const formData = new FormData(updateProfileForm);
            fetch(updateProfileForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken') // Asegúrate de incluir el token CSRF
                }
            })
            .then(response => {
                // Manejar la respuesta del servidor aquí
            });
        });
    }
});
