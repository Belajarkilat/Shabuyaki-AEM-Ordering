/* Service worker Sheet Order AEM. Cap bina: fc66137d
   Panggilan Supabase TIDAK PERNAH disimpan cache: ia bukan GET, atau ia
   pergi ke asal lain yang tidak disenaraikan di bawah.                     */
const CACHE = "aem-fc66137d";
const SHELL = ["./", "./index.html", "./manifest.webmanifest",
               "./ikon-192.png", "./ikon-512.png", "./ikon-maskable-512.png", "./ikon-180.png"];
const FON = ["https://fonts.googleapis.com", "https://fonts.gstatic.com"];

self.addEventListener("install", e=>{
  e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()));
});
self.addEventListener("activate", e=>{
  e.waitUntil(caches.keys()
    .then(k=>Promise.all(k.filter(x=>x!==CACHE).map(x=>caches.delete(x))))
    .then(()=>self.clients.claim()));
});
self.addEventListener("fetch", e=>{
  if(e.request.method !== "GET") return;
  const u = new URL(e.request.url);
  const boleh = (u.origin === location.origin) || FON.indexOf(u.origin) >= 0;
  if(!boleh) return;
  e.respondWith(caches.match(e.request).then(simpanan=>{
    const rangkaian = fetch(e.request).then(r=>{
      if(r && (r.ok || r.type === "opaque")){
        const salinan = r.clone();
        caches.open(CACHE).then(c=>c.put(e.request, salinan));
      }
      return r;
    }).catch(()=>simpanan);
    return simpanan || rangkaian;
  }));
});
