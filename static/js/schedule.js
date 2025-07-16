// --- DATOS Y CONFIGURACIÓN ---
let scheduleData = {
    // Datos iniciales (sin cambios, pero se sobreescribirán si hay datos guardados)
     "05:00-07:00": { Monday: null, Tuesday: { text: "Meditación / Estudio Silencioso", type: "routine", notes: "Preparar el día con calma" }, Wednesday: null, Thursday: null, Friday: null, Saturday: null },
    "07:00-07:30": { Monday: { text: "Rutina Mañana", type: "routine", notes: "" }, Tuesday: { text: "Cálculo Multivariable (FP301)", type: "class", notes: "" }, Wednesday: { text: "Rutina Mañana", type: "routine", notes: "" }, Thursday: { text: "Rutina Mañana", type: "routine", notes: "" }, Friday: { text: "Rutina Mañana", type: "routine", notes: "" }, Saturday: { text: "Camino a U / Rutina", type: "commute", notes: "" } },
    "07:30-08:30": { Monday: { text: "Desayuno Consciente", type: "meal", notes: "" }, Tuesday: { text: "Cálculo Multivariable (FP301)", type: "class", notes: "" }, Wednesday: { text: "Desayuno Consciente", type: "meal", notes: "" }, Thursday: { text: "Desayuno Consciente", type: "meal", notes: "" }, Friday: { text: "Desayuno Consciente", type: "meal", notes: "" }, Saturday: { text: "Bases de Datos II & Cálculo Multi.", type: "class", notes: "" } },
    "08:30-09:00": { Monday: { text: "Camino a U", type: "commute", notes: "" }, Tuesday: { text: "Cálculo Multivariable (FP301)", type: "class", notes: "" }, Wednesday: { text: "Ejercicio: Flexibilidad", type: "workout", notes: "" }, Thursday: { text: "Estudio Inglés", type: "study", notes: "" }, Friday: { text: "Ejercicio: Fuerza", type: "workout", notes: "" }, Saturday: { text: "Bases de Datos II & Cálculo Multi.", type: "class", notes: "" } },
    "09:00-12:00": { Monday: { text: "Desarrollo Plataformas (AULA TIC)", type: "class", notes: "" }, Tuesday: { text: "Estudio Programación Zen", type: "study", notes: "Enfoque profundo" }, Wednesday: { text: "Estructuras Discretas (FJ103-2)", type: "class", notes: "" }, Thursday: { text: "Estudio Programación Zen", type: "study", notes: "" }, Friday: { text: "Estructuras Discretas (FJ103-2)", type: "class", notes: "" }, Saturday: { text: "Bases de Datos II & Cálculo Multi.", type: "class", notes: "" } },
    "12:00-12:30": { Monday: { text: "Regreso & Podcast", type: "commute", notes: "" }, Tuesday: { text: "Estudio Japonés (Kanji)", type: "study", notes: "Practicar trazos" }, Wednesday: { text: "Regreso & Podcast", type: "commute", notes: "" }, Thursday: { text: "Estudio Japonés (Kanji)", type: "study", notes: "" }, Friday: { text: "Regreso & Podcast", type: "commute", notes: "" }, Saturday: { text: "Regreso & Podcast", type: "commute", notes: "" } },
    "12:30-13:00": { Monday: { text: "Estudio Japonés", type: "study", notes: "" }, Tuesday: { text: "Estudio Inglés", type: "study", notes: "" }, Wednesday: { text: "Estudio Inglés", type: "study", notes: "" }, Thursday: { text: "Tareas PhD", type: "study", notes: "" }, Friday: { text: "Estudio Programación", type: "study", notes: "" }, Saturday: { text: "Electromagnetismo (EC 111)", type: "class", notes: "" } },
    "13:00-14:00": { Monday: { text: "Almuerzo", type: "meal", notes: "" }, Tuesday: { text: "Almuerzo", type: "meal", notes: "" }, Wednesday: { text: "Almuerzo", type: "meal", notes: "" }, Thursday: { text: "Almuerzo", type: "meal", notes: "" }, Friday: { text: "Almuerzo", type: "meal", notes: "" }, Saturday: { text: "Almuerzo", type: "meal", notes: "" } },
    "14:00-15:30": { Monday: { text: "Programación Deep Work", type: "study", notes: "" }, Tuesday: { text: "Programación Deep Work", type: "study", notes: "" }, Wednesday: { text: "Programación Deep Work", type: "study", notes: "" }, Thursday: { text: "Ing. Software (FJ103-2)", type: "class", notes: "" }, Friday: { text: "Desarrollo Plataformas (AULA TIC)", type: "class", notes: "" }, Saturday: { text: "Estudio Inglés", type: "study", notes: "" } },
    "15:30-16:30": { Monday: { text: "Programación Deep Work", type: "study", notes: "" }, Tuesday: { text: "Repaso Cálculo Multi.", type: "review", notes: "" }, Wednesday: { text: "Repaso Electromagnetismo", type: "review", notes: "" }, Thursday: { text: "Ing. Software (FJ103-2)", type: "class", notes: "" }, Friday: { text: "Desarrollo Plataformas (AULA TIC)", type: "class", notes: "" }, Saturday: { text: "Estudio Japonés", type: "study", notes: "" } },
    "16:30-17:30": { Monday: { text: "Pausa Activa / Té", type: "break", notes: "Momento de calma" }, Tuesday: { text: "Ing. Software (FJ103-2)", type: "class", notes: "" }, Wednesday: { text: "Abierto (Flexible)", type: "open", notes: "" }, Thursday: { text: "Pausa Activa / Caminar", type: "break", notes: "" }, Friday: { text: "Abierto (Flexible)", type: "open", notes: "" }, Saturday: { text: "Socializar / Relax", type: "social", notes: "" } },
    "17:30-18:30": { Monday: { text: "Electromagnetismo (106)", type: "class", notes: "" }, Tuesday: { text: "Ing. Software (FJ103-2)", type: "class", notes: "" }, Wednesday: { text: "Japonés Gramática/Escucha", type: "study", notes: "" }, Thursday: { text: "Japonés Gramática/Escucha", type: "study", notes: "" }, Friday: { text: "Estudio Japonés", type: "study", notes: "" }, Saturday: { text: "Lectura Ligera", type: "break", notes: "" } },
    "18:30-19:30": { Monday: { text: "Electromagnetismo (106)", type: "class", notes: "" }, Tuesday: { text: "Ing. Software (FJ103-2)", type: "class", notes: "" }, Wednesday: { text: "Bases de Datos II (ME 108)", type: "class", notes: "" }, Thursday: { text: "Repaso Electromagnetismo", type: "review", notes: "" }, Friday: { text: "Electromagnetismo (EC 111)", type: "class", notes: "" }, Saturday: { text: "Repaso Electromagnetismo", type: "review", notes: "" } },
    "19:30-20:30": { Monday: { text: "Electromagnetismo (106)", type: "class", notes: "" }, Tuesday: { text: "Cena", type: "meal", notes: "" }, Wednesday: { text: "Bases de Datos II (MF 108)", type: "class", notes: "" }, Thursday: { text: "Cena", type: "meal", notes: "" }, Friday: { text: "Electromagnetismo (EC 111)", type: "class", notes: "" }, Saturday: { text: "Estudio Programación", type: "study", notes: "" } },
    "20:30-21:30": { Monday: { text: "Estudio Inglés & Cena", type: "study", notes: "" }, Tuesday: { text: "Repaso Bases Datos", type: "review", notes: "" }, Wednesday: { text: "Cena", type: "meal", notes: "" }, Thursday: { text: "Repaso Des. Plataformas", type: "review", notes: "" }, Friday: { text: "Electromagnetismo (EC 111)", type: "class", notes: "" }, Saturday: { text: "Repaso Estructuras Discretas", type: "review", notes: "" } },
    "21:30-22:00": { Monday: { text: "Repaso Ing. Software", type: "review", notes: "" }, Tuesday: { text: "Repaso Estructuras Discretas", type: "review", notes: "" }, Wednesday: { text: "Repaso Electro/Cálculo Multi.", type: "review", notes: "" }, Thursday: { text: "Repaso Ing. Software", type: "review", notes: "" }, Friday: { text: "Estudio Inglés", type: "study", notes: "" }, Saturday: { text: "Repaso Ing. Software", type: "review", notes: "" } },
    "22:00-23:00": { Monday: { text: "Desconectar / Preparar cama", type: "routine", notes: "Sin pantallas" }, Tuesday: { text: "Desconectar / Preparar cama", type: "routine", notes: "" }, Wednesday: { text: "Desconectar / Preparar cama", type: "routine", notes: "" }, Thursday: { text: "Desconectar / Preparar cama", type: "routine", notes: "" }, Friday: { text: "Desconectar / Preparar cama", type: "routine", notes: "" }, Saturday: { text: "Desconectar / Preparar cama", type: "routine", notes: "" } },
};

const quotes = [ // Manteniendo citas fuertes pero con enfoque en disciplina
    "La disciplina es el puente entre metas y logros. Cruza ese puente cada día.",
    "El dolor de la disciplina pesa onzas, el dolor del arrepentimiento pesa toneladas.",
    "No esperes la motivación, cultiva la disciplina. La motivación es fugaz, la disciplina es constante.",
    "El bambú que se dobla es más fuerte que el roble que resiste. Sé flexible pero firme en tu propósito.", // Toque cultural
    "Un viaje de mil millas comienza con un solo paso. Da ese paso hoy, y cada día.", // Clásico chino
    "El éxito no es la ausencia de fracaso; es la persistencia a través del fracaso.",
    "Domina tu mente o tu mente te dominará a ti.",
    "El mejor momento para plantar un árbol fue hace 20 años. El segundo mejor momento es ahora." // Proverbio chino
];

// Estilos de actividad - Mapeo a variables CSS (el nombre sigue igual)
// Los iconos y nombres se mantienen, las clases CSS aplicarán los colores de las variables
const activityStyles = {
    class: { name: "Clase", class: 'activity-class', icon: 'fa-solid fa-chalkboard-user' },
    study: { name: "Estudio", class: 'activity-study', icon: 'fa-solid fa-book-open-reader' },
    workout: { name: "Ejercicio", class: 'activity-workout', icon: 'fa-solid fa-dumbbell' },
    meal: { name: "Comida", class: 'activity-meal', icon: 'fa-solid fa-utensils' },
    routine: { name: "Rutina", class: 'activity-routine', icon: 'fa-solid fa-clock' },
    commute: { name: "Transporte", class: 'activity-commute', icon: 'fa-solid fa-bus-simple' },
    break: { name: "Descanso", class: 'activity-break', icon: 'fa-solid fa-mug-saucer' }, // Ícono de taza de té/café
    social: { name: "Social", class: 'activity-social', icon: 'fa-solid fa-users' },
    review: { name: "Repaso", class: 'activity-review', icon: 'fa-solid fa-clipboard-check' },
    open: { name: "Abierto", class: 'activity-open', icon: 'fa-regular fa-hourglass-half' },
    other: { name: "Otro", class: 'activity-other', icon: 'fa-regular fa-circle-question' }
};

// Variables globales
const scheduleBody = document.getElementById('schedule-body');
const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const modal = document.getElementById('editModal');
const modalTypeSelect = document.getElementById('modal-activity-type');
let notificationPermission = Notification.permission;
let lastNotifiedSlot = null;
const storageKey = 'miHorarioZenData'; // Clave para localStorage

// --- FUNCIONES ---

function populateModalTypeSelect() { /* Sin cambios */
    modalTypeSelect.innerHTML = '';
    for (const typeKey in activityStyles) {
        const option = document.createElement('option');
        option.value = typeKey;
        option.textContent = activityStyles[typeKey].name;
        modalTypeSelect.appendChild(option);
    }
}

function renderSchedule() {
    scheduleBody.innerHTML = '';
     const timeSlots = Object.keys(scheduleData).sort((a, b) => {
         const hourA = parseInt(a.split(':')[0]);
         const hourB = parseInt(b.split(':')[0]);
         return hourA - hourB;
     });

    timeSlots.forEach(timeSlot => {
        const row = scheduleBody.insertRow();
        row.setAttribute('data-time-slot', timeSlot);

        const timeCell = row.insertCell();
        timeCell.textContent = timeSlot;
        timeCell.classList.add('font-medium', 'text-xs'); // Ajuste visual

        days.forEach((day, dayIndex) => {
            const cell = row.insertCell();
            const activity = scheduleData[timeSlot]?.[day];
            cell.setAttribute('data-day-index', dayIndex);
            cell.setAttribute('data-time-slot', timeSlot);
            cell.setAttribute('data-day', day);
            cell.classList.add('border'); // Asegurar borde básico

            if (activity) {
                const style = activityStyles[activity.type] || activityStyles.other;
                cell.classList.add(style.class, 'p-2', 'text-xs'); // Aplicar clase de estilo
                cell.innerHTML = `<i class="icon ${style.icon}"></i>${activity.text}`;
                if (activity.notes && activity.notes.trim() !== "") {
                    const noteIndicator = document.createElement('div');
                    noteIndicator.classList.add('note-indicator');
                    noteIndicator.title = "Esta actividad tiene notas";
                    cell.appendChild(noteIndicator);
                }
                cell.onclick = () => openModal(timeSlot, day);
                cell.setAttribute('aria-label', `Actividad: ${activity.text} (${activityStyles[activity.type].name}) el ${day} de ${timeSlot}. Haz clic para editar.`);
            } else {
                cell.classList.add(activityStyles.open.class, 'p-2'); // Espacio abierto
                cell.innerHTML = '<i class="fa-solid fa-plus text-gray-400 opacity-50"></i>'; // Icono más tenue
                cell.onclick = () => openModal(timeSlot, day, true);
                 cell.setAttribute('aria-label', `Bloque libre el ${day} de ${timeSlot}. Haz clic para añadir actividad.`);
            }
        });
    });
    updateCurrentTimeIndicator();
}

function openModal(timeSlot, day, isNew = false) { /* Sin cambios funcionales */
    const activity = scheduleData[timeSlot]?.[day];
    document.getElementById('modal-time-slot').value = timeSlot;
    document.getElementById('modal-day').value = day;
    const modalTitle = document.getElementById('modal-title'); // ARIA necesita que el título esté presente

    if (isNew || !activity) {
        modalTitle.textContent = `Añadir Actividad (${day} ${timeSlot})`;
        document.getElementById('modal-activity-text').value = '';
        document.getElementById('modal-activity-type').value = 'other'; // Por defecto 'Otro'
        document.getElementById('modal-activity-notes').value = '';
    } else {
        modalTitle.textContent = `Editar Actividad (${day} ${timeSlot})`;
        document.getElementById('modal-activity-text').value = activity.text;
        document.getElementById('modal-activity-type').value = activity.type;
        document.getElementById('modal-activity-notes').value = activity.notes || '';
    }
    modal.style.display = "block";
    // Enfocar el primer campo del modal
    document.getElementById('modal-activity-text').focus();
}

function closeModal() { /* Sin cambios */
    modal.style.display = "none";
}

// Guardar cambios y persistir en localStorage
function saveActivity() {
    const timeSlot = document.getElementById('modal-time-slot').value;
    const day = document.getElementById('modal-day').value;
    const newText = document.getElementById('modal-activity-text').value.trim();
    const newType = document.getElementById('modal-activity-type').value;
    const newNotes = document.getElementById('modal-activity-notes').value.trim();

    if (!timeSlot || !day) return; // Validación básica

    // Asegurarse que el slot existe en la estructura principal
    if (!scheduleData[timeSlot]) {
        scheduleData[timeSlot] = {};
    }

    if (newText === "") {
        // Si se borra el texto, se elimina la actividad para ese día/hora
        scheduleData[timeSlot][day] = null;
         console.log(`Actividad eliminada para ${day} ${timeSlot}`);
    } else {
        // Crear o actualizar la actividad
         scheduleData[timeSlot][day] = {
             text: newText,
             type: newType,
             notes: newNotes
         };
         console.log(`Actividad guardada para ${day} ${timeSlot}:`, scheduleData[timeSlot][day]);
    }

    closeModal(); // Cerrar el modal

    // PERSISTENCIA: Guardar todo el objeto scheduleData en localStorage
    try {
        localStorage.setItem(storageKey, JSON.stringify(scheduleData));
        console.log("Horario guardado en localStorage.");
    } catch (e) {
        console.error("Error al guardar en localStorage:", e);
        alert("Hubo un error al guardar los cambios. Es posible que el almacenamiento esté lleno o deshabilitado.");
    }

    renderSchedule(); // Volver a renderizar la tabla con los cambios
}

function parseTimeSlot(timeSlot) { /* Sin cambios */
     const parts = timeSlot.split('-');
    if (parts.length !== 2) return null;
    const [startStr, endStr] = parts;
    const startParts = startStr.split(':');
    const endParts = endStr.split(':');
    if (startParts.length !== 2 || endParts.length !== 2) return null;
    const startHour = parseInt(startParts[0], 10);
    const startMinute = parseInt(startParts[1], 10);
    const endHour = parseInt(endParts[0], 10);
    const endMinute = parseInt(endParts[1], 10);
     if (isNaN(startHour) || isNaN(startMinute) || isNaN(endHour) || isNaN(endMinute)) return null;
    return { startHour, startMinute, endHour, endMinute };
}

function updateCurrentTimeIndicator() { /* Lógica sin cambios, estilos actualizados por CSS */
     const now = new Date();
    const currentHour = now.getHours();
    const currentMinute = now.getMinutes();
     // getDay() da 0 para Domingo, 1 para Lunes... Necesitamos 0 para Lunes... 5 para Sábado
    const currentDayIndex = (now.getDay() + 6) % 7; // Lunes=0, Martes=1 ... Sábado=5, Domingo=6

    document.querySelectorAll('.current-time-slot').forEach(cell => {
        cell.classList.remove('current-time-slot');
        cell.style.transform = '';
        const indicator = cell.querySelector('.current-time-indicator');
        if (indicator) indicator.remove();
    });

     // No mostrar indicador los domingos (índice 6)
     if (currentDayIndex > 5) return; // Mayor que 5 significa Domingo

    let currentActivity = null;
    let currentSlotIdentifier = null;
    const rows = scheduleBody.querySelectorAll('tr');

    rows.forEach(row => {
        const timeSlot = row.getAttribute('data-time-slot');
        if (!timeSlot) return;
        const parsedTime = parseTimeSlot(timeSlot);
        if (!parsedTime) return;

        const { startHour, startMinute, endHour, endMinute } = parsedTime;
        const slotStartMinutes = startHour * 60 + startMinute;
         // El final del slot es exclusivo (ej. 09:00-12:00 termina a las 11:59:59)
         let slotEndMinutes = endHour * 60 + endMinute;
         // Si el slot termina a las XX:00, el final real es ese minuto exacto.
         // Si es 09:00-12:00 (ends at 12:00), nowMinutes must be < 720.
         // Si es 07:00-07:30 (ends at 07:30), nowMinutes must be < 450.

        const nowMinutes = currentHour * 60 + currentMinute;

         if (nowMinutes >= slotStartMinutes && nowMinutes < slotEndMinutes) {
            const currentCell = row.querySelector(`td[data-day-index="${currentDayIndex}"]`);
            const timeCell = row.querySelector('td:first-child');
            currentSlotIdentifier = `${timeSlot}-${days[currentDayIndex]}`; // Identificador único para notificación

            if (currentCell) {
                currentCell.classList.add('current-time-slot');
                const slotDuration = slotEndMinutes - slotStartMinutes;
                 // Asegurarse de que duration no es 0 para evitar división por cero
                const percentageThroughSlot = slotDuration > 0 ? Math.max(0, Math.min(100, ((nowMinutes - slotStartMinutes) / slotDuration) * 100)) : 0;

                const indicatorLine = document.createElement('div');
                indicatorLine.classList.add('current-time-indicator');
                indicatorLine.style.top = `${percentageThroughSlot}%`;
                currentCell.appendChild(indicatorLine);

                currentActivity = scheduleData[timeSlot]?.[days[currentDayIndex]];
            }
            if (timeCell) {
                timeCell.classList.add('current-time-slot'); // Resaltar también la celda de hora
            }
        }
    });

    // Enviar notificación si la actividad actual es nueva y tenemos permiso
    if (currentActivity && notificationPermission === 'granted' && currentSlotIdentifier !== lastNotifiedSlot) {
        sendNotification(`Ahora: ${currentActivity.text}`, currentActivity.notes || "Es hora de comenzar.");
        lastNotifiedSlot = currentSlotIdentifier; // Marcar como notificado
    } else if (!currentActivity) {
         lastNotifiedSlot = null; // Resetear si no hay actividad actual (espacio libre)
    }
}

function displayRandomQuote() { /* Sin cambios */
     const quoteText = document.getElementById('quote-text');
    if (quoteText && quotes.length > 0) {
        const randomIndex = Math.floor(Math.random() * quotes.length);
        quoteText.textContent = `"${quotes[randomIndex]}"`;
    } else if (quoteText) {
        quoteText.textContent = "La disciplina es la clave del éxito."; // Mensaje por defecto
    }
}

function requestNotificationPermission() { /* Sin cambios funcionales */
    const statusElem = document.getElementById('notification-status');
    if (!("Notification" in window)) {
        statusElem.textContent = "Este navegador no soporta notificaciones.";
        return;
    }
    Notification.requestPermission().then(permission => {
        notificationPermission = permission; // Actualizar estado global
        if (permission === "granted") {
            statusElem.textContent = "¡Notificaciones habilitadas!";
            sendNotification("Permiso concedido", "Recibirás recordatorios de tus actividades.");
        } else if (permission === "denied") {
            statusElem.textContent = "Notificaciones bloqueadas. Revisa la configuración del navegador.";
        } else {
            statusElem.textContent = "Permiso de notificación no concedido.";
        }
         updateNotificationButtonStatus(); // Actualizar estado visual
    });
}

 function sendNotification(title, body = "") { /* Sin cambios */
     if (notificationPermission !== 'granted') return;
     const options = {
         body: body || "Es hora de empezar esta actividad.",
         icon: './icon.png' // Opcional: Añadir un icono (asegúrate que exista)
     };
     try {
         new Notification(title, options);
     } catch (error) {
         console.error("Error al enviar notificación:", error);
     }
 }

 function updateNotificationButtonStatus() { /* Lógica sin cambios */
     const statusElem = document.getElementById('notification-status');
     const button = document.getElementById('enable-notifications');
     if (!("Notification" in window)) {
         button.disabled = true;
         statusElem.textContent = "Notificaciones no soportadas.";
         return;
     }

     if (notificationPermission === 'granted') {
         statusElem.textContent = "Notificaciones habilitadas.";
         button.style.opacity = '0.7'; // Indicar que ya está activo
     } else if (notificationPermission === 'denied') {
         statusElem.textContent = "Notificaciones bloqueadas por el navegador.";
         button.disabled = true; // Deshabilitar si está bloqueado
         button.style.opacity = '0.5';
     } else {
         statusElem.textContent = "Haz clic para habilitar recordatorios.";
         button.disabled = false;
         button.style.opacity = '1';
     }
 }

// --- INICIALIZACIÓN ---
document.addEventListener('DOMContentLoaded', () => {
    // PERSISTENCIA: Cargar datos de localStorage al iniciar
    const savedData = localStorage.getItem(storageKey);
    if (savedData) {
        try {
            const parsedData = JSON.parse(savedData);
            // Validar si es un objeto antes de asignarlo
            if (parsedData && typeof parsedData === 'object') {
                 scheduleData = parsedData;
                 console.log("Horario cargado desde localStorage.");
            } else {
                 console.warn("Datos guardados en localStorage no son válidos, usando datos por defecto.");
            }
        } catch (e) {
            console.error("Error al parsear datos de localStorage:", e);
            // Opcional: borrar datos corruptos localStorage.removeItem(storageKey);
            alert("Hubo un error al cargar los datos guardados. Se usará el horario por defecto.");
        }
    } else {
         console.log("No se encontraron datos guardados, usando horario por defecto.");
    }


    populateModalTypeSelect(); // Llenar el <select> del modal
    renderSchedule();          // Dibujar la tabla inicial
    updateCurrentTimeIndicator(); // Marcar la hora actual
    displayRandomQuote();      // Mostrar una cita
    updateNotificationButtonStatus(); // Poner estado del botón de notificaciones

    document.getElementById('enable-notifications').addEventListener('click', requestNotificationPermission);

    // Actualizar indicador de hora cada 30 segundos
    setInterval(updateCurrentTimeIndicator, 30000);

    // Cerrar modal al hacer clic fuera de él
    window.onclick = function(event) {
        if (event.target == modal) {
            closeModal();
        }
    }

    // Cerrar modal con la tecla Escape
     window.addEventListener('keydown', function(event) {
         if (event.key === 'Escape' && modal.style.display === "block") {
             closeModal();
         }
     });
});
