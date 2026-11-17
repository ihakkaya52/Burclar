#!/usr/bin/env python3
"""Burç serisi video üretici.

Kullanım:
  python render.py liste                       # mevcut videoları listeler
  python render.py <video>                     # sesi hazırlar ve videoyu cikti/<video>.mp4 olarak üretir
  python render.py <video> --onizleme 3,8.5,20 # verilen saniyelerden kare alır (cikti/onizleme_<video>.png)
  python render.py hepsi                       # bütün videoları üretir
"""
import sys, os, subprocess, importlib

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(KOK, "motor"))
sys.path.insert(0, os.path.join(KOK, "videolar"))

# Sese eklenen boşluklar: {video: [(saniye, eklenecek_sessizlik), ...]}  (orijinal mp3 zamanına göre)
BOSLUK = {
    "ikizler_erkek_x_akrep_erkek_arkadaslik": [(24.40, 1.4)],   # "İkizler de hemen…" sonrası sansür şakası
    "akrep_erkegi": [(25.70, 0.6)],                             # "Ve bir numara…" sonrası gerilim
    "akrep_kadini": [(26.42, 0.6), (30.10, 0.35)],              # "Ve bir numara…" sonrası + "geçmiş olsun" öncesi
    "aslan_erkegi": [(25.46, 0.6)],                             # "Ve bir numara…" sonrası gerilim
    "aslan_kadini": [(25.22, 0.6)],                             # "Ve bir numara…" sonrası gerilim
}
ON_SESSIZLIK_MS = 150
TEMIZLIK = "highpass=f=80,acompressor=threshold=-20dB:ratio=3.5:attack=4:release=80:makeup=2,loudnorm=I=-15:TP=-1.5:LRA=7"

def videolar():
    return sorted(f[:-3] for f in os.listdir(os.path.join(KOK, "videolar")) if f.endswith(".py"))

def ses_hazirla(isim, gaps=None):
    src = os.path.join(KOK, "sesler", isim + ".mp3")
    dst = os.path.join(KOK, "build", "sesler", isim + ".wav")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    gaps = BOSLUK.get(isim, []) if gaps is None else gaps
    if not gaps:
        fc = f"[0]adelay={ON_SESSIZLIK_MS},{TEMIZLIK}[o]"
    else:
        parts, labels, prev = [], [], 0.0
        n = len(gaps) + 1
        fc = f"[0]asplit={n}" + "".join(f"[s{i}]" for i in range(n)) + ";"
        for i, (t, d) in enumerate(gaps + [(None, None)]):
            trim = f"atrim=start={prev}" + (f":end={t}" if t is not None else "")
            fc += f"[s{i}]{trim},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=mono[p{i}];"
            labels.append(f"[p{i}]")
            if t is not None:
                fc += f"anullsrc=r=44100:cl=mono,atrim=0:{d}[z{i}];"; labels.append(f"[z{i}]")
                prev = t
        fc += "".join(labels) + f"concat=n={len(labels)}:v=0:a=1,adelay={ON_SESSIZLIK_MS},{TEMIZLIK}[o]"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-filter_complex", fc, "-map", "[o]",
                    "-ar", "44100", "-ac", "1", dst], check=True)
    return dst

def yap(isim, onizleme=None):
    m = importlib.import_module(isim)
    ses_hazirla(isim, m.bosluk() if hasattr(m, "bosluk") else None)   # kalıp videoları boşluğu kendisi hesaplar
    v = m.video()
    os.makedirs(os.path.join(KOK, "cikti"), exist_ok=True)
    if onizleme:
        from PIL import Image
        v.prepare()
        fr = [v.frame(t).resize((360, 640)) for t in onizleme]
        o = Image.new("RGB", (360 * len(fr), 640))
        for i, f in enumerate(fr): o.paste(f, (i * 360, 0))
        out = os.path.join(KOK, "cikti", f"onizleme_{isim}.png"); o.save(out); print(out); return
    tmp = os.path.join(KOK, "build", isim + ".ham.mp4")
    v.render(tmp)
    out = os.path.join(KOK, "cikti", isim + ".mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-map", "0:v", "-map", "0:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-ar", "44100", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", out], check=True)
    os.remove(tmp); print(out)

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "liste":
        print("\n".join(videolar())); sys.exit()
    hedef = videolar() if a[0] == "hepsi" else [a[0]]
    on = [float(x) for x in a[a.index("--onizleme") + 1].split(",")] if "--onizleme" in a else None
    for isim in hedef: yap(isim, on)
