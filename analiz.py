#!/usr/bin/env python3
"""ElevenLabs sesini konuşma parçalarına böler; videodaki zamanlamaları buradan alırız.

Kullanım: python analiz.py sesler/<video>.mp3 [esik=0.004] [min_bosluk_sn=0.25]
Çıktı: her konuşma parçasının başlangıç/bitiş saniyesi. Videoda ses 0.15 sn gecikmeyle başlar,
yani senaryoya yazarken bu zamanlara +0.15 ekle.
"""
import sys, subprocess, numpy as np

src = sys.argv[1]; thr = float(sys.argv[2]) if len(sys.argv) > 2 else .004
gap = int(float(sys.argv[3]) * 100) if len(sys.argv) > 3 else 25
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", src, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.int16) / 32768
e = np.array([np.sqrt(np.mean(x[i:i + 320] ** 2)) for i in range(0, len(x) - 320, 160)])
sp = e > thr; segs = []; i = 0; n = len(sp)
while i < n:
    if sp[i]:
        j = i
        while j < n and (sp[j] or (j + gap < n and sp[j:j + gap].any())): j += 1
        segs.append((i / 100, j / 100)); i = j
    else: i += 1
print(f"süre: {len(x) / 16000:.2f} sn")
for k, (a, b) in enumerate(s for s in segs if s[1] - s[0] > .08):
    print(f"{k:2d}  {a:6.2f} – {b:6.2f}  ({b - a:4.2f} sn)")
