/* VOID SPACE — optional Three.js cinematic menu scene. No gameplay dependency. */
(function () {
  "use strict";

  const MODULE_URL = "https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js";
  const STORAGE_KEY = "voidSpace3DEnabled";
  const reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const lowPower = !!(navigator.deviceMemory && navigator.deviceMemory < 4) ||
    !!(navigator.connection && navigator.connection.saveData);
  const recordMode = new URLSearchParams(location.search).get("record") === "1";
  let enabled = true;
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    enabled = saved === null ? true : saved === "true";
  } catch (_) {}

  const toggle = document.getElementById("threeSceneToggle");
  const settingValue = document.getElementById("threeSceneValue");
  let renderer, scene, camera, frame = 0, running = false, disposed = false;
  let planet, planetHalo, ship, ring, stars, asteroids = [], clock;
  let threeAvailable = false;

  function updateToggle() {
    if (toggle) {
      toggle.textContent = enabled ? "ON" : "OFF";
      toggle.setAttribute("aria-pressed", String(enabled));
    }
    if (settingValue) settingValue.textContent = enabled ? "ENABLED" : "DISABLED";
  }

  function visibleScreen() {
    return !recordMode && !document.hidden && enabled &&
      !!document.querySelector(".screen.active");
  }

  function makeMaterial(THREE, color, emissive, roughness) {
    return new THREE.MeshStandardMaterial({
      color: color,
      emissive: emissive || 0x000000,
      emissiveIntensity: emissive ? 0.42 : 0,
      roughness: roughness === undefined ? 0.72 : roughness,
      metalness: 0.12
    });
  }

  function buildScene(THREE) {
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x070b1b, 0.012);
    camera = new THREE.PerspectiveCamera(42, 1, 0.1, 120);
    camera.position.set(0, 0, 19);

    const ambient = new THREE.AmbientLight(0x9ba9d8, 1.15);
    scene.add(ambient);
    const keyLight = new THREE.PointLight(0x91d9ff, 95, 48, 2);
    keyLight.position.set(-7, 8, 8);
    scene.add(keyLight);
    const rimLight = new THREE.PointLight(0xb69aff, 70, 40, 2);
    rimLight.position.set(8, -5, 2);
    scene.add(rimLight);

    const planetGroup = new THREE.Group();
    planetGroup.position.set(-5.2, 1.45, -5.4);
    scene.add(planetGroup);
    planet = new THREE.Mesh(
      new THREE.SphereGeometry(2.65, 48, 36),
      new THREE.MeshStandardMaterial({
        color: 0x465d9a, roughness: 0.92, metalness: 0.04,
        emissive: 0x111b43, emissiveIntensity: 0.35
      })
    );
    planetGroup.add(planet);

    const land = new THREE.Group();
    const landMat = new THREE.MeshStandardMaterial({
      color: 0x7389bd, roughness: 1, transparent: true, opacity: 0.56
    });
    for (let i = 0; i < 9; i++) {
      const patch = new THREE.Mesh(
        new THREE.IcosahedronGeometry(0.28 + (i % 3) * 0.12, 1),
        landMat
      );
      const a = i * 2.399;
      patch.position.set(Math.cos(a) * 2.1, Math.sin(a * 1.7) * 1.55, Math.sin(a) * 1.9);
      patch.scale.set(1.5, 0.35, 0.85);
      land.add(patch);
    }
    planet.add(land);

    ring = new THREE.Mesh(
      new THREE.TorusGeometry(3.55, 0.055, 8, 120),
      new THREE.MeshStandardMaterial({
        color: 0x9ab9ff, emissive: 0x6379d6, emissiveIntensity: 0.8,
        metalness: 0.62, roughness: 0.35, transparent: true, opacity: 0.7
      })
    );
    ring.rotation.set(1.18, 0.22, -0.35);
    planetGroup.add(ring);

    planetHalo = new THREE.Mesh(
      new THREE.SphereGeometry(2.82, 32, 24),
      new THREE.MeshBasicMaterial({
        color: 0x799cff, transparent: true, opacity: 0.075,
        side: THREE.BackSide, blending: THREE.AdditiveBlending
      })
    );
    planetGroup.add(planetHalo);

    const moon = new THREE.Mesh(
      new THREE.SphereGeometry(0.48, 24, 18),
      makeMaterial(THREE, 0x9eabc9, 0x242c52, 0.86)
    );
    moon.position.set(3.8, -1.8, 0.4);
    planetGroup.add(moon);
    planetGroup.userData.moon = moon;

    ship = new THREE.Group();
    ship.position.set(3.4, -2.15, 1.2);
    scene.add(ship);
    const hullMat = new THREE.MeshStandardMaterial({
      color: 0xbac8f4, metalness: 0.72, roughness: 0.27,
      emissive: 0x303d82, emissiveIntensity: 0.55
    });
    const wingMat = makeMaterial(THREE, 0x6878b8, 0x202d68, 0.34);
    const engineMat = new THREE.MeshBasicMaterial({
      color: 0x8fe7ff, transparent: true, opacity: 0.9,
      blending: THREE.AdditiveBlending
    });
    const body = new THREE.Mesh(new THREE.ConeGeometry(0.56, 2.15, 6), hullMat);
    body.rotation.x = Math.PI / 2;
    ship.add(body);
    const cockpit = new THREE.Mesh(
      new THREE.SphereGeometry(0.27, 20, 14),
      new THREE.MeshStandardMaterial({
        color: 0x9fe8ff, emissive: 0x3eafff, emissiveIntensity: 1.4,
        metalness: 0.55, roughness: 0.16
      })
    );
    cockpit.position.set(0, 0.08, 0.18);
    cockpit.scale.set(0.8, 0.75, 1.45);
    ship.add(cockpit);
    [-1, 1].forEach(function (side) {
      const wing = new THREE.Mesh(new THREE.BoxGeometry(1.55, 0.12, 0.72), wingMat);
      wing.position.set(side * 0.72, -0.2, -0.1);
      wing.rotation.z = side * -0.2;
      ship.add(wing);
      const engine = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.2, 0.85, 12), engineMat);
      engine.rotation.x = Math.PI / 2;
      engine.position.set(side * 0.63, -0.23, -0.92);
      ship.add(engine);
    });
    const shipLight = new THREE.PointLight(0x69cfff, 18, 6, 2);
    shipLight.position.set(0, 0, -1.1);
    ship.add(shipLight);

    const starPositions = new Float32Array(1500 * 3);
    for (let i = 0; i < 1500; i++) {
      starPositions[i * 3] = (Math.random() - 0.5) * 65;
      starPositions[i * 3 + 1] = (Math.random() - 0.5) * 38;
      starPositions[i * 3 + 2] = (Math.random() - 0.5) * 48 - 8;
    }
    const starGeometry = new THREE.BufferGeometry();
    starGeometry.setAttribute("position", new THREE.BufferAttribute(starPositions, 3));
    stars = new THREE.Points(starGeometry, new THREE.PointsMaterial({
      color: 0xcbdcff, size: 0.075, transparent: true, opacity: 0.76,
      sizeAttenuation: true
    }));
    scene.add(stars);

    const asteroidMat = makeMaterial(THREE, 0x66718e, 0x151c34, 0.95);
    for (let i = 0; i < 18; i++) {
      const asteroid = new THREE.Mesh(
        new THREE.IcosahedronGeometry(0.2 + Math.random() * 0.48, 1),
        asteroidMat
      );
      asteroid.position.set(
        (Math.random() - 0.5) * 28,
        (Math.random() - 0.5) * 17,
        -3 - Math.random() * 22
      );
      asteroid.rotation.set(Math.random() * 3, Math.random() * 3, Math.random() * 3);
      asteroid.userData.spin = {
        x: (Math.random() - 0.5) * 0.24,
        y: (Math.random() - 0.5) * 0.28,
        drift: 0.12 + Math.random() * 0.24
      };
      scene.add(asteroid);
      asteroids.push(asteroid);
    }

    const orbit = new THREE.Mesh(
      new THREE.TorusGeometry(5.2, 0.012, 4, 150),
      new THREE.MeshBasicMaterial({ color: 0x7385bd, transparent: true, opacity: 0.28 })
    );
    orbit.position.set(4.4, -2.2, -7);
    orbit.rotation.set(1.1, 0.4, 0.1);
    scene.add(orbit);
  }

  function resize() {
    if (!renderer || !camera) return;
    const width = Math.max(1, window.innerWidth);
    const height = Math.max(1, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, lowPower ? 1 : (width < 700 ? 1.25 : 1.6)));
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.position.z = width < 520 ? 23 : 19;
    camera.updateProjectionMatrix();
    if (planet && ship) {
      planet.parent.position.set(width < 520 ? -2.1 : -5.2, width < 520 ? 3.1 : 1.45, -5.4);
      shipBaseY = width < 520 ? -3.0 : -2.15;
      ship.position.set(width < 520 ? 1.5 : 3.4, shipBaseY, 1.2);
      ship.scale.setScalar(width < 520 ? 0.78 : 1);
    }
    drawStatic();
  }

  function drawStatic() {
    if (renderer && scene && camera && !disposed) renderer.render(scene, camera);
  }

  function shouldAnimate() {
    return !reducedMotion && !lowPower;
  }

  function animate() {
    if (!running || disposed) return;
    frame = requestAnimationFrame(animate);
    if (!visibleScreen()) {
      stop();
      return;
    }
    const elapsed = clock.getElapsedTime();
    if (planet) {
      planet.rotation.y = elapsed * 0.035;
      if (planet.parent && planet.parent.userData.moon) {
        const moon = planet.parent.userData.moon;
        moon.position.set(Math.cos(elapsed * 0.18) * 3.9, Math.sin(elapsed * 0.18) * 1.5, Math.sin(elapsed * 0.18) * 2.2);
      }
    }
    if (ship) {
      ship.position.y = shipBaseY + Math.sin(elapsed * 0.8) * 0.22;
      ship.rotation.z = Math.sin(elapsed * 0.22) * 0.055;
      ship.rotation.y = Math.sin(elapsed * 0.16) * 0.09;
    }
    if (ring) ring.rotation.z = -0.35 + Math.sin(elapsed * 0.08) * 0.025;
    if (stars) stars.rotation.z = elapsed * 0.002;
    asteroids.forEach(function (asteroid) {
      const spin = asteroid.userData.spin;
      asteroid.rotation.x += spin.x * 0.012;
      asteroid.rotation.y += spin.y * 0.012;
      asteroid.position.x += Math.sin(elapsed * 0.12 + asteroid.id) * 0.0008 * spin.drift;
    });
    renderer.render(scene, camera);
  }

  function start() {
    if (running || !renderer || !visibleScreen()) return;
    renderer.domElement.style.display = "block";
    running = true;
    clock.start();
    if (shouldAnimate()) {
      frame = requestAnimationFrame(animate);
    } else {
      drawStatic();
    }
  }

  function stop() {
    if (!running && renderer) renderer.domElement.style.display = "none";
    if (!running) return;
    running = false;
    if (renderer) renderer.domElement.style.display = "none";
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
  }

  function syncVisibility() {
    updateToggle();
    if (visibleScreen()) start();
    else stop();
    if (renderer && !shouldAnimate() && visibleScreen()) drawStatic();
  }

  async function init() {
    if (recordMode || !document.body) return;
    try {
      const THREE = await import(MODULE_URL);
      if (disposed || !document.body) return;
      renderer = new THREE.WebGLRenderer({
        alpha: true,
        antialias: !lowPower,
        powerPreference: "low-power",
        stencil: false,
        depth: true
      });
      renderer.setClearColor(0x000000, 0);
      renderer.domElement.id = "voidThreeScene";
      renderer.domElement.setAttribute("aria-hidden", "true");
      renderer.domElement.setAttribute("role", "presentation");
      renderer.domElement.style.cssText = "position:fixed;inset:0;z-index:1;width:100%;height:100%;display:block;pointer-events:none;opacity:.94;";
      document.body.insertBefore(renderer.domElement, document.body.firstChild);
      buildScene(THREE);
      clock = new THREE.Clock();
      threeAvailable = true;
      document.body.classList.add("void-three-ready");
      resize();
      syncVisibility();
      if (shouldAnimate() && visibleScreen()) start();
    } catch (error) {
      threeAvailable = false;
      stop();
      if (renderer) {
        renderer.dispose();
        renderer.domElement.remove();
        renderer = null;
      }
      document.body.classList.add("void-three-unavailable");
      const status = document.getElementById("threeSceneValue");
      if (status) status.textContent = "2D FALLBACK";
      if (toggle) {
        toggle.textContent = "UNAVAILABLE";
        toggle.disabled = true;
        toggle.setAttribute("aria-label", "Three-dimensional scene unavailable; standard graphics remain active");
      }
      console.info("VOID SPACE 3D scene unavailable; continuing with standard graphics.", error);
    }
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      if (!threeAvailable) return;
      enabled = !enabled;
      try { localStorage.setItem(STORAGE_KEY, String(enabled)); } catch (_) {}
      syncVisibility();
    });
  }
  document.addEventListener("visibilitychange", syncVisibility);
  window.addEventListener("resize", resize, { passive: true });
  window.addEventListener("orientationchange", function () { requestAnimationFrame(resize); }, { passive: true });
  const observer = new MutationObserver(syncVisibility);
  document.querySelectorAll(".screen").forEach(function (screen) {
    observer.observe(screen, { attributes: true, attributeFilter: ["class"] });
  });
  updateToggle();
  init();
  window.addEventListener("pagehide", function () {
    disposed = true;
    stop();
    observer.disconnect();
    if (renderer) renderer.dispose();
  }, { once: true });
})();
