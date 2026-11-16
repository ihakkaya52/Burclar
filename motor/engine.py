import math, random, subprocess, wave, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, SR = 1080, 1920, 30, 44100
HERE = os.path.dirname(os.path.abspath(__file__))
ANTON = os.path.join(HERE, "fonts/Anton-Regular.ttf")
MONT = os.path.join(HERE, "fonts/Montserrat-VF.ttf")
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

YEL = (255, 214, 10); WHITE = (255, 255, 255); BLACK = (0, 0, 0)
RED = (235, 64, 52); GREEN = (40, 190, 100); PINK = (255, 92, 150); BLUE = (64, 156, 255)
EL = {"Ateş": (232, 92, 40), "Toprak": (98, 150, 60), "Hava": (60, 150, 215), "Su": (80, 100, 200)}
SIGN = {"Koç": ("♈", "Ateş"), "Boğa": ("♉", "Toprak"), "İkizler": ("♊", "Hava"), "Yengeç": ("♋", "Su"), "Aslan": ("♌", "Ateş"),
        "Başak": ("♍", "Toprak"), "Terazi": ("♎", "Hava"), "Akrep": ("♏", "Su"), "Yay": ("♐", "Ateş"), "Oğlak": ("♑", "Toprak"),
        "Kova": ("♒", "Hava"), "Balık": ("♓", "Su")}
ORDER = list(SIGN)

def make_wheel(size, hi=None, labels=True):
    S = size * 2; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = S / 2; R = S / 2 - 10; r_in = R * .56
    for i, n in enumerate(ORDER):
        col = EL[SIGN[n][1]]; a = 255 if (hi is None or hi == i) else 70
        st = -90 - (i + 1) * 30
        d.pieslice([c - R, c - R, c + R, c + R], st, st + 30, fill=col + (a,), outline=(10, 10, 30, 255), width=6)
    d.ellipse([c - r_in, c - r_in, c + r_in, c + r_in], fill=(18, 20, 50, 255), outline=WHITE + (255,), width=6)
    d.ellipse([c - R - 8, c - R - 8, c + R + 8, c + R + 8], outline=YEL + (255,), width=8)
    gf = dj(int(R * .16)); lf = mont(int(R * .06), 900)
    for i, n in enumerate(ORDER):
        am = math.radians(-90 - i * 30 - 15); rg = (R + r_in) / 2
        gx, gy = c + rg * math.cos(am), c + rg * math.sin(am)
        d.text((gx, gy - (R * .04 if labels else 0)), SIGN[n][0], font=gf, fill=WHITE + (255,), anchor="mm")
        if labels: d.text((gx, gy + R * .1), up(n), font=lf, fill=WHITE + (255,), anchor="mm")
    q = r_in * .45
    d.polygon([(c, c - q), (c + q * .22, c - q * .22), (c + q, c), (c + q * .22, c + q * .22), (c, c + q), (c - q * .22, c + q * .22), (c - q, c), (c - q * .22, c - q * .22)], fill=YEL + (255,))
    return im.resize((size, size), Image.LANCZOS)

class Spin:
    def __init__(s, img, x, y, t0, t1, speed=-14, intro=True):
        s.__dict__.update(img=img, x=x, y=y, t0=t0, t1=t1, speed=speed, intro=intro)
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        lt = t - s.t0; p = lt / .7
        ang = s.speed * lt + (-220 * (1 - ease(p)) if s.intro else 0)
        sc = max(.05, back(p, 1.3)) if s.intro and p < 1 else 1
        a = min(1, p * 3, (s.t1 - t) / .14)
        img = s.img.rotate(ang, resample=Image.BILINEAR)
        if abs(sc - 1) > .003: img = img.resize((max(1, int(img.width * sc)), max(1, int(img.height * sc))), Image.BILINEAR)
        put(dst, img, s.x, s.y, a)

_fc = {}
def anton(s):
    k = ("a", s)
    if k not in _fc: _fc[k] = ImageFont.truetype(ANTON, s)
    return _fc[k]
def mont(s, w=900):
    k = ("m", s, w)
    if k not in _fc:
        f = ImageFont.truetype(MONT, s); f.set_variation_by_axes([w]); _fc[k] = f
    return _fc[k]
def dj(s):
    k = ("d", s)
    if k not in _fc: _fc[k] = ImageFont.truetype(DJ, s)
    return _fc[k]

def ease(t): t = max(0., min(1., t)); return 1 - (1 - t) ** 3
def back(t, c=1.9):
    t = max(0., min(1., t)); return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def up(s): return s.replace("i", "İ").replace("ı", "I").upper()

# ---------------- emoji / rich text ----------------
_em = {}
def is_emoji(ch): o = ord(ch); return o >= 0x1F000 or 0x2600 <= o <= 0x27BF or 0x23E9 <= o <= 0x23FA or ch in "⭐✅❤⌛⌚"
def emoji_img(ch, h):
    if ch not in _em:
        f = ImageFont.truetype(EMOJI, 109)
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
        _em[ch] = im.crop(im.getbbox())
    e = _em[ch]
    return e.resize((max(1, int(e.width * h / e.height)), h), Image.LANCZOS)

def runs(text):
    text = text.replace("️", "").replace("‍", "")
    out = []
    for ch in text:
        e = is_emoji(ch)
        if out and not e and not out[-1][1]: out[-1][0] += ch
        else: out.append([ch, e])
    return out

def rich_len(text, font):
    return sum(int(font.size * 1.12) if e else font.getlength(r) for r, e in runs(text))

def rich(text, font, fill=WHITE, stroke=0, sfill=BLACK, shadow=False):
    asc, desc = font.getmetrics()
    pad = stroke + 6
    w = int(rich_len(text, font) + 2 * pad + 4); h = int(asc + desc + 2 * pad)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x = pad
    for r, e in runs(text):
        if e:
            ei = emoji_img(r, int(font.size * 1.0))
            im.alpha_composite(ei, (int(x + font.size * 0.06), int(pad + (asc + desc - ei.height) / 2)))
            x += font.size * 1.12
        else:
            d.text((x, pad), r, font=font, fill=fill + (255,), stroke_width=stroke, stroke_fill=sfill + (255,), anchor="la")
            x += font.getlength(r)
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel("A").point(lambda v: v * 0.55))
        sh = sh.filter(ImageFilter.GaussianBlur(6)); out = Image.new("RGBA", (w + 8, h + 10), (0, 0, 0, 0))
        out.alpha_composite(sh, (6, 8)); out.alpha_composite(im, (0, 0)); return out
    return im

def words_of(text):
    out = []
    for w_ in text.split():
        if out and all(is_emoji(c) or c in "\ufe0f\u200d" for c in w_): out[-1] += " " + w_
        else: out.append(w_)
    return out

def wrap(text, font, maxw):
    lines, cur = [], ""
    for w_ in words_of(text):
        t = (cur + " " + w_).strip()
        if rich_len(t, font) <= maxw: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def sticker(text, size=62, bg=WHITE, fg=BLACK, rot=-3, maxw=820, weight=900):
    f = mont(size, weight)
    lines = [rich(l, f, fg) for l in wrap(text, f, maxw)]
    tw = max(l.width for l in lines); lh = int(size * 1.18)
    px, py = 34, 20
    w, h = tw + 2 * px, lh * len(lines) + 2 * py + 6
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([24, 28, 20 + w, 24 + h], radius=22, fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(im).rounded_rectangle([20, 20, 20 + w, 20 + h], radius=22, fill=bg + (255,))
    for k, l in enumerate(lines):
        im.alpha_composite(l, (int(20 + w / 2 - l.width / 2), int(20 + py + k * lh - 4)))
    return im.rotate(rot, resample=Image.BICUBIC, expand=True) if rot else im

def card(text, size=50, accent=YEL, maxw=880):
    f = mont(size, 800)
    lines = [rich(l, f, WHITE) for l in wrap(text, f, maxw)]
    tw = max(l.width for l in lines); lh = int(size * 1.25)
    w, h = max(tw + 90, 600), lh * len(lines) + 44
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=26, fill=(8, 8, 20, 185))
    d.rounded_rectangle([0, 0, 12, h - 1], radius=6, fill=accent + (255,))
    for k, l in enumerate(lines): im.alpha_composite(l, (40, 18 + k * lh))
    return im

def medallion(name, gender=None, size=340):
    g, e = SIGN[name]; col = EL[e]; S = size * 2
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([30, 30, S - 30, S - 30], fill=col + (190,))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(40)))
    d = ImageDraw.Draw(im); m = S * .12
    d.ellipse([m, m, S - m, S - m], fill=col + (255,), outline=WHITE + (255,), width=14)
    d.text((S / 2, S / 2 + 4), g, font=dj(int(S * .4)), fill=WHITE + (255,), anchor="mm")
    if gender:
        tint = BLUE if gender == "♂" else PINK; r = S * .14; cx = cy = S - m - r * .5
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE + (255,))
        d.text((cx, cy + 3), gender, font=ImageFont.truetype(DJ.replace("Sans", "Sans-Bold"), int(r * 1.4)), fill=tint + (255,), anchor="mm")
    return im.resize((size, size), Image.LANCZOS)

def mult_alpha(img, a):
    if a >= .999: return img
    im = img.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a))); return im

def put(dst, img, cx, cy, a=1.0):
    if a <= .01: return
    img = mult_alpha(img, a)
    x, y = int(round(cx - img.width / 2)), int(round(cy - img.height / 2))
    x0, y0 = max(0, x), max(0, y); x1, y1 = min(dst.width, x + img.width), min(dst.height, y + img.height)
    if x1 <= x0 or y1 <= y0: return
    dst.alpha_composite(img.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))

# ---------------- clips ----------------
class Img:
    def __init__(s, img, x, y, t0, t1, anim="pop", dur=None, bob=0, pulse=0, out=True, frm=None):
        s.img, s.x, s.y, s.t0, s.t1, s.anim, s.bob, s.pulse, s.out, s.frm = img, x, y, t0, t1, anim, bob, pulse, out, frm
        s.dur = dur or {"pop": .32, "slam": .2, "up": .35, "fade": .4, "left": .38, "right": .38, "spin": .5, "drop": .45}.get(anim, .3)
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        lt = t - s.t0; p = lt / s.dur; sc, a, x, y, rot = 1., 1., s.x, s.y, 0
        if p < 1:
            if s.anim == "pop": sc = max(.05, back(p)); a = min(1, p * 3)
            elif s.anim == "slam": sc = 1 + 1.6 * (1 - ease(p)); a = min(1, p * 4)
            elif s.anim == "up": y += 70 * (1 - ease(p)); a = ease(p)
            elif s.anim == "fade": a = ease(p)
            elif s.anim == "left": x -= 1000 * (1 - ease(p))
            elif s.anim == "right": x += 1000 * (1 - ease(p))
            elif s.anim == "spin": sc = max(.05, back(p)); rot = -200 * (1 - ease(p)); a = min(1, p * 3)
            elif s.anim == "drop": y -= 500 * (1 - back(p, 1.2)); a = min(1, p * 4)
            elif s.anim == "path":
                (fx, fy) = s.frm; k = ease(p); x = fx + (s.x - fx) * k; y = fy + (s.y - fy) * k
        if s.out and s.t1 - t < .14: sc *= .4 + .6 * (s.t1 - t) / .14; a *= (s.t1 - t) / .14
        if s.bob and p >= 1: y += s.bob * math.sin((lt - s.dur) * 2.4)
        if s.pulse and p >= 1:
            ph = (lt - s.dur) % .9; sc *= 1 + s.pulse * (math.exp(-ph * 9) + .6 * math.exp(-max(0, ph - .22) * 9) * (ph > .22))
        img = s.img
        if rot: img = img.rotate(rot, resample=Image.BILINEAR, expand=True)
        if abs(sc - 1) > .003: img = img.resize((max(1, int(img.width * sc)), max(1, int(img.height * sc))), Image.BILINEAR)
        put(dst, img, x, y, a)

class Caption:  # word-by-word kinetic caption
    KW_AMP = 1.0
    def __init__(s, text, kws, y, t0, t1, size=86, gap=.15, maxw=940, hl=YEL, x=W / 2, times=None):
        s.t0, s.t1, s.gap = t0, t1, gap
        f = mont(size, 900); kws = set(kws)
        words = words_of(text); imgs = []; s.kwflags = []
        for w_ in words:
            clean = w_.strip(".,!?…:“”\"")
            iskw = w_ in kws or clean in kws; s.kwflags.append(iskw)
            imgs.append(rich(w_, f, hl if iskw else WHITE, stroke=max(6, size // 11)))
        sp = f.getlength(" ") * .9; lines, cur, cw = [], [], 0
        for im in imgs:
            ww = im.width - 2 * (size // 11 + 6)
            if cur and cw + sp + ww > maxw: lines.append(cur); cur, cw = [], 0
            cur.append(im); cw += (sp if len(cur) > 1 else 0) + ww
        lines.append(cur)
        lh = int(size * 1.2); s.items = []
        y0 = y - lh * (len(lines) - 1) / 2; k = 0
        for li, line in enumerate(lines):
            tot = sum(i.width for i in line) + (sp - 2 * (size // 11 + 6)) * (len(line) - 1)
            xx = x - tot / 2
            for im in line:
                tt_ = times[k] if times else t0 + k * gap
                s.items.append((im, xx + im.width / 2, y0 + li * lh, tt_, s.kwflags[k])); k += 1
                xx += im.width + sp - 2 * (size // 11 + 6)
        s.end_t = (times[-1] + gap) if times else t0 + k * gap
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        fade = min(1, (s.t1 - t) / .14)
        for im, x, y, ts, kw in s.items:
            if t < ts: continue
            if kw: p = (t - ts) / .2; sc = 1 + Caption.KW_AMP * (1 - back(p, 1.2)) if p < 1 else 1
            else: p = (t - ts) / .14; sc = 1 + .4 * (1 - ease(p))
            sc = max(.3, sc)
            img = im if sc < 1.003 else im.resize((int(im.width * sc), int(im.height * sc)), Image.BILINEAR)
            put(dst, img, x, y, min(1, p * 2.5) * fade)

class Shock:
    def __init__(s, t0, x, y, col=YEL, r0=60, r1=420, dur=.45, width=14):
        s.__dict__.update(t0=t0, x=x, y=y, col=col, r0=r0, r1=r1, dur=dur, w=width)
    def draw(s, dst, t):
        p = (t - s.t0) / s.dur
        if not (0 <= p < 1): return
        r = s.r0 + (s.r1 - s.r0) * ease(p); a = int(230 * (1 - p))
        ov = Image.new("RGBA", (int(2 * r + 40), int(2 * r + 40)), (0, 0, 0, 0))
        ImageDraw.Draw(ov).ellipse([20, 20, 20 + 2 * r, 20 + 2 * r], outline=s.col + (a,), width=max(2, int(s.w * (1 - p))))
        put(dst, ov, s.x, s.y)

class Ring:
    def __init__(s, pct, label, col, y, t0, t1, dur=2.0, size=470):
        s.__dict__.update(pct=pct, label=label, col=col, y=y, t0=t0, t1=t1, dur=dur, size=size)
    def val(s, t):
        p = max(0, min(1, (t - s.t0) / s.dur)); return 1 - (1 - p) ** 2.2
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        p = s.val(t); S = s.size * 2; a = int(255 * min(1, (t - s.t0) * 4, (s.t1 - t) / .14))
        im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); th = 64
        bb = [th / 2 + 4, th / 2 + 4, S - th / 2 - 4, S - th / 2 - 4]
        d.ellipse([th, th, S - th, S - th], fill=(5, 5, 18, int(a * .55)))
        d.arc(bb, 0, 360, fill=(255, 255, 255, int(a * .14)), width=th)
        if p > .003: d.arc(bb, -90, -90 + 360 * s.pct / 100 * p, fill=s.col + (a,), width=th)
        d.text((S / 2, S / 2 - 20), f"%{int(round(s.pct * p))}", font=mont(200, 900), fill=WHITE + (a,), anchor="mm", stroke_width=6, stroke_fill=BLACK + (a,))
        d.text((S / 2, S / 2 + 150), s.label, font=mont(46, 900), fill=YEL + (a,), anchor="mm")
        im = im.resize((s.size, s.size), Image.BILINEAR)
        done = t - s.t0 - s.dur
        if 0 <= done < .3: im = im.resize((int(s.size * (1 + .12 * (1 - done / .3))),) * 2, Image.BILINEAR)
        put(dst, im, W / 2, s.y)

class Bars:
    def __init__(s, rows, y, t0, t1, step=.5, width=860):
        s.__dict__.update(rows=rows, y=y, t0=t0, t1=t1, step=step, w=width)
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); x0 = (W - s.w) // 2
        fade = min(1, (s.t1 - t) / .14)
        for k, (lab, pct, col) in enumerate(s.rows):
            ts = s.t0 + k * s.step
            if t < ts: continue
            p = ease((t - ts) / 1.0); a = int(255 * min(1, (t - ts) * 4) * fade)
            y = s.y + k * 175 + int((1 - ease((t - ts) / .35)) * 60)
            d.text((x0, y), lab, font=mont(56, 900), fill=WHITE + (a,), anchor="lm", stroke_width=5, stroke_fill=BLACK + (a,))
            d.text((x0 + s.w, y), f"%{int(round(pct * p))}", font=mont(64, 900), fill=YEL + (a,), anchor="rm", stroke_width=5, stroke_fill=BLACK + (a,))
            d.rounded_rectangle([x0, y + 52, x0 + s.w, y + 96], radius=22, fill=(255, 255, 255, int(a * .18)))
            if p > .01: d.rounded_rectangle([x0, y + 52, x0 + max(44, int(s.w * pct / 100 * p)), y + 96], radius=22, fill=col + (a,))
        dst.alpha_composite(ov)

class Particles:
    def __init__(s, t0, x, y, kind="confetti", n=70, seed=1, spread=1.0):
        rnd = random.Random(seed); s.t0, s.kind, s.ps = t0, kind, []
        cols = [YEL, PINK, BLUE, GREEN, WHITE, (255, 140, 0)]
        for _ in range(n):
            ang = rnd.uniform(-math.pi, 0) if kind != "hearts" else rnd.uniform(-2.6, -.5)
            sp = rnd.uniform(500, 1500) * spread
            s.ps.append(dict(x=x, y=y, vx=math.cos(ang) * sp, vy=math.sin(ang) * sp, r=rnd.uniform(0, 6.28), vr=rnd.uniform(-9, 9),
                             c=rnd.choice(cols), sz=rnd.uniform(12, 26), life=rnd.uniform(1.3, 2.2)))
        if kind == "hearts": s.heart = {k: emoji_img("❤", k) for k in (40, 56, 72)}
    def draw(s, dst, t):
        lt = t - s.t0
        if lt < 0 or lt > 2.3: return
        d = ImageDraw.Draw(dst)
        for p in s.ps:
            if lt > p["life"]: continue
            drag = (1 - math.exp(-2.2 * lt)) / 2.2
            x = p["x"] + p["vx"] * drag; y = p["y"] + p["vy"] * drag + 700 * lt * lt * .5
            a = 1 - max(0, (lt - p["life"] * .6) / (p["life"] * .4))
            if s.kind == "hearts":
                im = s.heart[[40, 56, 72][int(p["sz"]) % 3]]; put(dst, im, x, y, a)
            else:
                r = p["r"] + p["vr"] * lt; w, h = p["sz"], p["sz"] * .5 * abs(math.cos(r * 1.3)) + 3
                pts = [(x + math.cos(r) * dx - math.sin(r) * dy, y + math.sin(r) * dx + math.cos(r) * dy) for dx, dy in [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]]
                d.polygon(pts, fill=p["c"] + (int(255 * a),))

class Chat:
    def __init__(s, title, avatar, msgs, y0, t0, t1):
        s.__dict__.update(msgs=msgs, y0=y0, t0=t0, t1=t1)
        s.panel = Image.new("RGBA", (900, 920), (0, 0, 0, 0)); d = ImageDraw.Draw(s.panel)
        d.rounded_rectangle([0, 0, 899, 919], radius=44, fill=(14, 14, 22, 235))
        d.rounded_rectangle([0, 0, 899, 120], radius=44, fill=(32, 32, 44, 255)); d.rectangle([0, 80, 899, 120], fill=(32, 32, 44, 255))
        s.panel.alpha_composite(avatar.resize((84, 84), Image.LANCZOS), (34, 18))
        ti = rich(title, mont(40, 800), WHITE); s.panel.alpha_composite(ti, (134, 60 - ti.height // 2 - 12))
        d.text((140, 96), "çevrimiçi", font=mont(24, 500), fill=(140, 200, 140, 255), anchor="lm")
        s.bub = []
        for side, txt, ttype, tmsg in msgs:
            f = mont(46, 600); lines = wrap(txt, f, 640)
            li = [rich(l, f, WHITE) for l in lines]; bw = max(l.width for l in li) + 52; bh = 58 * len(li) + 40
            b = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); bd = ImageDraw.Draw(b)
            bd.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=34, fill=((0, 132, 255) if side == "R" else (58, 58, 72)) + (255,))
            for k, l in enumerate(li): b.alpha_composite(l, (24, 14 + k * 58))
            s.bub.append(b)
    def draw(s, dst, t):
        if not (s.t0 <= t < s.t1): return
        lt = t - s.t0; a = min(1, lt * 4, (s.t1 - t) / .14)
        pan = s.panel.copy(); y = 150
        for (side, txt, ttype, tmsg), b in zip(s.msgs, s.bub):
            if t < ttype: break
            x = 870 - b.width if side == "R" else 30
            if t < tmsg:  # typing dots
                ty = Image.new("RGBA", (150, 80), (0, 0, 0, 0)); td = ImageDraw.Draw(ty)
                td.rounded_rectangle([0, 0, 149, 79], radius=34, fill=((0, 132, 255) if side == "R" else (58, 58, 72)) + (255,))
                for k in range(3):
                    off = 8 * math.sin((t - ttype) * 12 - k * .9)
                    td.ellipse([30 + k * 34 - 9, 40 - 9 - off, 30 + k * 34 + 9, 40 + 9 - off], fill=(230, 230, 230, 255))
                pan.alpha_composite(ty, (870 - 150 if side == "R" else 30, y)); break
            p = (t - tmsg) / .25; sc = max(.05, back(p, 1.4))
            bi = b if sc > .999 else b.resize((max(1, int(b.width * sc)), max(1, int(b.height * sc))), Image.BILINEAR)
            ax = x + (b.width - bi.width) * (1 if side == "R" else 0); pan.alpha_composite(bi, (int(ax), int(y + (b.height - bi.height))))
            y += b.height + 22
        put(dst, pan, W / 2, s.y0 + 460, a)

# ---------------- video builder ----------------
class Video:
    def __init__(s, total, cols, seed):
        s.total, s.cols, s.seed = total, cols, seed
        s.clips, s.sfx, s.punch, s.shakes, s.flashes, s.cuts, s.ducks = [], [], [], [], [], [], []
    def add(s, c): s.clips.append(c); return c
    def slam(s, img, x, y, t, t1, power=.07, sound="hit", flash=True, **kw):
        s.add(Img(img, x, y, t, t1, "slam", **kw)); s.punch.append((t + .15, power)); s.sfx.append((t + .12, sound))
        s.add(Shock(t + .15, x, y, YEL, 80, 620, .5, 18))
        if flash: s.flashes.append((t + .15, 90))
    def pop(s, img, x, y, t, t1, sound="pop", anim="pop", **kw):
        s.add(Img(img, x, y, t, t1, anim, **kw))
        if sound: s.sfx.append((t, sound))
    def cap(s, text, kws, y, t, t1, size=86, gap=.15, emph=True, **kw):
        c = s.add(Caption(text, kws, y, t, t1, size, gap, **kw))
        if emph:
            for im, x, yy, ts, k in c.items:
                if k:
                    s.punch.append((ts + .05, .05 if size > 70 else .03)); s.shake(ts + .05, 12 if size > 70 else 7)
                    s.sfx.append((ts, "thud")); s.add(Shock(ts + .02, x, yy, YEL, 40, 300, .35, 10))
        return c.end_t
    def sub(s, text, y, t, t1, size=52, maxw=900):
        f = mont(size, 700); ls = wrap(text, f, maxw)
        for k, l in enumerate(ls):
            s.add(Img(rich(l, f, WHITE, stroke=6), W / 2, y + k * size * 1.3, t + k * .12, t1, "up"))
    def cut(s, t): s.cuts.append(t); s.sfx.append((t - .2, "whoosh"))
    def shake(s, t, amp=26): s.shakes.append((t, amp))

    # ---------- audio ----------
    def audio(s, path):
        n = int(s.total * SR); tt = np.arange(n) / SR
        mus = music(s.total, s.seed)
        g = np.ones(n)
        for a, b in s.ducks:
            i0, i1 = int(a * SR), int(b * SR); ramp = int(.08 * SR)
            g[i0:i1] = .12
            g[max(0, i0 - ramp):i0] = np.linspace(1, .12, len(g[max(0, i0 - ramp):i0]))
        voice = getattr(s, "voice", None)
        if voice is not None:
            vw = wave.open(voice); vx = np.frombuffer(vw.readframes(vw.getnframes()), np.int16).astype(float) / 32768
            v = np.zeros(n); m_ = min(n, len(vx)); v[:m_] = vx[:m_]
            env = np.convolve(np.abs(v), np.ones(int(.25 * SR)) / (.25 * SR), mode="same")
            env = np.convolve(env, np.ones(int(.3 * SR)) / (.3 * SR), mode="same")
            g = g * (1 - .62 * np.clip(env / (env.max() * .25 + 1e-9), 0, 1))
        mix = mus * g * .55
        for t, k in s.sfx:
            snd = SFX[k](); i = int(max(0, t) * SR); j = min(n, i + len(snd)); mix[i:j] += snd[:j - i]
        if voice is not None:
            mix = mix / (np.abs(mix).max() + 1e-9) * .5
            mix = v / (np.abs(v).max() + 1e-9) * .92 + mix * .62
        fade = np.clip(np.minimum(tt / .05, (s.total - tt) / .6), 0, 1); mix *= fade
        mix = np.tanh(mix * 1.1) / np.tanh(1.1); mix = mix / (np.abs(mix).max() + 1e-9) * .92
        st = (np.stack([mix, np.roll(mix, 180)], 1) * 32767).astype(np.int16)
        with wave.open(path, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())

    # ---------- video ----------
    def prepare(s):
        BW, BH = int(W * 1.18), int(H * 1.18)
        gy = np.linspace(0, 1, BH)[:, None]
        top, bot = np.array([6, 6, 22]), np.array([26, 24, 62])
        arr = (top + (bot - top) * gy[..., None]).repeat(BW, axis=1).astype(np.uint8)
        bg = Image.fromarray(arr, "RGB").convert("RGBA")
        glow = Image.new("RGBA", (BW, BH), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        pos = [(BW * .15, BH * .25), (BW * .9, BH * .75), (BW * .5, BH * .5)]
        for (x, y), c in zip(pos, (s.cols * 3)[:3]):
            gd.ellipse([x - 560, y - 560, x + 560, y + 560], fill=c + (85,))
        bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(170)))
        d = ImageDraw.Draw(bg); rnd = random.Random(s.seed)
        for _ in range(650):
            x, y = rnd.uniform(0, BW), rnd.uniform(0, BH); r = rnd.choice([.8, 1, 1.3, 1.7, 2.4]); v = rnd.randint(80, 235)
            d.ellipse([x - r, y - r, x + r, y + r], fill=(v, v, min(255, v + 18), 255))
        s.bg = bg.convert("RGB")
        yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W * .72)) ** 2 + ((yy - H / 2) / (H * .62)) ** 2)
        v = np.clip((r - .55) * 1.4, 0, 1) ** 1.6 * 200
        s.vig = Image.fromarray(np.dstack([np.zeros((H, W, 3)), v]).astype(np.uint8), "RGBA")
        g = np.random.default_rng(s.seed)
        s.grain = []
        for _ in range(5):
            nz = g.integers(0, 255, (H // 2, W // 2), dtype=np.uint8)
            im = Image.fromarray(np.dstack([nz, nz, nz, np.full_like(nz, 9)]), "RGBA").resize((W, H), Image.NEAREST)
            s.grain.append(im)
        s.tw = [(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(5, 10), rnd.uniform(0, 6.3), rnd.uniform(1.5, 3)) for _ in range(22)]

    def frame(s, t):
        # background: slow push-in + drift + a bit of punch
        z = 1.0 + .07 * t / s.total + sum(p * .4 * math.exp(-(t - tp) * 9) for tp, p in s.punch if 0 <= t - tp < .6)
        cw, ch = W * 1.18 / (1.18 * z) * 1.0, H / z
        cw, ch = W / z * 1.0, H / z * 1.0
        cx = s.bg.width / 2 + 40 * math.sin(t * .23); cy = s.bg.height / 2 + 60 * math.sin(t * .17)
        bgf = s.bg.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.BILINEAR).convert("RGBA")
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        for (x, y, sz, ph, sp) in s.tw:
            a = .25 + .75 * (.5 + .5 * math.sin(t * sp + ph)); q = sz
            d.polygon([(x, y - q), (x + q * .2, y - q * .2), (x + q, y), (x + q * .2, y + q * .2), (x, y + q), (x - q * .2, y + q * .2), (x - q, y), (x - q * .2, y - q * .2)], fill=(255, 238, 200, int(255 * a)))
        bgf.alpha_composite(ov)
        # content
        cont = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for c in s.clips: c.draw(cont, t)
        zc = 1 + sum(p * math.exp(-(t - tp) * 10) for tp, p in s.punch if 0 <= t - tp < .5)
        ox = oy = 0.
        for ts, amp in s.shakes:
            if 0 <= t - ts < .55:
                k = amp * math.exp(-(t - ts) * 7); ox += k * math.sin(t * 91); oy += k * math.cos(t * 73)
        blur = 0
        for tc in s.cuts:
            dt = t - tc
            if -.1 <= dt < 0: oy -= 520 * ease((dt + .1) / .1); blur = max(blur, 1 + 8 * ease((dt + .1) / .1))
            elif 0 <= dt < .12: oy += 520 * (1 - ease(dt / .12)); blur = max(blur, 1 + 8 * (1 - dt / .12))
        if blur > 1.5:
            f = int(blur); cont = cont.resize((W // f, H // f), Image.BILINEAR).resize((W, H), Image.BILINEAR)
        if zc > 1.002:
            nw, nh = int(W * zc), int(H * zc); big = cont.resize((nw, nh), Image.BILINEAR)
            x0 = (nw - W) / 2 - ox; y0 = (nh - H) / 2 - oy
            cont2 = Image.new("RGBA", (W, H), (0, 0, 0, 0)); put(cont2, big, W / 2 + (nw - W) / 2 - x0, H / 2 + (nh - H) / 2 - y0); cont = cont2
        elif abs(ox) + abs(oy) > .5:
            cont2 = Image.new("RGBA", (W, H), (0, 0, 0, 0)); put(cont2, cont, W / 2 + ox, H / 2 + oy); cont = cont2
        bgf.alpha_composite(cont)
        bgf.alpha_composite(s.vig)
        bgf.alpha_composite(s.grain[(int(t * FPS) // 3) % len(s.grain)])
        fl = 0
        for tf, amt in s.flashes:
            if 0 <= t - tf < .12: fl = max(fl, amt * (1 - (t - tf) / .12))
        for tc in s.cuts:
            if abs(t - tc) < .06: fl = max(fl, 150 * (1 - abs(t - tc) / .06))
        if fl > 1: bgf.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(fl))))
        return bgf.convert("RGB")

    def render(s, out):
        s.prepare(); wav = out + ".wav"; s.audio(wav); tmp = out[:-4] + ".part.mp4"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
               "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-maxrate", "12M", "-bufsize", "24M", "-pix_fmt", "yuv420p", "-profile:v", "high",
               "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", tmp]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for i in range(int(s.total * FPS)): p.stdin.write(s.frame(i / FPS).tobytes())
        p.stdin.close()
        if p.wait() == 0: os.replace(tmp, out)
        os.remove(wav); return out

# ---------------- sound design ----------------
_rng = np.random.default_rng(7)
def _t(d): return np.arange(int(d * SR)) / SR
def _noise(d): return _rng.uniform(-1, 1, int(d * SR))
def _lp(x, k):  # simple moving average lowpass
    k = max(1, int(k)); return np.convolve(x, np.ones(k) / k, mode="same")
def s_hit():
    t = _t(.9); f = 48 + 90 * np.exp(-t * 22)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5)
    clk = _lp(_noise(.9), 3) * np.exp(-t * 40) * .5
    return (body * .9 + clk) * .9
def s_whoosh():
    d = .42; t = _t(d); n = _noise(d)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    hi = n - _lp(n, 6); lo = _lp(n, 40)
    k = t / d; x = hi * k + lo * (1 - k) * 1.6
    return x * env * .5
def s_pop():
    t = _t(.12); f = 500 + 900 * (t / .12)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 35) * .45
def s_tick():
    t = _t(.03); return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 180) * .3
def s_riser():
    d = 1.6; t = _t(d); f = 180 + 900 * (t / d) ** 2
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * .25
    n = _noise(d); n = n - _lp(n, 4)
    return (tone + n * .25) * (t / d) ** 2.2 * .8
def s_ding():
    t = _t(1.4); x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * dcy) for f, a, dcy in [(1046.5, .5, 3), (1568, .3, 4), (2093, .2, 5), (3136, .1, 7)])
    return x * .6
def s_msg():
    t = _t(.14); f = 820 + 700 * np.minimum(1, t / .05)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 25) * .45
def s_type():
    out = np.zeros(int(.9 * SR)); r = random.Random(3); x = 0.
    while x < .8:
        i = int(x * SR); c = _lp(_noise(.02), 2) * np.exp(-_t(.02) * 260) * .25; out[i:i + len(c)] += c[:len(out) - i]; x += r.uniform(.07, .13)
    return out
def s_beep():
    t = _t(.55); return np.sign(np.sin(2 * np.pi * 1000 * t)) * .22 * np.minimum(1, t / .01) * np.clip((.55 - t) / .02, 0, 1)
def s_heart():
    t = _t(.6)
    def th(t0):
        tt = np.clip(t - t0, 0, None); return np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 16) * (t >= t0)
    return (th(0) + .7 * th(.22)) * .9
def s_boom():
    t = _t(2.0); f = 38 + 60 * np.exp(-t * 6)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2) + _lp(_noise(2), 30) * np.exp(-t * 5) * .6) * .95
def s_swish():
    d = .22; t = _t(d); n = _noise(d); return (n - _lp(n, 3)) * np.sin(np.pi * t / d) ** 2 * .25
def s_thud(): return s_hit()[:int(.5 * SR)] * .45
SFX = dict(thud=s_thud, hit=s_hit, whoosh=s_whoosh, pop=s_pop, tick=s_tick, riser=s_riser, ding=s_ding, msg=s_msg, type=s_type,
           beep=s_beep, heart=s_heart, boom=s_boom, swish=s_swish)

def music(dur, seed, bpm=112):
    n = int(dur * SR); t = np.arange(n) / SR; out = np.zeros(n)
    nf = lambda m: 440 * 2 ** ((m - 69) / 12); beat = 60 / bpm; bar = beat * 4
    prog = [[57, 60, 64], [53, 57, 60], [50, 53, 57], [52, 56, 59]]  # Am F Dm E
    kick = s_hit()[:int(.35 * SR)] * .55
    rnd = random.Random(seed)
    for b in range(int(dur / beat) + 1):
        i = int(b * beat * SR)
        if b % 4 in (0, 2) or (b % 8 == 7):
            j = min(n, i + len(kick))
            if i < n: out[i:j] += kick[:j - i]
        if b % 4 in (1, 3):
            c = _noise(.18); c = (c - _lp(c, 3)) * np.exp(-_t(.18) * 22) * .22; j = min(n, i + len(c))
            if i < n: out[i:j] += c[:j - i]
        for h in (0, .5):
            ih = int((b + h) * beat * SR); c = _noise(.05); c = (c - _lp(c, 2)) * np.exp(-_t(.05) * 90) * (.07 if h else .04)
            j = min(n, ih + len(c))
            if ih < n: out[ih:j] += c[:j - ih]
    for k in range(int(dur / bar) + 2):
        st = k * bar; ch = prog[k % 4]; m = (t >= st) & (t < st + bar); tt = t[m] - st
        env = np.minimum(tt / .3, 1) * np.clip((bar - tt) / .3, 0, 1)
        for nn in ch: out[m] += env * np.sin(2 * np.pi * nf(nn) * tt + np.sin(2 * np.pi * 5 * tt) * .3) * .03
        for q in range(8):
            m2 = (t >= st + q * beat / 2) & (t < st + q * beat / 2 + beat / 2); tt2 = t[m2] - st - q * beat / 2
            out[m2] += np.sin(2 * np.pi * nf(ch[0] - 24) * tt2) * np.exp(-tt2 * 6) * .13
        for q in range(8):
            if rnd.random() < .55:
                st2 = st + q * beat / 2; m3 = (t >= st2) & (t < st2 + .5); tt3 = t[m3] - st2
                out[m3] += np.sin(2 * np.pi * nf(rnd.choice(ch) + 12) * tt3) * np.exp(-tt3 * 9) * .05
    return out / (np.abs(out).max() + 1e-9)
