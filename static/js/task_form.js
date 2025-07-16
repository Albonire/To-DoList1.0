document.addEventListener('DOMContentLoaded', function() {
    // Aplica la clase .form-control a todos los inputs, selects y textareas del formulario
    const form = document.querySelector('.styled-form');
    if (form) {
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            if (input.type !== 'checkbox' && input.type !== 'submit' && input.type !== 'button') {
                input.classList.add('form-control');
            }
        });
    }

    // Lógica para mostrar/ocultar campos del horario
    const checkbox = document.getElementById('id_agregar_al_horario');
    if (checkbox) {
        const scheduleFields = [
            document.getElementById('id_dia_semana'),
            document.getElementById('id_hora_inicio'),
            document.getElementById('id_duracion_minutos')
        ];

        function toggleScheduleFields() {
            const isChecked = checkbox.checked;
            scheduleFields.forEach(field => {
                if (field) {
                    const formGroup = field.closest('.form-group');
                    if (formGroup) {
                        formGroup.style.display = isChecked ? 'block' : 'none';
                    }
                }
            });
        }

        // Estado inicial al cargar la página
        toggleScheduleFields();

        // Listener para cambios
        checkbox.addEventListener('change', toggleScheduleFields);
    }
});
