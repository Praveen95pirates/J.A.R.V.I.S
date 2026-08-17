self.addEventListener('install', (e) => {
  console.log('[SW] Install');
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  console.log('[SW] Activate');
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
