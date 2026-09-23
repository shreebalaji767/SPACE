from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,
               initial-scale=1.0,
               maximum-scale=1.0,
               minimum-scale=1.0,
               user-scalable=no,
               viewport-fit=cover">

<meta name="theme-color" content="#050914">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">

<title>VOID SPACE</title>

<style>
/* =========================================================
   RESET
========================================================= */

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-tap-highlight-color: transparent;
    user-select: none;
}

html,
body {
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #02040a;
    color: white;
    font-family:
        Inter,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

/* =========================================================
   GAME ROOT
========================================================= */

#app {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background:
        radial-gradient(
            circle at center,
            #09152d 0%,
            #040814 45%,
            #010207 100%
        );
}

/* Canvas always fills the actual viewport */

#gameCanvas {
    position: absolute;
    inset: 0;
    display: block;
    width: 100%;
    height: 100%;
    touch-action: none;
}

/* =========================================================
   UI
========================================================= */

.screen {
    position: absolute;
    inset: 0;

    display: flex;
    align-items: center;
    justify-content: center;

    padding:
        max(20px, env(safe-area-inset-top))
        max(20px, env(safe-area-inset-right))
        max(20px, env(safe-area-inset-bottom))
        max(20px, env(safe-area-inset-left));

    background:
        radial-gradient(
            circle at center,
            rgba(10, 25, 55, .45),
            rgba(0, 0, 0, .78)
        );

    z-index: 20;
}

.hidden {
    display: none !important;
}

.panel {
    width: min(92vw, 560px);
    max-height: 90vh;
    overflow-y: auto;

    padding: clamp(22px, 5vw, 42px);

    border: 1px solid rgba(120, 180, 255, .25);
    border-radius: clamp(16px, 3vw, 28px);

    background:
        linear-gradient(
            145deg,
            rgba(13, 25, 50, .94),
            rgba(3, 8, 20, .96)
        );

    box-shadow:
        0 30px 100px rgba(0, 0, 0, .7),
        inset 0 0 40px rgba(80, 140, 255, .04);

    backdrop-filter: blur(14px);
}

.logo {
    text-align: center;
    font-size: clamp(42px, 9vw, 86px);
    font-weight: 1000;
    letter-spacing: clamp(5px, 1.5vw, 15px);
    line-height: .95;

    color: #ffffff;

    text-shadow:
        0 0 8px rgba(100, 180, 255, .9),
        0 0 30px rgba(50, 120, 255, .6),
        0 0 80px rgba(30, 80, 255, .35);
}

.subtitle {
    margin-top: 14px;
    text-align: center;
    color: #8298bc;
    font-size: clamp(11px, 2vw, 15px);
    letter-spacing: 3px;
}

.menu-buttons {
    display: grid;
    gap: 12px;
    margin-top: clamp(28px, 5vh, 45px);
}

button {
    border: 0;
    outline: 0;

    min-height: 48px;
    padding: 13px 20px;

    border-radius: 13px;

    color: white;
    background:
        linear-gradient(
            135deg,
            rgba(45, 90, 170, .7),
            rgba(18, 35, 70, .85)
        );

    border: 1px solid rgba(130, 190, 255, .22);

    font-size: clamp(13px, 2vw, 16px);
    font-weight: 800;
    letter-spacing: 1px;

    cursor: pointer;

    transition:
        transform .15s ease,
        background .15s ease,
        border-color .15s ease;
}

button:hover {
    transform: translateY(-2px);
    border-color: rgba(150, 210, 255, .5);
    background:
        linear-gradient(
            135deg,
            rgba(65, 125, 220, .8),
            rgba(20, 45, 90, .9)
        );
}

button:active {
    transform: scale(.97);
}

/* =========================================================
   HUD
========================================================= */

#hud {
    position: absolute;
    inset:
        max(10px, env(safe-area-inset-top))
        max(10px, env(safe-area-inset-right))
        auto
        max(10px, env(safe-area-inset-left));

    z-index: 10;

    display: none;

    pointer-events: none;
}

.hud-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 10px;
}

.hud-box {
    min-width: 100px;
    padding: 8px 11px;

    border-radius: 10px;

    background: rgba(3, 8, 18, .55);
    border: 1px solid rgba(130, 180, 255, .16);

    backdrop-filter: blur(8px);
}

.hud-label {
    color: #6e86aa;
    font-size: 9px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.hud-value {
    margin-top: 2px;
    font-size: clamp(14px, 2.4vw, 21px);
    font-weight: 900;
}

.health-container {
    width: clamp(110px, 20vw, 230px);
}

.health-bar {
    height: 7px;
    margin-top: 5px;
    overflow: hidden;
    border-radius: 20px;
    background: rgba(255,255,255,.1);
}

#healthFill {
    width: 100%;
    height: 100%;
    background: #59e58b;
    transition: width .15s linear;
}

.energy-bar {
    height: 5px;
    margin-top: 4px;
    overflow: hidden;
    border-radius: 20px;
    background: rgba(255,255,255,.1);
}

#energyFill {
    width: 100%;
    height: 100%;
    background: #62b8ff;
}

/* =========================================================
   BOSS BAR
========================================================= */

#bossBar {
    position: absolute;

    top: max(70px, calc(env(safe-area-inset-top) + 60px));
    left: 50%;
    transform: translateX(-50%);

    width: min(75vw, 650px);

    display: none;

    z-index: 11;
    pointer-events: none;
}

.boss-title {
    text-align: center;
    margin-bottom: 5px;

    color: #ff7384;

    font-size: clamp(10px, 2vw, 15px);
    font-weight: 1000;
    letter-spacing: 3px;
}

.boss-track {
    height: clamp(7px, 1.5vw, 12px);

    overflow: hidden;
    border-radius: 20px;

    background: rgba(255,255,255,.1);
    border: 1px solid rgba(255,100,120,.3);
}

#bossFill {
    width: 100%;
    height: 100%;
    background: #ff405d;
}

/* =========================================================
   PAUSE BUTTON
========================================================= */

#pauseButton {
    position: absolute;

    top: max(12px, env(safe-area-inset-top));
    right: max(12px, env(safe-area-inset-right));

    z-index: 15;

    width: 44px;
    height: 44px;

    min-height: 44px;
    padding: 0;

    display: none;

    border-radius: 50%;

    font-size: 16px;

    pointer-events: auto;
}

/* =========================================================
   MOBILE CONTROLS
========================================================= */

#mobileControls {
    position: absolute;
    inset: auto 0
        max(12px, env(safe-area-inset-bottom))
        0;

    z-index: 12;

    display: none;

    height: min(32vh, 260px);

    pointer-events: none;
}

.joystick {
    position: absolute;

    left: max(18px, env(safe-area-inset-left) + 12px);
    bottom: 12px;

    width: clamp(110px, 28vw, 170px);
    height: clamp(110px, 28vw, 170px);

    border-radius: 50%;

    background: rgba(90, 140, 210, .08);
    border: 1px solid rgba(150, 200, 255, .2);

    pointer-events: auto;
    touch-action: none;
}

.joystick-knob {
    position: absolute;

    left: 50%;
    top: 50%;

    width: 38%;
    height: 38%;

    transform: translate(-50%, -50%);

    border-radius: 50%;

    background: rgba(100, 170, 255, .35);
    border: 1px solid rgba(180, 220, 255, .5);

    box-shadow: 0 0 30px rgba(80, 160, 255, .25);
}

.mobile-actions {
    position: absolute;

    right: max(18px, env(safe-area-inset-right) + 12px);
    bottom: 12px;

    display: flex;
    align-items: flex-end;
    gap: 10px;

    pointer-events: auto;
}

.action-button {
    width: clamp(62px, 17vw, 92px);
    height: clamp(62px, 17vw, 92px);

    min-height: 0;
    padding: 0;

    border-radius: 50%;

    background: rgba(30, 65, 110, .28);
    border: 1px solid rgba(130, 190, 255, .3);

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: clamp(10px, 2.7vw, 14px);
}

.fire-button {
    width: clamp(78px, 20vw, 110px);
    height: clamp(78px, 20vw, 110px);
    background: rgba(170, 50, 75, .22);
}

.boost-button {
    background: rgba(50, 130, 190, .2);
}

/* =========================================================
   IN-GAME INFO
========================================================= */

#comboText {
    position: absolute;

    left: 50%;
    top: 28%;

    transform: translate(-50%, -50%) scale(.8);

    opacity: 0;

    z-index: 13;

    pointer-events: none;

    font-size: clamp(22px, 6vw, 52px);
    font-weight: 1000;
    letter-spacing: 2px;

    text-shadow: 0 0 30px rgba(100, 180, 255, .8);

    transition:
        opacity .2s ease,
        transform .2s ease;
}

#comboText.show {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
}

/* =========================================================
   RESPONSIVE BREAKPOINTS
========================================================= */

/* Tablets */

@media (max-width: 900px) {

    .panel {
        width: min(94vw, 600px);
    }

    .hud-box {
        min-width: 85px;
    }
}

/* Phones */

@media (max-width: 700px) {

    .panel {
        width: 94vw;
        max-height: 86vh;
        padding: 24px 18px;
    }

    .logo {
        letter-spacing: 5px;
    }

    .hud-row {
        gap: 5px;
    }

    .hud-box {
        min-width: 0;
        padding: 6px 8px;
    }

    .hud-label {
        font-size: 7px;
    }

    #pauseButton {
        width: 40px;
        height: 40px;
    }
}

/* Very small phones */

@media (max-width: 380px) {

    .hud-box:nth-child(4) {
        display: none;
    }

    .mobile-actions {
        gap: 6px;
    }

    .joystick {
        left: 12px;
    }

    .mobile-actions {
        right: 12px;
    }
}

/* Landscape phones */

@media (max-height: 520px) and (orientation: landscape) {

    .panel {
        max-height: 90vh;
        padding: 18px 24px;
    }

    .logo {
        font-size: clamp(30px, 8vh, 54px);
    }

    .subtitle {
        margin-top: 5px;
    }

    .menu-buttons {
        margin-top: 15px;
        gap: 7px;
    }

    button {
        min-height: 38px;
        padding: 8px 15px;
    }

    #mobileControls {
        height: 45vh;
    }

    .joystick {
        width: min(30vh, 140px);
        height: min(30vh, 140px);
    }

    .action-button {
        width: min(19vh, 75px);
        height: min(19vh, 75px);
    }

    .fire-button {
        width: min(23vh, 90px);
        height: min(23vh, 90px);
    }
}

/* Prevent mobile browser selection */

@media (pointer: coarse) {

    button {
        min-height: 48px;
    }
}

/* Desktop */

@media (pointer: fine) and (min-width: 701px) {

    #mobileControls {
        display: none !important;
    }
}
</style>
</head>

<body>

<div id="app">

<canvas id="gameCanvas"></canvas>

<!-- =====================================================
     HUD
===================================================== -->

<div id="hud">

    <div class="hud-row">

        <div class="hud-box">
            <div class="hud-label">Score</div>
            <div class="hud-value" id="score">0</div>
        </div>

        <div class="hud-box">
            <div class="hud-label">Wave</div>
            <div class="hud-value" id="wave">1</div>
        </div>

        <div class="hud-box">
            <div class="hud-label">Kills</div>
            <div class="hud-value" id="kills">0</div>
        </div>

        <div class="hud-box health-container">
            <div class="hud-label">Hull</div>
            <div class="health-bar">
                <div id="healthFill"></div>
            </div>

            <div class="hud-label" style="margin-top:4px">
                Energy
            </div>

            <div class="energy-bar">
                <div id="energyFill"></div>
            </div>
        </div>

    </div>

</div>

<!-- =====================================================
     BOSS
===================================================== -->

<div id="bossBar">

    <div class="boss-title">
        VOID OVERLORD
    </div>

    <div class="boss-track">
        <div id="bossFill"></div>
    </div>

</div>

<!-- =====================================================
     PAUSE
===================================================== -->

<button id="pauseButton">Ⅱ</button>

<!-- =====================================================
     COMBO
===================================================== -->

<div id="comboText">
    COMBO ×2
</div>

<!-- =====================================================
     MOBILE
===================================================== -->

<div id="mobileControls">

    <div id="joystick" class="joystick">
        <div id="joystickKnob" class="joystick-knob"></div>
    </div>

    <div class="mobile-actions">

        <button
            id="boostButton"
            class="action-button boost-button">
            BOOST
        </button>

        <button
            id="fireButton"
            class="action-button fire-button">
            FIRE
        </button>

    </div>

</div>

<!-- =====================================================
     MAIN MENU
===================================================== -->

<div id="menuScreen" class="screen">

    <div class="panel">

        <div class="logo">
            VOID
        </div>

        <div class="logo" style="font-size:.55em;margin-top:6px">
            SPACE
        </div>

        <div class="subtitle">
            SURVIVE THE VOID
        </div>

        <div class="menu-buttons">

            <button id="playButton">
                ▶ START MISSION
            </button>

            <button id="howButton">
                ? HOW TO PLAY
            </button>

            <button id="settingsButton">
                ⚙ SETTINGS
            </button>

        </div>

    </div>

</div>

<!-- =====================================================
     HOW TO PLAY
===================================================== -->

<div id="howScreen" class="screen hidden">

    <div class="panel">

        <h2 style="text-align:center;margin-bottom:20px">
            HOW TO PLAY
        </h2>

        <div style="
            color:#aebed8;
            line-height:1.7;
            font-size:14px;
        ">

            <p>
                <b>Desktop</b>
            </p>

            <p>
                WASD / Arrow Keys — Move<br>
                Mouse — Aim<br>
                Left Mouse — Fire<br>
                Shift — Boost<br>
                P / Escape — Pause
            </p>

            <br>

            <p>
                <b>Mobile / Tablet</b>
            </p>

            <p>
                Left joystick — Move<br>
                FIRE — Shoot<br>
                BOOST — Boost
            </p>

            <br>

            <p>
                Destroy enemies, collect powerups,
                survive waves and defeat the Void Overlord.
            </p>

            <br>

            <p>
                Every fifth wave contains a boss.
            </p>

        </div>

        <div style="margin-top:22px">
            <button id="howBack">
                ← BACK
            </button>
        </div>

    </div>

</div>

<!-- =====================================================
     SETTINGS
===================================================== -->

<div id="settingsScreen" class="screen hidden">

    <div class="panel">

        <h2 style="text-align:center;margin-bottom:25px">
            SETTINGS
        </h2>

        <div class="menu-buttons">

            <button id="soundToggle">
                SOUND: ON
            </button>

            <button id="shakeToggle">
                SCREEN SHAKE: ON
            </button>

            <button id="particlesToggle">
                PARTICLES: ON
            </button>

            <button id="fullscreenButton">
                ⛶ FULLSCREEN
            </button>

            <button id="settingsBack">
                ← BACK
            </button>

        </div>

    </div>

</div>

<!-- =====================================================
     PAUSE SCREEN
===================================================== -->

<div id="pauseScreen" class="screen hidden">

    <div class="panel">

        <h2 style="text-align:center">
            PAUSED
        </h2>

        <div class="menu-buttons">

            <button id="resumeButton">
                ▶ RESUME
            </button>

            <button id="pauseMenuButton">
                MAIN MENU
            </button>

        </div>

    </div>

</div>

<!-- =====================================================
     GAME OVER
===================================================== -->

<div id="gameOverScreen" class="screen hidden">

    <div class="panel">

        <div class="logo"
             style="font-size:clamp(34px,8vw,65px)">
            DESTROYED
        </div>

        <div class="subtitle">
            MISSION TERMINATED
        </div>

        <div style="
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:10px;
            margin-top:28px;
        ">

            <div class="hud-box">
                <div class="hud-label">Score</div>
                <div class="hud-value" id="finalScore">
                    0
                </div>
            </div>

            <div class="hud-box">
                <div class="hud-label">Wave</div>
                <div class="hud-value" id="finalWave">
                    1
                </div>
            </div>

            <div class="hud-box">
                <div class="hud-label">Kills</div>
                <div class="hud-value" id="finalKills">
                    0
                </div>
            </div>

            <div class="hud-box">
                <div class="hud-label">Combo</div>
                <div class="hud-value" id="finalCombo">
                    1
                </div>
            </div>

        </div>

        <div class="menu-buttons">

            <button id="restartButton">
                ↻ PLAY AGAIN
            </button>

            <button id="gameOverMenuButton">
                MAIN MENU
            </button>

        </div>

    </div>

</div>

</div>

<script>
/* =========================================================
   CANVAS
========================================================= */

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d", {
    alpha: false
});

let W = 0;
let H = 0;
let DPR = 1;

/* =========================================================
   RESPONSIVE CANVAS
========================================================= */

function resizeCanvas() {

    const rect = canvas.getBoundingClientRect();

    DPR = Math.min(
        window.devicePixelRatio || 1,
        2
    );

    W = Math.max(1, rect.width);
    H = Math.max(1, rect.height);

    canvas.width = Math.floor(W * DPR);
    canvas.height = Math.floor(H * DPR);

    ctx.setTransform(
        DPR,
        0,
        0,
        DPR,
        0,
        0
    );
}

window.addEventListener(
    "resize",
    resizeCanvas,
    { passive: true }
);

window.addEventListener(
    "orientationchange",
    () => {
        setTimeout(resizeCanvas, 100);
    },
    { passive: true }
);

resizeCanvas();

/* =========================================================
   UI
========================================================= */

const menuScreen = document.getElementById("menuScreen");
const howScreen = document.getElementById("howScreen");
const settingsScreen = document.getElementById("settingsScreen");
const pauseScreen = document.getElementById("pauseScreen");
const gameOverScreen = document.getElementById("gameOverScreen");

const hud = document.getElementById("hud");
const pauseButton = document.getElementById("pauseButton");
const mobileControls = document.getElementById("mobileControls");

const scoreEl = document.getElementById("score");
const waveEl = document.getElementById("wave");
const killsEl = document.getElementById("kills");

const healthFill = document.getElementById("healthFill");
const energyFill = document.getElementById("energyFill");

const bossBar = document.getElementById("bossBar");
const bossFill = document.getElementById("bossFill");

const comboText = document.getElementById("comboText");

/* =========================================================
   SETTINGS
========================================================= */

const settings = {

    sound: true,
    shake: true,
    particles: true

};

/* =========================================================
   GAME STATE
========================================================= */

let running = false;
let paused = false;
let lastTime = 0;

const game = {

    score: 0,

    kills: 0,

    wave: 1,

    combo: 1,

    comboTimer: 0,

    spawnTimer: 0,

    boss: null,

    screenShake: 0,

    time: 0

};

/* =========================================================
   PLAYER
========================================================= */

const player = {

    x: 0,
    y: 0,

    vx: 0,
    vy: 0,

    radius: 15,

    angle: 0,

    speed: 420,

    health: 100,
    maxHealth: 100,

    energy: 100,
    maxEnergy: 100,

    fireCooldown: 0,

    invincible: 0,

    rapid: 0,
    spread: 0,
    shield: 0,

    boost: false

};

/* =========================================================
   ARRAYS
========================================================= */

const stars = [];
const enemies = [];
const bullets = [];
const enemyBullets = [];
const particles = [];
const powerups = [];

/* =========================================================
   INPUT
========================================================= */

const keys = {};

const mouse = {

    x: 0,
    y: 0,
    down: false

};

const joystickInput = {

    x: 0,
    y: 0,
    active: false

};

let touchFire = false;
let touchBoost = false;

window.addEventListener(
    "keydown",
    e => {

        keys[e.key.toLowerCase()] = true;

        if (
            e.key === "Escape" ||
            e.key.toLowerCase() === "p"
        ) {
            togglePause();
        }

        if (e.key === " ") {
            e.preventDefault();
        }

    }
);

window.addEventListener(
    "keyup",
    e => {
        keys[e.key.toLowerCase()] = false;
    }
);

canvas.addEventListener(
    "mousemove",
    e => {

        const r = canvas.getBoundingClientRect();

        mouse.x = e.clientX - r.left;
        mouse.y = e.clientY - r.top;

    },
    { passive: true }
);

canvas.addEventListener(
    "mousedown",
    e => {

        if (e.button === 0) {
            mouse.down = true;
            initAudio();
        }

    }
);

window.addEventListener(
    "mouseup",
    e => {

        if (e.button === 0) {
            mouse.down = false;
        }

    }
);

/* =========================================================
   AUDIO
========================================================= */

let audioCtx = null;

function initAudio() {

    if (!settings.sound) return;

    if (!audioCtx) {

        try {

            audioCtx =
                new (
                    window.AudioContext ||
                    window.webkitAudioContext
                )();

        } catch (e) {

            audioCtx = null;

        }

    }

    if (
        audioCtx &&
        audioCtx.state === "suspended"
    ) {
        audioCtx.resume();
    }
}

function beep(
    frequency = 440,
    duration = .05,
    type = "sine",
    volume = .025
) {

    if (!settings.sound) return;

    initAudio();

    if (!audioCtx) return;

    const osc =
        audioCtx.createOscillator();

    const gain =
        audioCtx.createGain();

    osc.type = type;
    osc.frequency.value = frequency;

    gain.gain.setValueAtTime(
        volume,
        audioCtx.currentTime
    );

    gain.gain.exponentialRampToValueAtTime(
        .001,
        audioCtx.currentTime + duration
    );

    osc.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start();
    osc.stop(
        audioCtx.currentTime + duration
    );
}

/* =========================================================
   STARS
========================================================= */

function createStars() {

    stars.length = 0;

    const count = Math.floor(
        Math.min(
            450,
            Math.max(
                100,
                (W * H) / 6500
            )
        )
    );

    for (let i = 0; i < count; i++) {

        stars.push({

            x: Math.random() * W,
            y: Math.random() * H,

            size:
                Math.random() *
                1.8 + .3,

            speed:
                Math.random() *
                35 + 8,

            alpha:
                Math.random() *
                .8 + .2

        });

    }
}

createStars();

/* =========================================================
   HELPERS
========================================================= */

function rand(min, max) {

    return Math.random() *
        (max - min) + min;

}

function clamp(value, min, max) {

    return Math.max(
        min,
        Math.min(max, value)
    );

}

function distance(a, b) {

    const dx = a.x - b.x;
    const dy = a.y - b.y;

    return Math.sqrt(
        dx * dx + dy * dy
    );

}

function angleTo(a, b) {

    return Math.atan2(
        b.y - a.y,
        b.x - a.x
    );

}

/* =========================================================
   PARTICLES
========================================================= */

function particleBurst(
    x,
    y,
    amount = 12,
    power = 120,
    size = 3
) {

    if (!settings.particles) return;

    for (let i = 0; i < amount; i++) {

        const a =
            Math.random() *
            Math.PI * 2;

        const speed =
            Math.random() *
            power;

        particles.push({

            x,
            y,

            vx:
                Math.cos(a) * speed,

            vy:
                Math.sin(a) * speed,

            life:
                Math.random() *
                .5 + .25,

            maxLife:
                .75,

            size:
                Math.random() *
                size + 1

        });

    }

}

function updateParticles(dt) {

    for (
        let i = particles.length - 1;
        i >= 0;
        i--
    ) {

        const p = particles[i];

        p.x += p.vx * dt;
        p.y += p.vy * dt;

        p.vx *= .97;
        p.vy *= .97;

        p.life -= dt;

        if (p.life <= 0) {

            particles.splice(i, 1);

        }

    }

}

function drawParticles() {

    if (!settings.particles) return;

    for (const p of particles) {

        const alpha =
            p.life / p.maxLife;

        ctx.globalAlpha = alpha;

        ctx.fillStyle = "#b8dfff";

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

/* =========================================================
   RESET GAME
========================================================= */

function resetGame() {

    game.score = 0;
    game.kills = 0;
    game.wave = 1;
    game.combo = 1;
    game.comboTimer = 0;
    game.spawnTimer = 0;
    game.boss = null;
    game.screenShake = 0;
    game.time = 0;

    enemies.length = 0;
    bullets.length = 0;
    enemyBullets.length = 0;
    particles.length = 0;
    powerups.length = 0;

    player.x = W / 2;
    player.y = H / 2;

    player.vx = 0;
    player.vy = 0;

    player.health = player.maxHealth;

    player.energy = player.maxEnergy;

    player.fireCooldown = 0;

    player.invincible = 1;

    player.rapid = 0;
    player.spread = 0;
    player.shield = 0;

    createStars();

    updateHUD();

}

/* =========================================================
   START
========================================================= */

function startGame() {

    initAudio();

    resetGame();

    running = true;
    paused = false;

    menuScreen.classList.add("hidden");
    howScreen.classList.add("hidden");
    settingsScreen.classList.add("hidden");
    pauseScreen.classList.add("hidden");
    gameOverScreen.classList.add("hidden");

    hud.style.display = "block";
    pauseButton.style.display = "block";

    if (isTouchDevice()) {

        mobileControls.style.display =
            "block";

    } else {

        mobileControls.style.display =
            "none";

    }

    lastTime = performance.now();

    requestAnimationFrame(loop);

}

/* =========================================================
   DEVICE DETECTION
========================================================= */

function isTouchDevice() {

    return (
        "ontouchstart" in window ||
        navigator.maxTouchPoints > 0
    );

}

/* =========================================================
   PLAYER
========================================================= */

function updatePlayer(dt) {

    let ax = 0;
    let ay = 0;

    if (keys["w"] || keys["arrowup"]) {
        ay -= 1;
    }

    if (keys["s"] || keys["arrowdown"]) {
        ay += 1;
    }

    if (keys["a"] || keys["arrowleft"]) {
        ax -= 1;
    }

    if (keys["d"] || keys["arrowright"]) {
        ax += 1;
    }

    if (joystickInput.active) {

        ax += joystickInput.x;
        ay += joystickInput.y;

    }

    const length =
        Math.sqrt(
            ax * ax + ay * ay
        );

    if (length > 1) {

        ax /= length;
        ay /= length;

    }

    const boosting =
        keys["shift"] ||
        touchBoost;

    player.boost = boosting &&
                   player.energy > 0 &&
                   length > .05;

    const targetSpeed =
        player.boost
            ? player.speed * 1.85
            : player.speed;

    const acceleration =
        player.boost
            ? 13
            : 9;

    player.vx +=
        (
            ax * targetSpeed -
            player.vx
        ) *
        acceleration *
        dt;

    player.vy +=
        (
            ay * targetSpeed -
            player.vy
        ) *
        acceleration *
        dt;

    player.x += player.vx * dt;
    player.y += player.vy * dt;

    const margin =
        Math.max(
            18,
            Math.min(
                35,
                W * .03
            )
        );

    player.x =
        clamp(
            player.x,
            margin,
            W - margin
        );

    player.y =
        clamp(
            player.y,
            margin,
            H - margin
        );

    if (player.boost) {

        player.energy -=
            42 * dt;

        particleBurst(
            player.x -
            Math.cos(player.angle) * 15,
            player.y -
            Math.sin(player.angle) * 15,
            1,
            30,
            2
        );

    } else {

        player.energy +=
            20 * dt;

    }

    player.energy =
        clamp(
            player.energy,
            0,
            player.maxEnergy
        );

    if (mouse.x !== 0 || mouse.y !== 0) {

        player.angle =
            Math.atan2(
                mouse.y - player.y,
                mouse.x - player.x
            );

    }

    player.fireCooldown -= dt;

    const firing =
        mouse.down ||
        keys[" "] ||
        touchFire;

    if (firing) {

        firePlayer();

    }

    if (player.invincible > 0) {

        player.invincible -= dt;

    }

    if (player.rapid > 0) {
        player.rapid -= dt;
    }

    if (player.spread > 0) {
        player.spread -= dt;
    }

    if (player.shield > 0) {
        player.shield -= dt;
    }

}

/* =========================================================
   PLAYER FIRE
========================================================= */

function firePlayer() {

    if (player.fireCooldown > 0) {
        return;
    }

    const cooldown =
        player.rapid > 0
            ? .075
            : .18;

    player.fireCooldown = cooldown;

    const angles = [];

    if (player.spread > 0) {

        angles.push(
            player.angle - .22,
            player.angle,
            player.angle + .22
        );

    } else {

        angles.push(
            player.angle
        );

    }

    for (const angle of angles) {

        bullets.push({

            x:
                player.x +
                Math.cos(angle) * 18,

            y:
                player.y +
                Math.sin(angle) * 18,

            vx:
                Math.cos(angle) * 850,

            vy:
                Math.sin(angle) * 850,

            life: 1.5,

            damage:
                player.spread > 0
                    ? 12
                    : 18

        });

    }

    beep(
        420,
        .035,
        "square",
        .018
    );

}

/* =========================================================
   SPAWN ENEMY
========================================================= */

function spawnEnemy() {

    const side =
        Math.floor(
            Math.random() * 4
        );

    let x;
    let y;

    if (side === 0) {
        x = -40;
        y = Math.random() * H;
    } else if (side === 1) {
        x = W + 40;
        y = Math.random() * H;
    } else if (side === 2) {
        x = Math.random() * W;
        y = -40;
    } else {
        x = Math.random() * W;
        y = H + 40;
    }

    const roll = Math.random();

    let type;

    if (game.wave < 3) {

        type =
            roll < .7
                ? "scout"
                : "shooter";

    } else {

        if (roll < .45) {
            type = "scout";
        } else if (roll < .7) {
            type = "shooter";
        } else if (roll < .9) {
            type = "tank";
        } else {
            type = "elite";
        }

    }

    const data = {

        scout: {
            radius: 14,
            hp: 25,
            speed: 120,
            score: 100
        },

        shooter: {
            radius: 17,
            hp: 45,
            speed: 75,
            score: 180
        },

        tank: {
            radius: 25,
            hp: 130,
            speed: 48,
            score: 350
        },

        elite: {
            radius: 21,
            hp: 85,
            speed: 105,
            score: 500
        }

    }[type];

    const difficulty =
        1 +
        (game.wave - 1) * .12;

    enemies.push({

        x,
        y,

        vx: 0,
        vy: 0,

        type,

        radius: data.radius,

        hp:
            data.hp * difficulty,

        maxHp:
            data.hp * difficulty,

        speed:
            data.speed *
            (
                1 +
                Math.min(
                    .6,
                    (game.wave - 1) * .025
                )
            ),

        score: data.score,

        fireTimer:
            rand(.5, 2),

        phase:
            Math.random() * 10,

        hitFlash: 0

    });

}

/* =========================================================
   UPDATE ENEMIES
========================================================= */

function updateEnemies(dt) {

    for (
        let i = enemies.length - 1;
        i >= 0;
        i--
    ) {

        const e = enemies[i];

        e.phase += dt;

        const angle =
            angleTo(e, player);

        let desiredSpeed = e.speed;

        if (e.type === "tank") {

            desiredSpeed =
                e.speed;

        }

        if (e.type === "shooter") {

            const d =
                distance(e, player);

            if (d < 320) {

                desiredSpeed *= -.45;

            }

        }

        if (e.type === "elite") {

            desiredSpeed =
                e.speed *
                (
                    .8 +
                    Math.sin(e.phase * 3) *
                    .25
                );

        }

        const targetVx =
            Math.cos(angle) *
            desiredSpeed;

        const targetVy =
            Math.sin(angle) *
            desiredSpeed;

        e.vx +=
            (
                targetVx -
                e.vx
            ) *
            3 *
            dt;

        e.vy +=
            (
                targetVy -
                e.vy
            ) *
            3 *
            dt;

        e.x += e.vx * dt;
        e.y += e.vy * dt;

        e.fireTimer -= dt;

        if (
            (
                e.type === "shooter" ||
                e.type === "elite"
            ) &&
            e.fireTimer <= 0
        ) {

            enemyShoot(e);

            e.fireTimer =
                e.type === "elite"
                    ? rand(.8, 1.5)
                    : rand(1.2, 2.4);

        }

        e.hitFlash -= dt;

        /* Enemy hits player */

        if (
            distance(e, player) <
            e.radius + player.radius
        ) {

            damagePlayer(
                e.type === "tank"
                    ? 25
                    : 15
            );

            destroyEnemy(i);

            continue;

        }

        /* Remove very distant enemies */

        if (
            e.x < -200 ||
            e.x > W + 200 ||
            e.y < -200 ||
            e.y > H + 200
        ) {

            enemies.splice(i, 1);

        }

    }

}

/* =========================================================
   ENEMY SHOOT
========================================================= */

function enemyShoot(e) {

    const angle =
        angleTo(e, player);

    enemyBullets.push({

        x: e.x,
        y: e.y,

        vx:
            Math.cos(angle) * 260,

        vy:
            Math.sin(angle) * 260,

        radius: 5,

        damage:
            e.type === "elite"
                ? 12
                : 9,

        life: 4

    });

    beep(
        180,
        .045,
        "sawtooth",
        .008
    );

}

/* =========================================================
   BULLETS
========================================================= */

function updateBullets(dt) {

    for (
        let i = bullets.length - 1;
        i >= 0;
        i--
    ) {

        const b = bullets[i];

        b.x += b.vx * dt;
        b.y += b.vy * dt;

        b.life -= dt;

        let remove = false;

        /* Enemy collision */

        for (
            let j = enemies.length - 1;
            j >= 0;
            j--
        ) {

            const e = enemies[j];

            if (
                Math.hypot(
                    b.x - e.x,
                    b.y - e.y
                ) <
                e.radius + 5
            ) {

                e.hp -= b.damage;
                e.hitFlash = .08;

                particleBurst(
                    b.x,
                    b.y,
                    4,
                    50,
                    2
                );

                remove = true;

                if (e.hp <= 0) {

                    destroyEnemy(j);

                }

                break;

            }

        }

        /* Boss collision */

        if (
            game.boss &&
            !remove
        ) {

            const boss =
                game.boss;

            if (
                Math.hypot(
                    b.x - boss.x,
                    b.y - boss.y
                ) <
                boss.radius + 5
            ) {

                boss.hp -= b.damage;

                boss.hitFlash = .08;

                particleBurst(
                    b.x,
                    b.y,
                    5,
                    70,
                    2
                );

                remove = true;

                if (boss.hp <= 0) {

                    defeatBoss();

                }

            }

        }

        if (
            b.life <= 0 ||
            b.x < -50 ||
            b.x > W + 50 ||
            b.y < -50 ||
            b.y > H + 50
        ) {

            remove = true;

        }

        if (remove) {

            bullets.splice(i, 1);

        }

    }

}

/* =========================================================
   ENEMY BULLETS
========================================================= */

function updateEnemyBullets(dt) {

    for (
        let i = enemyBullets.length - 1;
        i >= 0;
        i--
    ) {

        const b =
            enemyBullets[i];

        b.x += b.vx * dt;
        b.y += b.vy * dt;

        b.life -= dt;

        if (
            distance(b, player) <
            b.radius +
            player.radius
        ) {

            damagePlayer(
                b.damage
            );

            particleBurst(
                b.x,
                b.y,
                7,
                80,
                2
            );

            enemyBullets.splice(
                i,
                1
            );

            continue;

        }

        if (
            b.life <= 0 ||
            b.x < -100 ||
            b.x > W + 100 ||
            b.y < -100 ||
            b.y > H + 100
        ) {

            enemyBullets.splice(
                i,
                1
            );

        }

    }

}

/* =========================================================
   DESTROY ENEMY
========================================================= */

function destroyEnemy(index) {

    const e =
        enemies[index];

    if (!e) return;

    game.kills++;

    game.score +=
        Math.floor(
            e.score *
            game.combo
        );

    game.combo =
        Math.min(
            20,
            game.combo + .1
        );

    game.comboTimer = 2.5;

    particleBurst(
        e.x,
        e.y,
        e.type === "tank"
            ? 35
            : 18,
        e.type === "tank"
            ? 240
            : 150,
        e.type === "tank"
            ? 5
            : 3
    );

    if (settings.shake) {

        game.screenShake =
            Math.min(
                15,
                game.screenShake +
                (
                    e.type === "tank"
                        ? 7
                        : 3
                )
            );

    }

    if (
        Math.random() <
        (
            e.type === "tank"
                ? .22
                : .10
        )
    ) {

        spawnPowerup(
            e.x,
            e.y
        );

    }

    beep(
        e.type === "tank"
            ? 90
            : 130,
        .08,
        "sawtooth",
        .025
    );

    enemies.splice(
        index,
        1
    );

    showCombo();

}

/* =========================================================
   BOSS
========================================================= */

function spawnBoss() {

    enemies.length = 0;
    enemyBullets.length = 0;

    const maxHp =
        1200 +
        game.wave * 260;

    game.boss = {

        x: W / 2,

        y: -150,

        vx: 0,

        vy: 0,

        radius:
            Math.min(
                85,
                Math.max(
                    55,
                    Math.min(W, H) * .12
                )
            ),

        hp: maxHp,

        maxHp,

        angle: 0,

        phase: 0,

        fireTimer: 2,

        hitFlash: 0

    };

    bossBar.style.display =
        "block";

    beep(
        60,
        .6,
        "sawtooth",
        .05
    );

}

/* =========================================================
   UPDATE BOSS
========================================================= */

function updateBoss(dt) {

    const boss =
        game.boss;

    if (!boss) return;

    boss.phase += dt;

    boss.hitFlash -= dt;

    if (boss.y < H * .24) {

        boss.y +=
            70 * dt;

    }

    const targetX =
        W / 2 +
        Math.sin(
            boss.phase * .7
        ) *
        W *
        .32;

    boss.vx +=
        (
            targetX -
            boss.x
        ) *
        1.2 *
        dt;

    boss.vx *= .97;

    boss.x +=
        boss.vx * dt;

    boss.x =
        clamp(
            boss.x,
            boss.radius + 20,
            W -
            boss.radius -
            20
        );

    boss.angle =
        angleTo(
            boss,
            player
        );

    boss.fireTimer -= dt;

    if (boss.fireTimer <= 0) {

        bossShoot();

        boss.fireTimer =
            Math.max(
                .45,
                1.4 -
                game.wave * .025
            );

    }

    if (
        distance(
            boss,
            player
        ) <
        boss.radius +
        player.radius
    ) {

        damagePlayer(35);

    }

    bossFill.style.width =
        (
            Math.max(
                0,
                boss.hp /
                boss.maxHp
            ) *
            100
        ) + "%";

}

/* =========================================================
   BOSS SHOOT
========================================================= */

function bossShoot() {

    const boss =
        game.boss;

    if (!boss) return;

    const aimed =
        angleTo(
            boss,
            player
        );

    /* Aimed shots */

    for (
        let i = -1;
        i <= 1;
        i++
    ) {

        const angle =
            aimed + i * .18;

        enemyBullets.push({

            x: boss.x,
            y: boss.y,

            vx:
                Math.cos(angle) *
                310,

            vy:
                Math.sin(angle) *
                310,

            radius: 7,

            damage: 13,

            life: 5

        });

    }

    /* Radial attack occasionally */

    if (
        Math.random() <
        .35
    ) {

        const count = 12;

        for (
            let i = 0;
            i < count;
            i++
        ) {

            const angle =
                (
                    Math.PI * 2 *
                    i / count
                ) +
                boss.phase;

            enemyBullets.push({

                x: boss.x,
                y: boss.y,

                vx:
                    Math.cos(angle) *
                    170,

                vy:
                    Math.sin(angle) *
                    170,

                radius: 5,

                damage: 8,

                life: 5

            });

        }

    }

    beep(
        80,
        .15,
        "sawtooth",
        .035
    );

}

/* =========================================================
   BOSS DEFEATED
========================================================= */

function defeatBoss() {

    const boss =
        game.boss;

    if (!boss) return;

    game.score +=
        5000 *
        game.wave;

    game.combo += 3;

    particleBurst(
        boss.x,
        boss.y,
        100,
        450,
        8
    );

    game.screenShake = 25;

    beep(
        40,
        .8,
        "sawtooth",
        .08
    );

    game.boss = null;

    bossBar.style.display =
        "none";

    player.health =
        Math.min(
            player.maxHealth,
            player.health + 35
        );

    player.energy =
        player.maxEnergy;

    game.wave++;

    game.spawnTimer = 0;

}

/* =========================================================
   POWERUPS
========================================================= */

function spawnPowerup(x, y) {

    const types = [
        "heal",
        "shield",
        "rapid",
        "spread",
        "energy"
    ];

    powerups.push({

        x,
        y,

        type:
            types[
                Math.floor(
                    Math.random() *
                    types.length
                )
            ],

        radius: 13,

        life: 12,

        phase:
            Math.random() * 10

    });

}

function updatePowerups(dt) {

    for (
        let i = powerups.length - 1;
        i >= 0;
        i--
    ) {

        const p =
            powerups[i];

        p.life -= dt;

        p.phase += dt * 4;

        if (
            distance(
                p,
                player
            ) <
            p.radius +
            player.radius
        ) {

            collectPowerup(p);

            powerups.splice(
                i,
                1
            );

            continue;

        }

        if (p.life <= 0) {

            powerups.splice(
                i,
                1
            );

        }

    }

}

function collectPowerup(p) {

    if (p.type === "heal") {

        player.health =
            Math.min(
                player.maxHealth,
                player.health + 30
            );

    }

    if (p.type === "shield") {

        player.shield = 8;

    }

    if (p.type === "rapid") {

        player.rapid = 10;

    }

    if (p.type === "spread") {

        player.spread = 10;

    }

    if (p.type === "energy") {

        player.energy =
            player.maxEnergy;

    }

    game.score += 250;

    particleBurst(
        p.x,
        p.y,
        20,
        150,
        4
    );

    beep(
        700,
        .12,
        "sine",
        .025
    );

}

/* =========================================================
   DAMAGE PLAYER
========================================================= */

function damagePlayer(amount) {

    if (!running) return;

    if (
        player.invincible > 0
    ) return;

    if (player.shield > 0) {

        player.shield -=
            .5;

        particleBurst(
            player.x,
            player.y,
            12,
            120,
            3
        );

        game.screenShake = 5;

        return;

    }

    player.health -= amount;

    player.invincible = .6;

    game.screenShake = 10;

    particleBurst(
        player.x,
        player.y,
        15,
        180,
        4
    );

    beep(
        100,
        .12,
        "square",
        .035
    );

    if (
        player.health <= 0
    ) {

        gameOver();

    }

}

/* =========================================================
   WAVE SYSTEM
========================================================= */

function updateWave(dt) {

    if (game.boss) {
        return;
    }

    const required =
        8 +
        game.wave * 3;

    if (
        game.kills >=
        required *
        game.wave
    ) {

        game.wave++;

        beep(
            500,
            .25,
            "triangle",
            .035
        );

        if (
            game.wave % 5 === 0
        ) {

            spawnBoss();

        }

    }

}

/* =========================================================
   SPAWNING
========================================================= */

function updateSpawning(dt) {

    game.spawnTimer -= dt;

    if (
        game.boss
    ) {

        return;

    }

    const maxEnemies =
        Math.min(
            25,
            4 +
            game.wave * 2
        );

    if (
        game.spawnTimer <= 0 &&
        enemies.length <
        maxEnemies
    ) {

        spawnEnemy();

        game.spawnTimer =
            Math.max(
                .18,
                1.05 -
                game.wave * .035
            );

    }

}

/* =========================================================
   COMBO
========================================================= */

function updateCombo(dt) {

    if (
        game.comboTimer > 0
    ) {

        game.comboTimer -= dt;

    } else {

        game.combo =
            Math.max(
                1,
                game.combo - dt * .7
            );

    }

}

function showCombo() {

    if (
        game.combo < 1.1
    ) return;

    comboText.textContent =
        "COMBO ×" +
        Math.floor(game.combo);

    comboText.classList.add(
        "show"
    );

    clearTimeout(
        showCombo.timer
    );

    showCombo.timer =
        setTimeout(
            () => {
                comboText.classList.remove(
                    "show"
                );
            },
            550
        );

}

/* =========================================================
   STARS
========================================================= */

function updateStars(dt) {

    for (const s of stars) {

        s.y +=
            s.speed *
            dt;

        if (s.y > H) {

            s.y = 0;
            s.x = Math.random() * W;

        }

    }

}

function drawStars() {

    for (const s of stars) {

        ctx.globalAlpha =
            s.alpha;

        ctx.fillStyle =
            "#b7cfff";

        ctx.fillRect(
            s.x,
            s.y,
            s.size,
            s.size
        );

    }

    ctx.globalAlpha = 1;

}

/* =========================================================
   BACKGROUND
========================================================= */

function drawBackground() {

    const gradient =
        ctx.createRadialGradient(
            W / 2,
            H / 2,
            0,
            W / 2,
            H / 2,
            Math.max(W, H)
        );

    gradient.addColorStop(
        0,
        "#08172f"
    );

    gradient.addColorStop(
        .55,
        "#040a18"
    );

    gradient.addColorStop(
        1,
        "#010207"
    );

    ctx.fillStyle =
        gradient;

    ctx.fillRect(
        0,
        0,
        W,
        H
    );

    drawStars();

    /* subtle grid */

    ctx.globalAlpha = .06;

    ctx.strokeStyle =
        "#78aaff";

    const grid =
        Math.max(
            45,
            Math.min(
                90,
                W / 12
            )
        );

    for (
        let x = 0;
        x < W;
        x += grid
    ) {

        ctx.beginPath();

        ctx.moveTo(
            x,
            0
        );

        ctx.lineTo(
            x,
            H
        );

        ctx.stroke();

    }

    for (
        let y = 0;
        y < H;
        y += grid
    ) {

        ctx.beginPath();

        ctx.moveTo(
            0,
            y
        );

        ctx.lineTo(
            W,
            y
        );

        ctx.stroke();

    }

    ctx.globalAlpha = 1;

}

/* =========================================================
   DRAW PLAYER
========================================================= */

function drawPlayer() {

    if (
        player.invincible > 0 &&
        Math.floor(
            player.invincible * 15
        ) % 2 === 0
    ) {
        return;
    }

    ctx.save();

    ctx.translate(
        player.x,
        player.y
    );

    ctx.rotate(
        player.angle
    );

    /* Engine */

    ctx.beginPath();

    ctx.moveTo(
        -18,
        0
    );

    ctx.lineTo(
        -34,
        -7
    );

    ctx.lineTo(
        -28,
        0
    );

    ctx.lineTo(
        -34,
        7
    );

    ctx.closePath();

    ctx.fillStyle =
        "#4ec9ff";

    ctx.shadowBlur = 18;
    ctx.shadowColor =
        "#4ec9ff";

    ctx.fill();

    /* Ship */

    ctx.shadowBlur = 20;
    ctx.shadowColor =
        "#7ce4ff";

    ctx.beginPath();

    ctx.moveTo(
        25,
        0
    );

    ctx.lineTo(
        -13,
        -14
    );

    ctx.lineTo(
        -7,
        0
    );

    ctx.lineTo(
        -13,
        14
    );

    ctx.closePath();

    ctx.fillStyle =
        "#e8f8ff";

    ctx.fill();

    ctx.beginPath();

    ctx.moveTo(
        15,
        0
    );

    ctx.lineTo(
        -8,
        -7
    );

    ctx.lineTo(
        -5,
        7
    );

    ctx.closePath();

    ctx.fillStyle =
        "#4e9cff";

    ctx.fill();

    ctx.restore();

    /* Shield */

    if (player.shield > 0) {

        ctx.save();

        ctx.globalAlpha =
            .35 +
            Math.sin(
                performance.now() / 120
            ) * .12;

        ctx.strokeStyle =
            "#63c9ff";

        ctx.lineWidth = 3;

        ctx.shadowBlur = 20;
        ctx.shadowColor =
            "#63c9ff";

        ctx.beginPath();

        ctx.arc(
            player.x,
            player.y,
            player.radius + 9,
            0,
            Math.PI * 2
        );

        ctx.stroke();

        ctx.restore();

    }

}

/* =========================================================
   DRAW ENEMIES
========================================================= */

function drawEnemies() {

    for (const e of enemies) {

        ctx.save();

        ctx.translate(
            e.x,
            e.y
        );

        ctx.rotate(
            e.phase
        );

        ctx.shadowBlur =
            e.type === "tank"
                ? 24
                : 15;

        ctx.shadowColor =
            e.type === "tank"
                ? "#ff7b4d"
                : "#ff496b";

        ctx.fillStyle =
            e.hitFlash > 0
                ? "#ffffff"
                : (
                    e.type === "tank"
                        ? "#ff704d"
                        : e.type === "elite"
                            ? "#c16cff"
                            : "#ff4567"
                );

        if (
            e.type === "tank"
        ) {

            ctx.fillRect(
                -e.radius,
                -e.radius,
                e.radius * 2,
                e.radius * 2
            );

        } else {

            ctx.beginPath();

            ctx.moveTo(
                e.radius,
                0
            );

            ctx.lineTo(
                -e.radius,
                -e.radius
            );

            ctx.lineTo(
                -e.radius * .45,
                0
            );

            ctx.lineTo(
                -e.radius,
                e.radius
            );

            ctx.closePath();

            ctx.fill();

        }

        ctx.restore();

        /* HP */

        if (
            e.hp <
            e.maxHp
        ) {

            const width =
                e.radius * 2;

            ctx.fillStyle =
                "rgba(255,255,255,.12)";

            ctx.fillRect(
                e.x - width / 2,
                e.y - e.radius - 9,
                width,
                3
            );

            ctx.fillStyle =
                "#ff536d";

            ctx.fillRect(
                e.x - width / 2,
                e.y - e.radius - 9,
                width *
                clamp(
                    e.hp /
                    e.maxHp,
                    0,
                    1
                ),
                3
            );

        }

    }

}

/* =========================================================
   DRAW BOSS
========================================================= */

function drawBoss() {

    const boss =
        game.boss;

    if (!boss) return;

    ctx.save();

    ctx.translate(
        boss.x,
        boss.y
    );

    ctx.rotate(
        boss.phase * .3
    );

    ctx.shadowBlur = 45;
    ctx.shadowColor =
        "#ff405d";

    ctx.fillStyle =
        boss.hitFlash > 0
            ? "#ffffff"
            : "#8b1733";

    ctx.beginPath();

    const points = 12;

    for (
        let i = 0;
        i < points;
        i++
    ) {

        const a =
            Math.PI * 2 *
            i / points;

        const radius =
            i % 2 === 0
                ? boss.radius
                : boss.radius * .65;

        const x =
            Math.cos(a) *
            radius;

        const y =
            Math.sin(a) *
            radius;

        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }

    }

    ctx.closePath();

    ctx.fill();

    ctx.strokeStyle =
        "#ff5b73";

    ctx.lineWidth = 3;

    ctx.stroke();

    ctx.fillStyle =
        "#ffb1bd";

    ctx.beginPath();

    ctx.arc(
        0,
        0,
        boss.radius * .28,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.restore();

}

/* =========================================================
   DRAW BULLETS
========================================================= */

function drawBullets() {

    ctx.save();

    ctx.lineWidth = 3;

    for (const b of bullets) {

        ctx.strokeStyle =
            "#9fe6ff";

        ctx.shadowBlur = 15;
        ctx.shadowColor =
            "#6bdcff";

        ctx.beginPath();

        ctx.moveTo(
            b.x,
            b.y
        );

        ctx.lineTo(
            b.x -
            b.vx * .025,
            b.y -
            b.vy * .025
        );

        ctx.stroke();

    }

    ctx.restore();

    for (const b of enemyBullets) {

        ctx.save();

        ctx.fillStyle =
            "#ff506c";

        ctx.shadowBlur = 15;
        ctx.shadowColor =
            "#ff405d";

        ctx.beginPath();

        ctx.arc(
            b.x,
            b.y,
            b.radius,
            0,
            Math.PI * 2
        );

        ctx.fill();

        ctx.restore();

    }

}

/* =========================================================
   DRAW POWERUPS
========================================================= */

function drawPowerups() {

    for (const p of powerups) {

        const scale =
            1 +
            Math.sin(
                p.phase
            ) * .12;

        ctx.save();

        ctx.translate(
            p.x,
            p.y
        );

        ctx.scale(
            scale,
            scale
        );

        ctx.shadowBlur = 18;
        ctx.shadowColor =
            "#7ae3ff";

        ctx.strokeStyle =
            "#8deaff";

        ctx.lineWidth = 3;

        ctx.beginPath();

        ctx.arc(
            0,
            0,
            p.radius,
            0,
            Math.PI * 2
        );

        ctx.stroke();

        ctx.fillStyle =
            "#dffaff";

        ctx.font =
            "bold 12px system-ui";

        ctx.textAlign =
            "center";

        ctx.textBaseline =
            "middle";

        const letters = {

            heal: "+",
            shield: "S",
            rapid: "R",
            spread: "3",
            energy: "E"

        };

        ctx.fillText(
            letters[p.type],
            0,
            0
        );

        ctx.restore();

    }

}

/* =========================================================
   DRAW
========================================================= */

function draw() {

    ctx.save();

    if (
        settings.shake &&
        game.screenShake > 0
    ) {

        ctx.translate(
            rand(
                -game.screenShake,
                game.screenShake
            ),
            rand(
                -game.screenShake,
                game.screenShake
            )
        );

    }

    drawBackground();

    drawPowerups();

    drawBullets();

    drawEnemies();

    drawBoss();

    drawPlayer();

    drawParticles();

    ctx.restore();

}

/* =========================================================
   HUD
========================================================= */

function updateHUD() {

    scoreEl.textContent =
        Math.floor(
            game.score
        ).toLocaleString();

    waveEl.textContent =
        game.wave;

    killsEl.textContent =
        game.kills;

    healthFill.style.width =
        clamp(
            player.health /
            player.maxHealth *
            100,
            0,
            100
        ) + "%";

    energyFill.style.width =
        clamp(
            player.energy /
            player.maxEnergy *
            100,
            0,
            100
        ) + "%";

}

/* =========================================================
   GAME OVER
========================================================= */

function gameOver() {

    running = false;

    mobileControls.style.display =
        "none";

    hud.style.display =
        "none";

    pauseButton.style.display =
        "none";

    bossBar.style.display =
        "none";

    document.getElementById(
        "finalScore"
    ).textContent =
        Math.floor(
            game.score
        ).toLocaleString();

    document.getElementById(
        "finalWave"
    ).textContent =
        game.wave;

    document.getElementById(
        "finalKills"
    ).textContent =
        game.kills;

    document.getElementById(
        "finalCombo"
    ).textContent =
        Math.floor(
            game.combo
        );

    gameOverScreen.classList.remove(
        "hidden"
    );

}

/* =========================================================
   PAUSE
========================================================= */

function togglePause() {

    if (!running) return;

    paused = !paused;

    if (paused) {

        pauseScreen.classList.remove(
            "hidden"
        );

    } else {

        pauseScreen.classList.add(
            "hidden"
        );

        lastTime =
            performance.now();

    }

}

/* =========================================================
   LOOP
========================================================= */

function loop(timestamp) {

    if (!running) return;

    if (paused) {

        requestAnimationFrame(loop);

        return;

    }

    let dt =
        (timestamp - lastTime) /
        1000;

    lastTime = timestamp;

    dt =
        Math.min(
            dt,
            .033
        );

    game.time += dt;

    updateStars(dt);

    updatePlayer(dt);

    updateSpawning(dt);

    updateEnemies(dt);

    updateBoss(dt);

    updateBullets(dt);

    updateEnemyBullets(dt);

    updatePowerups(dt);

    updateParticles(dt);

    updateCombo(dt);

    updateWave(dt);

    if (
        game.screenShake > 0
    ) {

        game.screenShake -=
            35 * dt;

        game.screenShake =
            Math.max(
                0,
                game.screenShake
            );

    }

    updateHUD();

    draw();

    requestAnimationFrame(loop);

}

/* =========================================================
   JOYSTICK
========================================================= */

const joystick =
    document.getElementById(
        "joystick"
    );

const joystickKnob =
    document.getElementById(
        "joystickKnob"
    );

let joystickPointer = null;

function updateJoystick(
    clientX,
    clientY
) {

    const rect =
        joystick.getBoundingClientRect();

    const centerX =
        rect.left +
        rect.width / 2;

    const centerY =
        rect.top +
        rect.height / 2;

    let dx =
        clientX -
        centerX;

    let dy =
        clientY -
        centerY;

    const max =
        rect.width * .32;

    const length =
        Math.sqrt(
            dx * dx +
            dy * dy
        );

    if (length > max) {

        dx =
            dx / length *
            max;

        dy =
            dy / length *
            max;

    }

    joystickInput.x =
        dx / max;

    joystickInput.y =
        dy / max;

    joystickInput.active =
        true;

    joystickKnob.style.transform =
        `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`;

}

function resetJoystick() {

    joystickInput.x = 0;
    joystickInput.y = 0;
    joystickInput.active = false;

    joystickKnob.style.transform =
        "translate(-50%, -50%)";

}

joystick.addEventListener(
    "pointerdown",
    e => {

        joystickPointer =
            e.pointerId;

        joystick.setPointerCapture(
            e.pointerId
        );

        updateJoystick(
            e.clientX,
            e.clientY
        );

        initAudio();

    }
);

joystick.addEventListener(
    "pointermove",
    e => {

        if (
            e.pointerId ===
            joystickPointer
        ) {

            updateJoystick(
                e.clientX,
                e.clientY
            );

        }

    }
);

joystick.addEventListener(
    "pointerup",
    e => {

        if (
            e.pointerId ===
            joystickPointer
        ) {

            joystickPointer =
                null;

            resetJoystick();

        }

    }
);

joystick.addEventListener(
    "pointercancel",
    resetJoystick
);

/* =========================================================
   MOBILE FIRE / BOOST
========================================================= */

const fireButton =
    document.getElementById(
        "fireButton"
    );

const boostButton =
    document.getElementById(
        "boostButton"
    );

fireButton.addEventListener(
    "pointerdown",
    e => {

        e.preventDefault();

        touchFire = true;

        initAudio();

    }
);

fireButton.addEventListener(
    "pointerup",
    () => {
        touchFire = false;
    }
);

fireButton.addEventListener(
    "pointercancel",
    () => {
        touchFire = false;
    }
);

fireButton.addEventListener(
    "pointerleave",
    () => {
        touchFire = false;
    }
);

boostButton.addEventListener(
    "pointerdown",
    e => {

        e.preventDefault();

        touchBoost = true;

    }
);

boostButton.addEventListener(
    "pointerup",
    () => {
        touchBoost = false;
    }
);

boostButton.addEventListener(
    "pointercancel",
    () => {
        touchBoost = false;
    }
);

boostButton.addEventListener(
    "pointerleave",
    () => {
        touchBoost = false;
    }
);

/* =========================================================
   BUTTONS
========================================================= */

document.getElementById(
    "playButton"
).addEventListener(
    "click",
    startGame
);

document.getElementById(
    "howButton"
).addEventListener(
    "click",
    () => {

        menuScreen.classList.add(
            "hidden"
        );

        howScreen.classList.remove(
            "hidden"
        );

    }
);

document.getElementById(
    "howBack"
).addEventListener(
    "click",
    () => {

        howScreen.classList.add(
            "hidden"
        );

        menuScreen.classList.remove(
            "hidden"
        );

    }
);

document.getElementById(
    "settingsButton"
).addEventListener(
    "click",
    () => {

        menuScreen.classList.add(
            "hidden"
        );

        settingsScreen.classList.remove(
            "hidden"
        );

    }
);

document.getElementById(
    "settingsBack"
).addEventListener(
    "click",
    () => {

        settingsScreen.classList.add(
            "hidden"
        );

        menuScreen.classList.remove(
            "hidden"
        );

    }
);

document.getElementById(
    "resumeButton"
).addEventListener(
    "click",
    togglePause
);

document.getElementById(
    "pauseButton"
).addEventListener(
    "click",
    togglePause
);

document.getElementById(
    "pauseMenuButton"
).addEventListener(
    "click",
    () => {

        running = false;
        paused = false;

        pauseScreen.classList.add(
            "hidden"
        );

        hud.style.display =
            "none";

        pauseButton.style.display =
            "none";

        mobileControls.style.display =
            "none";

        menuScreen.classList.remove(
            "hidden"
        );

    }
);

document.getElementById(
    "restartButton"
).addEventListener(
    "click",
    startGame
);

document.getElementById(
    "gameOverMenuButton"
).addEventListener(
    "click",
    () => {

        gameOverScreen.classList.add(
            "hidden"
        );

        menuScreen.classList.remove(
            "hidden"
        );

    }
);

/* =========================================================
   SETTINGS BUTTONS
========================================================= */

const soundToggle =
    document.getElementById(
        "soundToggle"
    );

const shakeToggle =
    document.getElementById(
        "shakeToggle"
    );

const particlesToggle =
    document.getElementById(
        "particlesToggle"
    );

soundToggle.addEventListener(
    "click",
    () => {

        settings.sound =
            !settings.sound;

        soundToggle.textContent =
            "SOUND: " +
            (
                settings.sound
                    ? "ON"
                    : "OFF"
            );

        if (settings.sound) {
            initAudio();
        }

    }
);

shakeToggle.addEventListener(
    "click",
    () => {

        settings.shake =
            !settings.shake;

        shakeToggle.textContent =
            "SCREEN SHAKE: " +
            (
                settings.shake
                    ? "ON"
                    : "OFF"
            );

    }
);

particlesToggle.addEventListener(
    "click",
    () => {

        settings.particles =
            !settings.particles;

        particlesToggle.textContent =
            "PARTICLES: " +
            (
                settings.particles
                    ? "ON"
                    : "OFF"
            );

    }
);

/* =========================================================
   FULLSCREEN
========================================================= */

document.getElementById(
    "fullscreenButton"
).addEventListener(
    "click",
    async () => {

        try {

            if (!document.fullscreenElement) {

                await document.documentElement
                    .requestFullscreen();

            } else {

                await document.exitFullscreen();

            }

        } catch (e) {

            /* Browser may block fullscreen */

        }

    }
);

/* =========================================================
   FULLSCREEN RESIZE
========================================================= */

document.addEventListener(
    "fullscreenchange",
    () => {

        setTimeout(
            resizeCanvas,
            100
        );

    }
);

/* =========================================================
   PREVENT MOBILE SCROLL / ZOOM
========================================================= */

document.addEventListener(
    "touchmove",
    e => {

        if (running) {
            e.preventDefault();
        }

    },
    {
        passive: false
    }
);

document.addEventListener(
    "gesturestart",
    e => {
        e.preventDefault();
    },
    {
        passive: false
    }
);

/* =========================================================
   INITIAL STATE
========================================================= */

window.addEventListener(
    "load",
    () => {

        resizeCanvas();

        createStars();

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
    port = int(os.environ.get("PORT", "10000"))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
