# Burç Serisi – Instagram Reels üretici

Burç videolarını (1080×1920, 30 fps, Instagram Reels formatı) seslendirmeyle senkronlu olarak üreten araç.
Animasyonlar, altyazılar, ses efektleri ve fon müziği tamamen kodla üretilir. Dışarıdan görsel ya da müzik kullanılmaz.

## Klasörler

| Klasör / dosya | İçerik |
|---|---|
| `motor/engine.py` | Animasyon motoru: arka plan, altyazılar, etiketler, uyum halkası, puan çubukları, mesajlaşma ekranı, konfeti, ses efektleri, müzik |
| `motor/yardimci.py` | Ortak yardımcılar (`big`, `spread`, `soften`, `ses`, `zaman`) |
| `motor/kalip.py` | Tek burç videolarının ortak kalıbı: metin, otomatik zamanlama, sahne kalıpları, kurulum |
| `motor/sahne.py` | Hareketli sahne parçaları: takvim, gösterge, kapı, şalter, ses dalgası, yazan balon, şimşek, yağış |
| `videolar/*.py` | Her videonun senaryosu: hangi yazının, hangi saniyede, hangi efektle çıkacağı |
| `sesler/*.mp3` | ElevenLabs'tan alınan orijinal seslendirmeler |
| `aciklamalar/*.txt` | Her videonun Instagram açıklaması |
| `metinler/*.txt` | Seslendirme metinleri (ElevenLabs'a yapıştırılan halleri) |
| `render.py` | Sesi hazırlar ve videoyu üretir |
| `analiz.py` | Sesi konuşma parçalarına böler, zamanlamaları çıkarır |
| `kurulum.sh` | ffmpeg, Python paketleri ve fontları kurar |

## Kurulum

```bash
./kurulum.sh
```

Gerekenler: Python 3, ffmpeg, numpy, Pillow, DejaVu ve Noto Color Emoji fontları,
Anton ve Montserrat (kurulum betiği `motor/fonts/` klasörüne indirir).

## Kullanım

```bash
python render.py liste                          # mevcut videolar
python render.py koc_erkegi                     # cikti/koc_erkegi.mp4
python render.py koc_erkegi --onizleme 3,10,20  # belirtilen saniyelerden kare (cikti/onizleme_koc_erkegi.png)
python render.py hepsi                          # bütün videolar
```

Bitmiş videolar `cikti/` klasörüne yazılır ve Git'e eklenmez (çok büyükler). Ses seviyesi Instagram'ın
standardına (-14 LUFS) göre ayarlanır.

## Yeni video ekleme

1. **Metin:** `metinler/<video>.txt` dosyasına seslendirme metnini yaz. Duraklama istenen yerlere `…` koy.
2. **Ses:** Metni ElevenLabs'ta seslendir, MP3'ü `sesler/<video>.mp3` olarak kaydet.
3. **Zamanlama:** `python analiz.py sesler/<video>.mp3` komutuyla konuşma parçalarını çıkar ve her
   parçayı metindeki cümleyle eşleştir. Ses sessiz başlıyorsa ya da bölümler birbirine yapışıksa eşiği
   değiştir (`python analiz.py sesler/x.mp3 0.012 0.12`). Videoda ses 0,15 sn gecikmeyle başlar, bu
   yüzden senaryoya geçen her zamana +0,15 ekle.
4. **Senaryo:** Benzer bir videoyu kopyala (`videolar/koc_erkegi.py` ya da
   `videolar/boga_erkek_x_balik_kadin.py`) ve zamanları yeni sese göre güncelle.
5. **Kontrol ve üretim:** `python render.py <video> --onizleme ...` ile kareleri kontrol et, sonra
   `python render.py <video>` ile videoyu üret.

Bir şakaya ya da gerilim anına ek sessizlik gerekiyorsa, `render.py` içindeki `BOSLUK` sözlüğüne
`(saniye, süre)` olarak ekle. Saniye, orijinal MP3'teki zamandır.

## Video türleri

- **"5 şey" geri sayımı** (tek burç): 12 burç × erkek/kadın, `<burc>_erkegi` ve `<burc>_kadini`. Hareketli vurgu kullanır.
  Burcun adıyla açılır, tarih aralığı takvimle gelir, her maddenin kendi hareketli sahnesi vardır.
  Akrep ve Aslan elle yazıldı; diğerleri `motor/kalip.py` ile bir `SPEC`'ten kurulur.
  (`boga` eski kalıptaki cinsiyetsiz Boğa videosudur; yerini `boga_erkegi` ve `boga_kadini` aldı.)
- **Aşk uyumu**: giriş, uyum halkası, neden çekilirler, sorun, mesajlaşma, puanlar, formül, kapanış.
- **Arkadaşlık**: çarpışmalı giriş, uyum halkası, iyi taraf, kötü taraf (şaka), puanlar, sonuç, kapanış.
- **Genel**: `burclar_genel`. 12 burç ve tarihleri.

Sakin vurgu için senaryonun sonunda `soften(v)` çağrılır: sarsıntılar hafifler, patlama sesleri
kaldırılır, anahtar kelimeler daha az büyür.
