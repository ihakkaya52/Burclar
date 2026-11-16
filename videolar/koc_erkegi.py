import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from engine import *
from yardimci import big, spread, soften, ses

ATES = EL["Ateş"]

def video():
    T = 33.2
    v = Video(T, [ATES, (200, 40, 40)], 191)
    v.voice = ses("koc_erkegi")
    # hook
    v.add(Img(medallion("Koç", "♂", 230), W / 2, 410, 0.0, 3.57, "spin", bob=8)); v.sfx.append((0.0, "swish"))
    v.slam(big("KOÇ", 250, WHITE), W / 2, 625, 0.0, 3.57, power=.12, sound="boom")
    v.slam(big("ERKEĞİ", 230, YEL), W / 2, 905, 0.5, 3.57)
    v.cap("hakkında kimsenin söylemediği 5 şey 👀", {"5"}, 1100, .9, 3.57, size=62, gap=.1, emph=False)
    v.slam(sticker("DUR! önce şunu izle ✋", 56, RED, WHITE, rot=-4), W / 2, 1330, 1.72, 3.57, power=.08, sound="hit")
    v.shake(1.87, 26)

    items = [
        (5, 3.57, 8.62, "Beklemeyi sevmez.", {"sevmez."}, spread([(4.43, 5.66, 2)]),
         "Mesajına cevap gelmezse, kapına gelir.", {"kapına"}, spread([(5.93, 8.37, 5)]), "⏱"),
        (4, 8.62, 13.50, "Rekabeti çok sever.", {"Rekabeti"}, spread([(9.47, 10.73, 3)]),
         "Masa oyununda bile kaybetmeye dayanamaz.", {"dayanamaz."}, spread([(10.94, 13.25, 5)]), "🏆"),
        (3, 13.50, 18.56, "Öfkesi çabuk parlar…", {"parlar…"}, spread([(14.33, 15.6, 3)]),
         "ama beş dakika sonra her şeyi unutur.", {"unutur."}, spread([(15.86, 18.3, 7)]), "💥"),
        (2, 18.56, 22.79, "Ne düşünüyorsa yüzüne söyler.", {"yüzüne"}, spread([(19.32, 21.08, 4)]),
         "Lafı dolandırmayı bilmez.", {"bilmez."}, spread([(21.24, 22.66, 3)]), "🗣"),
        (1, 24.56, 28.06, "Sevdiği kişi için ateşe atlar.", {"ateşe"}, spread([(24.68, 26.6, 5)]),
         "Hem de düşünmeden.", {"düşünmeden."}, spread([(26.71, 27.86, 3)]), "🔥"),
    ]
    for n, t0, t1, title, kws, tt, sub, skws, st, emo in items:
        v.cut(t0)
        v.slam(big(str(n), 400, YEL, 16), W / 2, 540, t0, t1, power=.12 if n > 1 else .2, sound="hit" if n > 1 else "boom")
        v.shake(t0 + .15, 20 if n > 1 else 36)
        v.add(Img(emoji_img(emo, 140), W / 2 + 250, 450, t0 + .45, t1, "spin", bob=10)); v.sfx.append((t0 + .45, "pop"))
        v.cap(title, kws, 860, tt[0], t1, size=86, gap=.3, times=tt)
        v.cap(sub, skws, 1110, st[0], t1, size=60, gap=.3, times=st, maxw=900)
        if n == 1: v.add(Particles(t0 + .15, W / 2, 620, "confetti", 100, seed=5))
    v.shake(15.2, 24); v.punch.append((15.2, .07))          # "parlar…"
    # "Ve bir numara…"
    v.cut(22.79)
    v.cap("Ve 1 numara...", {"1"}, 880, 22.91, 24.56, size=110, gap=.3, times=[22.91, 23.2, 23.5])
    v.ducks.append((22.79, 24.56)); v.sfx.append((22.95, "riser"))
    # outro
    v.cut(28.06)
    v.slam(sticker("Tanıdık geldi mi? 👀", 74, WHITE, BLACK, rot=-4, maxw=960), W / 2, 740, 28.18, T, power=.07, sound="hit")
    v.cap("Bir Koç erkeğini etiketle 👇", {"etiketle"}, 1000, 29.28, T, size=82, gap=.3, times=spread([(29.28, 30.89, 4)]))
    v.slam(sticker("bu videoyu da kaydet 📌", 54, YEL, BLACK, rot=3), W / 2, 1240, 30.99, T, power=.05, sound="pop")
    return v
