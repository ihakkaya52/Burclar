"""Videolarda ortak kullanılan küçük yardımcılar."""
import os
from engine import rich, anton, Shock

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def big(text, size, col, stroke=12):
    """Anton fontuyla, kenarlıklı ve gölgeli büyük başlık."""
    return rich(text, anton(size), col, stroke=stroke, shadow=True)

def spread(segs):
    """[(başlangıç, bitiş, kelime_sayısı), ...] -> her kelimenin ekrana geleceği zaman."""
    out = []
    for a, b, n in segs:
        g = (b - a) * .85 / n; out += [a + i * g for i in range(n)]
    return out

def soften(v):
    """Sakin vurgu ayarı: daha hafif sarsıntı/zoom/parlama, patlama sesi yok."""
    v.punch = [(t, p * .45) for t, p in v.punch]
    v.shakes = [(t, a * .4) for t, a in v.shakes]
    v.flashes = [(t, a * .35) for t, a in v.flashes]
    v.sfx = [(t, "hit" if k == "boom" else k) for t, k in v.sfx]
    v.clips = [c for c in v.clips if not (isinstance(c, Shock) and c.r1 == 300)]

def ses(isim):
    """sesler/<isim>.mp3 dosyasından hazırlanan işlenmiş ses (build/sesler/<isim>.wav)."""
    return os.path.join(KOK, "build", "sesler", isim + ".wav")
