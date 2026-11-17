import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Kova", cins="e", maddeler=[
    (["Herkes sağa giderken, o sola gider.", "Sırf farklı olmak için."],
     "salter", dict(sol="O", sag="HERKES", gecis=[("sağa", 1), ("sola", 0)], son=("farklı. 👽", 1))),
    (["Mesajına 3 gün cevap vermez.", "Sonra hiçbir şey olmamış gibi bir video atar."],
     "sonra", dict(emo="📱", sure="3 GÜN SONRA… ⏰", balon="şuna bak 😂 [video]", tetik=1)),
    (["Duygusal konuşmalar onu gerer.", "“Biz neyiz” diye sorarsan, konu uzaya gider."],
     "mesaj", dict(msgs=[("r", "biz neyiz? 🥺", 1), ("l", "sence evren sonsuz mu? 🚀", "uzaya")])),
    (["Arkadaşları onun ailesidir.", "Önce dostun olur, sonra sevgilin."],
     "liste", dict(satirlar=[("1. arkadaş ✅", "önce"), ("2. kanka ✅", ("önce", .5))], son=("3. sevgili ❤", "sonra", PINK))),
    (["Onu değiştirmeye çalışma.", "Olduğu gibi kabul edersen, en sadık insan odur."],
     "yuksel", dict(arka="👽", tetik="sadık")),
])

video, bosluk = hazirla(SPEC)
