document.addEventListener('DOMContentLoaded', () => {
    const taskCards = document.querySelectorAll('.task-card');

    taskCards.forEach(card => {
        // Add a cursor pointer to the whole card to indicate it's clickable
        card.style.cursor = 'pointer';

        card.addEventListener('click', (event) => {
            // Do not navigate if the click was on an interactive element like the completion form, a priority badge, or any other link.
            if (event.target.closest('.task-complete-form, .task-priority, a')) {
                return;
            }

            const detailLink = card.querySelector('.task-title a');
            if (detailLink && detailLink.href) {
                window.location.href = detailLink.href;
            }
        });
    });
});
