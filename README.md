# VOID SPACE 🚀

A free, browser-based neon cyberpunk space-survival arcade game with a premium-style landing page and a looping **prerecorded gameplay video**. Pilot a ship through escalating enemy waves, fight multi-phase bosses, open reward crates, chain kill combos, complete daily contracts, earn credits, and unlock ships.

**No paid items, no ads, no external game assets, and no database required.** Player progression is stored locally in the browser.

## Features

- **Recorded cinematic trailer:** the landing page plays `/static/void-space-gameplay.webm` on loop. Regular visitors do not start the game simulation, autopilot, or gameplay animation on the landing page; only the isolated `?record=1` capture workflow runs the simulation to produce the footage. That capture starts in Boss Rush, stages the boss and six supporting enemies inside the camera for an immediate combined encounter, and displays both boss and hostile counts in the trailer HUD. The recording workflow checks that the HUD reports a boss plus at least one regular hostile before it accepts and publishes the video. **Play Now** starts real gameplay only after a deliberate click.
- **Arcade combat:** fast fighters, tanks, ranged snipers, enemy projectiles, escalating waves, and three named boss variants.
- **Multi-phase bosses + weak points:** Dreadnought, Void Wraith, and Nova Colossus change attacks at 66% and 32% health. A moving, intermittently exposed weak point deals bonus damage when hit, with impact slow motion, flashes, and a live phase-aware boss bar.
- **Six weapon families + permanent armory:** Pulse is the starter weapon; spend earned credits to unlock homing missiles, plasma shotgun, phase railgun, chain lightning, and singularity in the Ship Hangar. Choose a saved starting weapon, then weapon pickups cycle only through weapons you have unlocked and level them up. Rare reward crates can also unlock a weapon.
- **Cinematic effects:** slow-motion bombs, colored impact particles, boss phase flashes, glowing debris, and a lightweight-effects setting for slower devices.
- **Reward crates:** enemies can drop glowing, diamond-framed crates containing free credits, hull repair, energy, weapon damage, bomb upgrades, or a rare permanent weapon or ship unlock. No paid crates or purchases.
- **Kill-chain combo rewards:** consecutive eliminations within a four-second window build a combo; every five kills grants bonus credits, a neon burst, and a brief slow-motion impact. Boss defeats trigger a longer cinematic finish.
- **Daily contracts:** three UTC-date-based objectives — eliminate 10 hostiles, reach wave 5, and defeat a boss — award free credits and XP once per day. Progress and claims persist in localStorage.
- **Interactive environments:** destructible asteroids drift through each run, damage the ship on contact, and can drop credits when destroyed. Campaign routes tint the hazard fields.
- **Seven game modes:** Survival, faster-scaling Endless, Boss Rush, three-minute Time Attack, tougher Hardcore, **Daily Seed** — a reproducible challenge whose procedural enemy/hazard sequence is seeded by the UTC date — and the multi-sector Campaign.
- **Three-sector campaign:** choose Derelict Belt, Ion Storm, or Singularity Edge; clear waves and defeat the sector boss to earn a completion bonus.
- **Ship ultimates:** press **E** or use the on-screen ULTIMATE control. The Striker detonates a nova, Phantom phases through danger, Titan triggers an overdrive blast, and Spectre releases a screen-wide prism nova.
- **Build variety:** weapon damage, rapid fire, engine, hull, critical/multi-shot, salvage magnet, phase-piercing shots, shield charges, stronger bombs, hull regeneration, and side-cannon drones.
- **Weapon evolution:** combine run upgrades to evolve builds into Plasma Swarm, Starstorm, Phase Lance, Nova Singularity, or Aegis Engine.
- **Permanent ship skill trees:** spend earned credits on five-rank Hull, Thrusters, Reactor, and Weapon Calibration skills for each ship.
- **Achievements:** unlock persistent badges for kills, boss victories, high scores, weapon evolutions, ship collection, and campaign clears.
- **Save backup and restore:** export the local profile to JSON and import it later, useful for manual backups or moving between browsers.
- **Progression:** gain XP and pilot levels, earn credits, track best score and deepest wave, and unlock four ships.
- **Ship hangar:**
  - **Neon Striker** — balanced starter ship.
  - **Void Phantom** — faster, lighter interceptor.
  - **Nova Titan** — heavy hull and strong damage.
  - **Prism Spectre** — high-damage prototype.
- **Power-ups:** health, energy, rapid fire, bomb refill, weapon upgrade, temporary shield, and credits.
- **Neon presentation:** glowing cyberpunk colors, a deep-space background, particles, shockwaves, and boss health display.
- **Responsive controls:** keyboard, mouse, touch, and on-screen desktop controls. Touch FIRE supports held autofire; adaptive canvas pixel ratio and capped background stars reduce rendering cost on smaller or lower-powered devices.
- **Installable PWA:** manifest, SVG app icon, and a service worker that caches the game shell for offline reopening after the first successful load.
- **Performance options:** full/lite visual effects, sound toggle, and screen-shake toggle.
- **Accessibility basics:** focus-friendly buttons, reduced-motion CSS support, and mobile safe-area handling.

## Save system (no database)

VOID SPACE saves player progression directly in the browser using `localStorage` under the `voidSpaceProfile` key. It stores credits, pilot level and XP, unlocked/selected ships and weapons, per-ship permanent skill-tree ranks, best score, deepest wave, and sound/visual preferences. The profile is saved as progression changes and autosaved when the page is hidden or closed. The existing `voidSpaceProfile` key is preserved, and older profiles migrate forward when loaded. The versioned profile includes achievements, lifetime kills, boss defeats, campaign completions, per-mode records, ship and weapon unlocks/selections, ship skill ranks, daily contract progress/claims, and preferences. Existing profile keys are retained and older saves load with safe starter defaults for the new weapon fields. Daily contract progress resets at UTC midnight; claimed rewards cannot be claimed again for the same UTC date.

- **No database or server-side player account is used.**
- Saves belong to that browser and site origin; they do not automatically sync between devices or browsers.
- Clearing site data, private/incognito sessions, or browser storage restrictions can remove or prevent saves. Keep browser storage enabled.
- A save failure is reported in the browser console rather than being silently treated as successful.

## Play

Open the deployed game in a modern browser. On compatible browsers, choose **INSTALL VOID SPACE** to install it as an app.

### Controls

| Action | Keyboard / mouse |
| --- | --- |
| Rotate | **A / D** or **← / →** |
| Thrust | **W** or **↑** |
| Brake / reverse | **S** or **↓** |
| Fire | **Space** or **X**; left mouse button |
| Bomb | **B** |
| Cycle weapon | **Q** |
| Ship ultimate | **E** or the on-screen ULTIMATE button |
| Daily challenge | Select **DAILY SEED** from Game Modes; the seed changes at UTC midnight |
| Pause / resume | **P** or **Esc** |
| Aim | Move the mouse over the game |
| Touch | Use the on-screen touch controls |

On desktop, the on-screen control dock is available while a run is active. On mobile, use the touch controls displayed by the game. The Ship Hangar's Weapon Armory lets you unlock and equip permanent weapons. Weapon pickups cycle through your unlocked arsenal and increase its level. Keyboard players can use **Q** to cycle weapons during a run.

## Run locally

Requires **Python 3.10+** (Python 3.11+ recommended).

```bash
git clone https://github.com/shreebalaji767/SPACE.git
cd SPACE
python -m venv .venv
```

Activate the virtual environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install dependencies and start the server:

```bash
pip install -r requirements.txt
python app.py
```

Then visit [http://localhost:10000](http://localhost:10000).

The server listens on `0.0.0.0` and uses the `PORT` environment variable when provided (default `10000`). A simple health endpoint is available at `/health`.

## Deploy

This is a small Flask application with a single main game file.

- **Build/install command:** `pip install -r requirements.txt`
- **Gameplay recording workflow:** `.github/workflows/record-gameplay.yml` captures the dedicated `/?record=1` route and updates the prerecorded trailer asset. Normal landing-page visits never use this capture mode.
- **Start command:** `python app.py`
- **Health check:** `/health`
- **Recommended runtime:** Python 3.11+
- Serve over **HTTPS** in production for installable PWA/service-worker support.
- No database or secret environment variables are needed.

For a WSGI deployment, the Flask application object is `app` in `app.py`; a platform-supported server such as Gunicorn can run it with `gunicorn app:app` if Gunicorn is added to the deployment dependencies.


## Expansion systems

The **VOID COMMAND DECK** adds an optional expansion layer without replacing the original game engine or the existing `voidSpaceProfile` save:

- **Research lab:** permanently upgrade Squadron Link (wingman support), Quantum Reactor (starting energy), Salvage Array (bonus run credits), and Titanium Plating (starting hull) using banked credits.
- **Operations:** launch Mothership Siege, Invasion Protocol, One-Life Gauntlet, Endless Boss Hunt, Sector Exploration, and Convoy Escort. These reuse the existing combat engine and apply operation-specific rules; Convoy Escort is a 60-second protection objective.
- **New hostiles:** bomber, warden, and swarm variants begin appearing in later waves.
- **Expanded fleet:** unlock the Aegis Sentinel defensive escort and Rift Runner high-speed flanker in the existing Ship Hangar.
- **Faction standing:** Aurora Syndicate, Outer Rim Nomads, and Eclipse Collective reputation is earned through runs.
- **Enemy codex:** encountered hostile types are recorded locally.
- **Full save vault:** export or restore the original game profile and expansion data together. Imports validate the backup format and basic values before restoring.

Expansion data is stored separately in `localStorage` under `voidSpaceExpansion`. The original `voidSpaceProfile` key and its existing migration path are preserved. All progression remains local to the browser; no account, database, paid service, ad network, or external gameplay API is introduced.


## Galactic Command expansion

The **Galactic Command** hub adds a second, local-only layer to the existing game:

- **Galaxy map:** select the Derelict Belt, Ion Storm, or Singularity Edge as the active operation sector.
- **Fleet roster:** recruit up to three support fighters, choose Intercept / Guard / Support orders, and receive companion fire during active runs.
- **Space station:** upgrade Hull Foundry, Reactor Core, Armory Matrix, and Ion Thrusters. Upgrades are applied once after the original game resets the ship for a new run.
- **Galactic War:** choose Aurora Syndicate, Outer Rim Nomads, or Eclipse Collective; completed missions and victories build faction influence and sector control.
- **Mission board:** five repeatable mission types track kills, waves, survival time, and boss victories, paying local credits and materials.
- **Run chronicle:** stores the latest 12 runs locally and lets you replay the last mode/sector setup. It does not claim to be a video replay.
- **Materials:** alloy, crystal, and data are earned through mission and victory rewards and used by station upgrades.

Universe data is stored separately under `voidSpaceUniverse`. It does not replace the existing `voidSpaceProfile` or the first expansion's `voidSpaceExpansion` data.

## Responsive layout hardening

The additional responsive stylesheet uses dynamic viewport sizing, safe-area insets, content-aware panels, auto-fitting card grids, compact-phone and short-landscape layouts, touch-sized controls, keyboard focus indicators, and reduced-motion handling. Touch controls are hidden on menus and pause screens and shown only during active touch gameplay. Canvas dimensions follow visual viewport and orientation changes. The new universe UI follows the same responsive rules. Playwright browser regression checks exercise 320px phones through 1920px desktops, including landscape, command-hub tabs, game controls, pause behavior, and horizontal overflow. The service worker pre-caches the expansion scripts and stylesheet for offline use after the first successful load.

## Automated checks

GitHub Actions runs a Python compile check and Flask smoke tests on pushes and pull requests. The tests verify the game route, expansion asset, PWA endpoints, and health endpoint. Browser gameplay and touch-device testing should still be performed after major gameplay changes.

## Save data and privacy

The game stores credits, pilot level/XP, unlocked and selected ships, per-ship skill-tree ranks, achievements, lifetime combat statistics, campaign progress, mode records, best score/wave, daily contract progress/claims, and sound/visual settings in browser `localStorage` under `voidSpaceProfile`. The Save Backup / Restore screen exports and imports this profile as JSON.

- Data is local to that browser and origin; it does not automatically sync across devices.
- Clearing site data or using a different browser/profile can reset progression.
- There is no account system, analytics service, ad network, or remote leaderboard in this project.

## PWA / offline notes

The app serves `/manifest.json`, `/icon.svg`, and `/sw.js` directly from Flask. The service worker caches the game shell after a successful online load. Browser policies vary, and service workers generally require HTTPS (or localhost during development). If an older cached version appears after an update, close/reopen the installed app or clear the site's cached data.

## Project layout

```text
SPACE/
├── app.py           # Flask server + embedded HTML/CSS/JavaScript game
├── requirements.txt # Python dependencies
├── static/          # Recorded gameplay video and PWA assets
├── .github/workflows/ # Automated gameplay recording workflow
└── README.md        # Project documentation
```

## Troubleshooting

- **Server will not start:** confirm your virtual environment is active and run `pip install -r requirements.txt`.
- **Port already in use:** set a different `PORT` environment variable before starting.
- **Install button missing:** use a supported browser over HTTPS; some browsers do not expose the install prompt.
- **Offline mode not available:** first load the game online and allow the service worker to install.
- **Progress disappeared:** check that you are using the same browser profile and have not cleared this site's storage.

## Contributing

Bug reports and improvements are welcome. Test keyboard, mouse, and touch input; verify gameplay after changes; and keep the project dependency-light and playable without paid assets.

## License

No license file is currently included. Add a license before redistributing the project if you want to specify reuse permissions.

## Three.js cinematic 3D scene

VOID SPACE now has an optional, real-time Three.js scene behind its landing page and menus:

- A rotating ringed planet with a small orbiting moon and soft atmospheric glow.
- A detailed 3D player ship with animated engine lights and gentle hover motion.
- A deep star field, drifting 3D asteroids, orbital paths, and layered lighting.
- Responsive camera framing and capped pixel ratios for smaller screens.
- A **THREE.JS 3D SCENE** setting to turn the effect on or off. The preference is stored separately in localStorage as `voidSpace3DEnabled`.
- The 3D renderer is hidden during active combat so it cannot cover or slow the original 2D gameplay canvas. The existing combat engine, controls, and save keys are unchanged.
- If WebGL or the Three.js module is unavailable, VOID SPACE continues using its original 2D graphics. Reduced-motion and low-power devices receive a still 3D scene rather than a continuously animated one.

Three.js is loaded as a free, version-pinned ES module from jsDelivr (`three@0.180.0`). It is a graphics library, not an AI service or gameplay API. The service worker attempts to cache the module and its core file for offline use after a successful connection; if the CDN is unavailable on the first load, the game falls back cleanly and the normal game remains playable. No account, paid asset, subscription, ad network, or database is added.
