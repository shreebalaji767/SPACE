const CACHE = "void-space-pages-v1";
const BASE = self.registration.scope;
const CORE = [
  BASE,
  new URL("manifest.json", BASE).href,
  new URL("icon.svg", BASE).href,
  new URL("tree-menu.html", BASE).href,
  new URL("static/void-expansion.js", BASE).href,
  new URL("static/void-universe.js", BASE).href,
  new URL("static/void-responsive.css", BASE).href,
  new URL("static/void-3d.js", BASE).href,
  new URL("static/void-relics.js", BASE).href,
  new URL("static/void-space-gameplay.webm", BASE).href
];
const THREE = [
  "https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js",
  "https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.core.js"
];
self.addEventListener("install", event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await cache.addAll(CORE);
    await Promise.all(THREE.map(url => cache.add(url).catch(() => null)));
    await self.skipWaiting();
  })());
});
self.addEventListener("activate", event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(key => key !== CACHE).map(key => caches.delete(key)));
    await self.clients.claim();
  })());
});
self.addEventListener("fetch", event => {
  if (event.request.method !== "GET") return;
  const url = new URL(event.request.url);
  const local = url.origin === self.location.origin && url.href.startsWith(BASE);
  const three = THREE.includes(url.href);
  if (!local && !three) return;
  event.respondWith((async () => {
    const cached = await caches.match(event.request);
    if (cached) return cached;
    try {
      const response = await fetch(event.request);
      if (response.ok) {
        const copy = response.clone();
        caches.open(CACHE).then(cache => cache.put(event.request, copy));
      }
      return response;
    } catch (error) {
      if (local && event.request.mode === "navigate") {
        return (await caches.match(BASE)) || Response.error();
      }
      throw error;
    }
  })());
});
