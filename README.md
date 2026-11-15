# VOID SPACE 🚀

A browser-based space-survival arcade game. Pilot your ship, survive enemy waves, defeat multi-phase bosses, unlock ships and weapons, and explore new sectors.

**Play:** https://shreebalaji767.github.io/SPACE/

Free to play. No ads, paid items, accounts, backend, or database. Progress is saved locally in your browser.

## Static site deployment

VOID SPACE is published as a static GitHub Pages site. The playable site uses HTML, CSS, and browser JavaScript; it does not require Flask, Python, a server process, or a database.

- Entry page: `index.html`
- Game modules and styles: `static/`
- PWA manifest and offline worker: `manifest.json`, `sw.js`
- Additional tree menu: `tree-menu.html`
- GitHub Pages deployment: `.github/workflows/pages.yml`

After pushing to `main`, the Pages workflow uploads the repository as a static artifact and deploys it. In repository Settings → Pages, select **GitHub Actions** as the deployment source if it is not already selected.

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

Progress remains in browser `localStorage`, not on a server:

- `voidSpaceProfile` — main profile, ships, weapons, skills, achievements, and records.
- `voidSpaceExpansion` — Command Deck expansion.
- `voidSpaceUniverse` — Galactic Command progress.
- `voidSpaceRelics` — Rift Relic Forge progress.

Use the in-game backup/export options to keep a copy of your saves. Data stays in the same browser and site origin; it does not automatically sync between devices. Clearing browser site data can erase it.

## Run locally

Open `index.html` in a local static web server for full PWA behavior. For example, with Python installed:

```bash
python -m http.server 8000
```

Then visit http://localhost:8000/ when serving this folder directly. The game itself does not use Python as an application backend.

## Development checks

GitHub Actions runs static-site structure checks, Python legacy smoke tests, and JavaScript syntax checks. Responsive browser tests are retained for phone, tablet, desktop, and landscape layouts; automated tests do not replace testing on physical devices.

## Project structure

```text
SPACE/
├── index.html
├── manifest.json
├── sw.js
├── icon.svg
├── tree-menu.html
├── static/
├── tests/
└── .github/workflows/
```

## Notes

- The landing page uses prerecorded gameplay footage; gameplay begins when **Play Now** is selected.
- Three.js is an optional, version-pinned graphics library. If it cannot load or WebGL is unavailable, the game falls back to 2D.
- Existing `app.py` and its tests are retained as legacy development references; GitHub Pages serves `index.html` and does not execute them.
