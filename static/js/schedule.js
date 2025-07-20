document.addEventListener('DOMContentLoaded', function() {
    const scheduleBody = document.getElementById('schedule-body');
    const tasksDataElement = document.getElementById('tasks-data');
    
    if (!scheduleBody || !tasksDataElement) {
        console.error("Elementos del horario no encontrados.");
        return;
    }

    const tasks = JSON.parse(tasksDataElement.textContent);
    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    const hourStart = 5;
    const hourEnd = 22;

    function renderSchedule() {
        // 1. Limpiar y crear la parrilla de horas
        scheduleBody.innerHTML = '';
        const rows = {};
        for (let hour = hourStart; hour <= hourEnd; hour++) {
            const row = scheduleBody.insertRow();
            row.id = `time-${hour}`;
            
            const timeCell = row.insertCell();
            timeCell.textContent = `${String(hour).padStart(2, '0')}:00`;
            
            days.forEach(day => {
                const cell = row.insertCell();
                cell.id = `cell-${day}-${hour}`;
                cell.dataset.day = day;
                cell.dataset.hour = hour;

                // Añadir clase para el fin de semana
                if (day === "Saturday" || day === "Sunday") {
                    cell.classList.add('weekend-col');
                }
            });
            rows[hour] = row;
        }

        // 2. Colocar las tareas en la parrilla
        tasks.forEach(task => {
            if (!task.hora_inicio || !task.dia_semana || !Array.isArray(task.dia_semana)) {
                return; // Ignorar si faltan datos clave
            }

            const [startHour, startMinute] = task.hora_inicio.split(':').map(Number);
            
            // Ignorar tareas fuera del rango de horas visible
            if (startHour < hourStart || startHour > hourEnd) {
                return;
            }

            // Iterar sobre cada día que la tarea tiene asignado
            task.dia_semana.forEach(day => {
                const startCell = document.getElementById(`cell-${day}-${startHour}`);
                if (!startCell) return;

                // Calcular rowspan (asumiendo slots de 1 hora)
                const durationHours = Math.ceil(task.duracion_minutos / 60);
                if (durationHours > 1) {
                    startCell.rowSpan = durationHours;
                }

                // Ocultar las celdas que quedan debajo de la tarea
                for (let i = 1; i < durationHours; i++) {
                    const hourToDelete = startHour + i;
                    const cellToDelete = document.getElementById(`cell-${day}-${hourToDelete}`);
                    if (cellToDelete) {
                        cellToDelete.remove();
                    }
                }

                // Añadir contenido a la celda
                startCell.classList.add('activity-cell', `priority-${task.prioridad.toLowerCase()}`);
                startCell.innerHTML = `
                    <div class="font-semibold">${task.nombre}</div>
                    <div class="text-xs text-secondary">${task.descripcion ? task.descripcion.substring(0, 50) + '...' : ''}</div>
                `;
                // Añadir enlace al detalle de la tarea
                startCell.style.cursor = 'pointer';
                startCell.onclick = () => window.location.href = `/task/${task.id}/`;
            });
        });
    }

    // --- Lógica existente (citas, notificaciones, etc.) ---
    // (Se mantiene la lógica anterior para el modal, citas, etc., pero se simplifica
    // ya que la renderización principal ha cambiado)

    const modal = document.getElementById('editModal');
    
    function closeModal() {
        if(modal) modal.classList.remove('show');
    }

    // Mockup de la función openModal para evitar errores.
    // La edición real debería llevar a la página de edición de la tarea.
    window.openModal = function(timeSlot, day) {
        console.log("Abriendo modal para:", timeSlot, day);
        if(modal) modal.classList.add('show');
        // Aquí se llenaría el modal con datos si fuera necesario
    };

    window.saveActivity = function() {
        console.log("Guardando actividad...");
        closeModal();
    };

    // Lógica de la cita inspiradora
    const quotes = [
        "La disciplina es el puente entre metas y logros.",
        "El dolor de la disciplina pesa onzas, el dolor del arrepentimiento pesa toneladas.",
        "Domina tu mente o tu mente te dominará a ti."
    ];
    const quoteText = document.getElementById('quote-text');
    if (quoteText) {
        quoteText.textContent = `"${quotes[Math.floor(Math.random() * quotes.length)]}"`;
    }

    // Inicialización
    renderSchedule();
});