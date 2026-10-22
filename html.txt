<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Game Đá Bóng Đơn Giản</title>
    <style>
        body {
            margin: 0;
            background-color: #222;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: white;
            font-family: Arial, sans-serif;
            flex-direction: column;
        }
        canvas {
            border: 4px solid #fff;
            background-color: #2e8b57; /* Màu sân cỏ */
        }
        .controls {
            margin-top: 15px;
            display: flex;
            gap: 40px;
            font-size: 14px;
        }
    </style>
</head>
<body>

    <h2>Tỷ số: <span id="score1">0</span> - <span id="score2">0</span></h2>
    <canvas id="gameCanvas" width="800" height="500"></canvas>
    
    <div class="controls">
        <div><strong>Người chơi 1 (Đỏ):</strong> Phím W (Lên) | S (Xuống)</div>
        <div><strong>Người chơi 2 (Xanh):</strong> Phím Mũi tên Lên | Mũi tên Xuống</div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // Khởi tạo điểm
        let score1 = 0;
        let score2 = 0;

        // Cấu hình Cầu thủ (Thanh chắn)
        const paddleWidth = 15;
        const paddleHeight = 90;
        
        let p1Y = canvas.height / 2 - paddleHeight / 2;
        let p2Y = canvas.height / 2 - paddleHeight / 2;
        const paddleSpeed = 6;

        // Cấu hình Bóng
        let ballX = canvas.width / 2;
        let ballY = canvas.height / 2;
        let ballRadius = 12;
        let ballSpeedX = 4;
        let ballSpeedY = 4;

        // Trạng thái nút bấm
        const keys = {};

        window.addEventListener("keydown", (e) => keys[e.key] = true);
        window.addEventListener("keyup", (e) => keys[e.key] = false);

        // Hàm reset bóng khi có bàn thắng
        function resetBall(winner) {
            ballX = canvas.width / 2;
            ballY = canvas.height / 2;
            ballSpeedX = winner === 1 ? 4 : -4;
            ballSpeedY = (Math.random() > 0.5 ? 4 : -4);
        }

        // Vòng lặp cập nhật logic game
        function update() {
            // Di chuyển Người chơi 1 (Phím W / S)
            if (keys["w"] || keys["W"]) p1Y = Math.max(0, p1Y - paddleSpeed);
            if (keys["s"] || keys["S"]) p1Y = Math.min(canvas.height - paddleHeight, p1Y + paddleSpeed);

            // Di chuyển Người chơi 2 (Phím Mũi tên)
            if (keys["ArrowUp"]) p2Y = Math.max(0, p2Y - paddleSpeed);
            if (keys["ArrowDown"]) p2Y = Math.min(canvas.height - paddleHeight, p2Y + paddleSpeed);

            // Di chuyển bóng
            ballX += ballSpeedX;
            ballY += ballSpeedY;

            // Bóng chạm biên trên hoặc biên dưới
            if (ballY - ballRadius < 0 || ballY + ballRadius > canvas.height) {
                ballSpeedY = -ballSpeedY;
            }

            // Bóng va chạm với Cầu thủ 1 (Màu đỏ)
            if (ballX - ballRadius < paddleWidth + 10) {
                if (ballY > p1Y && ballY < p1Y + paddleHeight) {
                    ballSpeedX = -ballSpeedX;
                    // Tăng góc sút dựa vào vị trí chạm trên cầu thủ
                    let deltaY = ballY - (p1Y + paddleHeight / 2);
                    ballSpeedY = deltaY * 0.15;
                } else if (ballX < 0) { // Vào lưới bên trái -> Người chơi 2 ghi điểm
                    score2++;
                    document.getElementById("score2").innerText = score2;
                    resetBall(2);
                }
            }

            // Bóng va chạm với Cầu thủ 2 (Màu xanh)
            if (ballX + ballRadius > canvas.width - paddleWidth - 10) {
                if (ballY > p2Y && ballY < p2Y + paddleHeight) {
                    ballSpeedX = -ballSpeedX;
                    let deltaY = ballY - (p2Y + paddleHeight / 2);
                    ballSpeedY = deltaY * 0.15;
                } else if (ballX > canvas.width) { // Vào lưới bên phải -> Người chơi 1 ghi điểm
                    score1++;
                    document.getElementById("score1").innerText = score1;
                    resetBall(1);
                }
            }
        }

        // Hàm vẽ đồ họa lên màn hình
        function draw() {
            // Xóa màn hình cũ
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ vạch kẻ sân bóng
            ctx.strokeStyle = "rgba(255,255,255,0.4)";
            ctx.lineWidth = 4;
            // Đường giữa sân
            ctx.beginPath();
            ctx.moveTo(canvas.width / 2, 0);
            ctx.lineTo(canvas.width / 2, canvas.height);
            ctx.stroke();
            // Vòng tròn giữa sân
            ctx.beginPath();
            ctx.arc(canvas.width / 2, canvas.height / 2, 70, 0, Math.PI * 2);
            ctx.stroke();

            // Vẽ Người chơi 1 (Đỏ)
            ctx.fillStyle = "#ff4757";
            ctx.fillRect(10, p1Y, paddleWidth, paddleHeight);

            // Vẽ Người chơi 2 (Xanh nước biển)
            ctx.fillStyle = "#2ed573";
            ctx.fillRect(canvas.width - paddleWidth - 10, p2Y, paddleWidth, paddleHeight);

            // Vẽ quả bóng (Trắng)
            ctx.fillStyle = "#fff";
            ctx.beginPath();
            ctx.arc(ballX, ballY, ballRadius, 0, Math.PI * 2);
            ctx.fill();
        }

        // Vòng lặp chính của Game (Game Loop)
        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        // Chạy game
        gameLoop();
    </script>
</body>
</html>
