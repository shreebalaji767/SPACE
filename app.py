from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width,
             initial-scale=1.0,
             maximum-scale=1.0,
             user-scalable=no,
             viewport-fit=cover"
>

<meta name="theme-color" content="#030712">

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
}

html,
body {
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #02040a;
    color: #ffffff;
    font-family:
        Inter,
        Arial,
        Helvetica,
        sans-serif;
}

body {
    touch-action: none;
    user-select: none;
}


/* =========================================================
   GAME ROOT
========================================================= */

#gameRoot {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100dvh;
    overflow: hidden;
    background:
        radial-gradient(
            circle at center,
            #071326 0%,
            #030712 45%,
            #010207 100%
        );
}


/* =========================================================
   CANVAS
========================================================= */

#gameCanvas {
    position: absolute;
    inset: 0;

    width: 100%;
    height: 100%;

    display: block;

    touch-action: none;
}


/* =========================================================
   TOP HUD
========================================================= */

#hud {
    position: absolute;

    top:
        max(
            10px,
            env(safe-area-inset-top)
        );

    left: 0;
    right: 0;

    padding:
        12px
        clamp(10px, 2vw, 28px);

    display: flex;
    justify-content: space-between;
    align-items: flex-start;

    pointer-events: none;

    z-index: 20;
}


.hudLeft,
.hudRight {
    display: flex;
    flex-direction: column;
    gap: 7px;
}


.hudRight {
    align-items: flex-end;
}


.hudBox {
    min-width: 100px;

    padding: 7px 12px;

    border:
        1px solid
        rgba(130, 210, 255, 0.18);

    border-radius: 10px;

    background:
        rgba(3, 10, 24, 0.72);

    backdrop-filter: blur(8px);

    box-shadow:
        0 0 20px
        rgba(0, 160, 255, 0.08);
}


.hudLabel {
    display: block;

    font-size: 9px;
    letter-spacing: 2px;

    color: #6e91ac;

    text-transform: uppercase;
}


.hudValue {
    display: block;

    margin-top: 2px;

    font-size: clamp(13px, 2vw, 18px);

    font-weight: 800;

    letter-spacing: 1px;
}


/* =========================================================
   HEALTH / ENERGY
========================================================= */

.bars {
    width:
        clamp(140px, 22vw, 260px);

    display: flex;
    flex-direction: column;

    gap: 5px;
}


.bar {
    position: relative;

    height: 7px;

    overflow: hidden;

    border-radius: 10px;

    background:
        rgba(255,255,255,0.08);
}


.barFill {
    width: 100%;
    height: 100%;

    transform-origin: left center;

    transition:
        transform .12s linear;
}


#healthFill {
    background:
        linear-gradient(
            90deg,
            #ff3158,
            #ff7b7b
        );
}


#energyFill {
    background:
        linear-gradient(
            90deg,
            #1eb7ff,
            #8cecff
        );
}


/* =========================================================
   BOSS BAR
========================================================= */

#bossHud {
    position: absolute;

    left: 50%;
    top:
        max(
            78px,
            calc(
                env(safe-area-inset-top) + 70px
            )
        );

    width:
        min(
            600px,
            calc(100vw - 30px)
        );

    transform:
        translateX(-50%);

    z-index: 21;

    pointer-events: none;

    display: none;
}


#bossHud.visible {
    display: block;
}


#bossName {
    text-align: center;

    margin-bottom: 5px;

    font-size: 11px;

    font-weight: 900;

    letter-spacing: 4px;

    color: #ff7187;
}


#bossBar {
    height: 10px;

    overflow: hidden;

    border:
        1px solid
        rgba(255, 90, 120, .35);

    border-radius: 10px;

    background:
        rgba(20, 0, 8, .75);
}


#bossFill {
    width: 100%;
    height: 100%;

    transform-origin: left center;

    background:
        linear-gradient(
            90deg,
            #ff173e,
            #ff7b2f,
            #ff174f
        );

    box-shadow:
        0 0 18px
        rgba(255, 30, 70, .8);
}


/* =========================================================
   CROSSHAIR
========================================================= */

#crosshair {
    position: absolute;

    width: 25px;
    height: 25px;

    pointer-events: none;

    z-index: 18;

    display: none;

    transform:
        translate(-50%, -50%);
}


#crosshair.visible {
    display: block;
}


#crosshair::before,
#crosshair::after {
    content: "";

    position: absolute;

    background:
        rgba(140, 230, 255, .75);
}


#crosshair::before {
    width: 25px;
    height: 1px;

    top: 12px;
    left: 0;
}


#crosshair::after {
    width: 1px;
    height: 25px;

    top: 0;
    left: 12px;
}


.crossDot {
    position: absolute;

    width: 4px;
    height: 4px;

    border-radius: 50%;

    left: 10px;
    top: 10px;

    background: #ffffff;

    box-shadow:
        0 0 8px #55ddff;
}


/* =========================================================
   SCREENS
========================================================= */

.screen {
    position: absolute;

    inset: 0;

    z-index: 50;

    display: flex;

    align-items: center;
    justify-content: center;

    padding:
        20px
        max(20px, env(safe-area-inset-right))
        max(20px, env(safe-area-inset-bottom))
        max(20px, env(safe-area-inset-left));

    background:
        radial-gradient(
            circle at center,
            rgba(5, 25, 55, .45),
            rgba(0, 0, 0, .86)
        );

    backdrop-filter: blur(8px);
}


.screen.hidden {
    display: none;
}


.panel {
    width:
        min(
            620px,
            100%
        );

    max-height: 90dvh;

    overflow-y: auto;

    padding:
        clamp(22px, 5vw, 48px);

    border:
        1px solid
        rgba(80, 200, 255, .2);

    border-radius:
        clamp(16px, 3vw, 28px);

    background:
        linear-gradient(
            145deg,
            rgba(7, 19, 38, .94),
            rgba(2, 6, 17, .97)
        );

    box-shadow:
        0 0 80px
        rgba(0, 130, 255, .12);

    text-align: center;
}


.logo {
    font-size:
        clamp(
            42px,
            10vw,
            86px
        );

    font-weight: 1000;

    letter-spacing:
        clamp(4px, 1vw, 10px);

    line-height: .9;

    color: #ffffff;

    text-shadow:
        0 0 15px rgba(80, 210, 255, .7),
        0 0 50px rgba(0, 120, 255, .3);
}


.subtitle {
    margin-top: 16px;

    color: #6d91ad;

    font-size:
        clamp(10px, 2vw, 14px);

    letter-spacing: 4px;

    text-transform: uppercase;
}


.buttonGrid {
    display: grid;

    grid-template-columns:
        repeat(
            2,
            minmax(0, 1fr)
        );

    gap: 10px;

    margin-top: 28px;
}


button {
    min-height: 48px;

    border:
        1px solid
        rgba(100, 210, 255, .22);

    border-radius: 12px;

    background:
        rgba(12, 35, 59, .9);

    color: #ffffff;

    font-weight: 800;

    letter-spacing: 1px;

    cursor: pointer;

    transition:
        transform .12s,
        background .12s,
        border-color .12s;
}


button:hover {
    background:
        rgba(20, 62, 95, .95);

    border-color:
        rgba(110, 225, 255, .55);
}


button:active {
    transform: scale(.96);
}


.primary {
    grid-column: 1 / -1;

    background:
        linear-gradient(
            135deg,
            #07557a,
            #0875a4
        );

    border-color:
        rgba(120, 235, 255, .55);

    box-shadow:
        0 0 25px
        rgba(0, 180, 255, .15);
}


.info {
    margin-top: 22px;

    padding: 16px;

    border-radius: 12px;

    background:
        rgba(255,255,255,.035);

    color: #91aabd;

    font-size: 12px;

    line-height: 1.7;
}


.controls {
    margin-top: 20px;

    display: grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(130px, 1fr)
        );

    gap: 8px;

    text-align: left;
}


.control {
    padding: 10px;

    border:
        1px solid
        rgba(100,180,220,.12);

    border-radius: 10px;

    background:
        rgba(255,255,255,.025);
}


.control strong {
    display: block;

    color: #dff8ff;

    font-size: 12px;
}


.control span {
    display: block;

    margin-top: 3px;

    color: #66859a;

    font-size: 10px;
}


/* =========================================================
   SETTINGS
========================================================= */

.settingRow {
    display: flex;

    align-items: center;
    justify-content: space-between;

    gap: 20px;

    padding: 14px 0;

    border-bottom:
        1px solid
        rgba(255,255,255,.07);

    text-align: left;
}


.settingRow:last-child {
    border-bottom: 0;
}


.settingText strong {
    display: block;

    font-size: 13px;
}


.settingText span {
    display: block;

    margin-top: 4px;

    color: #67859a;

    font-size: 10px;
}


.toggle {
    position: relative;

    width: 50px;
    height: 28px;

    flex-shrink: 0;

    border-radius: 30px;

    background:
        #182332;

    border:
        1px solid
        rgba(255,255,255,.1);

    cursor: pointer;
}


.toggle.on {
    background:
        #0877a7;
}


.toggle::after {
    content: "";

    position: absolute;

    top: 3px;
    left: 3px;

    width: 20px;
    height: 20px;

    border-radius: 50%;

    background: #ffffff;

    transition:
        transform .15s;
}


.toggle.on::after {
    transform:
        translateX(22px);
}


/* =========================================================
   GAME OVER
========================================================= */

.resultTitle {
    font-size:
        clamp(32px, 8vw, 62px);

    font-weight: 1000;

    letter-spacing: 4px;
}


.resultStats {
    margin: 22px 0;

    display: grid;

    grid-template-columns:
        repeat(2, 1fr);

    gap: 8px;
}


.resultStat {
    padding: 15px;

    border-radius: 12px;

    background:
        rgba(255,255,255,.035);
}


.resultStat span {
    display: block;

    color: #648196;

    font-size: 9px;

    letter-spacing: 2px;
}


.resultStat strong {
    display: block;

    margin-top: 4px;

    font-size: 22px;
}


/* =========================================================
   MOBILE CONTROLS
========================================================= */

#touchControls {
    position: absolute;

    inset: 0;

    z-index: 30;

    pointer-events: none;

    display: none;
}


.touchButton {
    position: absolute;

    pointer-events: auto;

    border-radius: 50%;

    display: flex;

    align-items: center;
    justify-content: center;

    font-size: 10px;

    font-weight: 900;

    letter-spacing: 1px;

    color: rgba(255,255,255,.85);

    background:
        rgba(10, 35, 55, .55);

    border:
        1px solid
        rgba(120, 220, 255, .3);

    backdrop-filter: blur(6px);

    box-shadow:
        inset 0 0 20px
        rgba(0,160,255,.08);
}


#fireButton {
    right:
        max(
            25px,
            env(safe-area-inset-right)
        );

    bottom:
        max(
            35px,
            env(safe-area-inset-bottom)
        );

    width: 82px;
    height: 82px;
}


#boostButton {
    right:
        max(
            120px,
            calc(
                env(safe-area-inset-right) + 110px
            )
        );

    bottom:
        max(
            28px,
            env(safe-area-inset-bottom)
        );

    width: 62px;
    height: 62px;
}


#bombButton {
    right:
        max(
            120px,
            calc(
                env(safe-area-inset-right) + 110px
            )
        );

    bottom:
        max(
            100px,
            calc(
                env(safe-area-inset-bottom) + 95px
            )
        );

    width: 50px;
    height: 50px;

    display: none;
}


#joystick {
    position: absolute;

    left:
        max(
            25px,
            env(safe-area-inset-left)
        );

    bottom:
        max(
            30px,
            env(safe-area-inset-bottom)
        );

    width: 130px;
    height: 130px;

    pointer-events: auto;

    border-radius: 50%;

    border:
        1px solid
        rgba(100,210,255,.2);

    background:
        rgba(10,30,48,.38);
}


#joystickKnob {
    position: absolute;

    left: 50%;
    top: 50%;

    width: 58px;
    height: 58px;

    transform:
        translate(-50%, -50%);

    border-radius: 50%;

    background:
        rgba(40,150,205,.45);

    border:
        1px solid
        rgba(140,230,255,.5);

    box-shadow:
        0 0 20px
        rgba(0,170,255,.15);
}


/* =========================================================
   PAUSE BUTTON
========================================================= */

#pauseButton {
    position: absolute;

    top:
        max(
            12px,
            env(safe-area-inset-top)
        );

    right:
        max(
            12px,
            env(safe-area-inset-right)
        );

    z-index: 25;

    width: 42px;
    height: 42px;

    min-height: 42px;

    border-radius: 50%;

    display: none;

    font-size: 15px;
}


/* =========================================================
   DEVICE ADAPTATION
========================================================= */

@media
(pointer: coarse),
(max-width: 900px) {

    #touchControls {
        display: block;
    }

    #pauseButton {
        display: block;
    }

    #crosshair {
        display: none !important;
    }

    .hudBox {
        min-width: 80px;
        padding: 6px 9px;
    }

    .hudLabel {
        font-size: 8px;
    }

    .hudValue {
        font-size: 12px;
    }

}


@media
(pointer: fine)
and (min-width: 901px) {

    #crosshair.visible {
        display: block;
    }

}


@media (max-width: 600px) {

    .panel {
        padding: 22px 16px;
    }

    .buttonGrid {
        grid-template-columns: 1fr;
    }

    .primary {
        grid-column: auto;
    }

    .hud {
        padding-left: 8px;
        padding-right: 8px;
    }

    .hudBox {
        min-width: 70px;
    }

    .resultStats {
        grid-template-columns: 1fr 1fr;
    }

}


@media (max-width: 390px) {

    #joystick {
        width: 110px;
        height: 110px;
    }

    #joystickKnob {
        width: 50px;
        height: 50px;
    }

    #fireButton {
        width: 70px;
        height: 70px;
    }

    #boostButton {
        right: 105px;
        width: 55px;
        height: 55px;
    }

}


/* =========================================================
   LANDSCAPE MOBILE
========================================================= */

@media
(max-height: 500px)
and (orientation: landscape) {

    .hud {
        padding-top: 5px;
    }

    #joystick {
        bottom: 15px;
    }

    #fireButton {
        bottom: 15px;
    }

    #boostButton {
        bottom: 15px;
    }

    .panel {
        max-height: 92dvh;
        padding: 15px 25px;
    }

    .logo {
        font-size: 42px;
    }

}


/* =========================================================
   ACCESSIBILITY
========================================================= */

button:focus-visible {
    outline:
        2px solid
        #65ddff;

    outline-offset: 3px;
}

</style>
</head>


<body>

<div id="gameRoot">

    <canvas id="gameCanvas"></canvas>

    <!-- =====================================================
         HUD
    ====================================================== -->

    <div id="hud">

        <div class="hudLeft">

            <div class="hudBox">
                <span class="hudLabel">Score</span>
                <span class="hudValue" id="scoreText">0</span>
            </div>

            <div class="hudBox">
                <span class="hudLabel">Wave</span>
                <span class="hudValue" id="waveText">1</span>
            </div>

            <div class="bars">

                <div class="bar">
                    <div
                        id="healthFill"
                        class="barFill"
                    ></div>
                </div>

                <div class="bar">
                    <div
                        id="energyFill"
                        class="barFill"
                    ></div>
                </div>

            </div>

        </div>


        <div class="hudRight">

            <div class="hudBox">
                <span class="hudLabel">Kills</span>
                <span class="hudValue" id="killsText">0</span>
            </div>

            <div class="hudBox">
                <span class="hudLabel">Combo</span>
                <span class="hudValue" id="comboText">x1</span>
            </div>

        </div>

    </div>


    <!-- =====================================================
         BOSS HUD
    ====================================================== -->

    <div id="bossHud">

        <div id="bossName">
            VOID OVERLORD
        </div>

        <div id="bossBar">

            <div id="bossFill"></div>

        </div>

    </div>


    <!-- =====================================================
         CROSSHAIR
    ====================================================== -->

    <div id="crosshair">

        <div class="crossDot"></div>

    </div>


    <!-- =====================================================
         PAUSE
    ====================================================== -->

    <button
        id="pauseButton"
        onclick="togglePause()"
    >
        II
    </button>


    <!-- =====================================================
         MAIN MENU
    ====================================================== -->

    <section
        id="menuScreen"
        class="screen"
    >

        <div class="panel">

            <div class="logo">
                VOID
                <br>
                SPACE
            </div>

            <div class="subtitle">
                Survive the infinite darkness
            </div>


            <div class="buttonGrid">

                <button
                    class="primary"
                    onclick="startGame()"
                >
                    START MISSION
                </button>

                <button
                    onclick="showScreen('howScreen')"
                >
                    HOW TO PLAY
                </button>

                <button
                    onclick="showScreen('settingsScreen')"
                >
                    SETTINGS
                </button>

                <button
                    onclick="toggleFullscreen()"
                >
                    FULLSCREEN
                </button>

            </div>


            <div class="info">

                Free browser game.<br>

                No database • No accounts •
                No paid assets • No API keys

            </div>

        </div>

    </section>


    <!-- =====================================================
         HOW TO PLAY
    ====================================================== -->

    <section
        id="howScreen"
        class="screen hidden"
    >

        <div class="panel">

            <div class="logo"
                 style="font-size:clamp(30px,7vw,52px)">
                HOW TO PLAY
            </div>


            <div class="controls">

                <div class="control">

                    <strong>
                        W / S
                    </strong>

                    <span>
                        Move forward / backward
                    </span>

                </div>


                <div class="control">

                    <strong>
                        A / D
                    </strong>

                    <span>
                        Rotate left / right
                    </span>

                </div>


                <div class="control">

                    <strong>
                        ARROW KEYS
                    </strong>

                    <span>
                        Alternative movement / rotation
                    </span>

                </div>


                <div class="control">

                    <strong>
                        SPACE / X
                    </strong>

                    <span>
                        Shoot
                    </span>

                </div>


                <div class="control">

                    <strong>
                        SHIFT
                    </strong>

                    <span>
                        Boost
                    </span>

                </div>


                <div class="control">

                    <strong>
                        P / ESC
                    </strong>

                    <span>
                        Pause
                    </span>

                </div>


                <div class="control">

                    <strong>
                        MOUSE
                    </strong>

                    <span>
                        Aim and left-click to shoot
                    </span>

                </div>


                <div class="control">

                    <strong>
                        TOUCH
                    </strong>

                    <span>
                        Joystick + FIRE + BOOST
                    </span>

                </div>

            </div>


            <div class="info">

                Destroy enemies, collect power-ups,
                survive waves and defeat the VOID OVERLORD.

                <br><br>

                Every fifth wave contains a boss.

            </div>


            <div class="buttonGrid">

                <button
                    class="primary"
                    onclick="showScreen('menuScreen')"
                >
                    BACK
                </button>

            </div>

        </div>

    </section>


    <!-- =====================================================
         SETTINGS
    ====================================================== -->

    <section
        id="settingsScreen"
        class="screen hidden"
    >

        <div class="panel">

            <div class="logo"
                 style="font-size:clamp(30px,7vw,52px)">
                SETTINGS
            </div>


            <div style="margin-top:25px">

                <div class="settingRow">

                    <div class="settingText">

                        <strong>
                            SOUND
                        </strong>

                        <span>
                            Web Audio sound effects
                        </span>

                    </div>

                    <div
                        id="soundToggle"
                        class="toggle on"
                        onclick="toggleSetting('sound')"
                    ></div>

                </div>


                <div class="settingRow">

                    <div class="settingText">

                        <strong>
                            SCREEN SHAKE
                        </strong>

                        <span>
                            Camera impact effects
                        </span>

                    </div>

                    <div
                        id="shakeToggle"
                        class="toggle on"
                        onclick="toggleSetting('shake')"
                    ></div>

                </div>


                <div class="settingRow">

                    <div class="settingText">

                        <strong>
                            PARTICLES
                        </strong>

                        <span>
                            Explosion and engine particles
                        </span>

                    </div>

                    <div
                        id="particlesToggle"
                        class="toggle on"
                        onclick="toggleSetting('particles')"
                    ></div>

                </div>

            </div>


            <div class="buttonGrid">

                <button
                    class="primary"
                    onclick="showScreen('menuScreen')"
                >
                    BACK
                </button>

            </div>

        </div>

    </section>


    <!-- =====================================================
         PAUSE
    ====================================================== -->

    <section
        id="pauseScreen"
        class="screen hidden"
    >

        <div class="panel">

            <div class="resultTitle">
                PAUSED
            </div>

            <div class="subtitle">
                Mission suspended
            </div>

            <div class="buttonGrid">

                <button
                    class="primary"
                    onclick="togglePause()"
                >
                    RESUME
                </button>

                <button
                    onclick="restartGame()"
                >
                    RESTART
                </button>

                <button
                    onclick="quitGame()"
                >
                    MAIN MENU
                </button>

            </div>

        </div>

    </section>


    <!-- =====================================================
         GAME OVER
    ====================================================== -->

    <section
        id="gameOverScreen"
        class="screen hidden"
    >

        <div class="panel">

            <div class="resultTitle">
                MISSION FAILED
            </div>

            <div class="subtitle">
                The void consumed your ship
            </div>


            <div class="resultStats">

                <div class="resultStat">

                    <span>
                        SCORE
                    </span>

                    <strong id="finalScore">
                        0
                    </strong>

                </div>


                <div class="resultStat">

                    <span>
                        WAVE
                    </span>

                    <strong id="finalWave">
                        1
                    </strong>

                </div>


                <div class="resultStat">

                    <span>
                        KILLS
                    </span>

                    <strong id="finalKills">
                        0
                    </strong>

                </div>


                <div class="resultStat">

                    <span>
                        TIME
                    </span>

                    <strong id="finalTime">
                        0:00
                    </strong>

                </div>

            </div>


            <div class="buttonGrid">

                <button
                    class="primary"
                    onclick="restartGame()"
                >
                    TRY AGAIN
                </button>

                <button
                    onclick="quitGame()"
                >
                    MAIN MENU
                </button>

            </div>

        </div>

    </section>


    <!-- =====================================================
         TOUCH CONTROLS
    ====================================================== -->

    <div id="touchControls">

        <div id="joystick">

            <div id="joystickKnob"></div>

        </div>


        <div
            id="fireButton"
            class="touchButton"
        >
            FIRE
        </div>


        <div
            id="boostButton"
            class="touchButton"
        >
            BOOST
        </div>


        <div
            id="bombButton"
            class="touchButton"
        >
            BOMB
        </div>

    </div>

</div>


<script>

/* =========================================================
   CANVAS
========================================================= */

const canvas =
    document.getElementById("gameCanvas");

const ctx =
    canvas.getContext("2d", {
        alpha: false
    });


let W = 0;
let H = 0;
let DPR = 1;


function resizeCanvas() {

    DPR =
        Math.min(
            window.devicePixelRatio || 1,
            2
        );

    W =
        window.innerWidth;

    H =
        window.innerHeight;


    canvas.width =
        Math.floor(W * DPR);

    canvas.height =
        Math.floor(H * DPR);


    canvas.style.width =
        W + "px";

    canvas.style.height =
        H + "px";


    ctx.setTransform(
        DPR,
        0,
        0,
        DPR,
        0,
        0
    );


    if (player) {

        player.x =
            clamp(
                player.x,
                20,
                W - 20
            );

        player.y =
            clamp(
                player.y,
                20,
                H - 20
            );

    }

}


window.addEventListener(
    "resize",
    resizeCanvas
);


/* =========================================================
   UTILITY
========================================================= */

function clamp(v, a, b) {

    return Math.max(
        a,
        Math.min(b, v)
    );

}


function rand(a, b) {

    return Math.random() *
        (b - a) + a;

}


function randInt(a, b) {

    return Math.floor(
        rand(a, b + 1)
    );

}


function dist(a, b) {

    return Math.hypot(
        a.x - b.x,
        a.y - b.y
    );

}


function formatTime(seconds) {

    const m =
        Math.floor(seconds / 60);

    const s =
        Math.floor(seconds % 60);

    return (
        m +
        ":" +
        String(s).padStart(2, "0")
    );

}


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

let player;

let enemies = [];
let bullets = [];
let enemyBullets = [];
let particles = [];
let powerups = [];
let stars = [];

let boss = null;

let score = 0;
let kills = 0;
let wave = 1;
let combo = 1;

let missionTime = 0;

let waveKills = 0;
let nextWaveKills = 10;

let shakePower = 0;

let audioContext = null;


/* =========================================================
   INPUT
========================================================= */

const keys = {};

const mouse = {

    x: 0,
    y: 0,

    down: false,
    active: false

};


const joystick = {

    active: false,

    x: 0,
    y: 0

};


let touchFire = false;
let touchBoost = false;


/* =========================================================
   KEYBOARD
========================================================= */

window.addEventListener(
    "keydown",
    e => {

        const code =
            e.code;


        if (
            [
                "KeyW",
                "KeyA",
                "KeyS",
                "KeyD",
                "ArrowUp",
                "ArrowDown",
                "ArrowLeft",
                "ArrowRight",
                "Space",
                "KeyX",
                "ShiftLeft",
                "ShiftRight"
            ].includes(code)
        ) {

            e.preventDefault();

        }


        keys[code] = true;


        if (
            code === "Escape" ||
            code === "KeyP"
        ) {

            if (running) {

                togglePause();

            }

        }


        if (
            code === "KeyB"
        ) {

            useBomb();

        }


        if (
            !running &&
            (
                code === "Enter" ||
                code === "Space"
            )
        ) {

            const menu =
                document.getElementById(
                    "menuScreen"
                );


            if (
                !menu.classList.contains(
                    "hidden"
                )
            ) {

                startGame();

            }

        }

    }
);


window.addEventListener(
    "keyup",
    e => {

        keys[e.code] = false;

    }
);


window.addEventListener(
    "blur",
    () => {

        for (
            const key in keys
        ) {

            keys[key] = false;

        }

        mouse.down = false;

        touchFire = false;
        touchBoost = false;

        resetJoystick();

    }
);


/* =========================================================
   MOUSE
========================================================= */

canvas.addEventListener(
    "pointermove",
    e => {

        if (
            e.pointerType === "mouse" ||
            e.pointerType === "pen"
        ) {

            const rect =
                canvas.getBoundingClientRect();


            mouse.x =
                e.clientX -
                rect.left;


            mouse.y =
                e.clientY -
                rect.top;


            mouse.active = true;


            updateCrosshair();

        }

    },
    {
        passive: true
    }
);


canvas.addEventListener(
    "pointerdown",
    e => {

        if (
            e.pointerType === "mouse" &&
            e.button === 0
        ) {

            mouse.down = true;

            initAudio();

        }

    }
);


window.addEventListener(
    "pointerup",
    e => {

        if (
            e.pointerType === "mouse" &&
            e.button === 0
        ) {

            mouse.down = false;

        }

    }
);


function updateCrosshair() {

    const cross =
        document.getElementById(
            "crosshair"
        );


    if (
        mouse.active &&
        window.matchMedia(
            "(pointer:fine)"
        ).matches
    ) {

        cross.classList.add(
            "visible"
        );


        cross.style.left =
            mouse.x + "px";


        cross.style.top =
            mouse.y + "px";

    }

}


/* =========================================================
   TOUCH JOYSTICK
========================================================= */

const joystickElement =
    document.getElementById(
        "joystick"
    );

const joystickKnob =
    document.getElementById(
        "joystickKnob"
    );


let joystickPointer = null;


function setJoystick(
    clientX,
    clientY
) {

    const rect =
        joystickElement
            .getBoundingClientRect();


    const centerX =
        rect.left +
        rect.width / 2;


    const centerY =
        rect.top +
        rect.height / 2;


    let dx =
        clientX - centerX;

    let dy =
        clientY - centerY;


    const radius =
        rect.width / 2;


    const distance =
        Math.hypot(dx, dy);


    if (
        distance > radius
    ) {

        dx =
            dx / distance *
            radius;

        dy =
            dy / distance *
            radius;

    }


    joystick.x =
        dx / radius;

    joystick.y =
        dy / radius;

    joystick.active = true;


    joystickKnob.style.transform =
        "translate(" +
        (
            -50 +
            joystick.x * 70
        ) +
        "%, " +
        (
            -50 +
            joystick.y * 70
        ) +
        "%)";

}


function resetJoystick() {

    joystick.active = false;

    joystick.x = 0;
    joystick.y = 0;

    joystickKnob.style.transform =
        "translate(-50%, -50%)";

}


joystickElement.addEventListener(
    "pointerdown",
    e => {

        joystickPointer =
            e.pointerId;

        joystickElement.setPointerCapture(
            e.pointerId
        );

        setJoystick(
            e.clientX,
            e.clientY
        );

        initAudio();

    }
);


joystickElement.addEventListener(
    "pointermove",
    e => {

        if (
            e.pointerId ===
            joystickPointer
        ) {

            setJoystick(
                e.clientX,
                e.clientY
            );

        }

    }
);


joystickElement.addEventListener(
    "pointerup",
    e => {

        if (
            e.pointerId ===
            joystickPointer
        ) {

            joystickPointer = null;

            resetJoystick();

        }

    }
);


joystickElement.addEventListener(
    "pointercancel",
    resetJoystick
);


/* =========================================================
   TOUCH BUTTONS
========================================================= */

function holdButton(
    element,
    setter
) {

    element.addEventListener(
        "pointerdown",
        e => {

            e.preventDefault();

            setter(true);

            initAudio();

        }
    );


    element.addEventListener(
        "pointerup",
        e => {

            e.preventDefault();

            setter(false);

        }
    );


    element.addEventListener(
        "pointercancel",
        () => setter(false)
    );


    element.addEventListener(
        "pointerleave",
        e => {

            if (
                e.pointerType === "mouse"
            ) {

                setter(false);

            }

        }
    );

}


holdButton(
    document.getElementById(
        "fireButton"
    ),
    value => {
        touchFire = value;
    }
);


holdButton(
    document.getElementById(
        "boostButton"
    ),
    value => {
        touchBoost = value;
    }
);


document.getElementById(
    "bombButton"
).addEventListener(
    "pointerdown",
    e => {

        e.preventDefault();

        useBomb();

    }
);


/* =========================================================
   AUDIO
========================================================= */

function initAudio() {

    if (!settings.sound) {
        return;
    }


    if (!audioContext) {

        audioContext =
            new (
                window.AudioContext ||
                window.webkitAudioContext
            )();

    }


    if (
        audioContext.state ===
        "suspended"
    ) {

        audioContext.resume();

    }

}


function sound(
    frequency,
    duration,
    type = "sine",
    volume = .04
) {

    if (
        !settings.sound
    ) {

        return;

    }


    try {

        initAudio();


        if (!audioContext) {
            return;
        }


        const osc =
            audioContext.createOscillator();

        const gain =
            audioContext.createGain();


        osc.type = type;

        osc.frequency.value =
            frequency;


        gain.gain.setValueAtTime(
            volume,
            audioContext.currentTime
        );


        gain.gain.exponentialRampToValueAtTime(
            .001,
            audioContext.currentTime +
            duration
        );


        osc.connect(gain);

        gain.connect(
            audioContext.destination
        );


        osc.start();

        osc.stop(
            audioContext.currentTime +
            duration
        );

    } catch (error) {

        /* Sound is optional. */

    }

}


/* =========================================================
   SCREENS
========================================================= */

const screens = [

    "menuScreen",
    "howScreen",
    "settingsScreen",
    "pauseScreen",
    "gameOverScreen"

];


function showScreen(id) {

    screens.forEach(
        screenId => {

            document
                .getElementById(screenId)
                .classList.add(
                    "hidden"
                );

        }
    );


    document
        .getElementById(id)
        .classList.remove(
            "hidden"
        );

}


/* =========================================================
   FULLSCREEN
========================================================= */

async function toggleFullscreen() {

    try {

        if (!document.fullscreenElement) {

            await document
                .documentElement
                .requestFullscreen();

        } else {

            await document.exitFullscreen();

        }

    } catch (error) {

        /* Fullscreen may be unavailable. */

    }

}


/* =========================================================
   GAME START
========================================================= */

function startGame() {

    initAudio();

    resetGame();

    running = true;

    paused = false;

    showScreen(
        "gameScreen"
    );

}


function restartGame() {

    hideAllScreens();

    resetGame();

    running = true;

    paused = false;

}


function quitGame() {

    running = false;

    paused = false;

    boss = null;

    hideAllScreens();

    showScreen(
        "menuScreen"
    );

}


function hideAllScreens() {

    screens.forEach(
        id => {

            document
                .getElementById(id)
                .classList.add(
                    "hidden"
                );

        }
    );

}


/* =========================================================
   PAUSE
========================================================= */

function togglePause() {

    if (!running) {
        return;
    }


    paused =
        !paused;


    if (paused) {

        showScreen(
            "pauseScreen"
        );

    } else {

        hideAllScreens();

        lastTime =
            performance.now();

    }

}


/* =========================================================
   RESET
========================================================= */

function resetGame() {

    score = 0;

    kills = 0;

    wave = 1;

    combo = 1;

    missionTime = 0;

    waveKills = 0;

    nextWaveKills = 10;

    shakePower = 0;

    enemies = [];
    bullets = [];
    enemyBullets = [];
    particles = [];
    powerups = [];

    boss = null;


    player = {

        x: W / 2,

        y: H / 2,

        vx: 0,

        vy: 0,

        angle: -Math.PI / 2,

        speed: 300,

        radius: 15,

        maxHealth: 100,

        health: 100,

        maxEnergy: 100,

        energy: 100,

        fireCooldown: 0,

        rapid: 0,

        spread: 0,

        shield: 0,

        invincible: 0,

        bomb: 0,

        boost: false

    };


    createStars();

    updateHUD();

    hideBossHud();

    lastTime =
        performance.now();

}


/* =========================================================
   STARS
========================================================= */

function createStars() {

    stars = [];

    const count =
        Math.floor(
            Math.min(
                240,
                Math.max(
                    90,
                    W * H / 8000
                )
            )
        );


    for (
        let i = 0;
        i < count;
        i++
    ) {

        stars.push({

            x: rand(0, W),

            y: rand(0, H),

            z: rand(.2, 1),

            size: rand(.4, 2),

            speed: rand(10, 60)

        });

    }

}


/* =========================================================
   SPAWN ENEMIES
========================================================= */

function spawnEnemy() {

    const types = [
        "scout",
        "shooter",
        "tank",
        "hunter"
    ];


    let type =
        types[
            randInt(
                0,
                types.length - 1
            )
        ];


    if (
        wave < 2 &&
        type === "tank"
    ) {

        type = "scout";

    }


    let radius;
    let hp;
    let speed;
    let color;
    let scoreValue;


    if (type === "scout") {

        radius = 13;
        hp = 25 + wave * 3;
        speed = 85 + wave * 3;
        color = "#ef456b";
        scoreValue = 100;

    }


    if (type === "shooter") {

        radius = 16;
        hp = 40 + wave * 4;
        speed = 55 + wave * 2;
        color = "#b865ff";
        scoreValue = 160;

    }


    if (type === "tank") {

        radius = 24;
        hp = 100 + wave * 10;
        speed = 35 + wave;
        color = "#ff914d";
        scoreValue = 300;

    }


    if (type === "hunter") {

        radius = 18;
        hp = 70 + wave * 6;
        speed = 70 + wave * 2;
        color = "#37e6c0";
        scoreValue = 240;

    }


    let x;
    let y;


    const side =
        randInt(0, 3);


    if (side === 0) {

        x = rand(-50, W + 50);
        y = -60;

    } else if (side === 1) {

        x = W + 60;
        y = rand(-50, H + 50);

    } else if (side === 2) {

        x = rand(-50, W + 50);
        y = H + 60;

    } else {

        x = -60;
        y = rand(-50, H + 50);

    }


    enemies.push({

        type,

        x,
        y,

        vx: 0,
        vy: 0,

        angle: 0,

        radius,

        hp,
        maxHp: hp,

        speed,

        color,

        scoreValue,

        shootTimer:
            rand(.6, 2.5),

        phase:
            rand(0, Math.PI * 2),

        age: 0

    });

}


/* =========================================================
   BOSS
========================================================= */

function spawnBoss() {

    enemies = [];

    enemyBullets = [];

    boss = {

        x: W / 2,

        y: -130,

        vx: 0,

        vy: 0,

        radius: 72,

        maxHp:
            1600 +
            wave * 250,

        hp:
            1600 +
            wave * 250,

        phase: 0,

        shootTimer: 1,

        patternTimer: 3,

        age: 0

    };


    showBossHud();

    sound(
        70,
        .7,
        "sawtooth",
        .1
    );

    addShake(12);

}


/* =========================================================
   PLAYER FIRE
========================================================= */

function firePlayer() {

    if (
        player.fireCooldown > 0
    ) {

        return;

    }


    const rapid =
        player.rapid > 0;


    player.fireCooldown =
        rapid
            ? .085
            : .18;


    const count =
        player.spread > 0
            ? 3
            : 1;


    for (
        let i = 0;
        i < count;
        i++
    ) {

        let angle =
            player.angle;


        if (count === 3) {

            angle +=
                (
                    i - 1
                ) *
                .18;

        }


        bullets.push({

            x:
                player.x +
                Math.cos(angle) *
                20,

            y:
                player.y +
                Math.sin(angle) *
                20,

            vx:
                Math.cos(angle) *
                720,

            vy:
                Math.sin(angle) *
                720,

            radius: 3,

            life: 1.2,

            damage:
                rapid ? 18 : 25

        });

    }


    sound(
        rapid ? 720 : 580,
        .045,
        "square",
        .018
    );

}


/* =========================================================
   ENEMY FIRE
========================================================= */

function enemyFire(enemy) {

    const angle =
        Math.atan2(
            player.y - enemy.y,
            player.x - enemy.x
        );


    enemyBullets.push({

        x:
            enemy.x +
            Math.cos(angle) *
            enemy.radius,

        y:
            enemy.y +
            Math.sin(angle) *
            enemy.radius,

        vx:
            Math.cos(angle) *
            (230 + wave * 3),

        vy:
            Math.sin(angle) *
            (230 + wave * 3),

        radius: 5,

        damage:
            enemy.type === "tank"
                ? 18
                : 10,

        life: 5

    });


    sound(
        180,
        .08,
        "sawtooth",
        .012
    );

}


/* =========================================================
   BOSS FIRE
========================================================= */

function bossFire() {

    if (!boss) {
        return;
    }


    const aimed =
        Math.atan2(
            player.y - boss.y,
            player.x - boss.x
        );


    const count = 9;


    for (
        let i = 0;
        i < count;
        i++
    ) {

        const angle =
            i *
            Math.PI * 2 /
            count +
            boss.phase;


        enemyBullets.push({

            x:
                boss.x +
                Math.cos(angle) *
                boss.radius,

            y:
                boss.y +
                Math.sin(angle) *
                boss.radius,

            vx:
                Math.cos(angle) *
                190,

            vy:
                Math.sin(angle) *
                190,

            radius: 6,

            damage: 12,

            life: 6

        });

    }


    enemyBullets.push({

        x: boss.x,

        y: boss.y,

        vx:
            Math.cos(aimed) *
            330,

        vy:
            Math.sin(aimed) *
            330,

        radius: 8,

        damage: 24,

        life: 5

    });


    sound(
        100,
        .25,
        "sawtooth",
        .06
    );

}


/* =========================================================
   POWERUPS
========================================================= */

function spawnPowerup(
    x,
    y
) {

    const types = [

        "shield",
        "rapid",
        "spread",
        "repair",
        "energy",
        "bomb"

    ];


    powerups.push({

        x,
        y,

        type:
            types[
                randInt(
                    0,
                    types.length - 1
                )
            ],

        radius: 11,

        life: 12,

        phase:
            rand(0, Math.PI * 2)

    });

}


/* =========================================================
   APPLY POWERUP
========================================================= */

function collectPowerup(p) {

    if (
        p.type === "shield"
    ) {

        player.shield = 8;

    }


    if (
        p.type === "rapid"
    ) {

        player.rapid = 8;

    }


    if (
        p.type === "spread"
    ) {

        player.spread = 8;

    }


    if (
        p.type === "repair"
    ) {

        player.health =
            Math.min(
                player.maxHealth,
                player.health + 35
            );

    }


    if (
        p.type === "energy"
    ) {

        player.energy =
            player.maxEnergy;

    }


    if (
        p.type === "bomb"
    ) {

        player.bomb++;

        document.getElementById(
            "bombButton"
        ).style.display =
            "flex";

    }


    sound(
        880,
        .18,
        "sine",
        .04
    );


    particleBurst(
        p.x,
        p.y,
        18,
        100,
        3
    );

}


/* =========================================================
   BOMB
========================================================= */

function useBomb() {

    if (
        !running ||
        paused ||
        !player ||
        player.bomb <= 0
    ) {

        return;

    }


    player.bomb--;

    const damage =
        300;


    for (
        const enemy of enemies
    ) {

        enemy.hp -= damage;

    }


    if (boss) {

        boss.hp -=
            damage * 2;

    }


    for (
        const bullet of enemyBullets
    ) {

        bullet.life = 0;

    }


    particleBurst(
        player.x,
        player.y,
        100,
        500,
        5
    );


    addShake(18);


    sound(
        80,
        .7,
        "sawtooth",
        .12
    );


    if (
        player.bomb <= 0
    ) {

        document.getElementById(
            "bombButton"
        ).style.display =
            "none";

    }

}


/* =========================================================
   DAMAGE PLAYER
========================================================= */

function damagePlayer(
    amount
) {

    if (
        player.invincible > 0
    ) {

        return;

    }


    if (
        player.shield > 0
    ) {

        player.shield -= 1.5;

        addShake(3);

        return;

    }


    player.health -= amount;

    player.invincible = .4;

    addShake(7);


    particleBurst(
        player.x,
        player.y,
        12,
        100,
        2
    );


    sound(
        110,
        .18,
        "sawtooth",
        .05
    );


    if (
        player.health <= 0
    ) {

        gameOver();

    }

}


/* =========================================================
   ENEMY DEATH
========================================================= */

function killEnemy(
    enemy
) {

    const index =
        enemies.indexOf(enemy);


    if (
        index !== -1
    ) {

        enemies.splice(
            index,
            1
        );

    }


    kills++;

    waveKills++;

    combo =
        Math.min(
            99,
            combo + 0.15
        );


    score +=
        Math.floor(
            enemy.scoreValue *
            combo
        );


    particleBurst(
        enemy.x,
        enemy.y,
        enemy.type === "tank"
            ? 35
            : 20,

        enemy.type === "tank"
            ? 240
            : 160,

        enemy.type === "tank"
            ? 4
            : 2.5
    );


    addShake(
        enemy.type === "tank"
            ? 7
            : 3
    );


    sound(
        rand(100, 180),
        .15,
        "sawtooth",
        .035
    );


    if (
        Math.random() < .13
    ) {

        spawnPowerup(
            enemy.x,
            enemy.y
        );

    }


    checkWave();

}


/* =========================================================
   BOSS DAMAGE / DEATH
========================================================= */

function killBoss() {

    score +=
        10000 *
        wave;


    combo += 3;

    particleBurst(
        boss.x,
        boss.y,
        180,
        650,
        7
    );


    addShake(30);


    sound(
        40,
        1.2,
        "sawtooth",
        .15
    );


    boss = null;

    enemyBullets = [];

    hideBossHud();


    player.health =
        Math.min(
            player.maxHealth,
            player.health + 40
        );

    player.energy =
        player.maxEnergy;


    wave++;

    waveKills = 0;

    nextWaveKills =
        10 +
        wave * 3;

}


/* =========================================================
   WAVE SYSTEM
========================================================= */

function checkWave() {

    if (
        boss
    ) {

        return;

    }


    if (
        waveKills >=
        nextWaveKills
    ) {

        wave++;

        waveKills = 0;

        nextWaveKills =
            10 +
            wave * 3;


        score +=
            wave * 500;


        if (
            wave % 5 === 0
        ) {

            spawnBoss();

        } else {

            for (
                let i = 0;
                i < Math.min(6, wave);
                i++
            ) {

                spawnEnemy();

            }

        }

    }

}


/* =========================================================
   UPDATE
========================================================= */

function update(dt) {

    if (
        !running ||
        paused
    ) {

        return;

    }


    missionTime += dt;


    combo =
        Math.max(
            1,
            combo - dt * .08
        );


    updateStars(dt);

    updatePlayer(dt);

    updateBullets(dt);

    updateEnemies(dt);

    updateEnemyBullets(dt);

    updatePowerups(dt);

    updateParticles(dt);

    updateBoss(dt);


    /*
        Gradually create enemies.
    */

    const target =
        Math.min(
            4 + wave * 1.5,
            22
        );


    if (
        !boss &&
        enemies.length < target &&
        Math.random() <
            dt *
            (.55 + wave * .04)
    ) {

        spawnEnemy();

    }


    updateHUD();

}


/* =========================================================
   STARS
========================================================= */

function updateStars(dt) {

    for (
        const star of stars
    ) {

        star.y +=
            star.speed *
            star.z *
            dt;


        if (
            star.y > H + 5
        ) {

            star.y = -5;

            star.x =
                rand(0, W);

        }

    }

}


/* =========================================================
   PLAYER
========================================================= */

function updatePlayer(dt) {

    let forward = 0;
    let turn = 0;


    /*
        Keyboard:
        W / Up = forward
        S / Down = backward
        A / Left = rotate left
        D / Right = rotate right
    */

    if (
        keys["KeyW"] ||
        keys["ArrowUp"]
    ) {

        forward += 1;

    }


    if (
        keys["KeyS"] ||
        keys["ArrowDown"]
    ) {

        forward -= 1;

    }


    if (
        keys["KeyA"] ||
        keys["ArrowLeft"]
    ) {

        turn -= 1;

    }


    if (
        keys["KeyD"] ||
        keys["ArrowRight"]
    ) {

        turn += 1;

    }


    /*
        Keyboard rotation.
    */

    const rotationSpeed =
        3.5;


    if (
        !mouse.active
    ) {

        player.angle +=
            turn *
            rotationSpeed *
            dt;

    }


    /*
        Mouse aim.
    */

    if (
        mouse.active
    ) {

        player.angle =
            Math.atan2(
                mouse.y - player.y,
                mouse.x - player.x
            );

    }


    /*
        Touch joystick.
    */

    if (
        joystick.active
    ) {

        const joystickMagnitude =
            Math.hypot(
                joystick.x,
                joystick.y
            );


        if (
            joystickMagnitude > .12
        ) {

            player.angle =
                Math.atan2(
                    joystick.y,
                    joystick.x
                );


            forward =
                joystickMagnitude;

        }

    }


    const acceleration =
        player.speed *
        6;


    player.vx +=
        Math.cos(
            player.angle
        ) *
        forward *
        acceleration *
        dt;


    player.vy +=
        Math.sin(
            player.angle
        ) *
        forward *
        acceleration *
        dt;


    const boosting =
        keys["ShiftLeft"] ||
        keys["ShiftRight"] ||
        touchBoost;


    player.boost =
        boosting &&
        player.energy > 0;


    if (
        player.boost
    ) {

        player.vx +=
            Math.cos(
                player.angle
            ) *
            player.speed *
            2.5 *
            dt;


        player.vy +=
            Math.sin(
                player.angle
            ) *
            player.speed *
            2.5 *
            dt;


        player.energy -=
            45 * dt;


        if (
            settings.particles &&
            Math.random() < .8
        ) {

            particles.push({

                x:
                    player.x -
                    Math.cos(
                        player.angle
                    ) * 17,

                y:
                    player.y -
                    Math.sin(
                        player.angle
                    ) * 17,

                vx:
                    rand(-25, 25) -
                    Math.cos(
                        player.angle
                    ) * 70,

                vy:
                    rand(-25, 25) -
                    Math.sin(
                        player.angle
                    ) * 70,

                life: .25,

                maxLife: .25,

                size: rand(2, 5),

                color: "#57ddff"

            });

        }

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


    /*
        Friction.
    */

    const friction =
        Math.pow(
            .0007,
            dt
        );


    player.vx *= friction;

    player.vy *= friction;


    /*
        Maximum speed.
    */

    const maxSpeed =
        player.boost
            ? 720
            : 360;


    const speed =
        Math.hypot(
            player.vx,
            player.vy
        );


    if (
        speed > maxSpeed
    ) {

        player.vx =
            player.vx /
            speed *
            maxSpeed;


        player.vy =
            player.vy /
            speed *
            maxSpeed;

    }


    player.x +=
        player.vx * dt;


    player.y +=
        player.vy * dt;


    /*
        Screen boundaries.
    */

    const margin = 20;


    if (
        player.x < margin
    ) {

        player.x = margin;
        player.vx *= -.25;

    }


    if (
        player.x > W - margin
    ) {

        player.x =
            W - margin;

        player.vx *= -.25;

    }


    if (
        player.y < margin
    ) {

        player.y = margin;
        player.vy *= -.25;

    }


    if (
        player.y > H - margin
    ) {

        player.y =
            H - margin;

        player.vy *= -.25;

    }


    /*
        Shooting.
    */

    const firing =
        keys["Space"] ||
        keys["KeyX"] ||
        mouse.down ||
        touchFire;


    if (
        firing
    ) {

        firePlayer();

    }


    player.fireCooldown =
        Math.max(
            0,
            player.fireCooldown - dt
        );


    player.invincible =
        Math.max(
            0,
            player.invincible - dt
        );


    player.rapid =
        Math.max(
            0,
            player.rapid - dt
        );


    player.spread =
        Math.max(
            0,
            player.spread - dt
        );


    player.shield =
        Math.max(
            0,
            player.shield - dt
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

        const b =
            bullets[i];


        b.x +=
            b.vx * dt;


        b.y +=
            b.vy * dt;


        b.life -= dt;


        let removed = false;


        /*
            Enemy collision.
        */

        for (
            let j = enemies.length - 1;
            j >= 0;
            j--
        ) {

            const enemy =
                enemies[j];


            if (
                Math.hypot(
                    b.x - enemy.x,
                    b.y - enemy.y
                ) <
                b.radius +
                enemy.radius
            ) {

                enemy.hp -=
                    b.damage;


                b.life = 0;

                particleBurst(
                    b.x,
                    b.y,
                    3,
                    50,
                    1.5
                );


                if (
                    enemy.hp <= 0
                ) {

                    killEnemy(
                        enemy
                    );

                }


                removed = true;

                break;

            }

        }


        /*
            Boss collision.
        */

        if (
            !removed &&
            boss &&
            Math.hypot(
                b.x - boss.x,
                b.y - boss.y
            ) <
            b.radius +
            boss.radius
        ) {

            boss.hp -=
                b.damage;


            b.life = 0;


            particleBurst(
                b.x,
                b.y,
                2,
                45,
                1.5
            );


            if (
                boss.hp <= 0
            ) {

                killBoss();

            }

        }


        if (
            b.life <= 0 ||
            b.x < -100 ||
            b.x > W + 100 ||
            b.y < -100 ||
            b.y > H + 100
        ) {

            bullets.splice(
                i,
                1
            );

        }

    }

}


/* =========================================================
   ENEMIES
========================================================= */

function updateEnemies(dt) {

    for (
        let i = enemies.length - 1;
        i >= 0;
        i--
    ) {

        const enemy =
            enemies[i];


        enemy.age += dt;

        enemy.phase +=
            dt *
            2;


        const dx =
            player.x -
            enemy.x;


        const dy =
            player.y -
            enemy.y;


        const distance =
            Math.hypot(
                dx,
                dy
            );


        const angle =
            Math.atan2(
                dy,
                dx
            );


        enemy.angle =
            angle;


        /*
            Movement by enemy type.
        */

        if (
            enemy.type === "scout"
        ) {

            enemy.vx +=
                Math.cos(angle) *
                enemy.speed *
                1.8 *
                dt;


            enemy.vy +=
                Math.sin(angle) *
                enemy.speed *
                1.8 *
                dt;

        }


        else if (
            enemy.type === "shooter"
        ) {

            const preferred =
                260;


            const direction =
                distance >
                preferred
                    ? 1
                    : -1;


            enemy.vx +=
                Math.cos(angle) *
                enemy.speed *
                direction *
                dt;


            enemy.vy +=
                Math.sin(angle) *
                enemy.speed *
                direction *
                dt;


            enemy.vx +=
                Math.cos(
                    angle +
                    Math.PI / 2
                ) *
                Math.sin(
                    enemy.phase
                ) *
                20 *
                dt;


            enemy.vy +=
                Math.sin(
                    angle +
                    Math.PI / 2
                ) *
                Math.sin(
                    enemy.phase
                ) *
                20 *
                dt;

        }


        else if (
            enemy.type === "tank"
        ) {

            enemy.vx +=
                Math.cos(angle) *
                enemy.speed *
                dt;


            enemy.vy +=
                Math.sin(angle) *
                enemy.speed *
                dt;

        }


        else if (
            enemy.type === "hunter"
        ) {

            enemy.vx +=
                Math.cos(angle) *
                enemy.speed *
                1.4 *
                dt;


            enemy.vy +=
                Math.sin(angle) *
                enemy.speed *
                1.4 *
                dt;

        }


        /*
            Damping.
        */

        enemy.vx *=
            Math.pow(
                .002,
                dt
            );


        enemy.vy *=
            Math.pow(
                .002,
                dt
            );


        enemy.x +=
            enemy.vx * dt;


        enemy.y +=
            enemy.vy * dt;


        /*
            Shooting.
        */

        enemy.shootTimer -=
            dt;


        if (
            enemy.shootTimer <= 0 &&
            distance < 650
        ) {

            if (
                enemy.type !==
                "scout"
            ) {

                enemyFire(enemy);

            }


            enemy.shootTimer =
                enemy.type === "tank"
                    ? rand(2, 3.5)
                    : rand(1, 2.4);

        }


        /*
            Player collision.
        */

        if (
            Math.hypot(
                player.x - enemy.x,
                player.y - enemy.y
            ) <
            player.radius +
            enemy.radius
        ) {

            damagePlayer(
                enemy.type === "tank"
                    ? 30
                    : 20
            );


            enemy.hp = 0;


            killEnemy(enemy);

        }


        /*
            Remove distant enemies.
        */

        if (
            enemy.x < -250 ||
            enemy.x > W + 250 ||
            enemy.y < -250 ||
            enemy.y > H + 250
        ) {

            enemies.splice(
                i,
                1
            );

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


        b.x +=
            b.vx * dt;


        b.y +=
            b.vy * dt;


        b.life -= dt;


        if (
            Math.hypot(
                player.x - b.x,
                player.y - b.y
            ) <
            player.radius +
            b.radius
        ) {

            damagePlayer(
                b.damage
            );


            b.life = 0;

        }


        if (
            b.life <= 0 ||
            b.x < -150 ||
            b.x > W + 150 ||
            b.y < -150 ||
            b.y > H + 150
        ) {

            enemyBullets.splice(
                i,
                1
            );

        }

    }

}


/* =========================================================
   BOSS UPDATE
========================================================= */

function updateBoss(dt) {

    if (!boss) {
        return;
    }


    boss.age += dt;

    boss.phase +=
        dt *
        .7;


    /*
        Enter screen.
    */

    if (
        boss.y < 150
    ) {

        boss.y +=
            90 * dt;

        return;

    }


    /*
        Horizontal movement.
    */

    const targetX =
        W / 2 +
        Math.sin(
            boss.age *
            .6
        ) *
        Math.min(
            260,
            W * .3
        );


    boss.x +=
        (
            targetX -
            boss.x
        ) *
        dt *
        .8;


    /*
        Boss shooting.
    */

    boss.shootTimer -= dt;


    if (
        boss.shootTimer <= 0
    ) {

        bossFire();

        boss.shootTimer =
            Math.max(
                .7,
                1.8 -
                wave * .03
            );

    }


    /*
        Boss collision.
    */

    if (
        Math.hypot(
            player.x - boss.x,
            player.y - boss.y
        ) <
        player.radius +
        boss.radius
    ) {

        damagePlayer(45);

    }


    updateBossHud();

}


/* =========================================================
   POWERUPS UPDATE
========================================================= */

function updatePowerups(dt) {

    for (
        let i = powerups.length - 1;
        i >= 0;
        i--
    ) {

        const p =
            powerups[i];


        p.life -= dt;

        p.phase +=
            dt * 3;


        if (
            Math.hypot(
                player.x - p.x,
                player.y - p.y
            ) <
            player.radius +
            p.radius +
            5
        ) {

            collectPowerup(p);

            powerups.splice(
                i,
                1
            );

            continue;

        }


        if (
            p.life <= 0
        ) {

            powerups.splice(
                i,
                1
            );

        }

    }

}


/* =========================================================
   PARTICLES
========================================================= */

function particleBurst(
    x,
    y,
    count,
    speed,
    size
) {

    if (
        !settings.particles
    ) {

        return;

    }


    for (
        let i = 0;
        i < count;
        i++
    ) {

        const angle =
            rand(
                0,
                Math.PI * 2
            );


        const velocity =
            rand(
                speed * .2,
                speed
            );


        particles.push({

            x,
            y,

            vx:
                Math.cos(angle) *
                velocity,

            vy:
                Math.sin(angle) *
                velocity,

            life:
                rand(.25, .75),

            maxLife:
                .75,

            size:
                rand(
                    size * .5,
                    size * 1.5
                ),

            color:
                Math.random() < .5
                    ? "#62dfff"
                    : "#ffffff"

        });

    }

}


/* =========================================================
   PARTICLE UPDATE
========================================================= */

function updateParticles(dt) {

    for (
        let i = particles.length - 1;
        i >= 0;
        i--
    ) {

        const p =
            particles[i];


        p.x +=
            p.vx * dt;


        p.y +=
            p.vy * dt;


        p.vx *=
            Math.pow(
                .04,
                dt
            );


        p.vy *=
            Math.pow(
                .04,
                dt
            );


        p.life -= dt;


        if (
            p.life <= 0
        ) {

            particles.splice(
                i,
                1
            );

        }

    }

}


/* =========================================================
   SHAKE
========================================================= */

function addShake(amount) {

    if (
        !settings.shake
    ) {

        return;

    }


    shakePower =
        Math.max(
            shakePower,
            amount
        );

}


/* =========================================================
   DRAW
========================================================= */

function draw() {

    ctx.setTransform(
        DPR,
        0,
        0,
        DPR,
        0,
        0
    );


    ctx.fillStyle =
        "#02040a";


    ctx.fillRect(
        0,
        0,
        W,
        H
    );


    let sx = 0;
    let sy = 0;


    if (
        shakePower > 0
    ) {

        sx =
            rand(
                -shakePower,
                shakePower
            );


        sy =
            rand(
                -shakePower,
                shakePower
            );


        shakePower *= .88;

        if (
            shakePower < .1
        ) {

            shakePower = 0;

        }

    }


    ctx.save();

    ctx.translate(
        sx,
        sy
    );


    drawBackground();

    drawPowerups();

    drawBullets();

    drawEnemyBullets();

    drawEnemies();

    drawBoss();

    drawPlayer();

    drawParticles();


    ctx.restore();

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
        "#07172b"
    );


    gradient.addColorStop(
        .5,
        "#030a16"
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


    /*
        Stars.
    */

    for (
        const star of stars
    ) {

        ctx.globalAlpha =
            .25 +
            star.z *
            .75;


        ctx.fillStyle =
            "#bcecff";


        ctx.beginPath();


        ctx.arc(
            star.x,
            star.y,
            star.size *
            star.z,
            0,
            Math.PI * 2
        );


        ctx.fill();

    }


    ctx.globalAlpha = 1;


    /*
        Subtle grid.
    */

    ctx.strokeStyle =
        "rgba(50,150,200,.035)";


    ctx.lineWidth = 1;


    const grid = 70;


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

}


/* =========================================================
   PLAYER DRAW
========================================================= */

function drawPlayer() {

    if (
        !player
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


    /*
        Invincibility blink.
    */

    if (
        player.invincible > 0 &&
        Math.floor(
            player.invincible * 20
        ) % 2 === 0
    ) {

        ctx.globalAlpha = .45;

    }


    /*
        Shield.
    */

    if (
        player.shield > 0
    ) {

        ctx.strokeStyle =
            "rgba(70,220,255,.75)";

        ctx.lineWidth = 3;

        ctx.shadowBlur = 20;

        ctx.shadowColor =
            "#35dfff";


        ctx.beginPath();

        ctx.arc(
            0,
            0,
            27,
            0,
            Math.PI * 2
        );

        ctx.stroke();

    }


    /*
        Engine flame.
    */

    ctx.shadowBlur = 20;

    ctx.shadowColor =
        "#36dfff";


    const flame =
        player.boost
            ? rand(22, 38)
            : rand(10, 18);


    ctx.fillStyle =
        "#52dcff";


    ctx.beginPath();

    ctx.moveTo(
        -13,
        0
    );

    ctx.lineTo(
        -flame,
        -5
    );

    ctx.lineTo(
        -flame * .7,
        0
    );

    ctx.lineTo(
        -flame,
        5
    );

    ctx.closePath();

    ctx.fill();


    /*
        Ship body.
    */

    ctx.shadowBlur = 25;

    ctx.shadowColor =
        "#36bfff";


    ctx.fillStyle =
        "#d9f8ff";


    ctx.beginPath();

    ctx.moveTo(
        23,
        0
    );

    ctx.lineTo(
        -12,
        -13
    );

    ctx.lineTo(
        -7,
        0
    );

    ctx.lineTo(
        -12,
        13
    );

    ctx.closePath();

    ctx.fill();


    /*
        Cockpit.
    */

    ctx.shadowBlur = 12;

    ctx.fillStyle =
        "#16799c";


    ctx.beginPath();

    ctx.ellipse(
        5,
        0,
        9,
        5,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.restore();

}


/* =========================================================
   ENEMIES DRAW
========================================================= */

function drawEnemies() {

    for (
        const enemy of enemies
    ) {

        ctx.save();

        ctx.translate(
            enemy.x,
            enemy.y
        );


        ctx.rotate(
            enemy.angle
        );


        ctx.shadowBlur = 18;

        ctx.shadowColor =
            enemy.color;


        ctx.fillStyle =
            enemy.color;


        if (
            enemy.type === "scout"
        ) {

            ctx.beginPath();

            ctx.moveTo(
                18,
                0
            );

            ctx.lineTo(
                -13,
                -11
            );

            ctx.lineTo(
                -8,
                0
            );

            ctx.lineTo(
                -13,
                11
            );

            ctx.closePath();

            ctx.fill();

        }


        else if (
            enemy.type === "shooter"
        ) {

            ctx.beginPath();

            ctx.arc(
                0,
                0,
                enemy.radius,
                0,
                Math.PI * 2
            );

            ctx.fill();


            ctx.fillStyle =
                "#160b27";


            ctx.beginPath();

            ctx.arc(
                0,
                0,
                6,
                0,
                Math.PI * 2
            );

            ctx.fill();

        }


        else if (
            enemy.type === "tank"
        ) {

            ctx.beginPath();

            ctx.rect(
                -enemy.radius,
                -enemy.radius,
                enemy.radius * 2,
                enemy.radius * 2
            );

            ctx.fill();


            ctx.strokeStyle =
                "#ffd09d";

            ctx.lineWidth = 2;

            ctx.stroke();

        }


        else {

            ctx.beginPath();

            for (
                let i = 0;
                i < 6;
                i++
            ) {

                const a =
                    i *
                    Math.PI /
                    3;


                const r =
                    i % 2 === 0
                        ? enemy.radius
                        : enemy.radius * .55;


                const x =
                    Math.cos(a) * r;

                const y =
                    Math.sin(a) * r;


                if (i === 0) {

                    ctx.moveTo(
                        x,
                        y
                    );

                } else {

                    ctx.lineTo(
                        x,
                        y
                    );

                }

            }

            ctx.closePath();

            ctx.fill();

        }


        /*
            HP bar.
        */

        if (
            enemy.hp <
            enemy.maxHp
        ) {

            const width =
                enemy.radius * 2;


            ctx.shadowBlur = 0;

            ctx.fillStyle =
                "rgba(0,0,0,.55)";


            ctx.fillRect(
                -width / 2,
                -enemy.radius - 9,
                width,
                4
            );


            ctx.fillStyle =
                "#72e7ff";


            ctx.fillRect(
                -width / 2,
                -enemy.radius - 9,
                width *
                Math.max(
                    0,
                    enemy.hp /
                    enemy.maxHp
                ),
                4
            );

        }


        ctx.restore();

    }

}


/* =========================================================
   BOSS DRAW
========================================================= */

function drawBoss() {

    if (!boss) {
        return;
    }


    ctx.save();


    ctx.translate(
        boss.x,
        boss.y
    );


    ctx.rotate(
        boss.phase
    );


    ctx.shadowBlur = 45;

    ctx.shadowColor =
        "#ff2457";


    ctx.strokeStyle =
        "#ff315e";

    ctx.lineWidth = 7;


    ctx.beginPath();

    ctx.arc(
        0,
        0,
        boss.radius,
        0,
        Math.PI * 2
    );

    ctx.stroke();


    ctx.fillStyle =
        "#270816";


    ctx.beginPath();

    ctx.arc(
        0,
        0,
        boss.radius * .72,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.strokeStyle =
        "#ff7890";

    ctx.lineWidth = 3;


    for (
        let i = 0;
        i < 8;
        i++
    ) {

        const angle =
            i *
            Math.PI / 4;


        ctx.beginPath();

        ctx.moveTo(
            Math.cos(angle) *
            35,

            Math.sin(angle) *
            35
        );


        ctx.lineTo(
            Math.cos(angle) *
            95,

            Math.sin(angle) *
            95
        );

        ctx.stroke();

    }


    ctx.fillStyle =
        "#ff4168";


    ctx.shadowBlur = 35;

    ctx.shadowColor =
        "#ff0038";


    ctx.beginPath();

    ctx.arc(
        0,
        0,
        20 +
        Math.sin(
            boss.age * 4
        ) * 4,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.restore();

}


/* =========================================================
   BULLETS DRAW
========================================================= */

function drawBullets() {

    ctx.shadowBlur = 12;

    ctx.shadowColor =
        "#6ce8ff";

    ctx.fillStyle =
        "#bff7ff";


    for (
        const b of bullets
    ) {

        ctx.beginPath();

        ctx.arc(
            b.x,
            b.y,
            b.radius,
            0,
            Math.PI * 2
        );

        ctx.fill();

    }

}


/* =========================================================
   ENEMY BULLETS DRAW
========================================================= */

function drawEnemyBullets() {

    ctx.shadowBlur = 15;

    ctx.shadowColor =
        "#ff375d";

    ctx.fillStyle =
        "#ff718b";


    for (
        const b of enemyBullets
    ) {

        ctx.beginPath();

        ctx.arc(
            b.x,
            b.y,
            b.radius,
            0,
            Math.PI * 2
        );

        ctx.fill();

    }

}


/* =========================================================
   POWERUP DRAW
========================================================= */

function drawPowerups() {

    for (
        const p of powerups
    ) {

        const pulse =
            1 +
            Math.sin(
                p.phase
            ) *
            .15;


        let color =
            "#62ddff";


        if (
            p.type === "shield"
        ) {

            color = "#5bdcff";

        }


        if (
            p.type === "rapid"
        ) {

            color = "#ffe45c";

        }


        if (
            p.type === "spread"
        ) {

            color = "#c46cff";

        }


        if (
            p.type === "repair"
        ) {

            color = "#59ef88";

        }


        if (
            p.type === "energy"
        ) {

            color = "#36bfff";

        }


        if (
            p.type === "bomb"
        ) {

            color = "#ff4968";

        }


        ctx.save();


        ctx.translate(
            p.x,
            p.y
        );


        ctx.scale(
            pulse,
            pulse
        );


        ctx.shadowBlur = 25;

        ctx.shadowColor =
            color;


        ctx.strokeStyle =
            color;

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
            color;


        ctx.font =
            "bold 10px Arial";

        ctx.textAlign =
            "center";

        ctx.textBaseline =
            "middle";


        const symbol = {

            shield: "S",
            rapid: "R",
            spread: "W",
            repair: "+",
            energy: "E",
            bomb: "B"

        }[p.type];


        ctx.fillText(
            symbol,
            0,
            1
        );


        ctx.restore();

    }

}


/* =========================================================
   PARTICLES DRAW
========================================================= */

function drawParticles() {

    if (
        !settings.particles
    ) {

        return;

    }


    for (
        const p of particles
    ) {

        ctx.globalAlpha =
            Math.max(
                0,
                p.life /
                p.maxLife
            );


        ctx.fillStyle =
            p.color;


        ctx.shadowBlur =
            p.size * 3;


        ctx.shadowColor =
            p.color;


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
   HUD
========================================================= */

function updateHUD() {

    if (!player) {
        return;
    }


    document.getElementById(
        "scoreText"
    ).textContent =
        Math.floor(score)
            .toLocaleString();


    document.getElementById(
        "waveText"
    ).textContent =
        wave;


    document.getElementById(
        "killsText"
    ).textContent =
        kills;


    document.getElementById(
        "comboText"
    ).textContent =
        "x" +
        combo.toFixed(1);


    document.getElementById(
        "healthFill"
    ).style.transform =
        "scaleX(" +
        Math.max(
            0,
            player.health /
            player.maxHealth
        ) +
        ")";


    document.getElementById(
        "energyFill"
    ).style.transform =
        "scaleX(" +
        (
            player.energy /
            player.maxEnergy
        ) +
        ")";

}


/* =========================================================
   BOSS HUD
========================================================= */

function showBossHud() {

    document
        .getElementById(
            "bossHud"
        )
        .classList.add(
            "visible"
        );

}


function hideBossHud() {

    document
        .getElementById(
            "bossHud"
        )
        .classList.remove(
            "visible"
        );

}


function updateBossHud() {

    if (!boss) {

        hideBossHud();

        return;

    }


    const percentage =
        Math.max(
            0,
            boss.hp /
            boss.maxHp
        );


    document.getElementById(
        "bossFill"
    ).style.transform =
        "scaleX(" +
        percentage +
        ")";

}


/* =========================================================
   GAME OVER
========================================================= */

function gameOver() {

    if (!running) {
        return;
    }


    running = false;

    paused = false;


    particleBurst(
        player.x,
        player.y,
        100,
        500,
        5
    );


    addShake(20);


    sound(
        45,
        1,
        "sawtooth",
        .12
    );


    document.getElementById(
        "finalScore"
    ).textContent =
        Math.floor(
            score
        ).toLocaleString();


    document.getElementById(
        "finalWave"
    ).textContent =
        wave;


    document.getElementById(
        "finalKills"
    ).textContent =
        kills;


    document.getElementById(
        "finalTime"
    ).textContent =
        formatTime(
            missionTime
        );


    setTimeout(
        () => {

            showScreen(
                "gameOverScreen"
            );

        },
        350
    );

}


/* =========================================================
   SETTINGS
========================================================= */

function toggleSetting(
    name
) {

    settings[name] =
        !settings[name];


    updateSettingsUI();

}


function updateSettingsUI() {

    document
        .getElementById(
            "soundToggle"
        )
        .classList.toggle(
            "on",
            settings.sound
        );


    document
        .getElementById(
            "shakeToggle"
        )
        .classList.toggle(
            "on",
            settings.shake
        );


    document
        .getElementById(
            "particlesToggle"
        )
        .classList.toggle(
            "on",
            settings.particles
        );

}


/* =========================================================
   GAME LOOP
========================================================= */

function loop(timestamp) {

    const dt =
        Math.min(
            .033,
            (
                timestamp -
                lastTime
            ) / 1000
        );


    lastTime =
        timestamp;


    update(dt);

    draw();


    requestAnimationFrame(
        loop
    );

}


/* =========================================================
   INITIALIZE
========================================================= */

resizeCanvas();

resetGame();

updateSettingsUI();

showScreen(
    "menuScreen"
);


requestAnimationFrame(
    timestamp => {

        lastTime =
            timestamp;

        requestAnimationFrame(
            loop
        );

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
