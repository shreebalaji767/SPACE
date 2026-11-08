# VOID SPACE 🚀

A browser-based space-survival arcade game. Pilot your ship, survive enemy waves, defeat multi-phase bosses, unlock ships and weapons, and explore new sectors.

<p align="center">
  <a href="https://void-space-3d.onrender.com/"><strong>▶ PLAY VOID SPACE — LIVE</strong></a>
</p>

Free to play. No ads, paid items, accounts, or database. Progress is saved locally in your browser.

## Features

- **Combat:** escalating enemy waves, multi-phase bosses, weak points, destructible asteroids, power-ups, and cinematic effects.
- **7 game modes:** Survival, Endless, Boss Rush, Time Attack, Hardcore, Daily Seed, and Campaign.
- **Ships and weapons:** four ships, six weapon families, permanent upgrades, skill trees, ultimates, and weapon evolutions.
- **Progression:** credits, XP, achievements, daily contracts, reward crates, and personal records.
- **Expansions:** VOID Command Deck, Galactic Command, faction missions, wingmen, station upgrades, and the Rift Relic Forge.
- **3D landing scene:** optional Three.js visuals with a 2D fallback.
- **Responsive controls:** keyboard, mouse, and mobile touch controls.
- **PWA:** installable app and offline game-shell caching after the first successful online load.

## Controls

| Action | Control |
| --- | --- |
| Rotate | A / D or ← / → |
| Thrust / reverse | W / ↑ / S / ↓ |
| Fire | Space or X; left mouse button |
| Bomb | B |
| Change weapon | Q |
| Ship ultimate | E |
| Pause / resume | P or Esc |
| Aim | Move mouse over the game |
| Touch | On-screen mobile controls |

## Saves and privacy

Progress is stored in browser `localStorage`, not on a server:

- `voidSpaceProfile` — main profile, ships, weapons, skills, achievements, and records.
- `voidSpaceExpansion` — Command Deck expansion.
- `voidSpaceUniverse` — Galactic Command progress.
- `voidSpaceRelics` — Rift Relic Forge progress.

Use the in-game backup/export options to keep a copy of your saves. Data stays in the same browser and site origin; it does not automatically sync between devices. Clearing browser site data can erase it.

## Run locally

Requires Python 3.10+ (Python 3.11+ recommended).

```bash
git clone https://github.com/shreebalaji767/SPACE.git
cd SPACE
python -m venv .venv
```

Activate the environment:

```powershell
# Windows
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install and run:

```bash
pip install -r requirements.txt
python app.py
```

Open [http://localhost:10000](http://localhost:10000). The server uses the `PORT` environment variable when provided (default: `10000`).

## Deployment

The live version is hosted at [void-space-3d.onrender.com](https://void-space-3d.onrender.com/).

- Build command: `pip install -r requirements.txt`
- Start command: `python app.py`
- Health check: `/health`
- HTTPS is required for service-worker and PWA installation support.
- No database or secret environment variables are required.

## Development checks

GitHub Actions runs Python compilation, JavaScript syntax checks, Flask smoke tests, and responsive browser regression tests. Browser tests cover phone, tablet, desktop, and landscape layouts. Automated tests do not replace testing on physical devices.

## Project structure

```text
SPACE/
├── app.py
├── requirements.txt
├── static/
├── tests/
├── .github/workflows/
└── README.md
```

## Notes

- The landing page uses prerecorded gameplay footage; gameplay begins when **Play Now** is selected.
- Three.js is an optional, version-pinned graphics library. If it cannot load or WebGL is unavailable, the game falls back to 2D.
- The game is free and does not use ads, paid gameplay services, or a player database.
