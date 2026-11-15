
document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("game-form");

    if (!form) return;

    const screens = Array.from(
        document.querySelectorAll(".question-screen")
    );

    if (!screens.length) return;

    const previousBtn = document.getElementById("previous-btn");
    const nextBtn = document.getElementById("next-btn");
    const submitBtn = document.getElementById("submit-btn");

    const progressText = document.getElementById("progress-text");
    const progressFill = document.getElementById("progress-fill");
    const answeredCount = document.getElementById("answered-count");
    const timerDisplay = document.getElementById("game-timer");

    let currentQuestion = 0;
    let submitted = false;

    // TIMER SETTINGS
    const duration = 600;

    // Django template मधून game सुरू झाल्याची वेळ (milliseconds)
    const startedAt = Number(GAME_STARTED_AT);

    function updateAnsweredCount() {

        let answered = 0;

        screens.forEach(screen => {

            const selected = screen.querySelector(
                'input[type="radio"]:checked'
            );

            if (selected) answered++;

        });

        answeredCount.textContent =
            `${answered} / ${screens.length} Answered`;
    }

    // QUESTION NAVIGATION
    function showQuestion(index) {

        currentQuestion = index;

        screens.forEach((screen, i) => {
            screen.classList.toggle("active", i === index);
        });

        progressText.textContent =
            `QUESTION ${index + 1} / ${screens.length}`;

        progressFill.style.width =
            `${((index + 1) / screens.length) * 100}%`;

        previousBtn.style.display =
            index === 0 ? "none" : "inline-block";

        nextBtn.style.display =
            index === screens.length - 1 ? "none" : "inline-block";

        submitBtn.style.display =
            index === screens.length - 1 ? "inline-block" : "none";

        updateAnsweredCount();

    }

    // PREVIOUS QUESTION
    previousBtn.addEventListener("click", function () {

        if (currentQuestion > 0) {
            showQuestion(currentQuestion - 1);
        }

    });

    // NEXT QUESTION
    nextBtn.addEventListener("click", function () {

        if (currentQuestion < screens.length - 1) {
            showQuestion(currentQuestion + 1);
        }

    });

    // ANSWER COUNT
    form.addEventListener("change", updateAnsweredCount);

    // TIMER
    function updateTimer() {

        if (!Number.isFinite(startedAt) || startedAt <= 0) {
            timerDisplay.textContent = "--:--";
            return;
        }

        const currentTime = Date.now();

        const elapsed = Math.floor(
            (currentTime - startedAt) / 1000
        );

        const timeLeft = Math.max(0, duration - elapsed);

        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;

        timerDisplay.textContent =
            `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

        if (timeLeft <= 60) {
            timerDisplay.style.color = "#dc2626";
        }

        if (timeLeft <= 0 && !submitted) {

            submitted = true;

            // Timer संपल्यावर confirmation न विचारता submit
            form.submit();

        }

    }

    // SUBMIT CONFIRMATION
    form.addEventListener("submit", function (event) {

        if (submitted) return;

        const confirmed = window.confirm(
            "Are you sure you want to submit your challenge?"
        );

        if (!confirmed) {

            event.preventDefault();

        } else {

            submitted = true;

        }

    });

    // INITIALIZE GAME
    showQuestion(0);

    updateTimer();

    setInterval(updateTimer, 1000);

});
