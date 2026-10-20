# Galya Zincir Denetimi (Kayıt / DHE Etiketi / Olay Etkisi) — 20 Ekim 2026

Galya zincirinin (`.101`–`.123`) 20 Ekim 2026 denetimi: kayıt kapsamı, DHE
etiket bağı ve olay etkilerinin statik doğrulaması. Denetim tamamen çevrimdışı
yapıldı; oyun içi doğrulama Test B'ye bağlı.

## 1. Kayıt kapsamı (backlog `gaul_record_backfill`)

`2026-10-17_gaul_culture_transition.yml` içindeki 22 kayıt ile olay eşleşmesi:

- `.101`–`.123` arasındaki 23 olayın **23/23**'ü kayıtlı. `.112` (Tours/Strasbourg
  yeminleri) ve `.114`–`.118` dahil; 18 Ekim denetiminde eksik sayılan
  kayıtlar UPDATE 9 ile eklenmişti.
- Kayıtların kullandığı 27 kaynak id'sinin **tamamı** `sources.yml`'de (100
  kaynak kayıtlı); eksik id yok.
- `integration.target` içindeki olay id'lerinin tamamı olay dosyasındaki 29
  olay id'si içinde; notlarda geçen `culture:` anahtarlarının tamamı mod
  kültür tanımlarında.
- Kayıt şeması (entity, subject, finding, population, dating, mechanism,
  source_refs, confidence, integration) eksiksiz: eksik alanı kayıt yok.

Sonuç: görev tamamlandı; `gaul_record_backfill` `completed` olarak işaretlendi.

## 2. DHE etiket bağı (backlog `gaul_dhe_tag_binding_review`)

UPDATE 9 kararı: zincir tek etiketli DHE ile tarih dünyası katmanı olarak
kalır; bantlar ROM (`.101`–`.109`), FRAN (`.110`–`.113`), FRA (`.114`–`.123`).
Statik doğrulama:

| Olay | Tag | Pencere | monthly_chance |
|---|---|---|---:|
| `.101` | ROM | 58-100 | 15 |
| `.102` | ROM | 100-180 | 12 |
| `.103` | ROM | 177-350 | 15 |
| `.104` | ROM | 212-230 | 25 |
| `.105` | ROM | 260-274 | 20 |
| `.106` | ROM | 371-400 | 15 |
| `.107` | ROM | 380-550 | 10 |
| `.108` | ROM | 406-443 | 15 |
| `.109` | ROM | 457-486 | 20 |
| `.110` | FRAN | 496-508 | 20 |
| `.111` | FRAN | 650-850 | 10 |
| `.112` | FRAN | 813-842 | 15 |
| `.113` | FRAN | 911-1000 | 10 |
| `.114` | FRA | 1209-1229 | 15 |
| `.115` | FRA | 1337-1453 | 10 |
| `.116` | FRA | 1539-1540 | 25 |
| `.117` | FRA | 1562-1685 | 10 |
| `.118` | FRA | 1789-1794 | 15 |
| `.119` | FRA | 1881-1883 | 25 |
| `.120` | FRA | 1905-1906 | 20 |
| `.121` | FRA | 1914-1919 | 15 |
| `.122` | FRA | 1945-1975 | 15 |
| `.123` | FRA | 1992-2009 | 8 |

- Bantlar karara birebir uyuyor; 23 olayın **23'ünde** de `fire_only_once =
  yes` var, yani aynı olay ikinci kez ateşlenemez.
- Devir noktası: `.109` (ROM, 457-486) ile `.110` (FRAN, 496-508) farklı
  tag'de ve pencereleri örtüşmüyor → ROM→FRAN el değişiminde çift ateşleme
  yok. Test B'de tag değişimi (ROM → FRAN) R3'te doğrulanacak.
- Pencere örtüşmeleri mevcut ve normal: `.102`/`.103` (177-180), `.103`
  içinde `.104` ve `.105`, `.106`/`.107` (380-400), `.107` içinde `.108`.
  Protokol bunu "bir durakta iki olay birden düşebilir" diye kabul eder;
  örtüşen olaylar birbirinin kültür/din etkisini iptal etmez.
- Kayıt tarihleriyle pencere uyumu: 9 olayın penceresi kayıt tarihiyle birebir
  (`.105`, `.107`–`.109`, `.114`–`.118`, `.122`). Diğerlerinde pencere tek yıllık
  kayıtlar için birkaç yıllık bir aralık (`.104` 212-230, `.113` 911-1000,
  `.116` 1539-1540, `.119` 1881-1883, `.120` 1905-1906), dönem kayıtları için
  ise olay zamanına daraltılmış ya da bir yıl genişletilmiş aralıklardır
  (`.101` 48-100 → 58-100, `.102` 100-200 → 100-180, `.110` 486-530 → 496-508,
  `.121` 1914-1918 → 1914-1919, `.123` 1992-2008 → 1992-2009).
- Bilinen sınır kabul edildi: Paris'i elinde tutan ROM/FRAN/FRA dışı bir
  devlet (oyuncu devleti, yaşayan bir Roma devleti, başka bir tag) zinciri
  çalıştırmaz. Bu, UPDATE 9 kararının bilinçli sonucudur (Mısır tasarım notu
  2.1'deki owner-agnostic pulse deseni reddedilmişti); Test B'de
  `list_dhe_for` çıktısıyla belgelenecek.

## 3. `.105` etki denetimi: boş çalışan tarihsel seçenek

Bulgu: `et_culture.105` (Imperium Galliarum, 260-274) tarihsel seçeneğinin
etkisi hiçbir popu değiştiremiyordu.

Kanıt:

- `.105`in limiti `culture = culture:gallian` + dokuz şehir (lyon, paris,
  bordeaux, toulouse, nimes, arles, marseille, reims, rouen) + pop tipleri
  nobles/clergy/burghers idi ve sonucu `culture:gallo_roman` idi.
- `.101` (58-100) aynı dokuz şehirde aynı üç pop tipini `gallo_roman`'a
  çeviriyor. 260'ta bu poplar zaten `gallo_roman` olduğundan `.105`in
  limiti hiçbir popu tutmuyor.
- Bu, 18 Ekim'de `.107`de bulunan "tarihsel seçenek boş çalışıyor" sınıfının
  aynısıdır; `.107` o zaman limiti `gallian` **veya** `gallo_roman` olarak
  genişletilerek çözülmüştü. `.105`te genişletme işe yaramaz, çünkü hedef
  kültür zaten popların kültürüdür.

Düzeltme (20 Ekim 2026): kaydın kendi mekanizması siyasidir ("military
usurpation, frontier-army autonomy, negotiated reabsorption"; "frontier-army
secession, not a national revolt"). Bu yüzden `.105` siyasi bir olaya
çevrildi:

- Seçenek A (tarihsel): Aurelian'ın geri alışıyla ayrılık biter —
  `add_stability = 10`, `add_prestige = prestige_mild_bonus`.
- Seçenek B: eyaletler kalıcı olarak kopar — `add_stability = -10`,
  `add_prestige = prestige_mild_penalty`.
- Etkisiz `custom_tooltip`/`every_owned_location` bloğu ve `et_culture.105.tt`
  anahtarı kaldırıldı (siyasi olaylarda `.tt` kullanılmıyor: `.120` örneği).
- EN/TR metinleri (desc, a, b) yeni çerçeveye göre yazıldı; `historical_info`
  değişmedi (zaten 260-274 ve Châlons'u anlatıyor).

Neden kültür etkisi geri getirilmedi: geçici bir "Galya İmparatorluğu"
kültür anahtarı için kaynak destekli isim havuzu yok (Etruscan örneğinde
olduğu gibi yer tutucu kullanılmadı) ve geçici bir kimlik için 274'te bir
geri dönüş olayı gerekirdi; bu, olay ID'lerinin kronolojik sırasını bozardı
(`.105` ile `.106` arasına yeni ID, sonraki 18 olayın yeniden numaralanması).

## 4. Zincir genelinde etki (no-op) taraması

Aynı denetim 23 Galya olayının tamamına uygulandı: her tarihsel seçeneğin
etkisi, tükettiği pop (kültür/din) ve ürettiği pop çıkarıldı, zincir sırasıyla
karşılaştırıldı.

| Olay | Pencerede tüketilen | Üretilen | Durum |
|---|---|---|---|
| `.101` | gallian (dokuz şehrin elitleri) | gallo_roman | canlı girdi |
| `.102` | gallian (köylü, işçi) | gallo_roman | canlı girdi |
| `.103` | din sınırı yok | catholic | canlı girdi |
| `.104` | kalan gallian | gallo_roman | canlı girdi (kırsal elit) |
| `.105` | - | - | siyasi olay (bu not) |
| `.106` | din sınırı yok | catholic | canlı girdi |
| `.107` | gallian / gallo_roman | breton | canlı girdi |
| `.108` | - | burgundii / visigoth popları | canlı girdi |
| `.109` | gallo_roman / frankish | frankish (%25) | canlı girdi |
| `.110` | din sınırı yok | catholic | canlı girdi |
| `.111` | gallo_roman (şehir listesi) | french / occitan / arpitan | canlı girdi |
| `.112` | gallo_roman | fransızca dil | canlı girdi |
| `.113` | - | norman popu (Rouen) | canlı girdi |
| `.114` | occitan / french | french (%30) | canlı girdi |
| `.115` | norman / arpitan / frankish | french | canlı girdi |
| `.116` | gallo_roman / occitan / arpitan / norman | fransızca dil | canlı girdi |
| `.117` | calvinist | catholic | canlı girdi |
| `.118` | occitan / arpitan / norman / frankish | french (%50) | canlı girdi |
| `.119` | breton / french | french (%50) | canlı girdi |
| `.120` | - | - | siyasi olay (tasarım) |
| `.121` | breton / french | french | canlı girdi |
| `.122` | - | göçmen popları | canlı girdi |
| `.123` | - | - | siyasi olay (tasarım) |

Sonuç: `.105` dışında başka bir "tarihsel seçenek boş çalışıyor" örneği yok.
`.104`ün girdisi `.101`/`.102`den sonra kalan kırsal elittir (kayıt notu bunu
"remaining gallian" diye belirtir), `.103`/`.106`/`.110`un din sınırı yoktur,
`.111`in girdisi olan gallo_roman `.112`de tüketilir ama `.111` kendi
şehir listesini üretir, `.115`/`.121`in girdileri ise `.114`/`.118`/`.119`
tarafından üretilir. Etkisiz olan tek seçenek `.105`ti ve o da bu notta
siyasi olaya çevrildi.

## 5. Test B beklentisi

- Log: 0 `Invalid scope types`, 0 sınıf-1 `Failed to read key reference`,
  0 `et_german` satırı.
- R2 durak `change_date 266`: `.105` çıkmalı ve **stabilite/prestij değişimi
  üretmeli**; "olay çıktı ama etkisiz" durumu tekrar etmemeli.
- R3 devir: ROM → FRAN tag değişimi sonrası `.110` ateşlenmeli.
- `list_dhe_for` çıktısı ROM, FRAN ve FRA için beklenen pencereleri
  göstermeli.
