import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Koç", cins="e", maddeler=[
    (["Beklemeyi hiç sevmez.", "Mesajına geç dönersen, kapında bulursun."],
     "mesaj", dict(msgs=[("l", "neredesin? 👀", 0), ("l", "alo?? 😤", (0, .8))], damga=("KAPIDAYIM 🚪", "kapında"))),
    (["Onunla yarışa girme.", "Tavla bile olsa, kaybetmeyi kabul etmez."],
     "gosterge", dict(etiket="HIRS 🔥", soru="bir el daha? 🎲", cevap="kazanana kadar 😤", tetik=1)),
    (["Öfkesi çabuk parlar…", "ama 5 dakika sonra hiçbir şey olmamış gibi davranır."],
     "sonra", dict(emo="🌋", sure="5 DAKİKA SONRA… ⏰", balon="ee, ne yiyoruz? 😊", tetik=1)),
    (["Aklındakini direkt yüzüne söyler.", "Lafı dolandırmasını bekleme."],
     "yazi", dict(text="bence o sana hiç yakışmamış", damga="FİLTRESİZ 🎯", tetik=1)),
    (["Sevdiği kişi için ateşe atlar.", "Hem de hiç düşünmeden."],
     "yorunge", dict(merkez="❤", gezen="🔥", etiket=("düşünmeden. 🐏", 1))),
])

video, bosluk = hazirla(SPEC)
