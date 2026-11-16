import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from engine import *
from yardimci import big, spread, soften, ses

SU, TOP = EL["Su"], EL["Toprak"]

def video():
    T = 47.6
    v = Video(T, [SU, TOP], 71)
    v.voice = ses("akrep_erkek_x_basak_kadin")
    # A hook
    v.add(Img(medallion("Akrep", "♂", 280), W / 2 - 230, 640, 0.0, 6.25, "path", dur=.5, frm=(-300, 640), bob=8))
    v.add(Img(medallion("Başak", "♀", 280), W / 2 + 230, 640, 0.0, 6.25, "path", dur=.5, frm=(W + 300, 640), bob=-8))
    v.sfx.append((0.0, "whoosh"))
    v.add(Img(emoji_img("❤", 150), W / 2, 640, .5, 6.25, "pop", pulse=.14)); v.add(Shock(.55, W / 2, 640, PINK, 60, 500, .5, 16))
    for t in (.6, 1.5, 2.4): v.sfx.append((t, "heart"))
    v.punch.append((.6, .07))
    v.cap("Akrep erkeği + Başak kadını", {"Akrep", "Başak"}, 930, .25, 6.25, size=76, times=spread([(.25, 1.93, 5)]))
    v.cap("Dışarıdan sakin görünürler ama aralarında çok derin bir bağ var 🔥", {"sakin", "derin"}, 1210, 2.37, 6.25, size=58,
          times=spread([(2.37, 3.82, 3), (4.03, 5.93, 7)]), maxw=960)
    v.cut(6.25)
    # B score
    v.cap("Peki aşk uyumları kaç?", {"aşk"}, 400, 6.38, 9.45, size=78, times=[6.38] + spread([(6.90, 7.86, 3)]), emph=False)
    t0, dur = 6.95, 1.8; v.add(Ring(90, "AŞK UYUMU", PINK, 870, t0, 9.45, dur))
    for k in range(2, 91, 3):
        q = k / 90; p = 1 - (1 - q) ** (1 / 2.2); v.sfx.append((t0 + p * dur, "tick"))
    te = t0 + dur
    v.sfx += [(te, "hit"), (te, "ding")]; v.punch.append((te, .12)); v.flashes.append((te, 130)); v.shake(te, 26)
    v.ducks.append((6.85, te)); v.sfx.append((te - 1.6, "riser")); v.add(Shock(te, W / 2, 870, PINK, 200, 700, .6, 20))
    v.add(Particles(te, W / 2, 870, "hearts", 34, seed=4)); v.add(Particles(te, W / 2, 870, "confetti", 70, seed=6))
    v.slam(sticker("Çok yüksek! 🔥", 64, YEL, BLACK, rot=3), W / 2, 1320, 8.85, 9.45, power=.05, sound="pop", flash=False)
    v.cut(9.45)
    # C why
    v.cap("Neden mi? 🤔", set(), 400, 9.54, 18.2, size=80, times=[9.54, 9.8], emph=False)
    v.pop(medallion("Akrep", "♂", 240), W / 2 - 215, 640, 10.3, 18.2, bob=6)
    v.slam(sticker("Sadakat ister 🔒", 40, WHITE, BLACK, rot=-4, maxw=420), W / 2 - 240, 850, 10.85, 18.2, power=.05, sound="thud")
    v.pop(medallion("Başak", "♀", 240), W / 2 + 215, 640, 12.1, 18.2, bob=-6)
    v.slam(sticker("Sözünün eri 🤝", 40, YEL, BLACK, rot=4, maxw=420), W / 2 + 240, 850, 12.6, 18.2, power=.05, sound="thud")
    v.cap("Biri sezer, diğeri çözer.", {"sezer,", "çözer."}, 1080, 13.74, 18.2, size=76, times=spread([(13.74, 14.56, 2), (14.69, 15.47, 2)]))
    v.cap("İkisi de yüzeysel ilişkilerden nefret eder.", {"nefret"}, 1300, 15.78, 18.2, size=58, times=spread([(15.78, 17.92, 6)]))
    v.cut(18.2)
    # D1 problem
    v.slam(sticker("Ama bir sorun var... 👀", 60, WHITE, BLACK, rot=-2), W / 2, 420, 18.30, 24.75, power=.07, sound="hit")
    v.cap("İkisi de duygularını kolay açmaz.", {"açmaz."}, 690, 19.56, 24.75, size=72, times=spread([(19.56, 21.29, 5)]))
    v.cap("Akrep içine kapanır,", {"kapanır,"}, 930, 21.62, 24.75, size=76, times=spread([(21.62, 22.76, 3)]))
    v.cap("Başak her şeyi analiz eder. 🧐", {"analiz"}, 1140, 22.91, 24.75, size=76, times=[22.91] + spread([(23.37, 24.39, 4)]))
    v.cut(24.75)
    # D2 chat (POV: Akrep)
    msgs = [("L", "Bugün neden bu kadar sessizsin?", 24.85, 25.79), ("R", "Bir şey yok.", 27.35, 28.19),
            ("L", "O \"bir şey yok\"u üç farklı şekilde analiz ettim 🧐", 28.75, 29.61)]
    v.add(Chat("Başak 🌾", medallion("Başak", "♀", 120), msgs, 430, 24.75, 32.3))
    for side, txt, ty, tm in msgs: v.sfx += [(ty, "type"), (tm, "msg")]
    v.punch.append((28.19, .04))
    v.shake(31.85, 24); v.punch.append((31.85, .06)); v.sfx.append((31.85, "hit"))
    v.add(Img(emoji_img("💀", 150), W - 170, 1330, 31.0, 32.3, "spin")); v.sfx.append((31.0, "pop"))
    v.cut(32.3)
    # E bars
    v.cap("Puanlar 👇", set(), 400, 32.32, 37.75, size=84, emph=False)
    for k, (lab, pct, col, t) in enumerate([("Tutku", 90, RED, 32.40), ("Güven", 85, TOP, 33.41), ("Sadakat", 95, SU, 34.41), ("İletişim", 60, PINK, 36.2)]):
        v.add(Bars([(lab, pct, col)], 610 + k * 175, t, 37.75)); v.sfx.append((t, "pop"))
    v.pop(emoji_img("😬", 90), 430, 610 + 3 * 175, 36.9, 37.75, sound="thud"); v.shake(36.95, 12)
    v.cut(37.75)
    # F formula
    v.cap("Formül basit:", {"basit:"}, 480, 37.80, 43.95, size=92, times=[37.80, 38.15])
    v.pop(card("Akrep: kalbini biraz aç ❤", accent=SU), W / 2, 770, 38.82, 43.95, sound="swish", anim="left")
    v.sfx.append((40.0, "thud")); v.punch.append((40.0, .04))
    v.pop(card("Başak: analiz etmeyi bırak, sadece sev 💛", accent=TOP), W / 2, 1010, 40.74, 43.95, sound="swish", anim="right")
    v.sfx.append((42.83, "thud")); v.punch.append((42.83, .05)); v.shake(42.85, 10)
    v.cut(43.95)
    # G CTA
    v.cap("Bu çifti tanıyorsan etiketle 👇", {"etiketle"}, 820, 44.03, T, size=80, times=spread([(44.03, 45.63, 4)]))
    v.slam(sticker("videoyu da kaydet 📌", 56, YEL, BLACK, rot=3), W / 2, 1080, 45.81, T, power=.05, sound="pop")
    return v
