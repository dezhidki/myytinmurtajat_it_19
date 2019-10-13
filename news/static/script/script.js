const Swap = Swappable.default;

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
    });
};