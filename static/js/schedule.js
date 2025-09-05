document.addEventListener('DOMContentLoaded', function() {
    const scheduleBody = document.getElementById('schedule-body');
    const tasksDataElement = document.getElementById('tasks-data');
    
    if (!scheduleBody || !tasksDataElement) {
        console.error("Elementos del horario no encontrados.");
        return;
    }

    const tasks = JSON.parse(tasksDataElement.textContent);
    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

    function renderSchedule() {
        // Determine the hour range dynamically based on tasks
        let hourStart = 5; // Default start time if no tasks exist
        let hourEnd = 22;  // Default end time if no tasks exist

        if (tasks.length > 0) {
            let minHour = 24;
            let maxHour = -1;

            tasks.forEach(task => {
                if (task.hora_inicio) {
                    const [startHour] = task.hora_inicio.split(':').map(Number);
                    const durationHours = Math.ceil(task.duracion_minutos / 60);
                    // The last hour slot a task occupies determines the grid's end
                    const endHourOfTask = startHour + durationHours - 1;

                    if (startHour < minHour) {
                        minHour = startHour;
                    }
                    if (endHourOfTask > maxHour) {
                        maxHour = endHourOfTask;
                    }
                }
            });

            // If tasks with valid times were found, update the schedule's range
            if (minHour <= 23) {
                // Add a 1-hour buffer for better spacing and clamp values to a 24-hour day (0-23)
                hourStart = Math.max(0, minHour - 1);
                hourEnd = Math.min(23, maxHour + 1);
            }
        }

        // 1. Clean the existing grid and create the new dynamic one
        scheduleBody.innerHTML = '';
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

                if (day === "Saturday" || day === "Sunday") {
                    cell.classList.add('weekend-col');
                }
            });
        }

        // 2. Place the tasks onto the newly created grid
        tasks.forEach(task => {
            if (!task.hora_inicio || !task.dia_semana || !Array.isArray(task.dia_semana)) {
                return; // Ignore tasks with incomplete data
            }

            const [startHour] = task.hora_inicio.split(':').map(Number);

            // This check ensures we only try to place tasks that fit within our dynamic grid.
            if (startHour < hourStart || startHour > hourEnd) {
                console.warn(`Task "${task.nombre}" at ${startHour}:00 is outside the generated schedule view and will not be displayed.`);
                return;
            }

            task.dia_semana.forEach(day => {
                const startCell = document.getElementById(`cell-${day}-${startHour}`);
                if (!startCell) return;

                const durationHours = Math.ceil(task.duracion_minutos / 60);
                
                // Ensure a task's duration doesn't visually extend beyond the created grid
                const effectiveDuration = Math.min(durationHours, hourEnd - startHour + 1);
                if (effectiveDuration > 1) {
                    startCell.rowSpan = effectiveDuration;
                }

                // Hide the cells that are now covered by the multi-hour task
                for (let i = 1; i < effectiveDuration; i++) {
                    const hourToDelete = startHour + i;
                    const cellToDelete = document.getElementById(`cell-${day}-${hourToDelete}`);
                    if (cellToDelete) {
                        cellToDelete.remove();
                    }
                }

                if (startCell.classList.contains('weekend-col')) {
                    startCell.classList.remove('weekend-col');
                }

                startCell.classList.add('activity-cell', `priority-${task.prioridad.toLowerCase()}`);
                startCell.innerHTML = `
                    <div class="font-semibold">${task.nombre}</div>
                    <div class="text-xs text-secondary">${task.descripcion ? task.descripcion.substring(0, 50) + '...' : ''}</div>
                `;
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