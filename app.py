import streamlit as st
import streamlit.components.v1 as components

# 1. Cấu hình trang Streamlit hiện đại
st.set_page_config(
    page_title="Pro Soccer Streamlit Arena", 
    page_icon="⚽", 
    layout="centered"
)

# Thêm CSS tùy chỉnh cho giao diện Streamlit gọn gàng hơn
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { text-align: center; color: #1E90FF; font-family: 'Arial Black', sans-serif; text-shadow: 2px 2px #000; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ PRO SOCCER ARENA")

# 2. BẢNG ĐIỀU KHIỂN UI (Streamlit Native Columns)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    team1_color = st.color_picker("Áo Đội 1 (W/S)", "#FF4757")
with col2:
    team2_color = st.color_picker("Áo Đội 2 (⬆/⬇)", "#2ED573")
with col3:
    # Nút bấm ảo để nhắc nhở reset (game reset trực tiếp trong canvas mượt hơn)
    st.write(" ")
    st.write(" ")
    difficulty = st.selectbox("Độ khó bóng", ["Bình thường", "Bóng xoáy Pro"])

# Định nghĩa tốc độ bóng dựa theo độ khó tuyển chọn
ball_speed_modifier = 1.3 if difficulty == "Bóng xoáy Pro" else 1.0

# 3. MÃ NGUỒN GAME HTML5 VỚI UI CAO CẤP (Giao diện Sân vận động)
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
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            flex-direction: column;
            padding: 10px;
            border-radius: 16px;
            box-shadow: inset 0 0 100px rgba(0,0,0,0.5);
        }}
        
        /* Bảng điểm UI Neon phong cách Esport */
        .scoreboard-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0, 0, 0, 0.75);
            padding: 12px 30px;
            border-radius: 50px;
            margin-bottom: 15px;
            border: 2px solid #4a90e2;
            box-shadow: 0 0 20px rgba(74, 144, 226, 0.5);
            gap: 20px;
        }}
        .team-name {{
            color: #fff;
            font-weight: bold;
            font-size: 16px;
            letter-spacing: 1px;
        }}
        .score-display {{
            font-size: 32px;
            font-weight: 900;
            color: #fff;
            background: #222;
            padding: 2px 15px;
            border-radius: 8px;
            border: 1px solid #555;
            min-width: 40px;
            text-align: center;
            font-family: monospace;
        }}
        .vs {{
            color: #ff9f43;
            font-weight: bold;
            font-style: italic;
        }}

        /* Khung chứa sân vận động */
        .stadium-border {{
            padding: 8px;
            background: #333;
            border-radius: 12px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.6);
        }}

        canvas {{
            border: 4px solid #fff;
            background-color: #27ae60;
            /* Tạo sọc cỏ đậm nhạt bóng đá chuyên nghiệp */
            background-image: repeating-linear-gradient(90deg, #27ae60, #27ae60 40px, #2ecc71 40px, #2ecc71 80px);
            border-radius: 6px;
            cursor: pointer;
            outline: none;
        }}

        /* Chỉ dẫn điều khiển */
        .info-bar {{
            margin-top: 12px;
            color: #e0e0e0;
            font-size: 13px;
            text-align: center;
            background: rgba(0,0,0,0.4);
            padding: 6px 20px;
            border-radius: 20px;
        }}
        
        .btn-reset {{
            margin-top: 10px;
            background: #ff4757;
            color: white;
            border: none;
            padding: 6px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }}
        .btn-reset:hover {{ background: #ff6b81; }}
    </style>
</head>
<body>

    <!-- UI Bảng điểm lớn -->
    <div class="scoreboard-container">
        <span class="team-name" style="color: {team1_color}">ĐỘI ĐỎ</span>
        <span class="score-display" id="score1">0</span>
        <span class="vs">VS</span>
        <span class="score-display" id="score2">0</span>
        <span class="team-name" style="color: {team2_color}">ĐỘI XANH</span>
    </div>

    <!-- Khung sân cỏ -->
    <div class="stadium-border">
        <canvas id="gameCanvas" width="700" height="400" tabindex="1"></canvas>
    </div>

    <button class="btn-reset" onclick="resetMatch()">LÀM MỚI TRẬN ĐẤU</button>

    <div class="info-bar">
        🕹️ Nhấp vào sân cỏ để kích hoạt điều khiển phím di chuyển cầu thủ!
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        canvas.focus();

        let score1 = 0;
        let score2 = 0;

        const paddleWidth = 16;
        const paddleHeight = 85;
        
        let p1Y = canvas.height / 2 - paddleHeight / 2;
        let p2Y = canvas.height / 2 - paddleHeight / 2;
        const paddleSpeed = 8;

        // Cấu hình bóng chuyên nghiệp
        let ballX = canvas.width / 2;
        let ballY = canvas.height / 2;
        let ballRadius = 11;
        let baseSpeed = 5 * {ball_speed_modifier};
        let ballSpeedX = baseSpeed;
        let ballSpeedY = baseSpeed;

        const keys = {};

        window.addEventListener("keydown", (e) => {{
            keys[e.key] = true;
            if(["ArrowUp", "ArrowDown", " "].indexOf(e.key) > -1) {{
                e.preventDefault();
            }}
        }});
        window.addEventListener("keyup", (e) => keys[e.key] = false);
        canvas.addEventListener("click", () => canvas.focus());

        function resetBall(winner) {{
            ballX = canvas.width / 2;
            ballY = canvas.height / 2;
            ballSpeedX = winner === 1 ? baseSpeed : -baseSpeed;
            ballSpeedY = (Math.random() > 0.5 ? 4 : -4);
        }}

        function resetMatch() {{
            score1 = 0;
            score2 = 0;
            document.getElementById("score1").innerText = 0;
            document.getElementById("score2").innerText = 0;
            resetBall(1);
        }}

        function update() {{
            if (keys["w"] || keys["W"]) p1Y = Math.max(0, p1Y - paddleSpeed);
            if (keys["s"] || keys["S"]) p1Y = Math.min(canvas.height - paddleHeight, p1Y + paddleSpeed);

            if (keys["ArrowUp"]) p2Y = Math.max(0, p2Y - paddleSpeed);
            if (keys["ArrowDown"]) p2Y = Math.min(canvas.height - paddleHeight, p2Y + paddleSpeed);

            ballX += ballSpeedX;
            ballY += ballSpeedY;

            // Chạm biên dọc (Biên ném biên)
            if (ballY - ballRadius < 0 || ballY + ballRadius > canvas.height) {{
                ballSpeedY = -ballSpeedY;
            }}

            // Kiểm tra va chạm Cầu thủ 1 (Đỏ)
            if (ballX - ballRadius < paddleWidth + 10) {{
                if (ballY > p1Y && ballY < p1Y + paddleHeight) {{
                    ballSpeedX = -ballSpeedX;
                    let deltaY = ballY - (p1Y + paddleHeight / 2);
                    ballSpeedY = deltaY * 0.22; // Hiệu ứng xoáy bóng góc rộng
                }} else if (ballX < 0) {{
                    score2++;
                    document.getElementById("score2").innerText = score2;
                    resetBall(2);
                }}
            }}

            // Kiểm tra va chạm Cầu thủ 2 (Xanh)
            if (ballX + ballRadius > canvas.width - paddleWidth - 10) {{
                if (ballY > p2Y && ballY < p2Y + paddleHeight) {{
                    ballSpeedX = -ballSpeedX;
                    let deltaY = ballY - (p2Y + paddleHeight / 2);
                    ballSpeedY = deltaY * 0.22;
                }} else if (ballX > canvas.width) {{
                    score1++;
                    document.getElementById("score1").innerText = score1;
                    resetBall(1);
                }}
            }}
        }

        function draw() {{
            // Xóa khung hình để vẽ lại sân sọc
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Vẽ các đường kẻ vạch sân bóng chuyên nghiệp
            ctx.strokeStyle = "rgba(255,255,255,0.6)";
            ctx.lineWidth = 4;
            
            // Vòng tròn trung tâm
            ctx.beginPath();
            ctx.arc(canvas.width / 2, canvas.height / 2, 70, 0, Math.PI * 2);
            ctx.stroke();
            
            // Điểm giao bóng trung tâm
            ctx.fillStyle = "rgba(255,255,255,0.8)";
            ctx.beginPath();
            ctx.arc(canvas.width / 2, canvas.height / 2, 5, 0, Math.PI * 2);
            ctx.fill();

            // Đường giữa sân
            ctx.beginPath();
            ctx.moveTo(canvas.width / 2, 0);
            ctx.lineTo(canvas.width / 2, canvas.height);
            ctx.stroke();

            // Vòng cấm địa Đội 1 (Trái)
            ctx.strokeRect(0, canvas.height/4, 80, canvas.height/2);
            // Vòng cấm địa Đội 2 (Phải)
            ctx.strokeRect(canvas.width - 80, canvas.height/4, 80, canvas.height/2);

            // 2. Vẽ Cầu thủ 1 (Đỏ - Bo tròn góc mượt mà)
            ctx.fillStyle = "{team1_color}";
            ctx.beginPath();
            ctx.roundRect(10, p1Y, paddleWidth, paddleHeight, 8);
            ctx.fill();
            ctx.shadowBlur = 10;
            ctx.shadowColor = "{team1_color}";

            // 3. Vẽ Cầu thủ 2 (Xanh - Bo tròn góc mượt mà)
            ctx.fillStyle = "{team2_color}";
            ctx.beginPath();
            ctx.roundRect(canvas.width - paddleWidth - 10, p2Y, paddleWidth, paddleHeight, 8);
            ctx.fill();
            ctx.shadowColor = "{team2_color}";

