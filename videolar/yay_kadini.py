import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Yay", cins="k", maddeler=[
    (["Ona “yapma” dersen, önce onu yapar."],
     "damga", dict(emo="🚫", text="YAPTI BİLE 😏", tetik="önce")),
    (["Rutin onu boğar.", "Aynı kafeye 3 kez gittiyse, bu bir rekordur."],
     "sayac", dict(hedef=3, birim="kez aynı kafe", emo="☕", tetik=1, son=("REKOR 🏆", "rekordur"))),
    (["Fazla dürüsttür.", "Cevabına hazır değilsen, fikrini sorma."],
     "mesaj", dict(msgs=[("r", "sence o beni seviyor mu?", 0), ("l", "hayır.", 1)], damga=("SORDUN. 🤷", "sorma"))),
    (["Planı yoktur, bileti vardır.", "Gerisini yolda düşünür."],
     "kacis", dict(emo="✈", tetik="bileti", etiket="gerisi yolda 🗺")),
    (["Özgürlüğüne saygı duyarsan, dünyanın öbür ucundan bile sana döner."],
     "yorunge", dict(merkez="❤", gezen="✈", etiket=("hep sana döner", "döner"))),
])

video, bosluk = hazirla(SPEC)
