import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Koç", cins="k", maddeler=[
    (["Kararını bir saniyede verir.", "Sen düşünürken, o çoktan yola çıkmıştır."],
     "kacis", dict(emo="🏃", tetik="çoktan", etiket="çıktı bile 💨")),
    (["Ona “yapamazsın” deme.", "Sırf sana inat, iki katını yapar."],
     "gosterge", dict(etiket="İNAT 💪", soru="sen bunu yapamazsın", cevap="izle. 😏", tetik=1, hedef=200)),
    (["Sıkıcı bir hayata dayanamaz.", "Macera yoksa, kendi çıkarır."],
     "donusum", dict(a=("😴", (90, 90, 120), None), b=("🎢", ATES, "konfeti"), tetik=1)),
    (["Kızınca her şeyi söyler…", "ama kin tutmaz.", "Ertesi gün unutmuştur."],
     "sonra", dict(emo="🤬", sure="1 GÜN SONRA… ⏰", balon="kahve içelim mi? ☕", tetik=2)),
    (["Sevdiğini herkese karşı savunur.", "Arkandan konuşan, karşısında onu bulur."],
     "yuksel", dict(arka="🐏", tetik=1)),
])

video, bosluk = hazirla(SPEC)
