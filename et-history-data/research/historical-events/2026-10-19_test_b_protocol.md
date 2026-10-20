# Test B koşum protokolü — Mısır + Galya zincir doğrulaması (tek oturum)

**Tarih:** 19 Ekim 2026, Mısır eki 20 Ekim 2026 · **Durum:** koşum takımı
hazır, oyun içi koşum bekliyor.
**Ön koşul:** UPDATE 19 düzeltme paketi (commit `a718859`): 103 kapsam
düzeltmesi, `swiss_culture` onarımı, `jewish` kültürü, 5 eksik dil tanımı,
TR loc girdileri. Ayrıntı: `backlog.yml` UPDATE 19.
**20 Ekim eki:** `origin/main` senkronu (merge `aeee7f1`) — Gaul yeniden
numaralandırması (`.103`–`.105`), `outcome = good` → `positive` ve Mısır
Nübya + siyasi zincirleri aynı dosyada; koşumlar R1b/R1c olarak eklendi.

## Amaç

Tek oyun oturumunda beş alt koşum:

| Koşum | Sahip | Aralık | Olaylar |
|---|---|---|---|
| R1 Mısır | ROM | 58 → 1200 | `et_culture.1`–`.5` (direnç dalı dahil) |
| R1b Nübya | MERO | 300 → 900 | `.6`–`.7` (`et_nubia_yearly_pulse`) |
| R1c Mısır siyasi | ROM → BYZ | 214 → 969 | `.8`, `.10`–`.15` (yıllık nabız); `.9`, `.16` (işgalci nabzı) |
| R2 Galya (Roma) | ROM | 58 → ~490 | `.101`–`.109` |
| R3 Galya (Frenk/Fransa) | FRAN → FRA | ~490 → 2026 | `.110`–`.113` / `.114`–`.123` |

Ayrıca bu oturum sınıf-1 gizemini kapatacak veriyi üretir (mevcut
`*_language` anahtarlarının referans hataları) ve UPDATE 19 düzeltmelerinin
log etkisini gösterir.

## Dosyalar

- Hazırlık aracı: `et-history-data/scripts/test-b-prepare.py`
- Rapor aracı: `et-history-data/scripts/test-b-report.py`
- Ham kanıt (depo dışı): `et-history-data/tests/<zaman>_test_b/`
- Mısır zinciri tasarımı ve R1 adımları: `2026-10-17_egypt_event_design.md` bölüm 5

## Hazırlık (oyun kapalıyken)

1. `python et-history-data/scripts/test-b-prepare.py`
   — canlı logları yedekler, `debug.log`/`error.log`'u siler, koşum
   klasörünü açar (`run_info.txt`: git revizyonu + mod dosya özetleri).
2. Oyunu console+debug ile başlat:
   `"C:\Users\samet\Desktop\Europa Universalis V\binaries\eu5.exe" -debug_mode -console`
   (ya da Steam başlatma seçeneklerine `-debug_mode -console` ekleyin).
3. Yeni oyun: **58 CE, ROM** olarak başla; kaydet (öneri: `et_test_b_58`).

**Not:** Oturum boyunca `Log.ClearErrorLog` kullanmayın; kanıt biriksin.

## R1 — Mısır (ROM, 58 → 1200)

Ayrıntılı adımlar tasarım notu bölüm 5'te; özet kontrol listesi:

1. `event_probabilities yearly_country_pulse` → dökümde
   `et_egypt_yearly_pulse` görünmeli (kanca kanıtı).
2. `test_event_trigger et_culture.1` → **FAIL** beklenir (58 < pencere).
3. `change_date 250` → tekrar `test_event_trigger et_culture.1` → **PASS**.
4. Doğal ateşleme: yıl sınırını geçir (`tick_day`; gerekirse hız 5'te
   oynat) → `.1` penceresi çıkar → **önce kaydet** (`et_test_b_egypt_choice`).
5. **Direnç dalı:** `.1`'de direnç seçeneğini seç → `change_date 600` →
   `.2`–`.5` ateşlenmemeli (zincir burada durur).
6. `et_test_b_egypt_choice` kaydını yükle → `.1`'de **tarihsel** seçenek →
   `change_date 350` → `.2` doğal ateşlenir → `change_date 1100` → `.4` →
   `change_date 1200` → `.5`. (`.3` sahip-kapısı: ROM putperestken trigger
   FAIL; etkiler `event et_culture.3` ile zorlanır — gerekçe bölüm 5.)
7. Kapanış: panoda İslam çoğunluk + Kıptî azınlık + Mısır kültürleri;
   `test_event_trigger et_culture.1` → FAIL (tekilleştirme kanıtı).

## R1b — Nübya kültür zinciri (MERO, 300 → 900)

`et_test_b_58` kaydını yükle. `event_probabilities yearly_country_pulse`
dökümünde `et_nubia_yearly_pulse` da görünmeli (ikinci kanca kanıtı);
58 başlangıcında bölgenin sahibi MERO.

1. `test_event_trigger et_culture.6` → FAIL (58 < 300).
2. `change_date 350` → `test_event_trigger et_culture.6` PASS; birkaç ay
   akıt → `.6` doğal ateşlenir (Meroe'nin sessizliği; tarihsel seçenek
   kushite → nubian).
3. `change_date 600` → `test_event_trigger et_culture.7` PASS (536–900);
   doğal ateşleme → `.7` (Nobatia'nın vaftizi; nubian +
   egyptian_polytheism → miaphysite).
4. Çift ateşleme kontrolü: tekrar `test_event_trigger` → FAIL
   (`has_variable`: `et_nubia_6_fired` / `et_nubia_7_fired`).
5. Kaydet: `et_test_b_nubia`.

## R1c — Mısır siyasi zinciri (214 → 969)

`et_test_b_58` kaydını yükle. Zincir sahip-agnostik nabızlarda çalışır:
`.8` ve `.10`–`.15` → `et_egypt_yearly_pulse` (`owns`); `.9` ve `.16` →
`et_egypt_occupier_pulse` (`controls`). Ayrıntı: siyasi tasarım notu bölüm 5
(`2026-10-18_egypt_political_chain_design.md`).

| `tag` | `change_date` | Olay | Pencere |
|---|---|---|---|
| ROM | 215 | `.8` | 214–217 |
| RASH | 640 | `.10` | 639–650 |
| UMAY | 705 | `.11` | 700–712 |
| ABBA | 830 | `.12` | 825–835 |
| EGY | 870 | `.13` | 866–880 |
| EGY | 940 | `.14` | 933–945 |
| FATI | 970 | `.15` | 968–978 |
| ERA | 620 | `.9` | 618–630 (control) |
| BYZ | 645 | `.16` | 644–647 (control) |

- Her durakta: `test_event_trigger et_culture.N` → PASS; birkaç ay akıt →
  doğal ateşleme; sonra tekrar `test_event_trigger` → FAIL (`has_variable`
  kilidi; çift ateşleme yok).
- R2 sırasında ROM 214–217'den geçerken `.8` doğal düşebilir (Mısır'ın
  sahibi ROM) — beklenen; R2 akışını bozmaz.
- `.9` / `.16`: state katmanının ERA/BYZ kontrol pencereleri oyun içinde
  doğrulanmadı. `controls` FAIL verirse bulgu `egypt_political_chain_batch2`
  kapsamında backlog'a yazılır; olay hatası sayılmaz.
- Kaydet: `et_test_b_egypt_political`.

## R2 — Galya / Roma (58 → ~490)

`et_test_b_58` kaydını yükle. Başlangıç sahibi ROM (58 başlangıcı).

- `list_dhe_for` → Galya pencerelerinin ROM için listelendiğini doğrula
  (etiket bağı kanıtı).
- Tarih atlamaları: her durakta birkaç ay akıt (DHE aylık zar;
  `monthly_chance` 10–25) ve pencereyi bekle; teyit: `event_counts`.

| Durak | Beklenen olay | Pencere |
|---|---|---|
| `change_date 80` | `.101` | 58–100 |
| `change_date 140` | `.102` | 100–180 |
| `change_date 200` | `.103` | 177–350 |
| `change_date 220` | `.104` | 212–230 |
| `change_date 266` | `.105` | 260–274 |
| `change_date 375` | `.106` | 371–400 |
| `change_date 390` | `.107` | 380–550 |
| `change_date 420` | `.108` | 406–443 |
| `change_date 470` | `.109` | 457–486 |

- Pencereler örtüşür; bir durakta iki olay birden düşebilir (normal).
- Kaydet: `et_test_b_gaul_rom`.

## R3 — Galya / Frenk ve Fransa (~490 → 2026)

`tag FRAN` → `list_dhe_for` (FRAN pencereleri). FRAN çağrılamazsa bunu not
edin — `gaul_dhe_tag_binding_review` bulgusudur.

| Durak | Beklenen olay | Pencere |
|---|---|---|
| `change_date 500` | `.110` | 496–508 |
| `change_date 700` | `.111` | 650–850 |
| `change_date 830` | `.112` | 813–842 |
| `change_date 950` | `.113` | 911–1000 |

`tag FRA` → `list_dhe_for` (FRA pencereleri).

| Durak | Beklenen olay | Pencere |
|---|---|---|
| `change_date 1215` | `.114` | 1209–1229 |
| `change_date 1400` | `.115` | 1337–1453 |
| `change_date 1539` | `.116` | 1539–1540 |
| `change_date 1600` | `.117` | 1562–1685 |
| `change_date 1790` | `.118` | 1789–1794 |
| `change_date 1882` | `.119` | 1881–1883 |
| `change_date 1905` | `.120` | 1905–1906 |
| `change_date 1916` | `.121` | 1914–1919 |
| `change_date 1960` | `.122` | 1945–1975 |
| `change_date 2000` | `.123` | 1992–2009 |

- Kapanış: `change_date 2050` — zincir sonrası serbest akış gözlemi.
- Kaydet: `et_test_b_gaul_fra_final`.

## Oturum sonrası

1. `python et-history-data/scripts/test-b-report.py`
   — logları koşum klasörüne kopyalar, `report.md` üretir; çıkış kodu
   0 = temiz, 1 = inceleme gerekiyor.
2. Beklenen: kapsam 0, `et_german` satırı 0, 5 yeni dil ref'i 0; sınıf-1
   satırları ise gözlem (gizem verisi).
3. Konsol çıktıları + önemli panolar rapora eklenir; sonuç backlog'a
   işlenir (`gaul_record_backfill`, `gaul_dhe_tag_binding_review`,
   `egypt_political_chain_batch2` state katmanı bulguları;
   `et_culture.9000` emekliliği Test B'ye bağlı).

### Beklenen bilgi sınıfı (regresyon değil)

`test-b-report.py` bu satırları ayrı sayar; taban değerler 18 Ekim
oturumundan gelir:

- `Duplicated key ... will not be created`: 670 satır (et_german hariç;
  663 setup + 4 bilinen anahtar + 2 folk_european + 1 et_christianity).
  Taşıma sonrası aramaic/coptic/miaphysite satırlarında kaybeden dosya
  vanilla olur; satır sayısı değişmez.
- Kullanılmayan değişken uyarısı: 8 (`et_egypt_*` direnç/çoğunluk
  değişkenleri). Mısır zinciri bunları set ediyor, okumuyor; bilinçli kabul
  (18 Ekim analizi). Siyasi zincirin `et_egypt_polit_*_fired` ve Nübya'nın
  `et_nubia_*_fired` değişkenleri trigger'da okunur — yeni satır beklenmez.
- `could not be found in the database`: 1 (`ubian`, et_countries.txt:12849).
  `ubian` kültürü `et_german.txt:369`'da tanımlı; 18 Ekim satırı
  `swiss_culture {` sözdizimi hatasının alan çağlayanıydı (UPDATE 19:
  `swiss_culture = {`). Test B'de 0 beklenir.
- Sınıf-1 `*_language` referansları: 13 satır / 7 anahtar; gözlem verisi
  (rapor bölüm 2), kapanış Test B loguna bağlı.

## Kabul kriterleri

- Zincirler hedeflenen yönlerde ve sırayla ateşlenir; direnç dalı zinciri
  durdurur; etiket bağları (ROM/FRAN/FRA) `list_dhe_for` ile doğrulanır.
- Mısır siyasi zinciri `.8`–`.16` hedeflenen etiket/yıllarda ateşlenir;
  `.9`/`.16` yalnızca işgalci nabzındadır; `has_variable` kilidi çift
  ateşlemeyi engeller. R1b'de `.6`–`.7` MERO sahipliğinde ateşlenir.
- Loglarda mod kaynaklı **yeni** hata yok; UPDATE 19 hedefleri temiz.
- Sınıf-1 için veri: ya satırlar gitmiştir (çözüldü) ya da dosya
  bağlamıyla belgelenmiş şekilde durur (açık kalır, backlog güncellenir).
