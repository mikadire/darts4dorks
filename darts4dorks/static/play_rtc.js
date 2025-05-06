document.addEventListener("DOMContentLoaded", () => {
  const targetElement = document.getElementById("target");
  const input = document.getElementById("darts-thrown");
  const form = document.getElementById("dart-form");
  const errorMessage = document.getElementById("error-message");
  const undoButton = document.getElementById("undo-button");

  const resumeModalElement = document.getElementById("resume-modal");
  const resumeYes = document.getElementById("resume-yes");
  const resumeNo = document.getElementById("resume-no");

  const resumeModal = new bootstrap.Modal(resumeModalElement, {
    backdrop: "static",
    keyboard: false,
  });

  let target = 1;
  let attemptsData = [];

  const savedProgress = localStorage.getItem("darts-progress");

  if (savedProgress) {
    resumeModal.show();

    resumeYes.addEventListener("click", () => {
      try {
        const parsed = JSON.parse(savedProgress);
        if (
          typeof parsed.target === "number" &&
          Array.isArray(parsed.attemptsData)
        ) {
          target = parsed.target;
          attemptsData = parsed.attemptsData;
        }
      } catch (e) {
        console.error("Corrupt progress in localStorage:", e);
        localStorage.removeItem("darts-progress");
      }
      resumeModal.hide();
      initializeGame();
    });

    resumeNo.addEventListener("click", () => {
      localStorage.removeItem("darts-progress");
      resumeModal.hide();
      initializeGame();
    });
  } else {
    initializeGame();
  }

  function initializeGame() {
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
  }

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

  function saveProgressToLocalStorage() {
    const progress = {
      target,
      attemptsData,
    };
    localStorage.setItem("darts-progress", JSON.stringify(progress));
  }

  async function endGame() {
    try {
      const data = attemptsData;

      const response = await fetch("/submit_game", {
        method: "POST",
        headers: { "Content-Type": "application/json; charset=utf-8" },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json();
        const errorText =
          errorData.message || JSON.stringify(errorData.errors || errorData);
        throw new Error(
          `Response status: ${response.status}, Error: ${errorText}`
        );
      }

      const result = await response.json();

      if (result.success) {
        localStorage.removeItem("darts-progress");
        window.location.replace(result.url);
      } else {
        undoAttempt();
        errorMessage.textContent = `An error has occurred. Please try again.`;
      }
    } catch (error) {
      undoAttempt();
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

    attemptsData.push(attempt);
    target += 1;
    saveProgressToLocalStorage();

    updateTargetElement();
    input.value = "";
    input.focus();
  }

  function undoAttempt() {
    if (attemptsData.length === 0) return;

    attemptsData.pop();
    target -= 1;

    saveProgressToLocalStorage();

    updateTargetElement();
    errorMessage.textContent = `Try deleted. Please re-enter the number of darts
            thrown at target ${target}.`;
  }
});
