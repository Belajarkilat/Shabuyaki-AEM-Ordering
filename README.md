# Sheet Order AEM

Alat order dapur harian untuk Shabuyaki Aeon Maluri. Team dapur pilih supplier,
masukkan stok sedia ada, dan sheet mengira kuantiti order serta nilainya.

Langsung di **https://belajarkilat.github.io/Shabuyaki-AEM-Ordering/**

## Cara ia mengira

Setiap item disimpan sebagai kadar guna per RM1,000 jualan bersih, bukan
kuantiti tetap. Kuantiti = kadar x jangkaan jualan tempoh x (1 + buffer),
tolak stok sedia ada. Liputan dikira dari hari barang sampai sehingga
hantaran supplier itu yang berikutnya, mengikut bahagian jualan harian 13
minggu. Hari order milik supplier, buffer milik kategori, dan bajet dikunci
pada harga asas Jun hingga September 2026 supaya lonjakan harga muncul
sebagai melebihi bajet, bukan menaikkan bajet sendiri.

Item yang datang dalam karton dibundarkan ke karton terdekat, tanpa minimum
satu karton.

## Perkongsian dan PIN

Halaman bercakap terus dengan Supabase menggunakan kunci anon awam. Kunci itu
sendiri tidak membuka apa-apa. Setiap permintaan mesti membawa header
`x-sheet-pin` yang sepadan dengan PIN dalam jadual rahsia yang peranan anon
tidak boleh baca, dan dasar RLS di server yang menguatkuasakannya.

Semua tulisan turut disimpan dalam `localStorage`, jadi sheet tetap boleh
diguna dalam peti sejuk tanpa isyarat. Apa yang ditaip ketika putus talian
duduk dalam beratur tempatan dan dihantar naik sendiri apabila talian pulih.

Untuk menukar PIN, jalankan SQL ini pada projek Supabase. Halaman tidak perlu
diterbitkan semula, tetapi setiap peranti akan diminta PIN baharu.

```sql
update public.sheet_aem_rahsia set v = '1234' where k = 'pin';
```

## Bina dan terbit

`AEM Sheet Order.html` ialah satu-satunya sumber. Folder `pwa/` ialah keluaran
yang dibina, jangan edit terus.

```
python terbit.py
git add -A && git commit -m "kemas kini"
git push origin main
git subtree push --prefix pwa origin gh-pages
```

Fail inventori Excel dan PDF jualan sengaja tidak disimpan dalam repo ini
kerana ia awam. Fail itu kekal dalam folder kerja OneDrive.
