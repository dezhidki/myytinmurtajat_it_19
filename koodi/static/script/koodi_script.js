//#region Matrix Background effect
let matrixCanvas = null;
let ctx = null;
let cols = null;

const fps = 20;
const waitMs = 1000 / fps;
let start = null;
function matrix(timeStamp) {
    if (start && timeStamp - start < waitMs) {
        window.requestAnimationFrame(matrix);
        return;
    }
    start = timeStamp;

    ctx.fillStyle = "#0001";
    ctx.fillRect(0, 0, matrixCanvas.width, matrixCanvas.height);

    ctx.fillStyle = "#060";
    ctx.font = "15pt monospace";

    for (let i = 0; i < cols.length; i++) {
        const y = cols[i];

        ctx.fillText(String.fromCharCode(Math.random() * 1024), i * 20, y);
        cols[i] = y > 100 + Math.random() * window.outerHeight * 10 ? 0 : y + 20;
    }

    window.requestAnimationFrame(matrix);
}

function startBgEffect() {
    matrixCanvas = document.getElementById("bg-effect");
    ctx = matrixCanvas.getContext("2d");

    matrixCanvas.width = window.innerWidth;
    matrixCanvas.height = window.innerHeight;

    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, matrixCanvas.width, matrixCanvas.width);
    cols = Array(Math.floor(matrixCanvas.width / 20) + 1).fill(0);

    window.requestAnimationFrame(matrix);
}

window.onresize = e => {
    if (matrixCanvas) {
        matrixCanvas.width = window.innerWidth;
        matrixCanvas.height = window.innerHeight;

        let newColsCount = Math.floor(matrixCanvas.width / 20) + 1;
        if (newColsCount > cols.length)
            cols = cols.concat(Array(newColsCount - cols.length).fill(0));
    }
};

//#endregion

let form = null;
let codeInput = null;
let sendButton = null;
let wrongText = null;

async function checkSolution() {
    let solution = await fetch(`/verify/${codeInput.value.toUpperCase()}`);

    let result = await solution.json();
    codeInput.disabled = false;
    sendButton.disabled = false;

    if(result.success)
        window.location.replace(result.redirect);
    else
        wrongText.style.display = "block";
}

function initCodeForm() {
    form = document.getElementById("koodi-form");
    codeInput = document.getElementById("koodi-code");
    sendButton = document.getElementById("koodi-send");
    wrongText = document.getElementById("koodi-wrong-text");

    form.addEventListener("submit", e => {
        e.preventDefault();
        wrongText.style.display = "none";
        codeInput.disabled = true;
        sendButton.disabled = true;
        checkSolution();
    });
}

window.onload = () => {
    startBgEffect();
    initCodeForm();
};