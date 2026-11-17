import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Terazi", cins="k", maddeler=[
    (["Uyumsuz hiçbir şeye dayanamaz.", "Evi, kıyafeti, telefon kılıfı bile takımdır."],
     "gozler", dict(merkez="💅", cevre="✨", tetik=1)),
    (["“Fark etmez” derse, sakın inanma.", "Fark eder."],
     "mesaj", dict(msgs=[("r", "nereye gidelim?", 0), ("l", "fark etmez 😊", (0, .6))], damga=("FARK EDER ⚠", 1))),
    (["İki seçenek arasında kalırsa…", "ikisini de alır."],
     "salter", dict(sol="SİYAH", sag="BEYAZ", gecis=[(0, 1), ((0, .45), 0), ((0, .9), 1), ((0, 1.35), 0)], son=("İKİSİ DE 🛍", 1))),
    (["Yalnız kalmayı sevmez.", "Kahveye bile mutlaka biriyle gider."],
     "yorunge", dict(merkez="☕", gezen="👭", etiket=("tek başına? asla.", 1), n=2)),
    (["Herkese ikinci bir şans verir.", "Ama üçüncüsü yoktur."],
     "liste", dict(satirlar=[("1. şans ✅", 0), ("2. şans ✅", "ikinci")], son=("3. şans ❌", "yoktur", RED))),
])

video, bosluk = hazirla(SPEC)
