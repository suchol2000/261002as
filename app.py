import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌깨기 게임",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 벽돌깨기")

game = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        background: #111827;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 600px;
        overflow: hidden;
    }

    canvas {
        background: #0f172a;
        border: 3px solid #38bdf8;
        border-radius: 10px;
    }
</style>
</head>

<body>
<canvas id="game" width="480" height="550"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let ballX = canvas.width / 2;
let ballY = canvas.height - 60;

let dx = 3;
let dy = -3;

const ballRadius = 8;

const paddleWidth = 90;
const paddleHeight = 12;

let paddleX = (canvas.width - paddleWidth) / 2;

let rightPressed = false;
let leftPressed = false;

let score = 0;
let lives = 3;

const brickRowCount = 5;
const brickColumnCount = 8;

const brickWidth = 48;
const brickHeight = 20;
const brickPadding = 8;

const brickOffsetTop = 45;
const brickOffsetLeft = 18;

let bricks = [];

for (let c = 0; c < brickColumnCount; c++) {
    bricks[c] = [];

    for (let r = 0; r < brickRowCount; r++) {
        bricks[c][r] = {
            x: 0,
            y: 0,
            status: 1
        };
    }
}

document.addEventListener("keydown", keyDownHandler);
document.addEventListener("keyup", keyUpHandler);

function keyDownHandler(e) {
    if (e.key === "Right" || e.key === "ArrowRight") {
        rightPressed = true;
    }
    else if (e.key === "Left" || e.key === "ArrowLeft") {
        leftPressed = true;
    }
}

function keyUpHandler(e) {
    if (e.key === "Right" || e.key === "ArrowRight") {
        rightPressed = false;
    }
    else if (e.key === "Left" || e.key === "ArrowLeft") {
        leftPressed = false;
    }
}

function drawBall() {
    ctx.beginPath();
    ctx.arc(ballX, ballY, ballRadius, 0, Math.PI * 2);
    ctx.fillStyle = "#facc15";
    ctx.fill();
    ctx.closePath();
}

function drawPaddle() {
    ctx.beginPath();
    ctx.roundRect(
        paddleX,
        canvas.height - paddleHeight - 15,
        paddleWidth,
        paddleHeight,
        6
    );

    ctx.fillStyle = "#38bdf8";
    ctx.fill();
    ctx.closePath();
}

function drawBricks() {
    for (let c = 0; c < brickColumnCount; c++) {
        for (let r = 0; r < brickRowCount; r++) {

            if (bricks[c][r].status === 1) {

                const brickX =
                    c * (brickWidth + brickPadding) + brickOffsetLeft;

                const brickY =
                    r * (brickHeight + brickPadding) + brickOffsetTop;

                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;

                ctx.beginPath();

                ctx.roundRect(
                    brickX,
                    brickY,
                    brickWidth,
                    brickHeight,
                    4
                );

                const colors = [
                    "#ef4444",
                    "#f97316",
                    "#eab308",
                    "#22c55e",
                    "#8b5cf6"
                ];

                ctx.fillStyle = colors[r];
                ctx.fill();

                ctx.closePath();
            }
        }
    }
}

function collisionDetection() {

    for (let c = 0; c < brickColumnCount; c++) {

        for (let r = 0; r < brickRowCount; r++) {

            const brick = bricks[c][r];

            if (brick.status === 1) {

                if (
                    ballX > brick.x &&
                    ballX < brick.x + brickWidth &&
                    ballY > brick.y &&
                    ballY < brick.y + brickHeight
                ) {

                    dy = -dy;

                    brick.status = 0;

                    score++;

                    if (score === brickRowCount * brickColumnCount) {
                        setTimeout(() => {
                            alert("🎉 게임 클리어!");
                            document.location.reload();
                        }, 100);
                    }
                }
            }
        }
    }
}

function drawScore() {
    ctx.font = "16px Arial";
    ctx.fillStyle = "#ffffff";
    ctx.fillText("Score: " + score, 15, 25);
}

function drawLives() {
    ctx.font = "16px Arial";
    ctx.fillStyle = "#ffffff";
    ctx.fillText("Lives: " + lives, canvas.width - 75, 25);
}

function draw() {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawBricks();
    drawBall();
    drawPaddle();
    drawScore();
    drawLives();

    collisionDetection();

    if (
        ballX + dx > canvas.width - ballRadius ||
        ballX + dx < ballRadius
    ) {
        dx = -dx;
    }

    if (ballY + dy < ballRadius) {
        dy = -dy;
    }

    else if (ballY + dy >
        canvas.height - ballRadius - paddleHeight - 15) {

        if (
            ballX > paddleX &&
            ballX < paddleX + paddleWidth
        ) {
            dy = -dy;
        }

        else if (ballY + dy > canvas.height - ballRadius) {

            lives--;

            if (lives <= 0) {
                alert("게임 오버!");
                document.location.reload();
            }
            else {
                ballX = canvas.width / 2;
                ballY = canvas.height - 60;
                dx = 3;
                dy = -3;
                paddleX = (canvas.width - paddleWidth) / 2;
            }
        }
    }

    if (rightPressed && paddleX < canvas.width - paddleWidth) {
        paddleX += 6;
    }

    if (leftPressed && paddleX > 0) {
        paddleX -= 6;
    }

    ballX += dx;
    ballY += dy;

    requestAnimationFrame(draw);
}

draw();
</script>

</body>
</html>
"""

components.html(game, height=600)
