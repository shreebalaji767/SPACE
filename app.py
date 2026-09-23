from flask import Flask, render_template_string, jsonify, request
import os
import math
import random
import hashlib
import json

app = Flask(__name__)

# ============================================================
# VOID SPACE
# Minecraft-like procedural space universe
# ============================================================

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

canvas{
    position:fixed;
    inset:0;
    width:100%;
    height:100%;
    display:block;
    background:#02030a;
}

#ui{
    position:fixed;
    inset:0;
    pointer-events:none;
}

.screen{
    position:absolute;
    inset:0;
    display:flex;
    align-items:center;
    justify-content:center;
    pointer-events:auto;
    background:
        radial-gradient(circle at center,
        rgba(30,40,90,.15),
        rgba(0,0,0,.82));
}

.hidden{
    display:none!important;
}

.panel{
    width:min(900px,92vw);
    max-height:90vh;
    overflow:auto;
    padding:30px;
    border:1px solid rgba(130,170,255,.3);
    background:rgba(5,8,20,.9);
    box-shadow:
        0 0 60px rgba(50,100,255,.15),
        inset 0 0 30px rgba(255,255,255,.02);
    backdrop-filter:blur(12px);
    border-radius:18px;
}

.logo{
    font-size:clamp(42px,9vw,100px);
    font-weight:900;
    letter-spacing:.18em;
    text-align:center;
    text-shadow:
        0 0 10px #fff,
        0 0 30px #5c8dff,
        0 0 70px #315cff;
}

.subtitle{
    text-align:center;
    color:#8ea7d8;
    letter-spacing:.3em;
    margin:10px 0 35px;
}

button{
    appearance:none;
    border:1px solid rgba(120,160,255,.4);
    background:rgba(20,30,65,.8);
    color:#fff;
    padding:14px 20px;
    border-radius:10px;
    cursor:pointer;
    font-size:15px;
    transition:.15s;
}

button:hover{
    background:rgba(50,75,145,.8);
    border-color:#8bb1ff;
    transform:translateY(-1px);
}

.menu-buttons{
    display:grid;
    gap:12px;
    width:min(360px,100%);
    margin:auto;
}

h1,h2,h3{
    margin-bottom:15px;
}

p{
    line-height:1.6;
    color:#b9c4df;
}

#hud{
    position:absolute;
    inset:0;
    pointer-events:none;
}

.topbar{
    position:absolute;
    top:15px;
    left:15px;
    right:15px;
    display:flex;
    justify-content:space-between;
    gap:15px;
}

.hudbox{
    min-width:150px;
    padding:12px 15px;
    border:1px solid rgba(120,160,255,.2);
    border-radius:12px;
    background:rgba(2,5,15,.62);
    backdrop-filter:blur(8px);
}

.hud-title{
    color:#6e91d8;
    font-size:10px;
    letter-spacing:.15em;
    margin-bottom:4px;
}

.hud-value{
    font-weight:bold;
}

.bars{
    display:grid;
    gap:6px;
}

.bar{
    width:220px;
    max-width:35vw;
    height:8px;
    background:#121827;
    border-radius:10px;
    overflow:hidden;
}

.bar > div{
    height:100%;
    width:100%;
    transition:.15s;
}

#hullBar{
    background:#d84a55;
}

#shieldBar{
    background:#5e9eff;
}

#xpBar{
    background:#bd70ff;
}

.bottomHud{
    position:absolute;
    bottom:18px;
    left:18px;
    right:18px;
    display:flex;
    justify-content:space-between;
    align-items:end;
}

.info{
    padding:12px 15px;
    background:rgba(2,5,15,.65);
    border:1px solid rgba(120,160,255,.2);
    border-radius:12px;
}

#eventText{
    position:absolute;
    top:110px;
    left:50%;
    transform:translateX(-50%);
    padding:10px 18px;
    border-radius:20px;
    background:rgba(0,0,0,.65);
    color:#dce7ff;
    opacity:0;
    transition:.3s;
}

#eventText.show{
    opacity:1;
}

#crosshair{
    position:absolute;
    width:22px;
    height:22px;
    border:1px solid rgba(180,210,255,.7);
    border-radius:50%;
    transform:translate(-50%,-50%);
    display:none;
}

#minimap{
    width:170px;
    height:170px;
    border:1px solid rgba(120,160,255,.3);
    border-radius:12px;
    background:rgba(0,0,0,.7);
}

#mobileControls{
    position:absolute;
    inset:0;
    display:none;
    pointer-events:none;
}

.joystick{
    position:absolute;
    left:25px;
    bottom:35px;
    width:130px;
    height:130px;
    border:2px solid rgba(150,180,255,.25);
    border-radius:50%;
    pointer-events:auto;
}

.stick{
    position:absolute;
    width:55px;
    height:55px;
    left:35px;
    top:35px;
    border-radius:50%;
    background:rgba(100,140,255,.25);
}

.mobileButtons{
    position:absolute;
    right:25px;
    bottom:30px;
    display:grid;
    grid-template-columns:80px 80px;
    gap:12px;
    pointer-events:auto;
}

.mobileButtons button{
    width:80px;
    height:65px;
    padding:5px;
    font-size:12px;
}

#inventoryGrid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
    gap:10px;
}

.item{
    padding:14px;
    background:rgba(20,28,55,.7);
    border:1px solid rgba(120,160,255,.2);
    border-radius:10px;
}

.item b{
    display:block;
    margin-bottom:5px;
}

.grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
    gap:12px;
}

.card{
    padding:15px;
    border:1px solid rgba(120,160,255,.18);
    border-radius:12px;
    background:rgba(15,22,45,.55);
}

.warning{
    color:#ff9b9b;
}

.good{
    color:#9bffcf;
}

@media(max-width:700px){
    .topbar{
        top:8px;
        left:8px;
        right:8px;
    }

    .hudbox{
        min-width:0;
        padding:8px;
    }

    .bar{
        width:120px;
    }

    #minimap{
        width:120px;
        height:120px;
    }

    #mobileControls{
        display:block;
    }

    .bottomHud{
        bottom:10px;
        left:10px;
        right:10px;
    }
}
</style>
</head>

<body>

<canvas id="game"></canvas>

<div id="ui">

    <!-- MAIN MENU -->
    <section id="menu" class="screen">
        <div class="panel">
            <div class="logo">VOID SPACE</div>
            <div class="subtitle">A PROCEDURAL UNIVERSE</div>

            <div class="menu-buttons">
                <button onclick="newGame()">NEW UNIVERSE</button>
                <button onclick="continueGame()">CONTINUE</button>
                <button onclick="showScreen('howto')">HOW TO PLAY</button>
                <button onclick="showScreen('settings')">SETTINGS</button>
            </div>

            <p style="text-align:center;margin-top:30px">
                Every universe is generated from a seed.
                Explore. Fight. Discover. Survive.
            </p>
        </div>
    </section>

    <!-- HOW TO -->
    <section id="howto" class="screen hidden">
        <div class="panel">
            <h1>HOW TO PLAY</h1>

            <div class="grid">
                <div class="card">
                    <h3>MOVE</h3>
                    <p>WASD / Arrow Keys</p>
                </div>

                <div class="card">
                    <h3>AIM</h3>
                    <p>Move the mouse.</p>
                </div>

                <div class="card">
                    <h3>FIRE</h3>
                    <p>Left Mouse Button / Space</p>
                </div>

                <div class="card">
                    <h3>BOOST</h3>
                    <p>Hold Shift.</p>
                </div>

                <div class="card">
                    <h3>PAUSE</h3>
                    <p>P / Escape</p>
                </div>

                <div class="card">
                    <h3>WORLD</h3>
                    <p>Explore sectors and discover procedural structures.</p>
                </div>
            </div>

            <br>
            <button onclick="showScreen('menu')">BACK</button>
        </div>
    </section>

    <!-- SETTINGS -->
    <section id="settings" class="screen hidden">
        <div class="panel">
            <h1>SETTINGS</h1>

            <div class="card">
                <p>Universe seed</p>
                <input id="seedInput"
                       style="margin-top:10px;width:100%;padding:12px;border-radius:8px;border:1px solid #334;background:#080c18;color:white">
            </div>

            <br>

            <button onclick="applySeed()">USE SEED</button>
            <button onclick="showScreen('menu')">BACK</button>
        </div>
    </section>

    <!-- PAUSE -->
    <section id="pause" class="screen hidden">
        <div class="panel">
            <h1>PAUSED</h1>
            <div class="menu-buttons">
                <button onclick="togglePause()">RESUME</button>
                <button onclick="showInventory()">INVENTORY</button>
                <button onclick="saveGame()">SAVE UNIVERSE</button>
                <button onclick="showScreen('menu');gameRunning=false">MAIN MENU</button>
            </div>
        </div>
    </section>

    <!-- INVENTORY -->
    <section id="inventory" class="screen hidden">
        <div class="panel">
            <h1>SHIP INVENTORY</h1>
            <div id="inventoryGrid"></div>
            <br>
            <button onclick="showScreen('pause')">BACK</button>
        </div>
    </section>

    <!-- GAME OVER -->
    <section id="gameover" class="screen hidden">
        <div class="panel">
            <h1>SHIP DESTROYED</h1>
            <p id="gameOverText"></p>
            <br>
            <div class="menu-buttons">
                <button onclick="continueGame()">LOAD UNIVERSE</button>
                <button onclick="newGame()">NEW UNIVERSE</button>
                <button onclick="showScreen('menu')">MAIN MENU</button>
            </div>
        </div>
    </section>

    <!-- HUD -->
    <div id="hud" class="hidden">

        <div class="topbar">

            <div class="hudbox">
                <div class="hud-title">SECTOR</div>
                <div id="sectorText" class="hud-value">0 : 0</div>
            </div>

            <div class="hudbox">
                <div class="hud-title">SYSTEM</div>
                <div id="systemText" class="hud-value">UNKNOWN</div>
            </div>

            <div class="hudbox">
                <div class="hud-title">CREDITS</div>
                <div id="creditsText" class="hud-value">0</div>
            </div>

            <canvas id="minimap"></canvas>

        </div>

        <div id="eventText"></div>

        <div id="crosshair"></div>

        <div class="bottomHud">

            <div class="info">

                <div>HULL</div>
                <div class="bar">
                    <div id="hullBar"></div>
                </div>

                <div style="margin-top:6px">SHIELD</div>
                <div class="bar">
                    <div id="shieldBar"></div>
                </div>

                <div style="margin-top:6px">XP</div>
                <div class="bar">
                    <div id="xpBar"></div>
                </div>

            </div>

            <div class="info">
                <div id="weaponText">PULSE CANNON</div>
                <div id="levelText">LEVEL 1</div>
                <div id="objectiveText">EXPLORE</div>
            </div>

        </div>

        <div id="mobileControls">

            <div class="joystick" id="joystick">
                <div class="stick" id="stick"></div>
            </div>

            <div class="mobileButtons">
                <button id="fireBtn">FIRE</button>
                <button id="boostBtn">BOOST</button>
            </div>

        </div>

    </div>

</div>

<script>

/* ============================================================
   BASIC SETUP
============================================================ */

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const minimap = document.getElementById("minimap");
const mctx = minimap.getContext("2d");

let W = innerWidth;
let H = innerHeight;

function resize(){
    W = canvas.width = innerWidth;
    H = canvas.height = innerHeight;

    minimap.width = minimap.clientWidth * devicePixelRatio;
    minimap.height = minimap.clientHeight * devicePixelRatio;
}

addEventListener("resize",resize);
resize();


/* ============================================================
   SEEDED RANDOM
============================================================ */

function hashString(str){

    let h = 2166136261;

    for(let i=0;i<str.length;i++){
        h ^= str.charCodeAt(i);
        h +=
            (h<<1)+(h<<4)+(h<<7)+(h<<8)+(h<<24);
    }

    return h >>> 0;
}

function RNG(seed){

    let state = hashString(String(seed)) || 1;

    return function(){

        state += 0x6D2B79F5;

        let t = state;

        t = Math.imul(t ^ t >>> 15,t | 1);

        t ^= t + Math.imul(
            t ^ t >>> 7,
            t | 61
        );

        return ((t ^ t >>> 14) >>> 0) / 4294967296;
    }
}

let worldSeed = "VOID-829174";

function randomRange(rng,a,b){
    return a + rng()*(b-a);
}

function pick(rng,array){
    return array[Math.floor(rng()*array.length)];
}


/* ============================================================
   WORLD DATA
============================================================ */

let world = null;

let player = {
    x:0,
    y:0,

    vx:0,
    vy:0,

    angle:0,

    hull:100,
    maxHull:100,

    shield:100,
    maxShield:100,

    energy:100,
    maxEnergy:100,

    level:1,
    xp:0,

    credits:0,

    weapon:"pulse",

    inventory:{
        iron:0,
        crystal:0,
        alien:0,
        fuel:100,
        medkit:2
    },

    kills:0,

    discovered:[],

    reputation:{
        miners:0,
        pirates:0,
        federation:0,
        aliens:0
    }
};

let gameRunning = false;
let paused = false;

let camera = {
    x:0,
    y:0
};

let bullets = [];
let enemyBullets = [];
let enemies = [];
let particles = [];
let pickups = [];
let structures = [];
let stars = [];

let currentChunk = {
    x:0,
    y:0
};

let currentSystem = null;

let keys = {};
let mouse = {
    x:W/2,
    y:H/2,
    down:false
};

let mobile = {
    x:0,
    y:0,
    fire:false,
    boost:false
};


/* ============================================================
   WORLD GENERATION
============================================================ */

function sectorSeed(x,y){
    return `${worldSeed}:sector:${x}:${y}`;
}

function systemSeed(x,y){
    return `${worldSeed}:system:${x}:${y}`;
}

function generateSector(x,y){

    const rng = RNG(sectorSeed(x,y));

    const biomes = [
        "deep_space",
        "asteroid_field",
        "nebula",
        "ice_field",
        "debris_field",
        "gravity_rift",
        "alien_ruins",
        "pirate_territory",
        "mining_zone"
    ];

    const biome = pick(rng,biomes);

    const starTypes = [
        "blue",
        "yellow",
        "red",
        "white",
        "neutron"
    ];

    let sector = {
        x,
        y,
        biome,

        danger:Math.floor(randomRange(rng,1,11)),

        systemName:
            pick(rng,[
                "Aster",
                "Vega",
                "Nox",
                "Helios",
                "Draconis",
                "Kestrel",
                "Orion",
                "Nyx",
                "Erebus",
                "Solace"
            ]) + "-" +
            Math.floor(rng()*999),

        star:pick(rng,starTypes),

        planets:[],

        structures:[],

        resources:[],

        faction:pick(rng,[
            "miners",
            "federation",
            "pirates",
            "aliens",
            "neutral"
        ]),

        special:pick(rng,[
            "distress_signal",
            "ancient_signal",
            "pirate_patrol",
            "merchant_convoy",
            "derelict",
            "resource_rush",
            "none"
        ])
    };

    let planetCount = 1 + Math.floor(rng()*6);

    for(let i=0;i<planetCount;i++){

        sector.planets.push({
            name:
                String.fromCharCode(65+i) +
                "-" +
                Math.floor(rng()*99),

            type:pick(rng,[
                "rocky",
                "ice",
                "gas",
                "ocean",
                "lava",
                "dead"
            ]),

            radius:randomRange(rng,15,50),
            orbit:randomRange(rng,180,700)
        });
    }

    let structureCount = Math.floor(rng()*5);

    for(let i=0;i<structureCount;i++){

        sector.structures.push({
            type:pick(rng,[
                "station",
                "wreck",
                "mining_colony",
                "pirate_base",
                "alien_ruin",
                "research_outpost"
            ]),

            x:randomRange(rng,-1800,1800),
            y:randomRange(rng,-1800,1800),

            visited:false
        });
    }

    let resourceCount = 5 + Math.floor(rng()*15);

    for(let i=0;i<resourceCount;i++){

        sector.resources.push({
            type:pick(rng,[
                "iron",
                "crystal",
                "alien"
            ]),

            x:randomRange(rng,-2500,2500),
            y:randomRange(rng,-2500,2500),

            amount:1+Math.floor(rng()*8)
        });
    }

    return sector;
}


/* ============================================================
   STARFIELD
============================================================ */

function buildStars(){

    stars=[];

    const rng=RNG(worldSeed+":stars");

    for(let i=0;i<900;i++){

        stars.push({
            x:randomRange(rng,-10000,10000),
            y:randomRange(rng,-10000,10000),
            size:randomRange(rng,.4,2.5),
            alpha:randomRange(rng,.25,1),
            depth:randomRange(rng,.1,.8)
        });
    }
}


/* ============================================================
   CHUNK LOADING
============================================================ */

const CHUNK_SIZE=5000;

function chunkFromPosition(x,y){

    return {
        x:Math.floor(x/CHUNK_SIZE),
        y:Math.floor(y/CHUNK_SIZE)
    };
}

function loadChunk(cx,cy){

    if(
        currentChunk.x===cx &&
        currentChunk.y===cy
    ){
        return;
    }

    currentChunk={
        x:cx,
        y:cy
    };

    currentSystem=generateSector(cx,cy);

    structures =
        currentSystem.structures.map(s=>({
            ...s,
            active:true
        }));

    showEvent(
        `${currentSystem.systemName} • ${currentSystem.biome.replaceAll("_"," ").toUpperCase()}`
    );

    document.getElementById("sectorText").textContent=
        `${cx} : ${cy}`;

    document.getElementById("systemText").textContent=
        currentSystem.systemName;

    document.getElementById("objectiveText").textContent=
        objectiveForSector(currentSystem);

    saveWorldState();
}

function objectiveForSector(s){

    if(s.special==="distress_signal")
        return "INVESTIGATE DISTRESS SIGNAL";

    if(s.special==="ancient_signal")
        return "INVESTIGATE ANCIENT SIGNAL";

    if(s.special==="pirate_patrol")
        return "SURVIVE PIRATE PATROL";

    if(s.special==="merchant_convoy")
        return "PROTECT CONVOY";

    if(s.special==="resource_rush")
        return "COLLECT RESOURCES";

    return "EXPLORE SECTOR";
}


/* ============================================================
   ENEMIES
============================================================ */

const ENEMY_TYPES={

    scout:{
        hp:35,
        speed:2.3,
        size:13,
        damage:8,
        color:"#8aa9ff",
        score:20
    },

    fighter:{
        hp:70,
        speed:1.8,
        size:18,
        damage:12,
        color:"#ff6570",
        score:40
    },

    interceptor:{
        hp:55,
        speed:3.1,
        size:14,
        damage:16,
        color:"#ff9b55",
        score:55
    },

    tank:{
        hp:260,
        speed:.7,
        size:32,
        damage:25,
        color:"#a55cff",
        score:150
    },

    sniper:{
        hp:90,
        speed:.9,
        size:19,
        damage:30,
        color:"#ffdd67",
        score:120
    },

    bomber:{
        hp:130,
        speed:1.1,
        size:23,
        damage:40,
        color:"#ff4d9d",
        score:130
    },

    swarm:{
        hp:20,
        speed:3.5,
        size:9,
        damage:6,
        color:"#d9ff70",
        score:15
    },

    elite:{
        hp:450,
        speed:1.5,
        size:38,
        damage:35,
        color:"#ff38e8",
        score:400
    },

    guardian:{
        hp:900,
        speed:.8,
        size:60,
        damage:50,
        color:"#66eaff",
        score:1000
    }

};

function chooseEnemy(){

    const rng=RNG(
        worldSeed+
        ":"+
        currentChunk.x+
        ":"+
        currentChunk.y+
        ":enemy"
    );

    let danger=currentSystem.danger;

    let types=["scout","fighter","interceptor"];

    if(danger>=3)
        types.push("sniper");

    if(danger>=4)
        types.push("bomber");

    if(danger>=5)
        types.push("tank");

    if(danger>=6)
        types.push("swarm");

    if(danger>=8)
        types.push("elite");

    return pick(rng,types);
}

function spawnEnemy(type){

    type=type || chooseEnemy();

    const data=ENEMY_TYPES[type];

    const a=Math.random()*Math.PI*2;

    const distance=
        Math.max(W,H)*.8+
        Math.random()*600;

    enemies.push({

        type,

        x:player.x+Math.cos(a)*distance,
        y:player.y+Math.sin(a)*distance,

        vx:0,
        vy:0,

        hp:data.hp,
        maxHp:data.hp,

        shoot:Math.random()*100,

        phase:Math.random()*Math.PI*2,

        size:data.size,
        speed:data.speed,

        damage:data.damage,

        color:data.color,

        score:data.score
    });
}


/* ============================================================
   BOSSES
============================================================ */

function spawnBoss(){

    const rng=RNG(
        worldSeed+
        ":boss:"+
        currentChunk.x+
        ":"+
        currentChunk.y
    );

    let bossType=pick(rng,[
        "guardian",
        "guardian",
        "elite"
    ]);

    const d=ENEMY_TYPES[bossType];

    enemies.push({

        type:bossType,

        boss:true,

        x:player.x+900,
        y:player.y,

        vx:0,
        vy:0,

        hp:d.hp+
            player.level*180,

        maxHp:d.hp+
            player.level*180,

        shoot:0,

        phase:0,

        size:d.size,

        speed:d.speed,

        damage:d.damage,

        color:d.color,

        score:d.score
    });

    showEvent("⚠ BOSS DETECTED ⚠");
}


/* ============================================================
   PLAYER SHOOTING
============================================================ */

function shoot(){

    if(!gameRunning || paused)
        return;

    if(player.energy<=0)
        return;

    let rate=1;

    if(player.weapon==="laser")
        rate=0.35;

    if(player.weapon==="spread")
        rate=1.2;

    player.energy-=rate;

    const a=player.angle;

    if(player.weapon==="spread"){

        [-.25,0,.25].forEach(offset=>{

            createBullet(
                a+offset,
                11,
                9,
                16
            );

        });

    }else{

        createBullet(
            a,
            player.weapon==="plasma"?14:12,
            player.weapon==="laser"?25:12,
            player.weapon==="missile"?25:10
        );
    }

    createMuzzle();
}

function createBullet(angle,speed,damage,size){

    bullets.push({

        x:player.x+Math.cos(angle)*25,
        y:player.y+Math.sin(angle)*25,

        vx:Math.cos(angle)*speed,
        vy:Math.sin(angle)*speed,

        damage,
        size,

        life:100
    });
}


/* ============================================================
   UPDATE PLAYER
============================================================ */

function updatePlayer(){

    let dx=0;
    let dy=0;

    if(keys["w"]||keys["arrowup"])dy--;
    if(keys["s"]||keys["arrowdown"])dy++;
    if(keys["a"]||keys["arrowleft"])dx--;
    if(keys["d"]||keys["arrowright"])dx++;

    dx+=mobile.x;
    dy+=mobile.y;

    let len=Math.hypot(dx,dy);

    if(len>1){
        dx/=len;
        dy/=len;
    }

    let boost=
        keys["shift"]||
        mobile.boost;

    let acceleration=
        boost?0.55:0.28;

    let maxSpeed=
        boost?11:6;

    player.vx+=dx*acceleration;
    player.vy+=dy*acceleration;

    player.vx*=.94;
    player.vy*=.94;

    let speed=Math.hypot(
        player.vx,
        player.vy
    );

    if(speed>maxSpeed){

        player.vx=
            player.vx/speed*maxSpeed;

        player.vy=
            player.vy/speed*maxSpeed;
    }

    player.x+=player.vx;
    player.y+=player.vy;

    if(mouse.x!==null){

        const worldMouseX=
            camera.x+
            mouse.x;

        const worldMouseY=
            camera.y+
            mouse.y;

        player.angle=
            Math.atan2(
                worldMouseY-player.y,
                worldMouseX-player.x
            );
    }

    if(mouse.down || keys[" "] || mobile.fire)
        shoot();

    player.energy=Math.min(
        player.maxEnergy,
        player.energy+.4
    );

    if(player.shield<player.maxShield)
        player.shield+=.035;

    let chunk=
        chunkFromPosition(
            player.x,
            player.y
        );

    loadChunk(chunk.x,chunk.y);
}


/* ============================================================
   UPDATE ENEMIES
============================================================ */

function updateEnemies(){

    for(let i=enemies.length-1;i>=0;i--){

        const e=enemies[i];

        let dx=player.x-e.x;
        let dy=player.y-e.y;

        let dist=Math.hypot(dx,dy)||1;

        let nx=dx/dist;
        let ny=dy/dist;

        e.phase+=.03;

        let strafe=
            Math.sin(e.phase)*.8;

        e.vx+=
            nx*e.speed*.035+
            -ny*strafe*.025;

        e.vy+=
            ny*e.speed*.035+
            nx*strafe*.025;

        e.vx*=.96;
        e.vy*=.96;

        e.x+=e.vx;
        e.y+=e.vy;

        e.shoot--;

        if(e.shoot<=0){

            enemyShoot(e);

            e.shoot=
                e.boss?
                35:
                80+Math.random()*100;
        }

        if(dist<e.size+22){

            damagePlayer(e.damage*.02);

            e.x-=nx*3;
            e.y-=ny*3;
        }

        if(e.hp<=0){

            destroyEnemy(i,e);
        }
    }

    // Automatically create encounters based on world state.
    if(enemies.length<2){

        let chance=
            .002+
            currentSystem.danger*.0007;

        if(Math.random()<chance)
            spawnEnemy();
    }
}

function enemyShoot(e){

    let angle=Math.atan2(
        player.y-e.y,
        player.x-e.x
    );

    if(e.boss){

        for(let i=0;i<5;i++){

            let a=
                angle+
                (i-2)*.18;

            enemyBullets.push({
                x:e.x,
                y:e.y,

                vx:Math.cos(a)*5,
                vy:Math.sin(a)*5,

                damage:12,
                size:6,
                life:180
            });
        }

    }else{

        enemyBullets.push({

            x:e.x,
            y:e.y,

            vx:Math.cos(angle)*4,
            vy:Math.sin(angle)*4,

            damage:e.damage,
            size:4,
            life:180
        });
    }
}


/* ============================================================
   DAMAGE
============================================================ */

function damagePlayer(amount){

    if(amount<=0)
        return;

    if(player.shield>0){

        let absorbed=
            Math.min(
                player.shield,
                amount
            );

        player.shield-=absorbed;
        amount-=absorbed;
    }

    player.hull-=amount;

    if(player.hull<=0){

        player.hull=0;

        gameOver();
    }
}


/* ============================================================
   ENEMY DESTRUCTION
============================================================ */

function destroyEnemy(index,e){

    enemies.splice(index,1);

    player.kills++;

    player.xp+=e.score/2;

    player.credits+=
        Math.floor(
            e.score*.5+
            Math.random()*30
        );

    explosion(
        e.x,
        e.y,
        e.color,
        e.boss?60:20
    );

    if(Math.random()<.25){

        pickups.push({

            x:e.x,
            y:e.y,

            type:
                Math.random()<.5?
                "shield":
                "energy"
        });
    }

    checkLevel();
}


/* ============================================================
   LEVEL SYSTEM
============================================================ */

function checkLevel(){

    let needed=
        100+
        (player.level-1)*100;

    while(player.xp>=needed){

        player.xp-=needed;

        player.level++;

        player.maxHull+=10;
        player.hull=player.maxHull;

        player.maxShield+=10;
        player.shield=player.maxShield;

        showEvent(
            "LEVEL UP • SHIP UPGRADED"
        );

        needed=
            100+
            (player.level-1)*100;
    }
}


/* ============================================================
   BULLETS
============================================================ */

function updateBullets(){

    for(let i=bullets.length-1;i>=0;i--){

        const b=bullets[i];

        b.x+=b.vx;
        b.y+=b.vy;

        b.life--;

        let hit=false;

        for(let j=enemies.length-1;j>=0;j--){

            const e=enemies[j];

            if(
                Math.hypot(
                    b.x-e.x,
                    b.y-e.y
                )<
                b.size+e.size
            ){

                e.hp-=b.damage;

                explosion(
                    b.x,
                    b.y,
                    "#ffffff",
                    3
                );

                hit=true;

                if(e.hp<=0)
                    destroyEnemy(j,e);

                break;
            }
        }

        if(hit || b.life<=0)
            bullets.splice(i,1);
    }
}

function updateEnemyBullets(){

    for(let i=enemyBullets.length-1;i>=0;i--){

        const b=enemyBullets[i];

        b.x+=b.vx;
        b.y+=b.vy;

        b.life--;

        if(
            Math.hypot(
                b.x-player.x,
                b.y-player.y
            )<
            b.size+16
        ){

            damagePlayer(b.damage);

            explosion(
                b.x,
                b.y,
                "#ff5965",
                5
            );

            enemyBullets.splice(i,1);

        }else if(b.life<=0){

            enemyBullets.splice(i,1);
        }
    }
}


/* ============================================================
   RESOURCES / PICKUPS
============================================================ */

function updateResources(){

    if(!currentSystem)
        return;

    for(const r of currentSystem.resources){

        let dx=r.x+
            currentChunk.x*CHUNK_SIZE-
            player.x;

        let dy=r.y+
            currentChunk.y*CHUNK_SIZE-
            player.y;

        if(Math.hypot(dx,dy)<35){

            player.inventory[r.type]+=r.amount;

            r.amount=0;

            showEvent(
                `COLLECTED ${r.type.toUpperCase()}`
            );
        }
    }

    currentSystem.resources=
        currentSystem.resources.filter(
            r=>r.amount>0
        );
}

function updatePickups(){

    for(let i=pickups.length-1;i>=0;i--){

        let p=pickups[i];

        let dx=player.x-p.x;
        let dy=player.y-p.y;

        let d=Math.hypot(dx,dy)||1;

        if(d<120){

            p.x+=dx/d*2;
            p.y+=dy/d*2;
        }

        if(d<25){

            if(p.type==="shield")
                player.shield=
                    Math.min(
                        player.maxShield,
                        player.shield+40
                    );

            if(p.type==="energy")
                player.energy=
                    Math.min(
                        player.maxEnergy,
                        player.energy+50
                    );

            showEvent(
                p.type.toUpperCase()+" RECOVERED"
            );

            pickups.splice(i,1);
        }
    }
}


/* ============================================================
   STRUCTURES
============================================================ */

function updateStructures(){

    for(const s of structures){

        let sx=
            s.x+
            currentChunk.x*CHUNK_SIZE;

        let sy=
            s.y+
            currentChunk.y*CHUNK_SIZE;

        let d=
            Math.hypot(
                sx-player.x,
                sy-player.y
            );

        if(d<100 && !s.visited){

            s.visited=true;

            discoverStructure(s);
        }
    }
}

function discoverStructure(s){

    let text="";

    if(s.type==="station"){

        player.credits+=100;

        text=
            "SPACE STATION DISCOVERED • +100 CREDITS";
    }

    else if(s.type==="wreck"){

        player.inventory.iron+=5;

        text=
            "WRECK FOUND • SALVAGED MATERIALS";
    }

    else if(s.type==="mining_colony"){

        player.reputation.miners+=5;

        text=
            "MINING COLONY • MINER REPUTATION +5";
    }

    else if(s.type==="pirate_base"){

        player.reputation.pirates-=5;

        text=
            "PIRATE BASE • HOSTILE ACTIVITY";
    }

    else if(s.type==="alien_ruin"){

        player.inventory.alien+=2;

        player.reputation.aliens+=3;

        text=
            "ANCIENT ALIEN RUINS DISCOVERED";
    }

    else{

        text=
            "RESEARCH OUTPOST DISCOVERED";
    }

    showEvent(text);

    player.discovered.push(
        `${currentChunk.x}:${currentChunk.y}:${s.type}`
    );
}


/* ============================================================
   PARTICLES
============================================================ */

function explosion(x,y,color,count){

    for(let i=0;i<count;i++){

        let a=Math.random()*Math.PI*2;
        let speed=Math.random()*6+1;

        particles.push({

            x,
            y,

            vx:Math.cos(a)*speed,
            vy:Math.sin(a)*speed,

            life:30+Math.random()*30,

            size:Math.random()*4+1,

            color
        });
    }
}

function createMuzzle(){

    explosion(
        player.x+
        Math.cos(player.angle)*25,

        player.y+
        Math.sin(player.angle)*25,

        "#b8d6ff",
        4
    );
}

function updateParticles(){

    for(let i=particles.length-1;i>=0;i--){

        let p=particles[i];

        p.x+=p.vx;
        p.y+=p.vy;

        p.vx*=.96;
        p.vy*=.96;

        p.life--;

        if(p.life<=0)
            particles.splice(i,1);
    }
}


/* ============================================================
   DRAW
============================================================ */

function worldToScreen(x,y){

    return {
        x:x-camera.x+W/2,
        y:y-camera.y+H/2
    };
}

function drawBackground(){

    ctx.fillStyle="#02030a";
    ctx.fillRect(0,0,W,H);

    for(const s of stars){

        let x=
            (s.x-camera.x*s.depth)%W;

        let y=
            (s.y-camera.y*s.depth)%H;

        if(x<0)x+=W;
        if(y<0)y+=H;

        ctx.globalAlpha=s.alpha;

        ctx.fillStyle="#dce7ff";

        ctx.beginPath();

        ctx.arc(
            x,
            y,
            s.size,
            0,
            Math.PI*2
        );

        ctx.fill();
    }

    ctx.globalAlpha=1;

    drawBiome();
}

function drawBiome(){

    if(!currentSystem)
        return;

    if(currentSystem.biome==="nebula"){

        let g=
            ctx.createRadialGradient(
                W*.7,
                H*.3,
                50,
                W*.7,
                H*.3,
                W*.7
            );

        g.addColorStop(0,"rgba(80,40,160,.12)");
        g.addColorStop(1,"rgba(0,0,0,0)");

        ctx.fillStyle=g;
        ctx.fillRect(0,0,W,H);
    }

    if(currentSystem.biome==="asteroid_field"){

        for(let i=0;i<50;i++){

            let x=
                ((i*743-camera.x*.2)%W+W)%W;

            let y=
                ((i*421-camera.y*.2)%H+H)%H;

            ctx.fillStyle="rgba(130,130,145,.3)";

            ctx.beginPath();

            ctx.arc(
                x,
                y,
                2+(i%5),
                0,
                Math.PI*2
            );

            ctx.fill();
        }
    }
}

function drawPlayer(){

    let s=
        worldToScreen(
            player.x,
            player.y
        );

    ctx.save();

    ctx.translate(s.x,s.y);
    ctx.rotate(player.angle);

    ctx.beginPath();

    ctx.moveTo(25,0);
    ctx.lineTo(-18,-13);
    ctx.lineTo(-10,0);
    ctx.lineTo(-18,13);
    ctx.closePath();

    ctx.fillStyle="#dce7ff";
    ctx.fill();

    ctx.strokeStyle="#6ea1ff";
    ctx.lineWidth=2;
    ctx.stroke();

    if(player.shield>0){

        ctx.beginPath();

        ctx.arc(
            0,
            0,
            25,
            0,
            Math.PI*2
        );

        ctx.strokeStyle=
            "rgba(80,160,255,.35)";

        ctx.stroke();
    }

    ctx.restore();
}

function drawEnemies(){

    for(const e of enemies){

        let s=
            worldToScreen(
                e.x,
                e.y
            );

        ctx.save();

        ctx.translate(s.x,s.y);

        let a=Math.atan2(
            player.y-e.y,
            player.x-e.x
        );

        ctx.rotate(a);

        ctx.beginPath();

        ctx.moveTo(e.size,0);
        ctx.lineTo(-e.size,-e.size*.65);
        ctx.lineTo(-e.size*.6,0);
        ctx.lineTo(-e.size,e.size*.65);
        ctx.closePath();

        ctx.fillStyle=e.color;
        ctx.fill();

        ctx.strokeStyle="#fff";
        ctx.globalAlpha=.5;
        ctx.stroke();

        ctx.restore();

        // health bar

        if(e.hp<e.maxHp){

            let width=e.size*2.5;

            ctx.fillStyle="#111";

            ctx.fillRect(
                s.x-width/2,
                s.y-e.size-8,
                width,
                4
            );

            ctx.fillStyle="#ff4e63";

            ctx.fillRect(
                s.x-width/2,
                s.y-e.size-8,
                width*(e.hp/e.maxHp),
                4
            );
        }
    }
}

function drawBullets(){

    ctx.fillStyle="#b9d7ff";

    for(const b of bullets){

        let s=
            worldToScreen(
                b.x,
                b.y
            );

        ctx.beginPath();

        ctx.arc(
            s.x,
            s.y,
            b.size/2,
            0,
            Math.PI*2
        );

        ctx.fill();
    }

    ctx.fillStyle="#ff6670";

    for(const b of enemyBullets){

        let s=
            worldToScreen(
                b.x,
                b.y
            );

        ctx.beginPath();

        ctx.arc(
            s.x,
            s.y,
            b.size,
            0,
            Math.PI*2
        );

        ctx.fill();
    }
}

function drawParticles(){

    for(const p of particles){

        let s=
            worldToScreen(
                p.x,
                p.y
            );

        ctx.globalAlpha=
            Math.max(0,p.life/60);

        ctx.fillStyle=p.color;

        ctx.beginPath();

        ctx.arc(
            s.x,
            s.y,
            p.size,
            0,
            Math.PI*2
        );

        ctx.fill();
    }

    ctx.globalAlpha=1;
}

function drawStructures(){

    if(!currentSystem)
        return;

    for(const s of structures){

        let x=
            s.x+
            currentChunk.x*CHUNK_SIZE;

        let y=
            s.y+
            currentChunk.y*CHUNK_SIZE;

        let p=worldToScreen(x,y);

        if(
            p.x<-100 ||
            p.x>W+100 ||
            p.y<-100 ||
            p.y>H+100
        )
            continue;

        ctx.save();

        ctx.translate(p.x,p.y);

        ctx.fillStyle=
            s.visited?
            "rgba(100,110,140,.4)":
            "#728cff";

        ctx.strokeStyle="#b8c8ff";

        ctx.beginPath();

        if(s.type==="station"){

            ctx.rect(-30,-18,60,36);

        }else if(s.type==="wreck"){

            ctx.rotate(.4);
            ctx.rect(-20,-8,40,16);

        }else{

            ctx.moveTo(0,-25);
            ctx.lineTo(25,20);
            ctx.lineTo(-25,20);
            ctx.closePath();
        }

        ctx.fill();
        ctx.stroke();

        ctx.restore();
    }
}

function drawPickups(){

    for(const p of pickups){

        let s=
            worldToScreen(
                p.x,
                p.y
            );

        ctx.fillStyle=
            p.type==="shield"?
            "#6bbcff":
            "#c56cff";

        ctx.beginPath();

        ctx.arc(
            s.x,
            s.y,
            8,
            0,
            Math.PI*2
        );

        ctx.fill();
    }
}


/* ============================================================
   MINIMAP
============================================================ */

function drawMinimap(){

    const w=minimap.width;
    const h=minimap.height;

    mctx.clearRect(0,0,w,h);

    mctx.fillStyle="#02050d";
    mctx.fillRect(0,0,w,h);

    mctx.strokeStyle="rgba(100,140,255,.25)";

    for(let i=0;i<5;i++){

        mctx.beginPath();

        mctx.moveTo(
            w/2+i*25,
            0
        );

        mctx.lineTo(
            w/2+i*25,
            h
        );

        mctx.stroke();

        mctx.beginPath();

        mctx.moveTo(
            0,
            h/2+i*25
        );

        mctx.lineTo(
            w,
            h/2+i*25
        );

        mctx.stroke();
    }

    // player

    mctx.fillStyle="#fff";

    mctx.beginPath();

    mctx.arc(
        w/2,
        h/2,
        4,
        0,
        Math.PI*2
    );

    mctx.fill();

    // enemies

    mctx.fillStyle="#ff5968";

    for(const e of enemies){

        let dx=
            (e.x-player.x)/30;

        let dy=
            (e.y-player.y)/30;

        if(
            Math.abs(dx)<w/2 &&
            Math.abs(dy)<h/2
        ){

            mctx.beginPath();

            mctx.arc(
                w/2+dx,
                h/2+dy,
                3,
                0,
                Math.PI*2
            );

            mctx.fill();
        }
    }
}


/* ============================================================
   CAMERA
============================================================ */

function updateCamera(){

    camera.x+=
        (player.x-camera.x)*.12;

    camera.y+=
        (player.y-camera.y)*.12;
}


/* ============================================================
   HUD
============================================================ */

function updateHUD(){

    document.getElementById("hullBar").style.width=
        `${Math.max(0,player.hull/player.maxHull*100)}%`;

    document.getElementById("shieldBar").style.width=
        `${Math.max(0,player.shield/player.maxShield*100)}%`;

    let needed=
        100+
        (player.level-1)*100;

    document.getElementById("xpBar").style.width=
        `${Math.min(100,player.xp/needed*100)}%`;

    document.getElementById("creditsText").textContent=
        player.credits;

    document.getElementById("levelText").textContent=
        `LEVEL ${player.level}`;

    let names={
        pulse:"PULSE CANNON",
        spread:"SPREAD CANNON",
        laser:"LASER",
        missile:"MISSILE",
        plasma:"PLASMA"
    };

    document.getElementById("weaponText").textContent=
        names[player.weapon] || player.weapon;
}


/* ============================================================
   GAME LOOP
============================================================ */

let lastTime=0;

function loop(time){

    requestAnimationFrame(loop);

    if(!gameRunning || paused)
        return;

    updatePlayer();
    updateEnemies();
    updateBullets();
    updateEnemyBullets();
    updateParticles();
    updatePickups();
    updateResources();
    updateStructures();
    updateCamera();

    drawBackground();
    drawStructures();
    drawPickups();
    drawBullets();
    drawEnemies();
    drawParticles();
    drawPlayer();

    drawMinimap();
    updateHUD();
}

requestAnimationFrame(loop);


/* ============================================================
   UI
============================================================ */

function showScreen(id){

    document.querySelectorAll(".screen")
        .forEach(x=>x.classList.add("hidden"));

    if(id)
        document.getElementById(id)
            .classList.remove("hidden");

    if(id==="menu"){

        document.getElementById("hud")
            .classList.add("hidden");

    }else if(
        id!=="howto" &&
        id!=="settings" &&
        id!=="inventory"
    ){

        document.getElementById("hud")
            .classList.remove("hidden");
    }
}

function startGame(){

    gameRunning=true;
    paused=false;

    document.getElementById("hud")
        .classList.remove("hidden");

    document.querySelectorAll(".screen")
        .forEach(x=>x.classList.add("hidden"));

    buildStars();

    loadChunk(
        chunkFromPosition(
            player.x,
            player.y
        ).x,
        chunkFromPosition(
            player.x,
            player.y
        ).y
    );
}

function newGame(){

    worldSeed=
        document.getElementById("seedInput").value.trim()
        ||
        "VOID-"+Math.floor(Math.random()*999999999);

    player={
        x:0,
        y:0,

        vx:0,
        vy:0,

        angle:0,

        hull:100,
        maxHull:100,

        shield:100,
        maxShield:100,

        energy:100,
        maxEnergy:100,

        level:1,
        xp:0,

        credits:0,

        weapon:"pulse",

        inventory:{
            iron:0,
            crystal:0,
            alien:0,
            fuel:100,
            medkit:2
        },

        kills:0,

        discovered:[],

        reputation:{
            miners:0,
            pirates:0,
            federation:0,
            aliens:0
        }
    };

    bullets=[];
    enemyBullets=[];
    enemies=[];
    particles=[];
    pickups=[];

    currentChunk={
        x:999999,
        y:999999
    };

    saveGame();

    startGame();

    showEvent(
        `NEW UNIVERSE • SEED ${worldSeed}`
    );
}

function continueGame(){

    let saved=
        localStorage.getItem("VOID_SPACE_SAVE");

    if(!saved){

        newGame();
        return;
    }

    try{

        const data=JSON.parse(saved);

        worldSeed=data.seed || worldSeed;

        player=data.player || player;

        startGame();

        showEvent(
            "UNIVERSE RESTORED"
        );

    }catch(e){

        newGame();
    }
}

function saveGame(){

    saveWorldState();

    showEvent(
        "UNIVERSE SAVED"
    );
}

function saveWorldState(){

    try{

        localStorage.setItem(
            "VOID_SPACE_SAVE",

            JSON.stringify({

                seed:worldSeed,

                player,

                timestamp:Date.now()
            })
        );

    }catch(e){}
}

function applySeed(){

    worldSeed=
        document.getElementById("seedInput")
        .value
        .trim();

    if(!worldSeed)
        worldSeed="VOID-"+Math.floor(Math.random()*999999999);

    showEvent(
        "SEED READY"
    );

    showScreen("menu");
}

function showInventory(){

    const grid=
        document.getElementById("inventoryGrid");

    grid.innerHTML="";

    for(const key in player.inventory){

        let div=document.createElement("div");

        div.className="item";

        div.innerHTML=
            `<b>${key.toUpperCase()}</b>
             <span>${player.inventory[key]}</span>`;

        grid.appendChild(div);
    }

    showScreen("inventory");
}

function togglePause(){

    paused=!paused;

    if(paused)
        showScreen("pause");
    else
        document.querySelectorAll(".screen")
            .forEach(x=>x.classList.add("hidden"));
}

function gameOver(){

    gameRunning=false;

    document.getElementById("gameOverText")
        .innerHTML=
        `LEVEL ${player.level}<br>
         KILLS ${player.kills}<br>
         CREDITS ${player.credits}<br>
         SECTOR ${currentChunk.x}:${currentChunk.y}`;

    showScreen("gameover");

    saveWorldState();
}

function showEvent(text){

    const el=
        document.getElementById("eventText");

    el.textContent=text;

    el.classList.add("show");

    clearTimeout(showEvent.timer);

    showEvent.timer=
        setTimeout(()=>{
            el.classList.remove("show");
        },3500);
}


/* ============================================================
   INPUT
============================================================ */

addEventListener("keydown",e=>{

    keys[e.key.toLowerCase()]=true;

    if(e.key==="Escape" || e.key.toLowerCase()==="p"){

        if(gameRunning)
            togglePause();
    }

    if(e.key==="1")
        player.weapon="pulse";

    if(e.key==="2")
        player.weapon="spread";

    if(e.key==="3")
        player.weapon="laser";

    if(e.key==="4")
        player.weapon="missile";

    if(e.key==="5")
        player.weapon="plasma";
});

addEventListener("keyup",e=>{

    keys[e.key.toLowerCase()]=false;
});

canvas.addEventListener("mousemove",e=>{

    mouse.x=e.clientX;
    mouse.y=e.clientY;

    const cross=
        document.getElementById("crosshair");

    cross.style.display="block";

    cross.style.left=
        e.clientX+"px";

    cross.style.top=
        e.clientY+"px";
});

canvas.addEventListener("mousedown",e=>{

    if(e.button===0)
        mouse.down=true;
});

addEventListener("mouseup",e=>{

    if(e.button===0)
        mouse.down=false;
});


/* ============================================================
   MOBILE
============================================================ */

const joystick=
    document.getElementById("joystick");

const stick=
    document.getElementById("stick");

let joystickActive=false;

function joystickMove(e){

    const rect=
        joystick.getBoundingClientRect();

    const touch=
        e.touches[0];

    let x=
        touch.clientX-
        (rect.left+rect.width/2);

    let y=
        touch.clientY-
        (rect.top+rect.height/2);

    let d=Math.hypot(x,y);

    let max=45;

    if(d>max){

        x=x/d*max;
        y=y/d*max;
    }

    mobile.x=x/max;
    mobile.y=y/max;

    stick.style.transform=
        `translate(${x}px,${y}px)`;
}

joystick.addEventListener(
    "touchstart",
    e=>{
        joystickActive=true;
        joystickMove(e);
    },
    {passive:true}
);

joystick.addEventListener(
    "touchmove",
    e=>{
        if(joystickActive)
            joystickMove(e);
    },
    {passive:true}
);

joystick.addEventListener(
    "touchend",
    ()=>{
        joystickActive=false;
        mobile.x=0;
        mobile.y=0;
        stick.style.transform="";
    }
);

const fireBtn=
    document.getElementById("fireBtn");

fireBtn.addEventListener(
    "touchstart",
    ()=>{
        mobile.fire=true;
    }
);

fireBtn.addEventListener(
    "touchend",
    ()=>{
        mobile.fire=false;
    }
);

const boostBtn=
    document.getElementById("boostBtn");

boostBtn.addEventListener(
    "touchstart",
    ()=>{
        mobile.boost=true;
    }
);

boostBtn.addEventListener(
    "touchend",
    ()=>{
        mobile.boost=false;
    }
);


/* ============================================================
   INITIALIZATION
============================================================ */

document.getElementById("seedInput").value=
    worldSeed;

buildStars();

showScreen("menu");

</script>

</body>
</html>
"""


# ============================================================
# PYTHON PROCEDURAL WORLD API
# ============================================================

def deterministic_rng(seed):
    """
    Deterministic RNG for server-side world generation.
    Same seed always creates the same result.
    """
    digest = hashlib.sha256(str(seed).encode()).hexdigest()
    integer = int(digest[:16], 16)
    return random.Random(integer)


def generate_sector(seed, x, y):
    """
    Minecraft-style deterministic sector generation.

    The browser can request any sector without Python
    storing every sector in memory.
    """

    rng = deterministic_rng(f"{seed}:sector:{x}:{y}")

    biomes = [
        "deep_space",
        "asteroid_field",
        "nebula",
        "ice_field",
        "debris_field",
        "gravity_rift",
        "alien_ruins",
        "pirate_territory",
        "mining_zone"
    ]

    star_types = [
        "blue",
        "yellow",
        "red",
        "white",
        "neutron"
    ]

    system_names = [
        "Aster",
        "Vega",
        "Nox",
        "Helios",
        "Draconis",
        "Kestrel",
        "Orion",
        "Nyx",
        "Erebus",
        "Solace"
    ]

    factions = [
        "miners",
        "federation",
        "pirates",
        "aliens",
        "neutral"
    ]

    specials = [
        "distress_signal",
        "ancient_signal",
        "pirate_patrol",
        "merchant_convoy",
        "derelict",
        "resource_rush",
        "none"
    ]

    sector = {
        "x": x,
        "y": y,

        "biome": rng.choice(biomes),

        "danger": rng.randint(1, 10),

        "system_name":
            f"{rng.choice(system_names)}-{rng.randint(100,999)}",

        "star":
            rng.choice(star_types),

        "faction":
            rng.choice(factions),

        "special":
            rng.choice(specials),

        "planets": [],
        "structures": [],
        "resources": []
    }

    planet_types = [
        "rocky",
        "ice",
        "gas",
        "ocean",
        "lava",
        "dead"
    ]

    for i in range(rng.randint(1, 6)):

        sector["planets"].append({
            "name":
                f"{chr(65+i)}-{rng.randint(10,99)}",

            "type":
                rng.choice(planet_types),

            "radius":
                rng.randint(15, 50),

            "orbit":
                rng.randint(180, 700)
        })

    structure_types = [
        "station",
        "wreck",
        "mining_colony",
        "pirate_base",
        "alien_ruin",
        "research_outpost"
    ]

    for _ in range(rng.randint(0, 5)):

        sector["structures"].append({
            "type": rng.choice(structure_types),

            "x":
                round(rng.uniform(-1800, 1800), 2),

            "y":
                round(rng.uniform(-1800, 1800), 2)
        })

    resource_types = [
        "iron",
        "crystal",
        "alien"
    ]

    for _ in range(rng.randint(5, 20)):

        sector["resources"].append({
            "type":
                rng.choice(resource_types),

            "x":
                round(rng.uniform(-2500, 2500), 2),

            "y":
                round(rng.uniform(-2500, 2500), 2),

            "amount":
                rng.randint(1, 8)
        })

    return sector


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/health")
def health():
    return "VOID SPACE ONLINE"


@app.route("/api/sector")
def api_sector():

    seed = request.args.get(
        "seed",
        "VOID-829174"
    )

    try:
        x = int(request.args.get("x", 0))
        y = int(request.args.get("y", 0))
    except ValueError:
        return jsonify({
            "error": "Invalid coordinates"
        }), 400

    sector = generate_sector(
        seed,
        x,
        y
    )

    return jsonify(sector)


@app.route("/api/world")
def api_world():

    seed = request.args.get(
        "seed",
        "VOID-829174"
    )

    radius = min(
        max(
            int(request.args.get("radius", 1)),
            1
        ),
        5
    )

    sectors = []

    for x in range(-radius, radius + 1):

        for y in range(-radius, radius + 1):

            sectors.append(
                generate_sector(
                    seed,
                    x,
                    y
                )
            )

    return jsonify({
        "seed": seed,
        "radius": radius,
        "sectors": sectors
    })


@app.route("/api/galaxy")
def api_galaxy():

    seed = request.args.get(
        "seed",
        "VOID-829174"
    )

    rng = deterministic_rng(
        f"{seed}:galaxy"
    )

    galaxy_types = [
        "spiral",
        "cluster",
        "irregular",
        "ring"
    ]

    return jsonify({

        "seed": seed,

        "type":
            rng.choice(galaxy_types),

        "age":
            rng.randint(5, 14),

        "stars":
            rng.randint(
                1000000,
                9000000
            ),

        "civilizations":
            rng.randint(3, 15),

        "factions":
            [
                "Federation",
                "Mining Guild",
                "Pirate Clans",
                "Outer Colonies",
                "Ancient Aliens"
            ]
    })


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
