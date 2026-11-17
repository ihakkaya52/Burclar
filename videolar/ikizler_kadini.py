import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="İkizler", cins="k", maddeler=[
    (["Bir günde 3 farklı ruh haline girer.", "Hangisine denk geleceğini bilemezsin."],
     "slot", dict(emojiler="😄😢😡🥰😴🤪", tetik="bilemezsin", etiket="bugün: sürpriz 🎲")),
    (["Konuşmayı çok sever.", "“Kısa bir şey söyleyeceğim” derse, kahveni al, otur."],
     "sayac", dict(hedef=14, birim="dakikalık sesli mesaj", emo="🎙", tetik=1, son=("kahveni al ☕", "kahveni"))),
    (["Merakı hiç bitmez.", "Telefonunda 20 sekme açıktır, hepsi de ayrı bir konu."],
     "gozler", dict(merkez="📱", cevre="🔍", tetik=1)),
    (["Kararsızdır.", "Menüye yarım saat bakar, sonunda senin tabağından yer."],
     "salter", dict(sol="PİZZA", sag="MAKARNA", gecis=[(0, 1), ((0, .5), 0), (1, 1), ((1, .5), 0), ((1, 1.0), 1)], son=("senin tabağın 🍝", "senin"))),
    (["Onu kafese koyamazsın.", "Özgür bırakırsan, her seferinde sana geri döner."],
     "yorunge", dict(merkez="🙂", gezen="🕊", etiket=("hep geri döner", 1))),
])

video, bosluk = hazirla(SPEC)
