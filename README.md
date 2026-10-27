# VOID SPACE 🚀

A free, browser-based neon cyberpunk space-survival arcade game. Pilot a ship through escalating enemy waves, fight bosses, collect power-ups, build a run with upgrades, earn credits, and unlock ships.

**No paid items, no ads, no external game assets, and no database required.** Player progression is stored locally in the browser.

## Features

- **Arcade combat:** fast fighters, tanks, ranged sniper enemies, enemy projectiles, boss encounters, and escalating waves.
- **Bomb shockwave:** spend energy to damage nearby enemies, clear nearby enemy bullets, and trigger a short cinematic slow-motion effect.
- **Build variety:** weapon damage, rapid fire, engine, hull, critical/multi-shot, salvage magnet, phase-piercing shots, hit-blocking shield charges, stronger bombs, gradual hull regeneration, and side-cannon wingman drones.
- **Progression:** gain XP and pilot levels, earn credits, track best score and deepest wave, and unlock four ships.
- **Ship hangar:**
  - **Neon Striker** — balanced starter ship.
  - **Void Phantom** — faster, lighter interceptor.
  - **Nova Titan** — heavy hull and strong damage.
  - **Prism Spectre** — high-damage prototype.
- **Power-ups:** health, energy, rapid fire, bomb refill, weapon upgrade, temporary shield, and credits.
- **Neon presentation:** glowing cyberpunk colors, a deep-space background, particles, shockwaves, and boss health display.
- **Responsive controls:** keyboard, mouse, touch, and on-screen desktop controls.
- **Installable PWA:** manifest, SVG app icon, and a service worker that caches the game shell for offline reopening after the first successful load.
- **Performance options:** full/lite visual effects, sound toggle, and screen-shake toggle.
- **Accessibility basics:** focus-friendly buttons, reduced-motion CSS support, and mobile safe-area handling.

## Save system (no database)

VOID SPACE saves player progression directly in the browser using `localStorage` under the `voidSpaceProfile` key. It stores credits, pilot level and XP, unlocked/selected ships, best score, deepest wave, and sound/visual preferences. The profile is saved as progression changes and autosaved when the page is hidden or closed.

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
| Pause / resume | **P** or **Esc** |
| Aim | Move the mouse over the game |
| Touch | Use the on-screen touch controls |

On desktop, the on-screen control dock is available while a run is active. On mobile, use the touch controls displayed by the game.

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
- **Start command:** `python app.py`
- **Health check:** `/health`
- **Recommended runtime:** Python 3.11+
- Serve over **HTTPS** in production for installable PWA/service-worker support.
- No database or secret environment variables are needed.

For a WSGI deployment, the Flask application object is `app` in `app.py`; a platform-supported server such as Gunicorn can run it with `gunicorn app:app` if Gunicorn is added to the deployment dependencies.

## Save data and privacy

The game stores credits, pilot level/XP, unlocked and selected ships, best score/wave, and sound/visual settings in browser `localStorage` under `voidSpaceProfile`.

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
