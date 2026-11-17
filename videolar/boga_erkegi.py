import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Boğa", cins="e", maddeler=[
    (["Rahatını bozma.", "Koltuğundan kalkması için çok iyi bir sebebin olmalı."],
     "mesaj", dict(msgs=[("r", "dışarı çıkalım mı? 🙃", 0), ("l", "evde yemek var 🛋", 1)], damga=("KALKMAZ.", "sebebin"))),
    (["Kalbine giden yol, gerçekten midesinden geçer.", "Güzel bir sofra, ona en büyük iltifattır."],
     "saganak", dict(emo="🥟", buyuk="🍝", etiket=("aşk dili: yemek 😋", 1))),
    (["Bir karar verdiyse, onu kimse döndüremez.", "Boşuna uğraşma."],
     "duvar", dict(balonlar=[("hadi ama 🥺", 0), ("lütfen?", (0, .7)), ("bir kere! 😩", (0, 1.4))])),
    (["Az kişiyi sever…", "ama sevdiğini asla bırakmaz."],
     "liste", dict(satirlar=[("tanıdıklar ❌", 0), ("takipçiler ❌", (0, .45))], son=("SEN ✅ ömürlük", 1, GREEN))),
    (["Sabrı sonsuz gibi görünür.", "Ama bir gün taşarsa…", "kaçacak yer ara."],
     "donusum", dict(a=("😌", (60, 170, 120), None), b=("🌋", (230, 60, 40), None), tetik=2, simsek=True)),
])

video, bosluk = hazirla(SPEC)
