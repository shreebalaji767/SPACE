from flask import Flask, render_template_string, jsonify, request
import os
import random
import hashlib
import math

app = Flask(__name__)


# ============================================================
# VOID SPACE
# PROCEDURAL PERSISTENT SPACE SANDBOX
# ============================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,
               initial-scale=1.0,
               maximum-scale=1.0,
               user-scalable=no,
               viewport-fit=cover">

<meta name="theme-color" content="#02040a">

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

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    color:white;

    touch-action:none;

    user-select:none;
}

body{
    position:fixed;
    inset:0;
}

canvas{

    position:absolute;

    left:0;
    top:0;

    width:100%;
    height:100%;

    display:block;

    background:#02040a;

    touch-action:none;
}


/* ============================================================
   HUD
============================================================ */

#hud{

    position:absolute;

    left:0;
    top:0;

    width:100%;

    padding:
        max(10px,env(safe-area-inset-top))
        max(10px,env(safe-area-inset-right))
        10px
        max(10px,env(safe-area-inset-left));

    pointer-events:none;

    z-index:20;
}

.hudTop{

    display:flex;

    justify-content:space-between;

    align-items:flex-start;

    gap:10px;
}

.panel{

    background:
        rgba(3,7,18,.78);

    border:
        1px solid
        rgba(100,150,255,.28);

    border-radius:12px;

    padding:8px 10px;

    backdrop-filter:blur(8px);

    box-shadow:
        0 0 25px
        rgba(0,0,0,.35);
}

.stats{

    min-width:180px;

    font-size:12px;
}

.statLine{

    display:flex;

    justify-content:space-between;

    gap:15px;

    margin-bottom:4px;

    color:#b8c9e8;
}

.statLine b{
    color:white;
}

.bar{

    width:100%;

    height:5px;

    margin-top:3px;

    margin-bottom:5px;

    background:#101624;

    border-radius:10px;

    overflow:hidden;
}

.bar > div{

    width:100%;

    height:100%;
}

#hullBar{
    background:#ff4f61;
}

#shieldBar{
    background:#4da8ff;
}

#energyBar{
    background:#c76bff;
}

#xpBar{
    background:#65e68a;
}

.info{

    text-align:right;

    font-size:12px;

    line-height:1.5;

    color:#9fb2d9;
}

.info b{
    color:white;
}

#eventText{

    position:absolute;

    left:50%;

    top:
        calc(
            max(65px,env(safe-area-inset-top) + 55px)
        );

    transform:
        translate(-50%,-10px);

    opacity:0;

    transition:
        opacity .25s,
        transform .25s;

    padding:9px 15px;

    border-radius:20px;

    background:
        rgba(5,10,24,.9);

    border:
        1px solid
        rgba(120,160,255,.35);

    color:#d9e7ff;

    font-size:12px;

    white-space:nowrap;

    pointer-events:none;
}

#eventText.show{

    opacity:1;

    transform:
        translate(-50%,0);
}


/* ============================================================
   BUTTONS
============================================================ */

button{

    border:1px solid
        rgba(130,170,255,.4);

    background:
        rgba(10,18,40,.88);

    color:white;

    padding:11px 16px;

    border-radius:10px;

    cursor:pointer;

    font-weight:bold;

    letter-spacing:.5px;

    touch-action:none;
}

button:hover{

    background:
        rgba(25,40,75,.95);
}

button:active{

    transform:scale(.96);
}

.smallBtn{

    padding:7px 10px;

    font-size:11px;
}


/* ============================================================
   MOBILE HUD BUTTONS
============================================================ */

#mobileHUD{

    position:absolute;

    right:
        max(10px,env(safe-area-inset-right));

    bottom:
        max(115px,env(safe-area-inset-bottom) + 105px);

    display:none;

    gap:7px;

    z-index:25;
}

#mobileHUD button{

    padding:9px 11px;

    font-size:10px;

    opacity:.85;
}


/* ============================================================
   TOUCH CONTROLS
============================================================ */

#touchUI{

    position:absolute;

    inset:0;

    pointer-events:none;

    z-index:30;
}

#joystick{

    position:absolute;

    left:
        max(18px,env(safe-area-inset-left) + 12px);

    bottom:
        max(22px,env(safe-area-inset-bottom) + 18px);

    width:130px;
    height:130px;

    border-radius:50%;

    background:
        rgba(50,80,140,.16);

    border:
        2px solid
        rgba(120,160,255,.3);

    pointer-events:auto;

    touch-action:none;
}

#stick{

    position:absolute;

    left:50%;
    top:50%;

    width:58px;
    height:58px;

    margin-left:-29px;
    margin-top:-29px;

    border-radius:50%;

    background:
        rgba(100,150,255,.4);

    border:
        2px solid
        rgba(180,210,255,.65);

    box-shadow:
        0 0 25px
        rgba(80,130,255,.2);

    pointer-events:none;
}

.touchButton{

    position:absolute;

    border-radius:50%;

    display:flex;

    align-items:center;

    justify-content:center;

    font-size:11px;

    font-weight:bold;

    letter-spacing:.5px;

    pointer-events:auto;

    touch-action:none;
}

#fireBtn{

    right:
        max(20px,env(safe-area-inset-right) + 18px);

    bottom:
        max(35px,env(safe-area-inset-bottom) + 25px);

    width:100px;
    height:100px;

    background:
        rgba(255,70,90,.22);

    border:
        2px solid
        rgba(255,100,120,.55);
}

#boostBtn{

    right:
        max(32px,env(safe-area-inset-right) + 30px);

    bottom:
        max(145px,env(safe-area-inset-bottom) + 135px);

    width:70px;
    height:70px;

    background:
        rgba(120,80,255,.2);

    border:
        2px solid
        rgba(160,120,255,.55);
}

#aimHint{

    position:absolute;

    left:50%;

    bottom:15px;

    transform:translateX(-50%);

    color:
        rgba(180,200,240,.4);

    font-size:10px;

    pointer-events:none;
}


/* ============================================================
   CROSSHAIR
============================================================ */

#crosshair{

    position:absolute;

    width:28px;
    height:28px;

    transform:
        translate(-50%,-50%);

    display:none;

    pointer-events:none;

    z-index:18;
}

#crosshair:before,
#crosshair:after{

    content:"";

    position:absolute;

    background:
        rgba(170,210,255,.75);
}

#crosshair:before{

    width:28px;
    height:1px;

    top:13px;
    left:0;
}

#crosshair:after{

    width:1px;
    height:28px;

    left:13px;
    top:0;
}


/* ============================================================
   SCREENS
============================================================ */

.screen{

    position:absolute;

    inset:0;

    z-index:50;

    display:flex;

    align-items:center;

    justify-content:center;

    padding:
        max(20px,env(safe-area-inset-top))
        max(20px,env(safe-area-inset-right))
        max(20px,env(safe-area-inset-bottom))
        max(20px,env(safe-area-inset-left));

    background:
        radial-gradient(
            circle at center,
            rgba(15,30,65,.75),
            rgba(1,3,8,.96)
        );
}

.hidden{
    display:none !important;
}

.card{

    width:min(650px,94vw);

    max-height:90vh;

    overflow:auto;

    padding:30px;

    border-radius:18px;

    background:
        rgba(5,9,20,.94);

    border:
        1px solid
        rgba(120,160,255,.3);

    box-shadow:
        0 30px 100px
        rgba(0,0,0,.6);

    text-align:center;
}

.logo{

    font-size:
        clamp(34px,8vw,70px);

    letter-spacing:
        clamp(5px,2vw,15px);

    margin-bottom:8px;

    color:#dbe9ff;

    text-shadow:
        0 0 30px
        rgba(100,150,255,.55);
}

.subtitle{

    color:#7f95bd;

    margin-bottom:25px;

    font-size:13px;

    letter-spacing:2px;
}

.menuButtons{

    display:grid;

    gap:10px;

    max-width:360px;

    margin:auto;
}

.menuButtons button{

    width:100%;
}

.input{

    width:100%;

    padding:13px;

    border-radius:10px;

    border:
        1px solid
        rgba(120,160,255,.3);

    background:#070c18;

    color:white;

    outline:none;

    margin-bottom:10px;

    text-align:center;
}

.help{

    text-align:left;

    color:#a9b9d6;

    font-size:13px;

    line-height:1.8;
}

.help b{
    color:white;
}

.inventoryGrid{

    display:grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(110px,1fr)
        );

    gap:10px;

    margin:20px 0;
}

.item{

    padding:15px;

    border-radius:12px;

    background:#090f1e;

    border:
        1px solid
        rgba(100,140,230,.25);

    display:flex;

    flex-direction:column;

    gap:8px;
}

.item span{

    font-size:22px;

    color:#cfe0ff;
}


/* ============================================================
   MINIMAP
============================================================ */

#minimap{

    position:absolute;

    right:
        max(12px,env(safe-area-inset-right) + 8px);

    top:
        max(120px,env(safe-area-inset-top) + 105px);

    width:145px;
    height:145px;

    border-radius:12px;

    border:
        1px solid
        rgba(100,140,255,.3);

    background:#02050d;

    opacity:.85;

    z-index:15;
}


/* ============================================================
   RESPONSIVE
============================================================ */

@media(max-width:700px){

    #mobileHUD{
        display:flex;
    }

    .stats{

        min-width:
            min(
                165px,
                48vw
            );

        font-size:10px;
    }

    .info{
        font-size:9px;
    }

    #minimap{

        width:105px;
        height:105px;

        top:
            max(
                125px,
                env(safe-area-inset-top) + 105px
            );
    }

    .card{
        padding:22px;
    }

    .help{
        font-size:12px;
    }
}

@media(pointer:coarse){

    #touchUI{
        display:block;
    }
}

@media(pointer:fine){

    #touchUI{
        display:none;
    }
}

@media(max-height:500px){

    #joystick{

        width:105px;
        height:105px;
    }

    #stick{

        width:48px;
        height:48px;

        margin-left:-24px;
        margin-top:-24px;
    }

    #fireBtn{

        width:75px;
        height:75px;
    }

    #boostBtn{

        width:55px;
        height:55px;

        bottom:
            max(
                105px,
                env(safe-area-inset-bottom) + 95px
            );
    }
}

</style>
</head>


<body>

<canvas id="game"></canvas>


<!-- =========================================================
     HUD
========================================================== -->

<div id="hud" class="hidden">

    <div class="hudTop">

        <div class="panel stats">

            <div class="statLine">
                <span>HULL</span>
                <b id="hullValue">100</b>
            </div>

            <div class="bar">
                <div id="hullBar"></div>
            </div>

            <div class="statLine">
                <span>SHIELD</span>
                <b id="shieldValue">100</b>
            </div>

            <div class="bar">
                <div id="shieldBar"></div>
            </div>

            <div class="statLine">
                <span>ENERGY</span>
                <b id="energyValue">100</b>
            </div>

            <div class="bar">
                <div id="energyBar"></div>
            </div>

            <div class="statLine">
                <span>XP</span>
                <b id="xpValue">0</b>
            </div>

            <div class="bar">
                <div id="xpBar"></div>
            </div>

        </div>


        <div class="panel info">

            <div>
                <b id="levelText">LEVEL 1</b>
            </div>

            <div id="weaponText">
                PULSE CANNON
            </div>

            <div>
                CREDITS:
                <b id="creditsText">0</b>
            </div>

            <div>
                KILLS:
                <b id="killsText">0</b>
            </div>

            <div id="sectorText">
                SECTOR 0 : 0
            </div>

        </div>

    </div>

</div>


<div id="eventText"></div>

<div id="crosshair"></div>

<canvas id="minimap"
        width="145"
        height="145"></canvas>


<!-- =========================================================
     MOBILE HUD
========================================================== -->

<div id="mobileHUD">

    <button id="mobileInventory"
            class="smallBtn">
        INV
    </button>

    <button id="mobilePause"
            class="smallBtn">
        PAUSE
    </button>

</div>


<!-- =========================================================
     TOUCH CONTROLS
========================================================== -->

<div id="touchUI">

    <div id="joystick">

        <div id="stick"></div>

    </div>

    <div id="fireBtn"
         class="touchButton">
        FIRE
    </div>

    <div id="boostBtn"
         class="touchButton">
        BOOST
    </div>

    <div id="aimHint">
        DRAG TO AIM
    </div>

</div>


<!-- =========================================================
     MAIN MENU
========================================================== -->

<div id="menu"
     class="screen">

    <div class="card">

        <div class="logo">
            VOID SPACE
        </div>

        <div class="subtitle">
            PROCEDURAL PERSISTENT UNIVERSE
        </div>

        <input
            id="seedInput"
            class="input"
            placeholder="WORLD SEED">

        <div class="menuButtons">

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

    </div>

</div>


<!-- =========================================================
     HOW TO PLAY
========================================================== -->

<div id="howto"
     class="screen hidden">

    <div class="card">

        <h2>HOW TO PLAY</h2>

        <br>

        <div class="help">

            <p>
                <b>DESKTOP</b>
            </p>

            <p>
                WASD / ARROWS — Move
            </p>

            <p>
                Mouse — Aim / Rotate ship
            </p>

            <p>
                Left Mouse / SPACE — Fire
            </p>

            <p>
                SHIFT — Boost
            </p>

            <p>
                1–5 — Change weapon
            </p>

            <p>
                P / ESC — Pause
            </p>

            <br>

            <p>
                <b>TOUCH</b>
            </p>

            <p>
                Left joystick — Move
            </p>

            <p>
                Drag anywhere on the right — Aim
            </p>

            <p>
                FIRE — Fire weapon
            </p>

            <p>
                BOOST — Boost
            </p>

            <br>

            <p>
                Explore different procedural sectors.
                Each world is generated from its seed.
            </p>

            <p>
                Find stations, colonies, wrecks,
                alien ruins and resource fields.
            </p>

            <p>
                Defeat enemies, collect resources,
                gain XP and discover the universe.
            </p>

        </div>

        <br>

        <button onclick="showScreen('menu')">
            BACK
        </button>

    </div>

</div>


<!-- =========================================================
     SETTINGS
========================================================== -->

<div id="settings"
     class="screen hidden">

    <div class="card">

        <h2>SETTINGS</h2>

        <br>

        <div class="help">

            <p>
                VOID SPACE uses a deterministic
                procedural universe.
            </p>

            <p>
                The same seed creates the same
                sector layout.
            </p>

            <p>
                Progress is stored locally
                in your browser.
            </p>

        </div>

        <br>

        <button onclick="saveGame()">
            SAVE
        </button>

        <button onclick="showScreen('menu')">
            BACK
        </button>

    </div>

</div>


<!-- =========================================================
     INVENTORY
========================================================== -->

<div id="inventory"
     class="screen hidden">

    <div class="card">

        <h2>INVENTORY</h2>

        <div id="inventoryGrid"
             class="inventoryGrid"></div>

        <button onclick="resumeFromOverlay()">
            CLOSE
        </button>

    </div>

</div>


<!-- =========================================================
     PAUSE
========================================================== -->

<div id="pause"
     class="screen hidden">

    <div class="card">

        <h2>PAUSED</h2>

        <br>

        <button onclick="togglePause()">
            RESUME
        </button>

        <br><br>

        <button onclick="saveGame()">
            SAVE UNIVERSE
        </button>

        <br><br>

        <button onclick="showScreen('menu')">
            MAIN MENU
        </button>

    </div>

</div>


<!-- =========================================================
     GAME OVER
========================================================== -->

<div id="gameover"
     class="screen hidden">

    <div class="card">

        <h2>SHIP DESTROYED</h2>

        <br>

        <div id="gameOverText"></div>

        <br>

        <button onclick="newGame()">
            NEW UNIVERSE
        </button>

        <br><br>

        <button onclick="continueGame()">
            RESTORE SAVE
        </button>

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


let W = innerWidth;
let H = innerHeight;

function resize(){

    W = innerWidth;
    H = innerHeight;

    canvas.width =
        Math.floor(W * devicePixelRatio);

    canvas.height =
        Math.floor(H * devicePixelRatio);

    canvas.style.width =
        W + "px";

    canvas.style.height =
        H + "px";

    ctx.setTransform(
        devicePixelRatio,
        0,
        0,
        devicePixelRatio,
        0,
        0
    );
}

addEventListener(
    "resize",
    resize
);

resize();


/* ============================================================
   GLOBAL STATE
============================================================ */

let gameRunning = false;

let paused = false;

let worldSeed =
    "VOID-829174";

const CHUNK_SIZE = 5000;

let currentChunk = {
    x: 999999,
    y: 999999
};

let activeChunks = new Map();

let structures = [];

let resources = [];

let enemies = [];

let bullets = [];

let enemyBullets = [];

let pickups = [];

let particles = [];

let stars = [];

let keys = {};

let lastTime =
    performance.now();

let elapsed = 0;

let shake = 0;

let spawnTimer = 0;

let eventTimer = 0;

let lastLoadedChunkKey = "";


/* ============================================================
   PLAYER
============================================================ */

let player = {

    x:0,
    y:0,

    vx:0,
    vy:0,

    angle:0,

    targetAngle:0,

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
   CAMERA
============================================================ */

let camera = {
    x:0,
    y:0
};


/* ============================================================
   INPUT
============================================================ */

let mouse = {

    x:W/2,
    y:H/2,

    down:false
};

let mobile = {

    x:0,
    y:0,

    fire:false,

    boost:false,

    aiming:false,

    aimX:W/2,

    aimY:H/2
};


/* ============================================================
   SEEDED RANDOM
============================================================ */

function hashString(str){

    let h = 2166136261;

    for(let i=0;i<str.length;i++){

        h ^= str.charCodeAt(i);

        h +=
            (h<<1)+
            (h<<4)+
            (h<<7)+
            (h<<8)+
            (h<<24);
    }

    return h >>> 0;
}

function seededRandom(seed){

    let state =
        hashString(String(seed));

    return function(){

        state += 0x6D2B79F5;

        let t = state;

        t =
            Math.imul(
                t ^ (t >>> 15),
                t | 1
            );

        t ^= t +
            Math.imul(
                t ^ (t >>> 7),
                t | 61
            );

        return (
            (
                (t ^ (t >>> 14))
                >>> 0
            ) / 4294967296
        );
    };
}

function rr(r,min,max){

    return min +
        r() *
        (max-min);
}

function ri(r,min,max){

    return Math.floor(
        rr(r,min,max+1)
    );
}

function pick(r,array){

    return array[
        Math.floor(
            r()*array.length
        )
    ];
}


/* ============================================================
   CHUNK GENERATOR
============================================================ */

function generateChunk(cx,cy){

    const r =
        seededRandom(
            worldSeed +
            ":sector:" +
            cx +
            ":" +
            cy
        );

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

    const starsTypes = [

        "blue",
        "yellow",
        "red",
        "white",
        "neutron"
    ];

    const names = [

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

    const factions = [

        "miners",
        "federation",
        "pirates",
        "aliens",
        "neutral"
    ];

    const specials = [

        "distress_signal",
        "ancient_signal",
        "pirate_patrol",
        "merchant_convoy",
        "derelict",
        "resource_rush",
        "none"
    ];

    const chunk = {

        x:cx,
        y:cy,

        biome:pick(
            r,
            biomes
        ),

        danger:ri(
            r,
            1,
            10
        ),

        system_name:
            pick(r,names) +
            "-" +
            ri(r,100,999),

        star:
            pick(r,starsTypes),

        faction:
            pick(r,factions),

        special:
            pick(r,specials),

        structures:[],
        resources:[]
    };


    const structureTypes = [

        "station",
        "wreck",
        "mining_colony",
        "pirate_base",
        "alien_ruin",
        "research_outpost"
    ];

    const countStructures =
        ri(r,1,6);

    for(
        let i=0;
        i<countStructures;
        i++
    ){

        chunk.structures.push({

            id:
                "S-" +
                cx +
                "-" +
                cy +
                "-" +
                i,

            type:
                pick(
                    r,
                    structureTypes
                ),

            x:
                rr(
                    r,
                    -2200,
                    2200
                ),

            y:
                rr(
                    r,
                    -2200,
                    2200
                ),

            radius:
                rr(
                    r,
                    40,
                    100
                )
        });
    }


    const resourceTypes = [

        "iron",
        "crystal",
        "alien"
    ];

    const countResources =
        ri(r,8,25);

    for(
        let i=0;
        i<countResources;
        i++
    ){

        chunk.resources.push({

            id:
                "R-" +
                cx +
                "-" +
                cy +
                "-" +
                i,

            type:
                pick(
                    r,
                    resourceTypes
                ),

            x:
                rr(
                    r,
                    -2450,
                    2450
                ),

            y:
                rr(
                    r,
                    -2450,
                    2450
                ),

            amount:
                ri(r,1,8),

            collected:false
        });
    }

    return chunk;
}


/* ============================================================
   CHUNK MANAGEMENT
============================================================ */

function chunkFromPosition(x,y){

    return {

        x:
            Math.floor(
                x / CHUNK_SIZE
            ),

        y:
            Math.floor(
                y / CHUNK_SIZE
            )
    };
}

function chunkKey(x,y){

    return x + ":" + y;
}

function worldObjectPosition(obj,cx,cy){

    return {

        x:
            obj.x +
            cx*CHUNK_SIZE,

        y:
            obj.y +
            cy*CHUNK_SIZE
    };
}

function loadNearbyChunks(){

    const c =
        chunkFromPosition(
            player.x,
            player.y
        );

    const key =
        chunkKey(c.x,c.y);

    if(
        key ===
        lastLoadedChunkKey
    )
        return;

    lastLoadedChunkKey = key;

    activeChunks.clear();

    structures = [];
    resources = [];

    for(
        let dx=-1;
        dx<=1;
        dx++
    ){

        for(
            let dy=-1;
            dy<=1;
            dy++
        ){

            const cx =
                c.x+dx;

            const cy =
                c.y+dy;

            const chunk =
                generateChunk(
                    cx,
                    cy
                );

            activeChunks.set(
                chunkKey(cx,cy),
                chunk
            );


            for(
                const s of
                chunk.structures
            ){

                const p =
                    worldObjectPosition(
                        s,
                        cx,
                        cy
                    );

                structures.push({

                    ...s,

                    x:p.x,
                    y:p.y,

                    chunkX:cx,
                    chunkY:cy
                });
            }


            for(
                const r of
                chunk.resources
            ){

                const p =
                    worldObjectPosition(
                        r,
                        cx,
                        cy
                    );

                resources.push({

                    ...r,

                    x:p.x,
                    y:p.y,

                    chunkX:cx,
                    chunkY:cy
                });
            }
        }
    }

    currentChunk = c;

    document.getElementById(
        "sectorText"
    ).textContent =
        "SECTOR " +
        c.x +
        " : " +
        c.y;

    showEvent(
        "ENTERED " +
        generateChunk(
            c.x,
            c.y
        ).system_name
    );

    spawnSectorEnemies();
}


/* ============================================================
   STARFIELD
============================================================ */

function buildStars(){

    stars=[];

    const r =
        seededRandom(
            worldSeed +
            ":stars"
        );

    for(
        let i=0;
        i<700;
        i++
    ){

        stars.push({

            x:r(),

            y:r(),

            size:
                rr(
                    r,
                    .4,
                    2
                ),

            alpha:
                rr(
                    r,
                    .2,
                    .9
                )
        });
    }
}


/* ============================================================
   SCREEN / WORLD
============================================================ */

function worldToScreen(x,y){

    return {

        x:
            x -
            camera.x +
            W/2,

        y:
            y -
            camera.y +
            H/2
    };
}

function screenToWorld(x,y){

    return {

        x:
            camera.x +
            x -
            W/2,

        y:
            camera.y +
            y -
            H/2
    };
}


/* ============================================================
   AIM
============================================================ */

function aimPlayer(sx,sy){

    const world =
        screenToWorld(
            sx,
            sy
        );

    player.targetAngle =
        Math.atan2(
            world.y-player.y,
            world.x-player.x
        );
}


/* ============================================================
   PLAYER UPDATE
============================================================ */

function updatePlayer(dt){

    let mx=0;
    let my=0;

    if(
        keys["w"] ||
        keys["arrowup"]
    )
        my-=1;

    if(
        keys["s"] ||
        keys["arrowdown"]
    )
        my+=1;

    if(
        keys["a"] ||
        keys["arrowleft"]
    )
        mx-=1;

    if(
        keys["d"] ||
        keys["arrowright"]
    )
        mx+=1;


    if(
        Math.abs(mobile.x)>.05 ||
        Math.abs(mobile.y)>.05
    ){

        mx += mobile.x;
        my += mobile.y;
    }


    const magnitude =
        Math.hypot(mx,my);

    if(magnitude>1){

        mx/=magnitude;
        my/=magnitude;
    }


    const boosting =
        keys["shift"] ||
        mobile.boost;


    const acceleration =
        boosting
            ? 900
            : 500;


    if(
        magnitude>.01
    ){

        player.vx +=
            mx *
            acceleration *
            dt;

        player.vy +=
            my *
            acceleration *
            dt;
    }


    const maxSpeed =
        boosting
            ? 1100
            : 650;


    const speed =
        Math.hypot(
            player.vx,
            player.vy
        );

    if(
        speed>maxSpeed
    ){

        player.vx =
            player.vx/speed*
            maxSpeed;

        player.vy =
            player.vy/speed*
            maxSpeed;
    }


    const drag =
        Math.pow(
            .0005,
            dt
        );

    player.vx*=drag;
    player.vy*=drag;


    player.x +=
        player.vx*dt;

    player.y +=
        player.vy*dt;


    let difference =
        player.targetAngle -
        player.angle;

    while(
        difference >
        Math.PI
    )
        difference -=
            Math.PI*2;

    while(
        difference <
        -Math.PI
    )
        difference +=
            Math.PI*2;


    player.angle +=
        difference *
        Math.min(
            1,
            dt*12
        );


    if(
        mouse.down ||
        keys[" "] ||
        mobile.fire
    ){

        fireWeapon();
    }


    player.energy =
        Math.min(
            player.maxEnergy,
            player.energy +
            18*dt
        );


    player.shield =
        Math.min(
            player.maxShield,
            player.shield +
            3*dt
        );


    loadNearbyChunks();


    camera.x +=
        (
            player.x -
            camera.x
        ) *
        Math.min(
            1,
            dt*8
        );

    camera.y +=
        (
            player.y -
            camera.y
        ) *
        Math.min(
            1,
            dt*8
        );
}


/* ============================================================
   WEAPONS
============================================================ */

const weapons = {

    pulse:{
        cooldown:.16,
        energy:2,
        damage:18,
        speed:1300,
        size:4
    },

    spread:{
        cooldown:.34,
        energy:7,
        damage:13,
        speed:1100,
        size:4
    },

    laser:{
        cooldown:.08,
        energy:3,
        damage:10,
        speed:1800,
        size:3
    },

    missile:{
        cooldown:.65,
        energy:15,
        damage:70,
        speed:650,
        size:7
    },

    plasma:{
        cooldown:.42,
        energy:10,
        damage:55,
        speed:850,
        size:9
    }
};

let lastShot = 0;


function fireWeapon(){

    const now =
        performance.now()/1000;

    const w =
        weapons[
            player.weapon
        ];

    if(
        now-lastShot <
        w.cooldown
    )
        return;

    if(
        player.energy <
        w.energy
    )
        return;

    player.energy -=
        w.energy;

    lastShot = now;


    if(
        player.weapon ===
        "spread"
    ){

        for(
            let i=-2;
            i<=2;
            i++
        ){

            spawnBullet(
                player.angle +
                i*.12,
                w
            );
        }

    }else{

        spawnBullet(
            player.angle,
            w
        );
    }

    muzzleFlash();
}


function spawnBullet(angle,w){

    const offset=30;

    bullets.push({

        x:
            player.x +
            Math.cos(angle)*
            offset,

        y:
            player.y +
            Math.sin(angle)*
            offset,

        vx:
            Math.cos(angle)*
            w.speed +
            player.vx*.35,

        vy:
            Math.sin(angle)*
            w.speed +
            player.vy*.35,

        damage:w.damage,

        size:w.size,

        life:2,

        weapon:player.weapon
    });
}


function muzzleFlash(){

    for(
        let i=0;
        i<5;
        i++
    ){

        particles.push({

            x:
                player.x+
                Math.cos(player.angle)*
                35,

            y:
                player.y+
                Math.sin(player.angle)*
                35,

            vx:
                Math.cos(player.angle)*
                (100+Math.random()*200),

            vy:
                Math.sin(player.angle)*
                (100+Math.random()*200),

            life:.2,

            maxLife:.2,

            size:
                2+
                Math.random()*3,

            color:"#a8d7ff"
        });
    }
}


/* ============================================================
   ENEMIES
============================================================ */

const enemyTypes = {

    scout:{
        hp:35,
        speed:230,
        damage:8,
        radius:16,
        color:"#ff6474",
        xp:15
    },

    fighter:{
        hp:70,
        speed:180,
        damage:12,
        radius:20,
        color:"#ff445a",
        xp:25
    },

    interceptor:{
        hp:55,
        speed:340,
        damage:16,
        radius:15,
        color:"#ff9b50",
        xp:30
    },

    tank:{
        hp:260,
        speed:90,
        damage:25,
        radius:38,
        color:"#d34bff",
        xp:100
    },

    sniper:{
        hp:80,
        speed:100,
        damage:30,
        radius:22,
        color:"#72a0ff",
        xp:70
    },

    bomber:{
        hp:120,
        speed:125,
        damage:45,
        radius:25,
        color:"#ffbd4a",
        xp:80
    },

    swarm:{
        hp:20,
        speed:300,
        damage:6,
        radius:10,
        color:"#b0ff65",
        xp:10
    },

    elite:{
        hp:420,
        speed:150,
        damage:35,
        radius:45,
        color:"#ff3dca",
        xp:180
    },

    guardian:{
        hp:800,
        speed:100,
        damage:45,
        radius:65,
        color:"#ff314d",
        xp:500
    }
};


function spawnEnemy(type){

    const t =
        enemyTypes[type];

    const angle =
        Math.random()*
        Math.PI*2;

    const distance =
        900+
        Math.random()*1200;

    enemies.push({

        type:type,

        x:
            player.x+
            Math.cos(angle)*
            distance,

        y:
            player.y+
            Math.sin(angle)*
            distance,

        vx:0,
        vy:0,

        hp:t.hp,
        maxHp:t.hp,

        radius:t.radius,

        speed:t.speed,

        damage:t.damage,

        color:t.color,

        xp:t.xp,

        fireCooldown:
            .5+
            Math.random()*2,

        boss:
            type==="guardian"
    });
}


function spawnSectorEnemies(){

    const c =
        currentChunk;

    const chunk =
        generateChunk(
            c.x,
            c.y
        );

    const count =
        4+
        Math.floor(
            chunk.danger*
            .8
        );

    for(
        let i=0;
        i<count;
        i++
    ){

        const roll =
            Math.random();

        let type="fighter";

        if(
            roll<.15
        )
            type="scout";

        else if(
            roll<.28
        )
            type="interceptor";

        else if(
            roll<.40
        )
            type="swarm";

        else if(
            roll<.50
        )
            type="sniper";

        else if(
            roll<.58
        )
            type="bomber";

        else if(
            roll<.68
        )
            type="tank";

        else if(
            roll<.76
        )
            type="elite";

        spawnEnemy(type);
    }


    if(
        chunk.danger>=8 &&
        Math.random()<.45
    ){

        spawnBoss();
    }
}


function spawnBoss(){

    if(
        enemies.some(
            e=>e.boss
        )
    )
        return;

    spawnEnemy(
        "guardian"
    );

    showEvent(
        "WARNING • GUARDIAN DETECTED"
    );
}


/* ============================================================
   ENEMY UPDATE
============================================================ */

function updateEnemies(dt){

    for(
        let i=enemies.length-1;
        i>=0;
        i--
    ){

        const e =
            enemies[i];

        const dx =
            player.x-e.x;

        const dy =
            player.y-e.y;

        const distance =
            Math.hypot(
                dx,
                dy
            ) || 1;

        const nx =
            dx/distance;

        const ny =
            dy/distance;


        e.vx +=
            nx*
            e.speed*
            dt*
            .7;

        e.vy +=
            ny*
            e.speed*
            dt*
            .7;


        const velocity =
            Math.hypot(
                e.vx,
                e.vy
            );

        if(
            velocity>e.speed
        ){

            e.vx =
                e.vx/
                velocity*
                e.speed;

            e.vy =
                e.vy/
                velocity*
                e.speed;
        }


        e.x +=
            e.vx*dt;

        e.y +=
            e.vy*dt;


        e.fireCooldown -=
            dt;


        if(
            e.fireCooldown<=0 &&
            distance<1300
        ){

            enemyShoot(e);

            e.fireCooldown =
                e.boss
                    ? .55
                    : 1.2+
                      Math.random()*
                      2;
        }


        if(
            distance <
            e.radius+
            25
        ){

            damagePlayer(
                e.damage*
                dt
            );
        }


        if(
            e.hp<=0
        ){

            destroyEnemy(
                i
            );
        }
    }


    spawnTimer -= dt;

    if(
        spawnTimer<=0 &&
        enemies.length<28
    ){

        const roll =
            Math.random();

        let type =
            "fighter";

        if(
            roll<.15
        )
            type="scout";

        else if(
            roll<.30
        )
            type="interceptor";

        else if(
            roll<.42
        )
            type="swarm";

        else if(
            roll<.54
        )
            type="sniper";

        else if(
            roll<.64
        )
            type="bomber";

        else if(
            roll<.75
        )
            type="tank";

        else if(
            roll<.84
        )
            type="elite";

        spawnEnemy(type);

        spawnTimer =
            1+
            Math.random()*3;
    }
}


function enemyShoot(e){

    const angle =
        Math.atan2(
            player.y-e.y,
            player.x-e.x
        );

    const speed =
        e.boss
            ? 500
            : 420;

    enemyBullets.push({

        x:e.x,
        y:e.y,

        vx:
            Math.cos(angle)*
            speed,

        vy:
            Math.sin(angle)*
            speed,

        damage:
            e.damage,

        size:
            e.boss
                ? 8
                : 5,

        life:4
    });


    if(
        e.boss
    ){

        for(
            let i=0;
            i<7;
            i++
        ){

            const a =
                angle+
                (
                    i-3
                )*.18;

            enemyBullets.push({

                x:e.x,
                y:e.y,

                vx:
                    Math.cos(a)*
                    350,

                vy:
                    Math.sin(a)*
                    350,

                damage:
                    e.damage*.55,

                size:5,

                life:3
            });
        }
    }
}


/* ============================================================
   DAMAGE
============================================================ */

function damagePlayer(amount){

    if(
        player.shield>0
    ){

        const absorbed =
            Math.min(
                player.shield,
                amount
            );

        player.shield -=
            absorbed;

        amount -=
            absorbed;
    }

    if(
        amount>0
    ){

        player.hull -=
            amount;
    }

    shake =
        Math.min(
            20,
            shake+
            amount*.15
        );

    if(
        player.hull<=0
    ){

        player.hull=0;

        gameOver();
    }
}


/* ============================================================
   BULLET UPDATE
============================================================ */

function updateBullets(dt){

    for(
        let i=bullets.length-1;
        i>=0;
        i--
    ){

        const b =
            bullets[i];

        b.x +=
            b.vx*dt;

        b.y +=
            b.vy*dt;

        b.life -=
            dt;


        let hit=false;

        for(
            let j=enemies.length-1;
            j>=0;
            j--
        ){

            const e =
                enemies[j];

            const d =
                Math.hypot(
                    b.x-e.x,
                    b.y-e.y
                );

            if(
                d<
                b.size+
                e.radius
            ){

                e.hp -=
                    b.damage;

                createExplosion(
                    b.x,
                    b.y,
                    4,
                    "#b9d8ff"
                );

                hit=true;

                if(
                    b.weapon ===
                    "plasma"
                ){

                    for(
                        const other
                        of enemies
                    ){

                        if(
                            other===e
                        )
                            continue;

                        const splash =
                            Math.hypot(
                                other.x-b.x,
                                other.y-b.y
                            );

                        if(
                            splash<100
                        ){

                            other.hp -=
                                b.damage*.35;
                        }
                    }
                }

                break;
            }
        }


        if(
            hit ||
            b.life<=0
        ){

            bullets.splice(
                i,
                1
            );
        }
    }
}


/* ============================================================
   ENEMY BULLETS
============================================================ */

function updateEnemyBullets(dt){

    for(
        let i=
            enemyBullets.length-1;
        i>=0;
        i--
    ){

        const b =
            enemyBullets[i];

        b.x +=
            b.vx*dt;

        b.y +=
            b.vy*dt;

        b.life -=
            dt;


        const d =
            Math.hypot(
                b.x-player.x,
                b.y-player.y
            );

        if(
            d<
            25+
            b.size
        ){

            damagePlayer(
                b.damage
            );

            enemyBullets.splice(
                i,
                1
            );

            continue;
        }


        if(
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
   DESTROY ENEMY
============================================================ */

function destroyEnemy(index){

    const e =
        enemies[index];

    createExplosion(
        e.x,
        e.y,
        e.boss
            ? 80
            : 25,
        e.color
    );

    player.kills++;

    gainXP(
        e.xp
    );

    player.credits +=
        Math.floor(
            e.xp*.8+
            Math.random()*40
        );


    if(
        Math.random()<.18
    ){

        pickups.push({

            x:e.x,
            y:e.y,

            type:
                Math.random()<.5
                    ? "shield"
                    : "energy"
        });
    }


    if(
        e.boss
    ){

        player.credits +=
            1000;

        player.inventory.alien +=
            5;

        showEvent(
            "GUARDIAN DESTROYED • +1000 CREDITS"
        );
    }


    enemies.splice(
        index,
        1
    );
}


/* ============================================================
   XP
============================================================ */

function gainXP(amount){

    player.xp +=
        amount;

    while(
        player.xp >=
        xpRequired()
    ){

        player.xp -=
            xpRequired();

        player.level++;

        player.maxHull +=
            10;

        player.maxShield +=
            10;

        player.maxEnergy +=
            8;

        player.hull =
            player.maxHull;

        player.shield =
            player.maxShield;

        player.energy =
            player.maxEnergy;

        showEvent(
            "LEVEL UP • LEVEL " +
            player.level
        );
    }
}

function xpRequired(){

    return 100+
        (
            player.level-1
        )*100;
}


/* ============================================================
   RESOURCES
============================================================ */

function updateResources(){

    for(
        const r of resources
    ){

        if(
            r.collected
        )
            continue;

        const d =
            Math.hypot(
                r.x-player.x,
                r.y-player.y
            );

        if(
            d<35
        ){

            r.collected=true;

            player.inventory[
                r.type
            ] +=
                r.amount;

            player.credits +=
                r.amount*3;

            showEvent(
                "+" +
                r.amount +
                " " +
                r.type.toUpperCase()
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

        const d =
            Math.hypot(
                s.x-player.x,
                s.y-player.y
            );

        if(
            d<100 &&
            !player.discovered.includes(
                s.id
            )
        ){

            player.discovered.push(
                s.id
            );

            gainXP(25);

            showEvent(
                "DISCOVERED • " +
                s.type
                    .replaceAll(
                        "_",
                        " "
                    )
                    .toUpperCase()
            );
        }
    }
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

        const p =
            pickups[i];

        const d =
            Math.hypot(
                p.x-player.x,
                p.y-player.y
            );

        if(
            d<35
        ){

            if(
                p.type==="shield"
            ){

                player.shield =
                    Math.min(
                        player.maxShield,
                        player.shield+35
                    );

            }else{

                player.energy =
                    Math.min(
                        player.maxEnergy,
                        player.energy+50
                    );
            }

            showEvent(
                p.type.toUpperCase() +
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

function createExplosion(
    x,
    y,
    amount,
    color
){

    const count =
        Math.min(
            80,
            Math.floor(
                amount
            )
        );

    for(
        let i=0;
        i<count;
        i++
    ){

        const a =
            Math.random()*
            Math.PI*2;

        const speed =
            30+
            Math.random()*
            amount*5;

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
                .35+
                Math.random()*
                .9,

            maxLife:1.2,

            size:
                1+
                Math.random()*
                4,

            color:color
        });
    }

    shake =
        Math.min(
            25,
            shake+
            amount*.08
        );
}


function updateParticles(dt){

    for(
        let i=particles.length-1;
        i>=0;
        i--
    ){

        const p =
            particles[i];

        p.x +=
            p.vx*dt;

        p.y +=
            p.vy*dt;

        p.vx *=
            Math.pow(.01,dt);

        p.vy *=
            Math.pow(.01,dt);

        p.life -=
            dt;

        if(
            p.life<=0
        ){

            particles.splice(
                i,
                1
            );
        }
    }

    shake *=
        Math.pow(
            .001,
            dt
        );
}


/* ============================================================
   DRAW BACKGROUND
============================================================ */

function drawBackground(){

    ctx.fillStyle =
        "#02040a";

    ctx.fillRect(
        0,
        0,
        W,
        H
    );


    const current =
        generateChunk(
            currentChunk.x,
            currentChunk.y
        );


    if(
        current.biome===
        "nebula"
    ){

        const g =
            ctx.createRadialGradient(
                W*.5,
                H*.5,
                20,
                W*.5,
                H*.5,
                Math.max(W,H)*.7
            );

        g.addColorStop(
            0,
            "rgba(80,50,150,.18)"
        );

        g.addColorStop(
            1,
            "rgba(0,0,0,0)"
        );

        ctx.fillStyle=g;

        ctx.fillRect(
            0,
            0,
            W,
            H
        );
    }


    for(
        const s of stars
    ){

        let x =
            (
                s.x*W -
                camera.x*.03
            ) % W;

        let y =
            (
                s.y*H -
                camera.y*.03
            ) % H;

        if(x<0)x+=W;
        if(y<0)y+=H;

        ctx.globalAlpha =
            s.alpha;

        ctx.fillStyle =
            "#dce8ff";

        ctx.fillRect(
            x,
            y,
            s.size,
            s.size
        );
    }

    ctx.globalAlpha=1;
}


/* ============================================================
   DRAW STRUCTURES
============================================================ */

function drawStructures(){

    for(
        const s of structures
    ){

        const p =
            worldToScreen(
                s.x,
                s.y
            );

        if(
            p.x<-150 ||
            p.x>W+150 ||
            p.y<-150 ||
            p.y>H+150
        )
            continue;


        ctx.save();

        ctx.translate(
            p.x,
            p.y
        );


        if(
            s.type===
            "station"
        ){

            ctx.strokeStyle =
                "#75a9ff";

            ctx.lineWidth=3;

            ctx.beginPath();

            ctx.arc(
                0,
                0,
                42,
                0,
                Math.PI*2
            );

            ctx.stroke();

            ctx.fillStyle =
                "#6b91dc";

            ctx.fillRect(
                -12,
                -12,
                24,
                24
            );

        }else if(
            s.type===
            "mining_colony"
        ){

            ctx.fillStyle =
                "#c99550";

            ctx.fillRect(
                -28,
                -16,
                56,
                32
            );

            ctx.strokeStyle =
                "#d8b16e";

            ctx.strokeRect(
                -35,
                -25,
                70,
                50
            );

        }else if(
            s.type===
            "pirate_base"
        ){

            ctx.fillStyle =
                "#b64bff";

            ctx.beginPath();

            ctx.moveTo(
                0,
                -40
            );

            ctx.lineTo(
                35,
                20
            );

            ctx.lineTo(
                -35,
                20
            );

            ctx.closePath();

            ctx.fill();

        }else if(
            s.type===
            "alien_ruin"
        ){

            ctx.strokeStyle =
                "#59e6d4";

            ctx.lineWidth=4;

            ctx.beginPath();

            ctx.arc(
                0,
                0,
                35,
                0,
                Math.PI*2
            );

            ctx.stroke();

            ctx.beginPath();

            ctx.arc(
                0,
                0,
                15,
                0,
                Math.PI*2
            );

            ctx.stroke();

        }else{

            ctx.fillStyle =
                "#657087";

            ctx.rotate(
                .5
            );

            ctx.fillRect(
                -25,
                -15,
                50,
                30
            );
        }


        ctx.restore();
    }
}


/* ============================================================
   DRAW PLAYER
============================================================ */

function drawPlayer(){

    const s =
        worldToScreen(
            player.x,
            player.y
        );

    ctx.save();

    const sx =
        (
            Math.random()-.5
        )*
        shake;

    const sy =
        (
            Math.random()-.5
        )*
        shake;

    ctx.translate(
        s.x+sx,
        s.y+sy
    );

    ctx.rotate(
        player.angle
    );


    /* Engine */

    const moving =
        Math.hypot(
            player.vx,
            player.vy
        )>30;

    if(
        moving
    ){

        const flame =
            15+
            Math.random()*15;

        ctx.fillStyle =
            "#55c9ff";

        ctx.beginPath();

        ctx.moveTo(
            -25,
            -7
        );

        ctx.lineTo(
            -25-flame,
            0
        );

        ctx.lineTo(
            -25,
            7
        );

        ctx.closePath();

        ctx.fill();
    }


    /* Ship */

    ctx.fillStyle =
        "#d8e5ff";

    ctx.beginPath();

    ctx.moveTo(
        30,
        0
    );

    ctx.lineTo(
        -20,
        -17
    );

    ctx.lineTo(
        -12,
        0
    );

    ctx.lineTo(
        -20,
        17
    );

    ctx.closePath();

    ctx.fill();


    /* Wings */

    ctx.fillStyle =
        "#7188b5";

    ctx.beginPath();

    ctx.moveTo(
        -4,
        -5
    );

    ctx.lineTo(
        -18,
        -30
    );

    ctx.lineTo(
        8,
        -10
    );

    ctx.closePath();

    ctx.fill();

    ctx.beginPath();

    ctx.moveTo(
        -4,
        5
    );

    ctx.lineTo(
        -18,
        30
    );

    ctx.lineTo(
        8,
        10
    );

    ctx.closePath();

    ctx.fill();


    /* Cockpit */

    ctx.fillStyle =
        "#5dd8ff";

    ctx.beginPath();

    ctx.arc(
        7,
        0,
        6,
        0,
        Math.PI*2
    );

    ctx.fill();


    /* Shield */

    if(
        player.shield>0
    ){

        ctx.strokeStyle =
            "rgba(80,180,255,.35)";

        ctx.lineWidth=2;

        ctx.beginPath();

        ctx.arc(
            0,
            0,
            35,
            0,
            Math.PI*2
        );

        ctx.stroke();
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

        const s =
            worldToScreen(
                e.x,
                e.y
            );

        if(
            s.x<-100 ||
            s.x>W+100 ||
            s.y<-100 ||
            s.y>H+100
        )
            continue;


        ctx.save();

        ctx.translate(
            s.x,
            s.y
        );


        const angle =
            Math.atan2(
                player.y-e.y,
                player.x-e.x
            );

        ctx.rotate(
            angle
        );


        ctx.fillStyle =
            e.color;


        if(
            e.boss
        ){

            ctx.beginPath();

            ctx.moveTo(
                60,
                0
            );

            ctx.lineTo(
                -30,
                -45
            );

            ctx.lineTo(
                -60,
                0
            );

            ctx.lineTo(
                -30,
                45
            );

            ctx.closePath();

            ctx.fill();


            ctx.strokeStyle =
                "rgba(255,255,255,.5)";

            ctx.lineWidth=3;

            ctx.stroke();

        }else{

            ctx.beginPath();

            ctx.moveTo(
                e.radius,
                0
            );

            ctx.lineTo(
                -e.radius,
                -e.radius*.65
            );

            ctx.lineTo(
                -e.radius*.7,
                0
            );

            ctx.lineTo(
                -e.radius,
                e.radius*.65
            );

            ctx.closePath();

            ctx.fill();
        }


        ctx.restore();


        /* HP bar */

        if(
            e.hp<e.maxHp ||
            e.boss
        ){

            const width =
                e.radius*2.5;

            ctx.fillStyle =
                "#10131d";

            ctx.fillRect(
                s.x-width/2,
                s.y-e.radius-10,
                width,
                4
            );

            ctx.fillStyle =
                e.boss
                    ? "#ff314d"
                    : "#ff4f61";

            ctx.fillRect(
                s.x-width/2,
                s.y-e.radius-10,
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

        const s =
            worldToScreen(
                b.x,
                b.y
            );

        ctx.fillStyle =
            b.weapon==="plasma"
                ? "#d178ff"
                : "#c4ddff";

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

        const s =
            worldToScreen(
                b.x,
                b.y
            );

        ctx.fillStyle =
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

        const s =
            worldToScreen(
                p.x,
                p.y
            );

        ctx.fillStyle =
            p.type==="shield"
                ? "#65b9ff"
                : "#c96bff";

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

        const s =
            worldToScreen(
                p.x,
                p.y
            );

        ctx.globalAlpha =
            Math.max(
                0,
                p.life/
                p.maxLife
            );

        ctx.fillStyle =
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

    const w =
        minimap.width;

    const h =
        minimap.height;

    mctx.clearRect(
        0,
        0,
        w,
        h
    );

    mctx.fillStyle =
        "#02050d";

    mctx.fillRect(
        0,
        0,
        w,
        h
    );


    mctx.strokeStyle =
        "rgba(100,140,255,.15)";


    for(
        let i=-4;
        i<=4;
        i++
    ){

        mctx.beginPath();

        mctx.moveTo(
            w/2+i*20,
            0
        );

        mctx.lineTo(
            w/2+i*20,
            h
        );

        mctx.stroke();


        mctx.beginPath();

        mctx.moveTo(
            0,
            h/2+i*20
        );

        mctx.lineTo(
            w,
            h/2+i*20
        );

        mctx.stroke();
    }


    /* Player */

    mctx.fillStyle =
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

    mctx.fillStyle =
        "#ff5968";

    for(
        const e of enemies
    ){

        const dx =
            (
                e.x-player.x
            )/30;

        const dy =
            (
                e.y-player.y
            )/30;

        if(
            Math.abs(dx)<w/2 &&
            Math.abs(dy)<h/2
        ){

            mctx.beginPath();

            mctx.arc(
                w/2+dx,
                h/2+dy,
                e.boss
                    ? 5
                    : 3,
                0,
                Math.PI*2
            );

            mctx.fill();
        }
    }


    /* Structures */

    mctx.fillStyle =
        "#728cff";

    for(
        const s of structures
    ){

        const dx =
            (s.x-player.x)/30;

        const dy =
            (s.y-player.y)/30;

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

    const hullPercent =
        Math.max(
            0,
            player.hull/
            player.maxHull*
            100
        );

    const shieldPercent =
        Math.max(
            0,
            player.shield/
            player.maxShield*
            100
        );

    const energyPercent =
        Math.max(
            0,
            player.energy/
            player.maxEnergy*
            100
        );

    const xpPercent =
        Math.min(
            100,
            player.xp/
            xpRequired()*
            100
        );


    document.getElementById(
        "hullBar"
    ).style.width =
        hullPercent+"%";

    document.getElementById(
        "shieldBar"
    ).style.width =
        shieldPercent+"%";

    document.getElementById(
        "energyBar"
    ).style.width =
        energyPercent+"%";

    document.getElementById(
        "xpBar"
    ).style.width =
        xpPercent+"%";


    document.getElementById(
        "hullValue"
    ).textContent =
        Math.ceil(
            player.hull
        );

    document.getElementById(
        "shieldValue"
    ).textContent =
        Math.ceil(
            player.shield
        );

    document.getElementById(
        "energyValue"
    ).textContent =
        Math.ceil(
            player.energy
        );

    document.getElementById(
        "xpValue"
    ).textContent =
        Math.floor(
            player.xp
        );


    document.getElementById(
        "creditsText"
    ).textContent =
        player.credits;

    document.getElementById(
        "killsText"
    ).textContent =
        player.kills;

    document.getElementById(
        "levelText"
    ).textContent =
        "LEVEL " +
        player.level;


    const weaponNames = {

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
    ).textContent =
        weaponNames[
            player.weapon
        ];
}


/* ============================================================
   MAIN LOOP
============================================================ */

function gameLoop(now){

    requestAnimationFrame(
        gameLoop
    );

    let dt =
        (
            now-lastTime
        )/1000;

    lastTime=now;

    dt =
        Math.min(
            .033,
            Math.max(
                0,
                dt
            )
        );

    if(
        !gameRunning ||
        paused
    )
        return;

    elapsed += dt;


    updatePlayer(dt);

    updateEnemies(dt);

    updateBullets(dt);

    updateEnemyBullets(dt);

    updateResources();

    updateStructures();

    updatePickups();

    updateParticles(dt);


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

requestAnimationFrame(
    gameLoop
);


/* ============================================================
   UI
============================================================ */

function showScreen(id){

    document
        .querySelectorAll(".screen")
        .forEach(
            element =>
                element.classList.add(
                    "hidden"
                )
        );


    if(id){

        const screen =
            document.getElementById(
                id
            );

        if(screen)
            screen.classList.remove(
                "hidden"
            );
    }


    if(
        id==="pause" ||
        id==="inventory"
    ){

        document.getElementById(
            "hud"
        ).classList.remove(
            "hidden"
        );

    }else{

        document.getElementById(
            "hud"
        ).classList.add(
            "hidden"
        );
    }
}


function resumeFromOverlay(){

    document
        .querySelectorAll(".screen")
        .forEach(
            element =>
                element.classList.add(
                    "hidden"
                )
        );

    if(gameRunning){

        document.getElementById(
            "hud"
        ).classList.remove(
            "hidden"
        );
    }
}


/* ============================================================
   NEW GAME
============================================================ */

function newGame(){

    const input =
        document.getElementById(
            "seedInput"
        );

    worldSeed =
        input.value.trim();


    if(!worldSeed){

        worldSeed =
            "VOID-" +
            Math.floor(
                Math.random()*
                999999999
            );
    }


    input.value =
        worldSeed;


    player = {

        x:0,
        y:0,

        vx:0,
        vy:0,

        angle:0,
        targetAngle:0,

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
    structures=[];
    resources=[];

    activeChunks.clear();

    currentChunk={
        x:999999,
        y:999999
    };

    lastLoadedChunkKey="";

    camera={
        x:0,
        y:0
    };


    localStorage.removeItem(
        "VOID_SPACE_SAVE"
    );


    buildStars();

    startGame();

    saveWorldState();

    showEvent(
        "NEW UNIVERSE • " +
        worldSeed
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
            element =>
                element.classList.add(
                    "hidden"
                )
        );

    document.getElementById(
        "hud"
    ).classList.remove(
        "hidden"
    );


    buildStars();

    loadNearbyChunks();

    camera.x =
        player.x;

    camera.y =
        player.y;
}


/* ============================================================
   CONTINUE
============================================================ */

function continueGame(){

    const saved =
        localStorage.getItem(
            "VOID_SPACE_SAVE"
        );


    if(!saved){

        newGame();

        return;
    }


    try{

        const data =
            JSON.parse(
                saved
            );


        worldSeed =
            data.seed ||
            worldSeed;


        player =
            data.player ||
            player;


        document.getElementById(
            "seedInput"
        ).value =
            worldSeed;


        bullets=[];
        enemyBullets=[];
        enemies=[];
        particles=[];
        pickups=[];

        activeChunks.clear();

        currentChunk={
            x:999999,
            y:999999
        };

        lastLoadedChunkKey="";


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
   INVENTORY
============================================================ */

function showInventory(){

    const grid =
        document.getElementById(
            "inventoryGrid"
        );

    grid.innerHTML="";


    for(
        const key in
        player.inventory
    ){

        const div =
            document.createElement(
                "div"
            );

        div.className =
            "item";

        div.innerHTML =
            "<b>" +
            key.toUpperCase() +
            "</b>" +
            "<span>" +
            player.inventory[key] +
            "</span>";

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

    if(
        !gameRunning
    )
        return;


    paused =
        !paused;


    if(paused){

        showScreen(
            "pause"
        );

    }else{

        resumeFromOverlay();
    }
}


/* ============================================================
   GAME OVER
============================================================ */

function gameOver(){

    gameRunning=false;

    paused=false;


    document.getElementById(
        "gameOverText"
    ).innerHTML =

        "LEVEL " +
        player.level +
        "<br>" +

        "KILLS " +
        player.kills +
        "<br>" +

        "CREDITS " +
        player.credits +
        "<br>" +

        "SECTOR " +
        currentChunk.x +
        " : " +
        currentChunk.y;


    saveWorldState();

    showScreen(
        "gameover"
    );
}


/* ============================================================
   EVENTS
============================================================ */

function showEvent(text){

    const el =
        document.getElementById(
            "eventText"
        );

    el.textContent =
        text;

    el.classList.add(
        "show"
    );


    clearTimeout(
        showEvent.timer
    );


    showEvent.timer =
        setTimeout(
            ()=>{
                el.classList.remove(
                    "show"
                );
            },
            3200
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
            [
                " ",
                "arrowup",
                "arrowdown",
                "arrowleft",
                "arrowright"
            ].includes(
                e.key.toLowerCase()
            )
        ){

            e.preventDefault();
        }


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

        mouse.x =
            e.clientX;

        mouse.y =
            e.clientY;


        aimPlayer(
            mouse.x,
            mouse.y
        );


        const cross =
            document.getElementById(
                "crosshair"
            );

        cross.style.display =
            "block";

        cross.style.left =
            e.clientX+"px";

        cross.style.top =
            e.clientY+"px";
    }
);


canvas.addEventListener(
    "mousedown",
    e=>{

        if(e.button===0){

            mouse.down=true;

            aimPlayer(
                e.clientX,
                e.clientY
            );
        }
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
   TOUCH AIM
============================================================ */

canvas.addEventListener(
    "pointermove",
    e=>{

        if(
            e.pointerType==="touch"
        ){

            mobile.aimX =
                e.clientX;

            mobile.aimY =
                e.clientY;

            mobile.aiming=true;

            aimPlayer(
                e.clientX,
                e.clientY
            );
        }
    }
);


canvas.addEventListener(
    "pointerdown",
    e=>{

        if(
            e.pointerType==="touch"
        ){

            mobile.aimX =
                e.clientX;

            mobile.aimY =
                e.clientY;

            mobile.aiming=true;

            aimPlayer(
                e.clientX,
                e.clientY
            );
        }
    }
);


canvas.addEventListener(
    "pointerup",
    e=>{

        if(
            e.pointerType==="touch"
        ){

            mobile.aiming=false;
        }
    }
);


/* ============================================================
   MOBILE JOYSTICK
============================================================ */

const joystick =
    document.getElementById(
        "joystick"
    );

const stick =
    document.getElementById(
        "stick"
    );

let joystickPointer = null;


function updateJoystick(
    clientX,
    clientY
){

    const rect =
        joystick.getBoundingClientRect();

    let x =
        clientX -
        (
            rect.left+
            rect.width/2
        );

    let y =
        clientY -
        (
            rect.top+
            rect.height/2
        );


    const max =
        45;

    const distance =
        Math.hypot(
            x,
            y
        );


    if(
        distance>max
    ){

        x =
            x/distance*
            max;

        y =
            y/distance*
            max;
    }


    mobile.x =
        x/max;

    mobile.y =
        y/max;


    stick.style.transform =
        "translate(" +
        x +
        "px," +
        y +
        "px)";
}


function resetJoystick(){

    joystickPointer=null;

    mobile.x=0;
    mobile.y=0;

    stick.style.transform =
        "";
}


joystick.addEventListener(
    "pointerdown",
    e=>{

        e.preventDefault();

        joystickPointer =
            e.pointerId;

        joystick.setPointerCapture(
            e.pointerId
        );

        updateJoystick(
            e.clientX,
            e.clientY
        );
    }
);


joystick.addEventListener(
    "pointermove",
    e=>{

        if(
            e.pointerId===
            joystickPointer
        ){

            updateJoystick(
                e.clientX,
                e.clientY
            );
        }
    }
);


joystick.addEventListener(
    "pointerup",
    resetJoystick
);

joystick.addEventListener(
    "pointercancel",
    resetJoystick
);


/* ============================================================
   FIRE BUTTON
============================================================ */

const fireBtn =
    document.getElementById(
        "fireBtn"
    );


fireBtn.addEventListener(
    "pointerdown",
    e=>{

        e.preventDefault();

        mobile.fire=true;

        fireBtn.setPointerCapture(
            e.pointerId
        );
    }
);


fireBtn.addEventListener(
    "pointerup",
    ()=>{

        mobile.fire=false;
    }
);


fireBtn.addEventListener(
    "pointercancel",
    ()=>{

        mobile.fire=false;
    }
);


/* ============================================================
   BOOST BUTTON
============================================================ */

const boostBtn =
    document.getElementById(
        "boostBtn"
    );


boostBtn.addEventListener(
    "pointerdown",
    e=>{

        e.preventDefault();

        mobile.boost=true;

        boostBtn.setPointerCapture(
            e.pointerId
        );
    }
);


boostBtn.addEventListener(
    "pointerup",
    ()=>{

        mobile.boost=false;
    }
);


boostBtn.addEventListener(
    "pointercancel",
    ()=>{

        mobile.boost=false;
    }
);


/* ============================================================
   MOBILE HUD
============================================================ */

document.getElementById(
    "mobileInventory"
).addEventListener(
    "click",
    ()=>{
        if(gameRunning)
            showInventory();
    }
);


document.getElementById(
    "mobilePause"
).addEventListener(
    "click",
    ()=>{
        if(gameRunning)
            togglePause();
    }
);


/* ============================================================
   PREVENT MOBILE GESTURES
============================================================ */

document.addEventListener(
    "contextmenu",
    e=>{
        e.preventDefault();
    }
);


document.addEventListener(
    "gesturestart",
    e=>{
        e.preventDefault();
    }
);


document.addEventListener(
    "touchmove",
    e=>{

        if(
            e.target.closest(
                "#touchUI"
            ) ||
            e.target===canvas
        ){

            e.preventDefault();
        }
    },
    {
        passive:false
    }
);


/* ============================================================
   INITIALIZATION
============================================================ */

document.getElementById(
    "seedInput"
).value =
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
# SERVER-SIDE DETERMINISTIC RNG
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


# ============================================================
# SERVER-SIDE SECTOR GENERATOR
# ============================================================

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
            rng.choice(
                names
            )
            + "-"
            + str(
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

        "planets": [],

        "structures": [],

        "resources": []
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

    planet_count =
        rng.randint(
            1,
            6
        )

    for i in range(
        planet_count
    ):

        sector["planets"].append({

            "name":
                f"{chr(65 + i)}-"
                f"{rng.randint(10, 99)}",

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

    structure_count =
        rng.randint(
            1,
            6
        )

    for i in range(
        structure_count
    ):

        sector["structures"].append({

            "id":
                f"S-{x}-{y}-{i}",

            "type":
                rng.choice(
                    structure_types
                ),

            "x":
                round(
                    rng.uniform(
                        -2200,
                        2200
                    ),
                    2
                ),

            "y":
                round(
                    rng.uniform(
                        -2200,
                        2200
                    ),
                    2
                ),

            "radius":
                rng.randint(
                    40,
                    100
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

    resource_count =
        rng.randint(
            8,
            25
        )

    for i in range(
        resource_count
    ):

        sector["resources"].append({

            "id":
                f"R-{x}-{y}-{i}",

            "type":
                rng.choice(
                    resource_types
                ),

            "x":
                round(
                    rng.uniform(
                        -2450,
                        2450
                    ),
                    2
                ),

            "y":
                round(
                    rng.uniform(
                        -2450,
                        2450
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
# HOME
# ============================================================

@app.route("/")
def index():

    return render_template_string(
        HTML
    )


# ============================================================
# HEALTH
# ============================================================

@app.route("/health")
def health():

    return "VOID SPACE ONLINE"


# ============================================================
# SECTOR API
# ============================================================

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


# ============================================================
# WORLD API
# ============================================================

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

        radius = 1


    radius = max(
        1,
        min(
            radius,
            5
        )
    )


    sectors = []


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


# ============================================================
# GALAXY API
# ============================================================

@app.route("/api/galaxy")
def api_galaxy():

    seed = request.args.get(
        "seed",
        "VOID-829174"
    )

    rng = deterministic_rng(
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

    port = int(
        os.environ.get(
            "PORT",
            "10000"
        )
    )

    app.run(

        host="0.0.0.0",

        port=port,

        debug=False
    )
