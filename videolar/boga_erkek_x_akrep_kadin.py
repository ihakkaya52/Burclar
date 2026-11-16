import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
import engine
from engine import *
from yardimci import big, spread, soften, ses

SU, TOP = EL["Su"], EL["Toprak"]

def video():
    engine.Caption.KW_AMP = .45
    T = 46.1
    v = Video(T, [TOP, SU], 149)
    v.voice = ses("boga_erkek_x_akrep_kadin")
    # A hook
    v.add(Img(medallion("Boğa", "♂", 280), W / 2 - 230, 640, 0.0, 8.2, "path", dur=.5, frm=(-300, 640), bob=8))
    v.add(Img(medallion("Akrep", "♀", 280), W / 2 + 230, 640, 0.0, 8.2, "path", dur=.5, frm=(W + 300, 640), bob=-8))
    v.sfx.append((0.0, "whoosh"))
    v.add(Img(emoji_img("❤", 150), W / 2, 640, .5, 8.2, "pop", pulse=.12))
    for t in (.6, 1.5): v.sfx.append((t, "heart"))
    v.cap("Boğa erkeği + Akrep kadını", {"Boğa", "Akrep"}, 930, .18, 8.2, size=76, times=spread([(.18, 2.04, 5)]))
    v.cap("Zodyakta tam karşı karşıya duran iki burç.", {"karşıya"}, 1160, 2.56, 5.35, size=58, times=spread([(2.56, 5.02, 7)]), maxw=960)
    v.cap("Ama derler ya, zıtlar birbirini çeker 🧲", {"zıtlar"}, 1160, 5.39, 8.2, size=60, times=spread([(5.39, 7.81, 7)]), maxw=960)
    v.cut(8.2)
    # B score
    v.cap("Peki aşk uyumları kaç?", {"aşk"}, 400, 8.30, 11.48, size=78, times=spread([(8.30, 9.75, 4)]), emph=False)
    t0, dur = 8.9, 1.95; v.add(Ring(80, "AŞK UYUMU", PINK, 880, t0, 11.48, dur))
    for k in range(2, 81, 3):
        q = k / 80; p = 1 - (1 - q) ** (1 / 2.2); v.sfx.append((t0 + p * dur, "tick"))
    te = t0 + dur
    v.sfx += [(te, "hit"), (te, "ding")]; v.punch.append((te, .1)); v.flashes.append((te, 100)); v.shake(te, 20)
    v.ducks.append((8.8, te)); v.sfx.append((te - 1.6, "riser"))
    v.add(Particles(te, W / 2, 880, "hearts", 26, seed=4))
    v.cut(11.48)
    # C why
    v.cap("Neden mi? 🤔", set(), 400, 11.58, 18.15, size=80, times=[11.58, 11.8], emph=False)
    v.pop(medallion("Boğa", "♂", 240), W / 2 - 240, 640, 12.53, 18.15, bob=6)
    v.pop(sticker("Güven verir 🤝", 40, WHITE, BLACK, rot=-4, maxw=420), W / 2 - 240, 850, 13.3, 18.15, sound="thud")
    v.pop(medallion("Akrep", "♀", 240), W / 2 + 240, 640, 14.2, 18.15, bob=-6)
    v.pop(sticker("Tutku katar 🔥", 40, YEL, BLACK, rot=4, maxw=420), W / 2 + 240, 850, 14.8, 18.15, sound="thud")
    v.cap("İkisi de sadık, ikisi de ciddi.", {"sadık,", "ciddi."}, 1150, 15.79, 18.15, size=70, times=spread([(15.79, 16.70, 3), (16.97, 17.82, 3)]))
    v.cut(18.15)
    # D1 problem
    v.pop(sticker("Ama bir sorun var... 👀", 60, WHITE, BLACK, rot=-2), W / 2, 420, 18.23, 22.4, sound="hit")
    v.cap("İkisi de inatçı,", {"inatçı,"}, 760, 19.48, 22.4, size=86, times=spread([(19.48, 20.51, 3)]))
    v.cap("ikisi de kıskanç. 😒", {"kıskanç."}, 990, 20.83, 22.4, size=86, times=spread([(20.83, 21.85, 3)]))
    v.cut(22.4)
    # D2 chat (POV: Boğa)
    msgs = [("L", "Neden yazmadın?", 22.6, 23.94), ("R", "Yemek yiyordum 🍝", 25.15, 25.83),
            ("L", "Üç saat boyunca mı? 🤨", 26.96, 27.61), ("R", "Tatlı da vardı 🍰", 28.96, 29.60)]
    v.add(Chat("Akrep 🦂", medallion("Akrep", "♀", 120), msgs, 430, 22.4, 30.8))
    for side, txt, ty, tm in msgs: v.sfx += [(ty, "type"), (tm, "msg")]
    v.add(Img(emoji_img("😂", 140), W - 170, 1330, 30.0, 30.8, "spin")); v.sfx.append((30.0, "thud")); v.shake(30.05, 14)
    v.cut(30.8)
    # E bars
    v.cap("Puanlar 👇", set(), 400, 30.82, 36.5, size=84, emph=False)
    for k, (lab, pct, col, t) in enumerate([("Tutku", 90, RED, 30.91), ("Sadakat", 90, SU, 31.88), ("Güven", 85, TOP, 32.85), ("İnat", 100, (255, 140, 0), 34.6)]):
        v.add(Bars([(lab, pct, col)], 610 + k * 175, t, 36.5)); v.sfx.append((t, "pop"))
    v.pop(emoji_img("😤", 80), 330, 610 + 3 * 175, 35.5, 36.5, sound="thud")
    v.cut(36.5)
    # F formula
    v.cap("Formül basit:", {"basit:"}, 480, 36.55, 42.1, size=92, times=[36.55, 36.95])
    v.pop(card("Boğa: ona her şeyi anlat 💬", accent=TOP), W / 2, 770, 37.71, 42.1, sound="swish", anim="left")
    v.pop(card("Akrep: ona biraz alan bırak 🕊", accent=SU), W / 2, 1010, 39.84, 42.1, sound="swish", anim="right")
    v.cut(42.1)
    # G CTA
    v.cap("Bu çifti tanıyorsan etiketle 👇", {"etiketle"}, 820, 42.17, T, size=80, times=spread([(42.17, 43.89, 4)]))
    v.pop(sticker("videoyu da kaydet 📌", 56, YEL, BLACK, rot=3), W / 2, 1080, 44.14, T)
    soften(v)
    return v
