import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from kalip import *

# Her madde: (cümleler, sahne kalıbı, kalıbın ayarları). Sıra: 5, 4, 3, 2, 1.
# Tetik: sayı = o cümlenin başı, kelime = o kelimenin söylendiği an, (tetik, sn) = tetikten sn kadar sonra.
SPEC = dict(burc="Oğlak", cins="k", maddeler=[
    (["Hedefi olmayan bir günü yoktur.", "Pazar sabahı bile yapılacaklar listesi vardır."],
     "liste", dict(satirlar=[("07.00 spor ✅", (0, .4)), ("09.00 plan ✅", (0, .9)), ("pazar: yine liste ✅", 1)], son=("dinlenmek ⏳ sırada", "listesi", KOYU))),
    (["Zayıflığını kimseye göstermez.", "Yorulduğunu, ancak en yakını anlar."],
     "donusum", dict(a=("💪", (214, 150, 20), None), b=("🥱", (90, 90, 140), None), tetik=1)),
    (["Dakiktir.", "5 dakika geç kalırsan, o 5 dakikayı da not eder."],
     "sayac", dict(hedef=5, birim="dakika gecikme", emo="⏱", tetik=1, son=("not edildi 📝", "not"))),
    (["Lüksü sever, ama parasını kendi kazanır.", "Kimseye minnet etmez."],
     "damga", dict(emo="💎", text="KENDİ ALDI 💅", tetik="kendi", renk=(150, 40, 90))),
    (["Seni hayatına aldıysa, bu ciddi bir karardır.", "Çünkü o, hiçbir şeyi şansa bırakmaz."],
     "kapi", dict(ac=True, tetik="ciddi", etiket="ONAYLANDI ✅", ic="🙂")),
])

video, bosluk = hazirla(SPEC)
