import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from engine import *
from yardimci import big, spread, soften, ses

HAVA, ATES = EL["Hava"], EL["Ateş"]

def video():
    T = 41.4
    v = Video(T, [HAVA, ATES], 59)
    v.voice = ses("ikizler_erkek_x_aslan_kadin")
    # A hook
    v.add(Img(medallion("İkizler", "♂", 280), W / 2 - 230, 640, 0.0, 5.9, "path", dur=.5, frm=(-300, 640), bob=8))
    v.add(Img(medallion("Aslan", "♀", 280), W / 2 + 230, 640, 0.0, 5.9, "path", dur=.5, frm=(W + 300, 640), bob=-8))
    v.sfx.append((0.0, "whoosh"))
    v.add(Img(emoji_img("❤", 150), W / 2, 640, .5, 5.9, "pop", pulse=.14)); v.add(Shock(.55, W / 2, 640, PINK, 60, 500, .5, 16))
    for t in (.6, 1.5, 2.4): v.sfx.append((t, "heart"))
    v.punch.append((.6, .07))
    v.cap("İkizler erkeği + Aslan kadını", {"İkizler", "Aslan"}, 940, .23, 5.9, size=76, times=spread([(.23, 2.28, 5)]))
    v.cap("Bu ilişki ya çok iyi gider, ya da çok gürültülü biter 🔥", {"iyi", "gürültülü"}, 1190, 2.67, 5.9, size=58,
          times=spread([(2.67, 4.27, 6), (4.39, 5.52, 5)]), maxw=980)
    v.cut(5.9)
    # B score
    v.cap("Peki aşk uyumları kaç?", {"aşk"}, 400, 6.02, 9.25, size=78, times=spread([(6.02, 6.38, 1), (6.51, 7.43, 3)]), emph=False)
    ring = Ring(85, "AŞK UYUMU", PINK, 870, 6.6, 9.25, 1.85); v.add(ring)
    for k in range(2, 86, 3):
        q = k / 85; p = 1 - (1 - q) ** (1 / 2.2); v.sfx.append((6.6 + p * 1.85, "tick"))
    te = 6.6 + 1.85
    v.sfx += [(te, "hit"), (te, "ding")]; v.punch.append((te, .12)); v.flashes.append((te, 130)); v.shake(te, 26)
    v.ducks.append((6.5, te)); v.sfx.append((te - 1.6, "riser"))
    v.add(Shock(te, W / 2, 870, PINK, 200, 700, .6, 20))
    v.add(Particles(te, W / 2, 870, "hearts", 34, seed=4)); v.add(Particles(te, W / 2, 870, "confetti", 70, seed=6))
    v.slam(sticker("Çok yüksek! 🔥", 64, YEL, BLACK, rot=3), W / 2, 1320, 8.6, 9.25, power=.05, sound="pop", flash=False)
    v.cut(9.25)
    # C why
    v.cap("Neden mi? 🤔", set(), 400, 9.36, 14.15, size=80, times=[9.36, 9.6], emph=False)
    v.pop(medallion("İkizler", "♂", 250), W / 2 - 215, 680, 10.2, 14.15, bob=6)
    v.slam(sticker("O güldürür 😂", 48, WHITE, BLACK, rot=-4, maxw=380), W / 2 - 215, 900, 10.55, 14.15, power=.05, sound="thud")
    v.pop(medallion("Aslan", "♀", 250), W / 2 + 215, 680, 11.2, 14.15, bob=-6)
    v.slam(sticker("O parlar ✨", 48, YEL, BLACK, rot=4, maxw=380), W / 2 + 215, 900, 11.5, 14.15, power=.05, sound="thud")
    v.cap("Birlikte asla sıkılmazlar.", {"asla"}, 1170, 12.32, 14.15, size=76, times=spread([(12.32, 13.83, 3)]))
    v.cut(14.15)
    # D1 the problem
    v.slam(sticker("Ama bir sorun var... 👀", 60, WHITE, BLACK, rot=-2), W / 2, 420, 14.27, 19.45, power=.07, sound="hit")
    v.cap("Aslan kadını ilgi ister,", {"ilgi"}, 770, 15.82, 19.45, size=80, times=spread([(15.82, 17.12, 4)]))
    v.cap("İkizler'in aklı ise hep başka yerde. 🙄", {"başka"}, 1030, 17.42, 19.45, size=72, times=spread([(17.42, 19.22, 6)]))
    v.cut(19.45)
    # D2 chat
    msgs = [("L", "Beni hiç övmüyorsun 🙄", 19.6, 20.38), ("R", "Dün saçını beğendim ya?", 21.8, 22.58),
            ("L", "Dün dündü.", 24.4, 25.28)]
    v.add(Chat("Aslan 🦁", medallion("Aslan", "♀", 120), msgs, 430, 19.45, 26.3))
    for side, txt, ty, tm in msgs: v.sfx += [(ty, "type"), (tm, "msg")]
    v.shake(25.33, 26); v.punch.append((25.33, .07)); v.sfx.append((25.33, "hit"))
    v.add(Img(emoji_img("💀", 150), W - 170, 1330, 25.6, 26.3, "spin")); v.sfx.append((25.6, "pop"))
    v.cut(26.3)
    # E bars
    v.cap("Puanlar 👇", set(), 400, 26.35, 31.6, size=84, emph=False)
    for k, (lab, pct, col, t) in enumerate([("Tutku", 85, ATES, 26.42), ("Eğlence", 95, YEL, 27.4), ("İletişim", 85, HAVA, 28.36), ("Güven", 65, PINK, 29.9)]):
        v.add(Bars([(lab, pct, col)], 610 + k * 175, t, 31.6)); v.sfx.append((t, "pop"))
    v.pop(emoji_img("😬", 90), 420, 610 + 3 * 175, 30.5, 31.6, sound="thud"); v.shake(30.55, 12)
    v.cut(31.6)
    # F formula
    v.cap("Formül basit:", {"basit:"}, 480, 31.72, 37.5, size=92, times=[31.72, 32.05])
    v.pop(card("İkizler: iltifatı asla eksik etme 💬", accent=BLUE), W / 2, 770, 32.72, 37.5, sound="swish", anim="left")
    v.sfx.append((33.6, "thud")); v.punch.append((33.6, .04))
    v.pop(card("Aslan: ona nefes alacak alan bırak 🕊", accent=ATES), W / 2, 1010, 35.26, 37.5, sound="swish", anim="right")
    v.sfx.append((36.1, "thud")); v.punch.append((36.1, .04))
    v.cut(37.5)
    # G CTA
    v.cap("Bu çifti tanıyorsan etiketle 👇", {"etiketle"}, 820, 37.63, T, size=80, times=spread([(37.63, 39.21, 4)]))
    v.slam(sticker("videoyu da kaydet 📌", 56, YEL, BLACK, rot=3), W / 2, 1080, 39.41, T, power=.05, sound="pop")
    return v
