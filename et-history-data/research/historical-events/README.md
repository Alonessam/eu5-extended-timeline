# Tarihsel Olaylar ve Kültür Dönüşümü Planı (M.S. 58 → 2026)

Bu doküman, 58 CE senaryosunda halkların, kültürlerin ve dinlerin tarihsel
dönüşümünü sağlayacak **olay (script) katmanının** ve buna temel olacak **veri
araştırmasının** çalışma planıdır. Projenin veri-önce ilkesi gereği her dönüşüm
önce `et-history-data` içinde kaynaklı bir kayıt olarak toplanır; mod tarafındaki
olay scriptleri yalnızca bu kayıtlara dayanılarak yazılır. Planın teknik
kısımları 17 Ekim 2026'da incelenen kurulu EU5 1.3.x dosyalarından
doğrulanmıştır; doğrulama notları bu dokümandadır.

**Durum:** Plan yayında. **Faz 1 paralel iki pilotla sürüyor: Mısır ve Galya**
(17 Ekim 2026 mutabakatı). Mısır hattında kaynaklı geçiş kayıtları, kültür
grafiği düzeltmeleri ve **olay zinciri v1** hazır (`et_culture.1`–`.5` +
`on_action/et_history_pulses.txt`); **Test A geçti** (17 Ekim 2026:
`et_culture.9000` + Galya `.101` oyun içinde ateşlendi; `error.log`'da mod
satırı yok). Zincir doğrulaması (Test B) sırada. Samet'in inceleme commit'i (`f3d304d`) payları spec'e hizaladı; son-kimlik anahtar sahipliği ikinci incelemede (17 Ekim 2026) karara bağlandı — deltasız mod kopyaları geri alındı (vanilla içerik korunur), deltalılar vanilla birebir + delta olarak kaldı (design note §7, kararlar 7–8). Galya incelemesi (aynı gün): Samet'in `e271902` commit'i gözden geçirildi — boş `latin_language` kopyası geri alındı (vanilla `00_italy.txt` tanımı yüklenir); `french_group` kopyası vanilla'da da boş olduğundan zararsız bırakıldı (backlog UPDATE 4). Galya hattında
`gallo_roman` ara kimliği ve pilot olaylar (`.101`–`.103`) yazıldı (Samet); Faz 2–3 olayları (`.104`–`.110`) incelendi — din/locasyon/efekt/prestij token'ları vanilla'ya göre düzeltildi (backlog UPDATE 5);
numara rezervasyonu mutabık: Mısır `.1`–`.49`, Galya `.100`–`.149`.

**Galya modern dönemi (Faz 7-8):** 18 Ekim 2026'da Galya zinciri M.S. 2026'ya
uzatıldı. **Faz 7 — Modern Fransa (1837–1945):** Jules Ferry okul yasaları
(1881-1882, `.119`), Kilise-Devlet ayrılığı/laïcité (1905, `.120`) ve Büyük Savaş
ile Kutsal Birlik (1914-1918, `.121`). **Faz 8 — Çağdaş Fransa (1945–2026):**
savaş sonrası işgücü göçü / Otuz Şanlı Yıl (1945-1975, `.122`) ve Cumhuriyetin
dili anayasal düzenlemesi (1992-2008, `.123`). Yeni kaynaklar `wiki_jules_ferry_laws`,
`wiki_separation_church_state_1905`, `wiki_sacred_union`, `wiki_languages_of_france`,
`wiki_immigration_to_france` ve `wiki_portuguese_in_france` olarak `sources.yml`'e
eklendi; geçiş kayıtları `2026-10-17_gaul_culture_transition.yml` içinde `gaul_*`
anahtarlarıyla yer alır. Faz 7/Faz 8 sınırı projenin dönem sınıflarına dayanır
(`docs/Period Classes.md`: `industrial` 1800–1945, `contemporary` 1945+). Göç
olayı kronolojiyi korumak için `.122` numarasını aldı; eski "Cumhuriyetin dili"
olayı `.123`'e taşındı (yalnızca ID ve localization anahtarları değişti, içerik
aynı). Bu incelemede ayrıca `.102` ve `.106`'daki geçersiz `pop_type:craftsmen`
token'ı `pop_type:laborers` ile değiştirildi (vanilla 1.3.x'te `craftsmen` diye
bir pop tipi yok). Test B (oyun içi zincir doğrulaması) hâlâ sırada.

**Galya Faz 4-7 incelemesi (18 Ekim 2026):** Samet'in `2ca31cc`–`9c7d2b3`
commit'leri vanilla'ya karşı denetlendi. Doğrulananlar: `change_language` kültür
kapsamlı bir efekt ve `dialect:french_language` gerçek bir lehçe
(`00_france.txt`); `split_pop` `.fraction` + `culture` vanilla deseni;
`calvinist`/`catholic`, `arpitan`/`norman` ve kullanılan tüm lokasyon anahtarları
geçerli; `occitan` gerçekten yeni bir kültür anahtarı (vanilla gölgesi değil);
169 olay lokalizasyon anahtarı EN/TR'de tam. Bu turda düzeltilenler: yeni
`occitan` kültürünün eksik isim lokalizasyonu (EN/TR), `.113`'ün
Rouen/Cherbourg/Bayeux sahiplik koruması ve birkaç TR yazım hatası. Açık
kalanlar: `.112` ve `.114`–`.118` için kaynaklı kayıt yok (backlog:
`gaul_record_backfill`); zincirin tamamı DHE ile ROM/FRA tag'ine bağlı, bu
yüzden Paris'i elinde tutan diğer devletler zinciri çalıştıramıyor (backlog:
`gaul_dhe_tag_binding_review`). 01:33 oyun logları Faz 4-7 commit'lerinden
(02:28–02:59) önce alındı; Test B yeni blokları kapsayacak şekilde yeniden
çalıştırılmalı.

**Galya tarihsel denetimi (18 Ekim 2026):** Zincirin tamamı (`.101`–`.123`) kaynak
kayıtlara ve vanilla/mod tanımlarına karşı harf harf denetlendi. Mekanik doğrulama:
kullanılan tüm kültür, din, lokasyon ve `pop_type` anahtarları (göçmen kültürler
dahil) ile kaynak id'leri geçerli. Düzeltilen kritik hatalar: (a) `.107` `culture:gallian`
hedefliyordu ama `.102`/`.103` zaten tüm `gallian`'ı `gallo_roman`'a çevirdiği için
tarihsel seçeneklerle olay boş çalışıyordu; sınır artık `gallian` VEYA `gallo_roman`
kabul ediyor ve kaydın `entity` alanı `culture_gallo_roman` yapıldı (Armorika 380-500'de
Gallo-Romen'di). (b) `.108` Marsilya ve Nîmes'e kalıcı `vandal` pop'u yerleştiriyordu;
Vandallar Galya'dan yalnızca geçti (406-409, Hispania'ya), iki `add_pop` bloğu kaldırıldı
ve araç ipucu artık yalnız Burgund/Vizigot yerleşimini anıyor. (c) `.108` TR açıklaması
ve `historical_info`'su Vizigotları Akdeniz'e, Vandalları güneye gönderiyordu; Akitanya
(418) ve Akdeniz'e düzeltildi (EN ile uyumlu). (d) 58 CE temel kaydı modda hiç
tanımlı olmayan `celtic_paganism`'i yazıyordu; başlangıç kurulumu (06_pops.txt, 1.039
gallian bloğu) `gallo_roman_polytheism` kullanıyor ve kayıt düzeltildi. (e) `.123`
DHE penceresi 2000'de bitip kayıt/metin 1992-2008'i anlatıyordu; `to` artık 2009.1.1.
Kalan denetim bulguları (frankish'in hiç french'e dönüşmemesi; `.109`/`.114`/`.118`
tam nüfus kaymaları; beş kaynaksız ve dokuz eksik kayıt; TR/EN metinleri) yeni
`gaul_history_audit_followups` göreviyle `gaul_record_backfill` ve
`gaul_dhe_tag_binding_review` yanında izleniyor (backlog UPDATE 10). Test B hâlâ sırada.

**Galya zincir mantığı (§2, 18 Ekim 2026):** `.109`, `.114` ve `.118` artık
`change_pop_culture` yerine `split_pop` kullanıyor (`0.25`/`0.30`/`0.50`), böylece
Frenk, Oksitan, Arpitan ve Norman nüfusları tek seferde değil kademeli olarak kayıyor
(Frenkler Romance çoğunluk içinde eriyen küçük bir seçkin tabakaydı; Albigens Haçlı
Seferi Languedoc'u ilhak etti ama halkını Fransızlaştırmadı; Devrim'in okulu ve
yönetimi eyaletleri zorladı ama işi bitirmedi). `frankish`, `.115` ve `.118` dönüşüm
kümelerine eklendi; böylece Frenk kültürü artık `french`'e asimile oluyor. `.109`'un
Frenk yaptığı ama sonraki hiçbir olayın dokunmadığı `soissons`, `.111` ve `.115` konum
listelerine eklendi. `.109`/`.114`/`.115`/`.118` araç ipuçları (EN/TR) yeni kademeli
etkiye göre yazıldı. Açık kalan nokta: `.114` hâlâ İngiliz Gaskonyası olan `bordeaux`'yu
içeriyor (`gaul_history_audit_followups`).

**Nasıl kullanılır:** Bu doküman canlıdır; fazlar ilerledikçe güncellenir.
Katkı vermek isteyen ekip üyeleri bölüm 4'teki iş paketlerinden veya bölüm
5'teki Faz 1 kontrol listesinden başlayabilir. Yeni veri ve script işleri,
bölüm 6'daki kalite kurallarına bağlıdır.

---

## 1. Neden gerekli

- 58 CE başlangıcı, nüfusu ağırlıklı olarak antik kültür bloklarında tutuyor
  (`roman`, `germanic`, `slavic`, `gallian`, `ancient_greek`, `old_egyptian`,
  `berber`, `persian` ...). Modern kimlikler (`french`, `german`, `english`,
  `greek`, `arabic`, `turkish` ...) tanımlı fakat başlangıçta neredeyse boş.
- Motor kendiliğinden yalnızca **asimilasyon** üretir: pop'lar yönetici devletin
  ana kültürüne yakınsar. Kültürlerin **bölünmesi/ayrışması** ve yeni
  kimliklerin doğuşu kendiliğinden yoktur; asimilasyonun yönü ve hızı kültür
  grafiğine (dil, aile, grup bağları) bağlıdır.
- Sonuç: olay katmanı olmadan 58→1837 oyunu Gallia'da francien/occitan
  ayrışmasını, Mısır'da koptik→Arap dönüşümünü, Germen ve Slav kimliklerinin
  çeşitlenmesini üretmez; dünya antik bloklarda donar ya da egemen kültüre
  homojenleşir.
- Üç katmanlı model:
  1. **Kültür grafiği** — asimilasyonun yönü ve hızı (dil/aile/grup/opinion
     bağları). Kısmen mevcut; boşlukları ayrı iş kalemidir (WS3).
  2. **Tarihsel olay katmanı** — pop kültür/din dönüşümleri, göçler, dil
     kaymaları, kimlik doğuşları. **Eksik; bu planın ana konusu.**
  3. **Devlet/formable katmanı** — modern ana kültürlü devletler; asimilasyonun
     hedef alacağı taşıyıcılar. Maintainer kararıdır (WS6).

## 2. Motorda doğrulanan araçlar (EU5 1.3.x)

İncelenen kurulu oyun dosyalarından (vanilla) doğrulanan script araçları:

| Araç | İşlev | Vanilla doğrulama |
|---|---|---|
| `change_pop_culture` | Pop kültürünü değiştirir (pop kapsamı) | `in_game/events/DHE/flavor_SWE.txt:2148` — Savonian/Tavastian/Kven pop'ları `finnish` yapılıyor |
| `change_pop_religion` | Pop dinini değiştirir (pop kapsamı) | `in_game/events/debug/qa_debug.txt:164` |
| `change_culture` | Ülke ana kültürünü değiştirir | `in_game/events/wokou_events.txt:566-569` |
| `change_character_culture` | Karakter kültürünü değiştirir | efekt listesi (wiki) |
| `change_language` | Bir kültürün dilini değiştirir | efekt listesi (wiki) |
| `form_new_culture` | Cabinet action (adm, 10 yıl): ana kültürden yeni kültür oluşturur | `common/cabinet_actions/form_new_culture.txt` |
| `merge_culture_group` | Cabinet action (10 yıl): ana kültürün grubunu birleştirir | `common/cabinet_actions/merge_culture_group.txt` |
| `add_migration` / `remove_migration` | Kültür ve din parametreli göç kurar | `in_game/events/culture/culture_greek.txt:2945` |
| `add_cultural_influence` / `add_cultural_tradition` | Kültür savaşı ivmesi | efekt listesi (wiki) |
| `force_refresh_culture_and_religion` | Lokasyonun baskın kültür/dinini yeniden hesaplar | efekt listesi (wiki) |

Yollar, incelenen kurulu oyundaki vanilla dosyalara aittir.

**Şablon ve altyapı kaynakları (vanilla):**

- `in_game/events/culture/` klasörü: `cultural_event.txt`, `culture_greek.txt`,
  `culture_italian.txt`, `culture_japan.txt`, `culture_religion_events.txt`,
  `language_events.txt`, `haudenosaunee.txt` — kültür olay zincirleri için hazır
  desenler.
- `in_game/common/on_action/`: `country_yearly.txt`, `country_monthly.txt`,
  `location_pulses.txt` vb. periyodik kancalar.
- Tarih penceresi deseni:
  `dynamic_historical_event = { tag = SWE from = 1400.1.1 to = 1600.1.1 monthly_chance = 30 }`
  (`flavor_SWE.txt`, olay 43).
- Standart olay alanları: `historical_option = yes`, `fire_only_once = yes`,
  `illustration_tags`, `custom_tooltip`.

Doğrulanmış pop dönüşümü kalıbı (`flavor_SWE.42`'den sadeleştirilmiştir):

```txt
option = {
    name = ...
    custom_tooltip = { text = ... }
    every_owned_location = {
        every_pop = {
            limit = {
                OR = {
                    culture = culture:savonian
                    culture = culture:tavastian
                }
            }
            change_pop_culture = culture:finnish
        }
    }
}
```

**Bilinen sınırlar ve dikkat noktaları:**

- Script, pop'ları **mevcut kültür anahtarları** arasında taşır. Ara kimlik
  gerekiyorsa (ör. `gallo_roman`) kültür dosyalarında önceden tanımlanmalıdır;
  bu bir veri işidir.
- `form_new_culture` motor-yönetimli yeni kültür oluşturur; AI bu eylemi
  normalde yalnızca sömürge bağlamlarında kullanır. Tarihsel ayrışma bu yüzden
  olay yazımına bağlıdır.
- `every_pop` döngüleri pahalıdır: olaylar lokasyon/ülke kapsamıyla
  sınırlanmalı; toplu dönüşümler `monthly_chance` ve kademeli oranlarla zamana
  yayılmalı; test loglarıyla izlenmelidir.
- Asimilasyon sabitleri
  (`Extended Timeline/loading_screen/common/defines/00_defines.txt`,
  `ASSIMILATION_*`): aynı dil/aile/grup ve pazar dili etkileri. Olay tasarımı bu
  ivmelerle birlikte düşünülmelidir.

## 3. Mevcut durum (17 Ekim 2026)

- **Olay katmanı kuruldu** (17 Ekim 2026): `in_game/events/`
  (`et_culture_events.txt`: `et_culture` namespace'i; `et_culture.9000` test
  olayı; Mısır zinciri `.1`–`.5`; Galya pilotu `.101`–`.103`) ve localization
  dosyaları (`in_game/localization/{english,turkish}/et_culture_events_l_*.yml`).
  `on_action/et_history_pulses.txt` eklendi: `yearly_country_pulse`'a bağlı,
  sahip-bağımsız `et_egypt_yearly_pulse` (ileriki bölge zincirleri için desen);
  Galya olayları DHE pencereleriyle yürüyor. `decisions/` henüz yok.
- **Başlangıç pop verisi** (`main_menu/setup/start/06_pops.txt`, ~50 bin pop
  bloğu): örnek — `gallian` ~1.000, `old_egyptian` ~300, modern `french` 0. Bu
  dağılım, dönüşümün ancak olaylarla kurulabileceğini gösterir.
- **Kültür grafiği denetimi yapıldı** (17 Ekim 2026,
  `2026-10-17_culture_graph_audit.md`): Mısır pilotu için `old_egyptian` →
  `arabic_group` ve `kushite` → `nilosahelian_group` eşleştirildi; `gallian`
  hattına `french_group` eklendi. Taramada işaretlenen 39 kaydın kalanı
  (fallback kültürler, Balkan/Tohar/Pyu-Pear hatları, Doğu Asya izoleleri)
  önceliklendirildi; ayrıntı ve gerekçeler rapordadır.
- **Araştırma altyapısı hazır**:
  `research/native-history-requirements/2026-10-13/societies.yml` r13–r16,
  dönüşüm kayıt disiplinini tanımlıyor: etkilenen nüfus, başlangıç/bitiş
  kimliği, yer, aralık, ölçek, mekanizma, kaynak, güven. Bu planın veri işleri
  bu şemayı kullanır.
- **Referans sürüm**: incelenen kurulu dosyalar EU5 1.3.x içeriğidir (kurulum
  klasörü adı sürümü güvenilir biçimde göstermez; içerik esas alınmıştır).

## 4. İş paketleri

**WS1 — Kültür geçiş haritası (veri, P0).**
Her antik kültür için: ardıl kimlik(ler) (ara ve/veya modern), tarih aralığı,
bölge, mekanizma (fetih, göç, şehirleşme, din, ticaret), kaynak, güven. Kayıt
formatı: `societies.yml` r13–r16 alanları + `research/README.md` kayıt alanları
(`dating`, `source_refs`, `confidence`, `integration`). Çıktı: bu klasörde
`YYYY-MM-DD_<konu>.yml` dosyaları ve insan-okur raporu.

**WS2 — Din geçiş haritası (veri, P1).**
Hristiyanlaşma, İslamlaşma, Budizm/Manikeizm yayılımı gibi dalgalar;
`change_pop_religion` olaylarının temeli.

**WS3 — Kültür grafiği tamamlama (veri + mod, P1).**
Boş `culture_groups`, dil/aile bağları, `kindred`/opinion ağları. Asimilasyon
yönü ve hızı bu bağlara bağlıdır; WS1 ile çapraz çalışır.

**WS4 — Olay prototipleri (mod, P0 pilot).**
Pilot bölgede 3–5 olaylık zincir; bölüm 2'deki desenlerle yazılır; modda
`events/` + localization iskeleti kurulur; oyun içi test edilir.

**WS5 — Mekanizma kataloğu (doküman).**
Doğrulanmış efekt imzaları, olay şablonları, performans notları, localization
anahtarları — ekip için başvuru kaynağı. Bu doküman çekirdeğidir.

**WS6 — Devlet ve cabinet pacing (maintainer).**
Modern ana kültürlü devlet/formable'lar; `form_new_culture` /
`merge_culture_group` erişim ve AI davranışı; hangi olayların hangi devleti
zorlayacağı.

**WS7 — Süreç ve kalite.**
Veri-önce kuralı, test protokolü, merge disiplini (bkz. bölüm 6).

## 5. Fazlar

- **Faz 0 (bu dosya):** Plan yayında. ✓
- **Faz 1 — Pilotlar: Mısır + Galya (paralel)** (17 Ekim 2026 mutabakatı).
  Mısır hattı: kaynaklı geçiş kayıtları ✓ → zincir `.1`–`.5` ✓ → oyun içi
  test (sırada) → şablon çıkarma. Galya hattı: `gallo_roman` kimliği +
  kayıtlar + olaylar `.101`–`.103` ✓ → test (sırada).
- **Faz 2 — Geç Antik ve Kavimler Göçü (200–700):** Roma çöküşü sonrası
  Latin/Romance ayrışması; Germen ve Slav yayılımı; `add_migration` dalgaları.
- **Faz 3 — Postklasik (700–1400):** Arap fetihleri ve Arapçalaşma; Türk
  göçleri; Vikingler; Hristiyanlaşma dalgaları.
- **Faz 4 — Erken Modern ve Sanayi (1400–1837):** Kimlik konsolidasyonu ve
  sömürge dönemi; başlamadan önce vanilla sistemleriyle etkileşim incelemesi
  yapılır.

**Galya zinciri (uygulama fazları):** Mısır hattından bağımsız yürüyen Galya olay
zinciri şu uygulama fazlarına bölündü (numara rezervasyonu `.100`–`.149`):

- **Faz 4 — Dil Ayrışması ve Normanlar (600–1000):** `et_culture.111`–`.113`
- **Faz 5 — Yüksek Orta Çağ ve Fransız Krallığı (1000–1500):** `.114`–`.115`
- **Faz 6 — Erken Modern ve Fransız Devrimi (1500–1837):** `.116`–`.118`
- **Faz 7 — Modern Fransa (1837–1945):** `.119`–`.121`
- **Faz 8 — Çağdaş Fransa (1945–2026):** `.122`–`.123`

Faz 7/Faz 8 sınırı, projenin kendi dönem sınıflarına dayanır
(`docs/Period Classes.md`: `industrial` 1800–1945, `contemporary` 1945+); bu yüzden
Faz 7'nin 1945-sonrası içeriği ayrı bir faza taşındı. Faz 8 doldurulurken göç
olayı kronolojiyi korumak için `.122` numarasını aldı; eski `.122` "Cumhuriyetin
dili" olayı `.123`'e taşındı (içerik değişmedi, yalnızca ID ve localization
anahtarları).

Her fazın akışı: kaynaklı veri → olay tasarımı → mod uygulaması → oyun içi test
→ backlog senkronu.

**Faz 1 açılış kontrol listesi:**

- [x] Pilot bölge kararı — **Mısır** (17 Ekim 2026)
- [x] Kaynak seti toplama — `sources.yml`'e 5 yeni kaynak (coptic_language,
  islamization_egypt, arab_conquest_egypt, christianity_egypt, nobatia)
- [x] Geçiş kayıtları — `2026-10-17_egypt_culture_transition.yml` (11 kayıt)
- [x] Olay tasarım notu — `2026-10-17_egypt_event_design.md` (5 olaylık
  çekirdek zincir + Nübya eki önerisi; sahip-bağımsız on_action pulse
  mimarisi doğrulandı)
- [x] Mod iskeleti: `events/` + localization kuruldu (test olayı dahil)
- [x] Olay zincirleri: Mısır `et_culture.1`–`.5` + `et_history_pulses.txt`
  (17 Ekim 2026) · Galya `et_culture.101`–`.103` + `gallo_roman` (Samet)
- [x] Oyun içi test A — `et_culture.9000` ve Galya `.101` ateşlendi;
  oturumun `error.log`'u mod satırı içermiyor (17 Ekim 2026)
- [ ] Oyun içi test B — Mısır zinciri `.1`–`.5`: console protokolü
  (`event_probabilities`, `test_event_trigger`, `change_date`, `tick_day`;
  ayrıntı: design note bölüm 5)

## 6. Bağlayıcı kalite kuralları

1. Kaynaksız geçiş olayı yazılmaz; her kayıtta güven düzeyi ve belirsizlik
   açıkça belirtilir.
2. Tek lokasyon veya örneklem, bölge geneli dönüşüm iddiası kuramaz
   (`societies.yml` yorum kuralları).
3. Yönetici kimliği değişimi ile halk dönüşümü ayrı kaydedilir; siyasi din
   değişimi toplu dönüşüm sayılmaz.
4. Tarihler oyun gününe zorlanmaz; pencere (aralık/dönem) yaklaşımı kullanılır.
5. Sessiz override yok: maintainer kararı esastır; anlaşmazlıklar TODO notu veya
   backlog maddesiyle iletilir.
6. Performans bütçesi: toplu `every_pop` dönüşümleri kademeli ve sınırlı
   tutulur; test loglarıyla doğrulanır.

## 7. Açık kararlar (maintainer)

- ~~Pilot bölge: Galya mı, Mısır mı?~~ → **İkisi paralel pilot** (17 Ekim 2026
  mutabakatı): Mısır ve Galya hatları birbirini bloklamadan yürütülür.
- Ara kimlikler: **Mısır hattı yeni anahtar gerektirmiyor** — `old_egyptian` →
  `coptic_culture` → `lower_egyptian_culture`/`upper_egyptian_culture` ve
  `kushite` → `nubian` zincirlerinin tamamı vanilla'da mevcut. Galya hattında
  `gallo_roman` ara kimliği kullanılır; diğer bölgeler için politika açık.
- Railroad derecesi: sabit tarihler mi, koşullu pencereler mi? (Öneri:
  koşullu pencereler + sahiplik koşulu —
  `2026-10-17_egypt_event_design.md` bölüm 7.)
- Hangi olaylar AI'yı zorlar (fetih/göç dalgaları); hangileri serbest
  simülasyona bırakılır? (Öneri: fetihler zorlanmaz; aynı not.)
- Cabinet action erişimleri (`form_new_culture` / `merge_culture_group`)
  değiştirilecek mi?

## 8. Kaynaklar ve referanslar

- `research/native-history-requirements/2026-10-13/societies.yml` ve
  `societies.md` — r13–r16 geçiş kayıt gereksinimleri.
- `research/backlog.yml` — ilgili açık işler
  (`historical_events_and_culture_transition`, `ancient_economy_roads_and_town_ranks` vb.).
- Bu klasördeki veri dosyaları:
  `2026-10-17_egypt_culture_transition.yml` (Mısır geçiş kayıtları),
  `2026-10-17_egypt_event_design.md` (Mısır olay tasarım notu),
  `2026-10-17_gaul_culture_transition.yml` (Galya geçiş kayıtları),
  `2026-10-17_culture_graph_audit.md` (WS3 denetimi).
- `Extended Timeline/loading_screen/common/defines/00_defines.txt` — asimilasyon
  ve kültür sabitleri.
- Vanilla 1.3.x dosyaları: bölüm 2'deki tablo.
- EU5 Wiki: [Culture](https://eu5.paradoxwikis.com/Culture).
