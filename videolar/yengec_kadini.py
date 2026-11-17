import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Yengeç", cins="k", maddeler=[
    (["Ruh hali ay gibidir.", "Sabah güler, akşam sebepsiz yere dolar."],
     "donusum", dict(a=("🌞", (255, 190, 60), None), b=("🌧", (80, 100, 200), "yagmur"), tetik="akşam")),
    (["Söylediğin bir sözü yıllarca unutmaz.", "Kelimelerini seçerek konuş."],
     "arsiv", dict(baslik="📁 SÖZLER", satirlar=["“abartıyorsun”", "tarih: 2 yıl önce", "durum: hâlâ aklında"], damga="KAYITTA", tetik=(0, .9), once="🗣")),
    (["Sevdiklerini doyurmadan rahat etmez.", "“Tokum” desen de tabağın dolar."],
     "saganak", dict(emo="🥟", buyuk="🍲", etiket=("“tokum” geçersiz 😅", 1))),
    (["Kırıldığında kabuğuna çekilir.", "Kapıyı çalman yetmez, sabırla beklemen gerekir."],
     "kapi", dict(ac=True, tetik="gerekir", etiket="sabır 🔑", ic="🦀")),
    (["Bir kez ailesi olduysan, senin için dünyayı karşısına alır."],
     "yorunge", dict(merkez="❤", gezen="🦀", davetsiz="😈", tetik="dünyayı")),
])

video, bosluk = hazirla(SPEC)
