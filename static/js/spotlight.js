document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.spotlight-container');

    if (container) {
        container.addEventListener('mousemove', e => {
            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Usamos requestAnimationFrame para un rendimiento más suave
            requestAnimationFrame(() => {
                container.style.setProperty('--x', `${x}px`);
                container.style.setProperty('--y', `${y}px`);
            });
        });
    }
});