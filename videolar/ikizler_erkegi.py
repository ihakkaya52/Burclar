import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="İkizler", cins="e", maddeler=[
    (["Sıkıldığı an ortadan kaybolur.", "Sohbet onu sarmıyorsa, aklı çoktan başka yerde."],
     "kacis", dict(emo="😶", tetik="kaybolur", etiket="çevrimdışı 💨")),
    (["Aynı anda 5 kişiyle mesajlaşır…", "ve hepsine ayrı bir espri yapar."],
     "mesaj", dict(msgs=[("l", "😂😂😂", (0, .3)), ("r", "ahahah çok iyiydi", (0, .9)), ("l", "bu neydi şimdi 🤣", 1)])),
    (["Onunla tartışmaya girme.", "Lafı öyle bir çevirir ki, özür dileyen sen olursun."],
     "sonra", dict(emo="😤", sure="2 DAKİKA SONRA… ⏰", balon="…özür dilerim?? 😳", tetik="özür")),
    (["Bugün “evet” diyorsa, yarın “belki” der.", "Planlar son dakika değişir, alış."],
     "salter", dict(sol="BELKİ", sag="EVET", gecis=[("evet", 1), ("belki", 0), (1, 1), ((1, .5), 0)], son=("alış. 🤷", "alış"))),
    (["Onu güzellikle değil, sohbetle tutarsın.", "Aklını yakalarsan, kalbi peşinden gelir."],
     "yorunge", dict(merkez="🧠", gezen="❤", etiket=("önce akıl, sonra kalp", 1))),
])

video, bosluk = hazirla(SPEC)
