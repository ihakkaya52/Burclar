import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from engine import *
from yardimci import big, spread, ses, zaman
from sahne import *

ATES = EL["Ateş"]; ALTIN = (255, 190, 60); MAVI = (0, 132, 255); GRI = (58, 58, 72)

def video():
    z = zaman("aslan_kadini")          # mp3 saniyesi -> video saniyesi
    T = z(34.64) + .6
    v = Video(T, [ATES, (200, 50, 120)], 173)
    v.voice = ses("aslan_kadini")
    c = lambda t: z(t) - .12           # sahne kesmeleri kelimeden hemen önce

    # ---- giriş: "Hayatında bir Aslan kadını mı var?"  (önce burç, sonra takvim)
    t1 = c(2.21)
    v.add(Glow(PINK, W / 2, 620, 680, 0, t1, .6, nabiz=.12))
    v.add(Img(medallion("Aslan", "♀", 300), W / 2, 480, 0, t1, "pop", dur=.02, bob=8)); v.sfx.append((0.0, "swish"))
    for k in range(3): v.add(Yorunge(emoji_img("🦁", 100), W / 2, 480, 330, 140, .05, t1, 3.2, k * 2.094))
    v.cap("Hayatında bir", set(), 730, z(.06), t1, size=62, times=[z(.06), z(.50)], emph=False)
    v.slam(big("ASLAN", 240, WHITE), W / 2, 900, z(.80) - .12, t1, power=.15, sound="boom"); v.shake(z(.82), 30)
    v.slam(big("KADINI", 200, YEL), W / 2, 1120, z(1.12) - .12, t1, power=.1)
    v.slam(sticker("mı var? 👀", 60, WHITE, BLACK, rot=-4), W / 2, 1330, z(1.50), t1, power=.05, sound="pop")

    # ---- "23 Temmuz ile 22 Ağustos arasında doğduysa, şu beş şeyi aklına yaz."
    v.cut(t1); t2 = c(7.40)
    v.add(Glow(ALTIN, W / 2, 680, 620, t1, t2, .45))
    takvim(v, ASLAN, t1, z(2.28), z(3.30), z(4.25), t2, y=650)
    v.cap("23 Temmuz – 22 Ağustos", {"23", "22"}, 1120, z(2.22), t2, size=74, times=[z(2.22), z(2.62), z(3.05), z(3.30), z(3.75)], maxw=1000)
    v.cap("arasında doğduysa,", set(), 1230, z(4.30), t2, size=54, times=spread([(z(4.30), z(5.41), 2)]), emph=False)
    v.slam(sticker("şu 5 şeyi aklına yaz ✍", 62, PINK, WHITE, rot=-3, maxw=980), W / 2, 1380, z(5.56) - .12, t2, power=.1, sound="boom"); v.shake(z(5.6), 24)

    # ---- 5: "Sıradan olmayı sevmez. Girdiği yerde herkes dönüp bakar."
    v.cut(t2); t3 = c(12.10); a = t2 + .7
    sayi(v, 5, t2, t3, 150, 390, bekle=.6)
    v.add(Spot(W / 2, 330, 800, 480, a, t3))
    v.add(Img(emoji_img("💃", 300), W / 2, 620, a, t3, "drop", bob=8)); v.sfx.append((a + .35, "hit"))
    v.slam(sticker("sıradan ❌", 50, GRI, WHITE, rot=6), 800, 880, z(8.75), z(9.73), power=.05, sound="pop")
    for k in range(8):
        ang = -math.pi / 2 + (k + .5) * math.pi / 4; tk = z(10.25) + k * .1
        v.add(Img(emoji_img("👀", 96), W / 2 + 320 * math.cos(ang), 640 + 290 * math.sin(ang), tk, t3, "pop", bob=5)); v.sfx.append((tk, "tick"))
    v.shake(z(10.9), 18)
    v.cap("Sıradan olmayı sevmez.", {"Sıradan"}, 1110, z(8.11), t3, size=76, times=spread([(z(8.11), z(9.37), 3)]), maxw=960)
    v.cap("Girdiği yerde herkes dönüp bakar.", {"herkes"}, 1310, z(9.73), t3, size=50, times=spread([(z(9.73), z(11.26), 5)]), maxw=980)

    # ---- 4: "Onu görmezden gelme. Bunu asla affetmez."
    v.cut(t3); t4 = c(16.04); a = t3 + .65; eng = z(14.27) - .12
    sayi(v, 4, t3, t4, 910, 420, bekle=.55)
    v.pop(balon("günaydın ☀️ napıyorsun?", 46, GRI, WHITE, "l", maxw=560), 400, 540, a, t4, sound="msg")
    v.add(Img(sticker("görüldü · 3 saat önce", 34, (20, 20, 32), (170, 170, 190), rot=0, weight=700), 420, 680, z(13.2), t4, "up")); v.sfx.append((z(13.2), "tick"))
    v.add(Fx(emoji_img("⏳", 130), z(13.2), eng, lambda lt: (780, 700, 1, 180 * (int(lt * 1.6) % 2), min(1, lt * 5))))
    v.add(Glow((230, 60, 50), W / 2, 660, 620, eng, t4, .6, nabiz=.15))
    v.slam(sticker("ENGELLENDİ 🚫", 84, RED, WHITE, rot=-7, maxw=960), W / 2, 860, eng, t4, power=.13, sound="boom"); v.shake(eng + .15, 34)
    v.cap("Onu görmezden gelme.", {"görmezden"}, 1110, z(12.81), t4, size=76, times=spread([(z(12.81), z(14.01), 3)]), maxw=960)
    v.cap("Bunu asla affetmez.", {"asla"}, 1300, z(14.27), t4, size=66, times=spread([(z(14.27), z(15.07), 3)]))

    # ---- 3: "“Drama sevmem” der… ama en güzel sahne hep onundur."
    v.cut(t4); t5 = c(20.46); a = t4 + .6; b = z(18.03) - .12
    sayi(v, 3, t4, t5, 170, 420, bekle=.5)
    v.pop(balon("ben drama sevmem 🙄", 54, GRI, WHITE, "l"), W / 2 + 40, 620, z(16.67), b, sound="msg")
    v.cut(b)
    v.add(Glow((200, 50, 120), W / 2, 640, 640, b, t5, .6, nabiz=.12))
    v.add(Spot(W / 2, 330, 820, 560, b, t5, sallan=5))
    v.add(Img(emoji_img("🎭", 270), W / 2, 620, b, t5, "spin", bob=8)); v.sfx.append((b, "ding"))
    v.add(Yagis("kar", b, t5, (140, 330, 940, 960), 16, seed=6, emo="🌹"))
    for x, tt in ((220, 19.0), (860, 19.25)):
        v.add(Img(emoji_img("👏", 150), x, 880, z(tt), t5, "pop", pulse=.2)); v.sfx.append((z(tt), "pop"))
    v.cap("“Drama sevmem” der…", {"“Drama"}, 1110, z(16.67), b, size=78, times=spread([(z(16.67), z(17.66), 2), (z(17.70), z(17.86), 1)]), maxw=960)
    v.cap("ama en güzel sahne hep onundur.", {"sahne"}, 1180, z(18.03), t5, size=70, times=spread([(z(18.03), z(19.80), 6)]), maxw=900)

    # ---- 2: "Sevdiklerine laf ettirmez. Karşında onu bulursun."
    v.cut(t5); t6 = c(24.22); a = t5 + .6; kar = z(22.79) - .12
    sayi(v, 2, t5, t6, 910, 420, bekle=.48)
    v.add(Yazi("senin o arkadaşın biraz", 470, 600, a, kar, z(21.2), z(22.6), mod="yaz", size=50, bg=MAVI, kuyruk="r"))
    v.sfx += [(z(21.2), "type"), (z(22.0), "type")]
    v.add(Glow((230, 60, 40), W / 2, 640, 700, kar, t6, .75, nabiz=.2))
    v.add(Fx(emoji_img("🦁", 420), kar, t6, lambda lt: (W / 2, 640, 1 + 1.4 * (1 - ease(lt / .2)), 0, min(1, lt * 6))))
    v.sfx.append((kar + .1, "boom")); v.shake(kar + .15, 44); v.punch.append((kar + .15, .15)); v.flashes.append((kar + .15, 110))
    for k in range(3): v.add(Shock(kar + .15 + k * .14, W / 2, 640, YEL, 120, 700, .55, 16))
    v.cap("Sevdiklerine laf ettirmez.", {"laf"}, 1110, z(21.16), t6, size=72, times=spread([(z(21.16), z(22.48), 3)]), maxw=960)
    v.cap("Karşında onu bulursun.", {"onu"}, 1300, z(22.79), t6, size=70, times=spread([(z(22.79), z(23.85), 3)]))

    # ---- "Ve bir numara…" (ardından 0,6 sn sessizlik)
    v.cut(t6); t7 = c(25.34)
    v.cap("Ve 1 numara...", {"1"}, 880, z(24.23), t7, size=110, gap=.3, times=[z(24.23), z(24.45), z(24.65)])
    v.ducks.append((t6, t7)); v.sfx.append((t7 - 1.5, "riser"))

    # ---- 1: "Kalbi kocamandır. Ama onu kazanmak için, önce saygısını kazanman gerekir."
    v.cut(t7); t8 = c(30.40); b = z(26.85) - .12; anahtar = z(28.24); ac = z(29.25)
    sayi(v, 1, t7, t8, 170, 420, bekle=0, ses="boom")
    v.add(Glow(PINK, W / 2, 640, 640, t7, b, .65, nabiz=.15))
    v.add(Fx(emoji_img("❤", 420), t7 + .1, b, lambda lt: (W / 2, 640, (.35 + .65 * ease(lt / .9)) * (1 + .05 * math.sin(lt * 9)), 0, min(1, lt * 5))))
    v.sfx += [(t7 + .2, "heart"), (t7 + 1.0, "heart")]; v.add(Particles(z(25.9), W / 2, 600, "hearts", 30, seed=9, spread=.8))
    v.cut(b)
    v.add(Glow(ALTIN, W / 2, 650, 560, ac, t8, .75, nabiz=.1))
    v.add(Kapi(W / 2, 650, 340, 500, b, t8, 0.0, [(ac, 1.0, .35)]))
    v.add(Img(emoji_img("🔒", 150), W / 2, 660, b + .15, ac, "drop"))
    v.add(Fx(emoji_img("🔑", 150), anahtar, ac, lambda lt: (130 + 330 * ease(lt / .9), 660 + 12 * math.sin(lt * 10), 1, 0, min(1, lt * 5))))
    v.add(Fx(sticker("SAYGI", 46, YEL, BLACK, rot=-5), anahtar, ac, lambda lt: (130 + 330 * ease(lt / .9), 790, 1, 0, min(1, lt * 5))))
    v.sfx.append((anahtar, "swish")); v.sfx.append((ac, "ding")); v.shake(ac + .1, 20)
    v.add(Img(emoji_img("❤", 200), W / 2 + 40, 650, ac + .25, t8, "pop", pulse=.14)); v.add(Particles(ac + .3, W / 2, 620, "confetti", 70, seed=3, spread=.8))
    v.cap("Kalbi kocamandır. ❤", {"kocamandır."}, 1130, z(25.36), b, size=72, times=spread([(z(25.36), z(26.34), 2)]))
    v.cap("Ama onu kazanmak için,", {"kazanmak"}, 1110, z(26.85), t8, size=66, times=spread([(z(26.85), z(28.04), 4)]), maxw=960)
    v.cap("önce saygısını kazanman gerekir.", {"saygısını"}, 1300, z(28.24), t8, size=50, times=spread([(z(28.24), z(29.77), 4)]), maxw=1000)

    # ---- kapanış: "Tanıdık geldi mi? Bir Aslan kadınını etiketle, bu videoyu da kaydet."
    v.cut(t8)
    v.add(Glow(PINK, W / 2, 700, 640, t8, T, .45, nabiz=.1))
    v.add(Img(medallion("Aslan", "♀", 190), W / 2, 420, t8, T, "spin", bob=8))
    for k in range(2): v.add(Yorunge(emoji_img("🦁", 84), W / 2, 420, 250, 90, t8 + .2, T, 2.6, k * 3.1416))
    v.slam(sticker("Tanıdık geldi mi? 👀", 74, WHITE, BLACK, rot=-4, maxw=960), W / 2, 700, z(30.42) - .12, T, power=.07, sound="hit")
    v.cap("Bir Aslan kadınını etiketle 👇", {"etiketle"}, 980, z(31.59), T, size=76, times=spread([(z(31.59), z(33.19), 4)]), maxw=940)
    v.slam(sticker("bu videoyu da kaydet 📌", 54, YEL, BLACK, rot=3), W / 2, 1230, z(33.39) - .1, T, power=.05, sound="pop")
    return v
