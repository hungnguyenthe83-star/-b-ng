import streamlit as st
import streamlit.components.v1 as components

# Cấu hình giao diện trang Streamlit
st.set_page_config(
    page_title="Streamlit Space Shooter", 
    page_icon="🚀", 
    layout="centered"
)

st.title("🚀 SPACE SHOOTER ARENA - 2 PLAYERS")

# Bảng hướng dẫn chơi trực quan
st.markdown("""
<div style="background-color: rgba(255,255,255,0.05); padding: 12px; border-radius: 10px; margin-bottom: 10px; font-size: 14px;">
    <strong>🎮 HƯỚNG DẪN ĐIỀU KHIỂN BẮN SÚNG:</strong><br>
    <table style="width:100%; text-align:left; margin-top:5px; border-collapse: collapse; line-height: 1.6;">
        <tr style="color:#ff4757; font-weight:bold;">
            <td>🔴 PHI THUYỀN ĐỎ:</td>
            <td>Di chuyển: <strong>W, A, S, D</strong></td>
            <td>Bắn: <strong>F</strong></td>
        </tr>
        <tr style="color:#2ed573; font-weight:bold;">
            <td>🟢 PHI THUYỀN XANH:</td>
            <td>Di chuyển: <strong>Mũi tên ⬆ ⬇ ⬅ ➡</strong></td>
            <td>Bắn: <strong>M</strong> (hoặc <strong>0</strong>)</td>
        </tr>
    </table>
    <div style="margin-top: 8px; text-align:center; color: #ff9f43; font-weight: bold;">
        ⏸ Nhấn phím SPACE (Khoảng trắng) để Tạm dừng / Tiếp tục trò chơi
    </div>
</div>
""", unsafe_allow_html=True)

# Toàn bộ mã nguồn Game (HTML/CSS/JS) độc lập, không dùng f-string để tránh lỗi cú pháp Python
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background: #050510;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: system-ui, -apple-system, sans-serif;
            flex-direction: column;
            padding: 10px;
            border-radius: 16px;
            overflow: hidden;
        }

        /* Thanh trạng thái UI Neon Esport */
        .status-container {
            display: flex;
            justify-content: space-between;
            width: 760px;
            background: rgba(0, 0, 0, 0.8);
            padding: 10px 20px;
            border-radius: 12px;
            margin-bottom: 12px;
            border: 1px solid #1e3c72;
            box-sizing: border-box;
        }
        .player-ui { display: flex; flex-direction: column; gap: 5px; color: white; width: 45%; }
        .hp-bar-outer { width: 100%; height: 12px; background: #333; border-radius: 6px; overflow: hidden; border: 1px solid #555; }
        .hp-bar-inner { height: 100%; width: 100%; transition: width 0.1s; }
        .red-hp { background: #ff4757; box-shadow: 0 0 8px #ff4757; }
        .blue-hp { background: #2ed573; box-shadow: 0 0 8px #2ed573; }
        .stats-text { font-size: 13px; font-weight: bold; letter-spacing: 0.5px; }

        .stadium-border {
            padding: 4px; background: #222; border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.7); position: relative;
        }

        canvas {
            border: 2px solid #3b82f6;
            background: #020208;
            border-radius: 6px; outline: none;
        }

        .controls-btn { display: flex; gap: 15px; margin-top: 12px; }
        .btn {
            background: #3b82f6; color: white; border: none; padding: 10px 22px;
            border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3); transition: all 0.2s;
        }
        .btn-pause { background: #ff9f43; }
        .btn:hover { filter: brightness(1.2); }
        
        .overlay {
            display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.75); color: white; font-size: 36px; font-weight: bold;
            justify-content: center; align-items: center; border-radius: 10px;
            pointer-events: none; text-shadow: 0 0 10px rgba(255,255,255,0.5);
            flex-direction: column; gap: 15px;
        }
    </style>
</head>
<body>

    <!-- UI Thanh máu và Kills phía trên -->
    <div class="status-container">
        <div class="player-ui">
            <div class="stats-text" style="color: #ff4757;">🔴 ĐỘI ĐỎ - KILLS: <span id="kills1">0</span></div>
            <div class="hp-bar-outer"><div id="hp1" class="hp-bar-inner red-hp"></div></div>
        </div>
        <div class="player-ui" style="text-align: right; align-items: flex-end;">
            <div class="stats-text" style="color: #2ed573;">🟢 ĐỘI XANH - KILLS: <span id="kills2">0</span></div>
            <div class="hp-bar-outer"><div id="hp2" class="hp-bar-inner blue-hp"></div></div>
        </div>
    </div>

    <!-- Khung hiển thị màn chơi chiến đấu -->
    <div class="stadium-border">
        <canvas id="gameCanvas" width="760" height="400" tabindex="1"></canvas>
        <div class="overlay" id="gameOverlay">TRÒ CHƠI TẠM DỪNG</div>
    </div>

    <!-- Nút tương tác nhanh -->
    <div class="controls-btn">
        <button class="btn btn-pause" id="btnPause" onclick="togglePause()">TẠM DỪNG (Space)</button>
        <button class="btn" onclick="resetGame()">HỒI SINH TRẬN ĐẤU</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const overlay = document.getElementById("gameOverlay");
        const btnPause = document.getElementById("btnPause");

        canvas.focus();
        document.body.addEventListener("click", () => canvas.focus());

        let isPaused = false;
        let gameOver = false;

        // Cấu hình người chơi
        const shipSize = 30;
        const shipSpeed = 5;
        const maxHp = 100;

        let p1 = { x: 50, y: 185, hp: maxHp, kills: 0, cooldown: 0 };
        let p2 = { x: 680, y: 185, hp: maxHp, kills: 0, cooldown: 0 };

        let bullets = [];
        let stars = [];
        const keys = {};

        // Khởi tạo nền sao vũ trụ chuyển động sinh động
        for (let i = 0; i < 40; i++) {
            stars.push({ x: Math.random() * canvas.width, y: Math.random() * canvas.height, size: Math.random() * 2 + 1, speed: Math.random() * 0.5 + 0.2 });
        }

        window.addEventListener("keydown", (e) => {
            if (e.key === " " || e.key === "Spacebar") {
                e.preventDefault();
                togglePause();
                return;
            }
            keys[e.key.toLowerCase()] = true;
            if(["arrowup", "arrowdown", "arrowleft", "arrowright"].indexOf(e.key.toLowerCase()) > -1) {
                e.preventDefault();
            }
        });
        window.addEventListener("keyup", (e) => keys[e.key.toLowerCase()] = false);

        function togglePause() {
            if (gameOver) return;
            isPaused = !isPaused;
            if (isPaused) {
                overlay.style.display = "flex";
                overlay.innerText = "TRÒ CHƠI TẠM DỪNG";
                btnPause.innerText = "TIẾP TỤC (Space)";
            } else {
                overlay.style.display = "none";
                btnPause.innerText = "TẠM DỪNG (Space)";
                canvas.focus();
            }
        }

        function resetGame() {
            p1.hp = maxHp; p2.hp = maxHp;
            p1.x = 50; p1.y = 185;
            p2.x = 680; p2.y = 185;
            bullets = [];
            gameOver = false; isPaused = false;
            overlay.style.display = "none";
            btnPause.innerText = "TẠM DỪNG (Space)";
            updateUI();
            canvas.focus();
        }

        function updateUI() {
            document.getElementById("hp1").style.width = p1.hp + "%";
            document.getElementById("hp2").style.width = p2.hp + "%";
            document.getElementById("kills1").innerText = p1.kills;
            document.getElementById("kills2").innerText = p2.kills;
        }

        function update() {
            if (isPaused || gameOver) return;

            // --- PHI THUYỀN ĐỎ (W, A, S, D) ---
            if (keys["w"]) p1.y = Math.max(0, p1.y - shipSpeed);
            if (keys["s"]) p1.y = Math.min(canvas.height - shipSize, p1.y + shipSpeed);
            if (keys["a"]) p1.x = Math.max(0, p1.x - shipSpeed);
            if (keys["d"]) p1.x = Math.min(canvas.width/2 - shipSize, p1.x + shipSpeed); // Không qua phần sân đối phương

            // Bắn đạn Đỏ (F)
            if (p1.cooldown > 0) p1.cooldown--;
            if (keys["f"] && p1.cooldown === 0) {
                bullets.push({ x: p1.x + shipSize, y: p1.y + shipSize/2 - 3, vx: 8, vy: 0, color: "#ff4757", owner: 1 });
                p1.cooldown = 12; // Tốc độ bắn
            }

            // --- PHI THUYỀN XANH (Mũi tên) ---
            if (keys["arrowup"]) p2.y = Math.max(0, p2.y - shipSpeed);
            if (keys["arrowdown"]) p2.y = Math.min(canvas.height - shipSize, p2.y + shipSpeed);
            if (keys["arrowleft"]) p2.x = Math.max(canvas.width/2, p2.x - shipSpeed);
            if (keys["arrowright"]) p2.x = Math.min(canvas.width - shipSize, p2.x + shipSpeed);

            // Bắn đạn Xanh (M hoặc Phím 0)
            if (p2.cooldown > 0) p2.cooldown--;
            if ((keys["m"] || keys["0"]) && p2.cooldown === 0) {
                bullets.push({ x: p2.x - 10, y: p2.y + shipSize/2 - 3, vx: -8, vy: 0, color: "#2ed573", owner: 2 });
                p2.cooldown = 12;
            }

            // Cập nhật nền sao bay lùi tạo cảm giác đang di chuyển nhanh
            stars.forEach(star => {
                star.x -= star.speed;
                if (star.x < 0) star.x = canvas.width;
            });

            // Cập nhật vị trí Đạn & kiểm tra va chạm cơ thể
            for (let i = bullets.length - 1; i >= 0; i--) {
                let b = bullets[i];
                b.x += b.vx;

                // Xóa đạn bay ra khỏi màn hình
                if (b.x < 0 || b.x > canvas.width) {
                    bullets.splice(i, 1);
                    continue;
                }

                // Đạn chạm Phi thuyền Xanh (Người chơi 2)
