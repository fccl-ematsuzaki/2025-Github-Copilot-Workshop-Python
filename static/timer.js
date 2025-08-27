let timer = 1500; // 25*60
let interval = null;
let isRunning = false;
let session = 0;

function updateDisplay() {
    const min = String(Math.floor(timer / 60)).padStart(2, '0');
    const sec = String(timer % 60).padStart(2, '0');
    document.getElementById('timer-display').textContent = `${min}:${sec}`;
    document.getElementById('session-info').textContent = `セッション: ${session}`;
}

function startTimer() {
    if (isRunning) return;
    isRunning = true;
    interval = setInterval(() => {
        if (timer > 0) {
            timer--;
            updateDisplay();
        } else {
            clearInterval(interval);
            isRunning = false;
            session++;
            timer = 300; // 5分休憩
            updateDisplay();
            setTimeout(() => {
                timer = 1500; // 作業再開
                updateDisplay();
            }, 3000); // 3秒だけ休憩表示
        }
    }, 1000);
}

function pauseTimer() {
    if (interval) clearInterval(interval);
    isRunning = false;
}

function resetTimer() {
    if (interval) clearInterval(interval);
    timer = 1500;
    isRunning = false;
    updateDisplay();
}

document.getElementById('start-btn').onclick = startTimer;
document.getElementById('pause-btn').onclick = pauseTimer;
document.getElementById('reset-btn').onclick = resetTimer;

updateDisplay();
