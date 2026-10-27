from flask import Flask, render_template_string, Response, send_file
import os

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#02030a">
<meta name="description" content="VOID SPACE — a cinematic neon cyberpunk space roguelite. Defeat bosses, evolve weapons and unlock ships.">
<meta name="application-name" content="VOID SPACE">
<link rel="manifest" href="/manifest.json">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E%3Cdefs%3E%3ClinearGradient id=%22g%22 x1=%220%22 y1=%220%22 x2=%221%22 y2=%221%22%3E%3Cstop stop-color=%22%2363caff%22/%3E%3Cstop offset=%221%22 stop-color=%22%234d55ff%22/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width=%2264%22 height=%2264%22 rx=%2215%22 fill=%22%23040818%22/%3E%3Cpath d=%22M43 32 15 19l7 13-7 13z%22 fill=%22url(%23g)%22 stroke=%22%23d8f4ff%22 stroke-width=%222%22 stroke-linejoin=%22round%22/%3E%3Ccircle cx=%2241%22 cy=%2232%22 r=%224%22 fill=%22%23ffffff%22/%3E%3C/svg%3E">

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

.brand-mark{
    display:block;
    width:clamp(54px,8vw,78px);
    height:clamp(54px,8vw,78px);
    margin:0 auto 12px;
    filter:drop-shadow(0 0 18px rgba(77,187,255,.6));
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

#gameControls{
    display:none;
    position:fixed;
    z-index:12;
    left:50%;
    bottom:max(16px, env(safe-area-inset-bottom));
    transform:translateX(-50%);
    width:min(760px, calc(100vw - 28px));
    padding:10px;
    border:1px solid rgba(100,190,255,.22);
    border-radius:16px;
    background:rgba(0,7,20,.72);
    backdrop-filter:blur(10px);
    grid-template-columns:repeat(7,minmax(0,1fr));
    gap:7px;
}
#gameControls button{
    min-width:0;
    margin:0;
    min-height:44px;
    padding:8px 5px;
    font-size:clamp(10px,1.2vw,12px);
    letter-spacing:.3px;
}
#gameControls .fire-control{border-color:rgba(255,110,130,.7);}
#gameControls .pause-control{border-color:rgba(255,210,110,.7);}
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

.small{color:#8197ad;font-size:12px}

.neon-stats{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin:15px 0;color:#b5e5ff;font-size:12px}
.neon-stats span{border:1px solid #304274;background:#090f25;padding:8px 10px;border-radius:9px}
.ship-card{border:1px solid #5940a8;border-radius:12px;padding:15px;margin:12px 0;background:rgba(16,25,58,.7)}
#upgradeChoices{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:20px 0}
.upgrade-card{width:100%;min-height:120px;margin:0;padding:12px;border-color:#b84dff;background:linear-gradient(160deg,#281451,#070d22);white-space:normal}
.upgrade-card strong{display:block;color:#ff9cec;margin-bottom:10px}
.upgrade-card span{display:block;color:#c5d8ff;font-size:12px;font-weight:400;letter-spacing:0;line-height:1.5}
#bombFlash{position:fixed;inset:0;z-index:8;pointer-events:none;opacity:0;background:radial-gradient(circle,rgba(255,255,255,.9),rgba(70,220,255,.45) 18%,rgba(195,45,255,.2) 55%,transparent 75%)}
#bossBar{position:fixed;display:none;top:85px;left:15%;width:70%;height:14px;z-index:11;border:1px solid #ff70ec;border-radius:99px;background:#160a28;overflow:visible;pointer-events:none}
#bossName{position:absolute;bottom:17px;left:0;width:100%;text-align:center;color:#f8d5ff;font-size:11px;font-weight:900;letter-spacing:.2em;text-shadow:0 0 12px #f0f}
#bossBarFill{height:100%;width:100%;border-radius:99px;background:linear-gradient(90deg,#6b5bff,#ff42d0);box-shadow:0 0 15px #f0f;transition:width .12s linear}
#cinematicFlash{position:fixed;inset:0;z-index:25;pointer-events:none;opacity:0;background:radial-gradient(circle,rgba(210,230,255,.35),rgba(140,60,255,.18),transparent 70%)}
#toastNotice{position:fixed;left:50%;top:18%;transform:translate(-50%,-8px);z-index:40;opacity:0;pointer-events:none;padding:12px 20px;border:1px solid rgba(139,226,255,.65);border-radius:14px;background:rgba(4,9,25,.94);color:#c8f7ff;box-shadow:0 0 28px rgba(100,200,255,.2);font-weight:900;letter-spacing:.08em;text-align:center;transition:opacity .18s,transform .18s;max-width:90vw}
#toastNotice.show{opacity:1;transform:translate(-50%,0)}
.feature-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:18px 0}
.feature-grid button{min-height:78px;text-align:left;line-height:1.4}
.feature-grid small{display:block;color:#9dcaff;font-size:11px;margin-top:5px;font-weight:500}
.achievement-card{display:flex;gap:12px;align-items:center;text-align:left;border:1px solid rgba(160,180,255,.16);border-radius:12px;padding:12px;margin:8px 0;background:rgba(20,30,60,.35)}
.achievement-card.locked{opacity:.52;filter:saturate(.35)}
.achievement-card strong{display:block;color:#c4f6ff}
.achievement-card small{display:block;color:#9eafd0;margin-top:4px}
@media(max-width:560px){.feature-grid{grid-template-columns:1fr}#bossBar{top:118px;left:10%;width:80%}#toastNotice{top:24%}}
@media(max-width:700px){#upgradeChoices{grid-template-columns:1fr}.upgrade-card{min-height:75px;text-align:left}}


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

/* Adaptive layout, safe areas and accessible focus states */
button:focus-visible{
    outline:3px solid #a8e8ff;
    outline-offset:3px;
}
.screen{padding:max(12px,env(safe-area-inset-top)) 12px max(12px,env(safe-area-inset-bottom));}
.panel{overscroll-behavior:contain;}
#hud{top:max(12px,env(safe-area-inset-top));}
@media (pointer:fine) and (min-width:701px){
    #gameControls{display:grid;}
}
@media (max-width:700px){
    #gameControls{display:none !important;}
    #joystick{left:max(12px,env(safe-area-inset-left));bottom:max(12px,env(safe-area-inset-bottom));width:clamp(100px,27vw,140px);height:clamp(100px,27vw,140px);}
    #stick{left:50%;top:50%;transform:translate(-50%,-50%);width:42%;height:42%;}
    .touch-buttons{right:max(12px,env(safe-area-inset-right));bottom:max(12px,env(safe-area-inset-bottom));gap:8px;}
    .touch-btn{width:clamp(66px,18vw,82px);height:52px;font-size:11px;padding:0;}
    #fireTouch{width:clamp(78px,22vw,100px);height:clamp(78px,22vw,100px);}
    #hud{left:8px;right:8px;top:max(8px,env(safe-area-inset-top));}
    .hud-row{gap:6px;}
    .hud-box{max-width:34vw;padding:6px 7px;font-size:clamp(9px,2.5vw,11px);}
    #healthOuter,#energyOuter{width:clamp(64px,20vw,110px);}
}
@media (max-height:520px) and (orientation:landscape){
    .panel{padding:14px 18px;max-height:94dvh;}
    .subtitle{margin-bottom:12px;}
    .menu-buttons{gap:0;}
    button{min-height:40px;padding:8px 14px;margin:3px;}
    #joystick{width:94px;height:94px;}
    #stick{width:40px;height:40px;}
    .touch-buttons{flex-direction:row;align-items:flex-end;}
    #fireTouch{width:68px;height:68px;}
}
@media (prefers-reduced-motion:reduce){
    *,*::before,*::after{scroll-behavior:auto !important;transition:none !important;animation:none !important;}
}


/* CALM COSMIC UI — soft contrast, refined surfaces, reduced visual noise */
:root{
  color-scheme:dark;
  --ui-ink:#f1f3ff;
  --ui-muted:#a8b4d1;
  --ui-soft:#cbd4ee;
  --ui-line:rgba(173,190,255,.16);
  --ui-panel:rgba(12,17,39,.92);
  --ui-panel-deep:rgba(8,12,29,.96);
  --ui-lilac:#b7a7ff;
  --ui-blue:#91d9f7;
  --ui-mint:#9ce8d2;
}
html,body{
  background:#070a18;
  color:var(--ui-ink);
  font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  letter-spacing:.01em;
}
#game{background:radial-gradient(ellipse at 50% 45%,#101833 0%,#080c1d 52%,#050711 100%);}
.screen{
  background:
    radial-gradient(ellipse at 50% 20%,rgba(95,111,174,.12),transparent 54%),
    rgba(4,7,18,.68);
  -webkit-backdrop-filter:blur(8px);
  backdrop-filter:blur(8px);
}
.panel{
  width:min(660px,94vw);
  max-height:min(90dvh,900px);
  padding:clamp(24px,4vw,42px);
  border:1px solid var(--ui-line);
  border-radius:26px;
  background:
    linear-gradient(145deg,rgba(20,27,56,.97),rgba(8,12,29,.97) 72%);
  box-shadow:0 28px 90px rgba(0,0,0,.42),0 1px 0 rgba(255,255,255,.035) inset;
  text-align:center;
  scrollbar-color:rgba(183,167,255,.38) transparent;
}
.panel h1{
  margin:0 0 12px;
  color:#f2f3ff;
  font-size:clamp(24px,4vw,34px);
  font-weight:720;
  line-height:1.15;
  letter-spacing:.045em;
}
.brand-mark{
  width:clamp(58px,7vw,76px);
  height:clamp(58px,7vw,76px);
  margin-bottom:18px;
  filter:drop-shadow(0 8px 22px rgba(131,153,255,.22));
}
.logo{
  font-size:clamp(48px,9vw,82px);
  font-weight:760;
  line-height:.98;
  letter-spacing:.16em;
  padding-left:.16em;
  color:#f5f4ff;
  text-shadow:0 0 34px rgba(146,161,255,.24);
  margin-bottom:10px;
}
.subtitle{
  color:#b9c6ee;
  letter-spacing:.48em;
  padding-left:.48em;
  font-size:11px;
  font-weight:650;
  margin-bottom:30px;
}
button{
  min-height:46px;
  padding:12px 20px;
  border:1px solid rgba(166,181,255,.23);
  border-radius:13px;
  background:linear-gradient(180deg,rgba(47,58,100,.76),rgba(26,34,66,.9));
  color:#edf0ff;
  font:inherit;
  font-size:13px;
  font-weight:650;
  letter-spacing:.055em;
  box-shadow:0 4px 14px rgba(0,0,0,.12),inset 0 1px 0 rgba(255,255,255,.045);
  transition:transform .18s ease,border-color .18s ease,background .18s ease,box-shadow .18s ease;
}
button:hover{
  transform:translateY(-1px);
  border-color:rgba(184,196,255,.48);
  background:linear-gradient(180deg,rgba(62,75,125,.86),rgba(30,40,77,.96));
  box-shadow:0 8px 24px rgba(0,0,0,.2);
}
button:active{transform:translateY(0) scale(.99);}
button:focus-visible{outline:2px solid var(--ui-blue);outline-offset:3px;}
button.primary{
  width:min(360px,100%);
  min-height:54px;
  border-color:rgba(183,167,255,.45);
  background:linear-gradient(110deg,#a99af1,#8ebfe9);
  color:#11162d;
  font-size:14px;
  font-weight:800;
  letter-spacing:.12em;
  box-shadow:0 8px 28px rgba(131,135,233,.17),inset 0 1px 0 rgba(255,255,255,.4);
}
button.primary:hover{
  border-color:#d8d0ff;
  background:linear-gradient(110deg,#c1b5ff,#a8d9f1);
  box-shadow:0 10px 32px rgba(131,135,233,.25);
}
.menu-buttons{gap:7px;}
.menu-buttons>button:not(.primary){width:min(330px,100%);}
.neon-stats{
  gap:8px;
  margin:22px 0 4px;
  color:var(--ui-soft);
  font-size:11px;
}
.neon-stats span{
  padding:9px 12px;
  border:1px solid rgba(173,190,255,.13);
  border-radius:12px;
  background:rgba(255,255,255,.035);
  color:#c5cdec;
}
.neon-stats b{color:#f1f2ff;font-weight:750;}
.small{color:#8d9bbb;font-size:10px;letter-spacing:.12em;}
.info-grid{gap:12px;margin:22px 0;}
.info{
  padding:18px;
  border:1px solid rgba(173,190,255,.13);
  border-radius:16px;
  background:linear-gradient(145deg,rgba(255,255,255,.045),rgba(255,255,255,.018));
  text-align:left;
}
.info strong{
  color:var(--ui-blue);
  font-size:11px;
  letter-spacing:.13em;
  margin-bottom:10px;
}
.controls{color:#c2cce5;line-height:2;}
.controls kbd{
  min-width:30px;
  padding:3px 7px;
  border:1px solid rgba(173,190,255,.2);
  border-radius:7px;
  background:rgba(5,9,24,.7);
  color:#f0efff;
  font:600 11px ui-monospace,SFMono-Regular,Consolas,monospace;
}
.setting-row{
  padding:15px 0;
  border-bottom:1px solid rgba(173,190,255,.11);
  color:#d9def1;
  font-size:13px;
}
.setting-value{color:var(--ui-mint);font-size:12px;letter-spacing:.08em;}
.hud-box{
  padding:11px 14px;
  border:1px solid rgba(177,193,255,.16);
  border-radius:14px;
  background:rgba(8,12,29,.76);
  -webkit-backdrop-filter:blur(14px);
  backdrop-filter:blur(14px);
  color:#dce4ff;
  box-shadow:0 8px 28px rgba(0,0,0,.16),inset 0 1px 0 rgba(255,255,255,.035);
  font-size:11px;
  line-height:1.65;
}
.hud-box b{color:var(--ui-blue);}
#healthOuter,#energyOuter{height:7px;background:rgba(255,255,255,.09);}
#healthBar{background:linear-gradient(90deg,#7bd9b6,#b6edcf);}
#energyBar{background:linear-gradient(90deg,#8b9ff8,#9ddcf3);}
#rotationIndicator{color:var(--ui-lilac);}
#gameControls{
  padding:9px;
  border:1px solid rgba(173,190,255,.15);
  border-radius:18px;
  background:rgba(8,12,29,.8);
  -webkit-backdrop-filter:blur(14px);
  backdrop-filter:blur(14px);
  box-shadow:0 12px 36px rgba(0,0,0,.2);
}
#gameControls button{border-radius:11px;font-size:11px;}
#gameControls .fire-control{border-color:rgba(255,160,174,.3);}
#gameControls .pause-control{border-color:rgba(235,213,151,.3);}
#joystick{border:1px solid rgba(175,190,255,.36);background:rgba(115,132,202,.12);backdrop-filter:blur(5px);}
#stick{background:rgba(165,179,255,.42);border:1px solid rgba(220,226,255,.72);box-shadow:0 4px 20px rgba(110,133,255,.16);}
.touch-btn{background:rgba(33,43,82,.76);border-color:rgba(173,190,255,.28);backdrop-filter:blur(8px);}
#fireTouch{background:rgba(153,91,125,.62);border-color:rgba(255,184,209,.4);}
.gameover-score{color:#b9e5f6;text-shadow:0 0 28px rgba(145,217,247,.15);}
.ship-card{
  border:1px solid rgba(173,190,255,.16);
  border-radius:16px;
  padding:18px;
  margin:12px 0;
  background:linear-gradient(145deg,rgba(43,51,91,.38),rgba(14,20,43,.55));
  text-align:left;
}
.ship-card h2{font-size:16px;letter-spacing:.04em;}
.ship-card p{color:#b9c5e1;font-size:12px;line-height:1.7;}
#upgradeChoices{gap:12px;}
.upgrade-card{
  min-height:136px;
  border-color:rgba(190,174,255,.25);
  border-radius:16px;
  background:linear-gradient(150deg,rgba(71,62,120,.48),rgba(18,24,52,.96));
  text-align:left;
}
.upgrade-card:hover{border-color:rgba(198,188,255,.7);}
.upgrade-card strong{color:#d4caff;font-size:12px;letter-spacing:.04em;}
.upgrade-card span{color:#c5cee7;font-size:12px;line-height:1.65;}
#bossBar{border-color:rgba(225,170,220,.65);background:rgba(39,20,49,.8);}
#bossBarFill{background:linear-gradient(90deg,#8b91f6,#e9a8d0);box-shadow:0 0 12px rgba(200,164,255,.28);}
#jsError{
  border-color:#df929d;
  border-radius:14px;
  background:#24131f;
  color:#ffd8df;
}
@media(max-width:700px){
  .panel{width:min(560px,96vw);padding:24px 18px;border-radius:22px;}
  .subtitle{margin-bottom:22px;}
  .menu-buttons{gap:6px;}
  .menu-buttons>button:not(.primary){min-height:43px;}
  .neon-stats{gap:6px;}
  .neon-stats span{padding:8px 9px;font-size:10px;}
  .info-grid{gap:9px;}
  .info{padding:14px;}
  .hud-box{border-radius:11px;background:rgba(8,12,29,.82);}
  #upgradeChoices{grid-template-columns:1fr;}
  .upgrade-card{min-height:78px;}
}
@media(prefers-reduced-motion:reduce){
  button{transition:none;}
}


/* UI POLISH PASS — depth, hierarchy, and quieter micro-interactions */
body::before{
  content:"";
  position:fixed;
  inset:0;
  z-index:1;
  pointer-events:none;
  opacity:.68;
  background:
    radial-gradient(ellipse at 16% 18%,rgba(135,154,239,.09),transparent 34%),
    radial-gradient(ellipse at 84% 78%,rgba(132,205,226,.07),transparent 32%),
    linear-gradient(135deg,rgba(255,255,255,.012),transparent 42%);
}
.screen.active .panel{
  animation:panel-arrive .36s cubic-bezier(.2,.75,.25,1) both;
}
@keyframes panel-arrive{
  from{opacity:0;transform:translateY(9px) scale(.99);}
  to{opacity:1;transform:translateY(0) scale(1);}
}
.panel{
  position:relative;
  isolation:isolate;
  border-color:rgba(184,197,255,.17);
}
.panel::before{
  content:"";
  position:absolute;
  top:0;
  left:12%;
  right:12%;
  height:1px;
  pointer-events:none;
  background:linear-gradient(90deg,transparent,rgba(203,215,255,.5),transparent);
}
.panel h1{
  text-wrap:balance;
}
.menu-buttons{
  width:100%;
}
.menu-buttons>button{
  max-width:100%;
}
.menu-buttons>button:not(.primary){
  background:rgba(255,255,255,.025);
  border-color:rgba(173,190,255,.13);
  color:#dce2f8;
}
.menu-buttons>button:not(.primary):hover{
  background:rgba(173,190,255,.075);
  border-color:rgba(184,197,255,.34);
}
.info,.ship-card,.upgrade-card,.neon-stats span{
  box-shadow:inset 0 1px 0 rgba(255,255,255,.025);
}
.info:hover,.ship-card:hover{
  border-color:rgba(173,190,255,.25);
}
#pauseHint{
  color:#8e9bbd;
  letter-spacing:.015em;
}
#gameControls button,#touchControls button{
  -webkit-tap-highlight-color:transparent;
  user-select:none;
}
#gameControls button:active,#touchControls button:active{
  filter:brightness(1.12);
}
#healthBar,#energyBar{
  border-radius:inherit;
}
#healthOuter,#energyOuter{
  box-shadow:inset 0 1px 2px rgba(0,0,0,.28);
}
::selection{
  color:#10162c;
  background:#c3c8ff;
}
@media(hover:hover) and (pointer:fine){
  .info,.ship-card{transition:border-color .18s ease,background .18s ease;}
}
@media(prefers-reduced-motion:reduce){
  .screen.active .panel{animation:none;}
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
            <div>BUILD <b id="evolutionLabel">STANDARD</b></div>
            <div>WEAPON <b id="weaponLabel">PULSE</b></div>
            <div>MODE <b id="modeLabel">SURVIVAL</b></div>
            <div id="runTimerRow">TIME <b id="runTimerLabel">00:00</b></div>
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

        <svg class="brand-mark" viewBox="0 0 80 80" role="img" aria-label="VOID SPACE logo" xmlns="http://www.w3.org/2000/svg">
            <defs><linearGradient id="shipGlow" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#8be2ff"/><stop offset="1" stop-color="#5365ff"/></linearGradient></defs>
            <rect x="3" y="3" width="74" height="74" rx="20" fill="#071329" stroke="#397eb7" stroke-opacity=".65"/>
            <circle cx="40" cy="40" r="27" fill="none" stroke="#28618c" stroke-dasharray="3 6"/>
            <path d="M55 40 21 24l8 16-8 16z" fill="url(#shipGlow)" stroke="#e5f8ff" stroke-width="2" stroke-linejoin="round"/>
            <circle cx="49" cy="40" r="4" fill="#fff"/>
        </svg>
        <div class="logo">VOID</div>
        <div class="subtitle">SPACE</div>

        <div class="menu-buttons">

            <button class="primary" id="startButton">
                START GAME
            </button>
            <button id="modeSelectButton">GAME MODES</button>
            <button id="achievementsButton">ACHIEVEMENTS</button>
            <button id="saveToolsButton">SAVE BACKUP / RESTORE</button>

            <button id="howButton">
                HOW TO PLAY
            </button>

            <button id="hangarButton">SHIP HANGAR</button>
            <button id="missionsButton">MISSIONS & RECORDS</button>
            <button id="installButton" hidden>INSTALL VOID SPACE</button>
            <button id="settingsButton">SETTINGS</button>
            <div class="neon-stats"><span>◈ CREDITS <b id="metaCoins">0</b></span><span>✦ LEVEL <b id="metaLevel">1</b></span><span>🏆 BEST <b id="metaBest">0</b></span></div>

        </div>

        <div class="small" style="margin-top:25px">
            NEON ROGUELITE • LOCAL SAVES • FREE
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
            <span class="setting-value">AUTO</span>
        </div>
        <div class="setting-row"><span>SOUND EFFECTS</span><button id="soundToggle">ON</button></div>
        <div class="setting-row"><span>SCREEN SHAKE</span><button id="shakeToggle">ON</button></div>
        <div class="setting-row"><span>VISUAL FX</span><button id="fxToggle">FULL</button></div>

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

<div class="screen" id="hangarScreen"><div class="panel"><h1>SHIP HANGAR</h1><p style="color:#9dcaff;margin:12px">Choose a ship with unique stats.</p><div id="shipCards"></div><button id="skillTreeButton">SHIP SKILL TREE</button><button id="hangarBackButton">BACK</button></div></div>
<div class="screen" id="skillTreeScreen"><div class="panel"><h1>SHIP SKILL TREE</h1><p style="color:#9dcaff;margin:12px">Permanent upgrades for the currently selected ship. Ranks are saved on this device.</p><div class="neon-stats"><span>◈ CREDITS <b id="skillCoins">0</b></span><span>SHIP <b id="skillShipName">NEON STRIKER</b></span></div><div id="skillTreeCards"></div><button id="skillTreeBackButton">BACK TO HANGAR</button></div></div>
<div class="screen" id="missionScreen"><div class="panel"><h1>MISSIONS & RECORDS</h1><div id="missionContent" style="line-height:2;color:#c7d9ff;margin:20px 0"></div><button id="missionBackButton">BACK</button></div></div>
<div class="screen" id="modeScreen"><div class="panel"><h1>SELECT GAME MODE</h1><p style="color:#9dcaff;margin:10px">Choose your challenge. All modes are free.</p><div class="feature-grid">
<button data-mode="survival">SURVIVAL <small>Classic escalating waves</small></button><button data-mode="endless">ENDLESS <small>Push your highest wave</small></button><button data-mode="bossrush">BOSS RUSH <small>Boss encounters every wave</small></button><button data-mode="timeattack">TIME ATTACK <small>Three minutes to score</small></button><button data-mode="hardcore">HARDCORE <small>One life, no second chances</small></button><button id="campaignOpenButton">CAMPAIGN <small>Clear three sectors and their bosses</small></button>
</div><button id="modeBackButton">BACK</button></div></div>
<div class="screen" id="campaignScreen"><div class="panel"><h1>SECTOR CAMPAIGN</h1><p style="color:#9dcaff;margin:10px">Choose a route. Clear wave 8 and survive the sector.</p><div class="feature-grid"><button data-route="derelict">DERELICT BELT <small>Asteroids and wreckage</small></button><button data-route="ionstorm">ION STORM <small>Charged debris field</small></button><button data-route="singularity">SINGULARITY EDGE <small>Dark matter hazards</small></button></div><button id="campaignBackButton">BACK TO MODES</button></div></div>
<div class="screen" id="achievementsScreen"><div class="panel"><h1>ACHIEVEMENTS</h1><p style="color:#9dcaff;margin:10px">Earn badges through play. Progress is stored locally.</p><div id="achievementCards"></div><button id="achievementsBackButton">BACK</button></div></div>
<div class="screen" id="saveToolsScreen"><div class="panel"><h1>LOCAL SAVE TOOLS</h1><p style="color:#9dcaff;margin:10px">Export or restore a VOID SPACE profile. No account or server database.</p><div id="saveStatus" style="margin:16px;color:#c7d9ff"></div><button id="exportSaveButton">EXPORT SAVE JSON</button><button id="importSaveButton">IMPORT SAVE JSON</button><input id="importSaveFile" type="file" accept="application/json,.json" hidden><button id="saveToolsBackButton">BACK</button></div></div>
<div class="screen" id="upgradeScreen"><div class="panel"><h1>LEVEL UP // CHOOSE AN UPGRADE</h1><p style="color:#9dcaff;margin-top:10px">Pick a prototype to change your build.</p><div id="upgradeChoices"></div></div></div>
<div id="bombFlash"></div><div id="bossBar"><div id="bossName">BOSS</div><div id="bossBarFill"></div></div><div id="cinematicFlash"></div><div id="toastNotice" role="status" aria-live="polite"></div>
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

<!-- DESKTOP / KEYBOARD-ASSISTED CONTROLS -->
<div id="gameControls" aria-label="Game controls">
    <button data-hold="KeyA" aria-label="Rotate left">↶ LEFT</button>
    <button data-hold="KeyW" aria-label="Move forward">↑ THRUST</button>
    <button data-hold="KeyS" aria-label="Move backward">↓ BRAKE</button>
    <button class="fire-control" data-hold="Space" aria-label="Fire weapon">✦ FIRE</button>
    <button data-action="bomb" aria-label="Use bomb">◎ BOMB</button>
    <button data-hold="ShiftLeft" aria-label="Boost">⚡ BOOST</button>
    <button class="pause-control" data-action="pause" aria-label="Pause game">Ⅱ PAUSE</button>
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
    "gameOverScreen","hangarScreen","missionScreen","upgradeScreen","skillTreeScreen","modeScreen","campaignScreen","achievementsScreen","saveToolsScreen"
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

    if(!audioContext || window.voidSoundEnabled===false) return;

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

    score=0;wave=1;kills=0;runCoins=0;runXP=0;runTime=0;runEndedByVictory=false;runWeaponIndex=0;weaponLevel=0;hazardTimer=4;asteroids=[];cinematicSlow=0;screenFlash=0;runUpgrades={damage:0,fire:0,engine:0,hull:0,critical:0,magnet:0,pierce:0,shield:0,bomb:0,regen:0,drone:0};

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

    const ship=ships[selectedShip]||ships.striker;const skill=shipSkills[selectedShip]||{hull:0,thrusters:0,reactor:0,weapon:0};player.maxHealth=ship.hp+skill.hull*8;player.health=player.maxHealth;player.maxEnergy=100+skill.reactor*5;player.energy=player.maxEnergy;player.shipSpeed=ship.speed*(1+skill.thrusters*.035);player.shipDamage=ship.damage*(1+skill.weapon*.04);

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

function endGame(victory=false){

    if(!running) return;

    running = false;
    paused = false;
    runEndedByVictory=!!victory;
    document.querySelector("#gameOverScreen h1").textContent=victory?"SECTOR CLEARED":"GAME OVER";
    if(victory){campaignWins++;campaignProgress[currentRoute]=(campaignProgress[currentRoute]||0)+1;awardVoidCoins(500+wave*25);awardVoidXP(300);createBurst(player.x,player.y,150,12,"#ffe9a6");screenFlash=.9;}
    modeRecords[currentGameMode]=Math.max(modeRecords[currentGameMode]||0,score);
    checkVoidAchievements();
    document.getElementById("finalScore").textContent =
        score.toLocaleString();

    document.getElementById("finalWave").textContent =
        wave;

    document.getElementById("finalKills").textContent=kills;bestScore=Math.max(bestScore,score);bestWave=Math.max(bestWave,wave);saveVoidProfile();paintMeta();

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

document.getElementById("settingsButton").addEventListener("click",()=>showScreen("settingsScreen"));
window.voidSoundEnabled=true;window.voidShakeEnabled=true;window.voidFxEnabled=true;
document.getElementById("soundToggle")?.addEventListener("click",e=>{window.voidSoundEnabled=!(window.voidSoundEnabled!==false);e.currentTarget.textContent=window.voidSoundEnabled?"ON":"OFF";saveVoidProfile();});
document.getElementById("shakeToggle")?.addEventListener("click",e=>{window.voidShakeEnabled=!(window.voidShakeEnabled!==false);e.currentTarget.textContent=window.voidShakeEnabled?"ON":"OFF";saveVoidProfile();});
document.getElementById("fxToggle")?.addEventListener("click",e=>{window.voidFxEnabled=!(window.voidFxEnabled!==false);e.currentTarget.textContent=window.voidFxEnabled?"FULL":"LITE";saveVoidProfile();});
document.getElementById("hangarButton").addEventListener("click",()=>{renderVoidHangar();showScreen("hangarScreen")});
document.getElementById("missionsButton").addEventListener("click",()=>{renderVoidMissions();showScreen("missionScreen")});
document.getElementById("modeSelectButton").addEventListener("click",()=>showScreen("modeScreen"));
document.getElementById("modeBackButton").addEventListener("click",()=>showScreen("menuScreen"));
document.getElementById("campaignOpenButton").addEventListener("click",()=>showScreen("campaignScreen"));
document.getElementById("campaignBackButton").addEventListener("click",()=>showScreen("modeScreen"));
document.querySelectorAll("[data-mode]").forEach(b=>b.addEventListener("click",()=>{currentGameMode=b.dataset.mode;currentRoute="derelict";startGame();}));
document.querySelectorAll("[data-route]").forEach(b=>b.addEventListener("click",()=>{currentGameMode="campaign";currentRoute=b.dataset.route;startGame();}));
document.getElementById("achievementsButton").addEventListener("click",()=>{renderVoidAchievements();showScreen("achievementsScreen")});
document.getElementById("achievementsBackButton").addEventListener("click",()=>showScreen("menuScreen"));
document.getElementById("saveToolsButton").addEventListener("click",()=>{renderSaveTools();showScreen("saveToolsScreen")});
document.getElementById("saveToolsBackButton").addEventListener("click",()=>showScreen("menuScreen"));
document.getElementById("exportSaveButton").addEventListener("click",exportVoidSave);
document.getElementById("importSaveButton").addEventListener("click",()=>document.getElementById("importSaveFile").click());
document.getElementById("importSaveFile").addEventListener("change",importVoidSave);
document.getElementById("skillTreeButton").addEventListener("click",()=>{renderVoidSkillTree();showScreen("skillTreeScreen")});
document.getElementById("skillTreeBackButton").addEventListener("click",()=>{renderVoidHangar();showScreen("hangarScreen")});
document.getElementById("hangarBackButton").addEventListener("click",()=>showScreen("menuScreen"));
document.getElementById("missionBackButton").addEventListener("click",()=>showScreen("menuScreen"));
window.addEventListener("beforeinstallprompt",e=>{e.preventDefault();installPrompt=e;document.getElementById("installButton").hidden=false});
document.getElementById("installButton").addEventListener("click",async()=>{if(installPrompt){installPrompt.prompt();await installPrompt.userChoice;installPrompt=null;document.getElementById("installButton").hidden=true}});
try{if("serviceWorker" in navigator&&location.protocol!=="file:")navigator.serviceWorker.register("/sw.js").catch(()=>{})}catch(e){}

document.getElementById("howBackButton")
    .addEventListener("click",()=>{
        showScreen("menuScreen");
    });

document.getElementById("settingsBackButton")
    .addEventListener("click",()=>{
        showScreen("menuScreen");
    });


/* =========================================================
   ON-SCREEN DESKTOP CONTROL DOCK
========================================================= */
const gameControls = document.getElementById("gameControls");
if(gameControls){
    gameControls.querySelectorAll("[data-hold]").forEach((button)=>{
        const code = button.dataset.hold;
        const press = (event)=>{
            event.preventDefault();
            keys[code] = true;
            if(code === "Space") keys.MouseFire = true;
        };
        const release = (event)=>{
            event.preventDefault();
            keys[code] = false;
            if(code === "Space") keys.MouseFire = false;
        };
        button.addEventListener("pointerdown",press);
        ["pointerup","pointercancel","pointerleave","lostpointercapture"].forEach(type=>{
            button.addEventListener(type,release);
        });
        button.addEventListener("contextmenu",event=>event.preventDefault());
    });
    gameControls.querySelectorAll("[data-action]").forEach(button=>{
        button.addEventListener("click",()=>{
            if(button.dataset.action === "bomb") useBomb();
            if(button.dataset.action === "pause") togglePause();
        });
    });
}

/* Keep held controls from sticking when focus changes or the tab is hidden. */
document.addEventListener("visibilitychange",()=>{
    if(document.hidden){
        for(const code in keys) keys[code] = false;
        if(running && !paused) togglePause();
    }
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
    if(code==="KeyQ"&&!e.repeat&&running){runWeaponIndex=(runWeaponIndex+1)%weaponDefs.length;toastNotice("WEAPON SWITCHED: "+weaponDefs[runWeaponIndex].name);}

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

    player.fireCooldown=Math.max(.055,.12-runUpgrades.fire*.012);

    const weapon=weaponDefs[runWeaponIndex].id,speed=weaponDefs[runWeaponIndex].speed||720,evolved=voidWeaponEvolution();
    const baseCount=runUpgrades.critical>=4?3:(runUpgrades.critical>=2?2:1),shotCount=baseCount+(evolved==="STARSTORM"?2:0);
    const shotDamage=(30+runUpgrades.damage*12)*(player.shipDamage||1)*(Math.random()<Math.min(.35,runUpgrades.critical*.05)?2:1)*(evolved==="PLASMA SWARM"?1.35:1)*(1+weaponLevel*.12);
    const angles=weapon==="shotgun"?Array.from({length:5},(_,i)=>player.angle+(i-2)*.22):Array.from({length:shotCount},(_,i)=>player.angle+(i-(shotCount-1)/2)*.12);
    for(const angle of angles){const missile=weapon==="missile",rail=weapon==="railgun",chain=weapon==="chain",blackhole=weapon==="blackhole";bullets.push({damage:shotDamage*(weapon==="shotgun"?.55:missile?1.5:rail?1.8:1),x:player.x+Math.cos(angle)*20,y:player.y+Math.sin(angle)*20,vx:Math.cos(angle)*speed+player.vx*.2,vy:Math.sin(angle)*speed+player.vy*.2,life:missile?2.2:1.1,radius:missile?5:rail?4:3,pierce:runUpgrades.pierce+(evolved==="PHASE LANCE"?2:0)+(rail?99:0),homing:missile,chain:chain?3:0,splash:blackhole?100:0,blackhole,color:weaponDefs[runWeaponIndex].color});}
    for(let d=0;d<Math.min(3,runUpgrades.drone);d++){const side=d%2===0?-1:1,angle=player.angle+side*.32;bullets.push({damage:shotDamage*.65,x:player.x+Math.cos(angle)*18,y:player.y+Math.sin(angle)*18,vx:Math.cos(angle)*speed+player.vx*.2,vy:Math.sin(angle)*speed+player.vy*.2,life:1.1,radius:3,pierce:runUpgrades.pierce,color:"#8be2ff"});}
    for(let d=0;d<Math.min(3,runUpgrades.drone);d++){
        const side= d%2===0?-1:1, angle=player.angle+side*.32;
        bullets.push({damage:shotDamage*.65,x:player.x+Math.cos(angle)*18,y:player.y+Math.sin(angle)*18,vx:Math.cos(angle)*speed+player.vx*.2,vy:Math.sin(angle)*speed+player.vy*.2,life:1.1,radius:3,pierce:runUpgrades.pierce+(evolved==="PHASE LANCE"?2:0)});
    }

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
    const evolution=voidWeaponEvolution();

    if(!running || paused) return;

    if(player.bombCooldown > 0) return;

    if(player.energy < 35) return;

    player.energy -= 35;

    player.bombCooldown = 8;

    const radius=Math.min(Math.max(W,H)*.62,520)*(evolution==="NOVA SINGULARITY"?1.3:1);bombSlow=1.15;bombFx={x:player.x,y:player.y,r:12,max:radius,life:.95};const flash=document.getElementById("bombFlash");flash.style.transition="none";flash.style.opacity=".95";requestAnimationFrame(()=>{flash.style.transition="opacity .9s ease-out";flash.style.opacity="0"});
    for(let i=bullets.length-1;i>=0;i--){const b=bullets[i];if(b.enemyBullet&&Math.hypot(b.x-player.x,b.y-player.y)<radius)bullets.splice(i,1);}

    for(const enemy of enemies){

        const dx = enemy.x-player.x;
        const dy = enemy.y-player.y;

        const d = Math.sqrt(dx*dx+dy*dy);

        if(d < radius){

            enemy.health-=(90+runUpgrades.damage*22+runUpgrades.bomb*28)*(player.shipDamage||1);

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

    const roll=Math.random();
    let type="fighter";

    if(roll<.10&&wave>=4)type="sniper";else if(roll<.22&&wave>=3)type="tank";else if(roll<.42&&wave>=2)type="fast";

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

    }else if(type==="sniper"){
        enemy={x,y,vx:0,vy:0,radius:15,speed:65+wave*1.5,health:38+wave*6,maxHealth:38+wave*6,damage:14,type,score:95,fireTimer:1.2};
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
    const kinds=[{name:"DREADNOUGHT",color:"#bd65ff"},{name:"VOID WRAITH",color:"#57e8ff"},{name:"NOVA COLOSSUS",color:"#ff8bca"}];
    const kind=kinds[Math.max(0,Math.floor(wave/5)-1)%kinds.length];
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

        type:"boss",bossName:kind.name,bossColor:kind.color,bossKind:Math.max(0,Math.floor(wave/5)-1)%kinds.length,phase:1,
        score:1000,boss:true,fireTimer:1.8

    });

    createBurst(W/2,100,50,6);

    sound(55,.8,"sawtooth",.06);
}


/* =========================================================
   POWERUPS
========================================================= */

function spawnPowerup(){

    const types=["health","energy","rapid","bomb","weapon","shield","coins"];

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

    if(power.type==="weapon"){runWeaponIndex=(runWeaponIndex+1)%weaponDefs.length;weaponLevel=Math.min(5,weaponLevel+1);toastNotice("WEAPON ACQUIRED: "+weaponDefs[runWeaponIndex].name);}
    else if(power.type==="shield"){player.invincible=Math.max(player.invincible,5);}
    else if(power.type==="coins"){awardVoidCoins(40);}
    else if(power.type === "health"){

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

function createBurst(x,y,count,power,color){

    count=window.voidFxEnabled===false?Math.ceil(count*.35):count;
    const particleCap=window.voidFxEnabled===false?160:420;
    while(particles.length+count>particleCap)particles.shift();
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

            size:1+Math.random()*3,
            color:color||"#8edcff"

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

    if(runUpgrades.regen>0 && player.health<player.maxHealth)player.health=Math.min(player.maxHealth,player.health+runUpgrades.regen*1.15*dt*(voidWeaponEvolution()==="AEGIS ENGINE"?2:1));
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

    const acceleration=310*(player.shipSpeed||1)*(1+runUpgrades.engine*.08);

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
        if(b.homing&&!b.enemyBullet&&enemies.length){let target=null,best=Infinity;for(const e of enemies){const d=distance(b,e);if(d<best){best=d;target=e;}}if(target){const a=Math.atan2(target.y-b.y,target.x-b.x),v=Math.hypot(b.vx,b.vy)||720;b.vx+=(Math.cos(a)*v-b.vx)*Math.min(1,dt*3.5);b.vy+=(Math.sin(a)*v-b.vy)*Math.min(1,dt*3.5);}}

        b.x += b.vx*dt;
        b.y += b.vy*dt;

        if(!b.enemyBullet&&asteroids.length){let consumed=false;for(let j=asteroids.length-1;j>=0;j--){const rock=asteroids[j];if(distance(b,rock)<rock.radius+b.radius){rock.health-=b.damage||25;b.life=0;consumed=true;createBurst(b.x,b.y,5,2,b.color||"#9bb6d5");if(rock.health<=0){createBurst(rock.x,rock.y,22,5,"#ffc68b");if(Math.random()<.16)powerups.push({x:rock.x,y:rock.y,radius:13,type:"coins",life:12});asteroids.splice(j,1);}break;}}if(consumed){bullets.splice(i,1);continue;}}
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

        }else if(enemy.type==="sniper"){
            enemy.vx=nx*enemy.speed*.55;enemy.vy=ny*enemy.speed*.55;enemy.x+=enemy.vx*dt;enemy.y+=enemy.vy*dt;enemy.fireTimer-=dt;if(enemy.fireTimer<=0){enemy.fireTimer=1.4;bullets.push({x:enemy.x,y:enemy.y,vx:nx*300,vy:ny*300,life:4,radius:5,enemyBullet:true});}
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

                if(runUpgrades.shield>0){runUpgrades.shield--;player.invincible=.8;createBurst(player.x,player.y,14,3);}
                else{player.health -= enemy.damage;player.invincible=.8;}


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

            score+=enemy.score;kills++;awardVoidCoins(enemy.boss?80:Math.max(2,Math.round(enemy.score/12)));awardVoidXP(enemy.boss?180:Math.max(8,Math.round(enemy.score/3)));

            createBurst(
                enemy.x,
                enemy.y,
                enemy.boss ? 100 : 25,
                enemy.boss ? 9 : 4
            );

            if(enemy.boss){

                score+=2000;awardVoidCoins(250+wave*10);awardVoidXP(250);

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

                    if(runUpgrades.shield>0){runUpgrades.shield--;createBurst(player.x,player.y,12,3);}
                    else{player.health -= 12;}
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

                const dealt=bullet.damage||(enemy.boss?16:30);enemy.health-=dealt;
                if(bullet.splash){for(const other of enemies){if(other!==enemy&&distance(bullet,other)<bullet.splash){other.health-=dealt*.55;if(bullet.blackhole){other.x+=(bullet.x-other.x)*.12;other.y+=(bullet.y-other.y)*.12;}}}createBurst(bullet.x,bullet.y,30,6,"#c29bff");}
                if(bullet.chain>0){let left=bullet.chain,origin=enemy;while(left-->0){let target=null,nearest=Infinity;for(const other of enemies){if(other===origin)continue;const d=distance(origin,other);if(d<nearest&&d<190){nearest=d;target=other;}}if(!target)break;target.health-=dealt*.45;createBurst(target.x,target.y,9,3,"#72f7ff");origin=target;}}

                createBurst(
                    bullet.x,
                    bullet.y,
                    5,
                    2
                );

                hit = true;
                if(bullet.pierce>0){bullet.pierce--;hit=false;continue;}
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
           p.radius+player.radius+runUpgrades.magnet*35){

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
    if(currentGameMode==="timeattack"&&runTime>=180){endGame(false);return;}
    if(currentGameMode==="campaign"&&wave>=8&&enemies.length===0){endGame(true);return;}

    /*
       New wave every 18 seconds if
       current enemies are mostly cleared.
    */

    if(
        waveTimer > (currentGameMode==="bossrush"?12:currentGameMode==="campaign"?15:18) &&
        enemies.filter(e=>!e.boss).length < (currentGameMode==="bossrush"?2:5)
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

        if(currentGameMode==="bossrush"||wave%5===0)spawnBoss();
        if(wave%3===0)offerVoidUpgrades();
    }

    enemySpawnTimer -= dt;
    hazardTimer-=dt;
    if(hazardTimer<=0&&asteroids.length<7){spawnAsteroid();hazardTimer=7+Math.random()*5;}

    const enemyCount =
        enemies.filter(e=>!e.boss).length;

    const maximum =
        Math.min(
            8+wave*2,
            35
        );

    if(
        enemySpawnTimer <= 0 &&
        enemyCount < maximum && !(currentGameMode==="campaign"&&wave>=8)
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

    dt=Math.min(dt,.033);runTime+=dt;
    if(bombSlow>0){bombSlow=Math.max(0,bombSlow-dt);dt*=.22;}
    if(cinematicSlow>0){cinematicSlow=Math.max(0,cinematicSlow-dt);dt*=.28;}
    screenFlash=Math.max(0,screenFlash-dt*1.5);toastTimer=Math.max(0,toastTimer-dt);

    updateStars(dt);
    updatePlayer(dt);
    updateBullets(dt);
    updateEnemies(dt);
    updateHazards(dt);
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

    ctx.save();if(window.voidShakeEnabled!==false&&bombSlow>0)ctx.translate((Math.random()-.5)*12,(Math.random()-.5)*12);
    ctx.fillStyle="#02030a";ctx.fillRect(0,0,W,H);if(window.voidFxEnabled!==false){const neb=ctx.createRadialGradient(W*.72,H*.28,0,W*.72,H*.28,Math.max(W,H)*.72);neb.addColorStop(0,"rgba(105,30,160,.18)");neb.addColorStop(.5,"rgba(15,70,130,.07)");neb.addColorStop(1,"rgba(0,0,0,0)");ctx.fillStyle=neb;ctx.fillRect(0,0,W,H);}

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

    ctx.restore();
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

    ctx.fillStyle=enemy.boss?"#a23dff":enemy.type==="sniper"?"#ffb347":enemy.type==="tank"?"#8e2938":enemy.type==="fast"?"#e54a61":"#bd354f";

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

    for(const enemy of enemies)drawEnemy(enemy);
    const boss=enemies.find(e=>e.boss),bar=document.getElementById("bossBar");if(bar){bar.style.display=boss&&running?"block":"none";if(boss){document.getElementById("bossBarFill").style.width=Math.max(0,boss.health/boss.maxHealth*100)+"%";document.getElementById("bossName").textContent=(boss.bossName||"BOSS")+" • PHASE "+(boss.phase||1);document.getElementById("bossBarFill").style.background=boss.bossColor||"linear-gradient(90deg,#6b5bff,#ff42d0)";}}
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
        if(p.type === "bomb") symbol = "B";if(p.type==="weapon")symbol="W";if(p.type==="shield")symbol="S";if(p.type==="coins")symbol="¢";

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

        ctx.fillStyle = p.color || "#8edcff";

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
    if(bombFx){bombFx.life-=.016;bombFx.r=bombFx.max*(1-Math.pow(Math.max(0,bombFx.life/.95),2));ctx.save();ctx.globalAlpha=Math.max(0,bombFx.life/.95);ctx.strokeStyle="#8cf7ff";ctx.lineWidth=5;ctx.shadowBlur=35;ctx.shadowColor="#f0f";ctx.beginPath();ctx.arc(bombFx.x,bombFx.y,bombFx.r,0,Math.PI*2);ctx.stroke();ctx.restore();if(bombFx.life<=0)bombFx=null;}
    drawParticles();
    drawHazards();
    drawPowerups();
    drawBullets();
    drawEnemies();
    drawAim();

    if(running){
        drawPlayer();
    }
    if(screenFlash>0){ctx.save();ctx.globalAlpha=Math.min(.8,screenFlash);ctx.fillStyle="#d8c9ff";ctx.fillRect(0,0,W,H);ctx.restore();}
    const toast=document.getElementById("toastNotice");if(toast){toast.textContent=toastMessage;toast.style.borderColor=toastColor;toast.classList.toggle("show",toastTimer>0);}
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
    const weaponLabel=document.getElementById("weaponLabel");if(weaponLabel)weaponLabel.textContent=weaponDefs[runWeaponIndex].name+(weaponLevel?" +"+weaponLevel:"");
    const modeLabel=document.getElementById("modeLabel");if(modeLabel)modeLabel.textContent=currentGameMode.toUpperCase();
    const timerLabel=document.getElementById("runTimerLabel");if(timerLabel)timerLabel.textContent=Math.floor(runTime/60).toString().padStart(2,"0")+":"+Math.floor(runTime%60).toString().padStart(2,"0");
    checkVoidAchievements();

    const evolutionLabel=document.getElementById("evolutionLabel");
    if(evolutionLabel)evolutionLabel.textContent=voidWeaponEvolution()||"STANDARD";

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

    if(gameControls){
        gameControls.style.display = running && !paused && window.matchMedia("(pointer: fine) and (min-width: 701px)").matches ? "grid" : "none";
    }
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



/* VOID SPACE EXPANSION: progression, ship hangar, run upgrades and PWA */
let bankCoins=0,pilotLevel=1,xpProgress=0,xpNext=100,runXP=0,runCoins=0,bestScore=0,bestWave=1;
let currentGameMode="survival",currentRoute="derelict",runTime=0,runEndedByVictory=false,runWeaponIndex=0,weaponLevel=0,asteroids=[],hazardTimer=5,cinematicSlow=0,screenFlash=0,toastTimer=0,toastMessage="",toastColor="#8be2ff";
let unlockedAchievements=[],lifetimeKills=0,bossesDefeated=0,campaignWins=0,campaignProgress={},modeRecords={};
let selectedShip="striker",ownedShips=["striker"],shipSkills={},runUpgrades={damage:0,fire:0,engine:0,hull:0,critical:0,magnet:0,pierce:0,shield:0,bomb:0,regen:0,drone:0},installPrompt=null,bombFx=null,bombSlow=0;
const ships={striker:{name:"NEON STRIKER",cost:0,hp:100,speed:1,damage:1,desc:"Balanced all-rounder"},phantom:{name:"VOID PHANTOM",cost:350,hp:80,speed:1.28,damage:1.15,desc:"Fast interceptor"},titan:{name:"NOVA TITAN",cost:600,hp:155,speed:.82,damage:1.28,desc:"Heavy assault"},spectre:{name:"PRISM SPECTRE",cost:1000,hp:110,speed:1.12,damage:1.55,desc:"Prototype high damage"}};
function loadVoidProfile(){try{const p=JSON.parse(localStorage.getItem("voidSpaceProfile")||"{}");bankCoins=p.coins||0;pilotLevel=p.level||1;xpProgress=p.xp||0;xpNext=p.next||100;selectedShip=ships[p.ship]?p.ship:"striker";ownedShips=Array.isArray(p.owned)?p.owned.filter(id=>ships[id]):["striker"];if(!ownedShips.includes("striker"))ownedShips.unshift("striker");if(!ownedShips.includes(selectedShip))selectedShip="striker";shipSkills=p.shipSkills&&typeof p.shipSkills==="object"?p.shipSkills:{};for(const id of Object.keys(ships)){if(!shipSkills[id]||typeof shipSkills[id]!=="object")shipSkills[id]={};for(const k of ["hull","thrusters","reactor","weapon"])shipSkills[id][k]=Math.max(0,Math.min(5,Number(shipSkills[id][k])||0));}bestScore=p.best||0;bestWave=p.wave||1;unlockedAchievements=Array.isArray(p.achievements)?p.achievements:[];lifetimeKills=Number(p.lifetimeKills)||0;bossesDefeated=Number(p.bossesDefeated)||0;campaignWins=Number(p.campaignWins)||0;campaignProgress=p.campaignProgress&&typeof p.campaignProgress==="object"?p.campaignProgress:{};modeRecords=p.modeRecords&&typeof p.modeRecords==="object"?p.modeRecords:{};window.voidSoundEnabled=p.sound!==false;window.voidShakeEnabled=p.shake!==false;window.voidFxEnabled=p.fx!==false;}catch(e){shipSkills={};unlockedAchievements=[];for(const id of Object.keys(ships))shipSkills[id]={hull:0,thrusters:0,reactor:0,weapon:0};}}
function saveVoidProfile(){try{const profile={version:3,savedAt:Date.now(),coins:bankCoins,level:pilotLevel,xp:xpProgress,next:xpNext,ship:selectedShip,owned:ownedShips,shipSkills,best:bestScore,wave:bestWave,achievements:unlockedAchievements,lifetimeKills,bossesDefeated,campaignWins,campaignProgress,modeRecords,sound:window.voidSoundEnabled!==false,shake:window.voidShakeEnabled!==false,fx:window.voidFxEnabled!==false};localStorage.setItem("voidSpaceProfile",JSON.stringify(profile));window.voidSaveAvailable=true;}catch(e){window.voidSaveAvailable=false;console.warn("VOID SPACE local save unavailable; check browser storage settings.",e);}}
window.addEventListener("pagehide",saveVoidProfile);
document.addEventListener("visibilitychange",()=>{if(document.visibilityState==="hidden")saveVoidProfile();});
function paintMeta(){const vals={metaCoins:bankCoins,metaLevel:pilotLevel,metaBest:bestScore.toLocaleString()};for(const id in vals){const el=document.getElementById(id);if(el)el.textContent=vals[id];}}
function awardVoidXP(n){runXP+=n;xpProgress+=n;while(xpProgress>=xpNext){xpProgress-=xpNext;pilotLevel++;xpNext=Math.round(xpNext*1.2);offerVoidUpgrades();}saveVoidProfile();paintMeta();}
function awardVoidCoins(n){runCoins+=n;bankCoins+=n;saveVoidProfile();paintMeta();}
const runUpgradeDefs=[
["damage","OVERCHARGED CORE","+12 weapon damage per stack."],
["fire","RAPID-FIRE COILS","Shoot faster."],
["engine","ION AFTERBURNER","+8% thrust and mobility."],
["hull","REINFORCED HULL","+20 maximum health and heal 20."],
["critical","PRISM MULTI-SHOT","More critical damage; extra shots at higher stacks."],
["magnet","SALVAGE MAGNET","Pull nearby power-ups from farther away."],
["pierce","PHASE-PIERCER","Shots pass through +1 extra enemy per stack."],
["shield","AEGIS CHARGE","Block one hit per stack."],
["bomb","NOVA AMPLIFIER","Bombs deal +28 bonus damage per stack."],
["regen","NANITE REPAIR","Regenerate hull slowly over time."],
["drone","WINGMAN DRONE","Add a side cannon to each volley."]
];
function offerVoidUpgrades(){if(!running||paused||!document.getElementById("upgradeScreen"))return;paused=true;showScreen("upgradeScreen");const host=document.getElementById("upgradeChoices");host.innerHTML="";[...runUpgradeDefs].sort(()=>Math.random()-.5).slice(0,3).forEach(u=>{const b=document.createElement("button");b.className="upgrade-card";b.innerHTML="<strong>"+u[1]+"</strong><span>"+u[2]+"</span>";b.onclick=()=>{runUpgrades[u[0]]++;if(u[0]==="hull"){player.maxHealth+=20;player.health=Math.min(player.maxHealth,player.health+20)}if(u[0]==="shield")createBurst(player.x,player.y,22,4);paused=false;hideScreens();};host.appendChild(b);});}
function renderVoidHangar(){const host=document.getElementById("shipCards");host.innerHTML="";Object.entries(ships).forEach(([id,sh])=>{const own=ownedShips.includes(id),sel=selectedShip===id;const card=document.createElement("div");card.className="ship-card";const h=document.createElement("h2");h.textContent=sh.name+(sel?" • SELECTED":"");h.style.color="#ff9cec";card.appendChild(h);const p=document.createElement("p");p.textContent=sh.desc+" • Hull "+sh.hp+" • Thrust "+Math.round(sh.speed*100)+"% • Damage "+Math.round(sh.damage*100)+"%";p.style.margin="12px";card.appendChild(p);const b=document.createElement("button");b.textContent=own?(sel?"EQUIPPED":"SELECT SHIP"):"UNLOCK • ◈ "+sh.cost;b.disabled=sel||(!own&&bankCoins<sh.cost);b.onclick=()=>{if(!own){bankCoins-=sh.cost;ownedShips.push(id)}selectedShip=id;saveVoidProfile();paintMeta();renderVoidHangar()};card.appendChild(b);host.appendChild(card);});}
function renderVoidMissions(){document.getElementById("missionContent").innerHTML="<p>PILOT LEVEL: "+pilotLevel+" • XP "+xpProgress+"/"+xpNext+"</p><p>BANKED CREDITS: ◈ "+bankCoins+"</p><p>BEST SCORE: "+bestScore.toLocaleString()+"</p><p>DEEPEST WAVE: "+bestWave+"</p><p>SHIP COLLECTION: "+ownedShips.length+"/"+Object.keys(ships).length+"</p><p>RUN KILLS: "+Math.min(kills,25)+"/25</p><p>RUN WAVE: "+Math.min(wave,5)+"/5</p><p>PERMANENT SKILL RANKS: "+Object.values(shipSkills).reduce((n,s)=>n+Object.values(s).reduce((a,v)=>a+v,0),0)+"</p>";}
const voidSkillDefs=[
 {key:"hull",name:"TITANIUM HULL",desc:"+8 maximum hull per rank",base:100},
 {key:"thrusters",name:"ION THRUSTERS",desc:"+3.5% ship speed per rank",base:120},
 {key:"reactor",name:"QUANTUM REACTOR",desc:"+5 starting energy per rank",base:110},
 {key:"weapon",name:"WEAPON CALIBRATION",desc:"+4% ship weapon damage per rank",base:140}
];
function renderVoidSkillTree(){
 const host=document.getElementById("skillTreeCards");if(!host)return;
 const sh=ships[selectedShip]||ships.striker;
 const skill=shipSkills[selectedShip]||(shipSkills[selectedShip]={hull:0,thrusters:0,reactor:0,weapon:0});
 document.getElementById("skillCoins").textContent=bankCoins;
 document.getElementById("skillShipName").textContent=sh.name;
 host.innerHTML="";
 for(const def of voidSkillDefs){
  const rank=skill[def.key]||0,cost=Math.round(def.base*Math.pow(rank+1,1.55));
  const card=document.createElement("div");card.className="ship-card";card.style.margin="12px 0";
  const title=document.createElement("h2");title.textContent=def.name+" • RANK "+rank+"/5";title.style.color="#8be2ff";card.appendChild(title);
  const desc=document.createElement("p");desc.textContent=def.desc;desc.style.color="#b9c9e8";card.appendChild(desc);
  const b=document.createElement("button");b.textContent=rank>=5?"MAX RANK":("UPGRADE • ◈ "+cost);b.disabled=rank>=5||bankCoins<cost;
  b.onclick=()=>{if(rank>=5||bankCoins<cost)return;bankCoins-=cost;skill[def.key]=rank+1;saveVoidProfile();paintMeta();renderVoidSkillTree();};
  card.appendChild(b);host.appendChild(card);
 }
 const note=document.createElement("p");note.style.color="#8be2ff";note.textContent="Skills apply when a new run starts. Each ship has its own permanent skill ranks.";host.appendChild(note);
}
function voidWeaponEvolution(){
 if(runUpgrades.shield>=2&&runUpgrades.regen>=2)return "AEGIS ENGINE";
 if(runUpgrades.bomb>=3&&runUpgrades.magnet>=2)return "NOVA SINGULARITY";
 if(runUpgrades.pierce>=3&&runUpgrades.damage>=2)return "PHASE LANCE";
 if(runUpgrades.critical>=3&&runUpgrades.fire>=3)return "STARSTORM";
 if(runUpgrades.damage>=4&&runUpgrades.drone>=2)return "PLASMA SWARM";
 return "";
}

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

loadVoidProfile();createStars();updateHUD();paintMeta();
for(const [id,onText,offText,value] of [["soundToggle","ON","OFF",window.voidSoundEnabled],["shakeToggle","ON","OFF",window.voidShakeEnabled],["fxToggle","FULL","LITE",window.voidFxEnabled]]){const el=document.getElementById(id);if(el)el.textContent=value?onText:offText;}

</script>

</body>
</html>
"""


@app.route("/")
def index():
    # HTML is a complete static document; bypass Jinja parsing so CSS selectors
    # such as `{#id` are not mistaken for Jinja comment delimiters.
    return Response(HTML, mimetype="text/html")


@app.route("/manifest.json")
def pwa_manifest():
    return app.response_class(
        response='{"name":"VOID SPACE","short_name":"VOID SPACE","description":"Neon cyberpunk space survival roguelite","start_url":"/","scope":"/","display":"standalone","background_color":"#02030a","theme_color":"#02030a","orientation":"any","icons":[{"src":"/icon.svg","sizes":"any","type":"image/svg+xml","purpose":"any maskable"}]}',
        status=200,
        mimetype="application/manifest+json"
    )


@app.route("/favicon.ico")
def favicon():
    # Serve the same lightweight SVG icon for browsers requesting /favicon.ico.
    return pwa_icon()


@app.route("/icon.svg")
def pwa_icon():
    return app.response_class(
        response='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g"><stop stop-color="#63caff"/><stop offset="1" stop-color="#b84dff"/></linearGradient></defs><rect width="64" height="64" rx="15" fill="#040818"/><path d="M47 32 14 17l8 15-8 15z" fill="url(#g)" stroke="#fff" stroke-width="2" stroke-linejoin="round"/><circle cx="41" cy="32" r="4" fill="#fff"/></svg>',
        status=200,
        mimetype="image/svg+xml"
    )


@app.route("/sw.js")
def pwa_service_worker():
    worker = """
const CACHE = "void-space-v2";
self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(["/", "/manifest.json", "/icon.svg"])));
  self.skipWaiting();
});
self.addEventListener("activate", event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE).map(key => caches.delete(key)))));
  self.clients.claim();
});
self.addEventListener("fetch", event => {
  if (event.request.method !== "GET" || new URL(event.request.url).origin !== self.location.origin) return;
  event.respondWith(caches.match(event.request).then(cached => cached || fetch(event.request).then(response => {
    if (response.ok && (event.request.mode === "navigate" || /manifest\\.json|icon\\.svg/.test(new URL(event.request.url).pathname))) {
      const copy = response.clone(); caches.open(CACHE).then(cache => cache.put(event.request, copy));
    }
    return response;
  }).catch(() => caches.match("/"))));
});
"""
    return Response(worker, mimetype="application/javascript", headers={"Cache-Control": "no-cache"})


@app.route("/tree-menu")
def tree_menu():
    return send_file(os.path.join(os.path.dirname(__file__), "tree-menu.html"), mimetype="text/html")


@app.route("/health")
def health():
    return "VOID SPACE ONLINE"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port, debug=False)
