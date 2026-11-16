const CACHE_NAME = "multilanguage-docs-v1";

const STATIC_FILES = [
    "/",
    "/static/css/documentation.css",
    "/static/js/documentation.js",
    "/static/pwa/manifest.json",
    "/static/pwa/icons/icon-192.png",
    "/static/pwa/icons/icon-512.png"
];

// Install Service Worker
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(STATIC_FILES);
        })
    );

    self.skipWaiting();
});

// Activate Service Worker
self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );

    self.clients.claim();
});

// Fetch Resources
self.addEventListener("fetch", (event) => {

    if (event.request.method !== "GET") {
        return;
    }

    event.respondWith(
        fetch(event.request)
            .then((response) => {

                if (response && response.status === 200) {
                    const responseClone = response.clone();

                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseClone);
                    });
                }

                return response;
            })
            .catch(() => {
                return caches.match(event.request).then((cachedResponse) => {
                    return cachedResponse || caches.match("/");
                });
            })
    );
});