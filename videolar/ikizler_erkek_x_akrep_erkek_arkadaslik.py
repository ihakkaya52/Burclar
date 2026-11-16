import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from engine import *
from yardimci import big, spread, soften, ses

HAVA, SU = EL["Hava"], EL["Su"]

def video():
    T = 41.4
    v = Video(T, [HAVA, SU], 47)
    v.voice = ses("ikizler_erkek_x_akrep_erkek_arkadaslik")
    # A hook: collision
    v.add(Img(medallion("İkizler", "♂", 300), W / 2 - 175, 720, 0.0, 5.55, "path", dur=.45, frm=(-300, 720), bob=8))
    v.add(Img(medallion("Akrep", "♂", 300), W / 2 + 175, 720, 0.0, 5.55, "path", dur=.45, frm=(W + 300, 720), bob=-8))
    v.sfx += [(0.0, "whoosh"), (.42, "boom")]; v.shake(.45, 34); v.punch.append((.45, .1)); v.flashes.append((.45, 160))
    v.add(Particles(.45, W / 2, 720, "confetti", 60, seed=2, spread=.8)); v.add(Shock(.45, W / 2, 720, YEL, 60, 650, .5, 18))
    v.cap("Bir İkizler ile bir Akrep arkadaş olursa...", {"İkizler", "Akrep"}, 1050, .19, 5.55, size=72, times=spread([(.19, 2.87, 7)]))
    v.cap("ya kanka olurlar, ya düşman 💀", {"kanka", "düşman"}, 1300, 3.26, 5.55, size=68, times=spread([(3.26, 4.41, 3), (4.59, 5.20, 2)]))
    v.cut(5.55)
    # B score
    v.cap("Peki arkadaşlık uyumları kaç?", {"uyumları"}, 400, 5.66, 11.3, size=72, times=[5.66] + spread([(6.19, 7.53, 3)]), emph=False)
    t0, dur = 6.3, 2.15; v.add(Ring(60, "ARKADAŞLIK", YEL, 870, t0, 11.3, dur))
    for k in range(2, 61, 3):
        q = k / 60; p = 1 - (1 - q) ** (1 / 2.2); v.sfx.append((t0 + p * dur, "tick"))
    te = t0 + dur
    v.sfx += [(te, "hit"), (te, "ding")]; v.punch.append((te, .12)); v.flashes.append((te, 120)); v.shake(te, 22)
    v.ducks.append((6.2, te)); v.sfx.append((te - 1.6, "riser")); v.add(Shock(te, W / 2, 870, YEL, 200, 700, .6, 20))
    v.cap("Fena değil… ama 🤨", {"ama"}, 1320, 9.35, 11.3, size=68, times=[9.35, 9.65, 10.52])
    v.cut(11.3)
    # C good side
    v.slam(sticker("✅ İYİ TARAFI", 62, GREEN, WHITE, rot=-2), W / 2, 400, 11.46, 20.0, power=.07, sound="hit")
    for k, (txt, t) in enumerate([("Gece 3'te dertleşilecek ikili 🌙", 12.77), ("İkisi de dedektif kadar meraklı 🔍", 15.35),
                                  ("İkizler güldürür, Akrep dinler 😂", 17.57)]):
        v.pop(card(txt, accent=GREEN), W / 2, 660 + k * 230, t, 20.0, sound="swish", anim="left" if k % 2 == 0 else "right")
        v.punch.append((t + .3, .03))
    v.sfx.append((18.92, "thud")); v.shake(18.95, 10)
    v.cut(20.0)
    # D bad side + censor gag
    v.slam(sticker("🚩 KÖTÜ TARAFI", 62, RED, WHITE, rot=2), W / 2, 400, 20.16, 28.3, power=.07, sound="hit")
    v.cap("Akrep ona bir sır verir...", {"sır"}, 620, 21.66, 28.3, size=78, times=spread([(21.66, 23.11, 5)]))
    v.cap("İkizler de hemen...", {"hemen..."}, 810, 23.31, 28.3, size=78, times=spread([(23.31, 24.40, 3)]))
    v.add(Img(sticker("SANSÜRLENDİ 🤐", 70, BLACK, WHITE, rot=-3), W / 2, 975, 24.62, 28.3, "slam"))
    v.sfx += [(24.62, "beep"), (25.25, "beep")]; v.shake(24.7, 22); v.punch.append((24.7, .07)); v.flashes.append((24.7, 90))
    v.ducks.append((24.55, 25.95))
    v.slam(big("AKREP BUNU", 128, WHITE, 10), W / 2, 1180, 26.15, 28.3, power=.06)
    v.slam(big("10 YIL UNUTMAZ", 128, RED, 10), W / 2, 1345, 26.95, 28.3, power=.14, sound="boom"); v.shake(27.1, 32)
    v.add(Img(emoji_img("💀", 120), W - 150, 1180, 27.4, 28.3, "spin")); v.sfx.append((27.4, "pop"))
    v.cut(28.3)
    # E bars
    v.cap("Puanlar 👇", set(), 400, 28.35, 33.6, size=84, emph=False)
    for k, (lab, pct, col, t) in enumerate([("Eğlence", 75, HAVA, 28.45), ("Sohbet", 85, HAVA, 29.45), ("Güven", 40, RED, 31.1), ("Sadakat", 50, SU, 32.17)]):
        v.add(Bars([(lab, pct, col)], 610 + k * 175, t, 33.6)); v.sfx.append((t, "pop"))
    v.pop(emoji_img("😬", 90), 400, 610 + 2 * 175, 31.75, 33.6, sound="thud"); v.shake(31.8, 12)
    v.cut(33.6)
    # F verdict
    v.cap("Kısacası:", set(), 430, 33.77, 37.8, size=70, times=[33.77], emph=False)
    v.cap("İkizler ağzını sıkı tutarsa...", {"sıkı"}, 640, 34.61, 37.8, size=80, times=spread([(34.61, 36.42, 4)]))
    v.slam(big("ÖMÜRLÜK", 210, YEL), W / 2, 975, 36.5, 37.8, power=.14, sound="boom")
    v.slam(big("KANKA", 210, WHITE), W / 2, 1205, 36.95, 37.8, power=.08)
    v.add(Particles(37.0, W / 2, 1000, "confetti", 120, seed=9)); v.shake(37.0, 26); v.sfx.append((37.0, "ding"))
    v.cut(37.8)
    # G CTA
    v.cap("Akrep kankanı etiketle 👇", {"etiketle"}, 820, 37.90, T, size=84, times=spread([(37.90, 39.32, 3)]))
    v.slam(sticker("videoyu da kaydet 📌", 56, YEL, BLACK, rot=3), W / 2, 1080, 39.45, T, power=.05, sound="pop")
    return v
