// Primero intenta la versión nueva de internet; si no hay conexión, usa la guardada.
const CACHE='juegos-v3';
const FILES=['./','index.html','canciones.html','minecraft.html','pokemon.html','harrypotter.html','cole.html','calculo.html','total.html','cifrasyletras.html','ruleta.html','palabras.txt','manifest.json','icon-192.png','icon-512.png','apple-touch-icon.png'];
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).catch(()=>{}))});
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  e.respondWith(fetch(e.request).then(r=>{const cp=r.clone();caches.open(CACHE).then(c=>c.put(e.request,cp)).catch(()=>{});return r}).catch(()=>caches.match(e.request,{ignoreSearch:true}).then(r=>r||caches.match('./'))));
});
