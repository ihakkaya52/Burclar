import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Oğlak", cins="e", maddeler=[
    (["İşi her şeyden önce gelir.", "Tatilde bile maillerine bakar."],
     "donusum", dict(a=("🏖", (60, 170, 220), None), b=("💻", (90, 90, 140), None), tetik=1)),
    (["Duygularını belli etmez.", "“Fena değil” dediyse, bayılmış demektir."],
     "gosterge", dict(etiket="İÇİNDEKİ HEYECAN", cevap="fena değil.", tetik=1, c0=ALTIN, c1=PINK)),
    (["Boş vaat vermez.", "Söz verdiyse, çoktan takvimine yazmıştır."],
     "arsiv", dict(baslik="📁 TAKVİM", satirlar=["cumartesi 19.30", "konu: sana verdiği söz", "hatırlatıcı: 3 adet"], damga="KESİN", tetik=1, once="🤝")),
    (["Para harcamadan önce 3 kez düşünür.", "Ama sevdiğine kıyamaz."],
     "salter", dict(sol="ALMA", sag="AL", gecis=[(0, 0), ((0, .6), 1), ((0, 1.1), 0), (1, 1)], son=("sana alınır 🎁", (1, .4)))),
    (["Yavaş güvenir, geç bağlanır.", "Ama bir kez bağlandıysa, ömürlüktür."],
     "kapi", dict(ac=True, tetik="ömürlüktür", etiket="ÖMÜRLÜK ❤", ic="❤")),
])

video, bosluk = hazirla(SPEC)
