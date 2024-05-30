const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const player = {
    x: 100,
    y: canvas.height - 150,
    width: 50,
    height: 50,
    color: 'white',
    dx: 0,
    dy: 0,
    speed: 5,
    jumpPower: 10,
    gravity: 0.5,
    isJumping: false,
};

const platforms = [
    { x: 50, y: canvas.height - 100, width: 200, height: 20 },
    { x: 300, y: canvas.height - 200, width: 200, height: 20 },
    { x: 600, y: canvas.height - 300, width: 200, height: 20 },
    { x: 900, y: canvas.height - 400, width: 200, height: 20 },
    { x: 1200, y: canvas.height - 500, width: 200, height: 20 },
    { x: 1500, y: canvas.height - 600, width: 200, height: 20 },
    { x: 1800, y: canvas.height - 700, width: 200, height: 20 },
    { x: 2100, y: canvas.height - 800, width: 200, height: 20 },
];

const challenges = [
    { id: 1, text: "1. 점프 10번 하기", state: false }
];

let completedChallenges = [];
let challengeStartTime = null;
let jumpCount = 0;
let isplaying = false;

let camera = {
    x: 0,
    y: 0,
    width: canvas.width,
    height: canvas.height,
    update(player) {
        this.x = player.x - this.width / 2 + player.width / 2;
        this.y = player.y - this.height / 2 + player.height / 2;

        if (this.x < 0) this.x = 0;
        if (this.y < 0) this.y = 0;
        if (this.x + this.width > 3000) this.x = 3000 - this.width; // Adjust based on map size
        if (this.y + this.height > canvas.height) this.y = canvas.height - this.height;
    }
};

function drawPlayer() {
    ctx.fillStyle = player.color;
    ctx.fillRect(player.x - camera.x, player.y - camera.y, player.width, player.height);
}

function drawPlatforms() {
    ctx.fillStyle = 'black';
    platforms.forEach(platform => {
        ctx.fillRect(platform.x - camera.x, platform.y - camera.y, platform.width, platform.height);
    });
}

function showchalcompltxt() {
    document.getElementById('chal-compl').style.display = 'block';
    document.getElementById('chal-compl-txt').textContent = challenges[0].text;
    setTimeout(function() {
        document.getElementById('chal-compl').style.display = 'none';
    }, 2000);
}

function checkChallenges() {
    if (!challenges[0].state && jumpCount >= 10) {
        showchalcompltxt();
        challenges[0].state = true;
        completedChallenges.push(challenges[0]);
    }
}

function update() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    player.x += player.dx;
    player.y += player.dy;

    if (player.y + player.height < canvas.height) {
        player.dy += player.gravity;
    } else {
        player.dy = 0;
        player.isJumping = false;
        player.y = canvas.height - player.height;
    }

    platforms.forEach(platform => {
        if (player.x < platform.x + platform.width &&
            player.x + player.width > platform.x &&
            player.y + player.height < platform.y + platform.height &&
            player.y + player.height + player.dy >= platform.y) {
            player.dy = 0;
            player.isJumping = false;
            player.y = platform.y - player.height;
        }

        if (player.x < platform.x + platform.width &&
            player.x + player.width > platform.x &&
            player.y < platform.y + platform.height &&
            player.y + player.dy > platform.y + platform.height) {
            player.dy = 1; // Apply a small downward force to prevent sticking
        }
    });

    if (player.x < 0) {
        player.x = 0;
    } else if (player.x + player.width > 3000) { // Adjust based on map size
        player.x = 3000 - player.width;
    }

    camera.update(player);

    drawPlayer();
    drawPlatforms();
    checkChallenges();
    requestAnimationFrame(update);
}

function handleKeyDown(e) {
    if (isplaying) {
        if (e.key === 'ArrowRight' || e.key === 'd') {
            player.dx = player.speed;
        } else if (e.key === 'ArrowLeft' || e.key === 'a') {
            player.dx = -player.speed;
        } else if (e.key === ' ' || e.key === 'ArrowUp' || e.key === 'w') {
            if (!player.isJumping) {
                player.dy = -player.jumpPower;
                player.isJumping = true;
                jumpCount++;
            }
        }
    }
}

function showSubMenu() {
    document.getElementById('sub-menu').style.display = 'block';
}

function continu() {
    isplaying = true;
    document.getElementById('sub-menu').style.display = 'none';
}

document.addEventListener('keydown', function(event) {
    if (event.key === "Escape" && isplaying == true) {
        isplaying = false;
        showSubMenu();
    }
});

function exit() {
    isplaying = false;
    player.x = 100;
    player.y = canvas.height - 150;
    document.getElementById('menu').style.display = 'block';
    document.getElementById('sub-menu').style.display = 'none';
    document.getElementById('challenge-menu').style.display = 'none';
}

function handleKeyUp(e) {
    if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'ArrowLeft' || e.key === 'a') {
        player.dx = 0;
    }
}

document.addEventListener('keydown', handleKeyDown);
document.addEventListener('keyup', handleKeyUp);

document.getElementById('startButton').addEventListener('click', () => {
    document.getElementById('menu').style.display = 'none';
    isplaying = true;
    canvas.style.display = 'block';
    update();
});

document.getElementById('challenge').addEventListener('click', () => {
    for (let i = 0; i < completedChallenges.length; i++) {
        document.getElementById('chag-txt').textContent += completedChallenges[i].text;
    }
    document.getElementById('menu').style.display = 'none';
    document.getElementById('challenge-menu').style.display = 'block';
});

document.getElementById('cha-exit').addEventListener('click', () => {
    document.getElementById('menu').style.display = 'block';
    document.getElementById('challenge-menu').style.display = 'none';
});

// Show the menu initially
document.getElementById('menu').style.display = 'block';