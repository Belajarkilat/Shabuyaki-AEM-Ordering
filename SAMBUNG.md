# Sambung kerja: Sheet Order AEM

Nota ini ditulis 11 September 2026. Baca ini dahulu sebelum sentuh apa-apa.

## Keadaan semasa

| Perkara | Nilai |
|---|---|
| Pautan rasmi | https://belajarkilat.github.io/Shabuyaki-AEM-Ordering/ |
| PIN dapur | 2240 |
| Repo | https://github.com/Belajarkilat/Shabuyaki-AEM-Ordering (awam) |
| Repo tempatan | `C:\Users\Hasfi\shabuyaki-aem-ordering` |
| Folder kerja | `C:\Users\Hasfi\OneDrive\Desktop\Shabuyaki AEM` |
| Pangkalan data | Supabase, projek sama dengan Pijol AI Brain |

Sheet sudah siap dan diuji. Team dapur boleh guna hari ini. Tiada akaun
diperlukan, cuma pautan dan PIN.

## Cara pasang atas telefon

Buka pautan, taip PIN sekali sahaja, kemudian menu tiga titik dalam Chrome
atau Edge, pilih **Add to Home Screen**. Ikon mangkuk muncul atas skrin dan
sheet buka penuh skrin tanpa bar alamat. Ia jalan tanpa internet selepas
kali pertama.

## Tiga perkara yang Hasfi belum putuskan

Semuanya berkaitan data, bukan kod. Sheet berjalan elok tanpa
menyelesaikannya, tapi ia patut diselesaikan sebelum team bergantung penuh.

1. **Empat pasang item kembar dalam Frozen Pack.** Lamb Meat Ball, Beef Meat
   Ball, Teokbboki Mala Ball dan Fried Fish Tofu masing-masing wujud dua
   baris dengan nama beza sedikit, harga sama, dan kadar guna dipecah dua.
   Jumlah food cost tetap betul, tetapi team nampak barang sama dua kali dan
   pembundaran karton berlaku dua kali. Untuk melihatnya: pil hari **Sabtu**,
   kad **Central Kitchen**, skrol ke bahagian **Frozen Pack**.
2. **Dua item tiada saiz pek.** BONELESS Chicken datang dalam pek 2KG dan
   White Sesame Seed dalam pek 300 gram, tetapi kedua-duanya diorder dalam KG
   tanpa medan `k`, jadi order tidak dibundarkan ke pek.
3. **Satu salah taip.** `Black Pepper Powder -PKT/5OOGM` guna huruf O, bukan
   angka sifar.

## Matlamat asal: fail APK

PWA ini langkah satu dan tiada kerja terbuang. Untuk APK sebenar ada dua
jalan. Hantar pautan ke PWABuilder dan dapat APK bertandatangan tanpa pasang
apa-apa, atau pasang JDK 17 dan Android command line tools atas mesin ini
kemudian bungkus dengan Capacitor, lebih kurang sejam. Mesin ini **tiada**
Java, Android SDK atau adb setakat 11 September 2026.

## Hal pautan yang tergantung

Hasfi minta buang perkataan `belajarkilat` daripada pautan. Pautan GitHub
Pages sentiasa bermula dengan nama akaun, jadi ia hanya boleh dibuang dengan
organisasi GitHub baharu atau domain sendiri.

- Organisasi `shabuyaki-aem` tidak pernah tercipta walaupun disangka siap.
  Nama itu masih kosong.
- Laman Netlify `shabuyaki-aem` sudah dicipta dan keluaran sampai, tetapi ia
  pulangkan 401. Netlify kini mengunci setiap laman baharu akaun percuma di
  belakang skrin log masuk. Ia perlu satu suis dalam UI Netlify di **Site
  configuration**, bahagian **Access & security**. Empat cubaan melalui API
  tidak berkesan. Laman itu masih wujud tetapi tidak digunakan.

## Cara terbit selepas mengubah sheet

Sumber tunggal ialah `AEM Sheet Order.html` dalam folder kerja OneDrive.
Folder `pwa/` ialah keluaran yang dibina, jangan edit terus.

```
python terbit.py
git add -A && git commit -m "kemas kini"
git push origin main
git subtree push --prefix pwa origin gh-pages
```

`git push` biasa akan tergantung tanpa token. Remote dalam repo ini sudah
membawa token, jadi ia berjalan. Kalau perlu pasang semula, baca
`GITHUB_TOKEN` daripada `C:\Users\Hasfi\.claude\.env` dan guna URL bentuk
`https://x-access-token:TOKEN@github.com/...`.

## Cara tukar PIN

Jalankan SQL ini pada projek Supabase. Halaman tidak perlu diterbitkan
semula, tetapi setiap peranti akan diminta PIN baharu.

```sql
update public.sheet_aem_rahsia set v = '1234' where k = 'pin';
```

## Perangkap mesin

- Heredoc Bash pada mesin ini **memakan backslash**. Skrip Python tampalan
  mesti ditulis dengan alat Write, bukan heredoc. Guna `chr(92)` kalau perlu
  backslash literal dalam kod yang dijana.
- Akaun `Belajarkilat` ialah akaun **pengguna**, bukan organisasi. Cipta repo
  melalui `POST /user/repos`. `POST /orgs/Belajarkilat/repos` pulangkan
  `Not Found`.
- Token GitHub tiada skop `workflow`, jadi jangan tambah fail dalam
  `.github/workflows`.

## Pepijat yang sudah dibetulkan, jangan pulangkan

Stok hilang setiap kali muat semula pada mana-mana hari selain Jumaat.
`muatSetempat()` membaca stok menggunakan kitaran lalai 4 sebelum pemilih
hari menetapkan hari sebenar, dan tidak pernah baca semula. Pembetulannya
ialah `muatStokSetempat()` berasingan yang dipanggil selepas pemilih hari,
dan `lukisKitaran()` memanggil `tukarKitaran()` apabila ia terpaksa menukar
kitaran. Diuji tujuh hari dengan jam palsu. Salinan lama ada di
`AEM Sheet Order.html.bak` dalam folder kerja OneDrive.
