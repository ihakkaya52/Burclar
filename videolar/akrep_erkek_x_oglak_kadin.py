import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
import engine
from engine import *
from yardimci import big, spread, soften, ses

SU, TOP = EL["Su"], EL["Toprak"]

def video():
    engine.Caption.KW_AMP = .45
    T = 47.05
    v = Video(T, [SU, TOP], 177)
    v.voice = ses("akrep_erkek_x_oglak_kadin")
    # A hook
    v.add(Img(medallion("Akrep", "♂", 280), W / 2 - 230, 640, 0.0, 8.72, "path", dur=.5, frm=(-300, 640), bob=8))
    v.add(Img(medallion("Oğlak", "♀", 280), W / 2 + 230, 640, 0.0, 8.72, "path", dur=.5, frm=(W + 300, 640), bob=-8))
    v.sfx.append((0.0, "whoosh"))
    v.add(Img(emoji_img("❤", 150), W / 2, 640, .5, 8.72, "pop", pulse=.12))
    for t in (.6, 1.5): v.sfx.append((t, "heart"))
    v.cap("Akrep erkeği + Oğlak kadını", {"Akrep", "Oğlak"}, 930, .18, 8.72, size=76, times=spread([(.18, 1.95, 5)]))
    v.cap("Zodyakın en güçlü çiftlerinden biri. 💪", {"güçlü"}, 1150, 2.31, 4.62, size=58, times=spread([(2.31, 4.30, 5)]), maxw=980)
    v.cap("Dışarıdan soğuk görünürler, ama içten içe birbirlerine çok bağlıdırlar.", {"soğuk", "bağlıdırlar."}, 1190, 4.67, 8.72,
          size=54, times=spread([(4.67, 6.15, 3), (6.25, 8.39, 6)]), maxw=960)
    v.cut(8.72)
    # B score
    v.cap("Peki aşk uyumları kaç?", {"aşk"}, 400, 8.81, 12.28, size=78, times=spread([(8.81, 10.26, 4)]), emph=False)
    t0, dur = 9.4, 2.2; v.add(Ring(88, "AŞK UYUMU", PINK, 880, t0, 12.28, dur))
    for k in range(2, 89, 3):
        q = k / 88; p = 1 - (1 - q) ** (1 / 2.2); v.sfx.append((t0 + p * dur, "tick"))
    te = t0 + dur
    v.sfx += [(te, "hit"), (te, "ding")]; v.punch.append((te, .1)); v.flashes.append((te, 100)); v.shake(te, 20)
    v.ducks.append((9.3, te)); v.sfx.append((te - 1.6, "riser"))
    v.add(Particles(te, W / 2, 880, "hearts", 26, seed=4))
    v.cut(12.28)
    # C why
    v.cap("Neden mi? 🤔", set(), 400, 12.36, 18.38, size=80, times=[12.36, 12.6], emph=False)
    v.pop(medallion("Akrep", "♂", 240), W / 2 - 240, 640, 13.18, 18.38, bob=6)
    v.pop(sticker("Tutkuyu getirir 🔥", 38, WHITE, BLACK, rot=-4, maxw=440), W / 2 - 240, 850, 14.0, 18.38, sound="thud")
    v.pop(medallion("Oğlak", "♀", 240), W / 2 + 240, 640, 14.8, 18.38, bob=-6)
    v.pop(sticker("Düzeni getirir 🧩", 38, YEL, BLACK, rot=4, maxw=440), W / 2 + 240, 850, 15.3, 18.38, sound="thud")
    v.cap("İkisi de hırslı, ikisi de sadık.", {"hırslı,", "sadık."}, 1150, 16.18, 18.38, size=70, times=spread([(16.18, 17.1, 3), (17.2, 18.15, 3)]))
    v.cut(18.38)
    # D1 problem
    v.pop(sticker("Ama bir sorun var... 👀", 60, WHITE, BLACK, rot=-2), W / 2, 420, 18.46, 22.88, sound="hit")
    v.cap("Oğlak işine gömülür, 💼", {"işine"}, 760, 19.88, 22.88, size=78, times=spread([(19.88, 21.1, 3)]))
    v.cap("Akrep ise ilgi bekler. 🥺", {"ilgi"}, 990, 21.2, 22.88, size=78, times=spread([(21.2, 22.46, 4)]))
    v.cut(22.88)
    # D2 chat (POV: Akrep)
    msgs = [("R", "Akşam buluşalım mı? 🌙", 22.95, 24.35), ("L", "Takvimime bir bakayım...", 25.6, 26.35),
            ("R", "Takvim mi? 😐", 27.85, 28.62), ("L", "Salı 19:30 müsaitim ⏰", 29.5, 30.22)]
    v.add(Chat("Oğlak 🐐", medallion("Oğlak", "♀", 120), msgs, 430, 22.88, 32.35))
    for side, txt, ty, tm in msgs: v.sfx += [(ty, "type"), (tm, "msg")]
    v.add(Img(emoji_img("😂", 140), W - 170, 1330, 31.4, 32.35, "spin")); v.sfx.append((31.4, "thud")); v.shake(31.45, 14)
    v.cut(32.35)
    # E bars
    v.cap("Puanlar 👇", set(), 400, 32.37, 37.85, size=84, emph=False)
    for k, (lab, pct, col, t) in enumerate([("Sadakat", 95, SU, 32.42), ("Hırs", 100, (255, 140, 0), 33.4), ("Güven", 90, TOP, 34.3), ("Romantizm", 55, PINK, 35.8)]):
        v.add(Bars([(lab, pct, col)], 610 + k * 175, t, 37.85)); v.sfx.append((t, "pop"))
    v.pop(emoji_img("⏰", 80), 590, 610 + 3 * 175, 36.6, 37.85, sound="thud")
    v.cut(37.85)
    # F formula
    v.cap("Formül basit:", {"basit:"}, 480, 37.93, 43.15, size=92, times=[37.93, 38.25])
    v.pop(card("Akrep: onun hedeflerine saygı duy 🎯", accent=SU), W / 2, 770, 38.94, 43.15, sound="swish", anim="left")
    v.pop(card("Oğlak: takvime onu da ekle ❤", accent=TOP), W / 2, 1010, 41.18, 43.15, sound="swish", anim="right")
    v.cut(43.15)
    # G CTA
    v.cap("Bu çifti tanıyorsan etiketle 👇", {"etiketle"}, 820, 43.23, T, size=80, times=spread([(43.23, 44.75, 4)]))
    v.pop(sticker("videoyu da kaydet 📌", 56, YEL, BLACK, rot=3), W / 2, 1080, 44.85, T)
    soften(v)
    return v
