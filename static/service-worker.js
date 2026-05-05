const CACHE_NAME = 'micromatrix-v2';
const ASSETS_TO_CACHE = [
  '/',
  '/home',
  '/services',
  '/contact',
  '/about',
  '/static/images/logo.png',
  '/static/images/hero_bg.png',
  '/static/images/auth_bg.png',
  '/static/images/services_bg.png',
  '/static/manifest.json'
];

// Install: cache all core assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[SW] Caching core assets');
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

// Activate: clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: Network First for HTML, Cache First for assets
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  // Network First Strategy for Navigation (HTML)
  if (event.request.mode === 'navigate' || event.request.destination === 'document') {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          return response;
        })
        .catch(() => caches.match(event.request).then(cached => cached || caches.match('/home')))
    );
    return;
  }

  // Cache First Strategy for everything else (Images, CSS, JS)
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        if (response && response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => null);
    })
  );
});
