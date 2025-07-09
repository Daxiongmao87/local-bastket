/**
 * Service Worker for Local Basket PWA
 * Provides offline functionality and caching
 */

const CACHE_NAME = 'local-basket-v1';
const OFFLINE_URL = '/offline';

// Files to cache immediately
const PRECACHE_FILES = [
  '/',
  '/static/css/main.css',
  '/static/js/app.js',
  '/static/js/utils.js',
  '/static/js/geolocation.js',
  '/static/js/map.js',
  '/static/js/forms.js',
  '/static/manifest.json',
  '/offline'
];

// Files to cache on first visit
const CACHE_FIRST_FILES = [
  '/search',
  '/map',
  '/static/css/',
  '/static/js/',
  '/static/images/',
  '/static/icons/'
];

// Network first files (always try network first)
const NETWORK_FIRST_FILES = [
  '/api/',
  '/shop/',
  '/product/',
  '/review'
];

/**
 * Install event - cache essential files
 */
self.addEventListener('install', event => {
  console.log('[SW] Install event');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[SW] Precaching files');
        return cache.addAll(PRECACHE_FILES);
      })
      .then(() => {
        console.log('[SW] Skip waiting');
        self.skipWaiting();
      })
      .catch(error => {
        console.error('[SW] Precache failed:', error);
      })
  );
});

/**
 * Activate event - clean up old caches
 */
self.addEventListener('activate', event => {
  console.log('[SW] Activate event');
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== CACHE_NAME) {
              console.log('[SW] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('[SW] Claiming clients');
        return self.clients.claim();
      })
  );
});

/**
 * Fetch event - handle requests with caching strategies
 */
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Only handle GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Skip chrome-extension requests
  if (url.protocol === 'chrome-extension:') {
    return;
  }
  
  // Determine caching strategy
  if (shouldUseNetworkFirst(url.pathname)) {
    event.respondWith(networkFirst(request));
  } else if (shouldUseCacheFirst(url.pathname)) {
    event.respondWith(cacheFirst(request));
  } else {
    event.respondWith(staleWhileRevalidate(request));
  }
});

/**
 * Check if URL should use network-first strategy
 */
function shouldUseNetworkFirst(pathname) {
  return NETWORK_FIRST_FILES.some(pattern => pathname.includes(pattern));
}

/**
 * Check if URL should use cache-first strategy
 */
function shouldUseCacheFirst(pathname) {
  return CACHE_FIRST_FILES.some(pattern => pathname.includes(pattern));
}

/**
 * Network-first strategy
 * Try network first, fall back to cache
 */
async function networkFirst(request) {
  try {
    const networkResponse = await fetch(request);
    
    // If successful, cache the response
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[SW] Network failed, trying cache:', error);
    
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // If it's a navigation request, show offline page
    if (request.mode === 'navigate') {
      return caches.match(OFFLINE_URL);
    }
    
    // Otherwise, return a basic offline response
    return new Response('Offline', {
      status: 503,
      statusText: 'Service Unavailable'
    });
  }
}

/**
 * Cache-first strategy
 * Try cache first, fall back to network
 */
async function cacheFirst(request) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    return cachedResponse;
  }
  
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[SW] Cache miss and network failed:', error);
    
    if (request.mode === 'navigate') {
      return caches.match(OFFLINE_URL);
    }
    
    return new Response('Offline', {
      status: 503,
      statusText: 'Service Unavailable'
    });
  }
}

/**
 * Stale-while-revalidate strategy
 * Return cached version immediately, update cache in background
 */
async function staleWhileRevalidate(request) {
  const cachedResponse = await caches.match(request);
  
  const networkPromise = fetch(request).then(networkResponse => {
    if (networkResponse.ok) {
      const cache = caches.open(CACHE_NAME);
      cache.then(c => c.put(request, networkResponse.clone()));
    }
    return networkResponse;
  }).catch(() => {
    // Network failed, but we might have cache
    if (cachedResponse) {
      return cachedResponse;
    }
    
    if (request.mode === 'navigate') {
      return caches.match(OFFLINE_URL);
    }
    
    return new Response('Offline', {
      status: 503,
      statusText: 'Service Unavailable'
    });
  });
  
  return cachedResponse || networkPromise;
}

/**
 * Background sync event
 */
self.addEventListener('sync', event => {
  console.log('[SW] Background sync:', event.tag);
  
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

/**
 * Perform background sync
 */
async function doBackgroundSync() {
  console.log('[SW] Performing background sync');
  
  // This would sync any pending data when connection is restored
  try {
    // Example: sync pending reviews, shop updates, etc.
    const pendingData = await getPendingData();
    
    if (pendingData.length > 0) {
      for (const data of pendingData) {
        await syncData(data);
      }
      
      // Clear pending data after successful sync
      await clearPendingData();
    }
  } catch (error) {
    console.error('[SW] Background sync failed:', error);
  }
}

/**
 * Get pending data from IndexedDB
 */
async function getPendingData() {
  // This would integrate with IndexedDB to get pending data
  // For now, return empty array
  return [];
}

/**
 * Sync data to server
 */
async function syncData(data) {
  // This would send data to server
  console.log('[SW] Syncing data:', data);
}

/**
 * Clear pending data
 */
async function clearPendingData() {
  // This would clear pending data from IndexedDB
  console.log('[SW] Clearing pending data');
}

/**
 * Push event for notifications
 */
self.addEventListener('push', event => {
  console.log('[SW] Push event:', event);
  
  if (event.data) {
    const data = event.data.json();
    
    const options = {
      body: data.body,
      icon: '/static/icons/icon-192x192.png',
      badge: '/static/icons/badge-72x72.png',
      vibrate: [100, 50, 100],
      data: data.data,
      actions: data.actions || []
    };
    
    event.waitUntil(
      self.registration.showNotification(data.title, options)
    );
  }
});

/**
 * Notification click event
 */
self.addEventListener('notificationclick', event => {
  console.log('[SW] Notification click:', event);
  
  event.notification.close();
  
  if (event.action === 'open_shop') {
    const shopUrl = event.notification.data.shopUrl;
    event.waitUntil(
      clients.openWindow(shopUrl)
    );
  } else {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

/**
 * Message event for communication with main thread
 */
self.addEventListener('message', event => {
  console.log('[SW] Message event:', event);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({
      type: 'VERSION',
      version: CACHE_NAME
    });
  }
});

/**
 * Periodic background sync (if supported)
 */
self.addEventListener('periodicsync', event => {
  console.log('[SW] Periodic sync:', event.tag);
  
  if (event.tag === 'shop-updates') {
    event.waitUntil(syncShopUpdates());
  }
});

/**
 * Sync shop updates
 */
async function syncShopUpdates() {
  console.log('[SW] Syncing shop updates');
  
  try {
    const response = await fetch('/api/shops/updates');
    if (response.ok) {
      const updates = await response.json();
      
      // Cache updated shop data
      const cache = await caches.open(CACHE_NAME);
      updates.forEach(update => {
        cache.put(`/shop/${update.id}`, new Response(JSON.stringify(update)));
      });
    }
  } catch (error) {
    console.error('[SW] Shop updates sync failed:', error);
  }
}

console.log('[SW] Service worker loaded');