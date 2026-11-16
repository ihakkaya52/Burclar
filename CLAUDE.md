# Burç Serisi – Claude için çalışma notları

Bu repo, Harun'un Instagram'da paylaştığı burç Reels serisini üretir. Harun ile **Türkçe** konuş.
Kurulum ve komutlar için `README.md` dosyasına bak.

## Serinin planı

- **12 burç × erkek** ve **12 burç × kadın** için tek burç videoları ("5 şey" geri sayımı)
- **Arkadaşlık videoları:** bir burcun erkeği ile diğer burçların erkekleri
- **Aşk uyumu videoları:** bir burcun erkeği ile diğer burçların kadınları
- Bir de genel video var: `burclar_genel`, 12 burç ve tarihleri

Bitenleri görmek için `python render.py liste` komutunu çalıştır, ya da `videolar/` klasörüne bak.

## Her video için iş akışı

1. Harun bir video ister, örneğin "Koç erkeği" ya da "Boğa erkeği ve Balık kadını".
2. **Seslendirme metnini yaz** ve cevapta **tek paragraf** halinde ver. Harun bölümlere ayrılmış hali değil, tek metin istiyor.
   Metni `metinler/<video>.txt` dosyasına da kaydet. Önce sadece metni ver. Harun sesi ElevenLabs'ta kendisi üretip MP3 olarak gönderir.
3. Gelen MP3'ü `sesler/<video>.mp3` olarak kaydet.
4. **Zamanlamayı çıkar:** `python analiz.py sesler/<video>.mp3` (varsayılan eşik 0.004, boşluk 0.25 sn).
   - Her parçayı hece sayısına bakarak metindeki cümleyle eşleştir. Konuşma hızı yaklaşık 0,13–0,17 sn/hece.
   - Parçalar birbirine yapışıksa daha küçük eşik ya da boşlukla tekrar bak.
   - **Dikkat:** Bir keresinde sesin başındaki kısık cümleyi sessizlik sanıp kestim ve bütün senkron bir bölüm kaydı. Sesin başını mutlaka kontrol et.
   - Videoda ses 0,15 sn gecikmeyle başlar: senaryodaki her zamana +0,15 ekle.
5. **Senaryoyu yaz:** Benzer bir videoyu kopyala (`videolar/*.py`) ve zamanları güncelle.
   - Sayı ve isim çarpmaları, sahne kesmeleri (`v.cut`) söylenen kelimeden yaklaşık 0,12 sn önce olmalı.
   - Altyazı kelimeleri konuşmayla aynı anda çıkar: `times=spread([(başlangıç, bitiş, kelime_sayısı)])`.
6. **Kontrol et:** `python render.py <video> --onizleme t1,t2,...` ile en kalabalık anlardan kare al ve bak. Yazı taşması, üst üste binme ve kutu olarak görünen emoji olup olmadığını kontrol et.
7. **Üret:** `python render.py <video>` ve `cikti/<video>.mp4` dosyasını Harun'a gönder. Cevapta kısaca hangi anların sesle nasıl eşleştiğini anlat.

## Harun'un tercihleri

- **Instagram Reels:** 1080×1920. İçerik Instagram arayüzünün kapatmadığı güvenli alanda kalmalı: üst yaklaşık 300 px ve alt yaklaşık 420 px boş kalmalı.
- **Yapay zekâ yapımı gibi görünmesin:**
  - Günlük, samimi Türkçe kullan ("kanka", "Tanıdık geldi mi? 👀").
  - "SONUÇ" ya da "TAVSİYE" gibi resmi başlıklar kullanma.
  - CapCut tarzı kelime kelime altyazılar, hafif eğik etiketler ve film greni kullan.
- **Videonun sonunda bir sonraki videoyu duyurma.** Kapanış her zaman etiketle ve kaydet çağrısıdır.
- **Vurgu seviyesi:**
  - "5 şey" videoları hareketli ayarda yapılır.
  - Aşk ve arkadaşlık videoları sakin ayarda yapılır: senaryonun sonunda `soften(v)` çağrılır. Harun bir keresinde "vurguyu, patlamaları azalt" dedi.
  - Harun başka bir şey söylerse ona uy.
- **Şakalar:**
  - Aşk videolarında mesajlaşma ekranı (`Chat`) var. Şaka son mesajda patlar.
  - Arkadaşlık videolarında "kötü taraf" bölümünde bir gag var: sansür bip sesi, "1 GÜN SONRA…" sayacı gibi.
  - Şakanın oturması için gereken sessizliği `render.py` içindeki `BOSLUK` sözlüğüne ekle.
- **Uyum puanları:** Astrolojide yaygın kabul gören eşleşmelere göre temsili değerler.

## Teknik tuzaklar

- **📅 ve 🗓 emojileri:** Görselde İngilizce "July 17" yazısıyla çıkıyor. Kullanma, yerine ⏰ ya da Türkçe tarih etiketi kullan.
- **Kutu olarak çıkan emojiler:** 🍽 ve 📋 gibi bazı emojiler kutu olarak görünüyor. Önizlemede kontrol et.
- **Uzun etiketler:** `sticker()` metni sarar. Tek satırda kalması gerekiyorsa font boyutunu düşür ya da `maxw` değerini büyüt.
- **Ses seviyesi:** `render.py` sesi sonunda -14 LUFS'a (Instagram standardı) normalize eder.
- **Bitmiş videolar:** MP4'ler Git'e eklenmez (`.gitignore`). Gerektiğinde yeniden üretilirler.
