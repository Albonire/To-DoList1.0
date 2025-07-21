document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.task-complete-checkbox');

    // Configuración del Toast de SweetAlert2
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer);
            toast.addEventListener('mouseleave', Swal.resumeTimer);
        }
    });

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const form = this.closest('.task-complete-form');
            const taskId = form.dataset.taskId;
            const isCompleted = this.checked;
            const taskCard = this.closest('.task-card');

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name="csrfmiddlewaretoken"]').value,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    is_completed: isCompleted
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Actualizar UI
                    if (data.estado === 'completada') {
                        taskCard.classList.add('task-completed');
                    } else {
                        taskCard.classList.remove('task-completed');
                    }
                    // Mostrar notificación con SweetAlert2
                    Toast.fire({
                        icon: 'success',
                        title: data.message
                    });
                } else {
                    // Revertir el estado del checkbox si hay un error
                    this.checked = !isCompleted;
                    Toast.fire({
                        icon: 'error',
                        title: data.message
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                this.checked = !isCompleted; // Revertir en caso de error de red
                Toast.fire({
                    icon: 'error',
                    title: 'Ocurrió un error al actualizar la tarea.'
                });
            });
        });
    });
});
