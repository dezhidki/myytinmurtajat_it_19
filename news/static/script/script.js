const Swap = Swappable.default;

function scrollToElement(element, duration, callback) {
    let rect = element.getBoundingClientRect();
    let start = document.documentElement.scrollTop,
        change = rect.y - rect.height,
        currentTime = 0,
        increment = 20;

    let animateScroll = () => {
        currentTime += increment;
        document.documentElement.scrollTop = easeInOutQuad(currentTime, start, change, duration);
        if (currentTime < duration) {
            setTimeout(animateScroll, increment);
        } else if (callback)
            callback();
    };
    animateScroll();
}

function easeInOutQuad(t, b, c, d) {
    t /= d / 2;
    if (t < 1) return c / 2 * t * t + b;
    t--;
    return -c / 2 * (t * (t - 2) - 1) + b;
};

async function checkSolution(currentSolutions) {
    let status = await fetch("/check", {
        method: "POST",
        body: JSON.stringify({
            solutions: currentSolutions
        }),
        headers: {
            "Content-Type": "application/json"
        }
    });

    let solutionResult = await status.json();

    if (solutionResult.correct) {
        scrollToElement(document.getElementById("comments"), 1000, () => {
            let currentComments = document.getElementById("current-comments");
            currentComments.innerHTML = `${solutionResult.renderContent}${currentComments.innerHTML}`;
        });
    }
}

window.onload = () => {
    const swappables = document.querySelectorAll("span.swap-year");
    const swappable = new Swap(swappables, {
        draggable: "span"
    });

    swappable.on("swappable:start", () => {
        swappables.forEach(s => {
            s.classList.add("swappable-place");
        });
    });
    swappable.on("swappable:stop", () => {
        swappables.forEach(s => {
            s.classList.remove("swappable-place");
        });

        const currentSolutions = document.querySelectorAll("span.swap-year span");
        let solutions = [];
        currentSolutions.forEach(v => {
            if (v.classList.length != 0 && !v.classList.contains("draggable-source--is-dragging"))
                return;
            solutions.push(v.textContent);
        });
        checkSolution(solutions);
    });
};