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

<meta name="theme-color" content="#02040b">
<meta name="description" content="VOID SPACE - Free browser space combat game">
<title>VOID SPACE // FREE EDITION</title>

<style>
*{
    box-sizing:border-box;
    -webkit-tap-highlight-color:transparent;
}

html,body{
    margin:0;
    width:100%;
    height:100%;
    overflow:hidden;
    background:#01030a;
    color:#eaf8ff;
    font-family:Arial,Helvetica,sans-serif;
    touch-action:none;
}

body{
    user-select:none;
}

canvas{
    position:fixed;
    inset:0;
    width:100%;
    height:100%;
    display:block;
    background:#01030a;
}

.screen{
    position:fixed;
    inset:0;
    display:flex;
    justify-content:center;
    align-items:center;
    padding:18px;
    opacity:0;
    visibility:hidden;
    pointer-events:none;
    transition:.2s;
    z-index:20;
}

.screen.active{
    opacity:1;
    visibility:visible;
    pointer-events:auto;
}

.panel{
    width:min(95vw,720px);
    max-height:92vh;
    overflow:auto;
    padding:32px;
    border-radius:24px;
    border:1px solid rgba(79,200,255,.4);
    background:rgba(2,8,20,.92);
    box-shadow:
        0 0 60px rgba(0,150,255,.15),
        inset 0 0 50px rgba(0,120,255,.04);
    backdrop-filter:blur(15px);
    text-align:center;
}

.logo{
    font-size:clamp(40px,9vw,82px);
    font-weight:900;
    letter-spacing:.12em;
    line-height:.9;
    color:#effcff;
    text-shadow:
        0 0 10px #4ed9ff,
        0 0 30px rgba(40,190,255,.7),
        0 0 70px rgba(0,130,255,.4);
}

.subtitle{
    margin-top:14px;
    color:#70b9da;
    font-size:11px;
    letter-spacing:.3em;
}

.buttons{
    display:grid;
    gap:11px;
    margin-top:30px;
}

button{
    border:1px solid rgba(90,205,255,.45);
    border-radius:13px;
    min-height:52px;
    padding:14px 18px;
    color:#eaffff;
    background:linear-gradient(
        180deg,
        rgba(25,92,135,.6),
        rgba(5,28,54,.85)
    );
    font-size:14px;
    font-weight:800;
    letter-spacing:.08em;
    cursor:pointer;
    transition:.12s;
}

button:hover{
    background:linear-gradient(
        180deg,
        rgba(40,130,180,.75),
        rgba(8,43,75,.95)
    );
}

button:active{
    transform:scale(.97);
}

.primary{
    background:linear-gradient(
        180deg,
        #159bdc,
        #075281
    );
    box-shadow:0 0 25px rgba(20,160,230,.25);
}

.danger{
    border-color:rgba(255,70,100,.5);
}

.small{
    margin-top:18px;
    color:#648ba0;
    font-size:10px;
    letter-spacing:.08em;
}

.instructions{
    text-align:left;
    color:#a7c7d8;
    line-height:1.65;
    font-size:14px;
    margin-top:20px;
}

.instructions strong{
    color:white;
}

#hud{
    position:fixed;
    inset:0;
    pointer-events:none;
    z-index:5;
    opacity:0;
    transition:.2s;
}

#hud.active{
    opacity:1;
}

.hud-top{
    position:absolute;
    left:15px;
    right:15px;
    top:15px;
    display:flex;
    gap:10px;
    justify-content:space-between;
}

.hud-box{
    min-width:120px;
    padding:9px 13px;
    border-radius:12px;
    border:1px solid rgba(90,190,240,.25);
    background:rgba(1,8,19,.66);
    backdrop-filter:blur(10px);
}

.label{
    color:#658ba1;
    font-size:8px;
    letter-spacing:.16em;
}

.value{
    margin-top:3px;
    font-size:17px;
    font-weight:900;
}

#bossHud{
    position:absolute;
    top:95px;
    left:50%;
    transform:translateX(-50%);
    width:min(500px,70vw);
    display:none;
}

.boss-name{
    text-align:center;
    color:#ff91a4;
    font-weight:900;
    font-size:11px;
    letter-spacing:.2em;
    margin-bottom:5px;
}

.bar{
    height:9px;
    border-radius:20px;
    overflow:hidden;
    border:1px solid rgba(255,100,120,.35);
    background:rgba(0,0,0,.6);
}

.fill{
    width:100%;
    height:100%;
    transition:width:.12s;
}

.boss-fill{
    background:linear-gradient(90deg,#ff304e,#ffb2bc);
    box-shadow:0 0 15px #ff405e;
}

#pauseButton{
    position:absolute;
    right:15px;
    top:75px;
    pointer-events:auto;
    min-height:40px;
    width:48px;
    padding:0;
    font-size:17px;
}

.status{
    position:absolute;
    left:15px;
    bottom:18px;
    width:min(300px,52vw);
}

.status-row{
    margin-top:8px;
}

.status-label{
    color:#7199ad;
    font-size:8px;
    letter-spacing:.15em;
    margin-bottom:4px;
}

.hull-fill{
    background:linear-gradient(90deg,#1eb9ff,#d5f8ff);
    box-shadow:0 0 14px rgba(40,200,255,.7);
}

.shield-fill{
    background:linear-gradient(90deg,#586bff,#cbd0ff);
    box-shadow:0 0 14px rgba(100,110,255,.7);
}

.energy-fill{
    background:linear-gradient(90deg,#bd55ff,#f0bfff);
    box-shadow:0 0 14px rgba(190,80,255,.7);
}

#weaponHud{
    position:absolute;
    right:15px;
    bottom:18px;
    text-align:right;
}

.weapon-name{
    color:#8ee9ff;
    font-size:17px;
    font-weight:900;
}

.weapon-info{
    color:#668ca1;
    font-size:9px;
    letter-spacing:.12em;
}

#abilityHud{
    margin-top:8px;
    color:#b8a3ff;
    font-size:10px;
}

#mobileControls{
    position:fixed;
    inset:0;
    z-index:8;
    pointer-events:none;
    opacity:0;
}

#mobileControls.active{
    opacity:1;
}

.joystick{
    position:absolute;
    left:20px;
    bottom:22px;
    width:135px;
    height:135px;
    border-radius:50%;
    border:1px solid rgba(90,210,255,.28);
    background:rgba(5,28,50,.35);
    pointer-events:auto;
}

.stick{
    position:absolute;
    left:39px;
    top:39px;
    width:57px;
    height:57px;
    border-radius:50%;
    border:1px solid rgba(130,225,255,.65);
    background:rgba(60,175,235,.38);
}

.actions{
    position:absolute;
    right:18px;
    bottom:18px;
    display:flex;
    align-items:flex-end;
    gap:9px;
    pointer-events:auto;
}

.actions button{
    width:67px;
    height:67px;
    min-height:67px;
    padding:4px;
    border-radius:50%;
    font-size:9px;
}

.actions .fire{
    width:98px;
    height:98px;
    min-height:98px;
    border-color:rgba(80,220,255,.75);
    background:rgba(10,110,160,.6);
}

#damageFlash{
    position:fixed;
    inset:0;
    pointer-events:none;
    z-index:15;
    background:rgba(255,30,60,.3);
    opacity:0;
}

.gameover-score{
    margin:22px 0;
    font-size:45px;
    font-weight:900;
    color:#8eeaff;
}

.shop-grid{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:10px;
    margin-top:20px;
}

.shop-card{
    text-align:left;
    padding:15px;
    border:1px solid rgba(90,190,240,.2);
    border-radius:14px;
    background:rgba(10,30,50,.5);
}

.shop-card h3{
    margin:0 0 8px;
    font-size:14px;
}

.shop-card p{
    color:#789bad;
    font-size:11px;
    min-height:30px;
}

.shop-card button{
    width:100%;
    min-height:42px;
    font-size:10px;
}

@media(max-width:700px){
    .panel{
        padding:24px 18px;
    }

    .hud-top{
        left:8px;
        right:8px;
        top:8px;
    }

    .hud-box{
        min-width:0;
        flex:1;
        padding:7px 8px;
    }

    .value{
        font-size:13px;
    }

    .status{
        bottom:170px;
        left:14px;
        width:155px;
    }

    #weaponHud{
        bottom:175px;
        right:14px;
    }

    #bossHud{
        top:83px;
    }

    .shop-grid{
        grid-template-columns:1fr;
    }
}

@media(min-width:800px){
    #mobileControls{
        display:none!important;
    }
}
</style>
</head>

<body>

<canvas id="game"></canvas>
<div id="damageFlash"></div>

<!-- MAIN MENU -->
<div class="screen active" id="menu">
<div class="panel">

<div class="logo">VOID SPACE</div>
<div class="subtitle">DEEP SPACE COMBAT SYSTEM // FREE EDITION</div>

<div class="buttons">
<button class="primary" id="playBtn">START MISSION</button>
<button id="shipBtn">SHIP HANGAR</button>
<button id="shopBtn">UPGRADE SYSTEM</button>
<button id="missionBtn">MISSIONS</button>
<button id="howBtn">HOW TO PLAY</button>
<button id="settingsBtn">SETTINGS</button>
<button id="fullscreenBtn">FULLSCREEN</button>
</div>

<div class="small">
HTML5 CANVAS • PYTHON FLASK • PROCEDURAL GRAPHICS • OFFLINE
</div>

</div>
</div>

<!-- HOW -->
<div class="screen" id="howScreen">
<div class="panel">
<div class="logo" style="font-size:43px">HOW TO PLAY</div>

<div class="instructions">

<p><strong>OBJECTIVE</strong><br>
Destroy hostile spacecraft, survive increasingly difficult waves,
collect power-ups, defeat bosses and upgrade your ship.</p>

<p><strong>DESKTOP</strong><br>
WASD / Arrow Keys — Move<br>
Mouse — Aim<br>
Left Mouse / SPACE — Fire<br>
SHIFT — Boost<br>
1–5 — Weapons<br>
Q — Special Ability<br>
P / ESC — Pause</p>

<p><strong>MOBILE</strong><br>
Joystick — Move<br>
FIRE — Fire weapon<br>
BOOST — Boost<br>
MISSILE — Missile special<br>
EMP — EMP special</p>

<p><strong>WEAPONS</strong><br>
Pulse Laser, Plasma Cannon, Spread Cannon,
Missile Launcher and Void Beam.</p>

<p><strong>ENEMIES</strong><br>
Fighters, Fast Fighters, Heavy Ships, Snipers,
Kamikazes, Shielded ships and Elite enemies.</p>

<p><strong>BOSSES</strong><br>
Every major sector ends with a boss encounter.
Bosses have multiple phases and special attacks.</p>

</div>

<div class="buttons">
<button id="howBack">BACK</button>
</div>
</div>
</div>

<!-- SETTINGS -->
<div class="screen" id="settingsScreen">
<div class="panel">
<div class="logo" style="font-size:43px">SETTINGS</div>

<div class="buttons">
<button id="soundSetting">SOUND: ON</button>
<button id="shakeSetting">SCREEN SHAKE: ON</button>
<button id="mobileSetting">MOBILE CONTROLS: ON</button>
</div>

<div class="buttons">
<button id="settingsBack">BACK</button>
</div>
</div>
</div>

<!-- SHIP -->
<div class="screen" id="shipScreen">
<div class="panel">
<div class="logo" style="font-size:43px">SHIP HANGAR</div>
<div id="shipStats" class="instructions"></div>

<div class="buttons">
<button class="primary" id="selectShip">USE VOID FALCON</button>
<button id="shipBack">BACK</button>
</div>
</div>
</div>

<!-- SHOP -->
<div class="screen" id="shopScreen">
<div class="panel">
<div class="logo" style="font-size:43px">UPGRADE SYSTEM</div>
<div id="creditsDisplay" class="subtitle"></div>

<div class="shop-grid">

<div class="shop-card">
<h3>HULL</h3>
<p>Increase maximum hull integrity.</p>
<button onclick="buyUpgrade('hull')">UPGRADE</button>
</div>

<div class="shop-card">
<h3>SHIELD</h3>
<p>Increase maximum shield capacity.</p>
<button onclick="buyUpgrade('shield')">UPGRADE</button>
</div>

<div class="shop-card">
<h3>ENGINE</h3>
<p>Increase movement speed.</p>
<button onclick="buyUpgrade('speed')">UPGRADE</button>
</div>

<div class="shop-card">
<h3>WEAPON</h3>
<p>Increase weapon damage.</p>
<button onclick="buyUpgrade('damage')">UPGRADE</button>
</div>

<div class="shop-card">
<h3>FIRE RATE</h3>
<p>Reduce weapon cooldown.</p>
<button onclick="buyUpgrade('fireRate')">UPGRADE</button>
</div>

<div class="shop-card">
<h3>ENERGY</h3>
<p>Increase maximum energy.</p>
<button onclick="buyUpgrade('energy')">UPGRADE</button>
</div>

</div>

<div class="buttons">
<button id="shopBack">BACK</button>
</div>
</div>
</div>

<!-- MISSIONS -->
<div class="screen" id="missionScreen">
<div class="panel">
<div class="logo" style="font-size:43px">MISSIONS</div>
<div id="missionsList" class="instructions"></div>

<div class="buttons">
<button id="missionBack">BACK</button>
</div>
</div>
</div>

<!-- PAUSE -->
<div class="screen" id="pauseScreen">
<div class="panel">
<div class="logo" style="font-size:50px">PAUSED</div>
<div class="subtitle">MISSION SUSPENDED</div>

<div class="buttons">
<button class="primary" id="resumeBtn">RESUME</button>
<button id="restartBtn">RESTART</button>
<button id="exitBtn">EXIT TO MENU</button>
</div>
</div>
</div>

<!-- GAME OVER -->
<div class="screen" id="gameOverScreen">
<div class="panel">
<div class="logo" style="font-size:45px">MISSION LOST</div>
<div class="subtitle">SHIP DESTROYED</div>

<div class="gameover-score" id="finalScore">0</div>
<div id="finalStats" class="small"></div>

<div class="buttons">
<button class="primary" id="againBtn">TRY AGAIN</button>
<button id="gameOverExit">MAIN MENU</button>
</div>
</div>
</div>

<!-- HUD -->
<div id="hud">

<div class="hud-top">

<div class="hud-box">
<div class="label">SCORE</div>
<div class="value" id="score">0</div>
</div>

<div class="hud-box">
<div class="label">WAVE</div>
<div class="value" id="wave">1</div>
</div>

<div class="hud-box">
<div class="label">LEVEL</div>
<div class="value" id="level">1</div>
</div>

<div class="hud-box">
<div class="label">CREDITS</div>
<div class="value" id="credits">0</div>
</div>

</div>

<div id="bossHud">
<div class="boss-name" id="bossName">BOSS</div>
<div class="bar">
<div class="fill boss-fill" id="bossBar"></div>
</div>
</div>

<button id="pauseButton">Ⅱ</button>

<div class="status">

<div class="status-row">
<div class="status-label">HULL</div>
<div class="bar">
<div class="fill hull-fill" id="hullBar"></div>
</div>
</div>

<div class="status-row">
<div class="status-label">SHIELD</div>
<div class="bar">
<div class="fill shield-fill" id="shieldBar"></div>
</div>
</div>

<div class="status-row">
<div class="status-label">ENERGY</div>
<div class="bar">
<div class="fill energy-fill" id="energyBar"></div>
</div>
</div>

</div>

<div id="weaponHud">
<div class="weapon-name" id="weaponName">PULSE LASER</div>
<div class="weapon-info" id="weaponInfo">1 / NORMAL</div>
<div id="abilityHud">Q — VOID OVERDRIVE</div>
</div>

</div>

<!-- MOBILE -->
<div id="mobileControls">

<div class="joystick" id="joystick">
<div class="stick" id="stick"></div>
</div>

<div class="actions">
<button id="boostButton">BOOST</button>
<button id="missileButton">MISSILE</button>
<button id="empButton">EMP</button>
<button class="fire" id="fireButton">FIRE</button>
</div>

</div>

<script>

/* =========================================================
   VOID SPACE
   COMPLETE FREE PROCEDURAL BROWSER GAME
========================================================= */

const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");

let W=innerWidth;
let H=innerHeight;
let DPR=Math.min(devicePixelRatio||1,2);

function resize(){
    W=innerWidth;
    H=innerHeight;

    canvas.width=W*DPR;
    canvas.height=H*DPR;

    canvas.style.width=W+"px";
    canvas.style.height=H+"px";

    ctx.setTransform(DPR,0,0,DPR,0,0);

    createStars();
}

addEventListener("resize",resize);

const keys={};

const mouse={
    x:W/2,
    y:H/2,
    down:false
};

let fireHeld=false;
let boostHeld=false;

const settings={
    sound:true,
    shake:true,
    mobile:true
};

let audio=null;

function audioInit(){
    if(!settings.sound)return;

    if(!audio){
        try{
            audio=new(
                window.AudioContext||
                window.webkitAudioContext
            )();
        }catch(e){}
    }

    if(audio&&audio.state==="suspended"){
        audio.resume();
    }
}

function beep(type){

    if(!settings.sound||!audio)return;

    const o=audio.createOscillator();
    const g=audio.createGain();

    o.connect(g);
    g.connect(audio.destination);

    const t=audio.currentTime;

    if(type==="laser"){
        o.type="sawtooth";
        o.frequency.setValueAtTime(700,t);
        o.frequency.exponentialRampToValueAtTime(150,t+.07);
        g.gain.setValueAtTime(.035,t);
        g.gain.exponentialRampToValueAtTime(.001,t+.07);
        o.start(t);
        o.stop(t+.07);
    }

    if(type==="plasma"){
        o.type="square";
        o.frequency.setValueAtTime(250,t);
        o.frequency.exponentialRampToValueAtTime(80,t+.14);
        g.gain.setValueAtTime(.04,t);
        g.gain.exponentialRampToValueAtTime(.001,t+.14);
        o.start(t);
        o.stop(t+.14);
    }

    if(type==="explosion"){
        o.type="triangle";
        o.frequency.setValueAtTime(100,t);
        o.frequency.exponentialRampToValueAtTime(35,t+.25);
        g.gain.setValueAtTime(.08,t);
        g.gain.exponentialRampToValueAtTime(.001,t+.25);
        o.start(t);
        o.stop(t+.25);
    }

    if(type==="power"){
        o.type="sine";
        o.frequency.setValueAtTime(250,t);
        o.frequency.exponentialRampToValueAtTime(900,t+.3);
        g.gain.setValueAtTime(.06,t);
        g.gain.exponentialRampToValueAtTime(.001,t+.3);
        o.start(t);
        o.stop(t+.3);
    }
}

addEventListener("keydown",e=>{

    keys[e.key.toLowerCase()]=true;

    if(
        [" ","arrowup","arrowdown",
         "arrowleft","arrowright"].includes(
            e.key.toLowerCase()
        )
    ){
        e.preventDefault();
    }

    if(e.key==="Escape"||e.key.toLowerCase()==="p"){
        if(game.running)togglePause();
    }

    if(game.running){

        if(e.key==="1")weapon=0;
        if(e.key==="2")weapon=1;
        if(e.key==="3")weapon=2;
        if(e.key==="4")weapon=3;
        if(e.key==="5")weapon=4;

        if(e.key.toLowerCase()==="q"){
            activateOverdrive();
        }
    }
});

addEventListener("keyup",e=>{
    keys[e.key.toLowerCase()]=false;
});

canvas.addEventListener("mousemove",e=>{
    mouse.x=e.clientX;
    mouse.y=e.clientY;
});

canvas.addEventListener("mousedown",e=>{
    if(e.button===0){
        mouse.down=true;
        audioInit();
    }
});

addEventListener("mouseup",e=>{
    if(e.button===0)mouse.down=false;
});

const player={
    x:0,
    y:0,
    vx:0,
    vy:0,
    angle:-Math.PI/2,

    baseHull:100,
    baseShield:100,
    baseEnergy:100,

    hull:100,
    shield:100,
    energy:100,

    cooldown:0,
    missileCooldown:0,
    empCooldown:0,

    rapid:0,
    invincible:0,
    overdrive:0
};

const upgrades={
    hull:0,
    shield:0,
    speed:0,
    damage:0,
    fireRate:0,
    energy:0
};

let credits=0;

const game={
    running:false,
    paused:false,

    score:0,
    wave:1,
    level:1,
    xp:0,

    kills:0,
    totalKills:0,

    spawnTimer:0,
    boss:null,

    shake:0,

    stars:[],
    enemies:[],
    bullets:[],
    enemyBullets:[],
    particles:[],
    powerups:[],
    pickups:[],

    missions:{
        firstBlood:false,
        survivor:false,
        hunter:false,
        heavy:false,
        boss:false,
        untouched:false,
        arsenal:false
    },

    lastTime:performance.now()
};

let weapon=0;

const weapons=[
    {
        name:"PULSE LASER",
        rate:.16,
        damage:25,
        speed:700,
        color:"#9beeff"
    },
    {
        name:"PLASMA CANNON",
        rate:.38,
        damage:65,
        speed:500,
        color:"#d68cff"
    },
    {
        name:"SPREAD CANNON",
        rate:.45,
        damage:28,
        speed:600,
        color:"#fff09a"
    },
    {
        name:"MISSILE LAUNCHER",
        rate:.7,
        damage:110,
        speed:300,
        color:"#ff9c74"
    },
    {
        name:"VOID BEAM",
        rate:.65,
        damage:150,
        speed:1000,
        color:"#ffffff"
    }
];

function maxHull(){
    return 100+upgrades.hull*25;
}

function maxShield(){
    return 100+upgrades.shield*25;
}

function maxEnergy(){
    return 100+upgrades.energy*25;
}

function speedBonus(){
    return 350+upgrades.speed*25;
}

function damageMultiplier(){
    return 1+upgrades.damage*.12;
}

function fireMultiplier(){
    return Math.max(.45,1-upgrades.fireRate*.06);
}

function screen(id,on){
    document.getElementById(id).classList.toggle("active",on);
}

function menu(){

    game.running=false;
    game.paused=false;

    screen("menu",true);
    screen("howScreen",false);
    screen("settingsScreen",false);
    screen("shipScreen",false);
    screen("shopScreen",false);
    screen("missionScreen",false);
    screen("pauseScreen",false);
    screen("gameOverScreen",false);

    document.getElementById("hud").classList.remove("active");
    document.getElementById("mobileControls").classList.remove("active");
}

document.getElementById("playBtn").onclick=()=>{
    audioInit();
    startGame();
};

document.getElementById("howBtn").onclick=()=>{
    screen("menu",false);
    screen("howScreen",true);
};

document.getElementById("settingsBtn").onclick=()=>{
    screen("menu",false);
    screen("settingsScreen",true);
};

document.getElementById("shipBtn").onclick=()=>{
    screen("menu",false);
    screen("shipScreen",true);
    updateShipScreen();
};

document.getElementById("shopBtn").onclick=()=>{
    screen("menu",false);
    screen("shopScreen",true);
    updateShop();
};

document.getElementById("missionBtn").onclick=()=>{
    screen("menu",false);
    screen("missionScreen",true);
    updateMissions();
};

document.getElementById("howBack").onclick=()=>{
    screen("howScreen",false);
    screen("menu",true);
};

document.getElementById("settingsBack").onclick=()=>{
    screen("settingsScreen",false);
    screen("menu",true);
};

document.getElementById("shipBack").onclick=()=>{
    screen("shipScreen",false);
    screen("menu",true);
};

document.getElementById("shopBack").onclick=()=>{
    screen("shopScreen",false);
    screen("menu",true);
};

document.getElementById("missionBack").onclick=()=>{
    screen("missionScreen",false);
    screen("menu",true);
};

document.getElementById("fullscreenBtn").onclick=()=>{
    if(!document.fullscreenElement)
        document.documentElement.requestFullscreen?.();
    else
        document.exitFullscreen?.();
};

document.getElementById("soundSetting").onclick=()=>{
    settings.sound=!settings.sound;

    document.getElementById("soundSetting").textContent=
        "SOUND: "+(settings.sound?"ON":"OFF");
};

document.getElementById("shakeSetting").onclick=()=>{
    settings.shake=!settings.shake;

    document.getElementById("shakeSetting").textContent=
        "SCREEN SHAKE: "+(settings.shake?"ON":"OFF");
};

document.getElementById("mobileSetting").onclick=()=>{
    settings.mobile=!settings.mobile;

    document.getElementById("mobileSetting").textContent=
        "MOBILE CONTROLS: "+(settings.mobile?"ON":"OFF");

    updateMobile();
};

document.getElementById("pauseButton").onclick=togglePause;
document.getElementById("resumeBtn").onclick=togglePause;

document.getElementById("restartBtn").onclick=()=>{
    startGame();
};

document.getElementById("exitBtn").onclick=menu;

document.getElementById("againBtn").onclick=()=>{
    startGame();
};

document.getElementById("gameOverExit").onclick=menu;

document.getElementById("selectShip").onclick=()=>{
    document.getElementById("selectShip").textContent=
        "VOID FALCON SELECTED";
};

function updateShipScreen(){

    document.getElementById("shipStats").innerHTML=`
        <p><strong>VOID FALCON</strong></p>
        <p>Balanced interceptor designed for deep-space combat.</p>

        <p>
        HULL: ${maxHull()}<br>
        SHIELD: ${maxShield()}<br>
        ENERGY: ${maxEnergy()}<br>
        SPEED: ${speedBonus()}<br>
        DAMAGE: x${damageMultiplier().toFixed(2)}
        </p>
    `;
}

function upgradeCost(type){

    const level=upgrades[type]||0;

    return 500+level*450;
}

function buyUpgrade(type){

    const cost=upgradeCost(type);

    if(credits<cost){
        beep("explosion");
        return;
    }

    credits-=cost;
    upgrades[type]++;

    updateShop();
    updateShipScreen();
}

function updateShop(){

    document.getElementById("creditsDisplay").textContent=
        "CREDITS: "+credits.toLocaleString();

    document.querySelectorAll(".shop-card button")
        .forEach(btn=>{
            btn.disabled=false;
        });
}

function updateMissions(){

    const m=game.missions;

    document.getElementById("missionsList").innerHTML=`

        <p>${m.firstBlood?"✓":"○"} FIRST BLOOD<br>
        Destroy your first enemy.</p>

        <p>${m.survivor?"✓":"○"} SURVIVOR<br>
        Reach Wave 10.</p>

        <p>${m.hunter?"✓":"○"} VOID HUNTER<br>
        Destroy 100 enemies.</p>

        <p>${m.heavy?"✓":"○"} HEAVY METAL<br>
        Destroy 25 heavy ships.</p>

        <p>${m.boss?"✓":"○"} BOSS SLAYER<br>
        Defeat a boss.</p>

        <p>${m.untouched?"✓":"○"} UNTOUCHABLE<br>
        Complete a wave without taking damage.</p>

        <p>${m.arsenal?"✓":"○"} ARSENAL<br>
        Use all five weapons.</p>
    `;
}

/* =========================================================
   STARS
========================================================= */

function createStars(){

    game.stars.length=0;

    const count=Math.min(
        500,
        Math.max(
            160,
            Math.floor(W*H/5500)
        )
    );

    for(let i=0;i<count;i++){

        game.stars.push({
            x:Math.random()*W,
            y:Math.random()*H,
            z:Math.random(),
            size:.4+Math.random()*2,
            speed:.5+Math.random()*1.5
        });
    }
}

createStars();

/* =========================================================
   START
========================================================= */

function startGame(){

    screen("menu",false);
    screen("howScreen",false);
    screen("settingsScreen",false);
    screen("shipScreen",false);
    screen("shopScreen",false);
    screen("missionScreen",false);
    screen("pauseScreen",false);
    screen("gameOverScreen",false);

    document.getElementById("hud").classList.add("active");

    game.running=true;
    game.paused=false;

    game.score=0;
    game.wave=1;
    game.level=1;
    game.xp=0;
    game.kills=0;

    game.spawnTimer=.4;
    game.boss=null;

    game.enemies.length=0;
    game.bullets.length=0;
    game.enemyBullets.length=0;
    game.particles.length=0;
    game.powerups.length=0;

    player.x=W/2;
    player.y=H*.72;
    player.vx=0;
    player.vy=0;

    player.hull=maxHull();
    player.shield=maxShield();
    player.energy=maxEnergy();

    player.cooldown=0;
    player.missileCooldown=0;
    player.empCooldown=0;

    player.rapid=0;
    player.invincible=1.5;
    player.overdrive=0;

    createStars();

    updateHUD();
    updateMobile();

    game.lastTime=performance.now();
}

function togglePause(){

    if(!game.running)return;

    game.paused=!game.paused;

    screen("pauseScreen",game.paused);

    if(!game.paused)
        game.lastTime=performance.now();

    updateMobile();
}

/* =========================================================
   ENEMIES
========================================================= */

function randomEnemyType(){

    const r=Math.random();

    if(game.wave<3){
        return r<.7?"fighter":"fast";
    }

    if(game.wave<6){
        if(r<.55)return"fighter";
        if(r<.75)return"fast";
        if(r<.9)return"heavy";
        return"sniper";
    }

    if(r<.35)return"fighter";
    if(r<.52)return"fast";
    if(r<.7)return"heavy";
    if(r<.83)return"sniper";
    if(r<.93)return"kamikaze";
    return"elite";
}

function spawnEnemy(){

    const type=randomEnemyType();

    const side=Math.floor(Math.random()*3);

    let x,y;

    if(side===0){
        x=Math.random()*W;
        y=-70;
    }else if(side===1){
        x=-70;
        y=Math.random()*H*.45;
    }else{
        x=W+70;
        y=Math.random()*H*.45;
    }

    let hp=25+game.wave*5;
    let speed=70+game.wave*3;
    let r=18;
    let damage=8;
    let reward=100;

    if(type==="fast"){
        hp=20+game.wave*4;
        speed=125+game.wave*4;
        r=15;
        damage=10;
        reward=130;
    }

    if(type==="heavy"){
        hp=100+game.wave*12;
        speed=40+game.wave*2;
        r=29;
        damage=25;
        reward=300;
    }

    if(type==="sniper"){
        hp=50+game.wave*6;
        speed=48;
        r=20;
        damage=18;
        reward=240;
    }

    if(type==="kamikaze"){
        hp=30+game.wave*4;
        speed=160+game.wave*5;
        r=17;
        damage=35;
        reward=180;
    }

    if(type==="elite"){
        hp=150+game.wave*16;
        speed=80+game.wave*3;
        r=25;
        damage=20;
        reward=500;
    }

    game.enemies.push({
        type,
        x,
        y,
        vx:0,
        vy:0,
        r,
        hp,
        maxHp:hp,
        speed,
        damage,
        reward,
        shoot:1+Math.random()*2,
        wobble:Math.random()*Math.PI*2,
        angle:0,
        shield:type==="elite"?50+game.wave*5:0,
        maxShield:type==="elite"?50+game.wave*5:0
    });
}

/* =========================================================
   BOSS
========================================================= */

function spawnBoss(){

    const names=[
        "DREADNAUGHT OMEGA",
        "VOID TITAN",
        "NEBULA REAPER",
        "BLACK STAR",
        "THE ABYSS"
    ];

    const hp=
        1200+
        game.wave*250;

    game.boss={
        name:names[(game.wave/5-1)%names.length|0],
        x:W/2,
        y:-150,
        vx:0,
        vy:60,
        r:75,
        hp,
        maxHp:hp,
        phase:1,
        shoot:1,
        special:5,
        alive:true
    };

    document.getElementById("bossHud").style.display="block";
    document.getElementById("bossName").textContent=
        game.boss.name;

    game.enemies.length=0;
}

function updateBoss(dt){

    const b=game.boss;

    if(!b)return;

    if(b.y<150){
        b.y+=b.vy*dt;
    }else{
        b.x+=Math.sin(performance.now()*.0007)*35*dt;
    }

    b.phase=
        b.hp<b.maxHp*.5?3:
        b.hp<b.maxHp*.75?2:1;

    b.shoot-=dt;
    b.special-=dt;

    if(b.shoot<=0){

        bossFire(b);

        b.shoot=
            b.phase===3?.45:
            b.phase===2?.75:
            1.05;
    }

    if(b.special<=0){

        bossSpecial(b);

        b.special=
            b.phase===3?3:
            5;
    }

    const dx=player.x-b.x;
    const dy=player.y-b.y;

    if(
        dx*dx+
        dy*dy<
        (player.radius+b.r)*
        (player.radius+b.r)
    ){
        damagePlayer(30);
    }
}

function bossFire(b){

    const count=
        b.phase===3?7:
        b.phase===2?5:
        3;

    const base=
        Math.atan2(
            player.y-b.y,
            player.x-b.x
        );

    for(let i=0;i<count;i++){

        const spread=
            (i-(count-1)/2)*.16;

        const a=base+spread;

        game.enemyBullets.push({
            x:b.x,
            y:b.y,
            vx:Math.cos(a)*(220+game.wave*6),
            vy:Math.sin(a)*(220+game.wave*6),
            life:6,
            damage:12+b.phase*4
        });
    }

    beep("plasma");
}

function bossSpecial(b){

    explosion(b.x,b.y,false);

    for(let i=0;i<20;i++){

        const a=Math.PI*2*i/20;

        game.enemyBullets.push({
            x:b.x,
            y:b.y,
            vx:Math.cos(a)*180,
            vy:Math.sin(a)*180,
            life:5,
            damage:10
        });
    }
}

function damageBoss(amount){

    if(!game.boss)return;

    game.boss.hp-=amount;

    if(game.boss.hp<=0){

        game.score+=10000*game.wave;
        credits+=5000;
        game.missions.boss=true;

        explosion(
            game.boss.x,
            game.boss.y,
            true
        );

        game.boss=null;

        document.getElementById("bossHud")
            .style.display="none";

        game.wave++;
        player.shield=maxShield();

        beep("explosion");
    }
}

/* =========================================================
   PLAYER FIRE
========================================================= */

function firePlayer(){

    if(player.cooldown>0)return;

    const w=weapons[weapon];

    let a=Math.atan2(
        mouse.y-player.y,
        mouse.x-player.x
    );

    const damage=
        w.damage*
        damageMultiplier()*
        (player.overdrive>0?2:1)*
        (player.rapid>0?1.5:1);

    if(weapon===2){

        for(let i=-1;i<=1;i++){

            const angle=a+i*.16;

            game.bullets.push({
                x:player.x+Math.cos(angle)*25,
                y:player.y+Math.sin(angle)*25,
                vx:Math.cos(angle)*w.speed,
                vy:Math.sin(angle)*w.speed,
                life:1.5,
                damage
            });
        }

    }else{

        game.bullets.push({
            x:player.x+Math.cos(a)*28,
            y:player.y+Math.sin(a)*28,
            vx:Math.cos(a)*w.speed,
            vy:Math.sin(a)*w.speed,
            life:1.8,
            damage,
            missile:weapon===3
        });
    }

    player.energy=Math.max(
        0,
        player.energy-
        (weapon===4?12:3)
    );

    player.cooldown=
        w.rate*
        fireMultiplier()*
        (player.rapid>0?.45:1);

    beep(
        weapon===1||
        weapon===4?
        "plasma":
        "laser"
    );
}

/* =========================================================
   SPECIAL
========================================================= */

function fireMissile(){

    if(player.missileCooldown>0)return;

    let target=null;
    let best=Infinity;

    for(const e of game.enemies){

        const d=
            (e.x-player.x)**2+
            (e.y-player.y)**2;

        if(d<best){
            best=d;
            target=e;
        }
    }

    if(game.boss){
        const d=
            (game.boss.x-player.x)**2+
            (game.boss.y-player.y)**2;

        if(d<best){
            target=game.boss;
        }
    }

    if(!target)return;

    const a=Math.atan2(
        target.y-player.y,
        target.x-player.x
    );

    game.bullets.push({
        x:player.x,
        y:player.y,
        vx:Math.cos(a)*280,
        vy:Math.sin(a)*280,
        life:5,
        damage:180*damageMultiplier(),
        missile:true,
        target
    });

    player.missileCooldown=3;
    beep("plasma");
}

function activateEMP(){

    if(player.empCooldown>0)return;

    for(const e of game.enemies){

        const d=Math.hypot(
            e.x-player.x,
            e.y-player.y
        );

        if(d<300){
            e.hp-=100;
        }
    }

    for(let i=0;i<50;i++){

        const a=Math.random()*Math.PI*2;
        const s=100+Math.random()*300;

        game.particles.push({
            x:player.x,
            y:player.y,
            vx:Math.cos(a)*s,
            vy:Math.sin(a)*s,
            life:.6,
            maxLife:.6,
            size:2+Math.random()*4,
            type:"laser"
        });
    }

    player.empCooldown=8;
}

function activateOverdrive(){

    if(player.energy<50)return;

    player.energy-=50;
    player.overdrive=8;

    beep("power");
}

/* =========================================================
   DAMAGE
========================================================= */

function damagePlayer(amount){

    if(player.invincible>0)return;

    let remaining=amount;

    if(player.shield>0){

        const absorbed=
            Math.min(
                player.shield,
                remaining
            );

        player.shield-=absorbed;
        remaining-=absorbed;
    }

    if(remaining>0){
        player.hull-=remaining;
    }

    player.invincible=.3;

    document.getElementById("damageFlash")
        .animate(
            [
                {opacity:.8},
                {opacity:0}
            ],
            {duration:220}
        );

    if(settings.shake)
        game.shake=Math.min(
            18,
            game.shake+8
        );

    if(player.hull<=0){
        player.hull=0;
        gameOver();
    }
}

/* =========================================================
   POWERUPS
========================================================= */

function spawnPowerup(x,y){

    if(Math.random()>.18)return;

    const types=[
        "shield",
        "rapid",
        "energy",
        "repair",
        "damage"
    ];

    game.powerups.push({
        x,
        y,
        type:types[
            Math.floor(Math.random()*types.length)
        ],
        life:12,
        pulse:0
    });
}

function collectPowerup(p){

    if(p.type==="shield")
        player.shield=Math.min(
            maxShield(),
            player.shield+50
        );

    if(p.type==="repair")
        player.hull=Math.min(
            maxHull(),
            player.hull+35
        );

    if(p.type==="energy")
        player.energy=Math.min(
            maxEnergy(),
            player.energy+60
        );

    if(p.type==="rapid")
        player.rapid=8;

    if(p.type==="damage")
        player.overdrive=6;

    beep("power");
}

/* =========================================================
   MOVEMENT
========================================================= */

const joystick={
    active:false,
    id:null,
    x:0,
    y:0
};

function updatePlayer(dt){

    let ix=0;
    let iy=0;

    if(keys.w||keys.arrowup)iy--;
    if(keys.s||keys.arrowdown)iy++;
    if(keys.a||keys.arrowleft)ix--;
    if(keys.d||keys.arrowright)ix++;

    if(joystick.active){
        ix=joystick.x;
        iy=joystick.y;
    }

    const len=Math.hypot(ix,iy);

    if(len>1){
        ix/=len;
        iy/=len;
    }

    const boosting=
        keys.shift||
        boostHeld;

    const acceleration=
        boosting?1100:750;

    const max=
        boosting?
        speedBonus()*1.45:
        speedBonus();

    player.vx+=ix*acceleration*dt;
    player.vy+=iy*acceleration*dt;

    player.vx*=Math.pow(.001,dt);
    player.vy*=Math.pow(.001,dt);

    const v=Math.hypot(
        player.vx,
        player.vy
    );

    if(v>max){

        player.vx=
            player.vx/v*max;

        player.vy=
            player.vy/v*max;
    }

    player.x+=player.vx*dt;
    player.y+=player.vy*dt;

    player.x=Math.max(
        25,
        Math.min(W-25,player.x)
    );

    player.y=Math.max(
        25,
        Math.min(H-25,player.y)
    );

    player.angle=Math.atan2(
        mouse.y-player.y,
        mouse.x-player.x
    );

    if(player.cooldown>0)
        player.cooldown-=dt;

    if(player.missileCooldown>0)
        player.missileCooldown-=dt;

    if(player.empCooldown>0)
        player.empCooldown-=dt;

    if(player.rapid>0)
        player.rapid-=dt;

    if(player.overdrive>0)
        player.overdrive-=dt;

    if(player.invincible>0)
        player.invincible-=dt;

    const firing=
        mouse.down||
        keys[" "]||
        fireHeld;

    if(firing&&player.energy>0)
        firePlayer();

    if(keys.q)
        keys.q=false;

    player.energy=Math.min(
        maxEnergy(),
        player.energy+dt*8
    );

    if(player.shield<maxShield()){
        player.shield=Math.min(
            maxShield(),
            player.shield+dt*2.5
        );
    }
}

/* =========================================================
   ENEMIES UPDATE
========================================================= */

function updateEnemies(dt){

    if(!game.boss){

        game.spawnTimer-=dt;

        const desired=
            Math.min(
                5+game.wave*1.3,
                24
            );

        if(
            game.spawnTimer<=0&&
            game.enemies.length<desired
        ){

            spawnEnemy();

            game.spawnTimer=
                Math.max(
                    .25,
                    1.15-game.wave*.025
                );
        }
    }

    for(
        let i=game.enemies.length-1;
        i>=0;
        i--
    ){

        const e=game.enemies[i];

        const dx=player.x-e.x;
        const dy=player.y-e.y;

        const d=Math.max(
            1,
            Math.hypot(dx,dy)
        );

        const nx=dx/d;
        const ny=dy/d;

        e.wobble+=dt*(
            e.type==="heavy"?1:
            e.type==="fast"?3:
            2
        );

        let force=20;

        if(e.type==="sniper"){
            force=35;
        }

        if(e.type==="kamikaze"){
            force=5;
        }

        const side=
            Math.sin(e.wobble)*force;

        let desiredX=nx*e.speed;
        let desiredY=ny*e.speed;

        if(e.type==="sniper"&&d<350){
            desiredX=-nx*e.speed;
            desiredY=-ny*e.speed;
        }

        e.vx+=(desiredX-ny*side-e.vx)*dt*1.7;
        e.vy+=(desiredY+nx*side-e.vy)*dt*1.7;

        e.x+=e.vx*dt;
        e.y+=e.vy*dt;

        e.angle=Math.atan2(
            e.vy,
            e.vx
        );

        e.shoot-=dt;

        if(
            e.shoot<=0&&
            d<650&&
            e.type!=="kamikaze"
        ){

            enemyFire(e);

            e.shoot=
                e.type==="sniper"?
                2.8:
                e.type==="heavy"?
                1.8:
                2.2;
        }

        if(
            d<
            e.r+player.radius
        ){

            damagePlayer(e.damage);

            explosion(
                e.x,
                e.y,
                e.type==="heavy"||
                e.type==="elite"
            );

            game.enemies.splice(i,1);
        }
    }
}

function enemyFire(e){

    const a=Math.atan2(
        player.y-e.y,
        player.x-e.x
    );

    let speed=230+game.wave*5;

    if(e.type==="sniper")
        speed=420+game.wave*6;

    game.enemyBullets.push({
        x:e.x,
        y:e.y,
        vx:Math.cos(a)*speed,
        vy:Math.sin(a)*speed,
        life:6,
        damage:e.type==="sniper"?22:8
    });

    beep("plasma");
}

/* =========================================================
   BULLETS
========================================================= */

function updateBullets(dt){

    for(
        let i=game.bullets.length-1;
        i>=0;
        i--
    ){

        const b=game.bullets[i];

        if(b.missile&&b.target){

            const t=b.target;

            if(t){

                const desired=Math.atan2(
                    t.y-b.y,
                    t.x-b.x
                );

                const current=Math.atan2(
                    b.vy,
                    b.vx
                );

                let diff=
                    desired-current;

                while(diff>Math.PI)
                    diff-=Math.PI*2;

                while(diff<-Math.PI)
                    diff+=Math.PI*2;

                const turn=
                    Math.min(
                        Math.abs(diff),
                        2.2*dt
                    );

                const angle=
                    current+
                    Math.sign(diff)*turn;

                const speed=Math.hypot(
                    b.vx,
                    b.vy
                );

                b.vx=Math.cos(angle)*speed;
                b.vy=Math.sin(angle)*speed;
            }
        }

        b.x+=b.vx*dt;
        b.y+=b.vy*dt;

        b.life-=dt;

        let hit=false;

        if(game.boss){

            const dx=b.x-game.boss.x;
            const dy=b.y-game.boss.y;

            if(
                dx*dx+
                dy*dy<
                (game.boss.r+8)*
                (game.boss.r+8)
            ){

                damageBoss(b.damage);

                game.bullets.splice(i,1);
                continue;
            }
        }

        for(
            let j=game.enemies.length-1;
            j>=0;
            j--
        ){

            const e=game.enemies[j];

            const dx=b.x-e.x;
            const dy=b.y-e.y;

            if(
                dx*dx+
                dy*dy<
                (e.r+7)*
                (e.r+7)
            ){

                let damage=b.damage;

                if(e.shield>0){

                    const absorb=
                        Math.min(
                            e.shield,
                            damage
                        );

                    e.shield-=absorb;
                    damage-=absorb;
                }

                e.hp-=damage;

                hit=true;

                for(let p=0;p<5;p++){

                    game.particles.push({
                        x:b.x,
                        y:b.y,
                        vx:(Math.random()-.5)*130,
                        vy:(Math.random()-.5)*130,
                        life:.2,
                        maxLife:.2,
                        size:2,
                        type:"laser"
                    });
                }

                if(e.hp<=0){

                    game.score+=
                        e.reward*
                        Math.max(1,game.wave);

                    credits+=
                        Math.floor(
                            e.reward/10
                        );

                    game.kills++;
                    game.totalKills++;

                    game.missions.firstBlood=true;

                    if(e.type==="heavy")
                        game.missions.heavy=
                            true;

                    explosion(
                        e.x,
                        e.y,
                        e.type==="heavy"||
                        e.type==="elite"
                    );

                    spawnPowerup(
                        e.x,
                        e.y
                    );

                    game.enemies.splice(j,1);
                }

                break;
            }
        }

        if(
            !hit&&
            (
                b.life<=0||
                b.x<-80||
                b.x>W+80||
                b.y<-80||
                b.y>H+80
            )
        ){
            game.bullets.splice(i,1);
        }
    }
}

/* =========================================================
   ENEMY BULLETS
========================================================= */

function updateEnemyBullets(dt){

    for(
        let i=game.enemyBullets.length-1;
        i>=0;
        i--
    ){

        const b=game.enemyBullets[i];

        b.x+=b.vx*dt;
        b.y+=b.vy*dt;

        b.life-=dt;

        const dx=b.x-player.x;
        const dy=b.y-player.y;

        if(
            dx*dx+
            dy*dy<
            (player.radius+8)*
            (player.radius+8)
        ){

            damagePlayer(b.damage);

            game.enemyBullets.splice(i,1);
            continue;
        }

        if(
            b.life<=0||
            b.x<-50||
            b.x>W+50||
            b.y<-50||
            b.y>H+50
        ){
            game.enemyBullets.splice(i,1);
        }
    }
}

/* =========================================================
   PARTICLES
========================================================= */

function explosion(x,y,heavy=false){

    const count=heavy?60:25;

    for(let i=0;i<count;i++){

        const a=Math.random()*Math.PI*2;
        const s=
            Math.random()*
            (heavy?260:150);

        game.particles.push({
            x,
            y,
            vx:Math.cos(a)*s,
            vy:Math.sin(a)*s,
            life:.3+Math.random()*.8,
            maxLife:1,
            size:1.5+
                Math.random()*
                (heavy?6:3),
            type:"explosion"
        });
    }

    if(settings.shake){
        game.shake=Math.min(
            20,
            game.shake+(heavy?13:5)
        );
    }

    beep("explosion");
}

function updateParticles(dt){

    for(
        let i=game.particles.length-1;
        i>=0;
        i--
    ){

        const p=game.particles[i];

        p.x+=p.vx*dt;
        p.y+=p.vy*dt;

        p.vx*=Math.pow(.08,dt);
        p.vy*=Math.pow(.08,dt);

        p.life-=dt;

        if(p.life<=0)
            game.particles.splice(i,1);
    }
}

/* =========================================================
   POWERUPS UPDATE
========================================================= */

function updatePowerups(dt){

    for(
        let i=game.powerups.length-1;
        i>=0;
        i--
    ){

        const p=game.powerups[i];

        p.y+=20*dt;
        p.life-=dt;
        p.pulse+=dt*5;

        const dx=p.x-player.x;
        const dy=p.y-player.y;

        if(
            dx*dx+
            dy*dy<
            35*35
        ){

            collectPowerup(p);

            game.powerups.splice(i,1);
            continue;
        }

        if(p.life<=0)
            game.powerups.splice(i,1);
    }
}

/* =========================================================
   WAVES / LEVEL
========================================================= */

function updateProgress(){

    const required=
        game.level*800;

    while(game.score>=required&&
          game.level<99){

        game.level++;
        player.hull=maxHull();
        player.shield=maxShield();
        player.energy=maxEnergy();
    }

    const newWave=
        1+
        Math.floor(
            game.kills/8
        );

    if(newWave>game.wave){

        if(!game.boss&&
           game.wave%5===0){

            spawnBoss();
        }

        game.wave=newWave;

        player.shield=Math.min(
            maxShield(),
            player.shield+30
        );
    }

    if(game.wave>=10)
        game.missions.survivor=true;

    if(game.totalKills>=100)
        game.missions.hunter=true;
}

/* =========================================================
   STARS
========================================================= */

function updateStars(dt){

    for(const s of game.stars){

        s.y+=
            (25+s.z*200)*
            dt;

        if(s.y>H+5){

            s.y=-5;
            s.x=Math.random()*W;
        }
    }
}

/* =========================================================
   HUD
========================================================= */

function updateHUD(){

    document.getElementById("score").textContent=
        Math.floor(game.score).toLocaleString();

    document.getElementById("wave").textContent=
        game.wave;

    document.getElementById("level").textContent=
        game.level;

    document.getElementById("credits").textContent=
        credits.toLocaleString();

    document.getElementById("hullBar").style.width=
        Math.max(
            0,
            player.hull/maxHull()*100
        )+"%";

    document.getElementById("shieldBar").style.width=
        Math.max(
            0,
            player.shield/maxShield()*100
        )+"%";

    document.getElementById("energyBar").style.width=
        Math.max(
            0,
            player.energy/maxEnergy()*100
        )+"%";

    document.getElementById("weaponName").textContent=
        weapons[weapon].name;

    document.getElementById("weaponInfo").textContent=
        (weapon+1)+
        " / DAMAGE "+
        Math.floor(
            weapons[weapon].damage*
            damageMultiplier()
        );

    document.getElementById("abilityHud").textContent=
        "Q — OVERDRIVE | "+
        "MISSILE "+
        Math.max(0,player.missileCooldown).toFixed(1)+
        " | EMP "+
        Math.max(0,player.empCooldown).toFixed(1);

    document.getElementById("enemies")?.remove;

    if(game.boss){

        document.getElementById("bossBar")
            .style.width=
            Math.max(
                0,
                game.boss.hp/
                game.boss.maxHp*
                100
            )+"%";
    }
}

/* =========================================================
   DRAW BACKGROUND
========================================================= */

function drawBackground(){

    const g=
        ctx.createRadialGradient(
            W/2,
            H/2,
            0,
            W/2,
            H/2,
            Math.max(W,H)*.8
        );

    g.addColorStop(0,"#0a1d38");
    g.addColorStop(.5,"#030b1a");
    g.addColorStop(1,"#01030a");

    ctx.fillStyle=g;
    ctx.fillRect(0,0,W,H);

    for(const s of game.stars){

        ctx.globalAlpha=
            .2+s.z*.8;

        ctx.fillStyle="#c8efff";

        const size=
            s.size*
            (.5+s.z*1.7);

        ctx.fillRect(
            s.x,
            s.y,
            size,
            size
        );
    }

    ctx.globalAlpha=1;

    /* space lanes */

    ctx.strokeStyle=
        "rgba(30,130,190,.045)";

    for(
        let x=-W;
        x<W*2;
        x+=100
    ){

        ctx.beginPath();

        ctx.moveTo(
            W/2+(x-W/2)*.1,
            0
        );

        ctx.lineTo(
            x,
            H
        );

        ctx.stroke();
    }
}

/* =========================================================
   DRAW PLAYER
========================================================= */

function drawPlayer(){

    ctx.save();

    ctx.translate(
        player.x,
        player.y
    );

    ctx.rotate(
        player.angle+Math.PI/2
    );

    if(player.invincible>0){
        ctx.globalAlpha=
            .55+
            Math.sin(performance.now()*.03)*.3;
    }

    /* engine */

    const flame=
        ctx.createRadialGradient(
            0,
            28,
            1,
            0,
            28,
            30
        );

    flame.addColorStop(
        0,
        "rgba(150,245,255,.9)"
    );

    flame.addColorStop(
        1,
        "rgba(0,140,255,0)"
    );

    ctx.fillStyle=flame;

    ctx.beginPath();
    ctx.arc(0,28,30,0,Math.PI*2);
    ctx.fill();

    /* boost flame */

    if(
        keys.shift||
        boostHeld
    ){

        ctx.fillStyle="#bdf8ff";

        ctx.beginPath();

        ctx.moveTo(-6,20);
        ctx.lineTo(0,48+Math.random()*15);
        ctx.lineTo(6,20);

        ctx.closePath();
        ctx.fill();
    }

    /* body */

    ctx.beginPath();

    ctx.moveTo(0,-32);
    ctx.lineTo(17,15);
    ctx.lineTo(8,12);
    ctx.lineTo(0,27);
    ctx.lineTo(-8,12);
    ctx.lineTo(-17,15);

    ctx.closePath();

    const body=
        ctx.createLinearGradient(
            -18,-30,
            18,30
        );

    body.addColorStop(0,"#f3ffff");
    body.addColorStop(.45,"#52d5ff");
    body.addColorStop(1,"#07547e");

    ctx.fillStyle=body;
    ctx.fill();

    ctx.strokeStyle="#baf5ff";
    ctx.lineWidth=1.5;
    ctx.stroke();

    /* wings */

    ctx.beginPath();

    ctx.moveTo(-10,2);
    ctx.lineTo(-34,19);
    ctx.lineTo(-10,15);

    ctx.closePath();

    ctx.fillStyle="#126a98";
    ctx.fill();

    ctx.beginPath();

    ctx.moveTo(10,2);
    ctx.lineTo(34,19);
    ctx.lineTo(10,15);

    ctx.closePath();

    ctx.fill();

    /* cockpit */

    ctx.beginPath();

    ctx.ellipse(
        0,
        -9,
        5,
        10,
        0,
        0,
        Math.PI*2
    );

    ctx.fillStyle="#061d35";
    ctx.fill();

    ctx.strokeStyle="#85eeff";
    ctx.stroke();

    /* shield */

    if(player.shield>0){

        ctx.strokeStyle=
            "rgba(100,150,255,.2)";

        ctx.lineWidth=2;

        ctx.beginPath();

        ctx.arc(
            0,
            0,
            34+
            Math.sin(
                performance.now()*.005
            )*2,
            0,
            Math.PI*2
        );

        ctx.stroke();
    }

    ctx.restore();
}

/* =========================================================
   DRAW ENEMY
========================================================= */

function drawEnemy(e){

    ctx.save();

    ctx.translate(
        e.x,
        e.y
    );

    ctx.rotate(
        e.angle+Math.PI/2
    );

    let color="#e74373";

    if(e.type==="heavy")
        color="#ff627d";

    if(e.type==="fast")
        color="#ff8b51";

    if(e.type==="sniper")
        color="#b879ff";

    if(e.type==="kamikaze")
        color="#ffb33e";

    if(e.type==="elite")
        color="#ff315b";

    /* glow */

    const glow=
        ctx.createRadialGradient(
            0,0,
            2,
            0,0,
            e.r*2
        );

    glow.addColorStop(
        0,
        color+"55"
    );

    glow.addColorStop(
        1,
        "rgba(255,0,80,0)"
    );

    ctx.fillStyle=glow;

    ctx.beginPath();
    ctx.arc(0,0,e.r*2,0,Math.PI*2);
    ctx.fill();

    if(e.type==="heavy"||
       e.type==="elite"){

        ctx.beginPath();

        ctx.moveTo(0,-32);
        ctx.lineTo(28,7);
        ctx.lineTo(20,28);
        ctx.lineTo(0,20);
        ctx.lineTo(-20,28);
        ctx.lineTo(-28,7);

        ctx.closePath();

        ctx.fillStyle=
            e.type==="elite"?
            "#471126":
            "#35132a";

        ctx.fill();

        ctx.strokeStyle=color;
        ctx.lineWidth=2;
        ctx.stroke();

    }else{

        ctx.beginPath();

        ctx.moveTo(0,-24);
        ctx.lineTo(16,17);
        ctx.lineTo(0,10);
        ctx.lineTo(-16,17);

        ctx.closePath();

        ctx.fillStyle="#3d1024";
        ctx.fill();

        ctx.strokeStyle=color;
        ctx.lineWidth=1.5;
        ctx.stroke();
    }

    ctx.fillStyle=color;

    ctx.beginPath();
    ctx.arc(0,-5,5,0,Math.PI*2);
    ctx.fill();

    ctx.restore();

    /* shield */

    if(e.maxShield>0&&e.shield>0){

        ctx.strokeStyle=
            "rgba(110,130,255,.7)";

        ctx.beginPath();

        ctx.arc(
            e.x,
            e.y,
            e.r+4,
            0,
            Math.PI*2
        );

        ctx.stroke();
    }

    /* health */

    const bw=e.r*2.2;

    ctx.fillStyle="rgba(0,0,0,.6)";

    ctx.fillRect(
        e.x-bw/2,
        e.y-e.r-9,
        bw,
        3
    );

    ctx.fillStyle=color;

    ctx.fillRect(
        e.x-bw/2,
        e.y-e.r-9,
        bw*
        Math.max(
            0,
            e.hp/e.maxHp
        ),
        3
    );
}

/* =========================================================
   DRAW BOSS
========================================================= */

function drawBoss(){

    const b=game.boss;

    if(!b)return;

    ctx.save();

    ctx.translate(
        b.x,
        b.y
    );

    ctx.rotate(
        Math.sin(performance.now()*.001)*.04
    );

    const glow=
        ctx.createRadialGradient(
            0,0,
            5,
            0,0,
            b.r*2
        );

    glow.addColorStop(
        0,
        "rgba(255,40,90,.4)"
    );

    glow.addColorStop(
        1,
        "rgba(255,0,50,0)"
    );

    ctx.fillStyle=glow;

    ctx.beginPath();
    ctx.arc(
        0,0,
        b.r*2,
        0,
        Math.PI*2
    );

    ctx.fill();

    ctx.beginPath();

    ctx.moveTo(0,-85);
    ctx.lineTo(65,-20);
    ctx.lineTo(85,35);
    ctx.lineTo(40,65);
    ctx.lineTo(0,48);
    ctx.lineTo(-40,65);
    ctx.lineTo(-85,35);
    ctx.lineTo(-65,-20);

    ctx.closePath();

    const body=
        ctx.createLinearGradient(
            -80,-80,
            80,80
        );

    body.addColorStop(0,"#63203c");
    body.addColorStop(.5,"#260b1c");
    body.addColorStop(1,"#09040c");

    ctx.fillStyle=body;
    ctx.fill();

    ctx.strokeStyle=
        b.phase===3?
        "#ff315d":
        "#ff6b88";

    ctx.lineWidth=3;
    ctx.stroke();

    /* reactor */

    ctx.fillStyle=
        b.phase===3?
        "#ffffff":
        "#ff718a";

    ctx.shadowBlur=25;
    ctx.shadowColor="#ff315d";

    ctx.beginPath();

    ctx.arc(
        0,
        5,
        15+
        Math.sin(performance.now()*.008)*3,
        0,
        Math.PI*2
    );

    ctx.fill();

    ctx.restore();
}

/* =========================================================
   DRAW BULLETS
========================================================= */

function drawBullets(){

    for(const b of game.bullets){

        const a=Math.atan2(
            b.vy,
            b.vx
        );

        ctx.save();

        ctx.translate(
            b.x,
            b.y
        );

        ctx.rotate(a);

        ctx.shadowBlur=
            b.missile?18:14;

        ctx.shadowColor=
            b.missile?
            "#ff7a4d":
            weapons[weapon].color;

        ctx.fillStyle=
            b.missile?
            "#ffd1a8":
            weapons[weapon].color;

        ctx.fillRect(
            -b.missile?11:10,
            -2,
            b.missile?22:20,
            4
        );

        ctx.restore();
    }

    for(const b of game.enemyBullets){

        const a=Math.atan2(
            b.vy,
            b.vx
        );

        ctx.save();

        ctx.translate(
            b.x,
            b.y
        );

        ctx.rotate(a);

        ctx.shadowBlur=12;
        ctx.shadowColor="#ff4265";

        ctx.fillStyle="#ffb4c0";

        ctx.fillRect(
            -8,
            -2,
            16,
            4
        );

        ctx.restore();
    }
}

/* =========================================================
   PARTICLES
========================================================= */

function drawParticles(){

    for(const p of game.particles){

        ctx.globalAlpha=
            Math.max(
                0,
                p.life/p.maxLife
            );

        ctx.fillStyle=
            p.type==="laser"?
            "#9feeff":
            "#ff9d64";

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

    ctx.globalAlpha=1;
}

/* =========================================================
   POWERUPS
========================================================= */

function drawPowerups(){

    for(const p of game.powerups){

        const pulse=
            Math.sin(p.pulse)*3;

        let color="#5ce8ff";
        let letter="S";

        if(p.type==="rapid"){
            color="#48f4ff";
            letter="R";
        }

        if(p.type==="energy"){
            color="#d66bff";
            letter="E";
        }

        if(p.type==="repair"){
            color="#7cff9a";
            letter="+";
        }

        if(p.type==="damage"){
            color="#ffbd55";
            letter="D";
        }

        ctx.save();

        ctx.translate(
            p.x,
            p.y
        );

        ctx.shadowBlur=20;
        ctx.shadowColor=color;

        ctx.strokeStyle=color;
        ctx.lineWidth=3;

        ctx.beginPath();

        ctx.arc(
            0,
            0,
            14+pulse,
            0,
            Math.PI*2
        );

        ctx.stroke();

        ctx.fillStyle=color;

        ctx.font="bold 11px Arial";
        ctx.textAlign="center";
        ctx.textBaseline="middle";

        ctx.fillText(
            letter,
            0,
            0
        );

        ctx.restore();
    }
}

/* =========================================================
   CROSSHAIR
========================================================= */

function drawCrosshair(){

    if(
        "ontouchstart"in window||
        navigator.maxTouchPoints>0
    )return;

    ctx.save();

    ctx.translate(
        mouse.x,
        mouse.y
    );

    ctx.strokeStyle=
        "rgba(140,235,255,.65)";

    ctx.lineWidth=1;

    ctx.beginPath();

    ctx.arc(
        0,
        0,
        10,
        0,
        Math.PI*2
    );

    ctx.stroke();

    ctx.beginPath();

    ctx.moveTo(-18,0);
    ctx.lineTo(-5,0);

    ctx.moveTo(5,0);
    ctx.lineTo(18,0);

    ctx.moveTo(0,-18);
    ctx.lineTo(0,-5);

    ctx.moveTo(0,5);
    ctx.lineTo(0,18);

    ctx.stroke();

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

    let sx=0;
    let sy=0;

    if(
        settings.shake&&
        game.shake>0
    ){

        sx=
            (Math.random()-.5)*
            game.shake;

        sy=
            (Math.random()-.5)*
            game.shake;
    }

    ctx.save();

    ctx.translate(
        sx,
        sy
    );

    drawBackground();
    drawPowerups();
    drawBullets();

    for(const e of game.enemies)
        drawEnemy(e);

    drawBoss();
    drawPlayer();
    drawParticles();
    drawCrosshair();

    ctx.restore();

    if(game.shake>0){

        game.shake*=.9;

        if(game.shake<.1)
            game.shake=0;
    }
}

/* =========================================================
   GAME OVER
========================================================= */

function gameOver(){

    game.running=false;
    game.paused=false;

    document.getElementById("finalScore").textContent=
        Math.floor(game.score).toLocaleString();

    document.getElementById("finalStats").textContent=
        "WAVE "+
        game.wave+
        " • LEVEL "+
        game.level+
        " • HOSTILES "+
        game.kills+
        " • CREDITS "+
        credits;

    document.getElementById("hud")
        .classList.remove("active");

    document.getElementById("mobileControls")
        .classList.remove("active");

    screen("gameOverScreen",true);

    explosion(
        player.x,
        player.y,
        true
    );
}

/* =========================================================
   MOBILE
========================================================= */

function updateMobile(){

    const touch=
        "ontouchstart"in window||
        navigator.maxTouchPoints>0;

    document.getElementById(
        "mobileControls"
    ).classList.toggle(
        "active",
        settings.mobile&&
        touch&&
        game.running&&
        !game.paused
    );
}

const fireButton=
    document.getElementById("fireButton");

fireButton.addEventListener(
    "pointerdown",
    e=>{
        e.preventDefault();
        fireHeld=true;
        audioInit();
    }
);

fireButton.addEventListener(
    "pointerup",
    ()=>{
        fireHeld=false;
    }
);

fireButton.addEventListener(
    "pointercancel",
    ()=>{
        fireHeld=false;
    }
);

fireButton.addEventListener(
    "pointerleave",
    ()=>{
        fireHeld=false;
    }
);

const boostButton=
    document.getElementById("boostButton");

boostButton.addEventListener(
    "pointerdown",
    e=>{
        e.preventDefault();
        boostHeld=true;
    }
);

boostButton.addEventListener(
    "pointerup",
    ()=>{
        boostHeld=false;
    }
);

boostButton.addEventListener(
    "pointercancel",
    ()=>{
        boostHeld=false;
    }
);

document.getElementById("missileButton")
    .addEventListener(
        "pointerdown",
        e=>{
            e.preventDefault();
            fireMissile();
            audioInit();
        }
    );

document.getElementById("empButton")
    .addEventListener(
        "pointerdown",
        e=>{
            e.preventDefault();
            activateEMP();
        }
    );

/* joystick */

const joystickElement=
    document.getElementById("joystick");

const stickElement=
    document.getElementById("stick");

function joystickMove(x,y){

    const r=
        joystickElement
        .getBoundingClientRect();

    const cx=
        r.left+r.width/2;

    const cy=
        r.top+r.height/2;

    let dx=x-cx;
    let dy=y-cy;

    const max=r.width*.32;

    const d=Math.hypot(
        dx,
        dy
    );

    if(d>max){

        dx=dx/d*max;
        dy=dy/d*max;
    }

    joystick.x=dx/max;
    joystick.y=dy/max;

    stickElement.style.transform=
        `translate(${dx}px,${dy}px)`;
}

joystickElement.addEventListener(
    "pointerdown",
    e=>{

        e.preventDefault();

        joystick.active=true;
        joystick.id=e.pointerId;

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
    e=>{

        if(
            joystick.active&&
            e.pointerId===joystick.id
        ){

            joystickMove(
                e.clientX,
                e.clientY
            );
        }
    }
);

function joystickEnd(e){

    if(e.pointerId!==joystick.id)
        return;

    joystick.active=false;
    joystick.id=null;

    joystick.x=0;
    joystick.y=0;

    stickElement.style.transform=
        "translate(0,0)";
}

joystickElement.addEventListener(
    "pointerup",
    joystickEnd
);

joystickElement.addEventListener(
    "pointercancel",
    joystickEnd
);

/* =========================================================
   UPDATE
========================================================= */

function update(dt){

    if(!game.running||game.paused)
        return;

    dt=Math.min(dt,.033);

    updateStars(dt);
    updatePlayer(dt);
    updateEnemies(dt);
    updateBoss(dt);
    updateBullets(dt);
    updateEnemyBullets(dt);
    updateParticles(dt);
    updatePowerups(dt);
    updateProgress();

    updateHUD();
}

/* =========================================================
   LOOP
========================================================= */

function loop(now){

    let dt=
        (now-game.lastTime)/
        1000;

    game.lastTime=now;

    update(dt);
    draw();

    requestAnimationFrame(loop);
}

game.lastTime=performance.now();

requestAnimationFrame(loop);

/* =========================================================
   WINDOW BLUR
========================================================= */

addEventListener("blur",()=>{

    mouse.down=false;
    fireHeld=false;
    boostHeld=false;

    if(game.running&&!game.paused)
        togglePause();
});

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
