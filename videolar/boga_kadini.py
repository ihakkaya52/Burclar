import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Boğa", cins="k", maddeler=[
    (["Kaliteden anlar.", "Ucuz bir hediyeyle gönlünü alamazsın."],
     "damga", dict(emo="🎁", text="İADE ❌", tetik="alamazsın")),
    (["Planı son dakika değiştirme.", "Bunu günlerce unutmaz."],
     "arsiv", dict(baslik="📁 ARŞİV", satirlar=["cumartesi: akşam yemeği", "iptal: son dakika", "sebep: “işim çıktı”"], damga="UNUTULMADI", tetik=1, once="⏰")),
    (["Onu acele ettirme.", "Kendi hızında gider…", "ve yine de herkesten önce varır."],
     "yol", dict(giden="🐂", hedef="🏁", var="önce", etiket="1. 🏆")),
    (["İnadı meşhurdur.", "“Hayır” dediyse, o konu kapanmıştır."],
     "kapi", dict(ac=False, tetik="kapanmıştır", etiket="konu kapandı.")),
    (["Sana bir kez güvendiyse, ömür boyu yanında durur."],
     "yuksel", dict(arka="🐂", tetik="ömür")),
])

video, bosluk = hazirla(SPEC)
