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
