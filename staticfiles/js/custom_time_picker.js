document.addEventListener('DOMContentLoaded', function() {
    flatpickr(".time-picker-input", {
        enableTime: true,    // Enable time selection
        noCalendar: true,    // Disable calendar
        dateFormat: "H:i",   // F24h format (ej: 14:30)
        time_24hr: true,     
        minuteIncrement: 15, 
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
