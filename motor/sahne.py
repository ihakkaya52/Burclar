"""Hareketli sahne parçaları: takvim, gösterge, kapı, anahtar, ses dalgası, yazan balon, şimşek, yağış, yörünge.

Hepsi motor/engine.py içindeki klipler gibi çalışır: `v.add(Parca(...))` ile videoya eklenir, `draw(dst, t)` ile çizilir.
"""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from engine import *
from yardimci import big

GUNLER = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]

def _gir_cik(t, t0, t1, gir=.2, cik=.14): return max(0., min(1., (t - t0) / gir, (t1 - t) / cik))
def _kar(a, b, p): return tuple(int(x + (y - x) * max(0., min(1., p))) for x, y in zip(a, b))
def _olcek(im, sc):
    return im if abs(sc - 1) < .004 else im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)

# ---------------- genel ----------------
class Fx:
    """Serbest hareketli görsel. fn(geçen_süre) -> (x, y, ölçek, açı, alfa)."""
    def __init__(s, img, t0, t1, fn): s.img, s.t0, s.t1, s.fn, s._c = img, t0, t1, fn, (None, None)
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        x, y, sc, rot, a = s.fn(t - s.t0)
        key = (round(sc, 3), round(rot, 1))
        if s._c[0] != key:
            im = s.img.rotate(rot, resample=Image.BILINEAR, expand=True) if abs(rot) > .05 else s.img
            s._c = (key, _olcek(im, sc))
        put(dst, s._c[1], x, y, a * min(1, (s.t1 - t) / .14))

class Glow:
    """Sahnenin arkasına yumuşak renk lekesi: her sahnenin kendi havası olsun diye."""
    def __init__(s, col, x, y, r, t0, t1, a=.6, nabiz=0):
        yy, xx = np.mgrid[0:96, 0:96]; d = np.sqrt((xx - 47.5) ** 2 + (yy - 47.5) ** 2) / 47.5
        al = (np.clip(1 - d, 0, 1) ** 1.7 * 255).astype(np.uint8)
        im = Image.fromarray(np.dstack([np.full_like(al, col[0]), np.full_like(al, col[1]), np.full_like(al, col[2]), al]), "RGBA")
        s.img = im.resize((int(2 * r), int(2 * r)), Image.BILINEAR)
        s.x, s.y, s.t0, s.t1, s.a, s.nabiz = x, y, t0, t1, a, nabiz
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        k = 1 + s.nabiz * math.sin((t - s.t0) * 5)
        put(dst, s.img, s.x, s.y, s.a * k * _gir_cik(t, s.t0, s.t1, .3, .2))

class Yorunge:
    """Bir merkezin etrafında dönen görsel."""
    def __init__(s, img, cx, cy, rx, ry, t0, t1, hiz=2.0, faz=0.):
        s.__dict__.update(img=img, cx=cx, cy=cy, rx=rx, ry=ry, t0=t0, t1=t1, hiz=hiz, faz=faz)
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        lt = t - s.t0; ang = s.faz + s.hiz * lt
        sc = max(.05, back(lt / .35)) if lt < .35 else 1
        put(dst, _olcek(s.img, sc), s.cx + s.rx * math.cos(ang), s.cy + s.ry * math.sin(ang), _gir_cik(t, s.t0, s.t1, .15))

# ---------------- takvim ----------------
class Takvim:
    """Ay yaprağı. `isaret` listesindeki günler m0–m1 arasında sırayla boyanır.
    ilk: ayın 1'i haftanın kaçıncı günü (0 = Pazartesi). cik: yaprağın yukarı çevrilip kaybolduğu an."""
    def __init__(s, ay, ilk, gun, isaret, x, y, t0, t1, m0, m1, col=RED, w=720, giris="pop", cik=None, rot=-2):
        s.__dict__.update(isaret=list(isaret), x=x, y=y, t0=t0, t1=t1, m0=m0, m1=m1, col=col, giris=giris, cik=cik, rot=rot)
        s.cw = (w - 48) / 7; s.rh = 84; ust = 196; h = ust + 6 * s.rh + 26
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=38, fill=(250, 248, 242, 255))
        d.rounded_rectangle([0, 0, w - 1, 128], radius=38, fill=col + (255,)); d.rectangle([0, 92, w - 1, 128], fill=col + (255,))
        for rx in (w * .2, w * .8): d.ellipse([rx - 13, 15, rx + 13, 41], fill=(250, 248, 242, 255))
        d.text((w / 2, 70), up(ay), font=anton(84), fill=WHITE + (255,), anchor="mm")
        for k, g in enumerate(GUNLER):
            d.text((24 + s.cw * (k + .5), 162), g, font=mont(27, 800), fill=(150, 150, 162, 255), anchor="mm")
        s.pos = {}
        for g in range(1, gun + 1):
            i = ilk + g - 1; cx, cy = 24 + s.cw * (i % 7 + .5), ust + s.rh * (i // 7 + .5)
            s.pos[g] = (cx, cy)
            d.text((cx, cy), str(g), font=mont(38, 800), fill=(44, 44, 58, 255), anchor="mm")
        s.base = im
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        im = s.base.copy(); d = ImageDraw.Draw(im); n = len(s.isaret)
        for k, g in enumerate(s.isaret):
            ts = s.m0 + (s.m1 - s.m0) * k / max(1, n - 1)
            if t < ts: break
            p = min(1, (t - ts) / .12); cx, cy = s.pos[g]; r = (s.rh / 2 - 7) * (1 + .45 * (1 - ease(p)))
            d.rounded_rectangle([cx - s.cw / 2 + 3, cy - r, cx + s.cw / 2 - 3, cy + r], radius=20, fill=s.col + (255,),
                                outline=YEL + (255,) if k in (0, n - 1) else None, width=6)
            d.text((cx, cy), str(g), font=mont(40, 900), fill=WHITE + (255,), anchor="mm")
        lt = t - s.t0; a = min(1, (s.t1 - t) / .14); y = s.y
        if s.giris == "pop" and lt < .25: im = _olcek(im, .84 + .16 * back(lt / .25, 1.4))
        if s.cik is not None and t >= s.cik:
            q = ease((t - s.cik) / .24)
            if q >= .97: return
            nh = max(2, int(im.height * (1 - q))); y = s.y - im.height / 2 + nh / 2 - 70 * q
            im = im.resize((im.width, nh), Image.BILINEAR)
        if s.rot: im = im.rotate(s.rot, resample=Image.BILINEAR, expand=True)
        put(dst, im, s.x, y, a)

# ---------------- gösterge / anahtar / dalga ----------------
class Meter:
    """Dolan çubuk: f0 anında dolmaya başlar, yeşilden kırmızıya döner, dolunca titrer."""
    def __init__(s, etiket, x, y, w, t0, t1, f0, fdur=.8, hedef=100, c0=GREEN, c1=RED):
        s.__dict__.update(etiket=etiket, x=x, y=y, w=w, t0=t0, t1=t1, f0=f0, fdur=fdur, hedef=hedef, c0=c0, c1=c1)
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        p = ease((t - s.f0) / s.fdur) if t > s.f0 else 0.; col = _kar(s.c0, s.c1, p)
        Wi, Hi = s.w + 60, 190
        im = Image.new("RGBA", (Wi, Hi), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, Wi - 1, Hi - 1], radius=36, fill=(8, 8, 20, 205))
        et = rich(s.etiket, mont(40, 900), WHITE); im.alpha_composite(et, (26, 54 - et.height // 2))
        d.text((Wi - 32, 54), f"%{int(round(s.hedef * p))}", font=mont(56, 900), fill=col + (255,), anchor="rm")
        d.rounded_rectangle([30, 104, Wi - 30, 160], radius=28, fill=(255, 255, 255, 46))
        if p > .01: d.rounded_rectangle([30, 104, 30 + max(56, int(s.w * min(1, s.hedef / 100) * p)), 160], radius=28, fill=col + (255,))
        lt = t - s.t0; x = s.x; son = t - s.f0 - s.fdur
        if lt < .3: im = _olcek(im, max(.05, back(lt / .3)))
        if 0 <= son < .5: x += 9 * math.sin(t * 85) * (1 - son / .5)
        put(dst, im, x, s.y, _gir_cik(t, s.t0, s.t1, .12))

class Anahtar:
    """İki uçlu şalter. gecis: [(an, 0|1)]. İlk geçişe kadar ortada titrer (ortası yok)."""
    def __init__(s, x, y, t0, t1, gecis, sol="HİÇ", sag="HEP", w=520, h=180, c_sol=(74, 78, 104), c_sag=PINK):
        s.__dict__.update(x=x, y=y, t0=t0, t1=t1, gecis=gecis, sol=sol, sag=sag, w=w, h=h, c_sol=c_sol, c_sag=c_sag)
        s.fs = 58 if max(len(sol), len(sag)) <= 5 else 44
    def konum(s, t):
        v = prev = .5
        for tm, hedef in s.gecis:
            if t >= tm: v = prev + (hedef - prev) * back((t - tm) / .18, 2.4)
            prev = hedef
        return v
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        v = s.konum(t); once = t < s.gecis[0][0]; m = 200; Wi, Hi = s.w + 2 * m, s.h + 150
        im = Image.new("RGBA", (Wi, Hi), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([m, 10, m + s.w, 10 + s.h], radius=s.h // 2, fill=_kar(s.c_sol, s.c_sag, v) + (255,), outline=WHITE + (255,), width=8)
        r = s.h / 2 - 18; kx = m + s.h / 2 + max(-.08, min(1.08, v)) * (s.w - s.h) + (7 * math.sin(t * 60) if once else 0); ky = 10 + s.h / 2
        d.ellipse([kx - r + 4, ky - r + 8, kx + r + 4, ky + r + 8], fill=(0, 0, 0, 90))
        d.ellipse([kx - r, ky - r, kx + r, ky + r], fill=WHITE + (255,))
        for lab, lx, on in ((s.sol, m + s.h / 2, v < .3 and not once), (s.sag, m + s.w - s.h / 2, v > .7 and not once)):
            d.text((lx, s.h + 82), lab, font=mont(int(s.fs * 1.3) if on else s.fs, 900), fill=(YEL if on else (200, 200, 215)) + (255,), anchor="mm",
                   stroke_width=7, stroke_fill=BLACK + (255,))
        lt = t - s.t0
        if lt < .3: im = _olcek(im, max(.05, back(lt / .3)))
        put(dst, im, s.x, s.y + 60, _gir_cik(t, s.t0, s.t1, .12))

class Sayac:
    """Sıfırdan hedefe sayan dev rakam."""
    def __init__(s, hedef, x, y, t0, t1, f0, sure=.9, size=280, col=YEL):
        s.__dict__.update(hedef=hedef, x=x, y=y, t0=t0, t1=t1, f0=f0, sure=sure)
        s.im = [big(str(k), size, col, 14) for k in range(hedef + 1)]
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        p = max(0., min(1., (t - s.f0) / s.sure)); k = int(round(s.hedef * p)); im = s.im[k]
        adim = s.sure / max(1, s.hedef); son = (t - s.f0) - k * adim if 0 < p else 9
        if 0 <= son < .12: im = _olcek(im, 1 + .25 * (1 - son / .12))
        put(dst, im, s.x, s.y, _gir_cik(t, s.t0, s.t1, .15))

class Slot:
    """Hızla dönen emojiler; `dur` anında sonuncuda durur."""
    def __init__(s, emojiler, x, y, t0, t1, dur, h=250, adim=.13):
        s.__dict__.update(x=x, y=y, t0=t0, t1=t1, dur=dur, adim=adim)
        s.im = [emoji_img(e, h) for e in emojiler]
        z = Image.new("RGBA", (h + 120, h + 110), (0, 0, 0, 0))
        ImageDraw.Draw(z).rounded_rectangle([0, 0, h + 119, h + 109], radius=46, fill=(8, 8, 20, 205), outline=YEL + (255,), width=8); s.zemin = z
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        a = _gir_cik(t, s.t0, s.t1, .15); put(dst, s.zemin, s.x, s.y, a)
        if t >= s.dur:
            lt = t - s.dur; put(dst, _olcek(s.im[-1], 1 + .3 * (1 - ease(lt / .2)) if lt < .2 else 1), s.x, s.y, a); return
        k = int((t - s.t0) / s.adim); fr = ((t - s.t0) % s.adim) / s.adim
        put(dst, s.im[k % (len(s.im) - 1)], s.x, s.y - 40 + 80 * fr, a * min(1, fr * 3, (1 - fr) * 3))

class Dalga:
    """Ses dalgası çubukları (dinliyor / kaydediyor hissi)."""
    def __init__(s, x, y, w, h, t0, t1, n=19, col=WHITE, seed=3):
        r = random.Random(seed)
        s.__dict__.update(x=x, y=y, w=w, h=h, t0=t0, t1=t1, n=n, col=col)
        s.b = [(r.uniform(5, 11), r.uniform(0, 6.3), math.exp(-((k - (n - 1) / 2) / (n * .33)) ** 2)) for k in range(n)]
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        im = Image.new("RGBA", (s.w, s.h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); bw = s.w / s.n
        gir = ease((t - s.t0) / .3)
        for k, (f, ph, env) in enumerate(s.b):
            hh = s.h * (.1 + .9 * abs(math.sin(t * f + ph)) * env) * gir; cx = bw * (k + .5)
            d.rounded_rectangle([cx - bw * .3, s.h / 2 - hh / 2, cx + bw * .3, s.h / 2 + hh / 2], radius=int(bw * .3), fill=s.col + (255,))
        put(dst, im, s.x, s.y, _gir_cik(t, s.t0, s.t1, .12))

# ---------------- kapı ----------------
class Kapi:
    """Kapı. aciklik 1 = ardına kadar açık, 0 = kapalı. hareket: [(an, hedef_açıklık, süre)]."""
    def __init__(s, x, y, w, h, t0, t1, acik0, hareket, ahsap=(132, 82, 48), isik=(255, 226, 130)):
        s.__dict__.update(x=x, y=y, w=w, h=h, t0=t0, t1=t1, acik0=acik0, hareket=hareket, ahsap=ahsap)
        ic = Image.new("RGBA", (w, h), isik + (255,))
        par = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(par).ellipse([w * .15, h * .1, w * .85, h * .9], fill=(255, 255, 255, 230))
        ic.alpha_composite(par.filter(ImageFilter.GaussianBlur(w // 7))); s.ic = ic
    def aciklik(s, t):
        v = prev = s.acik0
        for tm, hedef, dur in s.hareket:
            if t >= tm: v = prev + (hedef - prev) * min(1., (t - tm) / dur) ** 2
            prev = hedef
        return v
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        a = s.aciklik(t); k = 22; Wi, Hi = s.w + 2 * k, s.h + k
        im = Image.new("RGBA", (Wi, Hi), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, Wi - 1, Hi - 1], radius=18, fill=(58, 34, 20, 255))
        im.paste(s.ic, (k, k))
        pw = int(s.w * (1 - .84 * a)); g = 1 - .4 * a; c = tuple(int(v * g) for v in s.ahsap); c2 = tuple(int(v * g * .72) for v in s.ahsap)
        d.rectangle([k, k, k + pw, k + s.h], fill=c + (255,))
        m = max(6, int(pw * .14))
        if pw > 60:
            d.rounded_rectangle([k + m, k + s.h * .07, k + pw - m, k + s.h * .45], radius=10, outline=c2 + (255,), width=8)
            d.rounded_rectangle([k + m, k + s.h * .52, k + pw - m, k + s.h * .93], radius=10, outline=c2 + (255,), width=8)
        d.ellipse([k + pw - m - 26, k + s.h * .5 - 14, k + pw - m + 2, k + s.h * .5 + 14], fill=YEL + (255,))
        lt = t - s.t0
        if lt < .3: im = _olcek(im, max(.05, back(lt / .3)))
        put(dst, im, s.x, s.y, _gir_cik(t, s.t0, s.t1, .12))

# ---------------- balonlar ----------------
def _balon_zemin(bw, bh, bg, kuyruk):
    im = Image.new("RGBA", (bw, bh + 24), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=40, fill=bg + (255,))
    if kuyruk == "l": d.polygon([(34, bh - 6), (78, bh - 6), (22, bh + 22)], fill=bg + (255,))
    elif kuyruk == "r": d.polygon([(bw - 34, bh - 6), (bw - 78, bh - 6), (bw - 22, bh + 22)], fill=bg + (255,))
    return im

def balon(text, size=48, bg=(58, 58, 72), fg=WHITE, kuyruk="l", maxw=640):
    """Hazır mesaj balonu (emoji destekli). Img ile ekrana getirilir."""
    f = mont(size, 700); li = [rich(l, f, fg) for l in wrap(text, f, maxw)]; lh = int(size * 1.22)
    bw, bh = max(l.width for l in li) + 52, lh * len(li) + 44
    im = _balon_zemin(bw, bh, bg, kuyruk)
    for k, l in enumerate(li): im.alpha_composite(l, (26, 16 + k * lh))
    return im

class Yazi:
    """İçindeki metin r0–r1 arasında harf harf gelen balon.
    mod="yaz": klavyeden yazılıyormuş gibi. mod="coz": önce noktalarla gizli, sonra çözülür."""
    def __init__(s, text, x, y, t0, t1, r0, r1, mod="yaz", size=50, bg=(58, 58, 72), fg=WHITE, kuyruk="l", maxw=700):
        s.__dict__.update(x=x, y=y, t0=t0, t1=t1, r0=r0, r1=r1, mod=mod, fg=fg)
        s.f = mont(size, 700); s.lines = wrap(text, s.f, maxw); s.lh = int(size * 1.25)
        s.n = sum(len(l) for l in s.lines)
        s.zemin = _balon_zemin(int(max(s.f.getlength(l) for l in s.lines)) + 84, s.lh * len(s.lines) + 50, bg, kuyruk)
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        n = int(s.n * max(0., min(1., (t - s.r0) / (s.r1 - s.r0)))); im = s.zemin.copy(); d = ImageDraw.Draw(im); k = 0
        for i, l in enumerate(s.lines):
            m = max(0, min(len(l), n - k)); k += len(l)
            txt = l[:m] + ("".join(" " if c == " " else "•" for c in l[m:]) if s.mod == "coz" else "")
            if s.mod == "yaz" and m < len(l) and n >= k - len(l) and int(t * 4) % 2 == 0: txt += "|"
            d.text((40, 22 + i * s.lh), txt, font=s.f, fill=s.fg + (255,))
        lt = t - s.t0
        if lt < .28: im = _olcek(im, max(.05, back(lt / .28)))
        put(dst, im, s.x, s.y, _gir_cik(t, s.t0, s.t1, .1))

def dosya(baslik, satirlar, damga=None, w=640):
    """Arşiv kartı: başlık şeridi + satırlar (+ sağ altta kırmızı damga)."""
    f = mont(40, 700); lh = 62; h = 110 + lh * len(satirlar) + 40 + (96 if damga else 0)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=30, fill=(248, 244, 232, 255))
    d.rounded_rectangle([0, 0, w - 1, 92], radius=30, fill=(40, 42, 60, 255)); d.rectangle([0, 60, w - 1, 92], fill=(40, 42, 60, 255))
    b = rich(baslik, mont(44, 900), WHITE); im.alpha_composite(b, (28, 46 - b.height // 2))
    for k, l in enumerate(satirlar):
        r = rich(l, f, (40, 40, 54)); im.alpha_composite(r, (30, 112 + k * lh))
    if damga:
        st = Image.new("RGBA", (w, 110), (0, 0, 0, 0)); sd = ImageDraw.Draw(st); tw = int(mont(46, 900).getlength(damga)) + 48
        sd.rounded_rectangle([w - tw - 30, 12, w - 30, 92], radius=14, outline=RED + (255,), width=7)
        sd.text((w - 30 - tw / 2, 52), damga, font=mont(46, 900), fill=RED + (255,), anchor="mm")
        im.alpha_composite(st.rotate(4, resample=Image.BICUBIC), (0, h - 116))
    return im

class Yaziyor:
    """"Yazıyor…" balonu: zıplayan üç nokta."""
    def __init__(s, x, y, t0, t1, bg=(58, 58, 72), kuyruk="l"):
        s.x, s.y, s.t0, s.t1 = x, y, t0, t1; s.zemin = _balon_zemin(230, 120, bg, kuyruk)
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        im = s.zemin.copy(); d = ImageDraw.Draw(im); lt = t - s.t0
        for k in range(3):
            off = 12 * math.sin(lt * 11 - k * .9)
            d.ellipse([58 + k * 56 - 15, 60 - 15 - off, 58 + k * 56 + 15, 60 + 15 - off], fill=(235, 235, 240, 255))
        if lt < .28: im = _olcek(im, max(.05, back(lt / .28)))
        put(dst, im, s.x, s.y, _gir_cik(t, s.t0, s.t1, .1))

class Spot:
    """Tepeden inen sahne ışığı (yumuşak kenarlı huzme) ve yerdeki ışık halkası."""
    def __init__(s, x, y_ust, y_alt, w_alt, t0, t1, col=(255, 236, 160), a=.5, sallan=0):
        h = int(y_alt - y_ust); w = int(w_alt + 80)
        im = Image.new("RGBA", (w, h + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.polygon([(w / 2 - 36, 0), (w / 2 + 36, 0), (w - 40, h), (40, h)], fill=col + (150,))
        d.ellipse([40, h - 46, w - 40, h + 46], fill=col + (190,))
        s.img = im.filter(ImageFilter.GaussianBlur(16)); s.x, s.y, s.t0, s.t1, s.a, s.sallan = x, (y_ust + y_alt) / 2 + 40, t0, t1, a, sallan
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        lt = t - s.t0; im = s.img
        if s.sallan: im = im.rotate(s.sallan * math.sin(lt * 2.2), resample=Image.BILINEAR, center=(im.width / 2, 0))
        put(dst, im, s.x, s.y, s.a * _gir_cik(t, s.t0, s.t1, .25, .15) * (.85 + .15 * math.sin(lt * 9)))

# ---------------- hava olayları ----------------
class Simsek:
    def __init__(s, t, x0, y0, x1, y1, seed=1, dur=.3):
        r = random.Random(seed); n = 7
        s.pts = [(x0 + (x1 - x0) * k / n + (r.uniform(-70, 70) if 0 < k < n else 0), y0 + (y1 - y0) * k / n) for k in range(n + 1)]
        j = s.pts[3]; s.dal = [j, (j[0] + r.choice([-1, 1]) * 110, j[1] + 110), (j[0] + r.choice([-1, 1]) * 150, j[1] + 230)]
        s.t, s.dur = t, dur
    def draw(s, dst, t):
        lt = t - s.t
        if not (0 <= lt < s.dur): return
        a = (1 - lt / s.dur) * (.55 + .45 * (int(lt * 30) % 2 == 0)); ov = Image.new("RGBA", dst.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        for pts, w in ((s.pts, 1), (s.dal, .6)):
            d.line(pts, fill=(170, 190, 255, int(110 * a)), width=int(30 * w), joint="curve")
            d.line(pts, fill=(255, 255, 225, int(255 * a)), width=int(11 * w), joint="curve")
        dst.alpha_composite(ov)

class Yagis:
    """Kutu içinde düşen kar (❄) ya da yağmur çizgileri."""
    def __init__(s, tur, t0, t1, kutu, n=26, seed=1, emo="❄"):
        r = random.Random(seed); s.tur, s.t0, s.t1, s.kutu = tur, t0, t1, kutu
        s.ps = [(r.uniform(0, 1), r.uniform(0, 1), r.uniform(.6, 1.4), r.uniform(0, 6.3), r.randrange(3)) for _ in range(n)]
        if tur == "kar": s.im = [emoji_img(emo, k) for k in (30, 44, 60)]
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        x0, y0, x1, y1 = s.kutu; bw, bh = x1 - x0, y1 - y0; lt = t - s.t0; fa = _gir_cik(t, s.t0, s.t1, .3, .2)
        if s.tur == "kar":
            for fx, fy, sp, ph, k in s.ps:
                yr = (fy * bh + 190 * sp * lt) % bh; kenar = min(1, yr / 90, (bh - yr) / 90)
                put(dst, s.im[k], x0 + fx * bw + 34 * math.sin(lt * 1.4 + ph), y0 + yr, fa * kenar)
        else:
            ov = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
            for fx, fy, sp, ph, k in s.ps:
                yr = (fy * bh + 1500 * sp * lt) % bh; x = (fx * bw + yr * .22) % bw; kenar = min(1, yr / 120, (bh - yr) / 120)
                d.line([(x, yr), (x + 12, yr + 54)], fill=(190, 212, 255, int(190 * fa * kenar)), width=5)
            dst.alpha_composite(ov, (int(x0), int(y0)))

# ---------------- sahne kalıpları ----------------
def sayi(v, n, t0, t1, hx, hy, bekle=.7, ses="hit"):
    """Geri sayım rakamı: önce ekranın ortasına çarpar, söylenince küçülüp köşeye (hx, hy) uçar.
    bekle=0 verilirse doğrudan köşeye çarpar."""
    img = big(str(n), 400, YEL, 16); cy = 640; k = .42
    def fn(lt):
        if bekle <= 0:
            p = lt / .2; return (hx, hy, k * (1 + 1.6 * (1 - ease(p))), -8, min(1, p * 4))
        if lt < .2: p = lt / .2; return (W / 2, cy, 1 + 1.6 * (1 - ease(p)), 0, min(1, p * 4))
        if lt < bekle: return (W / 2, cy, 1, 0, 1)
        q = ease((lt - bekle) / .32)
        return (W / 2 + (hx - W / 2) * q, cy + (hy - cy) * q, 1 - (1 - k) * q, -8 * q, 1)
    v.add(Fx(img, t0, t1, fn))
    mx, my = (hx, hy) if bekle <= 0 else (W / 2, cy)
    v.punch.append((t0 + .15, .12)); v.sfx.append((t0 + .12, ses)); v.shake(t0 + .15, 20); v.flashes.append((t0 + .15, 90))
    v.add(Shock(t0 + .15, mx, my, YEL, 80, 620 if bekle > 0 else 300, .5, 18))
    if bekle > 0: v.sfx.append((t0 + bekle, "swish"))

def takvim(v, aylar, t0, t_ilk, t_cevir, t_son, t1, y=670):
    """Tarih aralığı takvimi: ilk ayın günleri boyanır, yaprak çevrilir, ikinci ayın günleri boyanır.
    aylar: [(ad, ayın_1'i_haftanın_kaçıncı_günü, gün_sayısı, boyanacak_günler, renk), (ikinci ay için aynısı)]."""
    (a1, i1, g1, m1, c1), (a2, i2, g2, m2, c2) = aylar; m1, m2 = list(m1), list(m2)
    v.add(Takvim(a2, i2, g2, m2, W / 2, y, t_cevir - .05, t1, t_cevir + .12, t_son, col=c2, giris="yok", rot=1.5))
    v.add(Takvim(a1, i1, g1, m1, W / 2, y, t0, t1, t_ilk, t_cevir - .12, col=c1, cik=t_cevir, rot=-2))
    v.sfx += [(t_ilk + k * (t_cevir - .12 - t_ilk) / max(1, len(m1) - 1), "tick") for k in range(len(m1))]
    v.sfx.append((t_cevir - .05, "whoosh"))
    v.sfx += [(t_cevir + .12 + k * (t_son - t_cevir - .12) / max(1, len(m2) - 1), "tick") for k in range(0, len(m2), 2)]
    v.punch.append((t_cevir + .05, .05)); v.shake(t_cevir + .05, 10)

# 2026 takvimine göre: (ad, ayın 1'inin günü [0 = Pzt], gün sayısı, burcun günleri, renk)
AKREP = [("Ekim", 3, 31, range(23, 32), (200, 60, 50)), ("Kasım", 6, 30, range(1, 22), (150, 40, 90))]
ASLAN = [("Temmuz", 2, 31, range(23, 32), (232, 92, 40)), ("Ağustos", 5, 31, range(1, 23), (214, 150, 20))]

def takvim_giris(v, t_ilk, t_cevir, t_son, t1, y=670):
    """Akrep takvimi, videonun ilk karesinden başlar (akrep_erkegi ve akrep_kadini kullanır)."""
    takvim(v, AKREP, 0, t_ilk, t_cevir, t_son, t1, y)
