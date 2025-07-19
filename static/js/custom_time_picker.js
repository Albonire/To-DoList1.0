document.addEventListener('DOMContentLoaded', function() {
    // Inicializa Flatpickr en todos los campos con la clase 'time-picker-input'
    flatpickr(".time-picker-input", {
        enableTime: true,    // Habilita la selección de hora
        noCalendar: true,    // Deshabilita el calendario (solo selector de hora)
        dateFormat: "H:i",   // Formato de 24 horas (ej: 14:30)
        time_24hr: true,     // Usa el formato de 24 horas
        minuteIncrement: 15, // Incrementos de 15 minutos
        locale: {
            firstDayOfWeek: 1, // Lunes como primer día de la semana
            weekdays: {
                shorthand: ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"],
                longhand: ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
            },
            months: {
                shorthand: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
                longhand: [
                    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
                    "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
                ],
            },
        }
    });
});
