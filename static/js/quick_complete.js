document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.task-complete-checkbox');

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
            const taskCard = this.closest('.task-card');
            const statusBadge = taskCard.querySelector('.task-status');

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name="csrfmiddlewaretoken"]').value,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    is_completed: this.checked
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // --- INICIO DE LA LÓGICA MEJORADA ---

                    // 1. Actualizar clases de la tarjeta principal
                    taskCard.classList.remove('task-completed', 'task-overdue');
                    if (data.estado === 'completada') {
                        taskCard.classList.add('task-completed');
                    } else if (data.estado === 'vencida') {
                        taskCard.classList.add('task-overdue');
                    }

                    // 2. Actualizar el badge de estado
                    if (statusBadge) {
                        // Mapeo de estados a texto legible
                        const statusTextMap = {
                            'pendiente': 'Pendiente',
                            'completada': 'Completada',
                            'vencida': 'Vencida'
                        };
                        
                        // Actualizar texto del badge
                        statusBadge.innerHTML = `<i class="fas fa-circle"></i> ${statusTextMap[data.estado] || 'Desconocido'}`;
                        
                        // Actualizar clases del badge
                        statusBadge.className = 'task-status'; // Reset classes
                        statusBadge.classList.add(`status-${data.estado}`);
                    }
                    
                    // --- FIN DE LA LÓGICA MEJORADA ---

                    Toast.fire({
                        icon: 'success',
                        title: data.message
                    });

                } else {
                    this.checked = !this.checked; // Revertir checkbox en caso de error
                    Toast.fire({
                        icon: 'error',
                        title: data.message
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                this.checked = !this.checked; // Revertir en caso de error de red
                Toast.fire({
                    icon: 'error',
                    title: 'Ocurrió un error al actualizar la tarea.'
                });
            });
        });
    });
});