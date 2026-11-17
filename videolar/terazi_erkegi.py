import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Terazi", cins="e", maddeler=[
    (["Karar vermesi saatler sürer.", "Ona sakın “ne yiyelim” diye sorma."],
     "salter", dict(sol="PİZZA", sag="BURGER", gecis=[(0, 1), ((0, .5), 0), ((0, 1.0), 1), (1, 0), ((1, .5), 1), ((1, 1.0), 0)], son=("3 saat sonra: hâlâ aynı 🙃", "sorma"))),
    (["Kavgadan kaçar.", "Ortam gerilirse, konuyu hemen değiştirir."],
     "mesaj", dict(msgs=[("r", "konuşmamız lazım. 😐", 0), ("l", "hava ne güzel bugün ☀", 1)], damga=("KONU DEĞİŞTİ 💨", "değiştirir"))),
    (["Herkese iyi davranır.", "Bunu flört sanma, o hep böyledir."],
     "damga", dict(emo="😊", text="FLÖRT DEĞİL ❌", tetik="sanma")),
    (["Şıklığına düşkündür.", "Markete giderken bile aynaya bakar."],
     "isik", dict(emo="🤵", megafon="📸", tetik="aynaya")),
    (["Adaletsizliğe dayanamaz.", "Haksızlığa uğradıysan, yanında ilk o durur."],
     "yuksel", dict(arka="⚖", tetik="yanında")),
])

video, bosluk = hazirla(SPEC)
