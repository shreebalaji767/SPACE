from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">

<meta name="theme-color" content="#050812">
<title>VOID SPACE</title>

<style>
*{
    box-sizing:border-box;
    margin:0;
    padding:0;
    -webkit-tap-highlight-color:transparent;
}

html,
body{
    width:100%;
    height:100%;
    overflow:hidden;
    background:#02040a;
    color:#fff;
    font-family:Arial,Helvetica,sans-serif;
}

body{
    touch-action:none;
    user-select:none;
}

button{
    font:inherit;
}

#gameRoot{
    position:fixed;
    inset:0;
    overflow:hidden;
    background:
        radial-gradient(circle at center,#081329 0%,#030712 48%,#010207 100%);
}

#gameCanvas{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    display:block;
}

/* =========================================================
   HUD
========================================================= */

#hud{
    position:absolute;
    top:0;
    left:0;
    right:0;
    z-index:20;
    display:flex;
    align-items:flex-start;
    justify-content:space-between;
    padding:
        max(14px,env(safe-area-inset-top))
        max(14px,env(safe-area-inset-right))
        0
        max(14px,env(safe-area-inset-left));
    pointer-events:none;
}

.hudLeft,
.hudRight{
    display:flex;
    flex-direction:column;
    gap:7px;
}

.hudRight{
    align-items:flex-end;
}

.hudBox{
    min-width:130px;
    padding:8px 11px;
    border:1px solid rgba(100,190,255,.25);
    background:rgba(3,9,20,.72);
    backdrop-filter:blur(7px);
    box-shadow:0 0 18px rgba(0,130,255,.08);
    border-radius:9px;
}

.hudLabel{
    display:block;
    color:#7186a9;
    font-size:9px;
    letter-spacing:2px;
    font-weight:bold;
}

.hudValue{
    display:block;
    margin-top:2px;
    font-size:17px;
    font-weight:900;
    letter-spacing:1px;
}

.bar{
    width:150px;
    height:7px;
    margin-top:5px;
    border-radius:99px;
    overflow:hidden;
    background:#111a2c;
    border:1px solid rgba(255,255,255,.08);
}

.barFill{
    width:100%;
    height:100%;
    transition:width .12s linear;
}

#healthFill{
    background:linear-gradient(90deg,#ff315d,#ff9d45);
}

#energyFill{
    background:linear-gradient(90deg,#27a9ff,#8c63ff);
}

#bossHud{
    position:absolute;
    top:78px;
    left:50%;
    transform:translateX(-50%);
    width:min(520px,70vw);
    z-index:20;
    display:none;
    pointer-events:none;
}

#bossTitle{
    text-align:center;
    color:#ff405f;
    font-size:12px;
    font-weight:900;
    letter-spacing:4px;
    margin-bottom:6px;
    text-shadow:0 0 12px rgba(255,50,90,.8);
}

#bossBar{
    width:100%;
    height:12px;
    border:1px solid rgba(255,60,90,.45);
    background:#160711;
    border-radius:99px;
    overflow:hidden;
}

#bossFill{
    width:100%;
    height:100%;
    background:linear-gradient(90deg,#ff234d,#ff7a32);
}

#combo{
    color:#ffd45c;
}

#pauseButton{
    position:absolute;
    right:max(15px,env(safe-area-inset-right));
    bottom:max(15px,env(safe-area-inset-bottom));
    z-index:30;
    width:48px;
    height:48px;
    border:1px solid rgba(130,190,255,.35);
    border-radius:50%;
    background:rgba(4,10,22,.82);
    color:#fff;
    cursor:pointer;
    display:none;
    font-weight:900;
}

/* =========================================================
   SCREENS
========================================================= */

.screen{
    position:absolute;
    inset:0;
    z-index:100;
    display:none;
    align-items:center;
    justify-content:center;
    padding:24px;
    background:
        radial-gradient(circle at center,rgba(8,25,52,.70),rgba(1,3,9,.92));
    backdrop-filter:blur(3px);
}

.screen.active{
    display:flex;
}

.panel{
    width:min(850px,94vw);
    max-height:90vh;
    overflow:auto;
    padding:35px;
    border:1px solid rgba(85,180,255,.25);
    border-radius:20px;
    background:
        linear-gradient(145deg,rgba(7,18,38,.94),rgba(2,7,16,.97));
    box-shadow:
        0 0 60px rgba(0,120,255,.12),
        inset 0 0 35px rgba(80,150,255,.025);
}

.logo{
    text-align:center;
    font-size:clamp(40px,8vw,90px);
    font-weight:1000;
    letter-spacing:8px;
    line-height:1;
    color:#eaf7ff;
    text-shadow:
        0 0 10px #44baff,
        0 0 35px rgba(40,140,255,.65);
}

.subtitle{
    text-align:center;
    margin-top:13px;
    color:#7890b5;
    letter-spacing:5px;
    font-size:11px;
}

.menuButtons{
    width:min(380px,100%);
    margin:35px auto 0;
    display:grid;
    gap:12px;
}

.menuButton{
    width:100%;
    padding:15px 18px;
    border-radius:10px;
    border:1px solid rgba(90,180,255,.28);
    background:rgba(9,24,47,.85);
    color:#eaf7ff;
    font-size:14px;
    font-weight:900;
    letter-spacing:2px;
    cursor:pointer;
    transition:.18s ease;
}

.menuButton:hover{
    transform:translateY(-2px);
    border-color:#55baff;
    background:rgba(15,40,75,.95);
    box-shadow:0 0 22px rgba(30,160,255,.15);
}

.menuButton.primary{
    background:linear-gradient(135deg,#0c5f9f,#472c9d);
    border-color:rgba(120,220,255,.55);
}

.menuButton.danger{
    border-color:rgba(255,70,90,.35);
}

.screenTitle{
    text-align:center;
    font-size:30px;
    font-weight:1000;
    letter-spacing:4px;
    margin-bottom:25px;
}

.textSection{
    margin-bottom:23px;
}

.textSection h3{
    color:#63c9ff;
    font-size:13px;
    letter-spacing:2px;
    margin-bottom:9px;
}

.textSection p,
.textSection li{
    color:#9fb1cb;
    font-size:14px;
    line-height:1.7;
}

.textSection ul{
    padding-left:20px;
}

/* =========================================================
   SETTINGS
========================================================= */

.settingsList{
    display:grid;
    gap:10px;
}

.settingRow{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:15px;
    padding:16px;
    border:1px solid rgba(100,170,230,.15);
    background:rgba(4,13,27,.75);
    border-radius:12px;
}

.settingText{
    display:flex;
    flex-direction:column;
    gap:4px;
}

.settingText strong{
    font-size:13px;
    letter-spacing:1px;
}

.settingText span{
    color:#6f85a7;
    font-size:11px;
    line-height:1.4;
}

.toggle{
    flex:0 0 auto;
    width:52px;
    height:28px;
    border-radius:99px;
    padding:3px;
    background:#182238;
    border:1px solid rgba(255,255,255,.1);
    cursor:pointer;
    transition:.2s;
}

.toggle::after{
    content:"";
    display:block;
    width:20px;
    height:20px;
    border-radius:50%;
    background:#66738b;
    transition:.2s;
}

.toggle.on{
    background:#0a73b5;
    border-color:#42c8ff;
    box-shadow:0 0 14px rgba(40,180,255,.25);
}

.toggle.on::after{
    transform:translateX(24px);
    background:#fff;
}

/* =========================================================
   TOUCH CONTROLS
========================================================= */

#touchControls{
    position:absolute;
    inset:0;
    z-index:40;
    pointer-events:none;
    display:none;
}

.touchButton{
    pointer-events:auto;
    position:absolute;
    border:1px solid rgba(100,210,255,.3);
    background:rgba(5,15,31,.68);
    color:#fff;
    backdrop-filter:blur(6px);
    border-radius:50%;
    font-weight:1000;
    letter-spacing:1px;
}

#joystick{
    position:absolute;
    left:max(25px,env(safe-area-inset-left));
    bottom:max(25px,env(safe-area-inset-bottom));
    width:145px;
    height:145px;
    pointer-events:auto;
    border-radius:50%;
    border:1px solid rgba(80,190,255,.25);
    background:rgba(7,20,38,.42);
}

#joystickKnob{
    position:absolute;
    left:50%;
    top:50%;
    width:58px;
    height:58px;
    transform:translate(-50%,-50%);
    border-radius:50%;
    border:1px solid rgba(100,210,255,.45);
    background:rgba(40,130,200,.3);
    box-shadow:0 0 25px rgba(40,180,255,.15);
}

#fireButton{
    right:max(25px,env(safe-area-inset-right));
    bottom:max(40px,env(safe-area-inset-bottom));
    width:100px;
    height:100px;
}

#boostButton{
    right:max(45px,env(safe-area-inset-right));
    bottom:max(160px,calc(env(safe-area-inset-bottom) + 120px));
    width:68px;
    height:68px;
    font-size:10px;
}

#bombButton{
    right:max(125px,env(safe-area-inset-right));
    bottom:max(35px,env(safe-area-inset-bottom));
    width:55px;
    height:55px;
    font-size:10px;
}

@media (pointer:coarse), (max-width:800px){
    #touchControls{
        display:block;
    }

    #pauseButton{
        display:block;
    }

    .hudBox{
        min-width:100px;
        padding:6px 8px;
    }

    .hudValue{
        font-size:13px;
    }

    .bar{
        width:110px;
    }

    #bossHud{
        top:100px;
    }

    .panel{
        padding:25px 18px;
    }
}

@media (max-width:600px){
    .logo{
        font-size:43px;
        letter-spacing:5px;
    }

    .subtitle{
        font-size:9px;
        letter-spacing:3px;
    }

    .screenTitle{
        font-size:22px;
    }

    .hudLeft{
        gap:4px;
    }

    .hudRight{
        gap:4px;
    }

    .hudBox{
        min-width:92px;
    }

    #hud{
        padding-top:max(8px,env(safe-area-inset-top));
    }

    #bossHud{
        width:75vw;
        top:86px;
    }
}

/* =========================================================
   SCROLLBAR
========================================================= */

::-webkit-scrollbar{
    width:7px;
}

::-webkit-scrollbar-track{
    background:#050b15;
}

::-webkit-scrollbar-thumb{
    background:#193552;
    border-radius:99px;
}
</style>
</head>

<body>

<div id="gameRoot">

<canvas id="gameCanvas"></canvas>

<!-- =====================================================
     HUD
===================================================== -->

<div id="hud">

    <div class="hudLeft">

        <div class="hudBox">
            <span class="hudLabel">SCORE</span>
            <span class="hudValue" id="scoreText">0</span>
        </div>

        <div class="hudBox">
            <span class="hudLabel">HULL</span>
            <span class="hudValue" id="healthText">100</span>
            <div class="bar">
                <div id="healthFill" class="barFill"></div>
            </div>
        </div>

        <div class="hudBox">
            <span class="hudLabel">ENERGY</span>
            <span class="hudValue" id="energyText">100</span>
            <div class="bar">
                <div id="energyFill" class="barFill"></div>
            </div>
        </div>

    </div>

    <div class="hudRight">

        <div class="hudBox">
            <span class="hudLabel">WAVE</span>
            <span class="hudValue" id="waveText">1</span>
        </div>

        <div class="hudBox">
            <span class="hudLabel">KILLS</span>
            <span class="hudValue" id="killsText">0</span>
        </div>

        <div class="hudBox">
            <span class="hudLabel">COMBO</span>
            <span class="hudValue" id="combo">x1.0</span>
        </div>

    </div>

</div>

<div id="bossHud">
    <div id="bossTitle">BOSS</div>
    <div id="bossBar">
        <div id="bossFill"></div>
    </div>
</div>

<button id="pauseButton" onclick="togglePause()">Ⅱ</button>

<div id="crosshair"></div>

<!-- =====================================================
     MENU
===================================================== -->

<div id="menuScreen" class="screen active">
    <div class="panel">

        <div class="logo">VOID SPACE</div>
        <div class="subtitle">SURVIVE THE INFINITE VOID</div>

        <div class="menuButtons">
            <button class="menuButton primary" onclick="startGame()">
                START GAME
            </button>

            <button class="menuButton" onclick="showScreen('howScreen')">
                HOW TO PLAY
            </button>

            <button class="menuButton" onclick="showScreen('settingsScreen')">
                SETTINGS
            </button>
        </div>

    </div>
</div>

<!-- =====================================================
     HOW TO PLAY
===================================================== -->

<div id="howScreen" class="screen">
    <div class="panel">

        <div class="screenTitle">HOW TO PLAY</div>

        <div class="textSection">
            <h3>MOVEMENT</h3>
            <p>
                <b>W / ↑</b> — move forward<br>
                <b>S / ↓</b> — move backward
            </p>
        </div>

        <div class="textSection">
            <h3>ROTATION — 360° MODE</h3>
            <p>
                When <b>360° ROTATION</b> is ON:
            </p>
            <ul>
                <li><b>A</b> / <b>←</b> continuously rotate left.</li>
                <li><b>D</b> / <b>→</b> continuously rotate right.</li>
                <li>Hold the key to keep rotating.</li>
                <li>The ship can rotate through a complete 360° circle.</li>
                <li>W/S always move relative to the ship's current direction.</li>
            </ul>
        </div>

        <div class="textSection">
            <h3>WEAPONS</h3>
            <p>
                <b>SPACE / X</b> — fire<br>
                <b>Mouse Left Click</b> — fire toward cursor
            </p>
        </div>

        <div class="textSection">
            <h3>BOOST</h3>
            <p>
                Hold <b>SHIFT</b> to boost.
            </p>
        </div>

        <div class="textSection">
            <h3>PAUSE</h3>
            <p>
                Press <b>P</b> or <b>ESC</b> to pause.
            </p>
        </div>

        <div class="textSection">
            <h3>POWERUPS</h3>
            <p>
                Destroy enemies and collect powerups for repairs,
                shields, rapid fire, spread weapons, energy and bombs.
            </p>
        </div>

        <div class="menuButtons">
            <button class="menuButton" onclick="showScreen('menuScreen')">
                BACK
            </button>
        </div>

    </div>
</div>

<!-- =====================================================
     SETTINGS
===================================================== -->

<div id="settingsScreen" class="screen">
    <div class="panel">

        <div class="screenTitle">SETTINGS</div>

        <div class="settingsList">

            <div class="settingRow">
                <div class="settingText">
                    <strong>SOUND</strong>
                    <span>Enable game audio and weapon sounds</span>
                </div>
                <div id="soundToggle"
                     class="toggle on"
                     onclick="toggleSetting('sound')"></div>
            </div>

            <div class="settingRow">
                <div class="settingText">
                    <strong>SCREEN SHAKE</strong>
                    <span>Camera shake during explosions and impacts</span>
                </div>
                <div id="shakeToggle"
                     class="toggle on"
                     onclick="toggleSetting('shake')"></div>
            </div>

            <div class="settingRow">
                <div class="settingText">
                    <strong>PARTICLES</strong>
                    <span>Explosion and engine particle effects</span>
                </div>
                <div id="particlesToggle"
                     class="toggle on"
                     onclick="toggleSetting('particles')"></div>
            </div>

            <div class="settingRow">
                <div class="settingText">
                    <strong>360° ROTATION</strong>
                    <span>
                        ON: A/D and ←/→ continuously rotate the ship.
                        OFF: A/D and ←/→ strafe.
                    </span>
                </div>

                <div id="rotationToggle"
                     class="toggle on"
                     onclick="toggleSetting('rotation360')"></div>
            </div>

        </div>

        <div class="menuButtons">
            <button class="menuButton" onclick="showScreen('menuScreen')">
                BACK
            </button>
        </div>

    </div>
</div>

<!-- =====================================================
     PAUSE
===================================================== -->

<div id="pauseScreen" class="screen">
    <div class="panel">

        <div class="screenTitle">PAUSED</div>

        <div class="menuButtons">
            <button class="menuButton primary" onclick="togglePause()">
                RESUME
            </button>

            <button class="menuButton" onclick="restartGame()">
                RESTART
            </button>

            <button class="menuButton danger" onclick="quitGame()">
                QUIT TO MENU
            </button>
        </div>

    </div>
</div>

<!-- =====================================================
     GAME OVER
===================================================== -->

<div id="gameOverScreen" class="screen">
    <div class="panel">

        <div class="screenTitle">SHIP DESTROYED</div>

        <div style="text-align:center;color:#8195b4;line-height:2;">
            FINAL SCORE
            <div id="finalScore"
                 style="font-size:42px;font-weight:1000;color:#fff;">
                0
            </div>

            WAVE REACHED
            <div id="finalWave"
                 style="font-size:28px;font-weight:1000;color:#58c7ff;">
                1
            </div>
        </div>

        <div class="menuButtons">

            <button class="menuButton primary" onclick="restartGame()">
                PLAY AGAIN
            </button>

            <button class="menuButton" onclick="quitGame()">
                MAIN MENU
            </button>

        </div>

    </div>
</div>

<!-- =====================================================
     TOUCH
===================================================== -->

<div id="touchControls">

    <div id="joystick">
        <div id="joystickKnob"></div>
    </div>

    <button id="fireButton"
            class="touchButton">
        FIRE
    </button>

    <button id="boostButton"
            class="touchButton">
        BOOST
    </button>

    <button id="bombButton"
            class="touchButton">
        BOMB
    </button>

</div>

</div>

<script>
"use strict";

/* =========================================================
   DOM
========================================================= */

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const scoreText = document.getElementById("scoreText");
const waveText = document.getElementById("waveText");
const killsText = document.getElementById("killsText");
const healthText = document.getElementById("healthText");
const energyText = document.getElementById("energyText");
const comboText = document.getElementById("combo");

const healthFill = document.getElementById("healthFill");
const energyFill = document.getElementById("energyFill");

const bossHud = document.getElementById("bossHud");
const bossFill = document.getElementById("bossFill");

const touchControls = document.getElementById("touchControls");
const joystick = document.getElementById("joystick");
const joystickKnob = document.getElementById("joystickKnob");
const fireButton = document.getElementById("fireButton");
const boostButton = document.getElementById("boostButton");
const bombButton = document.getElementById("bombButton");

/* =========================================================
   SETTINGS
========================================================= */

const settings = {
    sound: true,
    shake: true,
    particles: true,

    /*
       IMPORTANT:
       This is the actual 360-degree rotation setting.
    */
    rotation360: true
};

function toggleSetting(name){
    settings[name] = !settings[name];
    updateSettingsUI();

    if(settings.sound){
        initAudio();
        beep(500,0.04,"sine",0.025);
    }
}

function updateSettingsUI(){

    const map = {
        sound:"soundToggle",
        shake:"shakeToggle",
        particles:"particlesToggle",
        rotation360:"rotationToggle"
    };

    Object.keys(map).forEach(name=>{
        const el = document.getElementById(map[name]);

        if(!el) return;

        el.classList.toggle("on", !!settings[name]);
    });
}

updateSettingsUI();

/* =========================================================
   SCREEN SYSTEM
========================================================= */

const screenIds = [
    "menuScreen",
    "howScreen",
    "settingsScreen",
    "pauseScreen",
    "gameOverScreen"
];

function hideAllScreens(){

    screenIds.forEach(id=>{
        const el = document.getElementById(id);

        if(el){
            el.classList.remove("active");
        }
    });
}

function showScreen(id){

    hideAllScreens();

    const el = document.getElementById(id);

    if(el){
        el.classList.add("active");
    }
}

/* =========================================================
   CANVAS
========================================================= */

let W = 0;
let H = 0;
let DPR = 1;

function resize(){

    W = window.innerWidth;
    H = window.innerHeight;

    DPR = Math.min(window.devicePixelRatio || 1,2);

    canvas.width = Math.floor(W * DPR);
    canvas.height = Math.floor(H * DPR);

    canvas.style.width = W + "px";
    canvas.style.height = H + "px";

    ctx.setTransform(DPR,0,0,DPR,0,0);

    createStars();
}

window.addEventListener("resize",resize);
resize();

/* =========================================================
   GAME STATE
========================================================= */

let running = false;
let paused = false;

let score = 0;
let wave = 1;
let kills = 0;
let waveKills = 0;

let combo = 1;
let comboTimer = 0;

let enemies = [];
let bullets = [];
let enemyBullets = [];
let particles = [];
let powerups = [];
let stars = [];

let boss = null;

let spawnTimer = 0;
let waveMessageTimer = 0;
let screenShake = 0;

let gameOverTimer = null;

/* =========================================================
   PLAYER
========================================================= */

const player = {
    x:0,
    y:0,

    angle:-Math.PI / 2,

    radius:16,

    speed:250,
    boostSpeed:440,

    rotationSpeed:3.6,

    health:100,
    maxHealth:100,

    energy:100,
    maxEnergy:100,

    fireCooldown:0,
    fireRate:.18,

    rapidTimer:0,
    spreadTimer:0,
    shieldTimer:0,

    invincibleTimer:0
};

/* =========================================================
   INPUT
========================================================= */

/*
   IMPORTANT:
   We use KeyboardEvent.code.

   A = KeyA
   D = KeyD
   Left = ArrowLeft
   Right = ArrowRight

   The key state stays TRUE while held.

   The game checks these values EVERY FRAME.
   Therefore browser key-repeat is irrelevant.
*/

const keys = Object.create(null);

window.addEventListener("keydown",e=>{

    const code = e.code;

    if([
        "ArrowUp",
        "ArrowDown",
        "ArrowLeft",
        "ArrowRight",
        "KeyW",
        "KeyS",
        "KeyA",
        "KeyD",
        "Space",
        "KeyX",
        "ShiftLeft",
        "ShiftRight",
        "KeyP",
        "Escape",
        "KeyB"
    ].includes(code)){
        e.preventDefault();
    }

    keys[code] = true;

    /*
       Pause should only trigger once per physical key press.
    */
    if(!e.repeat){

        if(code === "KeyP" || code === "Escape"){

            if(running){
                togglePause();
            }
        }

        if(code === "KeyB"){

            if(running && !paused){
                useBomb();
            }
        }

        if(code === "Space" && !running){

            if(
                document.getElementById("menuScreen").classList.contains("active") ||
                document.getElementById("gameOverScreen").classList.contains("active")
            ){
                startGame();
            }
        }
    }

    initAudio();
});

window.addEventListener("keyup",e=>{
    keys[e.code] = false;
});

window.addEventListener("blur",()=>{

    Object.keys(keys).forEach(k=>{
        keys[k] = false;
    });

    mouse.down = false;
    touch.fire = false;
    touch.boost = false;
});

/* =========================================================
   MOUSE
========================================================= */

const mouse = {
    x:0,
    y:0,
    down:false,
    activeUntil:0
};

canvas.addEventListener("pointermove",e=>{

    if(e.pointerType !== "mouse"){
        return;
    }

    const rect = canvas.getBoundingClientRect();

    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;

    /*
       Mouse aim gets temporary priority.

       It expires after 1.2 seconds.
       This is important because keyboard A/D must
       become usable again after mouse movement stops.
    */
    mouse.activeUntil = performance.now() + 1200;
});

canvas.addEventListener("pointerdown",e=>{

    if(e.pointerType === "mouse"){

        mouse.down = true;

        const rect = canvas.getBoundingClientRect();

        mouse.x = e.clientX - rect.left;
        mouse.y = e.clientY - rect.top;

        mouse.activeUntil = performance.now() + 1200;

        initAudio();
    }
});

window.addEventListener("pointerup",e=>{

    if(e.pointerType === "mouse"){
        mouse.down = false;
    }
});

function mouseIsAiming(){

    return performance.now() < mouse.activeUntil;
}

/* =========================================================
   TOUCH
========================================================= */

const touch = {
    joystickId:null,

    x:0,
    y:0,

    dx:0,
    dy:0,

    magnitude:0,

    fire:false,
    boost:false
};

function updateJoystick(clientX,clientY){

    const rect = joystick.getBoundingClientRect();

    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;

    let dx = clientX - cx;
    let dy = clientY - cy;

    const max = rect.width * .38;

    const len = Math.hypot(dx,dy);

    if(len > max){

        dx = dx / len * max;
        dy = dy / len * max;
    }

    touch.dx = dx / max;
    touch.dy = dy / max;

    touch.magnitude = Math.min(
        1,
        Math.hypot(touch.dx,touch.dy)
    );

    joystickKnob.style.transform =
        `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`;
}

function resetJoystick(){

    touch.dx = 0;
    touch.dy = 0;
    touch.magnitude = 0;

    joystickKnob.style.transform =
        "translate(-50%,-50%)";
}

joystick.addEventListener("pointerdown",e=>{

    if(e.pointerType === "mouse"){
        return;
    }

    touch.joystickId = e.pointerId;

    joystick.setPointerCapture(e.pointerId);

    updateJoystick(e.clientX,e.clientY);
});

joystick.addEventListener("pointermove",e=>{

    if(e.pointerId !== touch.joystickId){
        return;
    }

    updateJoystick(e.clientX,e.clientY);
});

joystick.addEventListener("pointerup",e=>{

    if(e.pointerId === touch.joystickId){

        touch.joystickId = null;
        resetJoystick();
    }
});

joystick.addEventListener("pointercancel",()=>{

    touch.joystickId = null;
    resetJoystick();
});

function setupTouchButton(button,downFn,upFn){

    button.addEventListener("pointerdown",e=>{

        if(e.pointerType === "mouse"){
            return;
        }

        e.preventDefault();

        downFn();

        button.setPointerCapture(e.pointerId);
    });

    button.addEventListener("pointerup",e=>{

        if(e.pointerType === "mouse"){
            return;
        }

        e.preventDefault();

        upFn();
    });

    button.addEventListener("pointercancel",()=>{

        upFn();
    });
}

setupTouchButton(
    fireButton,
    ()=>{
        touch.fire = true;
        initAudio();
    },
    ()=>{
        touch.fire = false;
    }
);

setupTouchButton(
    boostButton,
    ()=>{
        touch.boost = true;
    },
    ()=>{
        touch.boost = false;
    }
);

bombButton.addEventListener("pointerdown",e=>{

    if(e.pointerType === "mouse"){
        return;
    }

    e.preventDefault();

    useBomb();

    initAudio();
});

/* =========================================================
   AUDIO
========================================================= */

let audioCtx = null;

function initAudio(){

    if(!settings.sound){
        return;
    }

    if(!audioCtx){

        try{
            audioCtx = new (
                window.AudioContext ||
                window.webkitAudioContext
            )();
        }catch(err){
            audioCtx = null;
        }
    }

    if(audioCtx && audioCtx.state === "suspended"){
        audioCtx.resume().catch(()=>{});
    }
}

function beep(freq,duration,type="sine",volume=.03){

    if(!settings.sound){
        return;
    }

    initAudio();

    if(!audioCtx){
        return;
    }

    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();

    osc.type = type;
    osc.frequency.value = freq;

    gain.gain.setValueAtTime(volume,audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(
        .0001,
        audioCtx.currentTime + duration
    );

    osc.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start();
    osc.stop(audioCtx.currentTime + duration);
}

/* =========================================================
   STARS
========================================================= */

function createStars(){

    stars = [];

    const count = Math.max(
        100,
        Math.floor(W * H / 8500)
    );

    for(let i=0;i<count;i++){

        stars.push({
            x:Math.random() * W,
            y:Math.random() * H,
            z:.2 + Math.random() * .9,
            size:.4 + Math.random() * 1.8,
            speed:8 + Math.random() * 30
        });
    }
}

function updateStars(dt){

    for(const s of stars){

        s.y += s.speed * s.z * dt;

        if(s.y > H + 10){

            s.y = -10;
            s.x = Math.random() * W;
        }
    }
}

function drawStars(){

    for(const s of stars){

        ctx.globalAlpha = .25 + s.z * .5;

        ctx.fillStyle = "#9bcfff";

        ctx.beginPath();

        ctx.arc(
            s.x,
            s.y,
            s.size * s.z,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }

    ctx.globalAlpha = 1;
}

/* =========================================================
   PARTICLES
========================================================= */

function spawnParticle(
    x,
    y,
    vx,
    vy,
    life,
    size,
    type="normal"
){

    if(!settings.particles){
        return;
    }

    particles.push({
        x,
        y,
        vx,
        vy,
        life,
        maxLife:life,
        size,
        type
    });
}

function particleBurst(
    x,
    y,
    amount=20,
    force=150,
    type="normal"
){

    if(!settings.particles){
        return;
    }

    for(let i=0;i<amount;i++){

        const a = Math.random() * Math.PI * 2;
        const speed = Math.random() * force;

        spawnParticle(
            x,
            y,
            Math.cos(a) * speed,
            Math.sin(a) * speed,
            .3 + Math.random() * .6,
            1 + Math.random() * 3,
            type
        );
    }
}

function updateParticles(dt){

    for(let i=particles.length-1;i>=0;i--){

        const p = particles[i];

        p.x += p.vx * dt;
        p.y += p.vy * dt;

        p.vx *= .985;
        p.vy *= .985;

        p.life -= dt;

        if(p.life <= 0){
            particles.splice(i,1);
        }
    }
}

function drawParticles(){

    if(!settings.particles){
        return;
    }

    for(const p of particles){

        const alpha = Math.max(
            0,
            p.life / p.maxLife
        );

        ctx.globalAlpha = alpha;

        if(p.type === "enemy"){
            ctx.fillStyle = "#ff536f";
        }
        else if(p.type === "gold"){
            ctx.fillStyle = "#ffd45c";
        }
        else if(p.type === "energy"){
            ctx.fillStyle = "#5bcbff";
        }
        else{
            ctx.fillStyle = "#a9e8ff";
        }

        ctx.beginPath();

        ctx.arc(
            p.x,
            p.y,
            p.size * alpha + .5,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }

    ctx.globalAlpha = 1;
}

/* =========================================================
   GRID
========================================================= */

function drawGrid(){

    const spacing = 80;

    ctx.save();

    ctx.globalAlpha = .055;
    ctx.strokeStyle = "#55aaff";
    ctx.lineWidth = 1;

    const ox = ((performance.now() / 50) % spacing);

    for(let x=-spacing;x<W+spacing;x+=spacing){

        ctx.beginPath();
        ctx.moveTo(x + ox,0);
        ctx.lineTo(x + ox,H);
        ctx.stroke();
    }

    const oy = ((performance.now() / 70) % spacing);

    for(let y=-spacing;y<H+spacing;y+=spacing){

        ctx.beginPath();
        ctx.moveTo(0,y + oy);
        ctx.lineTo(W,y + oy);
        ctx.stroke();
    }

    ctx.restore();
}

/* =========================================================
   PLAYER DRAW
========================================================= */

function drawPlayer(){

    const p = player;

    ctx.save();

    ctx.translate(p.x,p.y);
    ctx.rotate(p.angle);

    /*
       Shield
    */

    if(p.shieldTimer > 0){

        const pulse =
            1 + Math.sin(performance.now()/100) * .06;

        ctx.beginPath();

        ctx.arc(
            0,
            0,
            25 * pulse,
            0,
            Math.PI * 2
        );

        ctx.strokeStyle = "rgba(60,210,255,.75)";
        ctx.lineWidth = 2;
        ctx.shadowBlur = 15;
        ctx.shadowColor = "#38cfff";
        ctx.stroke();
    }

    /*
       Engine
    */

    ctx.beginPath();

    ctx.moveTo(-12,-6);
    ctx.lineTo(
        -27 - Math.random() * 8,
        0
    );
    ctx.lineTo(-12,6);

    ctx.closePath();

    ctx.fillStyle = "#35baff";
    ctx.shadowBlur = 15;
    ctx.shadowColor = "#36baff";
    ctx.fill();

    /*
       Main ship
    */

    ctx.shadowBlur = 18;
    ctx.shadowColor = "#4ccfff";

    ctx.beginPath();

    ctx.moveTo(23,0);
    ctx.lineTo(-13,-11);
    ctx.lineTo(-8,0);
    ctx.lineTo(-13,11);
    ctx.closePath();

    ctx.fillStyle = "#e8f8ff";
    ctx.fill();

    ctx.shadowBlur = 0;

    ctx.strokeStyle = "#48c7ff";
    ctx.lineWidth = 2;
    ctx.stroke();

    /*
       Cockpit
    */

    ctx.beginPath();

    ctx.moveTo(8,0);
    ctx.lineTo(-4,-5);
    ctx.lineTo(-7,0);
    ctx.lineTo(-4,5);
    ctx.closePath();

    ctx.fillStyle = "#246b9c";
    ctx.fill();

    ctx.restore();
}

/* =========================================================
   ENEMY CREATION
========================================================= */

function randomEdgePosition(){

    const side = Math.floor(Math.random() * 4);

    if(side === 0){
        return {
            x:-50,
            y:Math.random()*H
        };
    }

    if(side === 1){
        return {
            x:W+50,
            y:Math.random()*H
        };
    }

    if(side === 2){
        return {
            x:Math.random()*W,
            y:-50
        };
    }

    return {
        x:Math.random()*W,
        y:H+50
    };
}

function createEnemy(type){

    const pos = randomEdgePosition();

    const difficulty = 1 + wave * .12;

    const e = {
        type,
        x:pos.x,
        y:pos.y,

        angle:0,

        radius:15,

        speed:70 + Math.random()*35,
        health:25,
        maxHealth:25,

        fireCooldown:1 + Math.random()*2,

        rotation:.8,

        value:100
    };

    if(type === "scout"){

        e.radius = 14;
        e.speed = 105 + wave*3;
        e.health = 24 * difficulty;
        e.maxHealth = e.health;
        e.value = 100;
    }

    if(type === "shooter"){

        e.radius = 18;
        e.speed = 60 + wave*2;
        e.health = 45 * difficulty;
        e.maxHealth = e.health;
        e.fireCooldown = 1 + Math.random()*1.5;
        e.value = 180;
    }

    if(type === "tank"){

        e.radius = 25;
        e.speed = 35 + wave;
        e.health = 150 * difficulty;
        e.maxHealth = e.health;
        e.value = 350;
    }

    if(type === "hunter"){

        e.radius = 19;
        e.speed = 90 + wave*2;
        e.health = 75 * difficulty;
        e.maxHealth = e.health;
        e.rotation = 1.7;
        e.value = 250;
    }

    enemies.push(e);
}

/* =========================================================
   SPAWNING
========================================================= */

function spawnEnemy(){

    let type = "scout";

    const r = Math.random();

    if(wave >= 8 && r > .88){
        type = "tank";
    }
    else if(wave >= 4 && r > .70){
        type = "hunter";
    }
    else if(wave >= 2 && r > .55){
        type = "shooter";
    }

    createEnemy(type);
}

/* =========================================================
   BOSS
========================================================= */

function spawnBoss(){

    const hp =
        1200 +
        wave * 280;

    boss = {
        x:W/2,
        y:-100,

        radius:60,

        health:hp,
        maxHealth:hp,

        speed:65 + wave*2,

        angle:Math.PI/2,

        fireCooldown:1,

        phase:0
    };

    bossHud.style.display = "block";

    beep(90,.4,"sawtooth",.04);

    for(let i=0;i<30;i++){

        particleBurst(
            W/2,
            80,
            1,
            160,
            "enemy"
        );
    }
}

function updateBoss(dt){

    if(!boss){
        return;
    }

    boss.phase += dt;

    /*
       Enter arena.
    */

    if(boss.y < 130){

        boss.y += 35 * dt;
    }
    else{

        const dx = player.x - boss.x;
        const dy = player.y - boss.y;

        const targetAngle = Math.atan2(dy,dx);

        let diff = normalizeAngle(
            targetAngle - boss.angle
        );

        boss.angle +=
            Math.sign(diff) *
            Math.min(
                Math.abs(diff),
                .8 * dt
            );

        boss.x +=
            Math.cos(boss.angle) *
            boss.speed *
            dt;

        boss.y +=
            Math.sin(boss.angle) *
            boss.speed *
            dt;

        boss.x +=
            Math.cos(boss.phase * 1.7) *
            20 *
            dt;

        boss.y +=
            Math.sin(boss.phase * 1.4) *
            15 *
            dt;
    }

    boss.fireCooldown -= dt;

    if(boss.fireCooldown <= 0){

        boss.fireCooldown =
            Math.max(
                .45,
                1.15 - wave*.025
            );

        const shots = 7;

        for(let i=0;i<shots;i++){

            const a =
                boss.angle -
                .8 +
                (1.6/(shots-1))*i;

            enemyBullets.push({
                x:boss.x + Math.cos(a)*50,
                y:boss.y + Math.sin(a)*50,

                vx:Math.cos(a)*190,
                vy:Math.sin(a)*190,

                radius:6,
                life:4,
                damage:12
            });
        }

        beep(120,.09,"sawtooth",.025);
    }

    /*
       Boss contact damage.
    */

    if(distance(
        player.x,
        player.y,
        boss.x,
        boss.y
    ) < player.radius + boss.radius){

        damagePlayer(25 * dt);
    }

    bossFill.style.width =
        Math.max(
            0,
            boss.health / boss.maxHealth * 100
        ) + "%";
}

function damageBoss(amount){

    if(!boss){
        return;
    }

    boss.health -= amount;

    particleBurst(
        boss.x,
        boss.y,
        2,
        100,
        "enemy"
    );

    if(boss.health <= 0){

        score += 5000 + wave*500;

        kills++;

        combo = Math.min(
            10,
            combo + 1
        );

        particleBurst(
            boss.x,
            boss.y,
            90,
            450,
            "enemy"
        );

        addShake(18);

        beep(55,.7,"sawtooth",.06);

        boss = null;

        bossHud.style.display = "none";

        wave++;

        waveKills = 0;

        waveMessageTimer = 2;

        updateHUD();
    }
}

/* =========================================================
   BULLETS
========================================================= */

function shoot(){

    if(!running || paused){
        return;
    }

    if(player.fireCooldown > 0){
        return;
    }

    const cost = 2;

    if(player.energy < cost){
        return;
    }

    player.energy -= cost;

    player.fireCooldown =
        player.rapidTimer > 0
        ? .075
        : player.fireRate;

    let aimAngle = player.angle;

    if(mouseIsAiming()){

        aimAngle = Math.atan2(
            mouse.y - player.y,
            mouse.x - player.x
        );
    }

    const count =
        player.spreadTimer > 0
        ? 3
        : 1;

    for(let i=0;i<count;i++){

        let a = aimAngle;

        if(count === 3){

            a += (i-1) * .18;
        }

        bullets.push({
            x:
                player.x +
                Math.cos(a)*22,

            y:
                player.y +
                Math.sin(a)*22,

            vx:
                Math.cos(a)*570,

            vy:
                Math.sin(a)*570,

            radius:4,
            damage:18,
            life:1.6
        });
    }

    particleBurst(
        player.x + Math.cos(aimAngle)*20,
        player.y + Math.sin(aimAngle)*20,
        3,
        80
    );

    beep(650,.035,"square",.018);
}

/* =========================================================
   ENEMY SHOOTING
========================================================= */

function enemyShoot(e){

    const a = Math.atan2(
        player.y-e.y,
        player.x-e.x
    );

    enemyBullets.push({
        x:e.x + Math.cos(a)*20,
        y:e.y + Math.sin(a)*20,

        vx:Math.cos(a)*190,
        vy:Math.sin(a)*190,

        radius:5,
        life:4,
        damage:9
    });

    beep(170,.045,"triangle",.012);
}

/* =========================================================
   ENEMY UPDATE
========================================================= */

function updateEnemies(dt){

    for(let i=enemies.length-1;i>=0;i--){

        const e = enemies[i];

        const dx = player.x-e.x;
        const dy = player.y-e.y;

        const targetAngle =
            Math.atan2(dy,dx);

        let diff =
            normalizeAngle(
                targetAngle-e.angle
            );

        e.angle +=
            Math.sign(diff) *
            Math.min(
                Math.abs(diff),
                e.rotation*dt
            );

        if(e.type === "shooter"){

            e.x +=
                Math.cos(e.angle) *
                e.speed *
                dt;

            e.y +=
                Math.sin(e.angle) *
                e.speed *
                dt;

            e.fireCooldown -= dt;

            if(e.fireCooldown <= 0){

                e.fireCooldown =
                    1.5 +
                    Math.random()*1.2;

                enemyShoot(e);
            }
        }

        else if(e.type === "hunter"){

            e.x +=
                Math.cos(e.angle) *
                e.speed *
                dt;

            e.y +=
                Math.sin(e.angle) *
                e.speed *
                dt;
        }

        else{

            e.x +=
                Math.cos(e.angle) *
                e.speed *
                dt;

            e.y +=
                Math.sin(e.angle) *
                e.speed *
                dt;
        }

        /*
           Contact.
        */

        if(
            distance(
                player.x,
                player.y,
                e.x,
                e.y
            ) <
            player.radius + e.radius
        ){

            damagePlayer(
                e.type === "tank"
                ? 28
                : 18
            );

            killEnemy(i);
            continue;
        }

        /*
           Remove far-away enemies.
        */

        if(
            e.x < -150 ||
            e.x > W+150 ||
            e.y < -150 ||
            e.y > H+150
        ){

            enemies.splice(i,1);
        }
    }
}

/* =========================================================
   ENEMY DEATH
========================================================= */

function killEnemy(index){

    const e = enemies[index];

    if(!e){
        return;
    }

    score += Math.floor(
        e.value * combo
    );

    kills++;
    waveKills++;

    combo = Math.min(
        10,
        combo + .15
    );

    comboTimer = 3;

    particleBurst(
        e.x,
        e.y,
        e.type === "tank" ? 35 : 20,
        e.type === "tank" ? 260 : 180,
        "enemy"
    );

    addShake(
        e.type === "tank" ? 7 : 3
    );

    if(Math.random() < .13){
        spawnPowerup(e.x,e.y);
    }

    enemies.splice(index,1);

    beep(
        e.type === "tank" ? 80 : 220,
        .08,
        "sawtooth",
        .02
    );
}

/* =========================================================
   BULLET UPDATE
========================================================= */

function updateBullets(dt){

    for(let i=bullets.length-1;i>=0;i--){

        const b = bullets[i];

        b.x += b.vx * dt;
        b.y += b.vy * dt;

        b.life -= dt;

        let removed = false;

        /*
           Boss collision.
        */

        if(boss){

            if(
                distance(
                    b.x,
                    b.y,
                    boss.x,
                    boss.y
                ) <
                b.radius + boss.radius
            ){

                damageBoss(b.damage);

                bullets.splice(i,1);

                removed = true;
            }
        }

        if(removed){
            continue;
        }

        /*
           Enemy collision.
        */

        for(let j=enemies.length-1;j>=0;j--){

            const e = enemies[j];

            if(
                distance(
                    b.x,
                    b.y,
                    e.x,
                    e.y
                ) <
                b.radius + e.radius
            ){

                e.health -= b.damage;

                particleBurst(
                    b.x,
                    b.y,
                    3,
                    60
                );

                bullets.splice(i,1);

                if(e.health <= 0){
                    killEnemy(j);
                }

                removed = true;
                break;
            }
        }

        if(removed){
            continue;
        }

        if(
            b.life <= 0 ||
            b.x < -50 ||
            b.x > W+50 ||
            b.y < -50 ||
            b.y > H+50
        ){

            bullets.splice(i,1);
        }
    }
}

/* =========================================================
   ENEMY BULLETS
========================================================= */

function updateEnemyBullets(dt){

    for(let i=enemyBullets.length-1;i>=0;i--){

        const b = enemyBullets[i];

        b.x += b.vx * dt;
        b.y += b.vy * dt;

        b.life -= dt;

        if(
            distance(
                b.x,
                b.y,
                player.x,
                player.y
            ) <
            b.radius + player.radius
        ){

            damagePlayer(b.damage);

            enemyBullets.splice(i,1);

            continue;
        }

        if(
            b.life <= 0 ||
            b.x < -80 ||
            b.x > W+80 ||
            b.y < -80 ||
            b.y > H+80
        ){

            enemyBullets.splice(i,1);
        }
    }
}

/* =========================================================
   POWERUPS
========================================================= */

function spawnPowerup(x,y){

    const types = [
        "heal",
        "shield",
        "rapid",
        "spread",
        "energy",
        "bomb"
    ];

    powerups.push({
        x,
        y,
        type:
            types[
                Math.floor(
                    Math.random()*types.length
                )
            ],
        radius:12,
        life:12,
        phase:Math.random()*10
    });
}

function updatePowerups(dt){

    for(let i=powerups.length-1;i>=0;i--){

        const p = powerups[i];

        p.life -= dt;
        p.phase += dt;

        if(
            distance(
                player.x,
                player.y,
                p.x,
                p.y
            ) <
            player.radius + p.radius + 4
        ){

            collectPowerup(p);

            powerups.splice(i,1);

            continue;
        }

        if(p.life <= 0){
            powerups.splice(i,1);
        }
    }
}

function collectPowerup(p){

    if(p.type === "heal"){

        player.health = Math.min(
            player.maxHealth,
            player.health + 30
        );

        beep(500,.15,"sine",.03);
    }

    if(p.type === "shield"){

        player.shieldTimer = 8;

        beep(700,.15,"sine",.03);
    }

    if(p.type === "rapid"){

        player.rapidTimer = 8;

        beep(850,.15,"square",.03);
    }

    if(p.type === "spread"){

        player.spreadTimer = 8;

        beep(950,.15,"square",.03);
    }

    if(p.type === "energy"){

        player.energy = Math.min(
            player.maxEnergy,
            player.energy + 50
        );

        beep(450,.15,"triangle",.03);
    }

    if(p.type === "bomb"){

        score += 250;

        useBomb();

        beep(100,.25,"sawtooth",.04);
    }

    particleBurst(
        p.x,
        p.y,
        18,
        150,
        "gold"
    );
}

/* =========================================================
   BOMB
========================================================= */

let bombCooldown = 0;

function useBomb(){

    if(!running || paused){
        return;
    }

    if(bombCooldown > 0){
        return;
    }

    bombCooldown = 5;

    /*
       Destroy / damage all enemies.
    */

    for(let i=enemies.length-1;i>=0;i--){

        const e = enemies[i];

        e.health -= 160;

        if(e.health <= 0){

            killEnemy(i);
        }
    }

    if(boss){

        damageBoss(260);
    }

    for(let i=0;i<55;i++){

        particleBurst(
            player.x,
            player.y,
            1,
            500,
            "gold"
        );
    }

    addShake(20);

    beep(60,.5,"sawtooth",.06);
}

/* =========================================================
   PLAYER DAMAGE
========================================================= */

function damagePlayer(amount){

    if(player.invincibleTimer > 0){
        return;
    }

    if(player.shieldTimer > 0){

        player.shieldTimer -= .3;

        addShake(2);

        return;
    }

    player.health -= amount;

    player.invincibleTimer = .35;

    addShake(7);

    particleBurst(
        player.x,
        player.y,
        10,
        150,
        "enemy"
    );

    beep(90,.12,"sawtooth",.03);

    if(player.health <= 0){

        player.health = 0;

        gameOver();
    }
}

/* =========================================================
   PLAYER UPDATE
========================================================= */

function updatePlayer(dt){

    if(player.invincibleTimer > 0){
        player.invincibleTimer -= dt;
    }

    if(player.fireCooldown > 0){
        player.fireCooldown -= dt;
    }

    if(player.rapidTimer > 0){
        player.rapidTimer -= dt;
    }

    if(player.spreadTimer > 0){
        player.spreadTimer -= dt;
    }

    if(player.shieldTimer > 0){
        player.shieldTimer -= dt;
    }

    if(bombCooldown > 0){
        bombCooldown -= dt;
    }

    /*
       ENERGY REGEN
    */

    player.energy = Math.min(
        player.maxEnergy,
        player.energy + 9 * dt
    );

    /* =====================================================
       ROTATION
       =====================================================

       THIS IS THE IMPORTANT FIX.

       A/D and ArrowLeft/ArrowRight are checked every
       animation frame.

       Holding the physical key therefore continuously
       changes player.angle.

       No browser key-repeat is used.
    */

    let rotateLeft =
        !!keys["KeyA"] ||
        !!keys["ArrowLeft"];

    let rotateRight =
        !!keys["KeyD"] ||
        !!keys["ArrowRight"];

    /*
       Mouse aim temporarily controls the angle.
       Keyboard rotation resumes automatically when
       mouse activity expires.
    */

    if(mouseIsAiming()){

        player.angle = Math.atan2(
            mouse.y-player.y,
            mouse.x-player.x
        );

    }
    else if(settings.rotation360){

        /*
           TRUE 360-DEGREE ROTATION
        */

        if(rotateLeft && !rotateRight){

            player.angle -=
                player.rotationSpeed * dt;
        }

        if(rotateRight && !rotateLeft){

            player.angle +=
                player.rotationSpeed * dt;
        }

    }
    else{

        /*
           360 ROTATION OFF

           A/D and ←/→ become sideways movement.
        */
    }

    /*
       Keep angle mathematically normalized.
       This allows unlimited continuous rotation.
    */

    player.angle =
        ((player.angle + Math.PI*2) %
        (Math.PI*2));

    /* =====================================================
       MOVEMENT
    ===================================================== */

    let forward = 0;

    if(
        keys["KeyW"] ||
        keys["ArrowUp"]
    ){
        forward += 1;
    }

    if(
        keys["KeyS"] ||
        keys["ArrowDown"]
    ){
        forward -= 1;
    }

    /*
       OFF mode:
       A/D/Left/Right strafe.
    */

    let strafe = 0;

    if(!settings.rotation360){

        if(rotateLeft && !rotateRight){
            strafe -= 1;
        }

        if(rotateRight && !rotateLeft){
            strafe += 1;
        }
    }

    /*
       Touch joystick.
    */

    let moveX = 0;
    let moveY = 0;

    if(touch.magnitude > .05){

        /*
           Joystick points in world movement direction.

           This provides full 360° movement on touch.
        */

        moveX = touch.dx;
        moveY = touch.dy;

        /*
           In touch mode, point the ship toward
           joystick direction.
        */

        player.angle = Math.atan2(
            touch.dy,
            touch.dx
        );
    }
    else{

        moveX =
            Math.cos(player.angle) * forward +
            Math.cos(player.angle + Math.PI/2) * strafe;

        moveY =
            Math.sin(player.angle) * forward +
            Math.sin(player.angle + Math.PI/2) * strafe;
    }

    const len = Math.hypot(moveX,moveY);

    if(len > 1){

        moveX /= len;
        moveY /= len;
    }

    const boosting =
        keys["ShiftLeft"] ||
        keys["ShiftRight"] ||
        touch.boost;

    const speed =
        boosting &&
        player.energy > 0
        ? player.boostSpeed
        : player.speed;

    if(boosting && len > .05){

        player.energy = Math.max(
            0,
            player.energy - 24 * dt
        );

        if(
            settings.particles &&
            Math.random() < .7
        ){

            spawnParticle(
                player.x -
                    Math.cos(player.angle)*15,
                player.y -
                    Math.sin(player.angle)*15,
                -Math.cos(player.angle) * 50,
                -Math.sin(player.angle) * 50,
                .25,
                2
            );
        }
    }

    player.x += moveX * speed * dt;
    player.y += moveY * speed * dt;

    /*
       Screen boundaries.
    */

    player.x = Math.max(
        20,
        Math.min(W-20,player.x)
    );

    player.y = Math.max(
        20,
        Math.min(H-20,player.y)
    );

    /*
       Shooting.
    */

    if(
        keys["Space"] ||
        keys["KeyX"] ||
        mouse.down ||
        touch.fire
    ){

        shoot();
    }
}

/* =========================================================
   WAVE SYSTEM
========================================================= */

function updateWave(dt){

    if(boss){
        return;
    }

    spawnTimer -= dt;

    const targetKills =
        10 + wave * 3;

    if(
        waveKills >= targetKills
    ){

        /*
           Every 5th wave = boss.
        */

        if(wave % 5 === 0){

            spawnBoss();
        }
        else{

            wave++;

            waveKills = 0;

            waveMessageTimer = 2;

            beep(320,.2,"triangle",.025);
        }

        return;
    }

    const spawnRate =
        Math.max(
            .25,
            1.2 - wave*.035
        );

    if(
        spawnTimer <= 0 &&
        enemies.length <
        4 + Math.min(wave,12)
    ){

        spawnTimer = spawnRate;

        spawnEnemy();
    }
}

/* =========================================================
   COMBO
========================================================= */

function updateCombo(dt){

    if(comboTimer > 0){

        comboTimer -= dt;
    }
    else{

        combo =
            Math.max(
                1,
                combo - dt*.25
            );
    }
}

/* =========================================================
   SHAKE
========================================================= */

function addShake(amount){

    if(settings.shake){

        screenShake =
            Math.max(
                screenShake,
                amount
            );
    }
}

/* =========================================================
   UPDATE
========================================================= */

function update(dt){

    if(!running || paused){
        return;
    }

    /*
       Avoid enormous time steps.
    */

    dt = Math.min(dt,.035);

    updateStars(dt);

    updatePlayer(dt);
    updateEnemies(dt);
    updateBullets(dt);
    updateEnemyBullets(dt);
    updatePowerups(dt);
    updateParticles(dt);

    updateBoss(dt);

    updateWave(dt);

    updateCombo(dt);

    if(waveMessageTimer > 0){
        waveMessageTimer -= dt;
    }

    screenShake *= .9;

    updateHUD();
}

/* =========================================================
   DRAW ENEMIES
========================================================= */

function drawEnemy(e){

    ctx.save();

    ctx.translate(e.x,e.y);
    ctx.rotate(e.angle);

    if(e.type === "scout"){

        ctx.beginPath();

        ctx.moveTo(20,0);
        ctx.lineTo(-13,-13);
        ctx.lineTo(-7,0);
        ctx.lineTo(-13,13);

        ctx.closePath();

        ctx.fillStyle = "#ff405f";
        ctx.shadowBlur = 14;
        ctx.shadowColor = "#ff405f";
        ctx.fill();

        ctx.shadowBlur = 0;
    }

    else if(e.type === "shooter"){

        ctx.beginPath();

        for(let i=0;i<8;i++){

            const a =
                i/8*Math.PI*2;

            const r =
                i%2 === 0 ? 21 : 13;

            const x =
                Math.cos(a)*r;

            const y =
                Math.sin(a)*r;

            if(i===0){
                ctx.moveTo(x,y);
            }
            else{
                ctx.lineTo(x,y);
            }
        }

        ctx.closePath();

        ctx.fillStyle = "#b13dff";
        ctx.shadowBlur = 14;
        ctx.shadowColor = "#b13dff";
        ctx.fill();

        ctx.shadowBlur = 0;
    }

    else if(e.type === "hunter"){

        ctx.beginPath();

        ctx.moveTo(23,0);
        ctx.lineTo(0,-20);
        ctx.lineTo(-18,-9);
        ctx.lineTo(-10,0);
        ctx.lineTo(-18,9);
        ctx.lineTo(0,20);

        ctx.closePath();

        ctx.fillStyle = "#ff9b38";
        ctx.shadowBlur = 14;
        ctx.shadowColor = "#ff9b38";
        ctx.fill();

        ctx.shadowBlur = 0;
    }

    else if(e.type === "tank"){

        ctx.beginPath();

        ctx.rect(
            -23,
            -23,
            46,
            46
        );

        ctx.fillStyle = "#a62949";
        ctx.shadowBlur = 18;
        ctx.shadowColor = "#ff315f";
        ctx.fill();

        ctx.shadowBlur = 0;

        ctx.strokeStyle = "#ff6680";
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.beginPath();

        ctx.arc(
            0,
            0,
            11,
            0,
            Math.PI*2
        );

        ctx.fillStyle = "#421022";
        ctx.fill();
    }

    /*
       Health bar.
    */

    const width =
        e.radius*2.2;

    ctx.fillStyle = "rgba(0,0,0,.6)";

    ctx.fillRect(
        -width/2,
        -e.radius-9,
        width,
        4
    );

    ctx.fillStyle = "#ff536f";

    ctx.fillRect(
        -width/2,
        -e.radius-9,
        width *
        Math.max(
            0,
            e.health/e.maxHealth
        ),
        4
    );

    ctx.restore();
}

/* =========================================================
   DRAW BOSS
========================================================= */

function drawBoss(){

    if(!boss){
        return;
    }

    ctx.save();

    ctx.translate(boss.x,boss.y);
    ctx.rotate(boss.angle);

    /*
       Outer glow.
    */

    ctx.beginPath();

    ctx.arc(
        0,
        0,
        65 + Math.sin(boss.phase*4)*3,
        0,
        Math.PI*2
    );

    ctx.strokeStyle = "rgba(255,45,80,.45)";
    ctx.lineWidth = 4;
    ctx.shadowBlur = 30;
    ctx.shadowColor = "#ff234d";
    ctx.stroke();

    ctx.shadowBlur = 0;

    /*
       Main body.
    */

    ctx.beginPath();

    for(let i=0;i<12;i++){

        const a =
            i/12*Math.PI*2;

        const r =
            i%2 === 0
            ? 56
            : 39;

        const x =
            Math.cos(a)*r;

        const y =
            Math.sin(a)*r;

        if(i===0){
            ctx.moveTo(x,y);
        }
        else{
            ctx.lineTo(x,y);
        }
    }

    ctx.closePath();

    ctx.fillStyle = "#531026";
    ctx.fill();

    ctx.strokeStyle = "#ff405f";
    ctx.lineWidth = 3;
    ctx.stroke();

    /*
       Core.
    */

    ctx.beginPath();

    ctx.arc(
        0,
        0,
        19 + Math.sin(boss.phase*5)*3,
        0,
        Math.PI*2
    );

    ctx.fillStyle = "#ff3158";
    ctx.shadowBlur = 25;
    ctx.shadowColor = "#ff3158";
    ctx.fill();

    ctx.restore();
}

/* =========================================================
   DRAW BULLETS
========================================================= */

function drawBullets(){

    ctx.save();

    for(const b of bullets){

        ctx.strokeStyle = "#7ee6ff";
        ctx.lineWidth = 3;
        ctx.shadowBlur = 10;
        ctx.shadowColor = "#37cfff";

        ctx.beginPath();

        ctx.moveTo(
            b.x - b.vx*.015,
            b.y - b.vy*.015
        );

        ctx.lineTo(
            b.x,
            b.y
        );

        ctx.stroke();
    }

    ctx.restore();
}

function drawEnemyBullets(){

    ctx.save();

    for(const b of enemyBullets){

        ctx.fillStyle = "#ff4e6b";
        ctx.shadowBlur = 10;
        ctx.shadowColor = "#ff3158";

        ctx.beginPath();

        ctx.arc(
            b.x,
            b.y,
            b.radius,
            0,
            Math.PI*2
        );

        ctx.fill();
    }

    ctx.restore();
}

/* =========================================================
   DRAW POWERUPS
========================================================= */

function drawPowerups(){

    for(const p of powerups){

        const pulse =
            1 +
            Math.sin(p.phase*5)*.1;

        ctx.save();

        ctx.translate(p.x,p.y);
        ctx.scale(pulse,pulse);

        let symbol = "?";
        let color = "#fff";

        if(p.type === "heal"){
            symbol = "+";
            color = "#53ff91";
        }

        if(p.type === "shield"){
            symbol = "S";
            color = "#51d7ff";
        }

        if(p.type === "rapid"){
            symbol = "R";
            color = "#ffda4f";
        }

        if(p.type === "spread"){
            symbol = "3";
            color = "#c275ff";
        }

        if(p.type === "energy"){
            symbol = "E";
            color = "#5ccaff";
        }

        if(p.type === "bomb"){
            symbol = "B";
            color = "#ff5975";
        }

        ctx.beginPath();

        ctx.arc(
            0,
            0,
            13,
            0,
            Math.PI*2
        );

        ctx.fillStyle = "rgba(5,15,30,.8)";
        ctx.fill();

        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.shadowBlur = 14;
        ctx.shadowColor = color;
        ctx.stroke();

        ctx.shadowBlur = 0;

        ctx.fillStyle = color;
        ctx.font = "bold 12px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        ctx.fillText(
            symbol,
            0,
            1
        );

        ctx.restore();
    }
}

/* =========================================================
   DRAW WAVE MESSAGE
========================================================= */

function drawWaveMessage(){

    if(waveMessageTimer <= 0){
        return;
    }

    const alpha =
        Math.min(
            1,
            waveMessageTimer
        );

    ctx.save();

    ctx.globalAlpha = alpha;

    ctx.textAlign = "center";

    ctx.font =
        "900 30px Arial";

    ctx.fillStyle = "#eaf8ff";

    ctx.shadowBlur = 20;
    ctx.shadowColor = "#39baff";

    ctx.fillText(
        boss
        ? "BOSS INCOMING"
        : "WAVE " + wave,
        W/2,
        H/2
    );

    ctx.restore();
}

/* =========================================================
   DRAW
========================================================= */

function draw(){

    ctx.clearRect(
        0,
        0,
        W,
        H
    );

    /*
       Background.
    */

    const gradient =
        ctx.createRadialGradient(
            W/2,
            H/2,
            0,
            W/2,
            H/2,
            Math.max(W,H)*.8
        );

    gradient.addColorStop(
        0,
        "#07152c"
    );

    gradient.addColorStop(
        1,
        "#01040a"
    );

    ctx.fillStyle = gradient;

    ctx.fillRect(
        0,
        0,
        W,
        H
    );

    drawStars();
    drawGrid();

    /*
       Camera shake.
    */

    ctx.save();

    if(settings.shake){

        const sx =
            (Math.random()-.5) *
            screenShake;

        const sy =
            (Math.random()-.5) *
            screenShake;

        ctx.translate(sx,sy);
    }

    drawPowerups();
    drawBullets();
    drawEnemyBullets();

    for(const e of enemies){
        drawEnemy(e);
    }

    drawBoss();
    drawPlayer();

    drawParticles();

    ctx.restore();

    drawWaveMessage();
}

/* =========================================================
   HUD
========================================================= */

function updateHUD(){

    scoreText.textContent =
        Math.floor(score);

    waveText.textContent =
        wave;

    killsText.textContent =
        kills;

    healthText.textContent =
        Math.ceil(player.health);

    energyText.textContent =
        Math.ceil(player.energy);

    comboText.textContent =
        "x" + combo.toFixed(1);

    healthFill.style.width =
        Math.max(
            0,
            player.health/player.maxHealth*100
        ) + "%";

    energyFill.style.width =
        Math.max(
            0,
            player.energy/player.maxEnergy*100
        ) + "%";

    if(boss){

        bossHud.style.display = "block";

        bossFill.style.width =
            Math.max(
                0,
                boss.health/boss.maxHealth*100
            ) + "%";
    }
    else{

        bossHud.style.display = "none";
    }
}

/* =========================================================
   GAME RESET
========================================================= */

function resetGame(){

    clearTimeout(gameOverTimer);

    score = 0;
    wave = 1;
    kills = 0;
    waveKills = 0;

    combo = 1;
    comboTimer = 0;

    enemies = [];
    bullets = [];
    enemyBullets = [];
    particles = [];
    powerups = [];

    boss = null;

    spawnTimer = .5;
    waveMessageTimer = 1.5;

    screenShake = 0;

    bombCooldown = 0;

    player.x = W/2;
    player.y = H/2;

    player.angle = -Math.PI/2;

    player.health = player.maxHealth;
    player.energy = player.maxEnergy;

    player.fireCooldown = 0;

    player.rapidTimer = 0;
    player.spreadTimer = 0;
    player.shieldTimer = 0;
    player.invincibleTimer = 0;

    mouse.down = false;
    mouse.activeUntil = 0;

    touch.fire = false;
    touch.boost = false;

    resetJoystick();

    Object.keys(keys).forEach(k=>{
        keys[k] = false;
    });

    createStars();

    updateHUD();
}

/* =========================================================
   START
========================================================= */

function startGame(){

    initAudio();

    resetGame();

    /*
       IMPORTANT:
       There is no "gameScreen".

       We simply hide all menu screens and run the game.
    */

    hideAllScreens();

    running = true;
    paused = false;

    if(audioCtx && audioCtx.state === "suspended"){
        audioCtx.resume().catch(()=>{});
    }
}

/* =========================================================
   RESTART
========================================================= */

function restartGame(){

    initAudio();

    resetGame();

    hideAllScreens();

    running = true;
    paused = false;
}

/* =========================================================
   PAUSE
========================================================= */

function togglePause(){

    if(!running){
        return;
    }

    paused = !paused;

    if(paused){

        showScreen("pauseScreen");

    }
    else{

        hideAllScreens();
    }
}

/* =========================================================
   QUIT
========================================================= */

function quitGame(){

    clearTimeout(gameOverTimer);

    running = false;
    paused = false;

    boss = null;

    bossHud.style.display = "none";

    showScreen("menuScreen");
}

/* =========================================================
   GAME OVER
========================================================= */

function gameOver(){

    if(!running){
        return;
    }

    running = false;
    paused = false;

    addShake(15);

    particleBurst(
        player.x,
        player.y,
        70,
        400,
        "enemy"
    );

    beep(50,.7,"sawtooth",.05);

    clearTimeout(gameOverTimer);

    gameOverTimer = setTimeout(()=>{

        /*
           Prevent an old timeout from opening
           GAME OVER after the player restarted.
        */

        if(!running && !paused){

            document.getElementById(
                "finalScore"
            ).textContent =
                Math.floor(score);

            document.getElementById(
                "finalWave"
            ).textContent =
                wave;

            showScreen("gameOverScreen");
        }

    },500);
}

/* =========================================================
   HELPERS
========================================================= */

function distance(x1,y1,x2,y2){

    return Math.hypot(
        x2-x1,
        y2-y1
    );
}

function normalizeAngle(a){

    while(a > Math.PI){
        a -= Math.PI*2;
    }

    while(a < -Math.PI){
        a += Math.PI*2;
    }

    return a;
}

/* =========================================================
   MAIN LOOP
========================================================= */

let lastTime = performance.now();

function gameLoop(now){

    let dt =
        (now-lastTime)/1000;

    lastTime = now;

    /*
       Protect against tab switching,
       browser throttling, etc.
    */

    dt = Math.min(dt,.05);

    update(dt);
    draw();

    requestAnimationFrame(gameLoop);
}

requestAnimationFrame(gameLoop);

/* =========================================================
   EXTRA POINTER PREVENTION
========================================================= */

document.addEventListener("contextmenu",e=>{
    e.preventDefault();
});

document.addEventListener("touchmove",e=>{
    e.preventDefault();
},{
    passive:false
});

/* =========================================================
   INITIAL HUD
========================================================= */

updateHUD();

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
