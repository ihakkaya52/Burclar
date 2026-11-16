import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from engine import *
from yardimci import big, spread, soften, ses

HAVA = EL["Hava"]

def spread(segs):
    """segs: list of (start, end, nwords) -> per-word times"""
    out = []
    for a, b, n in segs:
        g = (b - a) * .85 / n; out += [a + i * g for i in range(n)]
    return out

def video():
    T = 40.5
    v = Video(T, [HAVA, (120, 80, 200)], 31)
    v.voice = ses("ikizler_erkegi")
    # ---- hook: "İkizler erkeğiyle mi tanıştın? Dur, önce şunu izle."
    v.add(Img(medallion("İkizler", "♂", 230), W / 2, 410, 0.0, 4.01, "spin", bob=8)); v.sfx.append((0.0, "swish"))
    v.slam(big("İKİZLER", 220, WHITE), W / 2, 650, 0.0, 4.01, power=.12, sound="boom")
    v.slam(big("ERKEĞİ", 220, YEL), W / 2, 880, 0.62, 4.01)
    v.cap("hakkında kimsenin söylemediği 5 şey 👀", {"5"}, 1100, 1.1, 4.01, size=62, gap=.12, emph=False)
    v.slam(sticker("DUR! önce şunu izle ✋", 56, RED, WHITE, rot=-4), W / 2, 1330, 2.12, 4.01, power=.08, sound="hit")
    v.shake(2.27, 26)

    items = [
        (5, 4.01, 10.18, "Sıkıldığı an kaybolur.", {"kaybolur."}, spread([(4.89, 6.43, 3)]),
         "Sohbet onu sarmıyorsa, aklı çoktan başka yerde.", {"başka", "yerde."}, spread([(6.70, 8.19, 3), (8.34, 9.91, 4)]), "💨"),
        (4, 10.18, 15.75, "Aynı anda 5 kişiyle mesajlaşır…", {"5"}, spread([(11.02, 13.11, 5)]),
         "…ve hepsine ayrı bir espri yapar.", {"espri"}, spread([(13.34, 15.44, 6)]), "📱"),
        (3, 15.75, 22.01, "Onunla tartışmaya bile girme.", {"girme."}, spread([(16.57, 18.19, 4)]),
         "Lafı öyle bir çevirir ki, sonunda özür dileyen sen olursun.", {"sen"}, spread([(18.40, 21.68, 11)]), "😤"),
        (2, 22.01, 27.24, "Bugün “evet” diyorsa, yarın “belki” der.", {"“evet”", "“belki”"}, spread([(22.79, 25.39, 6)]),
         "Planlar son dakika değişir, alış.", {"alış."}, spread([(25.63, 27.21, 5)]), "🤔"),
        (1, 29.35, 35.34, "Onu güzellikle değil, sohbetle tutarsın.", {"sohbetle"}, spread([(29.47, 31.92, 5)]),
         "Aklını yakalarsan, kalbi zaten peşinden gelir.", {"Aklını", "kalbi"}, spread([(32.18, 33.26, 2), (33.41, 35.06, 4)]), "🧠"),
    ]
    for n, t0, t1, title, kws, tt, sub, skws, st, emo in items:
        v.cut(t0)
        v.slam(big(str(n), 400, YEL, 16), W / 2, 540, t0, t1, power=.12 if n > 1 else .2, sound="hit" if n > 1 else "boom")
        v.shake(t0 + .15, 20 if n > 1 else 36)
        v.add(Img(emoji_img(emo, 140), W / 2 + 250, 450, t0 + .5, t1, "spin", bob=10)); v.sfx.append((t0 + .5, "pop"))
        v.cap(title, kws, 860, tt[0], t1, size=86, gap=.3, times=tt)
        v.cap(sub, skws, 1110, st[0], t1, size=58, gap=.3, times=st, maxw=900)
        if n == 1:
            v.add(Particles(t0 + .15, W / 2, 620, "confetti", 100, seed=5))
    # ---- "Ve bir numara…"
    v.cut(27.24)
    v.cap("Ve 1 numara...", {"1"}, 880, 27.36, 29.35, size=110, gap=.3, times=[27.36, 28.15, 28.45])
    v.ducks.append((27.24, 29.35)); v.sfx.append((27.75, "riser"))
    # ---- outro: "Tanıdık geldi mi? Bir İkizler erkeğini etiketle, bu videoyu da kaydet."
    v.cut(35.34)
    v.slam(sticker("Tanıdık geldi mi? 👀", 74, WHITE, BLACK, rot=-4, maxw=960), W / 2, 740, 35.38, T, power=.07, sound="hit")
    v.cap("Bir İkizler erkeğini etiketle 👇", {"etiketle"}, 1000, 36.55, T, size=82, gap=.3, times=spread([(36.55, 38.22, 4)]))
    v.slam(sticker("bu videoyu da kaydet 📌", 54, YEL, BLACK, rot=3), W / 2, 1240, 38.3, T, power=.05, sound="pop")
    return v
