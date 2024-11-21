document.addEventListener('DOMContentLoaded', () => {
    const targetElement = document.getElementById('target');
    const input = document.getElementById('darts-thrown');
    const button = document.getElementById('submit-button');
    const errorMessage = document.getElementById('error-message');

    button.addEventListener('click', submitData);

    async function submitData() {
        errorMessage.textContent = '';

        const dartsThrown = parseInt(input.value);
        if (isNaN(dartsThrown) || dartsThrown < 1) {
            errorMessage.textContent = 'How did you manage that? Most people need \
            1 or more darts to hit their target.';
            return;
        };

        target = parseInt(targetElement.textContent);
        const data = {
            session_id: sessionID,
            target: target,
            darts_thrown: dartsThrown
        };

        try{
            const response = await fetch('/attempt', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json; charset=utf-8' },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`Response status: ${response.status}, 
                    Error: ${respone.message}`);
            };

            const newTarget = target + 1;
            targetElement.textContent = newTarget;
            input.value = '';

        } catch (error) {
            console.error(error.message);
        }
    };
})