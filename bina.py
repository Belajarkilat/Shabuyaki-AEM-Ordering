# -*- coding: utf-8 -*-
"""Bina folder pwa/ daripada satu fail sumber AEM Sheet Order.html."""
import io, os, zlib, struct, hashlib

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
ASAL = _os.path.join(_HERE, "AEM Sheet Order.html")
KELUAR = _os.path.join(_HERE, "pwa")

# ---------- penulis PNG ringkas ----------
def png(path, w, h, piksel):
    baris = bytearray()
    for y in range(h):
        baris.append(0)
        for x in range(w):
            baris += bytes(piksel(x, y))
    def bahagian(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))
    keluar = b"\x89PNG\r\n\x1a\n"
    keluar += bahagian(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
    keluar += bahagian(b"IDAT", zlib.compress(bytes(baris), 9))
    keluar += bahagian(b"IEND", b"")
    io.open(path, "wb").write(keluar)

LATAR = (31, 74, 107)      # --accent
TINTA = (245, 242, 236)    # --paper

def buat_ikon(path, saiz, skala=1.0, bulat=True):
    """Mangkuk shabu: separuh bawah bulatan, dengan satu jalur di atasnya."""
    s = float(saiz)
    jejari_sudut = s * 0.22
    pusat_x = s / 2.0
    # kotak selamat untuk ikon maskable
    lebar = s * skala
    tepi = (s - lebar) / 2.0
    mangkuk_r = lebar * 0.30
    mangkuk_y = tepi + lebar * 0.56
    jalur_y = tepi + lebar * 0.50
    jalur_t = lebar * 0.055
    jalur_x = lebar * 0.36

    def dalam_sudut(x, y):
        if not bulat:
            return True
        for cx, cy in ((jejari_sudut, jejari_sudut), (s - jejari_sudut, jejari_sudut),
                       (jejari_sudut, s - jejari_sudut), (s - jejari_sudut, s - jejari_sudut)):
            if ((x < jejari_sudut and cx < jejari_sudut) or (x > s - jejari_sudut and cx > s - jejari_sudut)) and \
               ((y < jejari_sudut and cy < jejari_sudut) or (y > s - jejari_sudut and cy > s - jejari_sudut)):
                if (x - cx) ** 2 + (y - cy) ** 2 > jejari_sudut ** 2:
                    return False
        return True

    def piksel(x, y):
        px, py = x + 0.5, y + 0.5
        if not dalam_sudut(px, py):
            return (0, 0, 0, 0)
        # mangkuk
        if py >= mangkuk_y and (px - pusat_x) ** 2 + (py - mangkuk_y) ** 2 <= mangkuk_r ** 2:
            return TINTA + (255,)
        # jalur sup
        if abs(py - jalur_y) <= jalur_t / 2.0 and abs(px - pusat_x) <= jalur_x:
            return TINTA + (255,)
        return LATAR + (255,)

    png(path, saiz, saiz, piksel)

# ---------- bina ----------
os.makedirs(KELUAR, exist_ok=True)
sumber = io.open(ASAL, encoding="utf-8").read()

potong = sumber.index("</style>") + len("</style>")
kepala, badan = sumber[:potong], sumber[potong:]

cap = hashlib.sha1(sumber.encode("utf-8")).hexdigest()[:8]

halaman = (
    "<!doctype html>\n"
    '<html lang="ms">\n'
    "<head>\n"
    '<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="theme-color" content="#141619" media="(prefers-color-scheme: dark)">\n'
    '<meta name="theme-color" content="#F5F2EC" media="(prefers-color-scheme: light)">\n'
    '<meta name="description" content="Alat order dapur Shabuyaki Aeon Maluri">\n'
    '<meta name="robots" content="noindex, nofollow">\n'
    '<link rel="manifest" href="manifest.webmanifest">\n'
    '<link rel="apple-touch-icon" href="ikon-180.png">\n'
    '<meta name="apple-mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-title" content="Order AEM">\n'
    + kepala + "\n</head>\n<body>\n" + badan.strip() + "\n"
    '<script>\n'
    'if("serviceWorker" in navigator){\n'
    '  addEventListener("load", ()=>navigator.serviceWorker.register("sw.js").catch(()=>{}));\n'
    '}\n'
    "</script>\n"
    "</body>\n</html>\n"
)
io.open(os.path.join(KELUAR, "index.html"), "w", encoding="utf-8").write(halaman)

manifest = """{
  "name": "Sheet Order AEM",
  "short_name": "Order AEM",
  "description": "Alat order dapur Shabuyaki Aeon Maluri",
  "lang": "ms",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "background_color": "#141619",
  "theme_color": "#141619",
  "icons": [
    { "src": "ikon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any" },
    { "src": "ikon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any" },
    { "src": "ikon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
"""
io.open(os.path.join(KELUAR, "manifest.webmanifest"), "w", encoding="utf-8").write(manifest)

sw = """/* Service worker Sheet Order AEM. Cap bina: %s
   Panggilan Supabase TIDAK PERNAH disimpan cache: ia bukan GET, atau ia
   pergi ke asal lain yang tidak disenaraikan di bawah.                     */
const CACHE = "aem-%s";
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
""" % (cap, cap)
io.open(os.path.join(KELUAR, "sw.js"), "w", encoding="utf-8").write(sw)

buat_ikon(os.path.join(KELUAR, "ikon-192.png"), 192)
buat_ikon(os.path.join(KELUAR, "ikon-512.png"), 512)
buat_ikon(os.path.join(KELUAR, "ikon-180.png"), 180)
buat_ikon(os.path.join(KELUAR, "ikon-maskable-512.png"), 512, skala=0.78, bulat=False)
io.open(os.path.join(KELUAR, ".nojekyll"), "w", encoding="utf-8").write("")

for f in sorted(os.listdir(KELUAR)):
    print("%-26s %8d bait" % (f, os.path.getsize(os.path.join(KELUAR, f))))
print("cap bina", cap)
