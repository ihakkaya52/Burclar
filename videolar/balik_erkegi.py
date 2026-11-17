import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Balık", cins="e", maddeler=[
    (["Hayal dünyasında yaşar.", "Seninle konuşurken bile aklı başka bir filmde."],
     "saganak", dict(emo="💭", buyuk="🎬", etiket=("şu an: başka filmde", 1))),
    (["“Hayır” demeyi beceremez.", "Bu yüzden başı hep derde girer."],
     "salter", dict(sol="HAYIR", sag="EVET", gecis=[(0, 1), ((0, .7), 1), (1, 1)], son=("yine “evet” dedi 😅", 1))),
    (["Kırıldığını söylemez.", "Ortadan kaybolur…", "ve hüzünlü bir şarkı paylaşır."],
     "sonra", dict(emo="💔", sure="1 SAAT SONRA… ⏰", balon="🎵 hikâyesinde: hüzünlü şarkı", tetik=2)),
    (["Senin derdini kendi derdi yapar.", "Sen ağlarsan, o da ağlar."],
     "donusum", dict(a=("😢", (80, 100, 200), None), b=("😭", (60, 80, 200), "yagmur"), tetik="o")),
    (["Onu seversen, sana masal gibi bir aşk yaşatır.", "Yeter ki kalbini kırma."],
     "yorunge", dict(merkez="❤", gezen="🐟", etiket=("yeter ki kırma 🥺", 1))),
])

video, bosluk = hazirla(SPEC)
