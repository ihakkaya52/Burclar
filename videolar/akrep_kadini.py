import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from engine import *
from yardimci import big, spread, ses, zaman
from sahne import *

SU = EL["Su"]; MAVI = (0, 132, 255); GRI = (58, 58, 72)

def video():
    z = zaman("akrep_kadini")          # mp3 saniyesi -> video saniyesi
    T = z(35.36) + .6
    v = Video(T, [SU, (190, 50, 130)], 131)
    v.voice = ses("akrep_kadini")
    c = lambda t: z(t) - .12           # sahne kesmeleri kelimeden hemen önce

    # ---- giriş: "23 Ekim ile 21 Kasım arasında doğan bir kadın mı var hayatında?"
    t1 = c(4.35)
    v.add(Glow((220, 60, 120), W / 2, 680, 620, 0, t1, .5))
    takvim_giris(v, z(.05), z(1.10), z(2.05), t1)
    v.cap("23 Ekim – 21 Kasım", {"23", "21"}, 1165, z(.02), t1, size=88, times=[z(.02), z(.48), z(.85), z(1.08), z(1.54)])
    v.cap("arasında doğan bir kadın mı var hayatında? 👀", {"kadın"}, 1335, z(1.85), t1, size=56,
          times=spread([(z(1.85), z(2.40), 1), (z(2.40), z(3.95), 6)]), maxw=900)
    v.slam(sticker("KADIN ♀", 50, PINK, WHITE, rot=6), 850, 1010, z(2.80), t1, power=.06, sound="hit")

    # ---- "O bir Akrep."
    v.cut(t1); t2 = c(5.37)
    v.add(Glow(PINK, W / 2, 620, 640, t1, t2, .55, nabiz=.12))
    v.add(Img(medallion("Akrep", "♀", 320), W / 2, 520, t1, t2, "spin", bob=8)); v.sfx.append((t1, "swish"))
    for k in range(3): v.add(Yorunge(emoji_img("🦂", 96), W / 2, 520, 330, 150, t1 + .15, t2, 3.2, k * 2.094))
    v.cap("O bir", set(), 860, z(4.35), t2, size=70, times=[z(4.35), z(4.48)], emph=False)
    v.slam(big("AKREP", 250, YEL), W / 2, 1060, z(4.62) - .12, t2, power=.15, sound="boom"); v.shake(z(4.65), 30)

    # ---- "Ve onu tanımak istiyorsan, şu beş şeyi bil."
    v.cut(t2); t3 = c(8.20)
    v.cap("Ve onu tanımak istiyorsan,", {"tanımak"}, 520, z(5.37), t3, size=70, times=spread([(z(5.37), z(6.66), 4)]), maxw=960)
    for k, n in enumerate((5, 4, 3, 2, 1)):
        tk = z(6.84) + k * .11
        v.add(Img(big(str(n), 190, YEL, 10), 180 + k * 180, 780 + (-22 if k % 2 else 22), tk, t3, "drop", bob=7)); v.sfx.append((tk + .3, "tick"))
    v.slam(sticker("şu 5 şeyi bil 👇", 80, PINK, WHITE, rot=-4, maxw=960), W / 2, 1120, z(6.84) - .12, t3, power=.1, sound="boom"); v.shake(z(6.9), 26)

    # ---- 5: "Ona yalan söyleme. Sen cümleni bitirmeden anlar."
    v.cut(t3); t4 = c(12.27); a = t3 + .75; yak = z(10.95)
    sayi(v, 5, t3, t4, 170, 420, bekle=.6)
    v.add(Glow((230, 60, 50), W / 2, 640, 580, yak, t4, .55, nabiz=.15))
    v.add(Img(emoji_img("🤥", 180), 760, 470, a, yak, "pop", bob=9)); v.sfx.append((a, "pop"))
    v.add(Yazi("aslında dün gece arkadaşlarla", W / 2, 700, a, t4, z(9.0), z(11.6), mod="yaz", size=50, bg=MAVI, kuyruk="r"))
    v.sfx += [(z(9.0), "type"), (z(9.9), "type")]
    v.slam(sticker("YALAN 🚨", 96, RED, WHITE, rot=-9), W / 2, 700, yak - .12, t4, power=.13, sound="boom"); v.shake(yak, 34)
    v.add(Img(emoji_img("🧐", 180), 760, 470, yak, t4, "spin", bob=9))
    v.cap("Ona yalan söyleme.", {"yalan"}, 1080, z(8.96), t4, size=84, times=spread([(z(8.96), z(9.98), 3)]))
    v.cap("Sen cümleni bitirmeden anlar.", {"bitirmeden"}, 1290, z(10.29), t4, size=52, times=spread([(z(10.29), z(11.75), 4)]), maxw=940)

    # ---- 4: "Dışarıdan soğuk görünür… ama içinde fırtınalar kopar."
    v.cut(t4); t5 = c(16.52); a = t4 + .65; f = z(14.58) - .12
    sayi(v, 4, t4, t5, 910, 420, bekle=.55)
    v.add(Glow((90, 190, 255), W / 2, 640, 600, a, f, .6))
    v.add(Img(emoji_img("🧊", 240), W / 2, 620, a, f, "pop", bob=10)); v.sfx.append((a, "pop"))
    v.add(Yagis("kar", a, f, (120, 330, 960, 940), 22, seed=2))
    v.cut(f)
    v.add(Glow((170, 60, 230), W / 2, 640, 640, f, t5, .7, nabiz=.2))
    v.add(Fx(emoji_img("🌪", 260), f, t5, lambda lt: (W / 2 + 40 * math.sin(lt * 7), 620, min(1, .3 + lt * 4), 10 * math.sin(lt * 9), min(1, lt * 6))))
    v.add(Yagis("yagmur", f, t5, (100, 320, 980, 960), 40, seed=5))
    for k, (ts, x0, x1) in enumerate(((15.0, 260, 330), (15.32, 840, 760), (15.62, 420, 300))):
        v.add(Simsek(z(ts), x0, 320, x1, 900, seed=k + 3)); v.flashes.append((z(ts), 120)); v.shake(z(ts), 30); v.sfx.append((z(ts) - .03, "boom" if k == 0 else "hit"))
    v.cap("Dışarıdan soğuk görünür…", {"soğuk"}, 1090, z(12.97), f, size=76, times=spread([(z(12.97), z(14.12), 3)]), maxw=960)
    v.cap("ama içinde fırtınalar kopar. ⚡", {"fırtınalar"}, 1090, z(14.58), t5, size=76, times=spread([(z(14.58), z(15.77), 4)]), maxw=900)

    # ---- 3: "Herkese kapısını açmaz. Sana açtıysa, sen özelsin."
    v.cut(t5); t6 = c(21.05); a = t5 + .6; ac = z(18.85)
    sayi(v, 3, t5, t6, 170, 400, bekle=.5)
    v.add(Glow((255, 200, 90), 740, 650, 520, ac, t6, .7, nabiz=.1))
    v.add(Kapi(740, 660, 320, 480, a, t6, 0.0, [(ac, 1.0, .35)]))
    for k, (ad, ts) in enumerate((("eski sevgili ❌", 17.25), ("iş arkadaşı ❌", 17.65), ("komşu teyze ❌", 18.05))):
        v.add(Img(sticker(ad, 40, (30, 30, 46), WHITE, rot=(-3, 2, -2)[k], maxw=460), 300, 560 + k * 120, z(ts), ac + .3, "left")); v.sfx.append((z(ts), "tick"))
    v.sfx.append((ac, "whoosh")); v.sfx.append((ac + .3, "ding"))
    v.slam(sticker("SEN 👑", 84, YEL, BLACK, rot=-6), 300, 660, z(19.90) - .12, t6, power=.1, sound="hit")
    v.add(Particles(z(19.95), 740, 660, "confetti", 60, seed=8, spread=.7))
    v.cap("Herkese kapısını açmaz.", {"açmaz."}, 1090, z(17.18), t6, size=78, times=spread([(z(17.18), z(18.57), 3)]), maxw=960)
    v.cap("Sana açtıysa, sen özelsin. ✨", {"özelsin."}, 1290, z(18.85), t6, size=60, times=spread([(z(18.85), z(19.73), 2), (z(19.90), z(20.59), 2)]), maxw=940)

    # ---- 2: "Onu kırarsan, belki affeder… ama asla unutmaz."
    v.cut(t6); t7 = c(25.53); a = t6 + .6; af = z(22.74) - .12; un = z(23.87) - .12
    sayi(v, 2, t6, t7, 910, 420, bekle=.5)
    v.add(Img(emoji_img("💔", 230), W / 2, 620, z(21.75), af, "pop", bob=9)); v.sfx.append((z(21.75), "pop"))
    v.add(Glow(GREEN, W / 2, 640, 560, af, un, .5))
    v.slam(sticker("AFFEDİLDİ ✅", 84, GREEN, WHITE, rot=-5), W / 2, 620, af, un, power=.09, sound="ding")
    v.add(Glow((230, 60, 50), W / 2, 660, 600, un, t7, .5, nabiz=.15))
    v.add(Img(dosya("📁 ARŞİV", ["14 Mart · saat 21.47", "“öyle demek istemedim”", "durum: asla silinmez"], "UNUTULMADI"), W / 2, 650, un, t7, "drop"))
    v.sfx.append((un + .35, "boom")); v.shake(un + .4, 30); v.punch.append((un + .4, .1))
    v.cap("Onu kırarsan,", {"kırarsan,"}, 1110, z(21.69), t7, size=70, times=spread([(z(21.69), z(22.47), 2)]))
    v.cap("belki affeder…", {"affeder…"}, 1220, z(22.74), un, size=70, times=spread([(z(22.74), z(23.49), 2)]))
    v.cap("ama asla unutmaz.", {"asla"}, 1270, z(23.87), t7, size=80, times=spread([(z(23.87), z(24.76), 3)]))

    # ---- "Ve bir numara…" (ardından 0,6 sn sessizlik)
    v.cut(t7); t8 = c(26.58)
    v.cap("Ve 1 numara...", {"1"}, 880, z(25.53), t8, size=110, gap=.3, times=[z(25.53), z(25.75), z(25.95)])
    v.ducks.append((t7, t8)); v.sfx.append((t8 - 1.5, "riser"))

    # ---- 1: "Sevdiğini sonuna kadar korur. Ama karşısına geçersen… geçmiş olsun."
    v.cut(t8); t9 = c(31.31); gel = z(28.56); son = z(30.29)
    sayi(v, 1, t8, t9, 170, 420, bekle=0, ses="boom")
    v.add(Glow(PINK, W / 2, 640, 600, t8, son, .6, nabiz=.15))
    v.add(Img(emoji_img("❤", 200), W / 2, 630, t8 + .1, t9, "pop", pulse=.14)); v.sfx += [(t8 + .2, "heart"), (t8 + 1.1, "heart")]
    for k in range(3): v.add(Yorunge(emoji_img("🦂", 110), W / 2, 630, 300, 170, t8 + .25, t9, 2.8, k * 2.094))
    v.add(Fx(emoji_img("😏", 150), gel, son, lambda lt: (1150 - 250 * ease(lt / 1.2), 380, 1, 0, 1)))
    v.add(Glow((230, 40, 40), W / 2, 640, 680, son, t9, .7, nabiz=.2))
    v.add(Img(emoji_img("💀", 170), 900, 380, son, t9, "spin")); v.sfx.append((son - .03, "boom")); v.shake(son, 40); v.punch.append((son, .14)); v.flashes.append((son, 110))
    v.cap("Sevdiğini sonuna kadar korur.", {"korur."}, 1080, z(26.58), gel - .1, size=74, times=spread([(z(26.58), z(28.14), 4)]), maxw=960)
    v.cap("Ama karşısına geçersen…", {"karşısına"}, 1060, z(28.56), t9, size=72, times=spread([(z(28.56), z(29.90), 3)]), maxw=960)
    v.slam(sticker("geçmiş olsun. 🫡", 84, RED, WHITE, rot=-4, maxw=960), W / 2, 1250, son - .12, t9, power=.1, sound="hit")

    # ---- kapanış: "Tanıdık geldi mi? Bir Akrep kadınını etiketle, bu videoyu da kaydet."
    v.cut(t9)
    v.add(Glow(PINK, W / 2, 700, 640, t9, T, .45, nabiz=.1))
    v.add(Img(medallion("Akrep", "♀", 190), W / 2, 420, t9, T, "spin", bob=8))
    for k in range(2): v.add(Yorunge(emoji_img("🦂", 80), W / 2, 420, 250, 90, t9 + .2, T, 2.6, k * 3.1416))
    v.slam(sticker("Tanıdık geldi mi? 👀", 74, WHITE, BLACK, rot=-4, maxw=960), W / 2, 700, z(31.31) - .12, T, power=.07, sound="hit")
    v.cap("Bir Akrep kadınını etiketle 👇", {"etiketle"}, 980, z(32.41), T, size=76, times=spread([(z(32.41), z(33.91), 4)]), maxw=940)
    v.slam(sticker("bu videoyu da kaydet 📌", 54, YEL, BLACK, rot=3), W / 2, 1230, z(34.10) - .1, T, power=.05, sound="pop")
    return v
