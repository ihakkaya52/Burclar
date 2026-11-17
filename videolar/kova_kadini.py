import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Kova", cins="k", maddeler=[
    (["Kalabalığın içinde bile kendi dünyasındadır.", "Bedeni orada, aklı başka bir gezegende."],
     "yorunge", dict(merkez="😶", gezen="🪐", etiket=("aklı: başka gezegen 🛸", "aklı"))),
    (["Sakın kıskançlık yapma.", "Özgürlüğüne dokunan herkese mesafe koyar."],
     "gosterge", dict(etiket="MESAFE 📏", soru="kimle konuşuyorsun? 🤨", tetik="mesafe", c0=ALTIN, c1=BLUE)),
    (["Sıradan iltifatlar işe yaramaz.", "Ona “güzelsin” deme, “farklısın” de."],
     "mesaj", dict(msgs=[("r", "çok güzelsin", "güzelsin"), ("r", "çok farklısın ✨", "farklısın"), ("l", "😍", ("farklısın", .6))], etiket=("görüldü", "deme"))),
    (["Bir davaya inandıysa, herkesi karşısına alır."],
     "isik", dict(emo="✊", megafon="📣", tetik="herkesi")),
    (["Önce en yakın arkadaşı ol.", "Kalbinin kapısı, o zaman kendiliğinden açılır."],
     "kapi", dict(ac=True, tetik="kendiliğinden", etiket="açıldı ❤", kilit=False)),
])

video, bosluk = hazirla(SPEC)
