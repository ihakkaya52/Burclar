import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Yengeç", cins="e", maddeler=[
    (["Dışı sert görünür, içi pamuk gibidir.", "Kabuğunu herkese açmaz."],
     "donusum", dict(a=("🦀", (200, 70, 50), None), b=("🧸", (255, 150, 170), "❤"), tetik="içi")),
    (["Annesi hakkında tek kelime etme.", "O konu, kırmızı çizgisidir."],
     "yazi", dict(text="bence annen biraz fazla", damga="KIRMIZI ÇİZGİ 🚫", tetik=1)),
    (["Küstüğünü söylemez.", "Sessizleşir…", "ve senin anlamanı bekler."],
     "mesaj", dict(msgs=[("r", "bir şey mi oldu? 🥺", 0), ("l", "yok.", 1)], yaziyor=2)),
    (["Eski anıları asla unutmaz.", "3 yıl önce ne giydiğini bile hatırlar."],
     "arsiv", dict(baslik="📁 ANILAR", satirlar=["ilk buluşma: mavi kazak", "tarih: 3 yıl önce", "saat: 19.30, yağmurlu"], damga="EZBERE", tetik=1, once="💭")),
    (["Sevdiğine yuva olur.", "Onun yanında, kendini hep evde hissedersin."],
     "yuksel", dict(arka="🏠", tetik=1)),
])

video, bosluk = hazirla(SPEC)
