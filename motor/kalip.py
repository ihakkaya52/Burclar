"""Tek burç ("5 şey") videolarının ortak kalıbı.

Her video dosyası yalnızca bir SPEC verir: burç, cinsiyet ve beş madde (cümleler + sahne kalıbı).
Seslendirme metni, zamanlama, altyazılar, giriş (burç + takvim) ve kapanış buradan otomatik çıkar.
"""
import os, re
from engine import *

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALTIN = (255, 190, 60); MAVI = (0, 132, 255); GRI = (58, 58, 72); MOR = (120, 90, 230); KOYU = (74, 78, 104)
ATES, TOPRAK, HAVA, SU = EL["Ateş"], EL["Toprak"], EL["Hava"], EL["Su"]

# 2026 takvimi: ay -> (ayın 1'i haftanın kaçıncı günü [0 = Pzt], gün sayısı)
AY = {"Ocak": (3, 31), "Şubat": (6, 28), "Mart": (6, 31), "Nisan": (2, 30), "Mayıs": (4, 31), "Haziran": (0, 30),
      "Temmuz": (2, 31), "Ağustos": (5, 31), "Eylül": (1, 30), "Ekim": (3, 31), "Kasım": (6, 30), "Aralık": (1, 31)}
# burç -> (dosya adı, "-i" hali, emoji, başlangıç günü, ay, bitiş günü, ay, ikinci renk)
BURC = {
    "Koç": ("koc", "Koç'u", "🐏", 21, "Mart", 19, "Nisan", (170, 60, 20)),
    "Boğa": ("boga", "Boğa'yı", "🐂", 20, "Nisan", 20, "Mayıs", (200, 150, 60)),
    "İkizler": ("ikizler", "İkizler'i", "👯", 21, "Mayıs", 20, "Haziran", (150, 110, 230)),
    "Yengeç": ("yengec", "Yengeç'i", "🦀", 21, "Haziran", 22, "Temmuz", (60, 150, 190)),
    "Aslan": ("aslan", "Aslan'ı", "🦁", 23, "Temmuz", 22, "Ağustos", (170, 60, 20)),
    "Başak": ("basak", "Başak'ı", "🌾", 23, "Ağustos", 22, "Eylül", (170, 130, 60)),
    "Terazi": ("terazi", "Terazi'yi", "⚖", 23, "Eylül", 22, "Ekim", (200, 110, 190)),
    "Akrep": ("akrep", "Akrep'i", "🦂", 23, "Ekim", 21, "Kasım", (150, 30, 70)),
    "Yay": ("yay", "Yay'ı", "🏹", 22, "Kasım", 21, "Aralık", (150, 60, 160)),
    "Oğlak": ("oglak", "Oğlak'ı", "🐐", 22, "Aralık", 19, "Ocak", (90, 90, 120)),
    "Kova": ("kova", "Kova'yı", "🏺", 20, "Ocak", 18, "Şubat", (90, 60, 200)),
    "Balık": ("balik", "Balık'ı", "🐟", 19, "Şubat", 20, "Mart", (130, 70, 200)),
}
SAYILAR = ["Beş:", "Dört:", "Üç:", "İki:", None]

def isim(spec): return BURC[spec["burc"]][0] + ("_erkegi" if spec["cins"] == "e" else "_kadini")

def cumleler(spec):
    """Videonun bütün cümleleri sırayla: [(tür, madde_no, metin)]. tür: giris, tarih, sayi, madde, numara, soru, etiket."""
    b = spec["burc"]; e = spec["cins"] == "e"; _, akk, _, d1, a1, d2, a2, _ = BURC[b]
    out = [("giris", None, f"Hayatında bir {b} {'erkeği mi' if e else 'kadını mı'} var?"),
           ("tarih", None, f"{d1} {a1} ile {d2} {a2} arasında doğduysa, şu beş şeyi {'bilmen lazım' if e else 'aklına yaz'}.")]
    for k, (cs, _, _) in enumerate(spec["maddeler"]):
        out.append(("sayi", k, SAYILAR[k]) if SAYILAR[k] else ("numara", k, "Ve bir numara…"))
        out += [("madde", k, c) for c in cs]
    out += [("soru", None, "Tanıdık geldi mi?"),
            ("etiket", None, f"O {akk} etiketle, bu videoyu da kaydet." if e else f"Bir {b} kadınını etiketle, bu videoyu da kaydet.")]
    return out

def metin(spec): return " ".join(c for _, _, c in cumleler(spec))

# =====================================================================================
# Zamanlama: sesi sessizliklerinden cümlelere, cümleleri hecelerine göre kelimelere böler
# =====================================================================================
import copy, math, subprocess
import numpy as np
from yardimci import big, ses
from sahne import *

_BIR = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
_ON = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
_SESLI = set("aeıioöuüâîûAEIİOÖUÜ")

def hece(kelime):
    w = re.sub(r"\d+", lambda m: _ON[int(m.group()) // 10 % 10] + _BIR[int(m.group()) % 10], kelime)
    return max(1, sum(ch in _SESLI for ch in w))

def sade(w):
    """Karşılaştırma için: küçük harf, noktalama ve tırnak yok."""
    return re.sub(r"[^0-9a-zçğıöşüâîû]", "", w.replace("İ", "i").replace("I", "ı").lower())

def _sessizlikler(mp3, esik=.012, enaz=.10):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", mp3, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16) / 32768
    e = np.array([np.sqrt(np.mean(x[i:i + 320] ** 2)) for i in range(0, len(x) - 320, 160)])
    sp = e > esik; idx = np.nonzero(sp)[0]; a, b = idx[0], idx[-1] + 1; out = []; i = a
    while i < b:
        if not sp[i]:
            j = i
            while j < b and not sp[j]: j += 1
            if (j - i) / 100 >= enaz: out.append((i / 100, j / 100))
            i = j
        else: i += 1
    return a / 100, b / 100, out, len(x) / 16000

def _bol(syl, t0, t1, sil, sabit, bilinen=None):
    """Birimleri (hece sayıları `syl`) t0–t1 arasındaki sessizliklere oturtur. Dönen: [(başlangıç, bitiş)].
    bilinen: {birim_no: süre}. Geri sayım rakamları ("Beş:", "İki:") hece sayısından bağımsız ~0,4 sn sürer."""
    n = len(syl)
    if n == 1: return [(t0, t1)]
    if len(sil) < n - 1: return None
    konusma = (t1 - t0) - sum(sorted((e - s for s, e in sil), reverse=True)[:n - 1])
    bilinen = bilinen or {}
    r = max(.06, (konusma - sabit * (n - len(bilinen)) - sum(bilinen.values())) / sum(s for i, s in enumerate(syl) if i not in bilinen))
    bek = [bilinen.get(i, sabit + s * r) for i, s in enumerate(syl)]
    c = lambda i, a, b: ((b - a - bek[i]) / (.25 + .35 * bek[i])) ** 2
    odul = lambda g: .8 * min(sil[g][1] - sil[g][0], .6)
    G = len(sil); INF = 1e9; f = [[INF] * G for _ in range(n - 1)]; arka = [[-1] * G for _ in range(n - 1)]
    for g in range(G): f[0][g] = c(0, t0, sil[g][0]) - odul(g)
    for i in range(1, n - 1):
        for g in range(i, G):
            for h in range(i - 1, g):
                v = f[i - 1][h] + c(i, sil[h][1], sil[g][0]) - odul(g)
                if v < f[i][g]: f[i][g], arka[i][g] = v, h
    g = min(range(n - 2, G), key=lambda g: f[n - 2][g] + c(n - 1, sil[g][1], t1)); sec = [g]
    for i in range(n - 2, 0, -1): g = arka[i][g]; sec.append(g)
    sec.reverse(); out = []; a = t0
    for g in sec: out.append((a, sil[g][0])); a = sil[g][1]
    return out + [(a, t1)]

class Birim:
    """Bir cümle: türü, hangi maddeye ait olduğu, metni, başlangıç/bitiş anı ve kelimelerin anları."""
    def __init__(s, tur, madde, metin): s.tur, s.madde, s.metin, s.t0, s.t1, s.kel = tur, madde, metin, 0., 0., []

_H = {}
def hizala(spec):
    """Cümleleri sese oturtur (mp3 saniyesiyle). Sonuç önbelleğe alınır."""
    ad = isim(spec)
    if ad in _H: return _H[ad]
    a, b, sil, sure = _sessizlikler(os.path.join(KOK, "sesler", ad + ".mp3"))
    U = [Birim(*c) for c in cumleler(spec)]
    araliklar = _bol([sum(hece(w) for w in u.metin.split()) for u in U], a, b, sil, .2, {i: .4 for i, u in enumerate(U) if u.tur == "sayi"})
    if araliklar is None: raise RuntimeError(f"{ad}: seste yeterince duraklama bulunamadı")
    for u, (t0, t1) in zip(U, araliklar):
        u.t0, u.t1 = t0, t1; ws = u.metin.split()
        parca = [[]]
        for w in ws:
            parca[-1].append(w)
            if w.endswith(",") and w is not ws[-1]: parca.append([])
        ic = [(s, e) for s, e in sil if s > t0 + .05 and e < t1 - .05 and e - s >= .12]
        ar = _bol([sum(hece(w) for w in p) for p in parca], t0, t1, ic, .03) if len(parca) > 1 else None
        if ar is None: parca, ar = [ws], [(t0, t1)]
        for p, (p0, p1) in zip(parca, ar):
            ag = [hece(w) + .4 for w in p]; top = sum(ag); k = 0.
            for w, g in zip(p, ag): u.kel.append((w, p0 + (p1 - p0) * k / top)); k += g
    _H[ad] = (U, sure); return _H[ad]

def bosluk(spec):
    """"Ve bir numara…" sonrasına eklenen 0,6 sn gerilim sessizliği (mp3 saniyesiyle)."""
    U, _ = hizala(spec); k = next(i for i, u in enumerate(U) if u.tur == "numara")
    return [(round(float((U[k].t1 + U[k + 1].t0) / 2), 2), .6)]

# =====================================================================================
# Sahne kalıpları. Hepsi c (Sahne) alır; içerik y ≥ 495 ve y ≤ 1000 arasında kalır.
# =====================================================================================
class Sahne:
    def __init__(s, v, a, t1, birimler, yan):
        s.v, s.a, s.t1, s.yan = v, a, t1, yan
        s.S = [u.t0 for u in birimler]; s.kel = [(sade(w), t) for u in birimler for w, t in u.kel]
    def T(s, x):
        """Tetik -> an. Sayı: o cümlenin başı. Kelime: söylendiği an. (tetik, sn): tetikten sn sonra."""
        if isinstance(x, tuple): return s.T(x[0]) + x[1]
        if isinstance(x, int): return s.S[x]
        k = sade(x)
        for w, t in s.kel:
            if w == k: return t
        for w, t in s.kel:
            if w.startswith(k): return t
        raise KeyError(f"tetik kelimesi bulunamadı: {x}")

def _tek_satir(text, size, maxw=900):
    while size > 30 and rich_len(text, mont(size, 900)) > maxw: size -= 4
    return size

def etiket_bas(c, text, t, y=950, size=56, bg=YEL, fg=BLACK, rot=-3, sound="pop", power=.05):
    c.v.slam(sticker(text, _tek_satir(text, size), bg, fg, rot=rot, maxw=960), W / 2, y, t, c.t1, power=power, sound=sound)

def damga_bas(c, text, t, y=800, renk=RED, size=88):
    v = c.v; v.add(Glow(renk, W / 2, y - 100, 640, t, c.t1, .55, nabiz=.15))
    v.slam(sticker(text, _tek_satir(text, size), renk, WHITE, rot=-7, maxw=960), W / 2, y, t, c.t1, power=.13, sound="boom"); v.shake(t + .15, 34)

def gosterge(c, etiket, soru=None, cevap=None, tetik=1, hedef=100, c0=GREEN, c1=RED, sure=.75):
    v = c.v; f0 = c.T(tetik)
    v.add(Glow(c1, W / 2, 700, 600, f0, c.t1, .5, nabiz=.15))
    if soru: v.pop(balon(soru, 44, MAVI, WHITE, "r", maxw=520), 600, 575, max(c.a, f0 - 1.1), c.t1, sound="msg")
    v.add(Meter(etiket, W / 2, 750, 700, c.a, c.t1, f0, sure, hedef=hedef, c0=c0, c1=c1))
    v.sfx.append((f0, "riser")); v.shake(f0 + sure, 30); v.punch.append((f0 + sure, .09)); v.sfx.append((f0 + sure - .05, "boom"))
    if cevap: v.pop(balon(cevap, 52, GRI, WHITE, "l", maxw=560), 470, 930, f0 + sure + .1, c.t1, sound="msg")

def mesaj(c, msgs, damga=None, etiket=None, yaziyor=None, buyutec=False):
    v = c.v; y0, adim = 570, 150
    for i, (yon, text, tet) in enumerate(msgs):
        v.pop(balon(text, 46, MAVI if yon == "r" else GRI, WHITE, yon, maxw=520), 620 if yon == "r" else 440, y0 + i * adim, max(c.a, c.T(tet)), c.t1, sound="msg")
    if etiket:
        te = c.T(etiket[1]); x = 620 if msgs[0][0] == "r" else 440
        v.add(Img(sticker(etiket[0], 32, (20, 20, 32), (170, 170, 190), rot=0, weight=700), x, y0 + 92, te, c.t1, "up")); v.sfx.append((te, "tick"))
    if yaziyor is not None:
        ty = c.T(yaziyor); v.add(Yaziyor(330, y0 + len(msgs) * adim, ty, c.t1)); v.sfx += [(ty, "type"), (ty + .8, "type")]
    if damga:
        td = c.T(damga[1]) - .12
        if buyutec: v.add(Fx(emoji_img("🔍", 140), td - 1.0, td, lambda lt: (420 + 320 * lt, y0 + 10 * math.sin(lt * 9), 1, 0, min(1, lt * 6))))
        damga_bas(c, damga[0], td, y=min(900, y0 + len(msgs) * adim + 30))

def donusum(c, a, b, tetik=1, simsek=False):
    v = c.v; tb = c.T(tetik) - .12
    def faz(emo, renk, hava, t0, t1, giris):
        v.add(Glow(renk, W / 2, 680, 640, t0, t1, .6, nabiz=.12))
        if hava == "yagmur": v.add(Yagis("yagmur", t0, t1, (100, 500, 980, 980), 40, seed=5))
        elif hava == "konfeti": v.add(Particles(t0 + .1, W / 2, 700, "confetti", 80, seed=7, spread=.8))
        elif hava: v.add(Yagis("kar", t0, t1, (130, 500, 950, 980), 14, seed=3, emo=hava))
        v.add(Img(emoji_img(emo, 270), W / 2, 700, t0, t1, giris, bob=9))
    faz(*a, c.a, tb, "pop"); v.sfx.append((c.a, "pop")); v.cut(tb); faz(*b, tb, c.t1, "spin"); v.sfx.append((tb + .1, "hit")); v.shake(tb + .15, 22)
    if simsek:
        for k, (dt, x0, x1) in enumerate(((.3, 250, 330), (.62, 840, 760), (.94, 420, 300))):
            v.add(Simsek(tb + dt, x0, 500, x1, 980, seed=k + 3)); v.flashes.append((tb + dt, 120)); v.shake(tb + dt, 32); v.sfx.append((tb + dt - .03, "boom" if k == 0 else "hit"))

def kapi(c, ac=False, tetik=1, kilit=True, etiket=None, ic="❤"):
    v = c.v; tk = c.T(tetik); x, y = W / 2, 720
    if not ac:
        v.add(Glow((255, 200, 90), x, y, 520, c.a, tk, .55))
        v.add(Kapi(x, y, 300, 420, c.a, c.t1, 1.0, [(tk - .16, 0.0, .16)]))
        v.sfx.append((tk - .05, "boom")); v.shake(tk, 38); v.punch.append((tk, .13)); v.flashes.append((tk, 90))
        if kilit: v.add(Img(emoji_img("🔒", 150), x, y + 10, tk + .35, c.t1, "drop")); v.sfx.append((tk + .7, "hit")); v.shake(tk + .73, 16)
        if etiket: v.slam(sticker(etiket, 46, RED, WHITE, rot=5), 790, 930, tk + .75, c.t1, power=.05, sound="pop")
    else:
        v.add(Glow((255, 200, 90), x, y, 560, tk, c.t1, .75, nabiz=.1))
        v.add(Kapi(x, y, 300, 420, c.a, c.t1, 0.0, [(tk, 1.0, .35)]))
        if kilit: v.add(Img(emoji_img("🔒", 140), x, y + 10, c.a + .15, tk, "drop"))
        v.sfx.append((tk, "whoosh")); v.sfx.append((tk + .3, "ding")); v.shake(tk + .1, 18)
        v.add(Img(emoji_img(ic, 180), x + 40, y, tk + .25, c.t1, "pop", pulse=.12)); v.add(Particles(tk + .3, x, y - 40, "confetti", 60, seed=3, spread=.75))
        if etiket: etiket_bas(c, etiket, tk + .5, y=955, size=52)

def salter(c, sol, sag, gecis, son=None):
    v = c.v; G = [(c.T(t) - .06, s) for t, s in gecis]
    v.add(Glow(PINK, W / 2, 700, 560, c.a, c.t1, .4))
    v.add(Anahtar(W / 2, 650, c.a, c.t1, G, sol, sag))
    for t, _ in G: v.sfx.append((t, "hit")); v.shake(t + .06, 14)
    if son: etiket_bas(c, son[0], c.T(son[1]), y=955, size=52, sound="hit", power=.07)

def isik(c, emo, tetik=1, kalabalik=("😐", "😳"), megafon="📣"):
    v = c.v; bag = c.T(tetik) - .1; mx = 830 if c.yan == "l" else 250
    v.add(Spot(W / 2, 500, 850, 500, c.a, c.t1))
    v.add(Img(emoji_img(emo, 230), W / 2, 690, c.a, c.t1, "drop", bob=8)); v.sfx.append((c.a + .35, "hit"))
    for k in range(5):
        x = 220 + k * 160
        v.add(Img(emoji_img(kalabalik[0], 84), x, 940, c.a + .2 + k * .07, bag, "pop")); v.add(Img(emoji_img(kalabalik[1], 94), x, 940, bag, c.t1, "pop"))
    v.add(Img(emoji_img(megafon, 180), mx, 640, bag, c.t1, "spin", pulse=.12))
    v.sfx.append((bag, "boom")); v.shake(bag + .05, 36); v.punch.append((bag + .05, .12)); v.flashes.append((bag + .05, 90))
    for k in range(3): v.add(Shock(bag + .05 + k * .16, mx, 640, YEL, 60, 500, .5, 14))

def sonra(c, emo, sure, balon, tetik=1):
    v = c.v; b = c.T(tetik) - .12
    v.add(Glow(RED, W / 2, 700, 600, c.a, b, .5, nabiz=.15))
    v.add(Img(emoji_img(emo, 260), W / 2, 700, c.a, b, "pop", pulse=.08)); v.sfx.append((c.a, "pop"))
    v.cut(b); v.add(Glow(MOR, W / 2, 700, 600, b, c.t1, .5))
    v.slam(sticker(sure, _tek_satir(sure, 68), YEL, BLACK, rot=-4, maxw=960), W / 2, 640, b, c.t1, power=.1, sound="boom"); v.shake(b + .15, 24)
    v.pop(globals()["balon"](balon, 46, GRI, WHITE, "l", maxw=600), W / 2, 860, b + .55, c.t1, sound="msg")

def yorunge(c, merkez, gezen, davetsiz=None, tetik=1, son="💥", etiket=None, n=3):
    v = c.v; x, y = W / 2, 700
    v.add(Glow(PINK, x, y, 620, c.a, c.t1, .55, nabiz=.15))
    v.add(Img(emoji_img(merkez, 200), x, y, c.a, c.t1, "pop", pulse=.12)); v.sfx += [(c.a + .1, "heart"), (c.a + 1.0, "heart")]
    for k in range(n): v.add(Yorunge(emoji_img(gezen, 104), x, y, 310, 150, c.a + .15, c.t1, 2.8, k * 6.2832 / n))
    if davetsiz:
        gel = c.T(tetik); vur = gel + 1.0
        v.add(Fx(emoji_img(davetsiz, 140), gel, vur, lambda lt: (1180 - 300 * ease(lt / .9), 940, 1, 0, 1)))
        v.add(Glow((230, 40, 40), x, y, 680, vur, c.t1, .6, nabiz=.2)); v.add(Img(emoji_img(son, 170), 880, 940, vur, c.t1, "spin"))
        v.sfx.append((vur - .03, "boom")); v.shake(vur, 40); v.punch.append((vur, .14)); v.flashes.append((vur, 110))
    if etiket: etiket_bas(c, etiket[0], c.T(etiket[1]), y=955, size=50)

def yuksel(c, arka, tetik=1, on="🙂"):
    v = c.v; gel = c.T(tetik) - .1
    v.add(Glow(ALTIN, W / 2, 680, 680, gel, c.t1, .65, nabiz=.15))
    v.add(Fx(emoji_img(arka, 320), gel, c.t1, lambda lt: (W / 2, 670 + 330 * (1 - back(lt / .4, 1.2)), .5 + .5 * ease(lt / .4), 0, min(1, lt * 5))))
    v.add(Img(emoji_img(on, 130), W / 2, 905, c.a, c.t1, "pop", bob=5)); v.add(Img(sticker("sen", 38, WHITE, BLACK, rot=-5), W / 2 + 125, 950, c.a + .25, c.t1, "pop"))
    v.sfx.append((gel, "whoosh")); v.sfx.append((gel + .3, "boom")); v.shake(gel + .35, 38); v.punch.append((gel + .35, .13)); v.flashes.append((gel + .35, 100))

def arsiv(c, baslik, satirlar, damga, tetik=1, once="💬"):
    v = c.v; un = c.T(tetik) - .12
    v.add(Img(emoji_img(once, 250), W / 2, 700, c.a, un, "pop", bob=9)); v.sfx.append((c.a, "pop"))
    v.add(Glow((230, 60, 50), W / 2, 720, 620, un, c.t1, .5, nabiz=.15))
    v.add(Img(dosya(baslik, satirlar, damga), W / 2, 740, un, c.t1, "drop")); v.sfx.append((un + .35, "boom")); v.shake(un + .4, 30); v.punch.append((un + .4, .1))

def gozler(c, merkez, cevre="👀", tetik=1):
    v = c.v; t0 = c.T(tetik)
    v.add(Spot(W / 2, 500, 880, 440, c.a, c.t1))
    v.add(Img(emoji_img(merkez, 230), W / 2, 740, c.a, c.t1, "drop", bob=8)); v.sfx.append((c.a + .35, "hit"))
    for k in range(8):
        ang = -math.pi / 2 + (k + .5) * math.pi / 4; tk = t0 + k * .1
        v.add(Img(emoji_img(cevre, 92), W / 2 + 340 * math.cos(ang), 750 + 200 * math.sin(ang), tk, c.t1, "pop", bob=5)); v.sfx.append((tk, "tick"))
    v.shake(t0 + .7, 16)

def yol(c, giden, hedef, var, etiket=None):
    v = c.v; tv = c.T(var); sure = max(.6, tv - c.a - .2)
    v.add(Glow(GREEN, 250, 720, 420, tv, c.t1, .6, nabiz=.15))
    v.add(Img(emoji_img(hedef, 190), 250, 720, c.a, c.t1, "pop", bob=6)); v.sfx.append((c.a, "pop"))
    v.add(Fx(emoji_img(giden, 180), c.a + .2, c.t1, lambda lt: (860 - 430 * min(1, lt / sure), 730 - 22 * abs(math.sin(lt * 9)) * (lt < sure), 1, 0, min(1, lt * 5))))
    v.sfx.append((tv, "ding")); v.shake(tv, 20); v.add(Shock(tv, 340, 720, YEL, 80, 520, .5, 16)); v.add(Particles(tv, 340, 700, "confetti", 60, seed=2, spread=.7))
    if etiket: etiket_bas(c, etiket, tv + .15, y=955, size=60, sound="hit", power=.08)

def yazi(c, text, damga, tetik=1, renk=RED):
    v = c.v; td = c.T(tetik) - .12
    v.add(Yazi(text, W / 2, 650, c.a, c.t1, c.a + .2, max(c.a + .6, td), mod="yaz", size=50, bg=MAVI, kuyruk="r", maxw=600))
    v.sfx += [(c.a + .2 + k * .85, "type") for k in range(max(1, int((td - c.a) / .85)))]
    damga_bas(c, damga, td, y=850, renk=renk)

def sayac(c, hedef, birim, emo, tetik=1, sure=.9, son=None):
    v = c.v; t0 = c.T(tetik)
    v.add(Glow(ALTIN, W / 2, 700, 600, c.a, c.t1, .45))
    v.add(Img(emoji_img(emo, 210), 290, 700, c.a, c.t1, "pop", bob=8)); v.sfx.append((c.a, "pop"))
    v.add(Sayac(hedef, 700, 670, c.a, c.t1, t0, sure)); v.sfx += [(t0 + sure * k / max(1, min(hedef, 12)), "tick") for k in range(min(hedef, 12) + 1)]
    v.sfx.append((t0 + sure, "hit")); v.shake(t0 + sure, 22)
    v.add(Img(sticker(birim, _tek_satir(birim, 42, 560), (20, 20, 34), WHITE, rot=-2, weight=800), 660, 845, c.a + .2, c.t1, "up"))
    if son: etiket_bas(c, son[0], c.T(son[1]), y=968, size=48, sound="hit", power=.07)

def saganak(c, emo, buyuk, etiket=None):
    v = c.v
    v.add(Glow(ALTIN, W / 2, 700, 620, c.a, c.t1, .5, nabiz=.1))
    v.add(Yagis("kar", c.a, c.t1, (130, 500, 950, 960), 18, seed=4, emo=emo))
    v.add(Img(emoji_img(buyuk, 260), W / 2, 710, c.a, c.t1, "drop", bob=9)); v.sfx.append((c.a + .35, "hit"))
    if etiket: etiket_bas(c, etiket[0], c.T(etiket[1]), y=955, size=50)

def kacis(c, emo, tetik=1, etiket="kayboldu 💨"):
    v = c.v; tk = c.T(tetik)
    v.add(Glow(HAVA, W / 2, 700, 600, c.a, c.t1, .45))
    v.add(Img(emoji_img(emo, 260), W / 2, 700, c.a, tk, "pop", bob=9, out=False)); v.sfx.append((c.a, "pop"))
    v.add(Fx(emoji_img(emo, 260), tk, tk + .45, lambda lt: (W / 2 + 1500 * (lt / .45) ** 2, 700 - 60 * lt, 1, -25 * lt / .45, 1)))
    v.add(Img(emoji_img("💨", 200), W / 2 - 40, 700, tk + .1, tk + 1.0, "pop")); v.sfx.append((tk - .05, "whoosh")); v.shake(tk + .1, 18)
    v.slam(sticker(etiket, _tek_satir(etiket, 64), WHITE, BLACK, rot=-4, maxw=960), W / 2, 740, tk + .55, c.t1, power=.08, sound="hit")

def slot(c, emojiler, tetik=1, etiket=None):
    v = c.v; dur = c.T(tetik)
    v.add(Glow(MOR, W / 2, 700, 620, c.a, c.t1, .5, nabiz=.12))
    v.add(Slot(emojiler, W / 2, 700, c.a, c.t1, dur)); v.sfx += [(c.a + k * .13, "tick") for k in range(int((dur - c.a) / .13))]
    v.sfx.append((dur, "hit")); v.shake(dur + .05, 26); v.punch.append((dur + .05, .09))
    if etiket: etiket_bas(c, etiket, dur + .25, y=955, size=52)

def duzelt(c, emo, tetik=1, etiket="oh. ✅"):
    v = c.v; tk = c.T(tetik); n = tk - c.a
    v.add(Glow(GREEN, W / 2, 700, 600, tk, c.t1, .5))
    v.add(Fx(emoji_img(emo, 300), c.a, c.t1, lambda lt: (W / 2, 700, min(1, .3 + lt * 4), (14 + 2 * math.sin(lt * 6)) if lt < n else 14 * (1 - back((lt - n) / .2, 2.2)), min(1, lt * 6))))
    v.sfx.append((c.a, "pop")); v.sfx.append((tk, "tick")); v.sfx.append((tk + .15, "ding")); v.shake(tk + .1, 14)
    if etiket: etiket_bas(c, etiket, tk + .3, y=955, size=60)

def duvar(c, balonlar, emo="🧱"):
    v = c.v
    for i in range(3):
        for j in range(3): v.add(Img(emoji_img(emo, 120), 690 + j * 112 + (56 if i % 2 else 0) - 28, 580 + i * 108, c.a + (i * 3 + j) * .04, c.t1, "drop"))
    v.sfx.append((c.a + .3, "hit"))
    for k, (text, tet) in enumerate(balonlar):
        t0 = max(c.a + .5, c.T(tet)); y = 600 + k * 95; im = balon(text, 44, MAVI, WHITE, "l", maxw=420)
        def fn(lt, y=y):
            if lt < .28: return (-250 + 640 * ease(lt / .28), y, 1, 0, 1)
            q = lt - .28; return (390 - 330 * q, y + 950 * q * q, 1, 45 * q, max(0., 1 - q / .75))
        v.add(Fx(im, t0, t0 + 1.0, fn)); v.sfx.append((t0, "swish")); v.sfx.append((t0 + .26, "thud")); v.shake(t0 + .28, 12)

def damga(c, emo, text, tetik=1, renk=RED):
    v = c.v
    v.add(Img(emoji_img(emo, 270), W / 2, 690, c.a, c.t1, "pop", bob=9)); v.sfx.append((c.a, "pop"))
    damga_bas(c, text, c.T(tetik) - .12, y=870, renk=renk)

def liste(c, satirlar, son=None):
    v = c.v; y0, adim = 565, 112
    for i, (text, tet) in enumerate(satirlar):
        t = max(c.a, c.T(tet))
        v.add(Img(sticker(text, 44, (30, 30, 46), WHITE, rot=(-3, 2, -2, 3)[i % 4], maxw=820), W / 2 + (-40, 40)[i % 2], y0 + i * adim, t, c.t1, ("left", "right")[i % 2])); v.sfx.append((t, "tick"))
    if son:
        ts = c.T(son[1]) - .1; y = y0 + len(satirlar) * adim + 20
        v.add(Glow(son[2], W / 2, y, 520, ts, c.t1, .5, nabiz=.15))
        v.slam(sticker(son[0], _tek_satir(son[0], 60), son[2], WHITE, rot=-4, maxw=960), W / 2, y, ts, c.t1, power=.1, sound="hit"); v.shake(ts + .15, 20)

SAHNELER = dict(gosterge=gosterge, mesaj=mesaj, donusum=donusum, kapi=kapi, salter=salter, isik=isik, sonra=sonra, yorunge=yorunge,
                yuksel=yuksel, arsiv=arsiv, gozler=gozler, yol=yol, yazi=yazi, sayac=sayac, saganak=saganak, kacis=kacis, slot=slot,
                duzelt=duzelt, duvar=duvar, damga=damga, liste=liste)

# =====================================================================================
# Videonun kurulması
# =====================================================================================
def _satir(text, size, maxw):
    f = mont(size, 900); bos = f.getlength(" ") * .9; n, w = 1, 0
    for k in text.split():
        kw = rich_len(k, f)
        if w and w + bos + kw > maxw: n, w = n + 1, 0
        w += (bos if w else 0) + kw
    return n

def _sigdir(text, size, maxw, satir):
    """Altyazı en fazla `satir` satıra sığana kadar yazıyı küçültür."""
    while size > 40 and _satir(text, size, maxw) > satir: size -= 4
    return size

def _altyazilar(v, cs, t1, ust=1050, alt=1425, maxw=960):
    """Bir maddenin cümlelerini alt alta dizer: satır sayısına göre yer açar, sığmazsa hepsini birlikte küçültür."""
    boy = {1: [84], 2: [76, 58], 3: [70, 58, 54]}[len(cs)]; kis = 0
    while True:
        sz = [_sigdir(u.metin, b - kis, maxw, 3 if len(cs) == 1 else 2) for u, b in zip(cs, boy)]
        h = [_satir(u.metin, z, maxw) * int(z * 1.2) for u, z in zip(cs, sz)]; ara = 54
        if sum(h) + ara * (len(cs) - 1) <= alt - ust or kis >= 24: break
        kis += 4
    y = ust + max(0, (min(330, alt - ust) - sum(h) - ara * (len(cs) - 1)) / 2)
    for u, z, hh in zip(cs, sz, h):
        ws = u.metin.split(); kw = max(ws, key=lambda w: len(sade(w)))
        v.cap(u.metin, {kw}, y + hh / 2, u.kel[0][1], t1, size=z, times=[t for _, t in u.kel], maxw=maxw); y += hh + ara

def kur(spec):
    ad = isim(spec); U0, sure = hizala(spec); gaps = bosluk(spec)
    z = lambda t: t + .15 + sum(d for g, d in gaps if t > g)
    U = copy.deepcopy(U0)
    for u in U: u.t0, u.t1, u.kel = z(u.t0), z(u.t1), [(w, z(t)) for w, t in u.kel]
    b = spec["burc"]; e = spec["cins"] == "e"; _, akk, emo, d1, a1, d2, a2, renk2 = BURC[b]; el = EL[SIGN[b][1]]
    T = z(sure) + .65
    v = Video(T, [el, renk2 if e else (200, 50, 120)], sum(map(ord, ad))); v.voice = ses(ad)
    kes = lambda u: u.t0 - .12
    giris, tarih = U[0], U[1]; sayilar = [u for u in U if u.tur in ("sayi", "numara")]
    soru, etk = U[-2], U[-1]

    # ---- giriş: "Hayatında bir X erkeği mi var?"
    t1 = kes(tarih); k = [t for _, t in giris.kel]
    v.add(Glow(el if e else PINK, W / 2, 620, 680, 0, t1, .62, nabiz=.12))
    v.add(Img(medallion(b, "♂" if e else "♀", 300), W / 2, 480, 0, t1, "pop", dur=.02, bob=8)); v.sfx.append((0.0, "swish"))
    for i in range(3): v.add(Yorunge(emoji_img(emo, 100), W / 2, 480, 330, 140, .05, t1, 3.2, i * 2.094))
    v.cap("Hayatında bir", set(), 700, k[0], t1, size=62, times=k[:2], emph=False)
    bs = 240
    while big(up(b), bs, WHITE).width > 1000: bs -= 10
    v.slam(big(up(b), bs, WHITE), W / 2, 915, k[2] - .12, t1, power=.15, sound="boom"); v.shake(k[2] + .02, 30)
    v.slam(big("ERKEĞİ" if e else "KADINI", 200, YEL), W / 2, 1120, k[3] - .12, t1, power=.1)
    v.slam(sticker("mi var? 👀" if e else "mı var? 👀", 60, WHITE, BLACK, rot=-4), W / 2, 1330, k[4], t1, power=.05, sound="pop")

    # ---- tarih: "21 Mart ile 19 Nisan arasında doğduysa, şu beş şeyi ..."
    v.cut(t1); t2 = kes(sayilar[0]); k = [t for _, t in tarih.kel]
    v.add(Glow(ALTIN, W / 2, 680, 620, t1, t2, .45))
    koyu = tuple(int(x * .72) for x in el)
    aylar = [(a1, AY[a1][0], AY[a1][1], range(d1, AY[a1][1] + 1), el), (a2, AY[a2][0], AY[a2][1], range(1, d2 + 1), koyu)]
    takvim(v, aylar, t1, k[0] + .05, k[3], k[5], t2, y=650)
    yz = f"{d1} {a1} – {d2} {a2}"
    v.cap(yz, {str(d1), str(d2)}, 1120, k[0], t2, size=_sigdir(yz, 78, 1000, 1), times=k[:5], maxw=1000)
    v.cap("arasında doğduysa,", set(), 1230, k[5], t2, size=54, times=k[5:7], emph=False)
    v.slam(sticker("şu 5 şeyi bilmen lazım 👇" if e else "şu 5 şeyi aklına yaz ✍", 62, RED if e else PINK, WHITE, rot=-3, maxw=980),
           W / 2, 1380, k[7] - .12, t2, power=.1, sound="boom"); v.shake(k[7] + .05, 24)

    # ---- beş madde
    for n in range(5):
        su = sayilar[n]; cs = [u for u in U if u.tur == "madde" and u.madde == n]
        son = kes(sayilar[n + 1]) if n < 4 else kes(soru)
        yan = "l" if n % 2 == 0 else "r"; hx = 170 if yan == "l" else 910; t0 = kes(su)
        v.cut(t0)
        if n < 4:
            bekle = max(.4, min(.7, cs[0].t0 - t0 - .1)); sayi(v, 5 - n, t0, son, hx, 400, bekle=bekle); a = t0 + bekle + .1
        else:
            bas = kes(cs[0])
            v.cap("Ve 1 numara...", {"1"}, 880, su.kel[0][1], bas, size=110, gap=.3, times=[t for _, t in su.kel])
            v.ducks.append((t0, bas)); v.sfx.append((bas - 1.5, "riser")); v.cut(bas)
            sayi(v, 1, bas, son, hx, 400, bekle=0, ses="boom"); a = bas + .1
        _, kalip, ayar = spec["maddeler"][n]
        SAHNELER[kalip](Sahne(v, a, son, cs, yan), **ayar)
        _altyazilar(v, cs, son)

    # ---- kapanış
    t9 = kes(soru); v.cut(t9)
    v.add(Glow(el if e else PINK, W / 2, 700, 640, t9, T, .5, nabiz=.1))
    v.add(Img(medallion(b, "♂" if e else "♀", 190), W / 2, 420, t9, T, "spin", bob=8))
    for i in range(2): v.add(Yorunge(emoji_img(emo, 84), W / 2, 420, 250, 90, t9 + .2, T, 2.6, i * 3.1416))
    v.slam(sticker("Tanıdık geldi mi? 👀", 74, WHITE, BLACK, rot=-4, maxw=960), W / 2, 700, t9, T, power=.07, sound="hit")
    k = [t for _, t in etk.kel]; nk = 3 if e else 4
    yz = (f"O {akk} etiketle 👇" if e else f"Bir {b} kadınını etiketle 👇")
    v.cap(yz, {"etiketle"}, 970, k[0], T, size=_sigdir(yz, 84, 940, 2), times=k[:nk], maxw=940)
    v.slam(sticker("bu videoyu da kaydet 📌", 54, YEL, BLACK, rot=3), W / 2, 1230, k[nk] - .1, T, power=.05, sound="pop")
    return v

def hazirla(spec):
    """Video dosyasının dışarı verdiği iki şey: video() ve bosluk()."""
    return (lambda: kur(spec)), (lambda: bosluk(spec))
