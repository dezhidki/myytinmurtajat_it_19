async function pollStatus(handle) {
    let status = await fetch("/poll_challenge");
    let skipResult = await status.json();
    if (!skipResult.inChallenge) {
        handle.shouldStop = true;
        window.location.replace(skipResult.redirect);
    }
}

function setIntervalAsync(callback, interval) {
    let handle = {
        shouldStop: false
    };
    let handler = () => {
        callback(handle).finally(() => {
            if (!handle.shouldStop)
                setTimeout(handler, interval);
        });
    };
    setTimeout(handler, interval);
    return handle;
}

window.onload = () => {
    setIntervalAsync(pollStatus, 5000);
};