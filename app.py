from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="theme-color" content="#050b18">
<title>VOID SPACE</title>

<style>
* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}

html,
body {
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #02050d;
    color: #eaf6ff;
    font-family: Arial, Helvetica, sans-serif;
    touch-action: none;
}

body {
    user-select: none;
}

#game {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    display: block;
    background:
        radial-gradient(circle at center, #08162c 0%, #030817 48%, #01030a 100%);
}

.screen {
    position: fixed;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    pointer-events: none;
    opacity: 0;
    visibility: hidden;
    transition: opacity .2s ease;
}

.screen.active {
    pointer-events: auto;
    opacity: 1;
    visibility: visible;
}

.panel {
    width: min(94vw, 620px);
    max-height: 90vh;
    overflow-y: auto;
    padding: 34px;
    border: 1px solid rgba(84, 193, 255, .45);
    border-radius: 24px;
    background: rgba(3, 10, 24, .91);
    box-shadow:
        0 0 50px rgba(0, 157, 255, .13),
        inset 0 0 40px rgba(0, 130, 255, .04);
    backdrop-filter: blur(16px);
    text-align: center;
}

.logo {
    font-size: clamp(38px, 9vw, 82px);
    font-weight: 900;
    letter-spacing: .12em;
    line-height: .95;
    color: #eaf9ff;
    text-shadow:
        0 0 8px #46c9ff,
        0 0 24px rgba(45, 181, 255, .7),
        0 0 60px rgba(0, 136, 255, .35);
}

.subtitle {
    margin-top: 12px;
    color: #79bfe4;
    letter-spacing: .3em;
    font-size: 12px;
}

.menu-buttons {
    display: grid;
    gap: 12px;
    margin-top: 32px;
}

button {
    appearance: none;
    border: 1px solid rgba(93, 204, 255, .48);
    border-radius: 13px;
    padding: 15px 18px;
    min-height: 52px;
    color: #eaf9ff;
    background: linear-gradient(
        180deg,
        rgba(26, 87, 128, .55),
        rgba(6, 28, 54, .8)
    );
    font-size: 15px;
    font-weight: 800;
    letter-spacing: .08em;
    cursor: pointer;
    box-shadow: inset 0 0 20px rgba(70, 190, 255, .04);
    transition: transform .12s ease, background .12s ease;
}

button:hover {
    background: linear-gradient(
        180deg,
        rgba(36, 119, 170, .7),
        rgba(7, 39, 73, .9)
    );
}

button:active {
    transform: scale(.97);
}

.primary {
    background: linear-gradient(
        180deg,
        #1689c7,
        #075183
    );
    box-shadow:
        0 0 25px rgba(24, 159, 230, .25),
        inset 0 1px rgba(255,255,255,.15);
}

.danger {
    border-color: rgba(255, 83, 105, .45);
}

#hud {
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: 0;
    transition: opacity .2s ease;
}

#hud.active {
    opacity: 1;
}

.hud-top {
    position: absolute;
    top: 16px;
    left: 16px;
    right: 16px;
    display: flex;
    justify-content: space-between;
    gap: 12px;
}

.hud-box {
    min-width: 115px;
    padding: 10px 14px;
    border: 1px solid rgba(79, 185, 235, .25);
    border-radius: 12px;
    background: rgba(2, 10, 22, .62);
    backdrop-filter: blur(10px);
}

.hud-label {
    font-size: 9px;
    color: #6d9ab5;
    letter-spacing: .15em;
    margin-bottom: 4px;
}

.hud-value {
    font-size: 18px;
    font-weight: 900;
}

.health-wrap {
    position: absolute;
    left: 16px;
    bottom: 18px;
    width: min(280px, 55vw);
}

.bar-label {
    font-size: 9px;
    letter-spacing: .15em;
    color: #75a8c1;
    margin-bottom: 5px;
}

.bar {
    width: 100%;
    height: 10px;
    border: 1px solid rgba(100, 200, 255, .3);
    background: rgba(0,0,0,.5);
    border-radius: 20px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    width: 100%;
    background: linear-gradient(90deg, #24bfff, #b9f1ff);
    box-shadow: 0 0 14px rgba(50, 193, 255, .8);
    transition: width .15s ease;
}

.shield-fill {
    background: linear-gradient(90deg, #586cff, #c4caff);
    box-shadow: 0 0 14px rgba(110, 120, 255, .8);
}

#pauseHud {
    position: absolute;
    top: 16px;
    right: 16px;
    pointer-events: auto;
}

#mobileControls {
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: 0;
}

#mobileControls.active {
    opacity: 1;
}

.joystick {
    position: absolute;
    left: 24px;
    bottom: 25px;
    width: 130px;
    height: 130px;
    border-radius: 50%;
    border: 1px solid rgba(95, 204, 255, .25);
    background: rgba(5, 25, 45, .35);
    pointer-events: auto;
}

.stick {
    position: absolute;
    width: 58px;
    height: 58px;
    left: 36px;
    top: 36px;
    border-radius: 50%;
    background: rgba(60, 177, 235, .35);
    border: 1px solid rgba(124, 220, 255, .6);
}

.mobile-actions {
    position: absolute;
    right: 22px;
    bottom: 22px;
    display: flex;
    gap: 12px;
    align-items: flex-end;
    pointer-events: auto;
}

.mobile-actions button {
    width: 78px;
    height: 78px;
    min-height: 78px;
    border-radius: 50%;
    padding: 5px;
    font-size: 11px;
}

.fire {
    width: 105px !important;
    height: 105px !important;
    min-height: 105px !important;
    border-color: rgba(85, 218, 255, .75);
    background: rgba(11, 105, 156, .55);
}

#pauseButton {
    position: absolute;
    right: 16px;
    top: 76px;
    width: 48px;
    height: 42px;
    min-height: 42px;
    padding: 0;
    pointer-events: auto;
    font-size: 18px;
}

.instructions {
    text-align: left;
    margin-top: 22px;
    line-height: 1.65;
    color: #a8c9dc;
    font-size: 14px;
}

.instructions strong {
    color: #e8f7ff;
}

.setting-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    border-bottom: 1px solid rgba(100, 180, 220, .12);
    color: #b7d8e8;
}

.toggle {
    width: 56px;
    height: 30px;
    min-height: 30px;
    border-radius: 30px;
    padding: 0;
    position: relative;
    background: #172536;
}

.toggle::after {
    content: "";
    position: absolute;
    width: 22px;
    height: 22px;
    top: 3px;
    left: 4px;
    border-radius: 50%;
    background: #7190a5;
    transition: .15s;
}

.toggle.on {
    background: #0879ae;
}

.toggle.on::after {
    left: 30px;
    background: white;
}

.small {
    color: #60869d;
    font-size: 11px;
    margin-top: 20px;
}

#damageFlash {
    position: fixed;
    inset: 0;
    pointer-events: none;
    background: rgba(255, 40, 70, .25);
    opacity: 0;
}

.gameover-score {
    margin: 25px 0;
    font-size: 42px;
    font-weight: 900;
    color: #8fe2ff;
}

@media (max-width: 600px) {
    .panel {
        padding: 25px 20px;
    }

    .hud-top {
        left: 10px;
        right: 10px;
        top: 10px;
    }

    .hud-box {
        min-width: 0;
        padding: 8px 10px;
    }

    .hud-value {
        font-size: 14px;
    }

    .health-wrap {
        bottom: 175px;
        left: 15px;
        width: 160px;
    }

    #pauseButton {
        top: 65px;
        right: 10px;
    }
}

@media (min-width: 800px) {
    #mobileControls {
        display: none !important;
    }
}
</style>
</head>

<body>

<canvas id="game"></canvas>

<div id="damageFlash"></div>

<!-- MAIN MENU -->
<div id="menu" class="screen active">
    <div class="panel">
        <div class="logo">VOID SPACE</div>
        <div class="subtitle">DEEP SPACE COMBAT SYSTEM</div>

        <div class="menu-buttons">
            <button class="primary" id="playBtn">START MISSION</button>
            <button id="howBtn">HOW TO PLAY</button>
            <button id="settingsBtn">SETTINGS</button>
            <button id="fullscreenBtn">FULLSCREEN</button>
        </div>

        <div class="small">
            SINGLE PLAYER • OFFLINE GAME • NO DATABASE
        </div>
    </div>
</div>

<!-- HOW TO PLAY -->
<div id="howScreen" class="screen">
    <div class="panel">
        <div class="logo" style="font-size:42px;">HOW TO PLAY</div>

        <div class="instructions">
            <p><strong>MISSION</strong><br>
            Survive as long as possible and destroy incoming enemy spacecraft.</p>

            <p><strong>DESKTOP</strong><br>
            WASD / Arrow Keys — Move<br>
            Mouse — Aim<br>
            Left Mouse / SPACE — Fire<br>
            SHIFT — Boost<br>
            P / ESC — Pause</p>

            <p><strong>MOBILE</strong><br>
            Use the virtual joystick to move.
            Hold FIRE to shoot.
            BOOST increases movement speed.</p>

            <p><strong>POWERUPS</strong><br>
            Blue shield capsules restore shield.
            Cyan rapid-fire capsules temporarily increase firing speed.</p>

            <p><strong>ENEMIES</strong><br>
            Small fighters attack quickly.
            Heavy ships are slower but have more health.</p>

            <p><strong>WAVES</strong><br>
            Each wave becomes progressively more difficult.</p>
        </div>

        <div class="menu-buttons">
            <button id="howBack">BACK</button>
        </div>
    </div>
</div>

<!-- SETTINGS -->
<div id="settingsScreen" class="screen">
    <div class="panel">
        <div class="logo" style="font-size:42px;">SETTINGS</div>

        <div class="setting-row">
            <span>Sound Effects</span>
            <button class="toggle on" id="soundToggle"></button>
        </div>

        <div class="setting-row">
            <span>Screen Shake</span>
            <button class="toggle on" id="shakeToggle"></button>
        </div>

        <div class="setting-row">
            <span>Mobile Controls</span>
            <button class="toggle on" id="mobileToggle"></button>
        </div>

        <div class="menu-buttons">
            <button id="settingsBack">BACK</button>
        </div>
    </div>
</div>

<!-- PAUSE -->
<div id="pauseScreen" class="screen">
    <div class="panel">
        <div class="logo" style="font-size:52px;">PAUSED</div>
        <div class="subtitle">MISSION SUSPENDED</div>

        <div class="menu-buttons">
            <button class="primary" id="resumeBtn">RESUME</button>
            <button id="restartBtn">RESTART</button>
            <button id="exitBtn">EXIT TO MENU</button>
        </div>
    </div>
</div>

<!-- GAME OVER -->
<div id="gameOverScreen" class="screen">
    <div class="panel">
        <div class="logo" style="font-size:48px;">MISSION LOST</div>
        <div class="subtitle">YOUR SHIP HAS BEEN DESTROYED</div>

        <div class="gameover-score" id="finalScore">0</div>

        <div id="finalStats" class="small"></div>

        <div class="menu-buttons">
            <button class="primary" id="againBtn">TRY AGAIN</button>
            <button id="gameOverExit">MAIN MENU</button>
        </div>
    </div>
</div>

<!-- HUD -->
<div id="hud">
    <div class="hud-top">
        <div class="hud-box">
            <div class="hud-label">SCORE</div>
            <div class="hud-value" id="score">0</div>
        </div>

        <div class="hud-box">
            <div class="hud-label">WAVE</div>
            <div class="hud-value" id="wave">1</div>
        </div>

        <div class="hud-box">
            <div class="hud-label">HOSTILES</div>
            <div class="hud-value" id="enemies">0</div>
        </div>
    </div>

    <button id="pauseButton">Ⅱ</button>

    <div class="health-wrap">
        <div class="bar-label">HULL</div>
        <div class="bar">
            <div class="bar-fill" id="hullBar"></div>
        </div>

        <div class="bar-label" style="margin-top:9px;">SHIELD</div>
        <div class="bar">
            <div class="bar-fill shield-fill" id="shieldBar"></div>
        </div>
    </div>
</div>

<!-- MOBILE -->
<div id="mobileControls">
    <div class="joystick" id="joystick">
        <div class="stick" id="stick"></div>
    </div>

    <div class="mobile-actions">
        <button id="boostButton">BOOST</button>
        <button class="fire" id="fireButton">FIRE</button>
    </div>
</div>

<script>
/*
    VOID SPACE
    Single-file browser game served by Python Flask.

    The Python file contains this complete HTML/CSS/JS payload.
*/

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let W = 0;
let H = 0;
let dpr = Math.min(window.devicePixelRatio || 1, 2);

function resize() {
    W = window.innerWidth;
    H = window.innerHeight;

    canvas.width = Math.floor(W * dpr);
    canvas.height = Math.floor(H * dpr);

    canvas.style.width = W + "px";
    canvas.style.height = H + "px";

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

window.addEventListener("resize", resize);
resize();

const keys = {};
const mouse = {
    x: W / 2,
    y: H / 2,
    down: false
};

document.addEventListener("keydown", e => {
    keys[e.key.toLowerCase()] = true;

    if (
        [" ", "arrowup", "arrowdown", "arrowleft", "arrowright"].includes(
            e.key.toLowerCase()
        )
    ) {
        e.preventDefault();
    }

    if (e.key === "Escape" || e.key.toLowerCase() === "p") {
        if (game.running) {
            togglePause();
        }
    }
});

document.addEventListener("keyup", e => {
    keys[e.key.toLowerCase()] = false;
});

canvas.addEventListener("mousemove", e => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
});

canvas.addEventListener("mousedown", e => {
    if (e.button === 0) {
        mouse.down = true;
        initAudio();
    }
});

window.addEventListener("mouseup", e => {
    if (e.button === 0) mouse.down = false;
});

let audioContext = null;

function initAudio() {
    if (!settings.sound) return;

    if (!audioContext) {
        try {
            audioContext = new (
                window.AudioContext ||
                window.webkitAudioContext
            )();
        } catch (e) {
            audioContext = null;
        }
    }

    if (audioContext && audioContext.state === "suspended") {
        audioContext.resume();
    }
}

function sound(type) {
    if (!settings.sound || !audioContext) return;

    const osc = audioContext.createOscillator();
    const gain = audioContext.createGain();

    osc.connect(gain);
    gain.connect(audioContext.destination);

    const now = audioContext.currentTime;

    if (type === "laser") {
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(620, now);
        osc.frequency.exponentialRampToValueAtTime(180, now + .08);
        gain.gain.setValueAtTime(.045, now);
        gain.gain.exponentialRampToValueAtTime(.001, now + .08);
        osc.start(now);
        osc.stop(now + .08);
    }

    if (type === "enemy") {
        osc.type = "square";
        osc.frequency.setValueAtTime(160, now);
        osc.frequency.exponentialRampToValueAtTime(70, now + .15);
        gain.gain.setValueAtTime(.03, now);
        gain.gain.exponentialRampToValueAtTime(.001, now + .15);
        osc.start(now);
        osc.stop(now + .15);
    }

    if (type === "hit") {
        osc.type = "triangle";
        osc.frequency.setValueAtTime(100, now);
        osc.frequency.exponentialRampToValueAtTime(40, now + .18);
        gain.gain.setValueAtTime(.08, now);
        gain.gain.exponentialRampToValueAtTime(.001, now + .18);
        osc.start(now);
        osc.stop(now + .18);
    }

    if (type === "power") {
        osc.type = "sine";
        osc.frequency.setValueAtTime(300, now);
        osc.frequency.exponentialRampToValueAtTime(900, now + .25);
        gain.gain.setValueAtTime(.07, now);
        gain.gain.exponentialRampToValueAtTime(.001, now + .25);
        osc.start(now);
        osc.stop(now + .25);
    }
}

const settings = {
    sound: true,
    shake: true,
    mobile: true
};

function screen(id, active) {
    document.getElementById(id).classList.toggle("active", active);
}

function showMenu() {
    game.running = false;
    game.paused = false;

    screen("menu", true);
    screen("howScreen", false);
    screen("settingsScreen", false);
    screen("pauseScreen", false);
    screen("gameOverScreen", false);

    document.getElementById("hud").classList.remove("active");
    document.getElementById("mobileControls").classList.remove("active");
}

document.getElementById("playBtn").onclick = () => {
    initAudio();
    startGame();
};

document.getElementById("howBtn").onclick = () => {
    screen("menu", false);
    screen("howScreen", true);
};

document.getElementById("settingsBtn").onclick = () => {
    screen("menu", false);
    screen("settingsScreen", true);
};

document.getElementById("howBack").onclick = () => {
    screen("howScreen", false);
    screen("menu", true);
};

document.getElementById("settingsBack").onclick = () => {
    screen("settingsScreen", false);
    screen("menu", true);
};

document.getElementById("fullscreenBtn").onclick = () => {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen?.();
    } else {
        document.exitFullscreen?.();
    }
};

function setupToggle(id, property) {
    const el = document.getElementById(id);

    el.onclick = () => {
        settings[property] = !settings[property];
        el.classList.toggle("on", settings[property]);

        if (property === "mobile") {
            updateMobileControls();
        }
    };
}

setupToggle("soundToggle", "sound");
setupToggle("shakeToggle", "shake");
setupToggle("mobileToggle", "mobile");

function updateMobileControls() {
    const isTouch =
        "ontouchstart" in window ||
        navigator.maxTouchPoints > 0;

    const active =
        settings.mobile &&
        isTouch &&
        game.running &&
        !game.paused;

    document
        .getElementById("mobileControls")
        .classList.toggle("active", active);
}

const player = {
    x: 0,
    y: 0,
    vx: 0,
    vy: 0,
    angle: 0,
    radius: 18,
    hull: 100,
    shield: 100,
    maxHull: 100,
    maxShield: 100,
    cooldown: 0,
    rapid: 0,
    invincible: 0
};

const game = {
    running: false,
    paused: false,
    score: 0,
    wave: 1,
    kills: 0,
    spawnTimer: 0,
    waveTimer: 0,
    shake: 0,
    stars: [],
    enemies: [],
    bullets: [],
    enemyBullets: [],
    particles: [],
    powerups: [],
    lastTime: 0
};

const joystick = {
    active: false,
    id: null,
    x: 0,
    y: 0
};

function createStars() {
    game.stars.length = 0;

    const count = Math.floor(
        Math.min(450, Math.max(150, W * H / 6000))
    );

    for (let i = 0; i < count; i++) {
        game.stars.push({
            x: Math.random() * W,
            y: Math.random() * H,
            z: Math.random(),
            size: Math.random() * 2 + .4,
            speed: Math.random() * .8 + .2
        });
    }
}

createStars();

function startGame() {
    screen("menu", false);
    screen("howScreen", false);
    screen("settingsScreen", false);
    screen("pauseScreen", false);
    screen("gameOverScreen", false);

    document.getElementById("hud").classList.add("active");

    game.running = true;
    game.paused = false;
    game.score = 0;
    game.wave = 1;
    game.kills = 0;
    game.spawnTimer = .5;
    game.waveTimer = 0;
    game.shake = 0;

    game.enemies.length = 0;
    game.bullets.length = 0;
    game.enemyBullets.length = 0;
    game.particles.length = 0;
    game.powerups.length = 0;

    player.x = W / 2;
    player.y = H * .78;
    player.vx = 0;
    player.vy = 0;
    player.hull = 100;
    player.shield = 100;
    player.cooldown = 0;
    player.rapid = 0;
    player.invincible = 1.5;

    createStars();
    updateHUD();
    updateMobileControls();

    game.lastTime = performance.now();
}

function togglePause() {
    if (!game.running) return;

    game.paused = !game.paused;

    screen("pauseScreen", game.paused);

    if (!game.paused) {
        game.lastTime = performance.now();
    }

    updateMobileControls();
}

document.getElementById("pauseButton").onclick = togglePause;
document.getElementById("resumeBtn").onclick = togglePause;

document.getElementById("restartBtn").onclick = () => {
    startGame();
};

document.getElementById("exitBtn").onclick = showMenu;

document.getElementById("againBtn").onclick = () => {
    startGame();
};

document.getElementById("gameOverExit").onclick = showMenu;

function spawnEnemy() {
    const heavy =
        Math.random() <
        Math.min(.35, .08 + game.wave * .012);

    const side = Math.floor(Math.random() * 3);

    let x;
    let y;

    if (side === 0) {
        x = Math.random() * W;
        y = -60;
    } else if (side === 1) {
        x = -60;
        y = Math.random() * H * .45;
    } else {
        x = W + 60;
        y = Math.random() * H * .45;
    }

    const hp = heavy
        ? 55 + game.wave * 8
        : 24 + game.wave * 4;

    game.enemies.push({
        x,
        y,
        vx: 0,
        vy: 0,
        r: heavy ? 28 : 18,
        hp,
        maxHp: hp,
        speed: heavy
            ? 35 + game.wave * 2
            : 65 + game.wave * 3,
        heavy,
        shoot: 1 + Math.random() * 2,
        wobble: Math.random() * Math.PI * 2,
        angle: 0
    });
}

function firePlayer() {
    if (player.cooldown > 0) return;

    const dx = mouse.x - player.x;
    const dy = mouse.y - player.y;

    let angle = Math.atan2(dy, dx);

    if (
        Math.abs(dx) < 3 &&
        Math.abs(dy) < 3
    ) {
        angle = -Math.PI / 2;
    }

    const speed = 650;

    game.bullets.push({
        x: player.x + Math.cos(angle) * 25,
        y: player.y + Math.sin(angle) * 25,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        life: 1.2,
        damage: player.rapid > 0 ? 18 : 25
    });

    player.cooldown = player.rapid > 0 ? .075 : .16;

    createMuzzle(
        player.x + Math.cos(angle) * 24,
        player.y + Math.sin(angle) * 24,
        angle
    );

    sound("laser");
}

function enemyFire(enemy) {
    const angle = Math.atan2(
        player.y - enemy.y,
        player.x - enemy.x
    );

    const speed = 230 + game.wave * 5;

    game.enemyBullets.push({
        x: enemy.x,
        y: enemy.y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        life: 5,
        damage: enemy.heavy ? 15 : 8
    });

    sound("enemy");
}

function createMuzzle(x, y, angle) {
    for (let i = 0; i < 5; i++) {
        game.particles.push({
            x,
            y,
            vx:
                Math.cos(angle) * (80 + Math.random() * 120) +
                (Math.random() - .5) * 50,
            vy:
                Math.sin(angle) * (80 + Math.random() * 120) +
                (Math.random() - .5) * 50,
            life: .18 + Math.random() * .15,
            maxLife: .3,
            size: 2 + Math.random() * 3,
            type: "laser"
        });
    }
}

function explosion(x, y, heavy = false) {
    const count = heavy ? 38 : 20;

    for (let i = 0; i < count; i++) {
        const a = Math.random() * Math.PI * 2;
        const s = Math.random() * (heavy ? 180 : 120);

        game.particles.push({
            x,
            y,
            vx: Math.cos(a) * s,
            vy: Math.sin(a) * s,
            life: .35 + Math.random() * .55,
            maxLife: 1,
            size: 1.5 + Math.random() * (heavy ? 5 : 3),
            type: "explosion"
        });
    }

    if (settings.shake) {
        game.shake = Math.min(
            16,
            game.shake + (heavy ? 10 : 5)
        );
    }

    sound("hit");
}

function damagePlayer(amount) {
    if (player.invincible > 0) return;

    let remaining = amount;

    if (player.shield > 0) {
        const absorbed = Math.min(
            player.shield,
            remaining
        );

        player.shield -= absorbed;
        remaining -= absorbed;
    }

    if (remaining > 0) {
        player.hull -= remaining;
    }

    player.invincible = .35;

    document.getElementById("damageFlash").animate(
        [
            { opacity: .7 },
            { opacity: 0 }
        ],
        { duration: 220 }
    );

    if (player.hull <= 0) {
        player.hull = 0;
        gameOver();
    }
}

function spawnPowerup(x, y) {
    if (Math.random() > .16) return;

    game.powerups.push({
        x,
        y,
        type: Math.random() < .55 ? "shield" : "rapid",
        life: 12,
        pulse: 0
    });
}

function collectPowerup(p) {
    if (p.type === "shield") {
        player.shield = Math.min(
            player.maxShield,
            player.shield + 45
        );
    } else {
        player.rapid = 8;
    }

    sound("power");
}

function updateStars(dt) {
    for (const s of game.stars) {
        s.y += (30 + s.z * 180) * dt;

        if (s.y > H + 5) {
            s.y = -5;
            s.x = Math.random() * W;
        }
    }
}

function updatePlayer(dt) {
    let ix = 0;
    let iy = 0;

    if (
        keys["w"] ||
        keys["arrowup"]
    ) iy -= 1;

    if (
        keys["s"] ||
        keys["arrowdown"]
    ) iy += 1;

    if (
        keys["a"] ||
        keys["arrowleft"]
    ) ix -= 1;

    if (
        keys["d"] ||
        keys["arrowright"]
    ) ix += 1;

    if (joystick.active) {
        ix = joystick.x;
        iy = joystick.y;
    }

    const length = Math.hypot(ix, iy);

    if (length > 1) {
        ix /= length;
        iy /= length;
    }

    const boosting =
        keys["shift"] ||
        boostHeld;

    const acceleration = boosting
        ? 950
        : 700;

    const maxSpeed = boosting
        ? 520
        : 350;

    player.vx += ix * acceleration * dt;
    player.vy += iy * acceleration * dt;

    const damping = Math.pow(.001, dt);

    player.vx *= damping;
    player.vy *= damping;

    const velocity =
        Math.hypot(player.vx, player.vy);

    if (velocity > maxSpeed) {
        player.vx =
            player.vx / velocity * maxSpeed;

        player.vy =
            player.vy / velocity * maxSpeed;
    }

    player.x += player.vx * dt;
    player.y += player.vy * dt;

    const margin = 25;

    player.x = Math.max(
        margin,
        Math.min(W - margin, player.x)
    );

    player.y = Math.max(
        margin,
        Math.min(H - margin, player.y)
    );

    if (
        mouse.x !== 0 ||
        mouse.y !== 0
    ) {
        player.angle = Math.atan2(
            mouse.y - player.y,
            mouse.x - player.x
        );
    }

    if (player.cooldown > 0) {
        player.cooldown -= dt;
    }

    if (player.rapid > 0) {
        player.rapid -= dt;
    }

    if (player.invincible > 0) {
        player.invincible -= dt;
    }

    const firing =
        mouse.down ||
        keys[" "] ||
        fireHeld;

    if (firing) {
        firePlayer();
    }

    if (player.shield < player.maxShield) {
        player.shield = Math.min(
            player.maxShield,
            player.shield + dt * 3
        );
    }
}

function updateEnemies(dt) {
    game.spawnTimer -= dt;

    const desired =
        Math.min(
            5 + game.wave * 1.2,
            18
        );

    if (
        game.spawnTimer <= 0 &&
        game.enemies.length < desired
    ) {
        spawnEnemy();

        game.spawnTimer =
            Math.max(
                .35,
                1.35 - game.wave * .035
            );
    }

    for (let i = game.enemies.length - 1; i >= 0; i--) {
        const e = game.enemies[i];

        const dx = player.x - e.x;
        const dy = player.y - e.y;
        const distance = Math.max(
            1,
            Math.hypot(dx, dy)
        );

        const nx = dx / distance;
        const ny = dy / distance;

        e.wobble += dt * (e.heavy ? 1 : 2);

        const sideForce =
            Math.sin(e.wobble) *
            (e.heavy ? 12 : 25);

        e.vx += (
            nx * e.speed +
            -ny * sideForce
        ) * dt;

        e.vy += (
            ny * e.speed +
            nx * sideForce
        ) * dt;

        const max =
            e.speed * 1.5;

        const v = Math.hypot(
            e.vx,
            e.vy
        );

        if (v > max) {
            e.vx = e.vx / v * max;
            e.vy = e.vy / v * max;
        }

        e.x += e.vx * dt;
        e.y += e.vy * dt;

        e.angle = Math.atan2(
            e.vy,
            e.vx
        );

        e.shoot -= dt;

        if (
            e.shoot <= 0 &&
            distance < 550
        ) {
            enemyFire(e);

            e.shoot =
                e.heavy
                    ? 1.6 + Math.random()
                    : 2.2 + Math.random() * 1.5;
        }

        if (
            distance <
            e.r + player.radius
        ) {
            damagePlayer(
                e.heavy ? 28 : 16
            );

            explosion(
                e.x,
                e.y,
                e.heavy
            );

            game.enemies.splice(i, 1);
        }
    }
}

function updateBullets(dt) {
    for (let i = game.bullets.length - 1; i >= 0; i--) {
        const b = game.bullets[i];

        b.x += b.vx * dt;
        b.y += b.vy * dt;
        b.life -= dt;

        let removed = false;

        for (
            let j = game.enemies.length - 1;
            j >= 0;
            j--
        ) {
            const e = game.enemies[j];

            const dx = b.x - e.x;
            const dy = b.y - e.y;

            if (
                dx * dx +
                dy * dy <
                (e.r + 5) *
                (e.r + 5)
            ) {
                e.hp -= b.damage;

                for (let p = 0; p < 4; p++) {
                    game.particles.push({
                        x: b.x,
                        y: b.y,
                        vx: (Math.random() - .5) * 100,
                        vy: (Math.random() - .5) * 100,
                        life: .2,
                        maxLife: .2,
                        size: 2,
                        type: "laser"
                    });
                }

                game.bullets.splice(i, 1);
                removed = true;

                if (e.hp <= 0) {
                    const reward =
                        e.heavy ? 250 : 100;

                    game.score +=
                        reward *
                        Math.max(1, game.wave);

                    game.kills++;

                    explosion(
                        e.x,
                        e.y,
                        e.heavy
                    );

                    spawnPowerup(
                        e.x,
                        e.y
                    );

                    game.enemies.splice(
                        j,
                        1
                    );
                }

                break;
            }
        }

        if (
            !removed &&
            (
                b.life <= 0 ||
                b.x < -50 ||
                b.x > W + 50 ||
                b.y < -50 ||
                b.y > H + 50
            )
        ) {
            game.bullets.splice(i, 1);
        }
    }
}

function updateEnemyBullets(dt) {
    for (
        let i = game.enemyBullets.length - 1;
        i >= 0;
        i--
    ) {
        const b = game.enemyBullets[i];

        b.x += b.vx * dt;
        b.y += b.vy * dt;
        b.life -= dt;

        const dx =
            b.x - player.x;

        const dy =
            b.y - player.y;

        if (
            dx * dx +
            dy * dy <
            (player.radius + 8) *
            (player.radius + 8)
        ) {
            damagePlayer(b.damage);
            game.enemyBullets.splice(i, 1);
            continue;
        }

        if (
            b.life <= 0 ||
            b.x < -40 ||
            b.x > W + 40 ||
            b.y < -40 ||
            b.y > H + 40
        ) {
            game.enemyBullets.splice(i, 1);
        }
    }
}

function updateParticles(dt) {
    for (
        let i = game.particles.length - 1;
        i >= 0;
        i--
    ) {
        const p = game.particles[i];

        p.x += p.vx * dt;
        p.y += p.vy * dt;

        p.vx *= Math.pow(.08, dt);
        p.vy *= Math.pow(.08, dt);

        p.life -= dt;

        if (p.life <= 0) {
            game.particles.splice(i, 1);
        }
    }
}

function updatePowerups(dt) {
    for (
        let i = game.powerups.length - 1;
        i >= 0;
        i--
    ) {
        const p = game.powerups[i];

        p.y += 25 * dt;
        p.life -= dt;
        p.pulse += dt * 5;

        const dx =
            p.x - player.x;

        const dy =
            p.y - player.y;

        if (
            dx * dx +
            dy * dy <
            30 * 30
        ) {
            collectPowerup(p);
            game.powerups.splice(i, 1);
            continue;
        }

        if (p.life <= 0) {
            game.powerups.splice(i, 1);
        }
    }
}

function updateWave(dt) {
    game.waveTimer += dt;

    const targetWave =
        1 +
        Math.floor(
            game.kills / 8
        );

    if (targetWave > game.wave) {
        game.wave = targetWave;
        player.shield = Math.min(
            player.maxShield,
            player.shield + 25
        );
    }
}

function updateHUD() {
    document.getElementById("score").textContent =
        Math.floor(game.score).toLocaleString();

    document.getElementById("wave").textContent =
        game.wave;

    document.getElementById("enemies").textContent =
        game.enemies.length;

    document.getElementById("hullBar").style.width =
        Math.max(
            0,
            player.hull
        ) + "%";

    document.getElementById("shieldBar").style.width =
        Math.max(
            0,
            player.shield
        ) + "%";
}

function drawBackground() {
    const gradient = ctx.createRadialGradient(
        W / 2,
        H / 2,
        0,
        W / 2,
        H / 2,
        Math.max(W, H) * .8
    );

    gradient.addColorStop(
        0,
        "#0a1b35"
    );

    gradient.addColorStop(
        .55,
        "#030b19"
    );

    gradient.addColorStop(
        1,
        "#01030a"
    );

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, W, H);

    for (const s of game.stars) {
        const alpha =
            .25 +
            s.z * .75;

        ctx.globalAlpha = alpha;

        ctx.fillStyle = "#bfeaff";

        const size =
            s.size *
            (.6 + s.z * 1.4);

        ctx.fillRect(
            s.x,
            s.y,
            size,
            size
        );
    }

    ctx.globalAlpha = 1;

    // distant grid / space lanes
    ctx.strokeStyle =
        "rgba(30,120,170,.055)";

    ctx.lineWidth = 1;

    const spacing = 90;

    for (
        let x = 0;
        x < W;
        x += spacing
    ) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(
            W / 2 +
            (x - W / 2) * .25,
            H
        );
        ctx.stroke();
    }
}

function drawPlayer() {
    ctx.save();

    ctx.translate(
        player.x,
        player.y
    );

    ctx.rotate(
        player.angle + Math.PI / 2
    );

    if (player.invincible > 0) {
        ctx.globalAlpha =
            .45 +
            Math.sin(performance.now() * .03) * .25;
    }

    // engine glow
    const glow =
        ctx.createRadialGradient(
            0,
            22,
            1,
            0,
            22,
            25
        );

    glow.addColorStop(
        0,
        "rgba(140,240,255,.9)"
    );

    glow.addColorStop(
        1,
        "rgba(20,140,255,0)"
    );

    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(
        0,
        22,
        25,
        0,
        Math.PI * 2
    );
    ctx.fill();

    // ship body
    ctx.beginPath();
    ctx.moveTo(0, -28);
    ctx.lineTo(15, 14);
    ctx.lineTo(7, 11);
    ctx.lineTo(0, 25);
    ctx.lineTo(-7, 11);
    ctx.lineTo(-15, 14);
    ctx.closePath();

    const body = ctx.createLinearGradient(
        -15,
        -28,
        15,
        25
    );

    body.addColorStop(
        0,
        "#e9fbff"
    );

    body.addColorStop(
        .45,
        "#56cfff"
    );

    body.addColorStop(
        1,
        "#07588b"
    );

    ctx.fillStyle = body;
    ctx.fill();

    ctx.strokeStyle =
        "rgba(180,245,255,.9)";

    ctx.lineWidth = 1.5;
    ctx.stroke();

    // wings
    ctx.beginPath();
    ctx.moveTo(-9, 3);
    ctx.lineTo(-28, 16);
    ctx.lineTo(-9, 14);
    ctx.closePath();
    ctx.fillStyle = "#146f9e";
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(9, 3);
    ctx.lineTo(28, 16);
    ctx.lineTo(9, 14);
    ctx.closePath();
    ctx.fill();

    // cockpit
    ctx.beginPath();
    ctx.ellipse(
        0,
        -7,
        5,
        9,
        0,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#071f38";
    ctx.fill();

    ctx.strokeStyle = "#7de8ff";
    ctx.stroke();

    ctx.restore();
}

function drawEnemy(e) {
    ctx.save();

    ctx.translate(
        e.x,
        e.y
    );

    ctx.rotate(
        e.angle + Math.PI / 2
    );

    const color =
        e.heavy
            ? "#ff6681"
            : "#d83d6a";

    // glow
    const glow =
        ctx.createRadialGradient(
            0,
            0,
            2,
            0,
            0,
            e.r * 1.8
        );

    glow.addColorStop(
        0,
        e.heavy
            ? "rgba(255,80,110,.35)"
            : "rgba(220,40,100,.25)"
    );

    glow.addColorStop(
        1,
        "rgba(255,30,80,0)"
    );

    ctx.fillStyle = glow;

    ctx.beginPath();
    ctx.arc(
        0,
        0,
        e.r * 1.8,
        0,
        Math.PI * 2
    );

    ctx.fill();

    if (e.heavy) {
        ctx.beginPath();
        ctx.moveTo(0, -30);
        ctx.lineTo(24, 8);
        ctx.lineTo(17, 27);
        ctx.lineTo(0, 19);
        ctx.lineTo(-17, 27);
        ctx.lineTo(-24, 8);
        ctx.closePath();

        ctx.fillStyle = "#541329";
        ctx.fill();

        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.fillStyle = "#ffb1bd";

        ctx.beginPath();
        ctx.arc(
            0,
            -5,
            6,
            0,
            Math.PI * 2
        );

        ctx.fill();
    } else {
        ctx.beginPath();
        ctx.moveTo(0, -23);
        ctx.lineTo(14, 17);
        ctx.lineTo(0, 10);
        ctx.lineTo(-14, 17);
        ctx.closePath();

        ctx.fillStyle = "#451124";
        ctx.fill();

        ctx.strokeStyle = color;
        ctx.lineWidth = 1.5;
        ctx.stroke();

        ctx.fillStyle = "#ff7b9a";

        ctx.beginPath();
        ctx.arc(
            0,
            -4,
            4,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }

    ctx.restore();

    // health bar
    const barW = e.r * 2.2;

    ctx.fillStyle =
        "rgba(0,0,0,.55)";

    ctx.fillRect(
        e.x - barW / 2,
        e.y - e.r - 9,
        barW,
        3
    );

    ctx.fillStyle =
        e.heavy
            ? "#ff7189"
            : "#e75d87";

    ctx.fillRect(
        e.x - barW / 2,
        e.y - e.r - 9,
        barW * (e.hp / e.maxHp),
        3
    );
}

function drawBullets() {
    for (const b of game.bullets) {
        const angle =
            Math.atan2(
                b.vy,
                b.vx
            );

        ctx.save();

        ctx.translate(
            b.x,
            b.y
        );

        ctx.rotate(angle);

        ctx.shadowBlur = 14;
        ctx.shadowColor = "#6ee7ff";

        ctx.fillStyle = "#d9fbff";

        ctx.fillRect(
            -10,
            -2,
            20,
            4
        );

        ctx.restore();
    }

    for (const b of game.enemyBullets) {
        const angle =
            Math.atan2(
                b.vy,
                b.vx
            );

        ctx.save();

        ctx.translate(
            b.x,
            b.y
        );

        ctx.rotate(angle);

        ctx.shadowBlur = 12;
        ctx.shadowColor = "#ff5070";

        ctx.fillStyle = "#ffb0bd";

        ctx.fillRect(
            -7,
            -2,
            14,
            4
        );

        ctx.restore();
    }
}

function drawParticles() {
    for (const p of game.particles) {
        const alpha =
            Math.max(
                0,
                p.life / p.maxLife
            );

        ctx.globalAlpha = alpha;

        ctx.fillStyle =
            p.type === "laser"
                ? "#8feaff"
                : "#ff9a63";

        ctx.beginPath();

        ctx.arc(
            p.x,
            p.y,
            p.size,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }

    ctx.globalAlpha = 1;
}

function drawPowerups() {
    for (const p of game.powerups) {
        const pulse =
            Math.sin(p.pulse) * 3;

        ctx.save();

        ctx.translate(
            p.x,
            p.y
        );

        ctx.shadowBlur = 20;

        ctx.shadowColor =
            p.type === "shield"
                ? "#6677ff"
                : "#55eaff";

        ctx.strokeStyle =
            p.type === "shield"
                ? "#8896ff"
                : "#65ecff";

        ctx.lineWidth = 3;

        ctx.beginPath();

        ctx.arc(
            0,
            0,
            13 + pulse,
            0,
            Math.PI * 2
        );

        ctx.stroke();

        ctx.fillStyle =
            p.type === "shield"
                ? "rgba(100,120,255,.25)"
                : "rgba(60,220,255,.25)";

        ctx.fill();

        ctx.fillStyle = "#eaffff";
        ctx.font = "bold 11px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        ctx.fillText(
            p.type === "shield"
                ? "S"
                : "R",
            0,
            0
        );

        ctx.restore();
    }
}

function drawCrosshair() {
    if (
        "ontouchstart" in window ||
        navigator.maxTouchPoints > 0
    ) {
        return;
    }

    ctx.save();

    ctx.translate(
        mouse.x,
        mouse.y
    );

    ctx.strokeStyle =
        "rgba(130,225,255,.65)";

    ctx.lineWidth = 1;

    ctx.beginPath();
    ctx.arc(
        0,
        0,
        10,
        0,
        Math.PI * 2
    );

    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(-17, 0);
    ctx.lineTo(-5, 0);
    ctx.moveTo(5, 0);
    ctx.lineTo(17, 0);
    ctx.moveTo(0, -17);
    ctx.lineTo(0, -5);
    ctx.moveTo(0, 5);
    ctx.lineTo(0, 17);

    ctx.stroke();

    ctx.restore();
}

function draw() {
    ctx.clearRect(
        0,
        0,
        W,
        H
    );

    let sx = 0;
    let sy = 0;

    if (
        settings.shake &&
        game.shake > 0
    ) {
        sx =
            (Math.random() - .5) *
            game.shake;

        sy =
            (Math.random() - .5) *
            game.shake;
    }

    ctx.save();
    ctx.translate(sx, sy);

    drawBackground();
    drawPowerups();
    drawBullets();

    for (const e of game.enemies) {
        drawEnemy(e);
    }

    drawPlayer();
    drawParticles();
    drawCrosshair();

    ctx.restore();

    if (game.shake > 0) {
        game.shake *= .9;

        if (game.shake < .1) {
            game.shake = 0;
        }
    }
}

function gameOver() {
    game.running = false;
    game.paused = false;

    document.getElementById("finalScore").textContent =
        Math.floor(game.score).toLocaleString();

    document.getElementById("finalStats").textContent =
        "WAVE " +
        game.wave +
        " • HOSTILES DESTROYED " +
        game.kills;

    document.getElementById("hud").classList.remove("active");
    document.getElementById("mobileControls").classList.remove("active");

    screen("gameOverScreen", true);

    explosion(
        player.x,
        player.y,
        true
    );
}

let fireHeld = false;
let boostHeld = false;

// FIRE button
const fireButton =
    document.getElementById("fireButton");

fireButton.addEventListener(
    "pointerdown",
    e => {
        e.preventDefault();
        fireHeld = true;
        initAudio();
    }
);

fireButton.addEventListener(
    "pointerup",
    e => {
        e.preventDefault();
        fireHeld = false;
    }
);

fireButton.addEventListener(
    "pointercancel",
    () => {
        fireHeld = false;
    }
);

fireButton.addEventListener(
    "pointerleave",
    () => {
        fireHeld = false;
    }
);

// BOOST button
const boostButton =
    document.getElementById("boostButton");

boostButton.addEventListener(
    "pointerdown",
    e => {
        e.preventDefault();
        boostHeld = true;
    }
);

boostButton.addEventListener(
    "pointerup",
    e => {
        e.preventDefault();
        boostHeld = false;
    }
);

boostButton.addEventListener(
    "pointercancel",
    () => {
        boostHeld = false;
    }
);

boostButton.addEventListener(
    "pointerleave",
    () => {
        boostHeld = false;
    }
);

// Joystick
const joystickElement =
    document.getElementById("joystick");

const stickElement =
    document.getElementById("stick");

function joystickMove(clientX, clientY) {
    const rect =
        joystickElement.getBoundingClientRect();

    const cx =
        rect.left + rect.width / 2;

    const cy =
        rect.top + rect.height / 2;

    let dx =
        clientX - cx;

    let dy =
        clientY - cy;

    const max =
        rect.width * .32;

    const distance =
        Math.hypot(dx, dy);

    if (distance > max) {
        dx =
            dx / distance * max;

        dy =
            dy / distance * max;
    }

    joystick.x =
        dx / max;

    joystick.y =
        dy / max;

    stickElement.style.transform =
        `translate(${dx}px, ${dy}px)`;
}

joystickElement.addEventListener(
    "pointerdown",
    e => {
        e.preventDefault();

        joystick.active = true;
        joystick.id = e.pointerId;

        joystickElement.setPointerCapture(
            e.pointerId
        );

        joystickMove(
            e.clientX,
            e.clientY
        );
    }
);

joystickElement.addEventListener(
    "pointermove",
    e => {
        if (
            joystick.active &&
            e.pointerId === joystick.id
        ) {
            joystickMove(
                e.clientX,
                e.clientY
            );
        }
    }
);

function joystickEnd(e) {
    if (
        e.pointerId === joystick.id
    ) {
        joystick.active = false;
        joystick.id = null;
        joystick.x = 0;
        joystick.y = 0;

        stickElement.style.transform =
            "translate(0, 0)";
    }
}

joystickElement.addEventListener(
    "pointerup",
    joystickEnd
);

joystickElement.addEventListener(
    "pointercancel",
    joystickEnd
);

function update(dt) {
    if (!game.running || game.paused) {
        return;
    }

    dt = Math.min(
        dt,
        .033
    );

    updateStars(dt);
    updatePlayer(dt);
    updateEnemies(dt);
    updateBullets(dt);
    updateEnemyBullets(dt);
    updateParticles(dt);
    updatePowerups(dt);
    updateWave(dt);

    updateHUD();
}

function loop(now) {
    const dt =
        (now - game.lastTime) /
        1000;

    game.lastTime = now;

    update(dt);
    draw();

    requestAnimationFrame(loop);
}

game.lastTime =
    performance.now();

requestAnimationFrame(loop);

window.addEventListener(
    "blur",
    () => {
        mouse.down = false;
        fireHeld = false;
        boostHeld = false;

        if (game.running && !game.paused) {
            togglePause();
        }
    }
);
</script>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/health")
def health():
    return "VOID SPACE ONLINE"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
