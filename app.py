from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">

<title>VOID SPACE</title>

<style>
*{
    box-sizing:border-box;
    margin:0;
    padding:0;
}

html,body{
    width:100%;
    height:100%;
    overflow:hidden;
    background:#02030a;
    color:#fff;
    font-family:Arial,Helvetica,sans-serif;
}

body{
    touch-action:none;
}

#game{
    position:fixed;
    inset:0;
    width:100%;
    height:100%;
    display:block;
    background:#02030a;
    cursor:crosshair;
}

.screen{
    position:fixed;
    inset:0;
    z-index:20;
    display:none;
    align-items:center;
    justify-content:center;
    padding:20px;
    background:
        radial-gradient(circle at center,
        rgba(20,30,80,.30),
        rgba(0,0,0,.90));
}

.screen.active{
    display:flex;
}

.panel{
    width:min(700px,94vw);
    max-height:92vh;
    overflow:auto;
    padding:35px;
    border:1px solid rgba(100,180,255,.45);
    border-radius:20px;
    background:rgba(5,8,22,.94);
    box-shadow:
        0 0 40px rgba(0,140,255,.15),
        inset 0 0 30px rgba(0,100,255,.05);
    text-align:center;
}

.logo{
    font-size:clamp(42px,9vw,90px);
    font-weight:900;
    letter-spacing:8px;
    color:#fff;
    text-shadow:
        0 0 10px #4db8ff,
        0 0 30px #167eff,
        0 0 60px #0055ff;
    margin-bottom:8px;
}

.subtitle{
    color:#7fbfff;
    letter-spacing:5px;
    font-size:13px;
    margin-bottom:35px;
}

button{
    appearance:none;
    border:1px solid rgba(90,190,255,.7);
    background:
        linear-gradient(180deg,
        rgba(20,80,130,.85),
        rgba(5,25,55,.95));
    color:#fff;
    min-height:48px;
    padding:12px 24px;
    border-radius:10px;
    font-size:15px;
    font-weight:700;
    letter-spacing:1px;
    cursor:pointer;
    transition:.15s;
    margin:6px;
}

button:hover{
    transform:translateY(-2px);
    border-color:#fff;
    box-shadow:0 0 20px rgba(50,170,255,.45);
}

button:active{
    transform:scale(.97);
}

.primary{
    width:min(360px,90%);
    min-height:58px;
    font-size:18px;
}

.menu-buttons{
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:2px;
}

.info-grid{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:10px;
    margin:20px 0;
}

.info{
    padding:15px;
    border:1px solid rgba(100,170,255,.2);
    border-radius:12px;
    background:rgba(255,255,255,.025);
}

.info strong{
    display:block;
    color:#6fc4ff;
    margin-bottom:7px;
}

.controls{
    text-align:left;
    line-height:1.8;
    color:#d4e8ff;
}

.controls kbd{
    display:inline-block;
    min-width:34px;
    padding:2px 7px;
    border:1px solid #4f83aa;
    border-radius:5px;
    background:#091321;
    color:#fff;
    text-align:center;
    font-size:12px;
}

.setting-row{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:15px;
    padding:18px 0;
    border-bottom:1px solid rgba(255,255,255,.08);
}

.setting-value{
    color:#55c7ff;
    font-weight:bold;
}

#hud{
    position:fixed;
    z-index:10;
    top:12px;
    left:12px;
    right:12px;
    pointer-events:none;
    display:none;
}

.hud-row{
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
    gap:10px;
}

.hud-box{
    padding:10px 14px;
    border:1px solid rgba(80,180,255,.25);
    border-radius:9px;
    background:rgba(0,5,15,.65);
    backdrop-filter:blur(4px);
    font-size:12px;
}

.hud-box b{
    color:#6bc9ff;
}

#healthOuter,
#energyOuter{
    width:160px;
    height:8px;
    background:#101522;
    border-radius:20px;
    overflow:hidden;
    margin-top:5px;
}

#healthBar,
#energyBar{
    height:100%;
    width:100%;
    background:#39e69a;
    transition:width .1s;
}

#energyBar{
    background:#48aaff;
}

#rotationIndicator{
    color:#55cfff;
}

#touchControls{
    display:none;
    position:fixed;
    inset:0;
    z-index:15;
    pointer-events:none;
}

#joystick{
    position:absolute;
    left:25px;
    bottom:25px;
    width:140px;
    height:140px;
    border-radius:50%;
    border:2px solid rgba(100,190,255,.35);
    background:rgba(20,50,90,.18);
    pointer-events:auto;
}

#stick{
    position:absolute;
    width:58px;
    height:58px;
    left:39px;
    top:39px;
    border-radius:50%;
    background:rgba(80,190,255,.45);
    border:1px solid rgba(180,230,255,.8);
}

.touch-buttons{
    position:absolute;
    right:20px;
    bottom:20px;
    display:flex;
    flex-direction:column;
    gap:10px;
    pointer-events:auto;
}

.touch-btn{
    width:82px;
    height:58px;
    margin:0;
    padding:0;
    border-radius:15px;
    background:rgba(10,40,70,.7);
}

#fireTouch{
    width:105px;
    height:105px;
    border-radius:50%;
    background:rgba(140,30,40,.65);
}

#pauseHint{
    margin-top:15px;
    color:#7893ad;
    font-size:12px;
}

.gameover-score{
    font-size:42px;
    font-weight:900;
    color:#6dcaff;
    margin:15px 0 25px;
}

.small{
    color:#8197ad;
    font-size:12px;
}

#jsError{
    position:fixed;
    left:10px;
    right:10px;
    bottom:10px;
    z-index:999;
    display:none;
    padding:14px;
    border:1px solid #ff5555;
    border-radius:10px;
    background:#26080b;
    color:#ffaaaa;
    font-family:monospace;
    font-size:12px;
    white-space:pre-wrap;
}

@media (max-width:700px){
    .panel{
        padding:25px 18px;
    }

    .logo{
        letter-spacing:4px;
    }

    .info-grid{
        grid-template-columns:1fr;
    }

    .hud-box{
        padding:7px 9px;
        font-size:10px;
    }

    #healthOuter,
    #energyOuter{
        width:110px;
    }
}

@media (pointer:coarse){
    #touchControls{
        display:block;
    }

    #game{
        cursor:default;
    }
}
</style>
</head>

<body>

<canvas id="game"></canvas>

<div id="hud">
    <div class="hud-row">

        <div class="hud-box">
            <div>SCORE <b id="score">0</b></div>
            <div>WAVE <b id="wave">1</b></div>
            <div>KILLS <b id="kills">0</b></div>
        </div>

        <div class="hud-box">
            <div>HP</div>
            <div id="healthOuter">
                <div id="healthBar"></div>
            </div>

            <div style="margin-top:5px">ENERGY</div>
            <div id="energyOuter">
                <div id="energyBar"></div>
            </div>
        </div>

        <div class="hud-box">
            <div>ROTATION</div>
            <div id="rotationIndicator">360° ON</div>
            <div>BOOST <b id="boostText">READY</b></div>
        </div>

    </div>
</div>

<!-- MAIN MENU -->
<div class="screen active" id="menuScreen">
    <div class="panel">

        <div class="logo">VOID</div>
        <div class="subtitle">SPACE</div>

        <div class="menu-buttons">

            <button class="primary" id="startButton">
                START GAME
            </button>

            <button id="howButton">
                HOW TO PLAY
            </button>

            <button id="settingsButton">
                SETTINGS
            </button>

        </div>

        <div class="small" style="margin-top:25px">
            NO DATABASE • NO LOCAL STORAGE • FREE
        </div>

    </div>
</div>

<!-- HOW TO PLAY -->
<div class="screen" id="howScreen">
    <div class="panel">

        <h1>HOW TO PLAY</h1>

        <div class="info-grid">

            <div class="info">
                <strong>MOVEMENT</strong>
                <div class="controls">
                    <kbd>W</kbd> / <kbd>↑</kbd>
                    Forward<br>

                    <kbd>S</kbd> / <kbd>↓</kbd>
                    Backward
                </div>
            </div>

            <div class="info">
                <strong>360° ROTATION</strong>
                <div class="controls">
                    <kbd>A</kbd> / <kbd>←</kbd>
                    Rotate left continuously<br>

                    <kbd>D</kbd> / <kbd>→</kbd>
                    Rotate right continuously
                </div>
            </div>

            <div class="info">
                <strong>WEAPONS</strong>
                <div class="controls">
                    <kbd>SPACE</kbd> / <kbd>X</kbd>
                    Shoot<br>

                    <kbd>B</kbd>
                    Bomb
                </div>
            </div>

            <div class="info">
                <strong>SPECIAL</strong>
                <div class="controls">
                    <kbd>SHIFT</kbd>
                    Boost<br>

                    <kbd>P</kbd> / <kbd>ESC</kbd>
                    Pause
                </div>
            </div>

        </div>

        <p style="line-height:1.7;color:#a9c5df">
            Destroy incoming enemies, collect power-ups and survive
            increasingly difficult waves.
            Every fifth wave contains a boss.
        </p>

        <p id="pauseHint">
            Mouse: move to aim • Left click to shoot
        </p>

        <button id="howBackButton">BACK</button>

    </div>
</div>

<!-- SETTINGS -->
<div class="screen" id="settingsScreen">
    <div class="panel">

        <h1>SETTINGS</h1>

        <div class="setting-row">
            <span>360° KEYBOARD ROTATION</span>
            <span class="setting-value" id="rotationSetting">
                ON
            </span>
        </div>

        <button id="rotationButton">
            TOGGLE 360° ROTATION
        </button>

        <div class="setting-row">
            <span>TOUCH CONTROLS</span>
            <span class="setting-value">
                AUTO
            </span>
        </div>

        <div class="setting-row">
            <span>MOUSE AIM</span>
            <span class="setting-value">
                ON
            </span>
        </div>

        <button id="settingsBackButton">
            BACK
        </button>

    </div>
</div>

<!-- PAUSE -->
<div class="screen" id="pauseScreen">
    <div class="panel">

        <h1>PAUSED</h1>

        <p style="margin:20px 0;color:#91aeca">
            The universe is waiting.
        </p>

        <button class="primary" id="resumeButton">
            RESUME
        </button>

        <button id="restartPauseButton">
            RESTART
        </button>

        <button id="menuPauseButton">
            MAIN MENU
        </button>

    </div>
</div>

<!-- GAME OVER -->
<div class="screen" id="gameOverScreen">
    <div class="panel">

        <h1>GAME OVER</h1>

        <div class="gameover-score" id="finalScore">
            0
        </div>

        <div class="info-grid">

            <div class="info">
                <strong>WAVE</strong>
                <span id="finalWave">1</span>
            </div>

            <div class="info">
                <strong>KILLS</strong>
                <span id="finalKills">0</span>
            </div>

        </div>

        <button class="primary" id="restartButton">
            PLAY AGAIN
        </button>

        <button id="menuGameOverButton">
            MAIN MENU
        </button>

    </div>
</div>

<!-- TOUCH -->
<div id="touchControls">

    <div id="joystick">
        <div id="stick"></div>
    </div>

    <div class="touch-buttons">

        <button class="touch-btn" id="boostTouch">
            BOOST
        </button>

        <button class="touch-btn" id="bombTouch">
            BOMB
        </button>

        <button class="touch-btn" id="fireTouch">
            FIRE
        </button>

    </div>

</div>

<div id="jsError"></div>

<script>
"use strict";

/* =========================================================
   CANVAS
========================================================= */

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let W = 0;
let H = 0;
let DPR = 1;

function resize(){
    DPR = Math.min(window.devicePixelRatio || 1, 2);

    W = window.innerWidth;
    H = window.innerHeight;

    canvas.width = Math.floor(W * DPR);
    canvas.height = Math.floor(H * DPR);

    canvas.style.width = W + "px";
    canvas.style.height = H + "px";

    ctx.setTransform(DPR,0,0,DPR,0,0);
}

window.addEventListener("resize", resize);
resize();


/* =========================================================
   SCREEN SYSTEM
========================================================= */

const screens = [
    "menuScreen",
    "howScreen",
    "settingsScreen",
    "pauseScreen",
    "gameOverScreen"
];

function hideScreens(){
    for(const id of screens){
        document.getElementById(id).classList.remove("active");
    }
}

function showScreen(id){
    hideScreens();
    document.getElementById(id).classList.add("active");
}


/* =========================================================
   SETTINGS
========================================================= */

let rotation360 = true;

function updateRotationUI(){

    document.getElementById("rotationSetting").textContent =
        rotation360 ? "ON" : "OFF";

    document.getElementById("rotationIndicator").textContent =
        rotation360 ? "360° ON" : "STRAFE";
}

document.getElementById("rotationButton").addEventListener("click",()=>{
    rotation360 = !rotation360;
    updateRotationUI();
});

updateRotationUI();


/* =========================================================
   GAME STATE
========================================================= */

let running = false;
let paused = false;

let score = 0;
let wave = 1;
let kills = 0;

let waveTimer = 0;
let enemySpawnTimer = 0;
let powerTimer = 0;

let gameOverTimer = null;

let lastTime = performance.now();

const keys = {};

const mouse = {
    x: 0,
    y: 0,
    active: false,
    activeUntil: 0
};

const joystick = {
    active:false,
    x:0,
    y:0,
    pointerId:null
};


/* =========================================================
   PLAYER
========================================================= */

const player = {
    x:0,
    y:0,

    vx:0,
    vy:0,

    angle:0,

    radius:16,

    health:100,
    maxHealth:100,

    energy:100,
    maxEnergy:100,

    fireCooldown:0,
    boostCooldown:0,
    bombCooldown:0,

    invincible:0
};


/* =========================================================
   OBJECT ARRAYS
========================================================= */

let bullets = [];
let enemies = [];
let particles = [];
let stars = [];
let powerups = [];


/* =========================================================
   AUDIO
========================================================= */

let audioContext = null;

function initAudio(){

    if(!audioContext){
        try{
            audioContext =
                new (window.AudioContext ||
                     window.webkitAudioContext)();
        }catch(e){}
    }

    if(audioContext &&
       audioContext.state === "suspended"){
        audioContext.resume().catch(()=>{});
    }
}

function sound(freq,duration,type="sine",volume=.035){

    if(!audioContext) return;

    try{

        const osc = audioContext.createOscillator();
        const gain = audioContext.createGain();

        osc.type = type;
        osc.frequency.value = freq;

        gain.gain.value = volume;

        osc.connect(gain);
        gain.connect(audioContext.destination);

        osc.start();

        gain.gain.exponentialRampToValueAtTime(
            .0001,
            audioContext.currentTime + duration
        );

        osc.stop(audioContext.currentTime + duration);

    }catch(e){}
}


/* =========================================================
   STARS
========================================================= */

function createStars(){

    stars = [];

    const count = Math.max(100,Math.floor(W*H/9000));

    for(let i=0;i<count;i++){

        stars.push({
            x:Math.random()*W,
            y:Math.random()*H,
            z:.2 + Math.random()*.8,
            size:.5 + Math.random()*2
        });

    }
}


/* =========================================================
   RESET GAME
========================================================= */

function resetGame(){

    score = 0;
    wave = 1;
    kills = 0;

    waveTimer = 0;
    enemySpawnTimer = 0;
    powerTimer = 0;

    bullets = [];
    enemies = [];
    particles = [];
    powerups = [];

    player.x = W/2;
    player.y = H/2;

    player.vx = 0;
    player.vy = 0;

    player.angle = 0;

    player.health = 100;
    player.energy = 100;

    player.fireCooldown = 0;
    player.boostCooldown = 0;
    player.bombCooldown = 0;
    player.invincible = 0;

    createStars();

    updateHUD();
}


/* =========================================================
   START / PAUSE / END
========================================================= */

function startGame(){

    initAudio();

    if(gameOverTimer){
        clearTimeout(gameOverTimer);
        gameOverTimer = null;
    }

    resetGame();

    paused = false;
    running = true;

    hideScreens();

    sound(440,.08,"square",.025);
    sound(660,.12,"square",.018);
}

function togglePause(){

    if(!running) return;

    paused = !paused;

    if(paused){
        showScreen("pauseScreen");
    }else{
        hideScreens();
    }
}

function endGame(){

    if(!running) return;

    running = false;
    paused = false;

    document.getElementById("finalScore").textContent =
        score.toLocaleString();

    document.getElementById("finalWave").textContent =
        wave;

    document.getElementById("finalKills").textContent =
        kills;

    sound(100,.5,"sawtooth",.05);

    gameOverTimer = setTimeout(()=>{
        showScreen("gameOverScreen");
    },500);
}


/* =========================================================
   BUTTONS
========================================================= */

document.getElementById("startButton")
    .addEventListener("click",startGame);

document.getElementById("restartButton")
    .addEventListener("click",startGame);

document.getElementById("resumeButton")
    .addEventListener("click",togglePause);

document.getElementById("restartPauseButton")
    .addEventListener("click",startGame);

document.getElementById("menuPauseButton")
    .addEventListener("click",()=>{
        running = false;
        paused = false;
        showScreen("menuScreen");
    });

document.getElementById("menuGameOverButton")
    .addEventListener("click",()=>{
        showScreen("menuScreen");
    });

document.getElementById("howButton")
    .addEventListener("click",()=>{
        showScreen("howScreen");
    });

document.getElementById("settingsButton")
    .addEventListener("click",()=>{
        showScreen("settingsScreen");
    });

document.getElementById("howBackButton")
    .addEventListener("click",()=>{
        showScreen("menuScreen");
    });

document.getElementById("settingsBackButton")
    .addEventListener("click",()=>{
        showScreen("menuScreen");
    });


/* =========================================================
   KEYBOARD
========================================================= */

window.addEventListener("keydown",(e)=>{

    const code = e.code;

    if([
        "ArrowUp",
        "ArrowDown",
        "ArrowLeft",
        "ArrowRight",
        "Space"
    ].includes(code)){
        e.preventDefault();
    }

    keys[code] = true;

    if(code === "KeyP" ||
       code === "Escape"){

        if(!e.repeat){
            togglePause();
        }

        return;
    }

    if(code === "KeyB" && !e.repeat){
        useBomb();
    }

});

window.addEventListener("keyup",(e)=>{
    keys[e.code] = false;
});

window.addEventListener("blur",()=>{
    for(const k in keys){
        keys[k] = false;
    }

    joystick.active = false;
    joystick.x = 0;
    joystick.y = 0;
});


/* =========================================================
   MOUSE
========================================================= */

canvas.addEventListener("pointermove",(e)=>{

    if(e.pointerType !== "mouse") return;

    const rect = canvas.getBoundingClientRect();

    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;

    mouse.active = true;
    mouse.activeUntil = performance.now()+1200;

});

canvas.addEventListener("pointerdown",(e)=>{

    if(e.pointerType !== "mouse") return;

    if(e.button === 0){
        keys.MouseFire = true;
        shoot();
    }

});

canvas.addEventListener("pointerup",(e)=>{

    if(e.pointerType !== "mouse") return;

    if(e.button === 0){
        keys.MouseFire = false;
    }

});


/* =========================================================
   TOUCH JOYSTICK
========================================================= */

const joystickElement =
    document.getElementById("joystick");

const stickElement =
    document.getElementById("stick");

function updateJoystick(clientX,clientY){

    const rect =
        joystickElement.getBoundingClientRect();

    const cx = rect.left + rect.width/2;
    const cy = rect.top + rect.height/2;

    let dx = clientX-cx;
    let dy = clientY-cy;

    const max = rect.width*.38;

    const distance =
        Math.sqrt(dx*dx+dy*dy);

    if(distance > max){

        dx = dx/distance*max;
        dy = dy/distance*max;

    }

    joystick.x = dx/max;
    joystick.y = dy/max;

    stickElement.style.transform =
        "translate("+dx+"px,"+dy+"px)";
}

joystickElement.addEventListener("pointerdown",(e)=>{

    if(e.pointerType === "mouse") return;

    joystick.active = true;
    joystick.pointerId = e.pointerId;

    joystickElement.setPointerCapture(e.pointerId);

    updateJoystick(e.clientX,e.clientY);

});

joystickElement.addEventListener("pointermove",(e)=>{

    if(!joystick.active) return;

    updateJoystick(e.clientX,e.clientY);

});

function resetJoystick(){

    joystick.active = false;
    joystick.x = 0;
    joystick.y = 0;

    stickElement.style.transform =
        "translate(0px,0px)";
}

joystickElement.addEventListener(
    "pointerup",
    resetJoystick
);

joystickElement.addEventListener(
    "pointercancel",
    resetJoystick
);


/* =========================================================
   TOUCH BUTTONS
========================================================= */

const fireTouch =
    document.getElementById("fireTouch");

const boostTouch =
    document.getElementById("boostTouch");

const bombTouch =
    document.getElementById("bombTouch");

function touchHold(element,key){

    element.addEventListener("pointerdown",(e)=>{
        e.preventDefault();
        keys[key] = true;
    });

    element.addEventListener("pointerup",(e)=>{
        e.preventDefault();
        keys[key] = false;
    });

    element.addEventListener("pointercancel",()=>{
        keys[key] = false;
    });

    element.addEventListener("pointerleave",()=>{
        keys[key] = false;
    });
}

touchHold(fireTouch,"TouchFire");
touchHold(boostTouch,"TouchBoost");

bombTouch.addEventListener("pointerdown",(e)=>{
    e.preventDefault();
    useBomb();
});


/* =========================================================
   SHOOTING
========================================================= */

function shoot(){

    if(!running || paused) return;

    if(player.fireCooldown > 0) return;

    if(player.energy < 2) return;

    player.energy -= 2;

    player.fireCooldown = 0.12;

    const speed = 720;

    bullets.push({

        x:player.x +
           Math.cos(player.angle)*20,

        y:player.y +
           Math.sin(player.angle)*20,

        vx:Math.cos(player.angle)*speed +
           player.vx*.2,

        vy:Math.sin(player.angle)*speed +
           player.vy*.2,

        life:1.1,

        radius:3

    });

    createBurst(
        player.x + Math.cos(player.angle)*22,
        player.y + Math.sin(player.angle)*22,
        3,
        1.5
    );

    sound(620,.045,"square",.018);
}


/* =========================================================
   BOMB
========================================================= */

function useBomb(){

    if(!running || paused) return;

    if(player.bombCooldown > 0) return;

    if(player.energy < 35) return;

    player.energy -= 35;

    player.bombCooldown = 8;

    const radius = 260;

    for(const enemy of enemies){

        const dx = enemy.x-player.x;
        const dy = enemy.y-player.y;

        const d = Math.sqrt(dx*dx+dy*dy);

        if(d < radius){

            enemy.health -= 90;

            createBurst(
                enemy.x,
                enemy.y,
                12,
                4
            );
        }
    }

    createBurst(
        player.x,
        player.y,
        70,
        9
    );

    sound(90,.4,"sawtooth",.05);
}


/* =========================================================
   SPAWN ENEMY
========================================================= */

function spawnEnemy(){

    const side =
        Math.floor(Math.random()*4);

    let x;
    let y;

    if(side === 0){
        x = -50;
        y = Math.random()*H;
    }else if(side === 1){
        x = W+50;
        y = Math.random()*H;
    }else if(side === 2){
        x = Math.random()*W;
        y = -50;
    }else{
        x = Math.random()*W;
        y = H+50;
    }

    const roll = Math.random();

    let type = "fighter";

    if(roll < .12 && wave >= 3){
        type = "tank";
    }else if(roll < .30 && wave >= 2){
        type = "fast";
    }

    let enemy;

    if(type === "tank"){

        enemy = {
            x,y,
            vx:0,
            vy:0,
            radius:28,
            speed:55 + wave*2,
            health:120 + wave*20,
            maxHealth:120 + wave*20,
            damage:22,
            type,
            score:80
        };

    }else if(type === "fast"){

        enemy = {
            x,y,
            vx:0,
            vy:0,
            radius:11,
            speed:180 + wave*5,
            health:25 + wave*5,
            maxHealth:25 + wave*5,
            damage:12,
            type,
            score:40
        };

    }else{

        enemy = {
            x,y,
            vx:0,
            vy:0,
            radius:18,
            speed:90 + wave*3,
            health:45 + wave*7,
            maxHealth:45 + wave*7,
            damage:16,
            type,
            score:30
        };
    }

    enemies.push(enemy);
}


/* =========================================================
   BOSS
========================================================= */

function spawnBoss(){

    enemies.push({

        x:W/2,
        y:-100,

        vx:0,
        vy:0,

        radius:65,

        speed:55,

        health:900 + wave*150,

        maxHealth:900 + wave*150,

        damage:35,

        type:"boss",

        score:1000,

        boss:true,

        fireTimer:2

    });

    createBurst(W/2,100,50,6);

    sound(55,.8,"sawtooth",.06);
}


/* =========================================================
   POWERUPS
========================================================= */

function spawnPowerup(){

    const types = [
        "health",
        "energy",
        "rapid",
        "bomb"
    ];

    powerups.push({

        x:60+Math.random()*(W-120),
        y:60+Math.random()*(H-120),

        radius:13,

        type:
            types[Math.floor(Math.random()*types.length)],

        life:12

    });
}

function collectPowerup(power){

    if(power.type === "health"){

        player.health =
            Math.min(
                player.maxHealth,
                player.health+30
            );

    }else if(power.type === "energy"){

        player.energy =
            Math.min(
                player.maxEnergy,
                player.energy+45
            );

    }else if(power.type === "rapid"){

        player.fireCooldown = -2;

    }else if(power.type === "bomb"){

        player.energy =
            Math.min(
                player.maxEnergy,
                player.energy+20
            );

        player.bombCooldown = 0;
    }

    createBurst(
        power.x,
        power.y,
        20,
        3
    );

    sound(880,.12,"sine",.025);
}


/* =========================================================
   PARTICLES
========================================================= */

function createBurst(x,y,count,power){

    for(let i=0;i<count;i++){

        const a =
            Math.random()*Math.PI*2;

        const speed =
            Math.random()*power;

        particles.push({

            x,
            y,

            vx:Math.cos(a)*speed*60,
            vy:Math.sin(a)*speed*60,

            life:.3+Math.random()*.6,

            maxLife:.9,

            size:1+Math.random()*3

        });
    }
}


/* =========================================================
   COLLISION
========================================================= */

function distance(a,b){

    const dx = a.x-b.x;
    const dy = a.y-b.y;

    return Math.sqrt(dx*dx+dy*dy);
}


/* =========================================================
   UPDATE PLAYER
========================================================= */

function updatePlayer(dt){

    let forward = 0;
    let rotation = 0;

    if(keys.KeyW || keys.ArrowUp){
        forward += 1;
    }

    if(keys.KeyS || keys.ArrowDown){
        forward -= 1;
    }

    if(keys.KeyA || keys.ArrowLeft){
        rotation -= 1;
    }

    if(keys.KeyD || keys.ArrowRight){
        rotation += 1;
    }

    /*
       =====================================================
       THIS IS THE 360° ROTATION FIX

       A / LEFT  -> continuously decrease angle
       D / RIGHT -> continuously increase angle

       There is NO -90° / +90° limitation.
       The angle is allowed to continue beyond 360°.
       sin/cos naturally handle unlimited rotation.
       =====================================================
    */

    if(rotation360){

        player.angle += rotation * 4.2 * dt;

    }else{

        const strafe =
            rotation * 250 * dt;

        player.vx +=
            Math.cos(player.angle + Math.PI/2)
            * strafe;

        player.vy +=
            Math.sin(player.angle + Math.PI/2)
            * strafe;
    }

    /*
       TOUCH JOYSTICK
    */

    if(joystick.active){

        const magnitude =
            Math.sqrt(
                joystick.x*joystick.x +
                joystick.y*joystick.y
            );

        if(magnitude > .05){

            player.angle =
                Math.atan2(
                    joystick.y,
                    joystick.x
                );

            forward = magnitude;
        }
    }

    /*
       MOUSE AIM
    */

    if(
        mouse.active &&
        performance.now() < mouse.activeUntil
    ){

        player.angle =
            Math.atan2(
                mouse.y-player.y,
                mouse.x-player.x
            );
    }

    /*
       FORWARD / BACKWARD
    */

    const acceleration = 310;

    player.vx +=
        Math.cos(player.angle)
        * forward
        * acceleration
        * dt;

    player.vy +=
        Math.sin(player.angle)
        * forward
        * acceleration
        * dt;

    /*
       BOOST
    */

    const boosting =
        keys.ShiftLeft ||
        keys.ShiftRight ||
        keys.TouchBoost;

    if(
        boosting &&
        player.energy > 0
    ){

        player.vx +=
            Math.cos(player.angle)
            * 520
            * dt;

        player.vy +=
            Math.sin(player.angle)
            * 520
            * dt;

        player.energy -= 24*dt;

        document.getElementById("boostText")
            .textContent = "ACTIVE";

    }else{

        document.getElementById("boostText")
            .textContent =
                player.energy > 10
                ? "READY"
                : "LOW";
    }

    /*
       LIMIT SPEED
    */

    const maxSpeed =
        boosting ? 700 : 360;

    const speed =
        Math.sqrt(
            player.vx*player.vx +
            player.vy*player.vy
        );

    if(speed > maxSpeed){

        player.vx =
            player.vx/speed*maxSpeed;

        player.vy =
            player.vy/speed*maxSpeed;
    }

    /*
       FRICTION
    */

    player.vx *= Math.pow(.90,dt*60);
    player.vy *= Math.pow(.90,dt*60);

    player.x += player.vx*dt;
    player.y += player.vy*dt;

    /*
       SCREEN WRAP
    */

    const margin = 30;

    if(player.x < -margin)
        player.x = W+margin;

    if(player.x > W+margin)
        player.x = -margin;

    if(player.y < -margin)
        player.y = H+margin;

    if(player.y > H+margin)
        player.y = -margin;

    /*
       TIMERS
    */

    player.fireCooldown -= dt;
    player.boostCooldown -= dt;
    player.bombCooldown -= dt;

    player.invincible -= dt;

    /*
       ENERGY REGEN
    */

    player.energy =
        Math.min(
            player.maxEnergy,
            player.energy + 8*dt
        );

    /*
       SHOOT
    */

    if(
        keys.Space ||
        keys.KeyX ||
        keys.MouseFire ||
        keys.TouchFire
    ){

        shoot();
    }
}


/* =========================================================
   UPDATE BULLETS
========================================================= */

function updateBullets(dt){

    for(let i=bullets.length-1;i>=0;i--){

        const b = bullets[i];

        b.x += b.vx*dt;
        b.y += b.vy*dt;

        b.life -= dt;

        if(
            b.life <= 0 ||
            b.x < -100 ||
            b.x > W+100 ||
            b.y < -100 ||
            b.y > H+100
        ){

            bullets.splice(i,1);
        }
    }
}


/* =========================================================
   UPDATE ENEMIES
========================================================= */

function updateEnemies(dt){

    for(let i=enemies.length-1;i>=0;i--){

        const enemy = enemies[i];

        const dx = player.x-enemy.x;
        const dy = player.y-enemy.y;

        const dist =
            Math.sqrt(dx*dx+dy*dy) || 1;

        const nx = dx/dist;
        const ny = dy/dist;

        if(enemy.boss){

            enemy.y += 20*dt;

            if(enemy.y > 150){

                enemy.x +=
                    Math.sin(performance.now()/1000)
                    * 35
                    * dt;
            }

            enemy.fireTimer -= dt;

            if(enemy.fireTimer <= 0){

                enemy.fireTimer = 1.8;

                for(let k=0;k<7;k++){

                    const angle =
                        Math.atan2(dy,dx) +
                        (k-3)*.12;

                    bullets.push({

                        x:enemy.x,
                        y:enemy.y,

                        vx:Math.cos(angle)*260,
                        vy:Math.sin(angle)*260,

                        life:4,

                        radius:5,

                        enemyBullet:true

                    });
                }

                sound(100,.15,"sawtooth",.025);
            }

        }else{

            enemy.vx = nx*enemy.speed;
            enemy.vy = ny*enemy.speed;

            enemy.x += enemy.vx*dt;
            enemy.y += enemy.vy*dt;
        }

        /*
           ENEMY -> PLAYER
        */

        if(dist < enemy.radius+player.radius){

            if(player.invincible <= 0){

                player.health -= enemy.damage;

                player.invincible = .8;

                player.vx -= nx*220;
                player.vy -= ny*220;

                createBurst(
                    player.x,
                    player.y,
                    20,
                    4
                );

                sound(70,.18,"sawtooth",.04);

                if(!enemy.boss){
                    enemy.health = 0;
                }

                if(player.health <= 0){

                    player.health = 0;

                    endGame();
                }
            }
        }

        /*
           REMOVE DEAD
        */

        if(enemy.health <= 0){

            score += enemy.score;
            kills++;

            createBurst(
                enemy.x,
                enemy.y,
                enemy.boss ? 100 : 25,
                enemy.boss ? 9 : 4
            );

            if(enemy.boss){

                score += 2000;

                for(let p=0;p<3;p++){
                    spawnPowerup();
                }

            }else if(Math.random() < .12){

                powerups.push({

                    x:enemy.x,
                    y:enemy.y,

                    radius:13,

                    type:[
                        "health",
                        "energy",
                        "rapid",
                        "bomb"
                    ][Math.floor(Math.random()*4)],

                    life:12
                });
            }

            enemies.splice(i,1);

            sound(
                enemy.boss ? 60 : 160,
                enemy.boss ? .4 : .08,
                "sawtooth",
                enemy.boss ? .06 : .02
            );
        }
    }
}


/* =========================================================
   BULLET COLLISIONS
========================================================= */

function bulletCollisions(){

    for(let i=bullets.length-1;i>=0;i--){

        const bullet = bullets[i];

        if(bullet.enemyBullet){

            const dx = player.x-bullet.x;
            const dy = player.y-bullet.y;

            const d =
                Math.sqrt(dx*dx+dy*dy);

            if(
                d <
                player.radius+bullet.radius
            ){

                if(player.invincible <= 0){

                    player.health -= 12;

                    player.invincible = .25;

                    createBurst(
                        player.x,
                        player.y,
                        8,
                        3
                    );

                    if(player.health <= 0){
                        player.health = 0;
                        endGame();
                    }
                }

                bullets.splice(i,1);
            }

            continue;
        }

        let hit = false;

        for(let j=enemies.length-1;j>=0;j--){

            const enemy = enemies[j];

            const dx = enemy.x-bullet.x;
            const dy = enemy.y-bullet.y;

            const d =
                Math.sqrt(dx*dx+dy*dy);

            if(
                d <
                enemy.radius+bullet.radius
            ){

                enemy.health -=
                    enemy.boss ? 16 : 30;

                createBurst(
                    bullet.x,
                    bullet.y,
                    5,
                    2
                );

                hit = true;

                break;
            }
        }

        if(hit){
            bullets.splice(i,1);
        }
    }
}


/* =========================================================
   UPDATE POWERUPS
========================================================= */

function updatePowerups(dt){

    for(let i=powerups.length-1;i>=0;i--){

        const p = powerups[i];

        p.life -= dt;

        if(distance(p,player) <
           p.radius+player.radius){

            collectPowerup(p);

            powerups.splice(i,1);

        }else if(p.life <= 0){

            powerups.splice(i,1);
        }
    }
}


/* =========================================================
   UPDATE PARTICLES
========================================================= */

function updateParticles(dt){

    for(let i=particles.length-1;i>=0;i--){

        const p = particles[i];

        p.x += p.vx*dt;
        p.y += p.vy*dt;

        p.vx *= .96;
        p.vy *= .96;

        p.life -= dt;

        if(p.life <= 0){
            particles.splice(i,1);
        }
    }
}


/* =========================================================
   WAVE SYSTEM
========================================================= */

function updateWave(dt){

    waveTimer += dt;

    /*
       New wave every 18 seconds if
       current enemies are mostly cleared.
    */

    if(
        waveTimer > 18 &&
        enemies.filter(e=>!e.boss).length < 5
    ){

        waveTimer = 0;
        wave++;

        createBurst(
            W/2,
            H/2,
            40,
            5
        );

        sound(220,.3,"square",.03);

        if(wave % 5 === 0){

            spawnBoss();

        }
    }

    enemySpawnTimer -= dt;

    const enemyCount =
        enemies.filter(e=>!e.boss).length;

    const maximum =
        Math.min(
            8+wave*2,
            35
        );

    if(
        enemySpawnTimer <= 0 &&
        enemyCount < maximum
    ){

        enemySpawnTimer =
            Math.max(
                .25,
                1.2-wave*.035
            );

        spawnEnemy();
    }

    powerTimer -= dt;

    if(powerTimer <= 0){

        powerTimer =
            10+Math.random()*8;

        if(powerups.length < 3){
            spawnPowerup();
        }
    }
}


/* =========================================================
   UPDATE STARS
========================================================= */

function updateStars(dt){

    for(const s of stars){

        s.y +=
            (15+s.z*35)*dt;

        if(s.y > H){
            s.y = 0;
            s.x = Math.random()*W;
        }
    }
}


/* =========================================================
   UPDATE GAME
========================================================= */

function update(dt){

    if(!running || paused) return;

    dt = Math.min(dt,.033);

    updateStars(dt);
    updatePlayer(dt);
    updateBullets(dt);
    updateEnemies(dt);
    bulletCollisions();
    updatePowerups(dt);
    updateParticles(dt);
    updateWave(dt);

    updateHUD();
}


/* =========================================================
   DRAW BACKGROUND
========================================================= */

function drawBackground(){

    ctx.fillStyle = "#02030a";
    ctx.fillRect(0,0,W,H);

    /*
       Stars
    */

    for(const s of stars){

        ctx.globalAlpha =
            .25+s.z*.65;

        ctx.fillStyle = "#b7ddff";

        ctx.beginPath();

        ctx.arc(
            s.x,
            s.y,
            s.size*s.z,
            0,
            Math.PI*2
        );

        ctx.fill();
    }

    ctx.globalAlpha = 1;

    /*
       Grid
    */

    ctx.strokeStyle =
        "rgba(40,100,160,.08)";

    ctx.lineWidth = 1;

    const grid = 80;

    for(let x=0;x<W;x+=grid){

        ctx.beginPath();
        ctx.moveTo(x,0);
        ctx.lineTo(x,H);
        ctx.stroke();
    }

    for(let y=0;y<H;y+=grid){

        ctx.beginPath();
        ctx.moveTo(0,y);
        ctx.lineTo(W,y);
        ctx.stroke();
    }
}


/* =========================================================
   DRAW PLAYER
========================================================= */

function drawPlayer(){

    ctx.save();

    ctx.translate(player.x,player.y);
    ctx.rotate(player.angle);

    /*
       Glow
    */

    ctx.shadowBlur = 25;
    ctx.shadowColor = "#4dbbff";

    /*
       Ship body
    */

    ctx.beginPath();

    ctx.moveTo(24,0);
    ctx.lineTo(-16,-12);
    ctx.lineTo(-9,0);
    ctx.lineTo(-16,12);
    ctx.closePath();

    ctx.fillStyle =
        player.invincible > 0
        ? "#ffffff"
        : "#63caff";

    ctx.fill();

    ctx.shadowBlur = 0;

    /*
       Cockpit
    */

    ctx.beginPath();

    ctx.arc(
        2,
        0,
        5,
        0,
        Math.PI*2
    );

    ctx.fillStyle = "#ffffff";
    ctx.fill();

    /*
       Engine
    */

    ctx.beginPath();

    ctx.moveTo(-15,-6);
    ctx.lineTo(
        -29-Math.random()*7,
        0
    );
    ctx.lineTo(-15,6);
    ctx.closePath();

    ctx.fillStyle = "#ff9b4a";
    ctx.fill();

    ctx.restore();
}


/* =========================================================
   DRAW BULLETS
========================================================= */

function drawBullets(){

    for(const b of bullets){

        ctx.save();

        ctx.shadowBlur = 12;

        ctx.shadowColor =
            b.enemyBullet
            ? "#ff4040"
            : "#6eeaff";

        ctx.fillStyle =
            b.enemyBullet
            ? "#ff5555"
            : "#ffffff";

        ctx.beginPath();

        ctx.arc(
            b.x,
            b.y,
            b.radius,
            0,
            Math.PI*2
        );

        ctx.fill();

        ctx.restore();
    }
}


/* =========================================================
   DRAW ENEMIES
========================================================= */

function drawEnemy(enemy){

    ctx.save();

    ctx.translate(enemy.x,enemy.y);

    const angle =
        Math.atan2(
            player.y-enemy.y,
            player.x-enemy.x
        );

    ctx.rotate(angle);

    ctx.shadowBlur =
        enemy.boss ? 30 : 15;

    ctx.shadowColor =
        enemy.boss ? "#c040ff" : "#ff4f6d";

    ctx.fillStyle =
        enemy.boss ? "#8f42bd" :
        enemy.type === "tank" ? "#8e2938" :
        enemy.type === "fast" ? "#e54a61" :
        "#bd354f";

    ctx.beginPath();

    if(enemy.boss){

        for(let i=0;i<12;i++){

            const a =
                i/12*Math.PI*2;

            const r =
                i%2===0
                ? enemy.radius
                : enemy.radius*.68;

            const x = Math.cos(a)*r;
            const y = Math.sin(a)*r;

            if(i===0){
                ctx.moveTo(x,y);
            }else{
                ctx.lineTo(x,y);
            }
        }

        ctx.closePath();

    }else{

        ctx.moveTo(enemy.radius,0);
        ctx.lineTo(-enemy.radius*.7,-enemy.radius*.75);
        ctx.lineTo(-enemy.radius*.7,enemy.radius*.75);
        ctx.closePath();
    }

    ctx.fill();

    ctx.shadowBlur = 0;

    /*
       Enemy health bar
    */

    if(enemy.health < enemy.maxHealth){

        const barWidth =
            enemy.radius*2;

        ctx.fillStyle =
            "rgba(0,0,0,.6)";

        ctx.fillRect(
            -barWidth/2,
            -enemy.radius-9,
            barWidth,
            4
        );

        ctx.fillStyle =
            "#ff6578";

        ctx.fillRect(
            -barWidth/2,
            -enemy.radius-9,
            barWidth*
            Math.max(
                0,
                enemy.health/enemy.maxHealth
            ),
            4
        );
    }

    ctx.restore();
}

function drawEnemies(){

    for(const enemy of enemies){
        drawEnemy(enemy);
    }
}


/* =========================================================
   DRAW POWERUPS
========================================================= */

function drawPowerups(){

    for(const p of powerups){

        const pulse =
            1+Math.sin(
                performance.now()/200
            )*.15;

        ctx.save();

        ctx.translate(p.x,p.y);
        ctx.scale(pulse,pulse);

        ctx.shadowBlur = 18;

        ctx.shadowColor =
            "#5cffb0";

        ctx.strokeStyle =
            "#7affc2";

        ctx.lineWidth = 2;

        ctx.beginPath();

        ctx.arc(
            0,
            0,
            p.radius,
            0,
            Math.PI*2
        );

        ctx.stroke();

        ctx.shadowBlur = 0;

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 12px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        let symbol = "?";

        if(p.type === "health") symbol = "+";
        if(p.type === "energy") symbol = "E";
        if(p.type === "rapid") symbol = "R";
        if(p.type === "bomb") symbol = "B";

        ctx.fillText(symbol,0,1);

        ctx.restore();
    }
}


/* =========================================================
   DRAW PARTICLES
========================================================= */

function drawParticles(){

    for(const p of particles){

        ctx.globalAlpha =
            Math.max(
                0,
                p.life/p.maxLife
            );

        ctx.fillStyle = "#8edcff";

        ctx.beginPath();

        ctx.arc(
            p.x,
            p.y,
            p.size,
            0,
            Math.PI*2
        );

        ctx.fill();
    }

    ctx.globalAlpha = 1;
}


/* =========================================================
   DRAW AIM LINE
========================================================= */

function drawAim(){

    if(!running) return;

    if(
        mouse.active &&
        performance.now() < mouse.activeUntil
    ){

        ctx.save();

        ctx.strokeStyle =
            "rgba(100,210,255,.12)";

        ctx.setLineDash([5,10]);

        ctx.beginPath();

        ctx.moveTo(
            player.x,
            player.y
        );

        ctx.lineTo(
            player.x +
            Math.cos(player.angle)*180,

            player.y +
            Math.sin(player.angle)*180
        );

        ctx.stroke();

        ctx.restore();
    }
}


/* =========================================================
   DRAW
========================================================= */

function draw(){

    drawBackground();

    drawParticles();
    drawPowerups();
    drawBullets();
    drawEnemies();
    drawAim();

    if(running){
        drawPlayer();
    }
}


/* =========================================================
   HUD
========================================================= */

function updateHUD(){

    document.getElementById("score")
        .textContent =
            score.toLocaleString();

    document.getElementById("wave")
        .textContent = wave;

    document.getElementById("kills")
        .textContent = kills;

    document.getElementById("healthBar")
        .style.width =
            Math.max(
                0,
                player.health/
                player.maxHealth*100
            )+"%";

    document.getElementById("energyBar")
        .style.width =
            Math.max(
                0,
                player.energy/
                player.maxEnergy*100
            )+"%";

    document.getElementById("hud")
        .style.display =
            running ? "block" : "none";
}


/* =========================================================
   MAIN LOOP
========================================================= */

function gameLoop(now){

    const dt =
        Math.min(
            (now-lastTime)/1000,
            .05
        );

    lastTime = now;

    update(dt);
    draw();

    requestAnimationFrame(gameLoop);
}

requestAnimationFrame(gameLoop);


/* =========================================================
   ERROR DISPLAY
========================================================= */

window.addEventListener("error",(event)=>{

    const box =
        document.getElementById("jsError");

    if(!box) return;

    box.style.display = "block";

    box.textContent =
        "JAVASCRIPT ERROR:\n" +
        event.message +
        "\nLine: " +
        event.lineno;

});


/* =========================================================
   INITIAL STATE
========================================================= */

createStars();
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
