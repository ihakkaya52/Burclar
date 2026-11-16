import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
import engine
from engine import *
from yardimci import big, spread, soften, ses

SU, TOP = EL["Su"], EL["Toprak"]

def video():
    engine.Caption.KW_AMP = .45
    T = 46.9
    v = Video(T, [TOP, SU], 163)
    v.voice = ses("boga_erkek_x_balik_kadin")
    # A hook
    v.add(Img(medallion("Boğa", "♂", 280), W / 2 - 230, 640, 0.0, 6.75, "path", dur=.5, frm=(-300, 640), bob=8))
    v.add(Img(medallion("Balık", "♀", 280), W / 2 + 230, 640, 0.0, 6.75, "path", dur=.5, frm=(W + 300, 640), bob=-8))
    v.sfx.append((0.0, "whoosh"))
    v.add(Img(emoji_img("❤", 150), W / 2, 640, .5, 6.75, "pop", pulse=.12))
    for t in (.6, 1.5): v.sfx.append((t, "heart"))
    v.cap("Boğa erkeği + Balık kadını", {"Boğa", "Balık"}, 930, .18, 6.75, size=76, times=spread([(.18, 1.78, 5)]))
    v.cap("Biri ayakları yere basan bir gerçekçi 🌍", {"gerçekçi"}, 1130, 2.16, 6.75, size=56, times=spread([(2.16, 4.2, 6)]), maxw=980)
    v.cap("diğeri bulutların üstünde bir hayalperest ☁", {"hayalperest"}, 1290, 4.35, 6.75, size=56, times=spread([(4.35, 6.47, 5)]), maxw=980)
    v.cut(6.75)
    # B score
    v.cap("Peki aşk uyumları kaç?", {"aşk"}, 400, 6.83, 10.08, size=78, times=spread([(6.83, 8.33, 4)]), emph=False)
    t0, dur = 7.4, 2.0; v.add(Ring(90, "AŞK UYUMU", PINK, 880, t0, 10.08, dur))
    for k in range(2, 91, 3):
        q = k / 90; p = 1 - (1 - q) ** (1 / 2.2); v.sfx.append((t0 + p * dur, "tick"))
    te = t0 + dur
    v.sfx += [(te, "hit"), (te, "ding")]; v.punch.append((te, .1)); v.flashes.append((te, 100)); v.shake(te, 20)
    v.ducks.append((7.3, te)); v.sfx.append((te - 1.6, "riser"))
    v.add(Particles(te, W / 2, 880, "hearts", 26, seed=4))
    v.cut(10.08)
    # C why
    v.cap("Neden mi? 🤔", set(), 400, 10.16, 17.5, size=80, times=[10.16, 10.4], emph=False)
    v.pop(medallion("Boğa", "♂", 240), W / 2 - 240, 640, 11.02, 17.5, bob=6)
    v.pop(sticker("Güvenli liman ⚓", 40, WHITE, BLACK, rot=-4, maxw=420), W / 2 - 240, 850, 12.3, 17.5, sound="thud")
    v.pop(medallion("Balık", "♀", 240), W / 2 + 240, 640, 13.0, 17.5, bob=-6)
    v.pop(sticker("Renk katar 🎨", 40, YEL, BLACK, rot=4, maxw=420), W / 2 + 240, 850, 14.2, 17.5, sound="thud")
    v.cap("İkisi de romantik, ikisi de sadık.", {"romantik,", "sadık."}, 1150, 15.23, 17.5, size=70, times=spread([(15.23, 16.25, 3), (16.35, 17.33, 3)]))
    v.cut(17.5)
    # D1 problem
    v.pop(sticker("Ama bir sorun var... 👀", 60, WHITE, BLACK, rot=-2), W / 2, 420, 17.59, 22.45, sound="hit")
    v.cap("Balık hayallerde yaşar, ☁", {"hayallerde"}, 760, 18.86, 22.45, size=76, times=spread([(18.86, 20.07, 3)]))
    v.cap("Boğa ise sadece bugünü düşünür. 🍲", {"bugünü"}, 990, 20.34, 22.45, size=72, times=spread([(20.34, 22.09, 5)]))
    v.cut(22.45)
    # D2 chat (POV: Boğa)
    msgs = [("L", "Sence geçmiş hayatta da tanışmış mıydık? ✨", 22.55, 23.79), ("R", "Bilmem. Akşam ne yiyoruz?", 26.24, 26.88),
            ("L", "...", 28.72, 29.4), ("R", "Mantı mı yapsak? 🥟", 30.44, 31.13)]
    v.add(Chat("Balık 🐟", medallion("Balık", "♀", 120), msgs, 430, 22.45, 32.2))
    for side, txt, ty, tm in msgs: v.sfx += [(ty, "type"), (tm, "msg")]
    v.add(Img(emoji_img("😂", 140), W - 170, 1330, 31.6, 32.2, "spin")); v.sfx.append((31.6, "thud")); v.shake(31.65, 14)
    v.cut(32.2)
    # E bars
    v.cap("Puanlar 👇", set(), 400, 32.22, 37.7, size=84, emph=False)
    for k, (lab, pct, col, t) in enumerate([("Romantizm", 95, PINK, 32.29), ("Sadakat", 90, SU, 33.65), ("Güven", 85, TOP, 34.55), ("Ortak dil", 45, (255, 140, 0), 36.2)]):
        v.add(Bars([(lab, pct, col)], 610 + k * 175, t, 37.7)); v.sfx.append((t, "pop"))
    v.pop(emoji_img("😅", 80), 450, 610 + 3 * 175, 36.9, 37.7, sound="thud")
    v.cut(37.7)
    # F formula
    v.cap("Formül basit:", {"basit:"}, 480, 37.76, 43.0, size=92, times=[37.76, 38.1])
    v.pop(card("Boğa: onun hayallerine eşlik et ✨", accent=TOP), W / 2, 770, 38.76, 43.0, sound="swish", anim="left")
    v.pop(card("Balık: onun pratikliğini küçümseme 🙏", accent=SU), W / 2, 1010, 40.88, 43.0, sound="swish", anim="right")
    v.cut(43.0)
    # G CTA
    v.cap("Bu çifti tanıyorsan etiketle 👇", {"etiketle"}, 820, 43.09, T, size=80, times=spread([(43.09, 44.6, 4)]))
    v.pop(sticker("videoyu da kaydet 📌", 56, YEL, BLACK, rot=3), W / 2, 1080, 44.75, T)
    soften(v)
    return v
