import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Balık", cins="k", maddeler=[
    (["Sezgileri çok güçlüdür.", "Yalan söylediğini, sen daha söylemeden hisseder."],
     "yazi", dict(text="dün gece erkenden uyu", damga="HİSSETTİ 🔮", tetik="hisseder")),
    (["Her şeye ağlayabilir.", "Reklama bile."],
     "donusum", dict(a=("📺", (90, 90, 140), None), b=("😭", (60, 80, 200), "yagmur"), tetik=1)),
    (["Sınır çizmekte zorlanır.", "Herkesin derdini dinler, kendi derdini saklar."],
     "gosterge", dict(etiket="BAŞKALARININ DERDİ", soru="sana bir şey anlatacağım…", cevap="ben iyiyim 🙂", tetik=1, c0=ALTIN, c1=MOR)),
    (["Kırıldığında kavga etmez.", "Sessizce uzaklaşır…", "ve geri dönmesi çok zordur."],
     "kapi", dict(ac=False, tetik=1, etiket="sessizce.")),
    (["Seni olduğun gibi sever.", "Kusurlarınla, geçmişinle, her halinle."],
     "yuksel", dict(arka="❤", tetik=1)),
])

video, bosluk = hazirla(SPEC)
