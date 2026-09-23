from flask import Flask, render_template_string, jsonify, request
import os
import random
import hashlib

app = Flask(__name__)

# ============================================================
# VOID SPACE
# Persistent Procedural Space Sandbox
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
    color:white;
    font-family:Arial,Helvetica,sans-serif;
}

body{
    touch-action:none;
}

canvas{
    position:fixed;
    inset:0;
    width:100%;
    height:100%;
    display:block;
    background:#02030a;
}

.hidden{
    display:none!important;
}

/* ============================================================
   UI
============================================================ */

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
        radial-gradient(
            circle at center,
            rgba(35,55,120,.15),
            rgba(0,0,0,.86)
        );
}

.panel{
    width:min(900px,92vw);
    max-height:90vh;

    overflow:auto;

    padding:32px;

    border:
        1px solid
        rgba(120,165,255,.28);

    border-radius:18px;

    background:
        rgba(5,8,20,.92);

    box-shadow:
        0 0 70px
        rgba(40,90,255,.16);

    backdrop-filter:blur(14px);
}

.logo{
    font-size:clamp(45px,9vw,100px);
    font-weight:900;

    text-align:center;

    letter-spacing:.16em;

    text-shadow:
        0 0 10px white,
        0 0 30px #5c8dff,
        0 0 70px #315cff;
}

.subtitle{
    text-align:center;

    color:#8ea7d8;

    letter-spacing:.3em;

    margin:
        10px
        0
        35px;
}

button{
    border:
        1px solid
        rgba(120,160,255,.4);

    background:
        rgba(20,30,65,.8);

    color:white;

    padding:
        14px
        20px;

    border-radius:10px;

    cursor:pointer;

    font-size:15px;

    transition:.15s;
}

button:hover{
    background:
        rgba(50,75,145,.8);

    border-color:#8bb1ff;

    transform:
        translateY(-1px);
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
    color:#b9c4df;
    line-height:1.6;
}

.grid{
    display:grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(220px,1fr)
        );

    gap:12px;
}

.card{
    padding:16px;

    border:
        1px solid
        rgba(120,160,255,.18);

    border-radius:12px;

    background:
        rgba(15,22,45,.55);
}

/* ============================================================
   HUD
============================================================ */

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

    align-items:flex-start;

    gap:10px;
}

.hudbox{
    min-width:130px;

    padding:10px 13px;

    border:
        1px solid
        rgba(120,160,255,.2);

    border-radius:12px;

    background:
        rgba(2,5,15,.62);

    backdrop-filter:blur(8px);
}

.hud-title{
    color:#6e91d8;

    font-size:9px;

    letter-spacing:.15em;

    margin-bottom:4px;
}

.hud-value{
    font-weight:bold;

    white-space:nowrap;
}

#minimap{
    width:170px;
    height:170px;

    border:
        1px solid
        rgba(120,160,255,.3);

    border-radius:12px;

    background:
        rgba(0,0,0,.7);
}

#eventText{
    position:absolute;

    top:115px;
    left:50%;

    transform:
        translateX(-50%);

    padding:
        10px
        20px;

    border-radius:20px;

    background:
        rgba(0,0,0,.7);

    color:#dce7ff;

    opacity:0;

    transition:.3s;

    white-space:nowrap;
}

#eventText.show{
    opacity:1;
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
    padding:
        12px
        15px;

    background:
        rgba(2,5,15,.68);

    border:
        1px solid
        rgba(120,160,255,.2);

    border-radius:12px;
}

.bar{
    width:220px;
    max-width:35vw;

    height:8px;

    margin-top:3px;

    background:#121827;

    border-radius:10px;

    overflow:hidden;
}

.bar div{
    height:100%;

    width:100%;

    transition:.15s;
}

#hullBar{
    background:#e0525e;
}

#shieldBar{
    background:#5e9eff;
}

#energyBar{
    background:#bd70ff;
}

#xpBar{
    background:#65e6a4;
}

#crosshair{
    position:absolute;

    width:24px;
    height:24px;

    border:
        1px solid
        rgba(190,220,255,.7);

    border-radius:50%;

    transform:
        translate(-50%,-50%);

    display:none;
}

#crosshair::before,
#crosshair::after{
    content:"";

    position:absolute;

    background:
        rgba(190,220,255,.6);
}

#crosshair::before{
    width:32px;
    height:1px;

    left:-5px;
    top:11px;
}

#crosshair::after{
    width:1px;
    height:32px;

    left:11px;
    top:-5px;
}

/* ============================================================
   MOBILE
============================================================ */

#mobileControls{
    display:none;

    position:absolute;

    inset:0;

    pointer-events:none;
}

.joystick{
    position:absolute;

    left:25px;
    bottom:30px;

    width:130px;
    height:130px;

    border:
        2px solid
        rgba(150,180,255,.25);

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

    background:
        rgba(100,140,255,.25);
}

.mobileButtons{
    position:absolute;

    right:25px;
    bottom:30px;

    display:grid;

    grid-template-columns:
        80px 80px;

    gap:12px;

    pointer-events:auto;
}

.mobileButtons button{
    width:80px;
    height:65px;

    padding:5px;

    font-size:11px;
}

/* ============================================================
   INVENTORY
============================================================ */

#inventoryGrid{
    display:grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(140px,1fr)
        );

    gap:10px;
}

.item{
    padding:14px;

    background:
        rgba(20,28,55,.7);

    border:
        1px solid
        rgba(120,160,255,.2);

    border-radius:10px;
}

.item b{
    display:block;

    margin-bottom:5px;
}

@media(max-width:700px){

    .topbar{
        top:7px;
        left:7px;
        right:7px;
    }

    .hudbox{
        min-width:0;
        padding:7px 9px;
    }

    .hudbox:nth-child(2){
        display:none;
    }

    #minimap{
        width:115px;
        height:115px;
    }

    .bar{
        width:125px;
    }

    #mobileControls{
        display:block;
    }

    .bottomHud{
        bottom:8px;
        left:8px;
        right:8px;
    }

    .info{
        padding:8px;
        font-size:11px;
    }

    #eventText{
        top:90px;
        font-size:11px;
    }
}
</style>
</head>

<body>

<canvas id="game"></canvas>

<div id="ui">

<!-- ==========================================================
     MAIN MENU
=========================================================== -->

<section id="menu" class="screen">

<div class="panel">

<div class="logo">
VOID SPACE
</div>

<div class="subtitle">
A PROCEDURAL UNIVERSE
</div>

<div class="menu-buttons">

<button onclick="newGame()">
NEW UNIVERSE
</button>

<button onclick="continueGame()">
CONTINUE
</button>

<button onclick="showScreen('howto')">
HOW TO PLAY
</button>

<button onclick="showScreen('settings')">
SETTINGS
</button>

</div>

<p style="text-align:center;margin-top:30px">
One seed creates an entire universe.
Explore it. Fight in it. Change it.
</p>

</div>

</section>


<!-- ==========================================================
     HOW TO PLAY
=========================================================== -->

<section id="howto" class="screen hidden">

<div class="panel">

<h1>HOW TO PLAY</h1>

<div class="grid">

<div class="card">
<h3>MOVE</h3>
<p>WASD or Arrow Keys.</p>
</div>

<div class="card">
<h3>ROTATE</h3>
<p>The spaceship smoothly rotates toward your mouse.</p>
</div>

<div class="card">
<h3>FIRE</h3>
<p>Left Mouse Button or Space.</p>
</div>

<div class="card">
<h3>BOOST</h3>
<p>Hold Shift.</p>
</div>

<div class="card">
<h3>WEAPONS</h3>
<p>Keys 1-5 switch weapons.</p>
</div>

<div class="card">
<h3>WORLD</h3>
<p>Move between procedural sectors.</p>
</div>

<div class="card">
<h3>DISCOVER</h3>
<p>Find stations, wrecks, colonies and alien ruins.</p>
</div>

<div class="card">
<h3>COMBAT</h3>
<p>Enemies are generated according to the danger of the region.</p>
</div>

</div>

<br>

<button onclick="showScreen('menu')">
BACK
</button>

</div>

</section>


<!-- ==========================================================
     SETTINGS
=========================================================== -->

<section id="settings" class="screen hidden">

<div class="panel">

<h1>SETTINGS</h1>

<div class="card">

<p>Universe Seed</p>

<input
id="seedInput"
style="
margin-top:10px;
width:100%;
padding:12px;
border-radius:8px;
border:1px solid #334;
background:#080c18;
color:white;
"
>

</div>

<br>

<button onclick="applySeed()">
USE SEED
</button>

<button onclick="showScreen('menu')">
BACK
</button>

</div>

</section>


<!-- ==========================================================
     PAUSE
=========================================================== -->

<section id="pause" class="screen hidden">

<div class="panel">

<h1>PAUSED</h1>

<div class="menu-buttons">

<button onclick="togglePause()">
RESUME
</button>

<button onclick="showInventory()">
INVENTORY
</button>

<button onclick="saveGame()">
SAVE UNIVERSE
</button>

<button onclick="showScreen('menu');gameRunning=false">
MAIN MENU
</button>

</div>

</div>

</section>


<!-- ==========================================================
     INVENTORY
=========================================================== -->

<section id="inventory" class="screen hidden">

<div class="panel">

<h1>SHIP INVENTORY</h1>

<div id="inventoryGrid"></div>

<br>

<button onclick="showScreen('pause')">
BACK
</button>

</div>

</section>


<!-- ==========================================================
     GAME OVER
=========================================================== -->

<section id="gameover" class="screen hidden">

<div class="panel">

<h1>SHIP DESTROYED</h1>

<p id="gameOverText"></p>

<br>

<div class="menu-buttons">

<button onclick="continueGame()">
LOAD UNIVERSE
</button>

<button onclick="newGame()">
NEW UNIVERSE
</button>

<button onclick="showScreen('menu')">
MAIN MENU
</button>

</div>

</div>

</section>


<!-- ==========================================================
     HUD
=========================================================== -->

<div id="hud" class="hidden">

<div class="topbar">

<div class="hudbox">

<div class="hud-title">
SECTOR
</div>

<div id="sectorText" class="hud-value">
0 : 0
</div>

</div>


<div class="hudbox">

<div class="hud-title">
SYSTEM
</div>

<div id="systemText" class="hud-value">
UNKNOWN
</div>

</div>


<div class="hudbox">

<div class="hud-title">
CREDITS
</div>

<div id="creditsText" class="hud-value">
0
</div>

</div>


<canvas id="minimap"></canvas>

</div>


<div id="eventText"></div>

<div id="crosshair"></div>


<div class="bottomHud">

<div class="info">

<div>
HULL
</div>

<div class="bar">
<div id="hullBar"></div>
</div>


<div style="margin-top:6px">
SHIELD
</div>

<div class="bar">
<div id="shieldBar"></div>
</div>


<div style="margin-top:6px">
ENERGY
</div>

<div class="bar">
<div id="energyBar"></div>
</div>


<div style="margin-top:6px">
XP
</div>

<div class="bar">
<div id="xpBar"></div>
</div>

</div>


<div class="info">

<div id="weaponText">
PULSE CANNON
</div>

<div id="levelText">
LEVEL 1
</div>

<div id="objectiveText">
EXPLORE
</div>

</div>

</div>


<!-- ========================================================
     MOBILE CONTROLS
========================================================= -->

<div id="mobileControls">

<div
class="joystick"
id="joystick"
>

<div
class="stick"
id="stick"
></div>

</div>


<div class="mobileButtons">

<button id="fireBtn">
FIRE
</button>

<button id="boostBtn">
BOOST
</button>

</div>

</div>

</div>

</div>


<script>

/* ============================================================
   CANVAS
============================================================ */

const canvas =
    document.getElementById("game");

const ctx =
    canvas.getContext("2d");

const minimap =
    document.getElementById("minimap");

const mctx =
    minimap.getContext("2d");

let W=innerWidth;
let H=innerHeight;

function resize(){

    W=canvas.width=innerWidth;
    H=canvas.height=innerHeight;

    minimap.width=
        minimap.clientWidth *
        devicePixelRatio;

    minimap.height=
        minimap.clientHeight *
        devicePixelRatio;
}

addEventListener(
    "resize",
    resize
);

resize();


/* ============================================================
   SEEDED RANDOM
============================================================ */

function hashString(str){

    let h=2166136261;

    for(let i=0;i<str.length;i++){

        h ^= str.charCodeAt(i);

        h +=
            (h<<1)+
            (h<<4)+
            (h<<7)+
            (h<<8)+
            (h<<24);
    }

    return h>>>0;
}

function RNG(seed){

    let state=
        hashString(String(seed)) || 1;

    return function(){

        state +=
            0x6D2B79F5;

        let t=state;

        t=
            Math.imul(
                t^t>>>15,
                t|1
            );

        t ^=
            t+
            Math.imul(
                t^t>>>7,
                t|61
            );

        return(
            (t^t>>>14)>>>0
        )/4294967296;
    };
}

function pick(rng,array){

    return array[
        Math.floor(
            rng()*array.length
        )
    ];
}


/* ============================================================
   WORLD
============================================================ */

let worldSeed="VOID-829174";

const CHUNK_SIZE=5000;

let currentChunk={
    x:999999,
    y:999999
};

let currentSystem=null;

let structures=[];

let stars=[];


/* ============================================================
   PLAYER
============================================================ */

let player={

    x:0,
    y:0,

    vx:0,
    vy:0,

    // Current visual facing
    angle:0,

    // Target facing
    targetAngle:0,

    rotationSpeed:.18,

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


/* ============================================================
   GAME STATE
============================================================ */

let gameRunning=false;
let paused=false;

let camera={
    x:0,
    y:0
};

let bullets=[];
let enemyBullets=[];
let enemies=[];
let particles=[];
let pickups=[];

let keys={};

let mouse={
    x:W/2,
    y:H/2,
    down:false
};

let mobile={
    x:0,
    y:0,
    fire:false,
    boost:false
};


/* ============================================================
   SECTOR GENERATOR
============================================================ */

function sectorSeed(x,y){

    return (
        worldSeed+
        ":sector:"+
        x+
        ":"+
        y
    );
}

function generateSector(x,y){

    const rng=
        RNG(
            sectorSeed(x,y)
        );

    const biomes=[
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

    const starTypes=[
        "blue",
        "yellow",
        "red",
        "white",
        "neutron"
    ];

    const names=[
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
    ];

    const factions=[
        "miners",
        "federation",
        "pirates",
        "aliens",
        "neutral"
    ];

    const specials=[
        "distress_signal",
        "ancient_signal",
        "pirate_patrol",
        "merchant_convoy",
        "derelict",
        "resource_rush",
        "none"
    ];

    let sector={

        x:x,
        y:y,

        biome:
            pick(rng,biomes),

        danger:
            1+
            Math.floor(
                rng()*10
            ),

        systemName:
            pick(rng,names)+
            "-"+
            Math.floor(
                rng()*999
            ),

        star:
            pick(rng,starTypes),

        faction:
            pick(rng,factions),

        special:
            pick(rng,specials),

        planets:[],
        structures:[],
        resources:[]
    };


    /* ========================================================
       PLANETS
    ======================================================== */

    const planetTypes=[
        "rocky",
        "ice",
        "gas",
        "ocean",
        "lava",
        "dead"
    ];

    let planetCount=
        1+
        Math.floor(
            rng()*6
        );

    for(let i=0;i<planetCount;i++){

        sector.planets.push({

            name:
                String.fromCharCode(
                    65+i
                )+
                "-"+
                Math.floor(
                    rng()*99
                ),

            type:
                pick(
                    rng,
                    planetTypes
                ),

            radius:
                15+
                rng()*35,

            orbit:
                180+
                rng()*520
        });
    }


    /* ========================================================
       STRUCTURES
    ======================================================== */

    const structureTypes=[
        "station",
        "wreck",
        "mining_colony",
        "pirate_base",
        "alien_ruin",
        "research_outpost"
    ];

    let structureCount=
        Math.floor(
            rng()*6
        );

    for(let i=0;i<structureCount;i++){

        sector.structures.push({

            type:
                pick(
                    rng,
                    structureTypes
                ),

            x:
                -1800+
                rng()*3600,

            y:
                -1800+
                rng()*3600,

            visited:false
        });
    }


    /* ========================================================
       RESOURCES
    ======================================================== */

    const resourceTypes=[
        "iron",
        "crystal",
        "alien"
    ];

    let resourceCount=
        5+
        Math.floor(
            rng()*16
        );

    for(let i=0;i<resourceCount;i++){

        sector.resources.push({

            type:
                pick(
                    rng,
                    resourceTypes
                ),

            x:
                -2500+
                rng()*5000,

            y:
                -2500+
                rng()*5000,

            amount:
                1+
                Math.floor(
                    rng()*8
                )
        });
    }

    return sector;
}


/* ============================================================
   LOAD CHUNK
============================================================ */

function loadChunk(x,y){

    if(
        currentChunk.x===x &&
        currentChunk.y===y
    ){
        return;
    }

    currentChunk={
        x:x,
        y:y
    };

    currentSystem=
        generateSector(
            x,
            y
        );

    structures=
        currentSystem.structures.map(
            s=>({...s})
        );

    document.getElementById(
        "sectorText"
    ).textContent=
        `${x} : ${y}`;

    document.getElementById(
        "systemText"
    ).textContent=
        currentSystem.systemName;

    document.getElementById(
        "objectiveText"
    ).textContent=
        getObjective(
            currentSystem
        );

    showEvent(
        `${currentSystem.systemName} • `+
        `${currentSystem.biome.replaceAll("_"," ").toUpperCase()}`
    );
}

function getObjective(s){

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
   STARS
============================================================ */

function buildStars(){

    stars=[];

    const rng=
        RNG(
            worldSeed+
            ":stars"
        );

    for(let i=0;i<1000;i++){

        stars.push({

            x:
                -10000+
                rng()*20000,

            y:
                -10000+
                rng()*20000,

            size:
                .4+
                rng()*2,

            alpha:
                .2+
                rng()*.8,

            depth:
                .1+
                rng()*.8
        });
    }
}


/* ============================================================
   ENEMY TYPES
============================================================ */

const ENEMY_TYPES={

    scout:{
        hp:35,
        speed:2.4,
        size:12,
        damage:8,
        color:"#87aaff",
        score:20
    },

    fighter:{
        hp:70,
        speed:1.8,
        size:17,
        damage:12,
        color:"#ff5967",
        score:40
    },

    interceptor:{
        hp:55,
        speed:3.1,
        size:14,
        damage:16,
        color:"#ff9c55",
        score:55
    },

    sniper:{
        hp:100,
        speed:.9,
        size:19,
        damage:28,
        color:"#ffdc67",
        score:120
    },

    bomber:{
        hp:140,
        speed:1,
        size:23,
        damage:35,
        color:"#ff4d9e",
        score:140
    },

    tank:{
        hp:280,
        speed:.65,
        size:31,
        damage:25,
        color:"#a15cff",
        score:180
    },

    swarm:{
        hp:22,
        speed:3.6,
        size:8,
        damage:6,
        color:"#d6ff70",
        score:15
    },

    elite:{
        hp:500,
        speed:1.4,
        size:38,
        damage:35,
        color:"#ff35e8",
        score:500
    },

    guardian:{
        hp:1100,
        speed:.7,
        size:62,
        damage:50,
        color:"#5fe8ff",
        score:1500
    }
};


/* ============================================================
   ENEMY GENERATION
============================================================ */

function chooseEnemy(){

    let danger=
        currentSystem
        ? currentSystem.danger
        : 1;

    let types=[
        "scout",
        "fighter",
        "interceptor"
    ];

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

    return pick(
        RNG(
            worldSeed+
            ":"+
            currentChunk.x+
            ":"+
            currentChunk.y+
            ":"+
            Math.floor(
                Math.random()*100000
            )
        ),
        types
    );
}

function spawnEnemy(type){

    type=
        type ||
        chooseEnemy();

    const d=
        ENEMY_TYPES[type];

    const a=
        Math.random()*
        Math.PI*2;

    const distance=
        Math.max(W,H)*.8+
        Math.random()*700;

    enemies.push({

        type:type,

        x:
            player.x+
            Math.cos(a)*
            distance,

        y:
            player.y+
            Math.sin(a)*
            distance,

        vx:0,
        vy:0,

        hp:d.hp,
        maxHp:d.hp,

        speed:d.speed,
        size:d.size,
        damage:d.damage,

        color:d.color,

        score:d.score,

        phase:
            Math.random()*
            Math.PI*2,

        shoot:
            60+
            Math.random()*120
    });
}


/* ============================================================
   BOSS
============================================================ */

function spawnBoss(){

    const type=
        Math.random()<.5
        ?"guardian"
        :"elite";

    const d=
        ENEMY_TYPES[type];

    let hp=
        d.hp+
        player.level*200;

    enemies.push({

        type:type,

        boss:true,

        x:
            player.x+
            1000,

        y:
            player.y,

        vx:0,
        vy:0,

        hp:hp,
        maxHp:hp,

        speed:d.speed,
        size:d.size,

        damage:d.damage,

        color:d.color,

        score:d.score,

        phase:0,

        shoot:20
    });

    showEvent(
        "⚠ BOSS DETECTED ⚠"
    );
}


/* ============================================================
   PLAYER AIM
============================================================ */

function updateAim(){

    const worldMouseX=
        camera.x+
        mouse.x-
        W/2;

    const worldMouseY=
        camera.y+
        mouse.y-
        H/2;

    player.targetAngle=
        Math.atan2(
            worldMouseY-player.y,
            worldMouseX-player.x
        );

    let difference=
        player.targetAngle-
        player.angle;

    while(
        difference >
        Math.PI
    )
        difference-=
            Math.PI*2;

    while(
        difference <
        -Math.PI
    )
        difference+=
            Math.PI*2;

    /*
       Smooth spaceship rotation.
       The ship now physically turns toward
       the mouse instead of instantly snapping.
    */

    player.angle +=
        difference *
        player.rotationSpeed;
}


/* ============================================================
   PLAYER UPDATE
============================================================ */

function updatePlayer(){

    let dx=0;
    let dy=0;

    if(
        keys["w"] ||
        keys["arrowup"]
    )
        dy--;

    if(
        keys["s"] ||
        keys["arrowdown"]
    )
        dy++;

    if(
        keys["a"] ||
        keys["arrowleft"]
    )
        dx--;

    if(
        keys["d"] ||
        keys["arrowright"]
    )
        dx++;

    dx+=mobile.x;
    dy+=mobile.y;

    let len=
        Math.hypot(dx,dy);

    if(len>1){

        dx/=len;
        dy/=len;
    }

    let boosting=
        keys["shift"] ||
        mobile.boost;

    let acceleration=
        boosting
        ? .55
        : .28;

    let maxSpeed=
        boosting
        ? 11
        : 6;

    player.vx+=
        dx*
        acceleration;

    player.vy+=
        dy*
        acceleration;

    player.vx*=.94;
    player.vy*=.94;

    let speed=
        Math.hypot(
            player.vx,
            player.vy
        );

    if(speed>maxSpeed){

        player.vx=
            player.vx/
            speed*
            maxSpeed;

        player.vy=
            player.vy/
            speed*
            maxSpeed;
    }

    player.x+=player.vx;
    player.y+=player.vy;


    // IMPORTANT:
    // Ship rotates independently from movement.

    updateAim();


    // Fire

    if(
        mouse.down ||
        keys[" "] ||
        mobile.fire
    )
        shoot();


    // Energy

    player.energy=
        Math.min(
            player.maxEnergy,
            player.energy+.35
        );


    // Shield recharge

    if(
        player.shield<
        player.maxShield
    )
        player.shield+=.035;


    // Chunk

    let chunk=
        chunkFromPosition(
            player.x,
            player.y
        );

    loadChunk(
        chunk.x,
        chunk.y
    );
}


/* ============================================================
   CHUNK COORDINATES
============================================================ */

function chunkFromPosition(x,y){

    return {

        x:
            Math.floor(
                x/CHUNK_SIZE
            ),

        y:
            Math.floor(
                y/CHUNK_SIZE
            )
    };
}


/* ============================================================
   SHOOTING
============================================================ */

function shoot(){

    if(
        !gameRunning ||
        paused
    )
        return;

    if(player.energy<=0)
        return;

    let angle=
        player.angle;

    if(
        player.weapon===
        "spread"
    ){

        player.energy-=1.5;

        [-.28,0,.28].forEach(
            offset=>{

                createBullet(
                    angle+offset,
                    11,
                    12,
                    4
                );
            }
        );

    }else{

        let cost=1;

        let speed=12;

        let damage=12;

        let size=4;

        if(player.weapon==="laser"){

            cost=.7;
            speed=18;
            damage=18;
            size=3;
        }

        if(player.weapon==="missile"){

            cost=4;
            speed=7;
            damage=35;
            size=7;
        }

        if(player.weapon==="plasma"){

            cost=3;
            speed=9;
            damage=30;
            size=8;
        }

        player.energy-=cost;

        createBullet(
            angle,
            speed,
            damage,
            size
        );
    }

    createMuzzle();
}

function createBullet(
    angle,
    speed,
    damage,
    size
){

    bullets.push({

        x:
            player.x+
            Math.cos(angle)*
            32,

        y:
            player.y+
            Math.sin(angle)*
            32,

        vx:
            Math.cos(angle)*
            speed,

        vy:
            Math.sin(angle)*
            speed,

        damage:damage,

        size:size,

        life:120
    });
}


/* ============================================================
   ENEMY UPDATE
============================================================ */

function updateEnemies(){

    for(
        let i=enemies.length-1;
        i>=0;
        i--
    ){

        const e=
            enemies[i];

        let dx=
            player.x-
            e.x;

        let dy=
            player.y-
            e.y;

        let dist=
            Math.hypot(dx,dy) ||
            1;

        let nx=dx/dist;
        let ny=dy/dist;

        e.phase+=.03;

        let strafe=
            Math.sin(
                e.phase
            );

        e.vx+=
            nx*
            e.speed*
            .035+
            -ny*
            strafe*
            .025;

        e.vy+=
            ny*
            e.speed*
            .035+
            nx*
            strafe*
            .025;

        e.vx*=.96;
        e.vy*=.96;

        e.x+=e.vx;
        e.y+=e.vy;

        e.shoot--;

        if(e.shoot<=0){

            enemyShoot(e);

            e.shoot=
                e.boss
                ? 35
                : 80+
                  Math.random()*100;
        }

        if(
            dist<
            e.size+20
        ){

            damagePlayer(
                e.damage*.025
            );
        }

        if(e.hp<=0){

            destroyEnemy(
                i,
                e
            );
        }
    }


    /*
       Procedural ambient encounters.
       There is no traditional Wave 1/2/3 loop.
    */

    if(enemies.length<2){

        let chance=
            .0015+
            (
                currentSystem
                ?currentSystem.danger
                :1
            )*.0008;

        if(
            Math.random()<
            chance
        )
            spawnEnemy();
    }
}


/* ============================================================
   ENEMY SHOOTING
============================================================ */

function enemyShoot(e){

    let angle=
        Math.atan2(
            player.y-e.y,
            player.x-e.x
        );

    if(e.boss){

        for(
            let i=0;
            i<7;
            i++
        ){

            let a=
                angle+
                (
                    i-3
                )*.15;

            enemyBullets.push({

                x:e.x,
                y:e.y,

                vx:
                    Math.cos(a)*5,

                vy:
                    Math.sin(a)*5,

                damage:13,

                size:6,

                life:200
            });
        }

    }else{

        enemyBullets.push({

            x:e.x,
            y:e.y,

            vx:
                Math.cos(angle)*4,

            vy:
                Math.sin(angle)*4,

            damage:e.damage,

            size:4,

            life:180
        });
    }
}


/* ============================================================
   BULLETS
============================================================ */

function updateBullets(){

    for(
        let i=bullets.length-1;
        i>=0;
        i--
    ){

        const b=
            bullets[i];

        b.x+=b.vx;
        b.y+=b.vy;

        b.life--;

        let hit=false;

        for(
            let j=enemies.length-1;
            j>=0;
            j--
        ){

            const e=
                enemies[j];

            if(
                Math.hypot(
                    b.x-e.x,
                    b.y-e.y
                )<
                b.size+
                e.size
            ){

                e.hp-=
                    b.damage;

                explosion(
                    b.x,
                    b.y,
                    "#ffffff",
                    3
                );

                hit=true;

                if(e.hp<=0)
                    destroyEnemy(
                        j,
                        e
                    );

                break;
            }
        }

        if(
            hit ||
            b.life<=0
        )
            bullets.splice(
                i,
                1
            );
    }
}

function updateEnemyBullets(){

    for(
        let i=
            enemyBullets.length-1;
        i>=0;
        i--
    ){

        const b=
            enemyBullets[i];

        b.x+=b.vx;
        b.y+=b.vy;

        b.life--;

        if(
            Math.hypot(
                b.x-player.x,
                b.y-player.y
            )<
            b.size+17
        ){

            damagePlayer(
                b.damage
            );

            explosion(
                b.x,
                b.y,
                "#ff5868",
                5
            );

            enemyBullets.splice(
                i,
                1
            );

        }else if(
            b.life<=0
        ){

            enemyBullets.splice(
                i,
                1
            );
        }
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

        player.shield-=
            absorbed;

        amount-=
            absorbed;
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

function destroyEnemy(
    index,
    e
){

    enemies.splice(
        index,
        1
    );

    player.kills++;

    player.xp+=
        e.score*.5;

    player.credits+=
        Math.floor(
            e.score*.5+
            Math.random()*30
        );

    explosion(
        e.x,
        e.y,
        e.color,
        e.boss?80:25
    );

    if(
        Math.random()<.25
    ){

        pickups.push({

            x:e.x,
            y:e.y,

            type:
                Math.random()<.5
                ?"shield"
                :"energy"
        });
    }

    if(e.boss){

        showEvent(
            "BOSS DESTROYED"
        );

        player.credits+=1000;
    }

    checkLevel();
}


/* ============================================================
   LEVEL
============================================================ */

function checkLevel(){

    let required=
        100+
        (
            player.level-1
        )*100;

    while(
        player.xp>=required
    ){

        player.xp-=
            required;

        player.level++;

        player.maxHull+=10;
        player.hull=
            player.maxHull;

        player.maxShield+=10;
        player.shield=
            player.maxShield;

        player.maxEnergy+=5;
        player.energy=
            player.maxEnergy;

        showEvent(
            "LEVEL UP • SHIP UPGRADED"
        );

        required=
            100+
            (
                player.level-1
            )*100;
    }
}


/* ============================================================
   RESOURCES
============================================================ */

function updateResources(){

    if(!currentSystem)
        return;

    for(
        let i=
            currentSystem.resources.length-1;
        i>=0;
        i--
    ){

        const r=
            currentSystem.resources[i];

        let rx=
            r.x+
            currentChunk.x*
            CHUNK_SIZE;

        let ry=
            r.y+
            currentChunk.y*
            CHUNK_SIZE;

        let d=
            Math.hypot(
                rx-player.x,
                ry-player.y
            );

        if(d<35){

            player.inventory[
                r.type
            ]+=r.amount;

            showEvent(
                `COLLECTED ${
                    r.type.toUpperCase()
                } × ${r.amount}`
            );

            currentSystem.resources.splice(
                i,
                1
            );
        }
    }
}


/* ============================================================
   STRUCTURES
============================================================ */

function updateStructures(){

    for(
        const s of structures
    ){

        let sx=
            s.x+
            currentChunk.x*
            CHUNK_SIZE;

        let sy=
            s.y+
            currentChunk.y*
            CHUNK_SIZE;

        let d=
            Math.hypot(
                sx-player.x,
                sy-player.y
            );

        if(
            d<110 &&
            !s.visited
        ){

            s.visited=true;

            discoverStructure(
                s
            );
        }
    }
}

function discoverStructure(s){

    let text="";

    switch(s.type){

        case "station":

            player.credits+=100;

            text=
                "SPACE STATION DISCOVERED • +100 CREDITS";

            break;

        case "wreck":

            player.inventory.iron+=5;

            text=
                "WRECK SALVAGED • +5 IRON";

            break;

        case "mining_colony":

            player.reputation.miners+=5;

            text=
                "MINING COLONY DISCOVERED • MINER REP +5";

            break;

        case "pirate_base":

            player.reputation.pirates-=5;

            text=
                "PIRATE BASE • HOSTILE TERRITORY";

            break;

        case "alien_ruin":

            player.inventory.alien+=3;

            player.reputation.aliens+=5;

            text=
                "ANCIENT ALIEN RUINS DISCOVERED";

            break;

        default:

            text=
                "RESEARCH OUTPOST DISCOVERED";
    }

    player.discovered.push(
        `${currentChunk.x}:`+
        `${currentChunk.y}:`+
        `${s.type}`
    );

    showEvent(text);
}


/* ============================================================
   PICKUPS
============================================================ */

function updatePickups(){

    for(
        let i=pickups.length-1;
        i>=0;
        i--
    ){

        const p=
            pickups[i];

        let dx=
            player.x-p.x;

        let dy=
            player.y-p.y;

        let d=
            Math.hypot(
                dx,
                dy
            )||1;

        if(d<120){

            p.x+=
                dx/d*2;

            p.y+=
                dy/d*2;
        }

        if(d<25){

            if(
                p.type==="shield"
            ){

                player.shield=
                    Math.min(
                        player.maxShield,
                        player.shield+40
                    );
            }

            if(
                p.type==="energy"
            ){

                player.energy=
                    Math.min(
                        player.maxEnergy,
                        player.energy+50
                    );
            }

            showEvent(
                p.type.toUpperCase()+
                " RECOVERED"
            );

            pickups.splice(
                i,
                1
            );
        }
    }
}


/* ============================================================
   PARTICLES
============================================================ */

function explosion(
    x,
    y,
    color,
    count
){

    for(
        let i=0;
        i<count;
        i++
    ){

        let a=
            Math.random()*
            Math.PI*2;

        let speed=
            1+
            Math.random()*6;

        particles.push({

            x:x,
            y:y,

            vx:
                Math.cos(a)*
                speed,

            vy:
                Math.sin(a)*
                speed,

            life:
                25+
                Math.random()*40,

            size:
                1+
                Math.random()*4,

            color:color
        });
    }
}

function createMuzzle(){

    explosion(

        player.x+
        Math.cos(
            player.angle
        )*30,

        player.y+
        Math.sin(
            player.angle
        )*30,

        "#b8d6ff",

        4
    );
}

function updateParticles(){

    for(
        let i=particles.length-1;
        i>=0;
        i--
    ){

        const p=
            particles[i];

        p.x+=p.vx;
        p.y+=p.vy;

        p.vx*=.96;
        p.vy*=.96;

        p.life--;

        if(p.life<=0)
            particles.splice(
                i,
                1
            );
    }
}


/* ============================================================
   CAMERA
============================================================ */

function updateCamera(){

    camera.x+=
        (
            player.x-
            camera.x
        )*.12;

    camera.y+=
        (
            player.y-
            camera.y
        )*.12;
}


/* ============================================================
   WORLD -> SCREEN
============================================================ */

function worldToScreen(
    x,
    y
){

    return {

        x:
            x-
            camera.x+
            W/2,

        y:
            y-
            camera.y+
            H/2
    };
}


/* ============================================================
   DRAW BACKGROUND
============================================================ */

function drawBackground(){

    ctx.fillStyle="#02030a";

    ctx.fillRect(
        0,
        0,
        W,
        H
    );

    for(
        const s of stars
    ){

        let x=
            (
                s.x-
                camera.x*
                s.depth
            )%W;

        let y=
            (
                s.y-
                camera.y*
                s.depth
            )%H;

        if(x<0)
            x+=W;

        if(y<0)
            y+=H;

        ctx.globalAlpha=
            s.alpha;

        ctx.fillStyle=
            "#dce7ff";

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

    if(
        currentSystem.biome===
        "nebula"
    ){

        let gradient=
            ctx.createRadialGradient(
                W*.7,
                H*.3,
                50,
                W*.7,
                H*.3,
                W*.7
            );

        gradient.addColorStop(
            0,
            "rgba(100,50,190,.14)"
        );

        gradient.addColorStop(
            1,
            "rgba(0,0,0,0)"
        );

        ctx.fillStyle=
            gradient;

        ctx.fillRect(
            0,
            0,
            W,
            H
        );
    }

    if(
        currentSystem.biome===
        "gravity_rift"
    ){

        ctx.strokeStyle=
            "rgba(100,180,255,.08)";

        for(
            let i=0;
            i<20;
            i++
        ){

            ctx.beginPath();

            ctx.arc(
                W/2,
                H/2,
                100+i*50+
                Math.sin(
                    performance.now()*.001+i
                )*15,
                0,
                Math.PI*2
            );

            ctx.stroke();
        }
    }
}


/* ============================================================
   DRAW STRUCTURES
============================================================ */

function drawStructures(){

    if(!currentSystem)
        return;

    for(
        const s of structures
    ){

        let x=
            s.x+
            currentChunk.x*
            CHUNK_SIZE;

        let y=
            s.y+
            currentChunk.y*
            CHUNK_SIZE;

        let p=
            worldToScreen(
                x,
                y
            );

        if(
            p.x<-100 ||
            p.x>W+100 ||
            p.y<-100 ||
            p.y>H+100
        )
            continue;

        ctx.save();

        ctx.translate(
            p.x,
            p.y
        );

        ctx.fillStyle=
            s.visited
            ?"rgba(100,110,140,.4)"
            :"#728cff";

        ctx.strokeStyle=
            "#b8c8ff";

        ctx.lineWidth=1.5;

        if(
            s.type===
            "station"
        ){

            ctx.fillRect(
                -30,
                -18,
                60,
                36
            );

            ctx.strokeRect(
                -30,
                -18,
                60,
                36
            );

        }else if(
            s.type===
            "wreck"
        ){

            ctx.rotate(.4);

            ctx.fillRect(
                -25,
                -9,
                50,
                18
            );

            ctx.strokeRect(
                -25,
                -9,
                50,
                18
            );

        }else{

            ctx.beginPath();

            ctx.moveTo(
                0,
                -25
            );

            ctx.lineTo(
                25,
                20
            );

            ctx.lineTo(
                -25,
                20
            );

            ctx.closePath();

            ctx.fill();
            ctx.stroke();
        }

        ctx.restore();
    }
}


/* ============================================================
   DRAW PLAYER
============================================================ */

function drawPlayer(){

    const s=
        worldToScreen(
            player.x,
            player.y
        );

    ctx.save();

    ctx.translate(
        s.x,
        s.y
    );

    /*
       THIS IS THE SHIP ROTATION.

       player.angle is continuously updated
       toward the mouse position.
    */

    ctx.rotate(
        player.angle
    );


    /* ========================================================
       ENGINE FLAME
    ======================================================== */

    let moving=
        Math.hypot(
            player.vx,
            player.vy
        )>.35;

    if(moving){

        let boosting=
            keys["shift"] ||
            mobile.boost;

        let flameLength=
            boosting
            ?42
            :25;

        let pulse=
            Math.sin(
                performance.now()*.03
            )*4;

        ctx.beginPath();

        ctx.moveTo(
            -10,
            0
        );

        ctx.lineTo(
            -flameLength-pulse,
            -7
        );

        ctx.lineTo(
            -flameLength-pulse,
            7
        );

        ctx.closePath();

        ctx.fillStyle=
            boosting
            ?"white"
            :"#65aaff";

        ctx.shadowBlur=
            boosting
            ?25
            :15;

        ctx.shadowColor=
            "#66aaff";

        ctx.fill();

        ctx.shadowBlur=0;
    }


    /* ========================================================
       SHIP MAIN BODY
    ======================================================== */

    ctx.beginPath();

    ctx.moveTo(
        32,
        0
    );

    ctx.lineTo(
        7,
        -11
    );

    ctx.lineTo(
        -13,
        -17
    );

    ctx.lineTo(
        -9,
        0
    );

    ctx.lineTo(
        -13,
        17
    );

    ctx.lineTo(
        7,
        11
    );

    ctx.closePath();

    ctx.fillStyle=
        "#e1eaff";

    ctx.fill();

    ctx.strokeStyle=
        "#78a8ff";

    ctx.lineWidth=2;

    ctx.stroke();


    /* ========================================================
       UPPER WING
    ======================================================== */

    ctx.beginPath();

    ctx.moveTo(
        0,
        -8
    );

    ctx.lineTo(
        -17,
        -25
    );

    ctx.lineTo(
        -22,
        -18
    );

    ctx.lineTo(
        -10,
        -3
    );

    ctx.closePath();

    ctx.fillStyle=
        "#718ab5";

    ctx.fill();


    /* ========================================================
       LOWER WING
    ======================================================== */

    ctx.beginPath();

    ctx.moveTo(
        0,
        8
    );

    ctx.lineTo(
        -17,
        25
    );

    ctx.lineTo(
        -22,
        18
    );

    ctx.lineTo(
        -10,
        3
    );

    ctx.closePath();

    ctx.fillStyle=
        "#718ab5";

    ctx.fill();


    /* ========================================================
       COCKPIT
    ======================================================== */

    ctx.beginPath();

    ctx.ellipse(
        8,
        0,
        9,
        5,
        0,
        0,
        Math.PI*2
    );

    ctx.fillStyle=
        "#3d6da8";

    ctx.fill();

    ctx.strokeStyle=
        "#c2dcff";

    ctx.stroke();


    /* ========================================================
       SHIELD
    ======================================================== */

    if(
        player.shield>0
    ){

        let alpha=
            .12+
            (
                player.shield/
                player.maxShield
            )*.28;

        ctx.beginPath();

        ctx.arc(
            0,
            0,
            34,
            0,
            Math.PI*2
        );

        ctx.strokeStyle=
            `rgba(80,170,255,${alpha})`;

        ctx.lineWidth=2;

        ctx.shadowBlur=15;

        ctx.shadowColor=
            "#4b9fff";

        ctx.stroke();

        ctx.shadowBlur=0;
    }

    ctx.restore();
}


/* ============================================================
   DRAW ENEMIES
============================================================ */

function drawEnemies(){

    for(
        const e of enemies
    ){

        const s=
            worldToScreen(
                e.x,
                e.y
            );

        ctx.save();

        ctx.translate(
            s.x,
            s.y
        );

        let angle=
            Math.atan2(
                player.y-e.y,
                player.x-e.x
            );

        ctx.rotate(angle);

        ctx.beginPath();

        ctx.moveTo(
            e.size,
            0
        );

        ctx.lineTo(
            -e.size,
            -e.size*.65
        );

        ctx.lineTo(
            -e.size*.6,
            0
        );

        ctx.lineTo(
            -e.size,
            e.size*.65
        );

        ctx.closePath();

        ctx.fillStyle=
            e.color;

        ctx.fill();

        ctx.strokeStyle=
            "rgba(255,255,255,.6)";

        ctx.stroke();

        ctx.restore();


        /* HEALTH BAR */

        if(
            e.hp<
            e.maxHp
        ){

            let width=
                e.size*2.5;

            ctx.fillStyle=
                "#10131d";

            ctx.fillRect(
                s.x-width/2,
                s.y-e.size-9,
                width,
                4
            );

            ctx.fillStyle=
                "#ff4f61";

            ctx.fillRect(
                s.x-width/2,
                s.y-e.size-9,
                width*
                Math.max(
                    0,
                    e.hp/e.maxHp
                ),
                4
            );
        }
    }
}


/* ============================================================
   DRAW BULLETS
============================================================ */

function drawBullets(){

    for(
        const b of bullets
    ){

        const s=
            worldToScreen(
                b.x,
                b.y
            );

        ctx.fillStyle=
            "#c4ddff";

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

    for(
        const b of enemyBullets
    ){

        const s=
            worldToScreen(
                b.x,
                b.y
            );

        ctx.fillStyle=
            "#ff5b68";

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


/* ============================================================
   DRAW PICKUPS
============================================================ */

function drawPickups(){

    for(
        const p of pickups
    ){

        const s=
            worldToScreen(
                p.x,
                p.y
            );

        ctx.fillStyle=
            p.type===
            "shield"
            ?" #65b9ff"
            :"#c96bff";

        ctx.beginPath();

        ctx.arc(
            s.x,
            s.y,
            8+
            Math.sin(
                performance.now()*.01
            )*2,
            0,
            Math.PI*2
        );

        ctx.fill();
    }
}


/* ============================================================
   DRAW PARTICLES
============================================================ */

function drawParticles(){

    for(
        const p of particles
    ){

        const s=
            worldToScreen(
                p.x,
                p.y
            );

        ctx.globalAlpha=
            Math.max(
                0,
                p.life/60
            );

        ctx.fillStyle=
            p.color;

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


/* ============================================================
   MINIMAP
============================================================ */

function drawMinimap(){

    const w=
        minimap.width;

    const h=
        minimap.height;

    mctx.clearRect(
        0,
        0,
        w,
        h
    );

    mctx.fillStyle=
        "#02050d";

    mctx.fillRect(
        0,
        0,
        w,
        h
    );


    /* Grid */

    mctx.strokeStyle=
        "rgba(100,140,255,.15)";

    for(
        let i=-4;
        i<=4;
        i++
    ){

        mctx.beginPath();

        mctx.moveTo(
            w/2+
            i*20,
            0
        );

        mctx.lineTo(
            w/2+
            i*20,
            h
        );

        mctx.stroke();

        mctx.beginPath();

        mctx.moveTo(
            0,
            h/2+
            i*20
        );

        mctx.lineTo(
            w,
            h/2+
            i*20
        );

        mctx.stroke();
    }


    /* Player */

    mctx.fillStyle=
        "white";

    mctx.beginPath();

    mctx.arc(
        w/2,
        h/2,
        4,
        0,
        Math.PI*2
    );

    mctx.fill();


    /* Enemies */

    mctx.fillStyle=
        "#ff5968";

    for(
        const e of enemies
    ){

        let dx=
            (
                e.x-
                player.x
            )/30;

        let dy=
            (
                e.y-
                player.y
            )/30;

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


    /* Structures */

    mctx.fillStyle=
        "#728cff";

    for(
        const s of structures
    ){

        let sx=
            s.x+
            currentChunk.x*
            CHUNK_SIZE;

        let sy=
            s.y+
            currentChunk.y*
            CHUNK_SIZE;

        let dx=
            (sx-player.x)/30;

        let dy=
            (sy-player.y)/30;

        if(
            Math.abs(dx)<w/2 &&
            Math.abs(dy)<h/2
        ){

            mctx.fillRect(
                w/2+dx-2,
                h/2+dy-2,
                4,
                4
            );
        }
    }
}


/* ============================================================
   HUD
============================================================ */

function updateHUD(){

    document.getElementById(
        "hullBar"
    ).style.width=
        `${
            Math.max(
                0,
                player.hull/
                player.maxHull*
                100
            )
        }%`;

    document.getElementById(
        "shieldBar"
    ).style.width=
        `${
            Math.max(
                0,
                player.shield/
                player.maxShield*
                100
            )
        }%`;

    document.getElementById(
        "energyBar"
    ).style.width=
        `${
            Math.max(
                0,
                player.energy/
                player.maxEnergy*
                100
            )
        }%`;

    let required=
        100+
        (
            player.level-1
        )*100;

    document.getElementById(
        "xpBar"
    ).style.width=
        `${
            Math.min(
                100,
                player.xp/
                required*
                100
            )
        }%`;

    document.getElementById(
        "creditsText"
    ).textContent=
        player.credits;

    document.getElementById(
        "levelText"
    ).textContent=
        `LEVEL ${player.level}`;

    const weaponNames={

        pulse:
            "PULSE CANNON",

        spread:
            "SPREAD CANNON",

        laser:
            "LASER",

        missile:
            "MISSILE",

        plasma:
            "PLASMA"
    };

    document.getElementById(
        "weaponText"
    ).textContent=
        weaponNames[
            player.weapon
        ];
}


/* ============================================================
   MAIN LOOP
============================================================ */

function gameLoop(){

    requestAnimationFrame(
        gameLoop
    );

    if(
        !gameRunning ||
        paused
    )
        return;

    updatePlayer();

    updateEnemies();

    updateBullets();

    updateEnemyBullets();

    updateResources();

    updateStructures();

    updatePickups();

    updateParticles();

    updateCamera();


    drawBackground();

    drawStructures();

    drawPickups();

    drawBullets();

    drawEnemyBullets();

    drawEnemies();

    drawParticles();

    drawPlayer();


    drawMinimap();

    updateHUD();
}

gameLoop();


/* ============================================================
   UI FUNCTIONS
============================================================ */

function showScreen(id){

    document
        .querySelectorAll(".screen")
        .forEach(
            x=>
                x.classList.add(
                    "hidden"
                )
        );

    if(id){

        document
            .getElementById(id)
            .classList.remove(
                "hidden"
            );
    }

    if(
        id==="menu" ||
        id==="howto" ||
        id==="settings" ||
        id==="inventory" ||
        id==="pause" ||
        id==="gameover"
    ){

        if(
            id==="pause" ||
            id==="inventory"
        ){

            document
                .getElementById("hud")
                .classList.remove(
                    "hidden"
                );

        }else{

            document
                .getElementById("hud")
                .classList.add(
                    "hidden"
                );
        }
    }
}


/* ============================================================
   NEW GAME
============================================================ */

function newGame(){

    worldSeed=
        document
            .getElementById(
                "seedInput"
            )
            .value
            .trim();

    if(!worldSeed){

        worldSeed=
            "VOID-"+
            Math.floor(
                Math.random()*
                999999999
            );
    }

    player={

        x:0,
        y:0,

        vx:0,
        vy:0,

        angle:0,
        targetAngle:0,

        rotationSpeed:.18,

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

    localStorage.removeItem(
        "VOID_SPACE_SAVE"
    );

    buildStars();

    startGame();

    saveWorldState();

    showEvent(
        `NEW UNIVERSE • ${worldSeed}`
    );
}


/* ============================================================
   START GAME
============================================================ */

function startGame(){

    gameRunning=true;
    paused=false;

    document
        .querySelectorAll(".screen")
        .forEach(
            x=>
                x.classList.add(
                    "hidden"
                )
        );

    document
        .getElementById("hud")
        .classList.remove(
            "hidden"
        );

    buildStars();

    let c=
        chunkFromPosition(
            player.x,
            player.y
        );

    loadChunk(
        c.x,
        c.y
    );
}


/* ============================================================
   CONTINUE
============================================================ */

function continueGame(){

    let saved=
        localStorage.getItem(
            "VOID_SPACE_SAVE"
        );

    if(!saved){

        newGame();

        return;
    }

    try{

        let data=
            JSON.parse(saved);

        worldSeed=
            data.seed ||
            worldSeed;

        player=
            data.player ||
            player;

        startGame();

        showEvent(
            "UNIVERSE RESTORED"
        );

    }catch(error){

        newGame();
    }
}


/* ============================================================
   SAVE
============================================================ */

function saveWorldState(){

    try{

        localStorage.setItem(

            "VOID_SPACE_SAVE",

            JSON.stringify({

                seed:
                    worldSeed,

                player:
                    player,

                timestamp:
                    Date.now()
            })
        );

    }catch(error){}
}

function saveGame(){

    saveWorldState();

    showEvent(
        "UNIVERSE SAVED"
    );
}


/* ============================================================
   SEED
============================================================ */

function applySeed(){

    let value=
        document
            .getElementById(
                "seedInput"
            )
            .value
            .trim();

    if(value)
        worldSeed=value;

    showEvent(
        "SEED READY"
    );

    showScreen(
        "menu"
    );
}


/* ============================================================
   INVENTORY
============================================================ */

function showInventory(){

    let grid=
        document.getElementById(
            "inventoryGrid"
        );

    grid.innerHTML="";

    for(
        const key in player.inventory
    ){

        let div=
            document.createElement(
                "div"
            );

        div.className=
            "item";

        div.innerHTML=
            `<b>${key.toUpperCase()}</b>
             <span>${player.inventory[key]}</span>`;

        grid.appendChild(
            div
        );
    }

    showScreen(
        "inventory"
    );
}


/* ============================================================
   PAUSE
============================================================ */

function togglePause(){

    paused=!paused;

    if(paused){

        showScreen(
            "pause"
        );

    }else{

        document
            .querySelectorAll(".screen")
            .forEach(
                x=>
                    x.classList.add(
                        "hidden"
                    )
            );
    }
}


/* ============================================================
   GAME OVER
============================================================ */

function gameOver(){

    gameRunning=false;

    document.getElementById(
        "gameOverText"
    ).innerHTML=

        `LEVEL ${player.level}<br>
         KILLS ${player.kills}<br>
         CREDITS ${player.credits}<br>
         SECTOR ${currentChunk.x}:${currentChunk.y}`;

    saveWorldState();

    showScreen(
        "gameover"
    );
}


/* ============================================================
   EVENTS
============================================================ */

function showEvent(text){

    const el=
        document.getElementById(
            "eventText"
        );

    el.textContent=text;

    el.classList.add(
        "show"
    );

    clearTimeout(
        showEvent.timer
    );

    showEvent.timer=
        setTimeout(
            ()=>{
                el.classList.remove(
                    "show"
                );
            },
            3500
        );
}


/* ============================================================
   KEYBOARD
============================================================ */

addEventListener(
    "keydown",
    e=>{

        keys[
            e.key.toLowerCase()
        ]=true;

        if(
            e.key==="Escape" ||
            e.key.toLowerCase()==="p"
        ){

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
    }
);

addEventListener(
    "keyup",
    e=>{

        keys[
            e.key.toLowerCase()
        ]=false;
    }
);


/* ============================================================
   MOUSE
============================================================ */

canvas.addEventListener(
    "mousemove",
    e=>{

        mouse.x=e.clientX;
        mouse.y=e.clientY;

        const cross=
            document.getElementById(
                "crosshair"
            );

        cross.style.display=
            "block";

        cross.style.left=
            e.clientX+
            "px";

        cross.style.top=
            e.clientY+
            "px";
    }
);

canvas.addEventListener(
    "mousedown",
    e=>{

        if(e.button===0)
            mouse.down=true;
    }
);

addEventListener(
    "mouseup",
    e=>{

        if(e.button===0)
            mouse.down=false;
    }
);


/* ============================================================
   MOBILE JOYSTICK
============================================================ */

const joystick=
    document.getElementById(
        "joystick"
    );

const stick=
    document.getElementById(
        "stick"
    );

let joystickActive=false;

function joystickMove(e){

    const rect=
        joystick.getBoundingClientRect();

    const touch=
        e.touches[0];

    let x=
        touch.clientX-
        (
            rect.left+
            rect.width/2
        );

    let y=
        touch.clientY-
        (
            rect.top+
            rect.height/2
        );

    let distance=
        Math.hypot(
            x,
            y
        );

    let max=45;

    if(distance>max){

        x=
            x/distance*
            max;

        y=
            y/distance*
            max;
    }

    mobile.x=
        x/max;

    mobile.y=
        y/max;

    stick.style.transform=
        `translate(${x}px,${y}px)`;
}

joystick.addEventListener(
    "touchstart",
    e=>{

        joystickActive=true;

        joystickMove(e);
    },
    {
        passive:true
    }
);

joystick.addEventListener(
    "touchmove",
    e=>{

        if(joystickActive)
            joystickMove(e);
    },
    {
        passive:true
    }
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


/* ============================================================
   MOBILE FIRE
============================================================ */

const fireBtn=
    document.getElementById(
        "fireBtn"
    );

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


/* ============================================================
   MOBILE BOOST
============================================================ */

const boostBtn=
    document.getElementById(
        "boostBtn"
    );

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

document.getElementById(
    "seedInput"
).value=
    worldSeed;

buildStars();

showScreen(
    "menu"
);

</script>

</body>
</html>
"""


# ============================================================
# SERVER-SIDE DETERMINISTIC GENERATOR
# ============================================================

def deterministic_rng(seed):
    digest = hashlib.sha256(
        str(seed).encode("utf-8")
    ).hexdigest()

    number = int(
        digest[:16],
        16
    )

    return random.Random(number)


def generate_sector(seed, x, y):

    rng = deterministic_rng(
        f"{seed}:sector:{x}:{y}"
    )

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

    stars = [
        "blue",
        "yellow",
        "red",
        "white",
        "neutron"
    ]

    names = [
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

        "biome":
            rng.choice(
                biomes
            ),

        "danger":
            rng.randint(
                1,
                10
            ),

        "system_name":
            rng.choice(names)+
            "-"+
            str(
                rng.randint(
                    100,
                    999
                )
            ),

        "star":
            rng.choice(
                stars
            ),

        "faction":
            rng.choice(
                factions
            ),

        "special":
            rng.choice(
                specials
            ),

        "planets":[],
        "structures":[],
        "resources":[]
    }


    # ========================================================
    # PLANETS
    # ========================================================

    planet_types = [
        "rocky",
        "ice",
        "gas",
        "ocean",
        "lava",
        "dead"
    ]

    for i in range(
        rng.randint(
            1,
            6
        )
    ):

        sector["planets"].append({

            "name":
                f"{chr(65+i)}-"+
                str(
                    rng.randint(
                        10,
                        99
                    )
                ),

            "type":
                rng.choice(
                    planet_types
                ),

            "radius":
                rng.randint(
                    15,
                    50
                ),

            "orbit":
                rng.randint(
                    180,
                    700
                )
        })


    # ========================================================
    # STRUCTURES
    # ========================================================

    structure_types = [
        "station",
        "wreck",
        "mining_colony",
        "pirate_base",
        "alien_ruin",
        "research_outpost"
    ]

    for _ in range(
        rng.randint(
            0,
            5
        )
    ):

        sector["structures"].append({

            "type":
                rng.choice(
                    structure_types
                ),

            "x":
                round(
                    rng.uniform(
                        -1800,
                        1800
                    ),
                    2
                ),

            "y":
                round(
                    rng.uniform(
                        -1800,
                        1800
                    ),
                    2
                )
        })


    # ========================================================
    # RESOURCES
    # ========================================================

    resource_types = [
        "iron",
        "crystal",
        "alien"
    ]

    for _ in range(
        rng.randint(
            5,
            20
        )
    ):

        sector["resources"].append({

            "type":
                rng.choice(
                    resource_types
                ),

            "x":
                round(
                    rng.uniform(
                        -2500,
                        2500
                    ),
                    2
                ),

            "y":
                round(
                    rng.uniform(
                        -2500,
                        2500
                    ),
                    2
                ),

            "amount":
                rng.randint(
                    1,
                    8
                )
        })

    return sector


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def index():
    return render_template_string(
        HTML
    )


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

        x = int(
            request.args.get(
                "x",
                0
            )
        )

        y = int(
            request.args.get(
                "y",
                0
            )
        )

    except ValueError:

        return jsonify({
            "error":
                "Invalid coordinates"
        }), 400

    return jsonify(
        generate_sector(
            seed,
            x,
            y
        )
    )


@app.route("/api/world")
def api_world():

    seed = request.args.get(
        "seed",
        "VOID-829174"
    )

    try:

        radius = int(
            request.args.get(
                "radius",
                1
            )
        )

    except ValueError:

        radius=1

    radius=max(
        1,
        min(
            radius,
            5
        )
    )

    sectors=[]

    for x in range(
        -radius,
        radius+1
    ):

        for y in range(
            -radius,
            radius+1
        ):

            sectors.append(
                generate_sector(
                    seed,
                    x,
                    y
                )
            )

    return jsonify({

        "seed":
            seed,

        "radius":
            radius,

        "sectors":
            sectors
    })


@app.route("/api/galaxy")
def api_galaxy():

    seed = request.args.get(
        "seed",
        "VOID-829174"
    )

    rng=
        deterministic_rng(
            f"{seed}:galaxy"
        )

    return jsonify({

        "seed":
            seed,

        "type":
            rng.choice([
                "spiral",
                "cluster",
                "irregular",
                "ring"
            ]),

        "age":
            rng.randint(
                5,
                14
            ),

        "stars":
            rng.randint(
                1000000,
                9000000
            ),

        "civilizations":
            rng.randint(
                3,
                15
            )
    })


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    port=int(
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
