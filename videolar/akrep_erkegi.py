import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from engine import *
from yardimci import big, spread, ses, zaman
from sahne import *

SU = EL["Su"]; MOR = (150, 40, 90); MAVI = (0, 132, 255)

def video():
    z = zaman("akrep_erkegi")          # mp3 saniyesi -> video saniyesi
    T = z(34.40) + .7
    v = Video(T, [SU, (150, 30, 70)], 97)
    v.voice = ses("akrep_erkegi")
    c = lambda t: z(t) - .12           # sahne kesmeleri kelimeden hemen önce

    # ---- giriş: "23 Ekim ile 21 Kasım arasında doğan bir erkek mi var hayatında?"
    t1 = c(3.91)
    v.add(Glow((200, 60, 50), W / 2, 680, 620, 0, t1, .5))
    takvim_giris(v, z(.05), z(1.02), z(1.95), t1)
    v.cap("23 Ekim – 21 Kasım", {"23", "21"}, 1165, z(.02), t1, size=88, times=[z(.02), z(.45), z(.80), z(1.0), z(1.44)])
    v.cap("arasında doğan bir erkek mi var hayatında? 👀", {"erkek"}, 1335, z(1.75), t1, size=56,
          times=spread([(z(1.75), z(2.25), 1), (z(2.25), z(3.58), 6)]), maxw=900)
    v.slam(sticker("ERKEK ♂", 50, BLUE, WHITE, rot=6), 850, 1010, z(2.60), t1, power=.06, sound="hit")

    # ---- "O bir Akrep."
    v.cut(t1); t2 = c(4.88)
    v.add(Glow(SU, W / 2, 620, 640, t1, t2, .6, nabiz=.12))
    v.add(Img(medallion("Akrep", "♂", 320), W / 2, 520, t1, t2, "spin", bob=8)); v.sfx.append((t1, "swish"))
    for k in range(3): v.add(Yorunge(emoji_img("🦂", 96), W / 2, 520, 330, 150, t1 + .15, t2, 3.2, k * 2.094))
    v.cap("O bir", set(), 860, z(3.91), t2, size=70, times=[z(3.91), z(4.05)], emph=False)
    v.slam(big("AKREP", 250, YEL), W / 2, 1060, z(4.18) - .12, t2, power=.15, sound="boom"); v.shake(z(4.2), 30)

    # ---- "Ve şu beş şeyi bilmeden ona yaklaşma."
    v.cut(t2); t3 = c(7.38)
    for k, n in enumerate((5, 4, 3, 2, 1)):
        tk = z(4.95) + k * .14
        v.add(Img(big(str(n), 190, YEL, 10), 180 + k * 180, 560 + (-22 if k % 2 else 22), tk, t3, "drop", bob=7)); v.sfx.append((tk + .3, "tick"))
    v.cap("Ve şu 5 şeyi bilmeden", {"5"}, 900, z(4.89), t3, size=78, times=[z(4.89), z(5.05), z(5.25), z(5.50), z(5.80)])
    v.slam(sticker("ona yaklaşma ✋", 80, RED, WHITE, rot=-4, maxw=960), W / 2, 1150, z(6.33) - .12, t3, power=.1, sound="boom"); v.shake(z(6.4), 26)

    # ---- 5: "Ondan hiçbir şey saklayamazsın. Sen söylemeden, gözlerinden okur."
    v.cut(t3); t4 = c(12.19); a = t3 + .8
    sayi(v, 5, t3, t4, 170, 420)
    v.add(Glow((70, 200, 220), W / 2, 640, 560, a, t4, .45))
    v.add(Img(emoji_img("👀", 210), W / 2, 500, a, t4, "pop", bob=10)); v.sfx.append((a, "pop"))
    v.add(Yazi("bunu kimseye söylemedim", W / 2, 790, z(8.6), t4, z(10.10), z(11.55), mod="coz", size=54, kuyruk="l"))
    v.sfx += [(z(10.10), "type"), (z(10.9), "type")]
    v.add(Fx(emoji_img("🔍", 130), z(10.0), z(11.7), lambda lt: (250 + 360 * lt, 760 + 14 * math.sin(lt * 9), 1, 0, min(1, lt * 6))))
    v.slam(sticker("okundu ✅", 50, MAVI, WHITE, rot=5), 780, 930, z(11.55), t4, power=.07, sound="hit")
    v.cap("Ondan hiçbir şey saklayamazsın.", {"saklayamazsın."}, 1100, z(8.10), t4, size=74, times=spread([(z(8.10), z(9.80), 4)]), maxw=960)
    v.cap("Sen söylemeden, gözlerinden okur.", {"gözlerinden"}, 1320, z(10.10), t4, size=58, times=spread([(z(10.10), z(10.80), 2), (z(10.85), z(11.67), 2)]), maxw=900)

    # ---- 4: "Kıskanır… ama sorarsan, yok bir şey der."
    v.cut(t4); t5 = c(15.84); a = t4 + .75
    sayi(v, 4, t4, t5, 910, 420, bekle=.6)
    v.add(Glow((230, 60, 50), W / 2, 620, 580, z(12.93), t5, .5, nabiz=.15))
    v.add(Meter("KISKANÇLIK 😒", W / 2 - 110, 520, 620, a, t5, z(12.93), .75))
    v.sfx.append((z(12.93), "riser")); v.shake(z(13.68), 30); v.punch.append((z(13.68), .09)); v.sfx.append((z(13.62), "boom"))
    v.pop(balon("kıskandın mı? 🤨", 46, MAVI, WHITE, "r"), 700, 720, z(13.78), t5, sound="msg")
    v.pop(balon("yok bir şey 🙂", 54, (58, 58, 72), WHITE, "l"), 400, 880, z(14.78), t5, sound="msg")
    v.cap("Kıskanır…", {"Kıskanır…"}, 1090, z(12.93), t5, size=100, times=[z(12.93)])
    v.cap("ama sorarsan, “yok bir şey” der.", {"“yok", "şey”"}, 1300, z(13.78), t5, size=52, times=spread([(z(13.78), z(14.59), 2), (z(14.82), z(15.45), 4)]), maxw=900)

    # ---- 3: "Az konuşur, çok dinler. Bugün söylediğini, 3 yıl sonra sana hatırlatır."
    v.cut(t5); t6 = c(21.01); a = t5 + .7; b = z(19.29) - .12
    sayi(v, 3, t5, t6, 170, 420, bekle=.55)
    v.add(Glow((120, 90, 230), W / 2, 640, 580, a, t6, .5))
    v.add(Fx(sticker("🔴 KAYITTA", 44, RED, WHITE, rot=-3), a, b, lambda lt: (W / 2 + 60, 430, 1, 0, .45 + .55 * (int(lt * 2.5) % 2 == 0))))
    v.add(Img(emoji_img("👂", 170), 190, 660, a, b, "left")); v.sfx.append((a, "pop"))
    v.add(Dalga(630, 660, 620, 300, a, b, col=(190, 170, 255)))
    v.cut(b)
    v.slam(sticker("3 YIL SONRA… ⏰", 70, YEL, BLACK, rot=-4, maxw=900), W / 2 + 70, 580, b, t6, power=.1, sound="boom"); v.shake(b + .15, 24)
    v.pop(balon("sen o gün demiştin ki… 🙂", 46, (58, 58, 72), WHITE, "l"), W / 2, 800, z(19.95), t6, sound="msg")
    v.cap("Az konuşur, çok dinler.", {"dinler."}, 1090, z(16.47), b, size=80, times=spread([(z(16.47), z(17.13), 2), (z(17.34), z(17.85), 2)]))
    v.cap("Bugün söylediğini,", set(), 1290, z(18.21), b, size=58, times=spread([(z(18.21), z(19.16), 2)]), emph=False)
    v.cap("3 yıl sonra sana hatırlatır.", {"3", "hatırlatır."}, 1120, z(19.29), t6, size=74, times=spread([(z(19.29), z(20.48), 5)]), maxw=940)

    # ---- 2: "Güvenini bir kez kırarsan, o kapı bir daha açılmaz."
    v.cut(t6); t7 = c(24.78); a = t6 + .65; kapan = z(23.40)
    sayi(v, 2, t6, t7, 910, 420, bekle=.5)
    v.add(Glow((255, 200, 90), W / 2, 640, 520, a, kapan, .55))
    v.add(Kapi(W / 2, 650, 340, 500, a, t7, 1.0, [(kapan - .16, 0.0, .16)]))
    v.add(Img(emoji_img("💔", 150), 250, 620, z(22.55), t7, "pop", bob=8)); v.sfx.append((z(22.55), "pop"))
    v.sfx.append((kapan - .05, "boom")); v.shake(kapan, 38); v.punch.append((kapan, .13)); v.flashes.append((kapan, 90))
    v.add(Img(emoji_img("🔒", 170), W / 2, 660, z(23.80), t7, "drop")); v.sfx.append((z(23.80) + .35, "hit")); v.shake(z(23.80) + .38, 16)
    v.slam(sticker("bir daha açılmaz.", 46, RED, WHITE, rot=5), 810, 880, z(24.05), t7, power=.05, sound="pop")
    v.cap("Güvenini bir kez kırarsan,", {"kırarsan,"}, 1100, z(21.66), t7, size=70, times=spread([(z(21.66), z(23.09), 4)]), maxw=960)
    v.cap("o kapı bir daha açılmaz.", {"açılmaz."}, 1300, z(23.35), t7, size=64, times=spread([(z(23.35), z(24.36), 5)]), maxw=900)

    # ---- "Ve bir numara…" (ardından 0,6 sn sessizlik)
    v.cut(t7); t8 = c(25.84)
    v.cap("Ve 1 numara...", {"1"}, 880, z(24.78), t8, size=110, gap=.3, times=[z(24.78), z(25.0), z(25.2)])
    v.ducks.append((t7, t8)); v.sfx.append((t8 - 1.5, "riser"))

    # ---- 1: "Onda ortası yok. Ya hep, ya hiç. Severse, tüm kalbiyle sever."
    v.cut(t8); t9 = c(30.80)
    sayi(v, 1, t8, t9, 170, 420, bekle=0, ses="boom")
    v.add(Glow(PINK, W / 2, 640, 600, z(28.57), t9, .6, nabiz=.15))
    v.add(Anahtar(W / 2, 640, t8 + .1, t9, [(z(27.17) - .06, 1), (z(27.81) - .06, 0), (z(28.57) - .06, 1)]))
    for tt in (27.17, 27.81, 28.57): v.sfx.append((z(tt) - .06, "hit")); v.shake(z(tt), 16)
    v.add(Img(emoji_img("❤", 170), W / 2, 440, z(28.57), t9, "pop", pulse=.16)); v.sfx.append((z(28.6), "heart")); v.sfx.append((z(29.5), "heart"))
    v.add(Particles(z(29.38), W / 2, 520, "hearts", 34, seed=4, spread=.8))
    v.cap("Onda ortası yok.", {"ortası"}, 1000, z(25.84), t9, size=70, times=spread([(z(25.84), z(26.77), 3)]))
    v.cap("Ya hep, ya hiç.", {"hep,", "hiç."}, 1150, z(27.17), t9, size=104, times=[z(27.17), z(27.32), z(27.81), z(27.98)])
    v.cap("Severse, tüm kalbiyle sever. ❤", {"kalbiyle"}, 1330, z(28.57), t9, size=52, times=spread([(z(28.57), z(29.21), 1), (z(29.38), z(30.28), 3)]), maxw=940)

    # ---- kapanış: "Tanıdık geldi mi? O Akrep'i etiketle, bu videoyu da kaydet."
    v.cut(t9)
    v.add(Glow(SU, W / 2, 700, 640, t9, T, .5, nabiz=.1))
    v.add(Img(medallion("Akrep", "♂", 190), W / 2, 420, t9, T, "spin", bob=8))
    v.slam(sticker("Tanıdık geldi mi? 👀", 74, WHITE, BLACK, rot=-4, maxw=960), W / 2, 700, z(30.80) - .12, T, power=.07, sound="hit")
    v.cap("O Akrep'i etiketle 👇", {"etiketle"}, 960, z(31.87), T, size=84, times=spread([(z(31.87), z(33.02), 3)]))
    v.slam(sticker("bu videoyu da kaydet 📌", 54, YEL, BLACK, rot=3), W / 2, 1200, z(33.14) - .1, T, power=.05, sound="pop")
    for k in range(2): v.add(Yorunge(emoji_img("🦂", 80), W / 2, 420, 250, 90, t9 + .2, T, 2.6, k * 3.1416))
    return v
