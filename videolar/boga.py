import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from engine import *
from yardimci import big, spread, soften, ses

TOP = EL["Toprak"]

def video():
    T = 35.6
    v = Video(T, [TOP, (200, 150, 60)], 113)
    v.voice = ses("boga")
    # intro: "20 Nisan ile 20 Mayıs arasında doğduysan, bu video senin için."
    v.slam(sticker("20 NİSAN – 20 MAYIS", 64, TOP, WHITE, rot=-3), W / 2, 480, 0.05, 4.1, power=.1, sound="boom"); v.shake(.2, 22)
    v.cap("20 Nisan ile 20 Mayıs arasında doğduysan,", {"Nisan", "Mayıs"}, 720, .19, 4.1, size=78, times=spread([(.19, 2.64, 7)]))
    v.cap("bu video senin için.", {"senin"}, 990, 2.85, 4.1, size=84, times=spread([(2.85, 3.84, 4)]))
    v.cut(4.1)
    # "Sen bir Boğa'sın. Ve Boğa'yı tanımayanlar şu beş şeyi bilmiyor."
    v.add(Img(medallion("Boğa", None, 300), W / 2, 470, 4.1, 8.56, "spin", bob=8)); v.sfx.append((4.1, "swish"))
    v.cap("Sen bir", set(), 690, 4.23, 8.56, size=72, times=[4.23, 4.45], emph=False)
    v.slam(big("BOĞA'SIN", 210, YEL), W / 2, 870, 4.7, 8.56, power=.15, sound="boom"); v.shake(4.85, 30)
    v.add(Img(emoji_img("🐂", 130), W / 2 + 250, 400, 5.0, 8.56, "spin", bob=10)); v.sfx.append((5.0, "pop"))
    v.cap("Ve Boğa'yı tanımayanlar şu 5 şeyi bilmiyor.", {"5"}, 1120, 5.55, 8.56, size=62, times=spread([(5.55, 6.77, 3), (6.97, 8.10, 4)]), maxw=940)

    items = [
        (5, 8.56, 12.0, "Rahatı bozulursa,", {"bozulursa,"}, spread([(9.51, 10.55, 2)]),
         "bütün günü bozulur.", {"bütün"}, spread([(10.65, 11.61, 3)]), "🛋"),
        (4, 12.0, 15.63, "Güzel bir yemek,", {"yemek,"}, spread([(12.91, 13.75, 3)]),
         "onun için bir aşk dilidir. 🍝", {"aşk"}, spread([(13.97, 15.31, 5)]), "😋"),
        (3, 15.63, 21.15, "Bir karar verdiyse,", {"karar"}, spread([(16.52, 17.61, 3)]),
         "onu kimse ikna edemez. Gerçekten… kimse.", {"kimse."}, spread([(17.73, 19.12, 4), (19.45, 19.98, 1), (20.41, 20.79, 1)]), "🧱"),
        (2, 21.15, 25.34, "Az kişiyi sever…", {"Az"}, spread([(21.99, 22.83, 3)]),
         "ama sevdiğini asla bırakmaz.", {"asla"}, spread([(23.24, 25.05, 4)]), "💛"),
        (1, 26.6, 31.16, "Sabrı sonsuz gibi görünür.", {"sonsuz"}, spread([(26.72, 28.07, 4)]),
         "Ama bir gün taşarsa… kaçacak yer ara.", {"kaçacak"}, spread([(28.37, 29.59, 4), (29.92, 30.71, 3)]), "🌋"),
    ]
    for n, t0, t1, title, kws, tt, sub, skws, st, emo in items:
        v.cut(t0)
        v.slam(big(str(n), 400, YEL, 16), W / 2, 540, t0, t1, power=.12 if n > 1 else .2, sound="hit" if n > 1 else "boom")
        v.shake(t0 + .15, 20 if n > 1 else 36)
        v.add(Img(emoji_img(emo, 140), W / 2 + 250, 450, t0 + .45, t1, "spin", bob=10)); v.sfx.append((t0 + .45, "pop"))
        v.cap(title, kws, 860, tt[0], t1, size=86, gap=.3, times=tt)
        v.cap(sub, skws, 1110, st[0], t1, size=60, gap=.3, times=st, maxw=900)
        if n == 1: v.add(Particles(t0 + .15, W / 2, 620, "confetti", 100, seed=5))
    v.shake(20.45, 22)                                                       # "Gerçekten… kimse."
    v.sfx.append((29.9, "boom")); v.shake(29.95, 36); v.punch.append((29.95, .12)); v.flashes.append((29.95, 90))  # "kaçacak yer ara"
    # "Ve bir numara…"
    v.cut(25.34)
    v.cap("Ve 1 numara...", {"1"}, 880, 25.46, 26.6, size=110, gap=.3, times=[25.46, 25.75, 26.0])
    v.ducks.append((25.34, 26.6)); v.sfx.append((25.0, "riser"))
    # outro
    v.cut(31.16)
    v.slam(sticker("Sen de Boğa mısın? 🐂", 72, WHITE, BLACK, rot=-4, maxw=960), W / 2, 740, 31.28, T, power=.07, sound="hit")
    v.cap("Yorumlara yaz 👇", {"Yorumlara"}, 990, 32.43, T, size=86, times=spread([(32.43, 33.12, 2)]))
    v.slam(sticker("bir Boğa'yı da etiketle 🏷", 54, YEL, BLACK, rot=3), W / 2, 1230, 33.38, T, power=.05, sound="pop")
    return v
