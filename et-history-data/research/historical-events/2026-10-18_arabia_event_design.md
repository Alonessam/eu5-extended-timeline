# Arabistan Kültür ve Din Geçişi — Olay Tasarım Notu (M.S. 58 → 2026)

**Tarih:** 18 Ekim 2026  
**Durum:** v1 tasarımı ve script'i yazıldı; Test A/B bekliyor.  
**Kapsam:** Arap Yarımadası (Hicaz, Necid, Yemen, Uman, Körfez kıyısı). Bereketli
Hilal, Mağrip ve İran bu notun dışında.  
**Olay numarası rezervasyonu:** `et_culture.50`–`.99` (Mısır `.1`–`.49`,
Galya `.100`–`.149`). v1: `.50`–`.57`.

## 1. Amaç

58 CE başlangıcında yarımadada tek bir "Arap" kimliği yok: Nebati, Sabai,
Himyer, Thamud, Uman ve Körfez toplulukları farklı kültür ve dinlerde. Bu
zincir, antik toplulukların yüzyıllar içinde İslamlaşmasını, Araplaşmasını ve
Hicazi/Necdi/Yemeni/Umani/Hadrami gibi bölgesel kimliklere ayrışmasını
amaçlar. Zincir **fetih zorlamaz**; yalnızca pop kültürü/dini, devlet dini ve
modern dönem prestij/istikrar katmanlarını işler.

## 2. 58 CE başlangıç durumu (setup'tan doğrulandı)

| Bölge | Başlangıç sahibi | Kültür | Din | Not |
|---|---|---|---|---|
| Mekke/Taif (Hicaz) | `THAM` (Thamud) | `hijazi_culture`; poplarda `bedouin`/`bedouin_culture` | `south_arabian_polytheism` | Mekke'de az sayıda `gonga_culture` köle popu |
| Medine/Khaybar/Tebük | `NABA` (Nabataea) | `nabataean_culture` | `nabataean_religion` | Kuzey Hicaz ve Maan hattı |
| Sana/Marib/Necran | `SABA` (Saba) | `yemeni_culture`; poplarda `bedouin`/`bedouin_culture` | `south_arabian_polytheism` | Sana'da `teimani` Yahudi popları |
| Maskat/Uman | `MASC` | `omani_culture`; poplarda `bedouin` | `south_arabian_polytheism` | Körfez kıyısı |
| Yemen (tagsiz) | `YEM` | `yemeni_culture` | `judaism` | 58 CE'de toprağı yok; Himyer devlet katmanı eksik |

Setup dosyaları: `main_menu/setup/start/06_pops.txt`,
`main_menu/setup/start/10_countries.txt`,
`in_game/setup/countries/et_countries.txt`.

## 3. Veri ve anahtar notları

- **`bedouin` / `bedouin_culture` çifti:** `bedouin` mod anahtarıdır
  (`et_missing.txt:121`, `arabic_language`, `middle_eastern_gfx`);
  `bedouin_culture` vanilla anahtarıdır (`egypt.txt`, `egyptian_dialect`,
  `egyptian_gfx`). İkisi de Arabistan poplarında karışık kullanılıyor;
  `location_templates.txt` Mekke/Sana gibi yerlerde `bedouin_culture`
  kullanıyor. v1 ikisini de "antik Arap" kabul eder, setup'ı normalize etmez;
  karar `arabia_bedouin_key_consistency` backlog maddesindedir.
- **`YEM` topraksız:** 58 CE'de Yahudi Himyer devleti haritada yok; Sana
  polytheist `SABA`'nın elinde. v1 devlet-tag bağlamaz; `.51` sahibinden
  bağımsız çalışır. Himyer devlet katmanı `arabia_himyar_state_layer`
  backlog maddesidir.
- **Din anahtarları:** `south_arabian_polytheism`, `nabataean_religion`,
  `judaism`, `miaphysite` ve modun birleşik `islam` dini
  (`et_muslim.txt`, `group = muslim`) kullanılır. `sunni`/`shia`/`ibadi`
  vanilla anahtarlarıdır ve `.55`'te birleşik `islam` poplarını böler.
- **Coğrafya:** `hedjaz_area` (vanilla yazımı), `najd_area`, `hail_area`,
  `north_yemen_area`, `south_yemen_area`, `oman_area`. `oman_area` BAE'yi,
  `south_yemen_area` Hadramut'u da kapsar; Bahreyn/Al-Ahsa için ayrı kara
  alanı v1'de kullanılmaz. Bu yaklaşım `arabia_area_approximation`
  maddesindedir.
- **Devlet dini ile pop dini ayrıdır:** `.51`, `.52` ve `.53` tarihsel
  seçeneklerinde `change_religion` (ve hükümdar/aile dönüşümü) yalnızca devlet
  katmanını dönüştürür; pop payları ayrı `split_pop` bloklarıyla işlenir.
  `.54`'te `change_religion` kullanılmaz; çünkü `sunni`/`shia`/`ibadi` bir
  devleti birleşik `islam`a düşürmek istenmez.

## 4. Zincir mimarisi

- **Pulse:** `yearly_country_pulse` → `et_arabia_yearly_pulse`
  (`in_game/common/on_action/et_history_pulses.txt`). Dış koşul yalnızca
  `mecca`, `medina`, `sana_yemen` veya `masqat` limanlarından birine sahip
  olmaktır; pahalı koşullar olayların içindedir.
- **Sahip-bağımsız:** Hiçbir olay DHE/tag bağlı değildir. Ülke değişse bile
  yeni sahip, tarih penceresi ve liman koşuluyla aynı süreci çalıştırabilir.
- **Sert zincir yok:** `.52` Vahiy ve `.53` Ridde anlatı değişkenlerini
  kurar; ancak `.54`–`.57` yalnızca tarih + liman + (gerektiğinde) Müslüman
  devlet/İslam etkisi koşuluna bakar. Böylece bir bölge el değiştirdiğinde
  zincir tıkanmaz. Her ülke için `et_arabia_X_fired` işaretleri tekrarı
  önler.
- **Sıra:** `.52` yalnızca Mekke sahibinde; `.53` Mekke/Medine sahibinde;
  `.54`–`.55` dört limandan herhangi birine sahip Müslüman/İslam etkisindeki
  devlette; `.56`–`.57` herhangi bir liman sahibinde çalışır.
- **Ölçek:** Etkiler `every_owned_location` + `area` + `every_pop` ile
  sınırlandırılır; sahip olunmayan şehirde pop yaratılmaz (Galya `.122`
  dersinden). Oranlar kademelidir; `split_pop` art arda çalıştığında ikinci
  oran kalan pop üzerinden uygulanır.

## 5. Olaylar

| ID | Pencere | Tetik | Tarihsel seçenek | Alternatif | Kayıt |
|---|---|---|---|---|---|
| `.50` | 58–120 | `owns = location:medina` | Kervan yolları açık; prestij | Sınırı tahkim et; istikrar | `arabia_nabataean_annexation_106` |
| `.51` | 300–530 | Sana/Marib/Necran | Himyer sarayı Yahudiliği benimser; kuzeyde %20 Yahudi, güneyde %5 Hristiyan | Eski tanrılar; %5/%2 | `arabia_himyar_book_religions`, `arabia_aksumite_yemen_525` |
| `.52` | 610–632 | `owns = location:mecca` | Devlet İslam'a girer; Hicaz'da %30 ihtida | Eski düzen; %10 ihtida | `arabia_muhammad_revelation_610_632` |
| `.53` | 632–700 | Mekke/Medine | Ridde sonrası birlik; Hicaz %30, Necid/Yemen/Uman %15 | Kabile özerkliği; %15/%5 | `arabia_ridda_unification_632_634` |
| `.54` | 700–1400 | Müslüman devlet veya `et_arabia_islam_1` + liman | Hicaz %50, Yemen %40, Necid %30, Uman %30 ihtida | Yarısı; eski cemaatler yaşar | `arabia_islamization_and_arabization` |
| `.55` | 900–1700 | `et_arabia_islamized` veya Müslüman devlet + liman | Sünni/Şii/İbadi okulları yerleşir | Daha küçük bölünme; birlik | `arabia_sectarian_consolidation` |
| `.56` | 1000–1600 | Herhangi bir liman | Antik Arap/Nebati popları bölgesel kimliklere döner | Daha küçük kayma; çöl kimliği | `arabia_regional_identities` |
| `.57` | 1900–2026 | Herhangi bir liman | Petrol ve dünya pazarı; prestij/istikrar | Eski düzeni koru; istikrar | `arabia_oil_and_modern_states` |

Not: `.55` ve `.56` pencereleri kısmen örtüşür; ikisi de bağımsız
işaretlere sahiptir. Tarihsel sıra için `.55` normalde `.54`'ün
`et_arabia_islamized` işaretini arar; sahip değişiminde Müslüman devlet de
kabul edilir. `.56` kültür kaymasıdır ve din koşulundan bağımsızdır.

## 6. Etki oranları (oyun dengesi, nüfus tahmini değil)

- **`.51`:** kuzey Yemen polytheist poplarında `judaism` %20; güneyde
  `miaphysite` %5. Alternatif: %5 / %2.
- **`.52`:** Hicaz'da polytheist + Nabati poplarda `islam` %30; alternatif
  %10. Tarihsel seçenek devleti (Müslüman değilse) `islam` yapar.
- **`.53`:** Hicaz %30; Necid/Hail, kuzey/güney Yemen ve Uman %15; alternatif
  Hicaz %15, diğerleri %5.
- **`.54`:** Hicaz %50; Yemen %40; Necid/Hail %30; Uman %30; alternatif
  %25/%20/%15/%15. Yahudi, Hristiyan ve Zerdüşt azınlıklar limit içindedir;
  tamamen yok edilmez.
- **`.55`:** Hicaz'da %70 Sünni, %5 Şii, %25 islam; Necid/Hail %80 Sünni,
  %20 islam; kuzey Yemen %55 Şii, %20 Sünni, %25 islam; güney Yemen %55
  Sünni, %15 Şii, %30 islam; Uman %65 İbadi, %15 Sünni, %20 islam.
  Alternatifte nihai oranlar yarıya iner; ikinci `split_pop` oranları kalan
  pop üzerinden hesaplanır.
- **`.56`:** Hicaz'da antik popların %60'ı Hicazi; Necid/Hail %60 Necdi;
  kuzey Yemen %60 Yemeni; güney Yemen'de %50 Yemeni, kalanın %50'si (toplamın
  %25'i) Hadrami; Uman %60 Umani. Alternatif: %30/%25.
- **`.57`:** Pop etkisi yok; prestij + istikrar. Körfez'e yabancı işgücü
  göçü v1'de modellenmez (`arabia_modern_migration_layer`).

## 7. Kayıt eşlemesi

| Olay | Kayıtlar | Kaynaklar |
|---|---|---|
| `.50` | `arabia_58ce_population_baseline`, `arabia_nabataean_annexation_106` | `wiki_nabataean_kingdom` |
| `.51` | `arabia_himyar_book_religions`, `arabia_aksumite_yemen_525` | `wiki_himyarite_kingdom`, `wiki_aksumite_empire` |
| `.52` | `arabia_muhammad_revelation_610_632` | `wiki_muhammad` |
| `.53` | `arabia_ridda_unification_632_634` | `wiki_ridda_wars` |
| `.54` | `arabia_islamization_and_arabization` | `wiki_early_muslim_conquests`, `wiki_islamization` |
| `.55` | `arabia_sectarian_consolidation` | `wiki_zaydism`, `wiki_ibadi_islam` |
| `.56` | `arabia_regional_identities` | `wiki_history_of_arabia`, `wiki_arabian_peninsula` |
| `.57` | `arabia_oil_and_modern_states`, `arabia_modern_labor_migration` | `wiki_arab_revolt`, `wiki_unification_of_saudi_arabia`, `wiki_petroleum_industry_in_saudi_arabia`, `wiki_gulf_cooperation_council`, `wiki_demographics_of_saudi_arabia` |

Kayıt dosyası: `2026-10-18_arabia_culture_transition.yml`. Kayıtlar Test B'ye
kadar `pending`; yalnızca 58 CE taban çizgisi `applied`.

## 8. Test planı

**Test A (dosya yükleme ve tek olay):**
1. Modu temiz bir worktree'den çalıştır; `error.log`'u `Log.ClearErrorLog`
   öncesinde yedekle.
2. Debug/free console, ironman kapalı.
3. `change_date 610.1.1`, `event et_culture.52`; olayın açıldığını ve
   `error.log`'da mod satırı olmadığını doğrula.
4. Sırayla `.50`, `.51`, `.53`–`.57` için `change_date` + `event` dene;
   bilinmeyen kültür/din/lokasyon/area token'ı arama.

**Test B (zincir ve sahiplik):**
1. 58 CE'de `THAM` ile başla; `event_probabilities` ile `.50`/`.51`
   pencerelerini gözle.
2. 610'a gelince `.52`'nin kendiliğinden geldiğini, 632'de `.53`'ün
   geldiğini doğrula; `et_arabia_islam_1`, `et_arabia_unified` işaretlerini
   kontrol et.
3. 700–1400 arasında `.54`'ün Müslüman/İslam etkisindeki sahipte çalıştığını,
   `.55`'in `et_arabia_islamized` sonrası veya Müslüman bir sahipte geldiğini
   doğrula.
4. 1000–1600 arasında `.56`'nın din koşulundan bağımsız çalıştığını doğrula.
5. 1900'de `.57`'yi doğrula.
6. **Sahip değişimi:** Mekke'yi başka bir tag'e ver (console/`own`), yeni
   sahibin `.54`/`.55`/`.56` olaylarını alabildiğini ve aynı ülkenin olayı
   iki kez almadığını kontrol et.
7. Pop paylarını `location` panelinden veya console pop komutlarıyla örnekle;
   `split_pop` art arda uygulandığı için nihai payların nominalden düşük
   olduğunu unutma.

**Test B geçince:** kayıtları `pending` → `applied` yap; README/backlog
durumlarını güncelle; `.57` için modern göç katmanı ayrı iş.

## 9. Açık işler

- `arabia_bedouin_key_consistency` — `bedouin`/`bedouin_culture` setup
  normalizasyonu.
- `arabia_area_approximation` — BAE, Hadramut, Dhofar ve Bahreyn/Al-Ahsa
  için alan yerine il/lokasyon kapsamı.
- `arabia_owner_transfer` — sahip değişiminde işaretlerin tekrar/atlama
  davranışı; gerekirse lokasyon/global değişken veya bölgesel modüller.
- `arabia_modern_migration_layer` — Güney Asya, Mısır, Filipinler vb.
  işgücü için doğrulanmış kültür anahtarları ve sahiplik güvenli `add_pop`.
- `arabia_himyar_state_layer` — topraksız `YEM` ve Yahudi Himyer devleti.
- `arabia_aksumite_christian_state` — 518–530 Aksum fethi sonrası devlet
  dininin Hristiyanlığa dönüşü; v1 yalnızca güneyde %5 Miaphysite popu ve
  kaydı işler.
- `gaul_122_ownership_scope` — Samet'in `.122` olayı yalnızca Paris'i
  koşul alıp Lyon/Marsilya/Lille/Bordeaux/Toulouse'a pop ekliyor; ayrı
  inceleme maddesi.
- Doğu Arabistan/Bahreyn modülü `.58`+ için rezerve.

## 10. Kaynaklar

Ayrıntılı künyeler `sources.yml` içinde: `wiki_nabataean_kingdom`,
`wiki_himyarite_kingdom`, `wiki_aksumite_empire`, `wiki_muhammad`,
`wiki_ridda_wars`, `wiki_early_muslim_conquests`, `wiki_islamization`,
`wiki_history_of_arabia`, `wiki_arabian_peninsula`, `wiki_zaydism`,
`wiki_ibadi_islam`, `wiki_arab_revolt`,
`wiki_unification_of_saudi_arabia`,
`wiki_petroleum_industry_in_saudi_arabia`, `wiki_gulf_cooperation_council`,
`wiki_demographics_of_saudi_arabia`.

Tarih ve yorum belirsizlikleri kayıtlarda `confidence` ve `caveat`
alanlarıyla işaretlenmiştir; bu nottaki oranlar oyun dengesi içindir, tarihsel
nüfus istatistiği değildir.
