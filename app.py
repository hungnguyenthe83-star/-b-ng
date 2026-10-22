import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="4-Player Soccer Pro Arena", 
    page_icon="⚽", 
    layout="centered"
)

st.title("⚽ PRO SOCCER ARENA - 4 PLAYERS")

# Hướng dẫn nút bấm chia cột trực quan bằng Streamlit
st.markdown("""
<div style="background-color: rgba(255,255,255,0.05); padding: 12px; border-radius: 10px; margin-bottom: 10px; font-size: 14px;">
    <strong>🎮 SƠ ĐỒ ĐIỀU KHIỂN (4 NGƯỜI CHƠI):</strong><br>
    <table style="width:100%; text-align:left; margin-top:5px; border-collapse: collapse; line-height: 1.6;">
        <tr style="color:#ff4757; font-weight:bold;">
            <td>🔴 ĐỘI ĐỎ:</td>
            <td>Hậu vệ: <strong>F / V</strong></td>
            <td>Tiền đạo: <strong>W / S</strong></td>
        </tr>
        <tr style="color:#2ed573; font-weight:bold;">
            <td>🟢 ĐỘI XANH:</td>
            <td>Tiền đạo: <strong>Mũi tên ⬆ / ⬇</strong></td>
            <td>Hậu vệ: <strong>I / K</strong></td>
        </tr>
    </table>
    <div style="margin-top: 8px; text-align:center; color: #ff9f43; font-weight: bold;">
        ⏸ Nhấn phím SPACE (Khoảng trắng) hoặc click nút trong game để Tạm dừng
    </div>
</div>
""", unsafe_allow_html=True)

# Đưa toàn bộ UI Điều khiển & Game vào nội bộ HTML để tránh lỗi mất Focus bàn phím của Streamlit
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: system-ui, -apple-system, sans-serif;
            flex-direction: column;
            padding: 15px;
            border-radius: 16px;
            overflow: hidden;
        }
        
        /* Bộ tinh chỉnh màu áo ngay trong Game */
        .color-pickers-bar {
            display: flex;
            gap: 20px;
            margin-bottom: 12px;
            color: white;
            font-size: 14px;
            align-items: center;
        }
        .color-item { display: flex; align-items: center; gap: 8px; }
        .color-item input { cursor: pointer; border: none; width: 30px; height: 25px; border-radius: 4px; }

        /* Bảng điểm Esport */
        .scoreboard-container {
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0, 0, 0, 0.85);
            padding: 8px 25px;
            border-radius: 50px;
            margin-bottom: 15px;
            border: 2px solid #4a90e2;
            gap: 20px;
        }
        .team-name { color: #fff; font-weight: bold; font-size: 16px; letter-spacing: 1px; }
        .score-display {
            font-size: 32px; font-weight: 900; color: #fff; background: #111;
            padding: 2px 15px; border-radius: 8px; min-width: 40px; text-align: center;
            font-family: monospace; box-shadow: inset 0 0 5px rgba(255,255,255,0.2);
        }
        .vs { color: #ff9f43; font-weight: bold; font-style: italic; }

        /* Khung sân vận động */
        .stadium-border {
            padding: 6px; background: #333; border-radius: 12px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.6); position: relative;
        }

        canvas {
            border: 4px solid #fff;
            background-color: #27ae60;
            background-image: repeating-linear-gradient(90deg, #27ae60, #27ae60 40px, #2ecc71 40px, #2ecc71 80px);
            border-radius: 6px; outline: none;
        }

        .controls-btn { display: flex; gap: 15px; margin-top: 15px; }
        .btn {
            background: #ff4757; color: white; border: none; padding: 10px 20px;
            border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2); transition: all 0.2s;
        }
        .btn-pause { background: #ff9f43; }
        .btn:hover { filter: brightness(1.2); transform: translateY(-1px); }
        .btn:active { transform: translateY(1px); }
        
        /* Phủ mờ khi Tạm dừng */
        .pause-overlay {
            display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.65); color: white; font-size: 42px; font-weight: bold;
            justify-content: center; align-items: center; border-radius: 12px;
            pointer-events: none; letter-spacing: 4px; text-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
    </style>
</head>
<body>

    <!-- Khu vực chỉnh màu nội bộ không làm mất focus -->
    <div class="color-pickers-bar">
        <div class="color-item">
            <span>Áo Đội Đỏ:</span>
            <input type="color" id="colorRed" value="#ff4757">
        </div>
        <div class="color-item">
            <span>Áo Đội Xanh:</span>
            <input type="color" id="colorBlue" value="#2ed573">
        </div>
    </div>

    <!-- UI Bảng điểm -->
    <div class="scoreboard-container">
        <span class="team-name" id="nameRed" style="color: #ff4757">ĐỘI ĐỎ</span>
        <span class="score-display" id="score1">0</span>
        <span class="vs">VS</span>
        <span class="score-display" id="score2">0</span>
        <span class="team-name" id="nameBlue" style="color: #2ed573">ĐỘI XANH</span>
    </div>

    <!-- Khung sân cỏ -->
    <div class="stadium-border">
        <canvas id="gameCanvas" width="780" height="420" tabindex="1"></canvas>
        <div class="pause-overlay" id="pauseOverlay">TRÒ CHƠI TẠM DỪNG</div>
    </div>

    <!-- Thanh nút chức năng -->
    <div class="controls-btn">
        <button class="btn btn-pause" id="btnPause" onclick="togglePause()">TẠM DỪNG (Space)</button>
        <button class="btn" onclick="resetMatch()">LÀM MỚI TRẬN ĐẤU</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const pauseOverlay = document.getElementById("pauseOverlay");
        const btnPause = document.getElementById("btnPause");
        
        // Element đổi màu
        const colorRedInput = document.getElementById("colorRed");
        const colorBlueInput = document.getElementById("colorBlue");
        const nameRedLabel = document.getElementById("nameRed");
        const nameBlueLabel = document.getElementById("nameBlue");

        // Ép hệ thống nhận diện chuột và giữ tiêu điểm bàn phím liên tục
        canvas.focus();
        document.body.addEventListener("click", () => canvas.focus());

        let score1 = 0;
        let score2 = 0;
        let isPaused = false;

        const pWidth = 15;
        const pHeight = 75;
        const pSpeed = 6;

        // Vị trí cầu thủ 4 người
        let redHauVeY = canvas.height / 2 - pHeight / 2;
        let redTienDaoY = canvas.height / 2 - pHeight / 2;
        let blueTienDaoY = canvas.height / 2 - pHeight / 2;
        let blueHauVeY = canvas.height / 2 - pHeight / 2;

        const redHauVeX = 40;
        const redTienDaoX = 240;
        const blueTienDaoX = canvas.width - 240 - pWidth;
        const blueHauVeX = canvas.width - 40 - pWidth;

        // Cấu hình bóng
        let ballX = canvas.width / 2;
        let ballY = canvas.height / 2;
        let ballRadius = 10;
        let ballSpeedX = 5;
        let ballSpeedY = 4;

        const keys = {};

        // Bắt sự kiện phím
        window.addEventListener("keydown", (e) => {
            if (e.key === " " || e.key === "Spacebar") {
                e.preventDefault();
                togglePause();
                return;
            }
            keys[e.key] = true;
            // Chặn cuộn màn hình khi dùng phím mũi tên
            if(["ArrowUp", "ArrowDown"].indexOf(e.key) > -1) {
                e.preventDefault();
            }
        });
        
        window.addEventListener("keyup", (e) => keys[e.key] = false);

        function togglePause() {
            isPaused = !isPaused;
            if (isPaused) {
                pauseOverlay.style.display = "flex";
                btnPause.innerText = "TIẾP TỤC (Space)";
                btnPause.style.background = "#2ed573";
            } else {
                pauseOverlay.style.display = "none";
                btnPause.innerText = "TẠM DỪNG (Space)";
                btnPause.style.background = "#ff9f43";
                canvas.focus();
            }
        }

        function resetBall(winner) {
            ballX = canvas.width / 2;
            ballY = canvas.height / 2;
            ballSpeedX = winner === 1 ? 5 : -5;
            ballSpeedY = (Math.random() > 0.5 ? 4 : -4);
        }

        function resetMatch() {
            score1 = 0; score2 = 0;
            document.getElementById("score1").innerText = 0;
            document.getElementById("score2").innerText = 0;
            isPaused = false;
            pauseOverlay.style.display = "none";
            btnPause.innerText = "TẠM DỪNG (Space)";
            btnPause.style.background = "#ff9f43";
            resetBall(1);
            canvas.focus();
        }

        function checkCollision(pX, pY) {
            return ballX + ballRadius > pX && 
                   ballX - ballRadius < pX + pWidth && 
                   ballY > pY && 
                   ballY < pY + pHeight;
        }

        function update() {
            if (isPaused) return;

            // Đồng bộ màu sắc áo đấu theo thời gian thực khi chỉnh bảng chọn màu
            nameRedLabel.style.color = colorRedInput.value;
            nameBlueLabel.style.color = colorBlueInput.value;

            // --- ĐIỀU KHIỂN CẦU THỦ ---
            // Đội Đỏ - Tiền đạo (W / S)
            if (keys["w"] || keys["W"]) redTienDaoY = Math.max(0, redTienDaoY - pSpeed);
            if (keys["s"] || keys["S"]) redTienDaoY = Math.min(canvas.height - pHeight, redTienDaoY + pSpeed);
            
            // Đội Đỏ - Hậu vệ (F / V)


