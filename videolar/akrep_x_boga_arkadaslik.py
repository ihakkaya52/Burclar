import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
import engine
from engine import *
from yardimci import big, spread, soften, ses

SU, TOP = EL["Su"], EL["Toprak"]

def video():
    engine.Caption.KW_AMP = .45
    T = 43.2
    v = Video(T, [SU, TOP], 131)
    v.voice = ses("akrep_x_boga_arkadaslik")
    # A hook
    v.add(Img(medallion("Akrep", "♂", 300), W / 2 - 175, 720, 0.0, 5.7, "path", dur=.45, frm=(-300, 720), bob=8))
    v.add(Img(medallion("Boğa", "♂", 300), W / 2 + 175, 720, 0.0, 5.7, "path", dur=.45, frm=(W + 300, 720), bob=-8))
    v.sfx += [(0.0, "whoosh"), (.42, "hit")]; v.shake(.45, 24); v.punch.append((.45, .08))
    v.add(Particles(.45, W / 2, 720, "confetti", 40, seed=2, spread=.7))
    v.cap("Bir Akrep ile bir Boğa arkadaş olursa...", {"Akrep", "Boğa"}, 1050, .2, 5.7, size=70, times=spread([(.20, 2.28, 7)]))
    v.cap("zodyakın en inatçı ikilisi doğar 🦂🐂", {"inatçı"}, 1290, 3.08, 5.7, size=62, times=spread([(3.08, 5.12, 5)]))
    v.cut(5.7)
    # B score
    v.cap("Peki arkadaşlık uyumları kaç?", {"uyumları"}, 400, 5.79, 9.55, size=72, times=spread([(5.79, 7.52, 4)]), emph=False)
    t0, dur = 6.6, 2.0; v.add(Ring(75, "ARKADAŞLIK", YEL, 880, t0, 9.55, dur))
    for k in range(2, 76, 3):
        q = k / 75; p = 1 - (1 - q) ** (1 / 2.2); v.sfx.append((t0 + p * dur, "tick"))
    te = t0 + dur
    v.sfx += [(te, "hit"), (te, "ding")]; v.punch.append((te, .1)); v.flashes.append((te, 100)); v.shake(te, 20)
    v.ducks.append((6.5, te)); v.sfx.append((te - 1.6, "riser"))
    v.cut(9.55)
    # C good side
    v.pop(sticker("✅ İYİ TARAFI", 62, GREEN, WHITE, rot=-2), W / 2, 400, 9.67, 19.9)
    for k, (txt, t) in enumerate([("İkisi de sadakati her şeyden üstün tutar 🤝", 11.03),
                                  ("Biri sır tutar, diğeri sırtını yaslar 🛡", 13.87),
                                  ("Akrep sohbet açar, Boğa yemeği ısmarlar 🍕", 16.66)]):
        v.pop(card(txt, accent=GREEN), W / 2, 650 + k * 240, t, 19.9, sound="swish", anim="left" if k % 2 == 0 else "right")
    v.cut(19.9)
    # D bad side: the endless argument
    v.pop(sticker("🚩 KÖTÜ TARAFI", 62, RED, WHITE, rot=2), W / 2, 400, 20.11, 28.98)
    v.cap("Bir gün küçük bir konuda tartışırlar…", {"tartışırlar…"}, 590, 21.75, 28.98, size=64, times=[21.75, 21.92] + spread([(22.17, 23.46, 4)]))
    v.pop(medallion("Akrep", None, 190), W / 2 - 210, 850, 22.9, 28.98, bob=5)
    v.pop(medallion("Boğa", None, 190), W / 2 + 210, 850, 23.1, 28.98, bob=-5)
    v.pop(emoji_img("😤", 80), W / 2 - 130, 770, 23.3, 28.98, sound=None)
    v.pop(emoji_img("😤", 80), W / 2 + 290, 770, 23.45, 28.98, sound=None)
    v.pop(sticker("⏳ 1 GÜN SONRA…", 56, WHITE, BLACK, rot=-3), W / 2, 1090, 24.17, 25.3, sound="tick")
    v.pop(sticker("⏳ 1 HAFTA SONRA…", 56, YEL, BLACK, rot=3), W / 2, 1090, 25.35, 28.98, sound="tick")
    v.cap("İkisi de hâlâ ilk adımı atmaz. 🙄", {"atmaz."}, 1320, 26.62, 28.98, size=60, times=spread([(26.62, 28.50, 6)]))
    v.cut(28.98)
    # E bars
    v.cap("Puanlar 👇", set(), 400, 29.0, 34.1, size=84, emph=False)
    for k, (lab, pct, col, t) in enumerate([("Sadakat", 95, SU, 29.10), ("Güven", 85, TOP, 30.23), ("Eğlence", 70, YEL, 31.23), ("Esneklik", 0, RED, 32.6)]):
        v.add(Bars([(lab, pct, col)], 610 + k * 175, t, 34.1)); v.sfx.append((t, "pop"))
    v.pop(emoji_img("💀", 80), 450, 610 + 3 * 175, 33.35, 34.1, sound="thud")
    v.cut(34.1)
    # F verdict
    v.cap("Kısacası:", set(), 430, 34.24, 38.8, size=70, times=[34.24], emph=False)
    v.cap("Biri “haklısın” demeyi öğrenirse...", {"“haklısın”"}, 640, 35.16, 38.8, size=76, times=[35.16] + spread([(35.67, 37.07, 3)]))
    v.slam(big("KIRK YILLIK", 170, YEL), W / 2, 930, 37.3, 38.8, power=.08, sound="hit", flash=False)
    v.slam(big("KANKA", 200, WHITE), W / 2, 1150, 37.75, 38.8, power=.06, sound="hit", flash=False)
    v.add(Particles(37.8, W / 2, 1000, "confetti", 60, seed=9)); v.sfx.append((37.8, "ding"))
    v.cut(38.8)
    # G CTA
    v.cap("Akrep ya da Boğa kankanı etiketle 👇", {"etiketle"}, 820, 38.87, T, size=76, times=spread([(38.87, 39.77, 4), (40.0, 41.01, 2)]))
    v.pop(sticker("videoyu da kaydet 📌", 56, YEL, BLACK, rot=3), W / 2, 1090, 41.24, T)
    soften(v)
    return v
