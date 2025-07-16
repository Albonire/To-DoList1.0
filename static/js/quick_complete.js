document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.task-complete-checkbox');

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
                    // Update UI
                    if (data.estado === 'completada') {
                        taskCard.classList.add('task-completed');
                    } else {
                        taskCard.classList.remove('task-completed');
                    }
                    // Show a temporary notification (you might need a dedicated notification system)
                    alert(data.message); 
                } else {
                    // Revert checkbox state if there was an error
                    this.checked = !isCompleted;
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                this.checked = !isCompleted; // Revert checkbox on network error
                alert('Ocurrió un error al actualizar la tarea.');
            });
        });
    });
});
