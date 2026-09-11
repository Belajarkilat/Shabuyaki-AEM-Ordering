# -*- coding: utf-8 -*-
"""Terbitkan Sheet Order AEM.

Sumber tunggal ialah fail HTML dalam folder kerja OneDrive. Skrip ini
menyalinnya ke repo, membina folder pwa/, kemudian kau tolak sendiri:

    python terbit.py
    git add -A && git commit -m "kemas kini"
    git push origin main
    git subtree push --prefix pwa origin gh-pages

Fail inventori Excel dan PDF jualan TIDAK disalin ke sini. Ia kekal dalam
OneDrive sahaja kerana repo ini awam.
"""
import io, os, shutil, subprocess, sys

REPO = os.path.dirname(os.path.abspath(__file__))
KERJA = "C:/Users/Hasfi/OneDrive/Desktop/Shabuyaki AEM"
SUMBER = os.path.join(KERJA, "AEM Sheet Order.html")

if not os.path.exists(SUMBER):
    sys.exit("tidak jumpa sumber: " + SUMBER)

shutil.copy2(SUMBER, os.path.join(REPO, "AEM Sheet Order.html"))
os.makedirs(os.path.join(REPO, "data"), exist_ok=True)
shutil.copy2(os.path.join(KERJA, "data", "sheet-data.json"),
             os.path.join(REPO, "data", "sheet-data.json"))
print("sumber disalin")

subprocess.check_call([sys.executable, os.path.join(REPO, "bina.py")])

for f in sorted(os.listdir(os.path.join(REPO, "pwa"))):
    print("  pwa/" + f)
