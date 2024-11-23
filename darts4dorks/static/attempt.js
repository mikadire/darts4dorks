document.addEventListener('DOMContentLoaded', () => {
    const targetElement = document.getElementById('target');
    const input = document.getElementById('darts-thrown');
    const form = document.getElementById('dart-form');
    const errorMessage = document.getElementById('error-message');
    let target = startTarget;

    input.focus();

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        submitData();
    });

    async function submitData() {
        errorMessage.textContent = '';

        const dartsThrown = parseInt(input.value);

        if (isNaN(dartsThrown) || dartsThrown < 1) {
            errorMessage.textContent = 'How did you manage that? Most people need \
            1 or more darts to hit their target.';
            return;
        };

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

        } catch (error) {
            console.error(error.message);
        }

        target += 1;

        if (target === 22) {
            console.log('Game Over');
            endGame();
        } else if (target === 21) {
            targetElement.textContent = 'Bull';
        } else {
            targetElement.textContent = target;
        };

        input.value = '';
        input.focus();
    };

    async function endGame() {
        try{
            const response = await fetch('/redirect_game_over', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json; charset=utf-8' },
                body: JSON.stringify({session_id: sessionID})
            });

            if (!response.ok) {
                throw new Error(`Response status: ${response.status}, 
                    Error: ${respone.message}`);
            };
            
            const result = await response.json();
            if (result.redirected) {
                window.location.replace(result.url);
            };

        } catch (error) {
            console.error(error.message);
        }
    }
})