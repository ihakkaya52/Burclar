import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Yay", cins="e", maddeler=[
    (["Yerinde duramaz.", "Bavulu her zaman yarı hazırdır."],
     "kacis", dict(emo="🧳", tetik=1, etiket="yolda ✈")),
    (["Aklına geleni söyler.", "Kırıcı olabilir, ama sana asla yalan söylemez."],
     "mesaj", dict(msgs=[("r", "yeni saçım nasıl? 🥰", 0), ("l", "eskisi daha iyiydi.", 1)], damga=("DÜRÜST 🎯", "asla"))),
    (["Onu kısıtlama.", "Sıkıştığını hissettiği an, uzaklaşır."],
     "gosterge", dict(etiket="MESAFE 🏃", soru="neredesin? kiminlesin? 🤨", tetik=1, c0=ALTIN, c1=BLUE)),
    (["En kötü günde bile güldürür.", "Morali bozuk bir Yay görmen çok zordur."],
     "donusum", dict(a=("🌧", (80, 100, 200), "yagmur"), b=("🤣", ALTIN, "konfeti"), tetik="güldürür")),
    (["Onunla hayat bir maceradır.", "“Hadi gidelim” derse, sorgulama, bavulunu al."],
     "yorunge", dict(merkez="🌍", gezen="✈", etiket=("bavulunu al 🎒", "bavulunu"))),
])

video, bosluk = hazirla(SPEC)
