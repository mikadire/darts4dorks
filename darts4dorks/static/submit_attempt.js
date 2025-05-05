document.addEventListener("DOMContentLoaded", () => {
  const targetElement = document.getElementById("target");
  const input = document.getElementById("darts-thrown");
  const form = document.getElementById("dart-form");
  const errorMessage = document.getElementById("error-message");
  const undoButton = document.getElementById("undo-button");
  let target = startTarget;
  let throwsData = [];

  updateTargetElement();
  input.focus();

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    addAttempt();
  });

  undoButton.addEventListener("click", (event) => {
    event.preventDefault();
    undoAttempt();
  });

  function updateTargetElement() {
    if (target === 22) {
      endGame();
    } else if (target === 21) {
      targetElement.textContent = "Bull";
    } else {
      targetElement.textContent = target;
    }
    undoButton.disabled = target <= 1;
  }

  async function endGame() {
    try {
      const data = { session_id: sessionID, throws_data: throwsData };

      const response = await fetch("/submit_game", {
        method: "POST",
        headers: { "Content-Type": "application/json; charset=utf-8" },
        body: JSON.stringify(data),
      });

      if (!response.success) {
        const errorData = await response.json();
        throw new Error(`Response status: ${response.status}, 
                    Error: ${errorData.message}`);
      }

      const result = await response.json();
      if (result.success) {
        window.location.replace(result.url);
      }
    } catch (error) {
      console.error(error.message);
      errorMessage.textContent = `An error has occurred. Please try again.`;
    }
  }

  function addAttempt() {
    errorMessage.textContent = "";

    const dartsThrown = parseInt(input.value);

    if (isNaN(dartsThrown) || dartsThrown < 1) {
      errorMessage.textContent = `How did you manage that? Most people need
            1 or more darts to hit their target.`;
      return;
    }

    const attempt = {
      target: target,
      darts_thrown: dartsThrown,
    };

    throwsData.push(attempt);

    // Testing
    console.log(throwsData);
    // Testing

    target += 1;
    updateTargetElement();
    input.value = "";
    input.focus();
  }

  function undoAttempt() {
    // Removes last attempt
    throwsData.pop();

    // Testing
    console.log(throwsData);
    // Testing

    target -= 1;
    updateTargetElement;
    errorMessage.textContent = `Try deleted. Please re-enter the number of darts
            thrown at target ${target}.`;
  }
});
