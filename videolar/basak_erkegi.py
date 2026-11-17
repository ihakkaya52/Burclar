import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Başak", cins="e", maddeler=[
    (["Her detayı fark eder.", "Yamuk asılmış bir tabloyu görmeden geçemez."],
     "duzelt", dict(emo="🖼", tetik="geçemez", etiket="oh. ✅")),
    (["Seni eleştiriyorsa, önemsiyordur.", "Sustuysa, asıl o zaman endişelen."],
     "mesaj", dict(msgs=[("l", "şurası olmamış 🧐", 0), ("l", "burası da.", (0, .7))], damga=("…sustu. 😶", 1))),
    (["Plansız iş yapmaz.", "Tatile bile liste hazırlayarak gider."],
     "liste", dict(satirlar=[("güneş kremi ✅", (0, .3)), ("yedek şarj ✅", (0, .8)), ("B planı ✅", 1)], son=("B planının yedeği ✅", "liste", GREEN))),
    (["Duygularını sözle anlatamaz.", "Ama arabanın lastiğini kontrol ediyorsa, seni seviyordur."],
     "donusum", dict(a=("🤐", (90, 90, 120), None), b=("🔧", (60, 170, 120), "❤"), tetik=1)),
    (["Ona güvenebilirsin.", "Söz verdiyse, o iş olmuş demektir."],
     "damga", dict(emo="🤝", text="SÖZ = İMZA ✅", tetik=1, renk=GREEN)),
])

video, bosluk = hazirla(SPEC)
