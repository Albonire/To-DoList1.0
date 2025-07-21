document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.spotlight-container');

    // Solo ejecutar el script si el contenedor del efecto existe en la página.
    if (container) {
        
        // Adjuntar el listener al 'document' para rastrear el cursor en toda la página.
        document.addEventListener('mousemove', e => {
            // Aún necesitamos las dimensiones y posición del contenedor para el cálculo.
            const rect = container.getBoundingClientRect();
            
            // Calculamos la posición del cursor RELATIVA al contenedor.
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Actualizamos las variables CSS en el contenedor.
            // requestAnimationFrame asegura que la animación sea fluida.
            requestAnimationFrame(() => {
                container.style.setProperty('--x', `${x}px`);
                container.style.setProperty('--y', `${y}px`);
            });
        });

        // Opcional: Si el cursor abandona por completo la ventana del navegador,
        // podemos reiniciar el efecto.
        document.addEventListener('mouseleave', () => {
            requestAnimationFrame(() => {
                container.style.setProperty('--x', '50%');
                container.style.setProperty('--y', '50%');
            });
        });
    }
});
