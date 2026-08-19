/* Word Family Rush — offline service worker.
   The game is one self-contained file, so caching index.html (plus the icons
   and manifest) is enough to run with no network at all once installed. */
const CACHE = 'wfr-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './apple-touch-icon.png'
];

// Precache — resilient: a single missing file won't abort the install.
self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await Promise.all(ASSETS.map(url => cache.add(url).catch(() => {})));
    self.skipWaiting();
  })());
});

// Drop old caches on activate.
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)));
    self.clients.claim();
  })());
});

// Cache-first, fall back to network, then to the cached game for navigations.
self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  event.respondWith((async () => {
    const cached = await caches.match(req);
    if (cached) return cached;
    try {
      const res = await fetch(req);
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
      return res;
    } catch (e) {
      const fallback = await caches.match('./index.html');
      if (fallback) return fallback;
      throw e;
    }
  })());
});
