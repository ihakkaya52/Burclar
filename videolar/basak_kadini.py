import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Başak", cins="k", maddeler=[
    (["Dağınıklığa dayanamaz.", "Farkında olmadan senin masanı bile toplar."],
     "donusum", dict(a=("🌪", (120, 90, 60), None), b=("✨", (60, 170, 200), None), tetik=1)),
    (["Her şeyi analiz eder.", "Attığın mesajdaki noktayı bile."],
     "mesaj", dict(msgs=[("r", "Tamam.", 0)], damga=("NOKTA MI KOYDU? 🧐", "noktayı"), buyutec=True)),
    (["Mükemmeliyetçidir.", "En çok da kendine karşı acımasızdır."],
     "gosterge", dict(etiket="OLDU MU? 📏", cevap="hâlâ olmadı 😩", tetik=0, hedef=99, c0=ALTIN, c1=GREEN)),
    (["Yardım istemeyi bilmez.", "Ama herkesin yardımına ilk o koşar."],
     "yol", dict(giden="🏃", hedef="🆘", var="koşar", etiket="ilk o 🥇")),
    (["Sevgisini büyük laflarla değil, küçük detaylarla gösterir.", "Kahveni nasıl içtiğini asla unutmaz."],
     "arsiv", dict(baslik="📁 SEN", satirlar=["kahve: sütlü, şekersiz", "alerji: çilek", "üşürsün, hırka aldım"], damga="EZBERE", tetik=1, once="☕")),
])

video, bosluk = hazirla(SPEC)
