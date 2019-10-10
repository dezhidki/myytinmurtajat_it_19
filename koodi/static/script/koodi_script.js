function startBgEffect() {
    const canvas = document.getElementById("bg-effect");
    const ctx = canvas.getContext("2d");

    const w = canvas.width = window.innerWidth;
    const h = canvas.height = window.innerHeight;

    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, w, h);
}

window.onload = () => {
    startBgEffect();
};