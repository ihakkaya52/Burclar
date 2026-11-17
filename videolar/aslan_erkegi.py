import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from engine import *
from yardimci import big, spread, ses, zaman
from sahne import *

ATES = EL["Ateş"]; ALTIN = (255, 190, 60); MAVI = (0, 132, 255); GRI = (58, 58, 72)

def video():
    z = zaman("aslan_erkegi")          # mp3 saniyesi -> video saniyesi
    T = z(32.48) + .7
    v = Video(T, [ATES, (170, 60, 20)], 211)
    v.voice = ses("aslan_erkegi")
    c = lambda t: z(t) - .12           # sahne kesmeleri kelimeden hemen önce

    # ---- giriş: "Hayatında bir Aslan erkeği mi var?"  (önce burç, sonra takvim)
    t1 = c(2.18)
    v.add(Glow(ATES, W / 2, 620, 680, 0, t1, .65, nabiz=.12))
    v.add(Img(medallion("Aslan", "♂", 300), W / 2, 480, 0, t1, "pop", dur=.02, bob=8)); v.sfx.append((0.0, "swish"))
    for k in range(3): v.add(Yorunge(emoji_img("🦁", 100), W / 2, 480, 330, 140, .05, t1, 3.2, k * 2.094))
    v.cap("Hayatında bir", set(), 730, z(.05), t1, size=62, times=[z(.05), z(.45)], emph=False)
    v.slam(big("ASLAN", 240, WHITE), W / 2, 900, z(.80) - .12, t1, power=.15, sound="boom"); v.shake(z(.82), 30)
    v.slam(big("ERKEĞİ", 200, YEL), W / 2, 1120, z(1.10) - .12, t1, power=.1)
    v.slam(sticker("mi var? 👀", 60, WHITE, BLACK, rot=-4), W / 2, 1330, z(1.50), t1, power=.05, sound="pop")

    # ---- "23 Temmuz ile 22 Ağustos arasında doğduysa, şu beş şeyi bilmen lazım."
    v.cut(t1); t2 = c(6.94)
    v.add(Glow(ALTIN, W / 2, 680, 620, t1, t2, .45))
    takvim(v, ASLAN, t1, z(2.25), z(3.15), z(4.10), t2, y=650)
    v.cap("23 Temmuz – 22 Ağustos", {"23", "22"}, 1120, z(2.19), t2, size=74, times=[z(2.19), z(2.55), z(2.95), z(3.15), z(3.60)], maxw=1000)
    v.cap("arasında doğduysa,", set(), 1230, z(4.15), t2, size=54, times=spread([(z(4.15), z(5.12), 2)]), emph=False)
    v.slam(sticker("şu 5 şeyi bilmen lazım 👇", 62, RED, WHITE, rot=-3, maxw=980), W / 2, 1380, z(5.24) - .12, t2, power=.1, sound="boom"); v.shake(z(5.3), 24)

    # ---- 5: "Girdiği ortamda fark edilmek ister. Fark etmezsen, fark ettirir."
    v.cut(t2); t3 = c(11.66); a = t2 + .75; bag = z(10.72) - .1
    sayi(v, 5, t2, t3, 170, 420)
    v.add(Spot(W / 2, 330, 800, 520, a, t3))
    v.add(Img(emoji_img("🦁", 240), W / 2, 610, a, t3, "drop", bob=8)); v.sfx.append((a + .35, "hit"))
    for k in range(5):
        x = 220 + k * 160
        v.add(Img(emoji_img("😐", 90), x, 900, a + .2 + k * .07, bag, "pop")); v.add(Img(emoji_img("😳", 100), x, 900, bag, t3, "pop"))
    v.add(Img(emoji_img("📣", 190), 830, 560, bag, t3, "spin", pulse=.12)); v.sfx.append((bag, "boom")); v.shake(bag + .05, 36); v.punch.append((bag + .05, .12)); v.flashes.append((bag + .05, 90))
    for k in range(3): v.add(Shock(bag + .05 + k * .16, 830, 560, YEL, 60, 520, .5, 14))
    v.cap("Girdiği ortamda fark edilmek ister.", {"fark"}, 1110, z(7.61), t3, size=66, times=spread([(z(7.61), z(8.42), 2), (z(8.47), z(9.34), 3)]), maxw=940)
    v.cap("Fark etmezsen, fark ettirir. 📣", {"ettirir."}, 1330, z(9.70), t3, size=58, times=spread([(z(9.70), z(10.47), 2), (z(10.72), z(11.25), 2)]), maxw=960)

    # ---- 4: "Ona bir iltifat et, gerisini o halleder."
    v.cut(t3); t4 = c(14.80); a = t3 + .7
    sayi(v, 4, t3, t4, 910, 420, bekle=.58)
    v.add(Glow(ALTIN, W / 2, 660, 600, z(13.47), t4, .55, nabiz=.15))
    v.pop(balon("bugün çok iyi görünüyorsun 😍", 44, MAVI, WHITE, "r", maxw=520), 430, 520, z(12.40), t4, sound="msg")
    v.add(Meter("EGO 👑", W / 2, 730, 700, a, t4, z(13.47), .7, c0=(255, 190, 60), c1=RED))
    v.sfx.append((z(13.47), "riser")); v.shake(z(14.17), 30); v.punch.append((z(14.17), .09)); v.sfx.append((z(14.12), "boom"))
    v.pop(balon("biliyorum 😎", 54, GRI, WHITE, "l"), 620, 920, z(14.15), t4, sound="msg")
    v.cap("Ona bir iltifat et,", {"iltifat"}, 1110, z(12.33), t4, size=78, times=spread([(z(12.33), z(13.13), 4)]))
    v.cap("gerisini o halleder.", {"halleder."}, 1300, z(13.47), t4, size=62, times=spread([(z(13.47), z(14.43), 3)]))

    # ---- 3: "Gururu her şeyden önce gelir. Özür dilemesi… biraz uzun sürer."
    v.cut(t4); t5 = c(19.68); a = t4 + .65; b = z(17.22) - .12; g = z(18.50) - .12
    sayi(v, 3, t4, t5, 170, 420, bekle=.5)
    v.add(Glow(ALTIN, W / 2, 620, 600, a, b, .6, nabiz=.12))
    v.add(Img(emoji_img("👑", 250), W / 2, 620, a, b, "drop", pulse=.08)); v.sfx.append((a + .35, "ding"))
    v.cut(b)
    v.add(Glow((120, 90, 230), W / 2, 640, 600, b, t5, .5))
    v.pop(balon("özür dileyecek misin? 🙃", 44, MAVI, WHITE, "r"), 690, 480, b, t5, sound="msg")
    v.add(Yaziyor(330, 660, z(17.5), g)); v.sfx += [(z(17.5), "type"), (z(18.2), "type")]
    v.slam(sticker("3 GÜN SONRA… ⏰", 66, YEL, BLACK, rot=-4, maxw=900), W / 2, 680, g, t5, power=.1, sound="boom"); v.shake(g + .15, 24)
    v.pop(balon("tamam… belki biraz haklısın 🙄", 44, GRI, WHITE, "l"), W / 2, 880, z(18.95), t5, sound="msg")
    v.cap("Gururu her şeyden önce gelir.", {"Gururu"}, 1110, z(15.34), b, size=70, times=spread([(z(15.34), z(16.83), 5)]), maxw=940)
    v.cap("Özür dilemesi…", {"Özür"}, 1110, z(17.22), t5, size=84, times=spread([(z(17.22), z(18.25), 2)]))
    v.cap("biraz uzun sürer.", {"uzun"}, 1290, z(18.50), t5, size=64, times=spread([(z(18.50), z(19.28), 3)]))

    # ---- 2: "Cömerttir. Sevdiğine son lokmasını verir… ama bunu herkese anlatır."
    v.cut(t5); t6 = c(24.51); a = t5 + .6; b = z(22.96) - .12
    sayi(v, 2, t5, t6, 910, 420, bekle=.48)
    v.add(Glow(ATES, W / 2, 620, 600, a, t6, .5))
    v.add(Yagis("kar", a, z(21.3), (120, 330, 820, 940), 14, seed=4, emo="🎁"))
    v.add(Img(emoji_img("🎁", 230), W / 2, 620, a, z(21.0), "drop", bob=9)); v.sfx.append((a + .35, "pop"))
    v.add(Img(emoji_img("🦁", 190), 260, 620, z(21.0), t6, "left")); v.add(Img(emoji_img("🙂", 150), 800, 640, z(21.0), t6, "right"))
    v.add(Fx(emoji_img("🍕", 130), z(21.5), t6, lambda lt: (380 + 300 * ease(lt / .9), 640 - 90 * math.sin(math.pi * min(1, lt / .9)), 1, 40 * min(1, lt / .9), min(1, lt * 6))))
    v.sfx.append((z(21.5), "swish")); v.sfx.append((z(22.4), "pop"))
    v.add(Img(emoji_img("📣", 170), W / 2, 440, b, t6, "spin", pulse=.1)); v.sfx.append((b, "hit")); v.shake(b + .1, 22)
    for k, (m, x, y, yon) in enumerate((("ben ısmarladım 😎", 330, 820, "l"), ("son lokmamı verdim!", 730, 900, "r"), ("duydunuz mu? 👂", 400, 980, "l"))):
        v.pop(balon(m, 40, GRI if yon == "l" else MAVI, WHITE, yon), x, y, b + .25 + k * .3, t6, sound="msg")
    v.cap("Cömerttir.", {"Cömerttir."}, 1100, z(20.23), b, size=100, times=[z(20.23)])
    v.cap("Sevdiğine son lokmasını verir…", {"son"}, 1290, z(21.09), b, size=50, times=spread([(z(21.09), z(22.49), 4)]), maxw=960)
    v.cap("ama bunu herkese anlatır.", {"herkese"}, 1220, z(22.96), t6, size=74, times=spread([(z(22.96), z(24.03), 4)]), maxw=940)

    # ---- "Ve bir numara…" (ardından 0,6 sn sessizlik)
    v.cut(t6); t7 = c(25.58)
    v.cap("Ve 1 numara...", {"1"}, 880, z(24.52), t7, size=110, gap=.3, times=[z(24.52), z(24.75), z(24.95)])
    v.ducks.append((t6, t7)); v.sfx.append((t7 - 1.5, "riser"))

    # ---- 1: "Seni bir kez sahiplendiyse, arkanda dağ gibi durur."
    v.cut(t7); t8 = c(29.00); gel = z(27.36) - .1; dag = z(27.75)
    sayi(v, 1, t7, t8, 170, 420, bekle=0, ses="boom")
    v.add(Glow(ATES, W / 2, 620, 680, gel, t8, .7, nabiz=.15))
    v.add(Fx(emoji_img("🏔", 520), dag - .1, t8, lambda lt: (W / 2, 600 + 260 * (1 - ease(lt / .3)), 1, 0, min(1, lt * 5) * .9)))
    v.add(Fx(emoji_img("🦁", 330), gel, t8, lambda lt: (W / 2, 590 + 330 * (1 - back(lt / .4, 1.2)), .5 + .5 * ease(lt / .4), 0, min(1, lt * 5))))
    v.add(Img(emoji_img("🙂", 140), W / 2, 850, t7 + .15, t8, "pop", bob=5)); v.add(Img(sticker("sen", 40, WHITE, BLACK, rot=-5), W / 2 + 130, 900, t7 + .35, t8, "pop"))
    v.sfx.append((gel, "whoosh")); v.sfx.append((dag - .05, "boom")); v.shake(dag, 40); v.punch.append((dag, .14)); v.flashes.append((dag, 100))
    v.cap("Seni bir kez sahiplendiyse,", {"sahiplendiyse,"}, 1100, z(25.60), t8, size=64, times=spread([(z(25.60), z(27.20), 4)]), maxw=980)
    v.cap("arkanda dağ gibi durur.", {"dağ"}, 1290, z(27.36), t8, size=78, times=spread([(z(27.36), z(28.61), 4)]), maxw=960)

    # ---- kapanış: "Tanıdık geldi mi? O Aslan'ı etiketle, bu videoyu da kaydet."
    v.cut(t8)
    v.add(Glow(ATES, W / 2, 700, 640, t8, T, .5, nabiz=.1))
    v.add(Img(medallion("Aslan", "♂", 190), W / 2, 420, t8, T, "spin", bob=8))
    for k in range(2): v.add(Yorunge(emoji_img("🦁", 84), W / 2, 420, 250, 90, t8 + .2, T, 2.6, k * 3.1416))
    v.slam(sticker("Tanıdık geldi mi? 👀", 74, WHITE, BLACK, rot=-4, maxw=960), W / 2, 700, z(29.02) - .12, T, power=.07, sound="hit")
    v.cap("O Aslan'ı etiketle 👇", {"etiketle"}, 960, z(30.00), T, size=84, times=spread([(z(30.00), z(31.15), 3)]))
    v.slam(sticker("bu videoyu da kaydet 📌", 54, YEL, BLACK, rot=3), W / 2, 1200, z(31.28) - .1, T, power=.05, sound="pop")
    return v
