import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="4-Player Pro Soccer Arena", 
    page_icon="⚽", 
    layout="centered"
)

st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
    h1 { text-align: center; color: #1E90FF; font-family: 'Arial Black', sans-serif; text-shadow: 2px 2px #000; }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ PRO SOCCER ARENA - 4 PLAYERS")

# Bảng điều khiển màu sắc
col1, col2 = st.columns(2)
with col1:
    team1_color = st.color_picker("Màu áo Đội Đỏ", "#FF4757")
with col2:
    team2_color = st.color_picker("Màu áo Đội Xanh", "#2ED573")

# Hướng dẫn nút bấm chia cột rõ ràng
st.markdown(f"""
<div style="background-color: rgba(255,255,255,0.05); padding: 12px; border-radius: 10px; margin-bottom: 15px; font-size: 14px;">
    <strong>🎮 HƯỚNG DẪN ĐIỀU KHIỂN (4 NGƯỜI CHƠI):</strong><br>
    <table style="width:100%; text-align:left; margin-top:5px; border-collapse: collapse;">
        <tr style="color:{team1_color}; font-weight:bold;">
            <td>🔴 ĐỘI ĐỎ:</td>
            <td>Hậu vệ: <strong>F / V</strong></td>
            <td>Tiền đạo: <strong>W / S</strong></td>
        </tr>
        <tr style="color:{team2_color}; font-weight:bold;">
            <td>🟢 ĐỘI XANH:</td>
            <td>Tiền đạo: <strong> Mũi tên ⬆ / ⬇</strong></td>
            <td>Hậu vệ: <strong>I / K</strong></td>
        </tr>
    </table>
    <div style="margin-top: 8px; text-align:center; color: #ff9f43;">⏸ Bấm phím <strong>Spacebar (Khoảng trắng)</strong> để Tạm dừng / Tiếp tục</div>
</div>
""", unsafe_allow_html=True)

# Khung HTML Game
game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            margin: 0;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: sans-serif;
            flex-direction: column;
            padding: 10px;
            border-radius: 16px;
        }}
        .scoreboard-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0, 0, 0, 0.8);
            padding: 10px 25px;
            border-radius: 50px;
            margin-bottom: 12px;
            border: 2px solid #4a90e2;
            gap: 20px;
        }}
        .team-name {{ color: #fff; font-weight: bold; font-size: 16px; }}
        .score-display {{
            font-size: 30px; font-weight: 900; color: #fff; background: #222;
            padding: 2px 15px; border-radius: 8px; min-width: 40px; text-align: center;
        }}
        .stadium-border {{
            padding: 6px; background: #333; border-radius: 12px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.6); position: relative;
        }}
        canvas {{
            border: 4px solid #fff;
            background-color: #27ae60;
            background-image: repeating-linear-gradient(90deg, #27ae60, #27ae60 40px, #2ecc71 40px, #2ecc71 80px);
            border-radius: 6px; outline: none;
        }}
        .controls-btn {{
            display: flex; gap: 15px; margin-top: 10px;
        }}
        .btn {{
            background: #ff4757; color: white; border: none; padding: 8px 18px;
            border-radius: 5px; cursor: pointer; font-weight: bold; font-size: 14px;
        }}
        .btn-pause {{ background: #ff9f43; }}
        .btn:hover {{ filter: brightness(1.2); }}
        
        /* Hiển thị chữ PAUSED đè lên sân game */
        .pause-overlay {{
            display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.6); color: white; font-size: 40px; font-weight: bold;
            justify-content: center; align-items: center; border-radius: 12px;
            pointer-events: none; letter-spacing: 2px;
        }}
    </style>
</head>
<body>

    <div class="scoreboard-container">
        <span class="team-name" style="color: {team1_color}">ĐỘI ĐỎ</span>
        <span class="score-display" id="score1">0</span>
        <span class="score-display" id="score2">0</span>
        <span class="team-name" style="color: {team2_color}">ĐỘI XANH</span>
    </div>

    <div class="stadium-border">
        <canvas id="gameCanvas" width="800" height="450" tabindex="1"></canvas>
        <div class="pause-overlay" id="pauseOverlay">TẠM DỪNG</div>
    </div>

    <div class="controls-btn">
        <button class="btn btn-pause" id="btnPause" onclick="togglePause()">TẠM DỪNG (Space)</button>
        <button class="btn" onclick="resetMatch()">LÀM MỚI TRẬN DẤU</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const pauseOverlay = document.getElementById("pauseOverlay");
        const btnPause = document.getElementById("btnPause");

        canvas.focus();

        let score1 = 0;
        let score2 = 0;
        let isPaused = false; // Trạng thái tạm dừng

        // Cấu hình kích thước thanh cầu thủ
        const pWidth = 15;
        const pHeight = 75;
        const pSpeed = 6;

        // Tọa độ Y ban đầu cho 4 cầu thủ
        let redHauVeY = canvas.height / 2 - pHeight / 2;
        let redTienDaoY = canvas.height / 2 - pHeight / 2;
        let blueTienDaoY = canvas.height / 2 - pHeight / 2;
        let blueHauVeY = canvas.height / 2 - pHeight / 2;

        // Vị trí X cố định cho sơ đồ chiến thuật 4 người
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

        window.addEventListener("keydown", (e) => {{
            if (e.key === " ") {{
                e.preventDefault();
                togglePause();
                return;
            }}
            keys[e.key] = true;
            if(["ArrowUp", "ArrowDown"].indexOf(e.key) > -1) {{
                e.preventDefault();
            }}
        }});
        
        window.addEventListener("keyup", (e) => keys[e.key] = false);
        canvas.addEventListener("click", () => canvas.focus());

        function togglePause() {{
            isPaused = !isPaused;
            if (isPaused) {{
                pauseOverlay.style.display = "flex";
                btnPause.innerText = "TIẾP TỤC (Space)";
                btnPause.style.background = "#2ed573";
            }} else {{
                pauseOverlay.style.display = "none";
                btnPause.innerText = "TẠM DỪNG (Space)";
                btnPause.style.background = "#ff9f43";
                canvas.focus();
            }}
        }}

        function resetBall(winner) {{
            ballX = canvas.width / 2;
            ballY = canvas.height / 2;
            ballSpeedX = winner === 1 ? 5 : -5;
            ballSpeedY = (Math.random() > 0.5 ? 4 : -4);
        }}

        function resetMatch() {{
            score1 = 0; score2 = 0;
            document.getElementById("score1").innerText = 0;
            document.getElementById("score2").innerText = 0;
            isPaused = false;
            pauseOverlay.style.display = "none";
            btnPause.innerText = "TẠM DỪNG (Space)";
            btnPause.style.background = "#ff9f43";
            resetBall(1);
            canvas.focus();
        }}

        // Hàm kiểm tra va chạm giữa bóng và một cầu thủ bất kỳ
        function checkCollision(pX, pY) {{
            return ballX + ballRadius > pX && 
                   ballX - ballRadius < pX + pWidth && 
                   ballY > pY && 
                   ballY < pY + pHeight;
        }}

        function update() {{
            if (isPaused) return; // Nếu đang tạm dừng thì đóng băng logic game

            // --- DI CHUYỂN 4 CẦU THỦ ---
            // 1. Đội Đỏ - Tiền đạo (W / S)
            if (keys["w"] || keys["W"]) redTienDaoY = Math.max(0, redTienDaoY - pSpeed);
            if (keys["s"] || keys["S"]) redTienDaoY = Math.min(canvas.height - pHeight, redTienDaoY + pSpeed);
            
            // 2. Đội Đỏ - Hậu vệ (F / V)
            if (keys["f"] || keys["F"]) redHauVeY = Math.max(0, redHauVeY - pSpeed);
            if (keys["v"] || keys["V"]) redHauVeY = Math.min(canvas.height - pHeight, redHauVeY + pSpeed);

            // 3. Đội Xanh - Tiền đạo (Mũi tên Lên / Xuống)
            if (keys["ArrowUp"]) blueTienDaoY = Math.max(0, blueTienDaoY - pSpeed);
            if (keys["ArrowDown"]) blueTienDaoY = Math.min(canvas.height - pHeight, blueTienDaoY + pSpeed);

            // 4. Đội Xanh - Hậu vệ (I / K)
            if (keys["i"] || keys["I"]) blueHauVeY = Math.max(0, blueHauVeY - pSpeed);
            if (keys["k"] || keys["K"]) blueHauVeY = Math.min(canvas.height - pHeight, blueHauVeY + pSpeed);

            // --- DI CHUYỂN BÓNG ---
            ballX += ballSpeedX;
            ballY += ballSpeedY;

            // Bóng đập biên dọc trên dưới
            if (ballY - ballRadius < 0 || ballY + ballRadius > canvas.height) {{
                ballSpeedY = -ballSpeedY;
            }}

            // --- XỬ LÝ VA CHẠM CẦU THỦ ---
            // Kiểm tra va chạm với Đội Đỏ (Bóng đang bay sang trái)
            if (ballSpeedX < 0) {{
                if (checkCollision(redTienDaoX, redTienDaoY)) {{
                    ballSpeedX = -ballSpeedX;
                    ballSpeedY = (ballY - (redTienDaoY + pHeight/2)) * 0.2;
                }} else if (checkCollision(redHauVeX, redHauVeY)) {{
                    ballSpeedX = -ballSpeedX;
                    ballSpeedY = (ballY - (redHauVeY + pHeight/2)) * 0.2;
                }}
            }}
            

