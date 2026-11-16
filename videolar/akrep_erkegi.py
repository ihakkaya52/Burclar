import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from engine import *
from yardimci import big, spread, soften, ses

SU = EL["Su"]

def video():
    T = 32.2
    v = Video(T, [SU, (150, 30, 70)], 97)
    v.voice = ses("akrep_erkegi")
    # hook: "Akrep erkeğiyle mi tanıştın? Dur, önce şunu izle."
    v.add(Img(medallion("Akrep", "♂", 230), W / 2, 410, 0.0, 3.76, "spin", bob=8)); v.sfx.append((0.0, "swish"))
    v.slam(big("AKREP", 230, WHITE), W / 2, 650, 0.0, 3.76, power=.12, sound="boom")
    v.slam(big("ERKEĞİ", 230, YEL), W / 2, 885, 0.55, 3.76)
    v.cap("hakkında kimsenin söylemediği 5 şey 👀", {"5"}, 1100, 1.0, 3.76, size=62, gap=.1, emph=False)
    v.slam(sticker("DUR! önce şunu izle ✋", 56, RED, WHITE, rot=-4), W / 2, 1330, 1.85, 3.76, power=.08, sound="hit")
    v.shake(2.0, 26)

    items = [
        (5, 3.76, 8.48, "Her şeyi fark eder.", {"fark"}, spread([(4.67, 5.78, 4)]),
         "Sen söylemeden, gözlerinden okur.", {"gözlerinden"}, spread([(6.09, 8.17, 4)]), "👁"),
        (4, 8.48, 12.64, "Kıskançtır…", {"Kıskançtır…"}, [9.40],
         "ama bunu asla itiraf etmez.", {"asla"}, spread([(10.47, 12.40, 5)]), "😒"),
        (3, 12.64, 17.30, "Az konuşur, çok dinler.", {"dinler."}, spread([(13.43, 14.21, 2), (14.39, 15.09, 2)]),
         "Sessizliği bile bir şey anlatır.", {"Sessizliği"}, spread([(15.36, 17.03, 5)]), "🤫"),
        (2, 17.30, 21.93, "Bir kez güvenini kırarsan,", {"kırarsan,"}, spread([(18.11, 19.53, 4)]),
         "o kapıyı sonsuza kadar kapatır.", {"sonsuza"}, spread([(19.73, 21.72, 5)]), "🚪"),
        (1, 23.19, 27.08, "Ya hep ya hiç.", {"hep", "hiç."}, spread([(23.31, 24.49, 4)]),
         "Severse, tüm kalbiyle sever.", {"kalbiyle"}, spread([(24.77, 25.48, 1), (25.67, 26.81, 3)]), "❤"),
    ]
    for n, t0, t1, title, kws, tt, sub, skws, st, emo in items:
        v.cut(t0)
        v.slam(big(str(n), 400, YEL, 16), W / 2, 540, t0, t1, power=.12 if n > 1 else .2, sound="hit" if n > 1 else "boom")
        v.shake(t0 + .15, 20 if n > 1 else 36)
        v.add(Img(emoji_img(emo, 140), W / 2 + 250, 450, t0 + .45, t1, "spin", bob=10)); v.sfx.append((t0 + .45, "pop"))
        v.cap(title, kws, 860, tt[0], t1, size=96 if n == 4 else 86, gap=.3, times=tt)
        v.cap(sub, skws, 1110, st[0], t1, size=60, gap=.3, times=st, maxw=900)
        if n == 1:
            v.add(Particles(t0 + .15, W / 2, 620, "confetti", 100, seed=5))
    v.shake(9.45, 28); v.punch.append((9.45, .08))               # "Kıskançtır…"
    v.sfx.append((21.5, "boom")); v.shake(21.55, 34); v.punch.append((21.55, .12)); v.flashes.append((21.55, 80))  # door slams
    # "Ve bir numara…"
    v.cut(21.93)
    v.cap("Ve 1 numara...", {"1"}, 880, 22.05, 23.19, size=110, gap=.3, times=[22.05, 22.35, 22.62])
    v.ducks.append((21.93, 23.19)); v.sfx.append((21.6, "riser"))
    # outro
    v.cut(27.08)
    v.slam(sticker("Tanıdık geldi mi? 👀", 74, WHITE, BLACK, rot=-4, maxw=960), W / 2, 740, 27.2, T, power=.07, sound="hit")
    v.cap("Bir Akrep erkeğini etiketle 👇", {"etiketle"}, 1000, 28.30, T, size=82, gap=.3, times=spread([(28.30, 29.85, 4)]))
    v.slam(sticker("bu videoyu da kaydet 📌", 54, YEL, BLACK, rot=3), W / 2, 1240, 29.95, T, power=.05, sound="pop")
    return v
