// Service Worker for My Fitness App
const CACHE_NAME = 'fitness-app-v1';
const urlsToCache = [
    '/',
    '/static/style.css',
    '/static/app.js'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});
