import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Streamlit Soccer Game", layout="centered")

st.title("⚽ Game Đá Bóng 2 Người Trên Streamlit")
st.markdown("""
**Hướng dẫn điều khiển:**
* 🔴 **Người chơi 1 (Đỏ):** Phím **W** (Lên) | **S** (Xuống)
* 🟢 **Người chơi 2 (Xanh):** Phím **Mũi tên Lên** | **Mũi tên Xuống**
* 💡 *Lưu ý: Click chuột vào khung game trước khi bấm phím để kích hoạt điều khiển.*
""")

# Đoạn mã nguồn HTML/JS của Game
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background-color: #222;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            flex-direction: column;
        }
        canvas {
            border: 4px solid #fff;
            background-color: #2e8b57;
            cursor: pointer;
        }
        h2 {
            color: white;
            margin: 10px 0;
        }
    </style>
</head>
<body>

    <h2>Tỷ số: <span id="score1">0</span> - <span id="score2">0</span></h2>
    <!-- Thêm tabIndex để canvas có thể nhận sự kiện bàn phím trong iframe -->
    <canvas id="gameCanvas" width="700" height="400" tabindex="1"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // Tự động focus vào canvas khi load
        canvas.focus();

        let score1 = 0;
        let score2 = 0;

        const paddleWidth = 15;
        const paddleHeight = 80;
        
        let p1Y = canvas.height / 2 - paddleHeight / 2;
        let p2Y = canvas.height / 2 - paddleHeight / 2;
        const paddleSpeed = 7;

        let ballX = canvas.width / 2;
        let ballY = canvas.height / 2;
        let ballRadius = 10;
        let ballSpeedX = 5;
        let ballSpeedY = 5;

        const keys = {};

        // Lắng nghe sự kiện phím trực tiếp trên canvas hoặc window của iframe
        window.addEventListener("keydown", (e) => {
            keys[e.key] = true;
            // Ngăn màn hình streamlit bị cuộn lên xuống khi bấm phím mũi tên
            if(["ArrowUp", "ArrowDown", " "].indexOf(e.key) > -1) {
                e.preventDefault();
            }
        });
        window.addEventListener("keyup", (e) => keys[e.key] = false);
        canvas.addEventListener("click", () => canvas.focus());

        function resetBall(winner) {
            ballX = canvas.width / 2;
            ballY = canvas.height / 2;
            ballSpeedX = winner === 1 ? 5 : -5;
            ballSpeedY = (Math.random() > 0.5 ? 4 : -4);
        }

        function update() {
            if (keys["w"] || keys["W"]) p1Y = Math.max(0, p1Y - paddleSpeed);
            if (keys["s"] || keys["S"]) p1Y = Math.min(canvas.height - paddleHeight, p1Y + paddleSpeed);

            if (keys["ArrowUp"]) p2Y = Math.max(0, p2Y - paddleSpeed);
            if (keys["ArrowDown"]) p2Y = Math.min(canvas.height - paddleHeight, p2Y + paddleSpeed);

            ballX += ballSpeedX;
            ballY += ballSpeedY;

            if (ballY - ballRadius < 0 || ballY + ballRadius > canvas.height) {
                ballSpeedY = -ballSpeedY;
            }

            if (ballX - ballRadius < paddleWidth + 10) {
                if (ballY > p1Y && ballY < p1Y + paddleHeight) {
                    ballSpeedX = -ballSpeedX;
                    let deltaY = ballY - (p1Y + paddleHeight / 2);
                    ballSpeedY = deltaY * 0.2;
                } else if (ballX < 0) {
                    score2++;
                    document.getElementById("score2").innerText = score2;
                    resetBall(2);
                }
            }

            if (ballX + ballRadius > canvas.width - paddleWidth - 10) {
                if (ballY > p2Y && ballY < p2Y + paddleHeight) {
                    ballSpeedX = -ballSpeedX;
                    let deltaY = ballY - (p2Y + paddleHeight / 2);
                    ballSpeedY = deltaY * 0.2;
                } else if (ballX > canvas.width) {
                    score1++;
                    document.getElementById("score1").innerText = score1;
                    resetBall(1);
                }
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.strokeStyle = "rgba(255,255,255,0.4)";
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(canvas.width / 2, 0);
            ctx.lineTo(canvas.width / 2, canvas.height);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.arc(canvas.width / 2, canvas.height / 2, 60, 0, Math.PI * 2);
            ctx.stroke();

            // Cầu thủ 1 (Đỏ)
            ctx.fillStyle = "#ff4757";
            ctx.fillRect(10, p1Y, paddleWidth, paddleHeight);

            // Cầu thủ 2 (Xanh)
            ctx.fillStyle = "#2ed573";
            ctx.fillRect(canvas.width - paddleWidth - 10, p2Y, paddleWidth, paddleHeight);

            // Bóng
            ctx.fillStyle = "#fff";
            ctx.beginPath();
            ctx.arc(ballX, ballY, ballRadius, 0, Math.PI * 2);
            ctx.fill();
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
"""

# Nhúng component HTML vào ứng dụng Streamlit
components.html(game_html, height=500)
