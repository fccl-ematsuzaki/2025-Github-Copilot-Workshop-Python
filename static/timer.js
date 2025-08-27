
let timer = 1500; // 25*60
let interval = null;
let isRunning = false;
let session = 0;
let isBreak = false;

const startBtn = document.getElementById('start-btn');
const pauseBtn = document.getElementById('pause-btn');
const resetBtn = document.getElementById('reset-btn');
const timerDisplay = document.getElementById('timer-display');

function updateDisplay() {
    const min = String(Math.floor(timer / 60)).padStart(2, '0');
    const sec = String(timer % 60).padStart(2, '0');
    // アニメーション: 数字が変わるときフェード
    timerDisplay.classList.remove('fade');
    void timerDisplay.offsetWidth; // reflow
    timerDisplay.classList.add('fade');
    timerDisplay.textContent = `${min}:${sec}`;
    document.getElementById('session-info').textContent = `セッション: ${session}`;
    // ボタン状態
    startBtn.disabled = isRunning;
    pauseBtn.disabled = !isRunning;
}

function notify(msg) {
    if (Notification.permission === 'granted') {
        new Notification(msg);
    }
}

function startTimer() {
    if (isRunning) return;
    isRunning = true;
    updateDisplay();
    interval = setInterval(() => {
        if (timer > 0) {
            timer--;
            updateDisplay();
        } else {
            clearInterval(interval);
            isRunning = false;
            if (!isBreak) {
                session++;
                isBreak = true;
                timer = 300; // 5分休憩
                notify('作業セッション終了！休憩しましょう。');
                startBtn.textContent = '休憩スタート';
            } else {
                isBreak = false;
                timer = 1500; // 作業再開
                notify('休憩終了！作業を再開しましょう。');
                startBtn.textContent = 'スタート';
            }
            updateDisplay();
        }
    }, 1000);
}

function pauseTimer() {
    if (interval) clearInterval(interval);
    isRunning = false;
    updateDisplay();
}

function resetTimer() {
    if (interval) clearInterval(interval);
    timer = 1500;
    isBreak = false;
    isRunning = false;
    startBtn.textContent = 'スタート';
    updateDisplay();
}

startBtn.onclick = startTimer;
pauseBtn.onclick = pauseTimer;
resetBtn.onclick = resetTimer;

// 通知許可リクエスト
if ('Notification' in window && Notification.permission !== 'granted') {
    Notification.requestPermission();
}

updateDisplay();
