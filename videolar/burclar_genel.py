import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "motor"))
from engine import *
from yardimci import big, spread, soften, ses

def el_tile(name, emo, col, w=410, h=330):
    im = Image.new("RGBA", (w + 30, h + 30), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([18, 22, w + 12, h + 16], radius=36, fill=(0, 0, 0, 140))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(im); d.rounded_rectangle([12, 12, w + 8, h + 8], radius=36, fill=col + (255,), outline=WHITE + (255,), width=6)
    e = emoji_img(emo, 110); im.alpha_composite(e, (int(12 + w / 2 - e.width / 2), 36))
    t = rich(up(name), anton(92), WHITE, stroke=6); im.alpha_composite(t, (int(12 + w / 2 - t.width / 2), 150))
    return im

def dots(i):
    w = 12 * 56; im = Image.new("RGBA", (w + 20, 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k, n in enumerate(ORDER):
        x = 10 + k * 56 + 28; col = EL[SIGN[n][1]]
        r = 20 if k == i else 13
        d.ellipse([x - r, 30 - r, x + r, 30 + r], fill=(col if k <= i else (90, 90, 110)) + (255,), outline=(WHITE + (255,)) if k == i else None, width=4)
    return im

def video():
    T = 60.6
    v = Video(T, [(150, 90, 220), EL["Ateş"]], 83)
    v.voice = ses("burclar_genel")
    # A intro: "12 burç, 12 farklı karakter… Sen hangisisin?"
    v.add(Spin(make_wheel(500), W / 2, 610, 0.0, 4.1)); v.sfx.append((0.0, "whoosh"))
    v.slam(big("12 BURÇ", 200, YEL), W / 2, 1010, 0.2, 4.1, power=.14, sound="boom"); v.shake(.35, 26)
    v.cap("12 farklı karakter…", {"farklı"}, 1190, 1.24, 4.1, size=70, times=spread([(1.24, 2.15, 3)]))
    v.slam(sticker("Sen hangisisin? 🤔", 58, WHITE, BLACK, rot=-3), W / 2, 1365, 2.95, 4.1, power=.06, sound="hit")
    v.cut(4.1)
    # B elements
    v.cap("Önce şunu bil:", {"bil:"}, 400, 4.21, 14.75, size=80, times=spread([(4.21, 4.86, 3)]), emph=False)
    v.cap("Her burç dört elementten birine ait.", {"dört"}, 545, 5.40, 14.75, size=56, times=spread([(5.40, 7.47, 6)]))
    tiles = [("Ateş", "🔥", 8.07, "tutkulu", 8.85), ("Toprak", "🌱", 9.74, "sağlam", 10.65), ("Hava", "💨", 11.45, "özgür", 12.25), ("Su", "💧", 13.09, "duygusal", 13.75)]
    for k, (n, e, t, adj, ta) in enumerate(tiles):
        x = W / 2 + (-218 if k % 2 == 0 else 218); y = 840 + (k // 2) * 370
        v.slam(el_tile(n, e, EL[n]), x, y, t, 14.75, power=.07, sound="hit", flash=False); v.shake(t + .15, 12)
        v.slam(sticker(adj, 40, WHITE, BLACK, rot=(-4 if k % 2 == 0 else 4)), x, y + 150, ta, 14.75, power=.03, sound="thud", flash=False)
    v.cut(14.75)
    # C transition
    v.cap("Şimdi hızlıca tanışalım ⚡", {"tanışalım"}, 880, 14.85, 16.55, size=92, times=spread([(14.85, 16.09, 3)]))
    v.cut(16.55)
    # D 12 signs
    S = [("Koç", 16.67, "Önce yapar, sonra düşünür.", {"düşünür."}, [(17.46, 18.11, 2), (18.36, 19.02, 2)], "⚡"),
         ("Boğa", 19.55, "Rahatını kimseye bozdurmaz.", {"bozdurmaz."}, [(20.32, 22.07, 3)], "🛋"),
         ("İkizler", 22.47, "Aynı anda beş sohbet yürütür.", {"beş"}, [(23.41, 25.11, 5)], "💬"),
         ("Yengeç", 25.63, "Kalbi kocaman… alınganlığı da.", {"alınganlığı"}, [(26.54, 27.59, 2), (27.98, 28.77, 2)], "🥺"),
         ("Aslan", 29.24, "Sahne onun, ışıklar da.", {"ışıklar"}, [(30.07, 30.89, 2), (31.16, 31.76, 2)], "👑"),
         ("Başak", 32.21, "Her detayı fark eder. Evet, her detayı.", {"detayı."}, [(33.02, 34.17, 4), (34.61, 34.82, 1), (35.16, 35.81, 2)], "🔍"),
         ("Terazi", 36.25, "Karar vermesi biraz… uzun sürer.", {"uzun"}, [(37.11, 38.64, 3), (38.86, 39.50, 2)], "⚖"),
         ("Akrep", 40.08, "Unutmaz. Asla.", {"Asla."}, [(40.90, 41.52, 1), (41.85, 42.32, 1)], "🦂"),
         ("Yay", 42.77, "Bavulu her zaman hazırdır.", {"hazırdır."}, [(43.48, 44.96, 4)], "🧳"),
         ("Oğlak", 45.48, "Hedefi koyar, zirveye tırmanır.", {"zirveye"}, [(46.32, 47.01, 2), (47.26, 48.14, 2)], "🏔"),
         ("Kova", 48.66, "Herkesten farklı düşünür, hem de bilerek.", {"bilerek."}, [(49.37, 50.66, 3), (51.15, 51.80, 3)], "💡"),
         ("Balık", 52.36, "Gözlerini kapatır, başka bir dünyaya gider.", {"dünyaya"}, [(53.18, 54.13, 2), (54.49, 55.60, 4)], "🌊")]
    DATES = {"Koç": "21 Mart – 19 Nisan", "Boğa": "20 Nisan – 20 Mayıs", "İkizler": "21 Mayıs – 20 Haziran",
             "Yengeç": "21 Haziran – 22 Temmuz", "Aslan": "23 Temmuz – 22 Ağustos", "Başak": "23 Ağustos – 22 Eylül",
             "Terazi": "23 Eylül – 22 Ekim", "Akrep": "23 Ekim – 21 Kasım", "Yay": "22 Kasım – 21 Aralık",
             "Oğlak": "22 Aralık – 19 Ocak", "Kova": "20 Ocak – 18 Şubat", "Balık": "19 Şubat – 20 Mart"}
    for i, (n, tn, line, kws, segs, emo) in enumerate(S):
        t0 = tn - .12; t1 = S[i + 1][1] - .12 if i < 11 else 56.1
        if i: v.cut(t0)
        v.add(Img(dots(i), W / 2, 330, t0, t1, "fade", out=False))
        v.add(Img(medallion(n, None, 330), W / 2, 600, t0, t1, "spin", dur=.4, bob=8))
        v.add(Shock(t0 + .2, W / 2, 600, EL[SIGN[n][1]], 120, 560, .5, 16))
        v.slam(big(up(n), 150, YEL if SIGN[n][1] in ("Ateş", "Toprak") else WHITE, 10), W / 2, 850, t0 + .05, t1, power=.1, sound="hit", flash=False)
        v.add(Img(emoji_img(emo, 120), W / 2 + 230, 500, t0 + .35, t1, "spin", bob=10)); v.sfx.append((t0 + .35, "pop"))
        v.add(Img(sticker("📅 " + DATES[n], 44, EL[SIGN[n][1]], WHITE, rot=0, weight=800), W / 2, 1005, t0 + .3, t1, "pop"))
        v.cap(line, kws, 1215, segs[0][0], t1, size=74, times=spread(segs), maxw=940)
        if n == "Akrep": v.sfx.append((41.85, "boom")); v.shake(41.9, 30); v.punch.append((41.9, .1))
        if n == "Başak": v.shake(35.2, 16)
    v.cut(56.1)
    # E outro
    v.add(Spin(make_wheel(560), W / 2, 640, 56.1, T, speed=-20))
    v.cap("Peki sen hangisisin?", {"sen"}, 1050, 56.25, T, size=82, times=[56.25] + spread([(56.77, 57.60, 2)]))
    v.cap("Burcunu yorumlara yaz 👇", {"yorumlara"}, 1230, 58.02, T, size=72, times=spread([(58.02, 59.10, 3)]))
    v.slam(sticker("arkadaşını da etiketle 🏷", 50, YEL, BLACK, rot=3), W / 2, 1390, 59.3, T, power=.05, sound="pop", flash=False)
    return v
