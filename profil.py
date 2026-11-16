#!/usr/bin/env python3
"""Instagram profil resmi adayları üretir: cikti/profil_a.png, profil_b.png, profil_c.png (1080×1080).
Instagram resmi daire olarak kırpar; önemli her şey ortadaki dairenin içinde durur."""
import sys, os, math, random
KOK = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(KOK, "motor"))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from engine import make_wheel, dj, YEL, WHITE, EL, SIGN, ORDER

S = 1080

def zemin(renkler, seed):
    gy = np.linspace(0, 1, S)[:, None]; top, bot = np.array([8, 7, 26]), np.array([34, 26, 78])
    bg = Image.fromarray((top + (bot - top) * gy[..., None]).repeat(S, axis=1).astype(np.uint8), "RGB").convert("RGBA")
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    for (x, y), c in zip([(.2, .25), (.85, .8), (.5, .5)], renkler):
        gd.ellipse([x * S - 420, y * S - 420, x * S + 420, y * S + 420], fill=c + (110,))
    bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(130)))
    d = ImageDraw.Draw(bg); r = random.Random(seed)
    for _ in range(260):
        x, y = r.uniform(0, S), r.uniform(0, S); q = r.choice([1, 1.4, 2, 2.8]); v = r.randint(110, 240)
        d.ellipse([x - q, y - q, x + q, y + q], fill=(v, v, min(255, v + 15), 255))
    return bg

def yildiz(d, cx, cy, q, col):
    k = .2
    d.polygon([(cx, cy - q), (cx + q * k, cy - q * k), (cx + q, cy), (cx + q * k, cy + q * k), (cx, cy + q), (cx - q * k, cy + q * k), (cx - q, cy), (cx - q * k, cy - q * k)], fill=col + (255,))

def a():  # burç çarkı
    im = zemin([EL["Su"], (150, 30, 70), (60, 40, 140)], 3)
    w = make_wheel(860, labels=False)
    g = Image.new("RGBA", (S, S), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([90, 90, S - 90, S - 90], fill=YEL + (90,))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(50))); im.alpha_composite(w, ((S - 860) // 2,) * 2)
    return im

def b():  # altın hilal ve yıldız
    im = zemin([(120, 50, 190), (200, 60, 120), (40, 60, 160)], 7)
    g = Image.new("RGBA", (S, S), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([250, 250, 830, 830], fill=YEL + (120,))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(70)))
    ay = Image.new("RGBA", (S * 2, S * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(ay)
    d.ellipse([460, 460, 1700, 1700], fill=YEL + (255,)); d.ellipse([760, 380, 1880, 1500], fill=(0, 0, 0, 0))
    im.alpha_composite(ay.resize((S, S), Image.LANCZOS))
    d = ImageDraw.Draw(im); yildiz(d, 690, 470, 120, WHITE); yildiz(d, 800, 690, 46, YEL); yildiz(d, 560, 300, 34, WHITE)
    return im

def c():  # ortada yıldız, etrafında 12 burç simgesi
    im = zemin([(232, 92, 40), EL["Su"], (150, 40, 90)], 11); d = ImageDraw.Draw(im)
    g = Image.new("RGBA", (S, S), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([340, 340, 740, 740], fill=YEL + (150,))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(70))); d = ImageDraw.Draw(im)
    d.ellipse([150, 150, S - 150, S - 150], outline=YEL + (255,), width=6)
    for i, n in enumerate(ORDER):
        ang = math.radians(-90 + i * 30); x, y = S / 2 + 330 * math.cos(ang), S / 2 + 330 * math.sin(ang)
        d.ellipse([x - 58, y - 58, x + 58, y + 58], fill=EL[SIGN[n][1]] + (255,), outline=WHITE + (255,), width=5)
        d.text((x, y + 2), SIGN[n][0], font=dj(64), fill=WHITE + (255,), anchor="mm")
    yildiz(d, S / 2, S / 2, 190, YEL)
    return im

if __name__ == "__main__":
    os.makedirs(os.path.join(KOK, "cikti"), exist_ok=True); out = []
    for ad, f in (("a", a), ("b", b), ("c", c)):
        im = f().convert("RGB"); im.save(os.path.join(KOK, "cikti", f"profil_{ad}.png")); out.append(im)
    # Instagram'daki daire kırpmasıyla yan yana önizleme
    sheet = Image.new("RGB", (3 * 400 + 80, 480), (18, 18, 22))
    m = Image.new("L", (360, 360), 0); ImageDraw.Draw(m).ellipse([0, 0, 359, 359], fill=255)
    for k, im in enumerate(out): sheet.paste(im.resize((360, 360), Image.LANCZOS), (60 + k * 400, 60), m)
    sheet.save(os.path.join(KOK, "cikti", "profil_onizleme.png")); print("cikti/profil_a.png, profil_b.png, profil_c.png")
