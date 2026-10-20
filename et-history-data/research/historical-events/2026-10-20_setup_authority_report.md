# Setup Ülke Tanımları Otorite Raporu — 2026-10-20

`2026-10-20_vanilla_shadow_report.md`, `setup/countries` için 174 ölü (mod tanımı yüklenmiyor) ve 235 mod-içi çakışma (iki mod dosyası farklı değer taşıyor) bırakmıştı. Bu rapor, hangi dosyanın otorite olacağını offline kanıtla çözer, uygulanan birleştirmeyi ve fix sonrası durumu belgeler.

Üretici: `et-history-data/scripts/shadow-audit.py` (gölge modeli) + tek seferlik alan karşılaştırması (bu raporun ekleri). Veri değişikliği: `et_countries.txt` → `00_et_countries.txt`; 10 aynı-yol bölge override'ı silindi.

## Sonuç

| Konu | Sonuç |
|---|---|
| Otorite | `setup/countries/00_et_countries.txt` (eski `et_countries.txt`) |
| Silinen | 10 aynı-yol bölge override'ı (`bengal`, `british_isles`, `caucasus`, `east_asia`, `france`, `horn_of_africa`, `india`, `lowlands`, `maghreb`, `south_east_asia`) |
| Etkin tanımı değişen etiket | 277 (174 vanilla yenilgisi + 103 mod-içi yenilgi) |
| Düzeltilen kültür/din | 199 (133 + 66) |
| Niyet edilen veriyi kaybeden etiket | 0 |
| Fix sonrası setup | 663 gölgelenen = 663 yaşayan, 0 ölü, 0 mod-içi |
| Fix sonrası toplam | 669 gölgelenen = 669 yaşayan, 0 ölü, 0 mod-içi |

Kısa gerekçe: 10 override, vanilla bölge dosyalarının birebir kopyasıydı; vanilla'ya göre tek farkları 17 etiket düzenlemesiydi ve bu düzenlemelerin tamamı `et_countries` ile birebir aynıydı. Override'lar yeni bilgi taşımıyordu; yalnızca dosya sırası yüzünden `et_countries`'in 277 tanımını gölgeliyorlardı.

## Kanıt 1 — 18 Ekim log'u ve audit 663/663

18 Ekim 2026 oturumunun `debug.log` dosyasında `setup/countries` için tam **663** `Duplicated key` satırı vardır. Satırdaki `(key, kaybeden dosya)` çiftleri, `shadow-audit.py`'nin hesapladığı 663 çiftle birebir aynıdır: log-only **0**, audit-only **0**.

| Kaybeden sınıfı | Satır | Anlamı |
|---|---|---|
| `setup/countries/et_countries.txt` | 277 | 174 vanilla'ya + 103 aynı-yol override'a yeniliyordu |
| Vanilla bölge dosyaları | 254 | Mod tanımı kazanıyordu |
| 10 aynı-yol override | 132 | `et_countries` kazanıyordu; override tanımı ölüydü |
| **Toplam** | **663** | Her anahtar için bir kaybeden |

Bu dağılım, fix'in neden tek dosyada toplanması gerektiğini gösterir: `et_countries` 277 anahtarda yeniliyor, 386 anahtarda kazanıyordu; kazanan taraf dosya adının alfabetik sırasına göre bölge bölge değişiyordu.

## Kanıt 2 — 10 override vanilla kopyası

Her override, vanilla dosyasının tam kopyasıdır: anahtar kümeleri eşit, mod-only veya vanilla-only anahtar yok. Toplam 866 bloğun 849'u vanilla ile birebir aynı; yalnızca 17 etiket düzenlenmiş.

| Dosya | Vanilla blok | Birebir aynı | Farklı etiket | Mod-only / vanilla-only |
|---|---|---|---|---|
| `bengal.txt` | 27 | 25 | 2 (DGL, KTU) | 0 / 0 |
| `british_isles.txt` | 70 | 66 | 4 (CNN, DMS, LEI, ULS) | 0 / 0 |
| `caucasus.txt` | 27 | 25 | 2 (ALN, ARM) | 0 / 0 |
| `east_asia.txt` | 426 | 425 | 1 (DRG) | 0 / 0 |
| `france.txt` | 69 | 68 | 1 (BUR) | 0 / 0 |
| `horn_of_africa.txt` | 41 | 40 | 1 (MDI) | 0 / 0 |
| `india.txt` | 104 | 102 | 2 (GLI, SND) | 0 / 0 |
| `lowlands.txt` | 23 | 22 | 1 (FRI) | 0 / 0 |
| `maghreb.txt` | 22 | 20 | 2 (MZB, SOS) | 0 / 0 |
| `south_east_asia.txt` | 57 | 56 | 1 (KED) | 0 / 0 |
| **Toplam** | **866** | **849** | **17** | **0 / 0** |

## Kanıt 3 — 17 düzenleme `et_countries` ile birebir aynı

Override'ların vanilla'ya göre tek içerik farkı aşağıdaki 17 etikettir. Her satırda override değeri, `et_countries` değeriyle aynıdır; yani override'lar `et_countries`'e yeni bir kültür/din bilgisi eklemiyor, aynı düzeltmeyi ikinci kez taşıyor.

| Etiket | Dosya | Alan | Vanilla | Override = `et_countries` |
|---|---|---|---|---|
| `DGL` | `bengal.txt` | din | `sunni` | `hindu` |
| `KTU` | `bengal.txt` | din | `tibetan_buddhism` | `hindu` |
| `CNN` | `british_isles.txt` | din | `catholic` | `druidism` |
| `DMS` | `british_isles.txt` | kültür | `anglo_irish` | `irish` |
| `DMS` | `british_isles.txt` | din | `catholic` | `druidism` |
| `LEI` | `british_isles.txt` | din | `catholic` | `druidism` |
| `ULS` | `british_isles.txt` | kültür | `anglo_irish` | `irish` |
| `ULS` | `british_isles.txt` | din | `catholic` | `druidism` |
| `ALN` | `caucasus.txt` | din | `orthodox` | `alan_paganism` |
| `ARM` | `caucasus.txt` | din | `miaphysite` | `armenian_religion` |
| `DRG` | `east_asia.txt` | din | `tibetan_buddhism` | `bon` |
| `BUR` | `france.txt` | kültür | `burgundian` | `burgundione` |
| `BUR` | `france.txt` | din | `catholic` | `germanic_polytheism` |
| `MDI` | `horn_of_africa.txt` | din | `sunni` | `waaqeffanna_religion` |
| `GLI` | `india.txt` | din | `shia` | `hindu` |
| `SND` | `india.txt` | din | `shia` | `hindu` |
| `FRI` | `lowlands.txt` | din | `catholic` | `germanic_polytheism` |
| `MZB` | `maghreb.txt` | kültür | `mozabite` | `zenati` |
| `MZB` | `maghreb.txt` | din | `ibadi` | `berber_polytheism` |
| `SOS` | `maghreb.txt` | din | `sunni` | `berber_polytheism` |
| `KED` | `south_east_asia.txt` | din | `sunni` | `hindu` |

Bu 17 etiket, `b9f6ab9` ile kapatılan 17 aktif 58 AD etiketinin tamamıdır. Fix sonrası bu etiketlerin kültür/din değerleri `00_et_countries.txt`'ten aynen yüklenir; değer kaybı yoktur.

## Kanıt 4 — `et_countries` bütünlüğü

| Ölçüm | Sonuç |
|---|---|
| Üst düzey blok | 1753 |
| Yinelenen anahtar | 0 |
| Geçersiz `culture_definition` | 0 / 2242 kültür anahtarı |
| Geçersiz `religion_definition` | 0 / 330 din anahtarı |
| Eksik `color` / `color2` / kültür / din | 0 |
| Vanilla ile kesişim | 663 (2340 vanilla etiketinden) |
| Moda özel | 1090 |

Doğrulama, vanilla + mod kültür/din tanımlarının birleşimine karşı yapıldı; etkinleşen 277 blok dahil tüm dosya geçerli. Bu, fix'in oyun açılışında 'culture/religion not found' üretmeyeceğini gösterir.

## Etki analizi

| Sınıf | Anahtar | Kültür/din farkı | Etkin sonuç |
|---|---|---|---|
| Ölü (vanilla kazanıyordu) | 174 | 133 | `et_countries` değerleri yüklenir |
| Mod-içi, `et_countries` yeniliyordu | 103 | 66 | `et_countries` değerleri yüklenir |
| Mod-içi, `et_countries` kazanıyordu | 132 | 81 | Değişim yok; ölü override kopyası silinir |
| Mod lehine (vanilla kaybediyordu) | 254 | — | Değişim yok |
| **Etkin değişim** | **277** | **199** | 0 veri kaybı |

Kalan 78 etikette fark yalnızca metadata alanlarındadır (renk, açıklama kategorisi, zorluk, birim rengi, `is_historic`). `et_countries` stili (rgb renkler, `diplomatic`, zorluk 2) fix öncesinde de 386 etikette yürürlükteydi; fix bu tutarlılığı 663 etikete yayar. Vanilla'nın `map_*`/açıklama metadata'sını korumak isteyen ayrı bir birleştirme görevi yapılmadı; bu raporun kapsamı kültür/din otoritesidir.

Tarihsel olarak anlamlı örnekler (vanilla → `et_countries`):

- `BYZ` — din: `orthodox` → `chalcedonism`
- `BUL` — kültür: `bulgarian` → `bolghar_culture`; din: `orthodox` → `tengri`
- `CAR` — kültür: `slovene` → `danube_bavarian`; din: `catholic` → `chalcedonism`
- `CIL` — kültür: `armenian_culture` → `syriac_culture`; din: `miaphysite` → `hellenism_religion`
- `FZA` — kültür: `toubou_culture` → `eastern_amazigh`; din: `sunni` → `bantu_religion`
- `SWE` — din: `catholic` → `norse`
- `YEM` — din: `sunni` → `judaism`

## Neden taşıma veya etiket bazlı override değil?

- **Taşıma:** 277 tanımı 21 dosyanın (17 vanilla bölge dosyası + 4 erken sıralanan override) önüne taşımak, 21 aynı-yol kopya üretir. 10 override deneyi bu modelin kaçınılmaz olarak mod-içi çakışma ve bakım yükü ürettiğini gösterdi.
- **Etiket bazlı drop:** 199 kültür/din düzeltmesi ve 78 metadata geçişi kaybolur; 58 CE setup'ı vanilla 1337 değerlerine döner.
- **Tek dosya:** Tek kural — `00_` öneki göreli yol sırasında tüm vanilla dosyalarından önce gelir; 663 anahtarın tamamı moddan yüklenir, tek bakım noktası kalır.

## Uygulama ve doğrulama

```powershell
git mv "Extended Timeline/in_game/setup/countries/et_countries.txt" "Extended Timeline/in_game/setup/countries/00_et_countries.txt"
```

10 override dosyası ayrı ayrı `git rm` ile silindi (liste Sonuç tablosunda).

| Ölçüm | Fix öncesi | Fix sonrası |
|---|---|---|
| Setup gölgelenen | 663 | 663 |
| Setup ölü | 174 | **0** |
| Setup mod-içi | 235 | **0** |
| Setup yaşayan | 254 | **663** |
| Toplam ölü | 174 | **0** |
| Toplam mod-içi | 235 | **0** |
| Toplam yaşayan | 260 | **669** |

`shadow-audit.py` fix sonrası yeniden üretildi: `2026-10-20_vanilla_shadow_report.md` artık 0 ölü / 0 mod-içi gösteriyor. `et_countries` bütünlük kontrolü 1753 blokta 0 hata verdi.

### Test B beklentisi

- `Duplicated key` bilgi sınıfı **670** satır kalır (663 setup + 4 bilinen + 2 folk_european + 1 et_christianity).
- 663 setup satırının tamamında kaybeden artık **vanilla bölge dosyasıdır**; `setup/countries/00_et_countries.txt` veya silinen override adlarını gösteren setup satırı **0** olmalıdır.
- 18 Ekim log'undaki 277 `et_countries` ve 132 override kaybeden satırı yeni log'da görünmemelidir; satır sayısı yine 663'tür.

## Sınırlar

- Bu rapor statik modeldir; asıl teyit Test B log'unda kaybeden dosya adlarının vanilla'ya dönmesidir.
- Metadata birleştirmesi yapılmadı (yukarıdaki 78 etiket); istenirse ayrı görev.
- 18 Ekim log'u fix öncesi dosya adlarını taşır; yeni log'da yollar ve kaybeden adları değişecektir.

## Ek A — 174 ölü tanım (vanilla kazanan)

Alanlar `shadow-audit.py`'nin normalize edilmiş blok karşılaştırmasından; ok yönü **vanilla → et_countries**.

### `eastcoast.txt` — 31 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `APA` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `apalachee_culture` → `apache`; din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `BDK` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `bodewadomik_culture` → `ojibwe_culture`; din: `midewiwin_religion` → `iroquoian_totemism` |
| `CFQ` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `issati_culture` → `catawba_culture`; din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `CHC` | renk, renk2, açıklama, zorluk, din | din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `CHK` | renk, renk2, zorluk, din | din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `CLG` | renk, renk2, açıklama, zorluk, din | din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `COO` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `coosa_culture` → `muscogee_culture`; din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `COW` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `coweta_culture` → `muscogee_culture`; din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `ERI` | renk, renk2, kültür, açıklama, zorluk | kültür: `erielhonan_culture` → `tionontate_culture` |
| `HAT` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `hathawekela_culture` → `chalahgawtha_culture`; din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `JOA` | renk, renk2, açıklama, zorluk, din | din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `KKA` | renk, renk2, kültür, zorluk | kültür: `kanienkehaka_culture` → `onondowaga_culture` |
| `KPK` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `kispoko_culture` → `chalahgawtha_culture`; din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `KSK` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `kaskinampo_culture` → `cahokia_culture`; din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `MCG` | renk, renk2, açıklama, zorluk, din | din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `MCN` | renk, renk2, açıklama, zorluk, din | din: `midewiwin_religion` → `iroquoian_totemism` |
| `MSC` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `massachusett_culture` → `naadahende_culture`; din: `midewiwin_religion` → `iroquoian_totemism` |
| `MSK` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `meskwaki_culture` → `baxoje_culture`; din: `midewiwin_religion` → `iroquoian_totemism` |
| `NCZ` | renk, renk2, açıklama, zorluk, din | din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `OCT` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `oconee_culture` → `yamasee_culture`; din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `ONN` | renk, renk2, zorluk | — |
| `ONO` | renk, renk2, kültür, zorluk | kültür: `onondagega_culture` → `onondowaga_culture` |
| `ONY` | renk, renk2, kültür, zorluk | kültür: `onyotaaka_culture` → `onondowaga_culture` |
| `PEO` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `peewareewa_culture` → `cahokia_culture`; din: `midewiwin_religion` → `iroquoian_totemism` |
| `PQT` | renk, renk2, açıklama, zorluk, din | din: `midewiwin_religion` → `iroquoian_totemism` |
| `QUZ` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `chakchiuma_culture` → `natchez_culture`; din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `UNA` | renk, renk2, açıklama, zorluk, din | din: `midewiwin_religion` → `iroquoian_totemism` |
| `WMG` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `wampanoag_culture` → `massachusett_culture`; din: `midewiwin_religion` → `iroquoian_totemism` |
| `WRO` | renk, renk2, kültür, açıklama, zorluk | kültür: `wenrohronon_culture` → `tionontate_culture` |
| `WZZ` | renk, renk2, açıklama, zorluk, din | din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `YMS` | renk, renk2, açıklama, zorluk, din | din: `mississippian_ceremonial` → `iroquoian_totemism` |

### `east_africa.txt` — 30 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `ATK` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `antaisaka_culture` → `sakalava_culture`; din: `fomba_gasy_religion` → `bantu_religion` |
| `ATM` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `antaifasy_culture` → `sakalava_culture`; din: `fomba_gasy_religion` → `sunni` |
| `BAA` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `bara_culture` → `sakalava_culture`; din: `fomba_gasy_religion` → `bantu_religion` |
| `BNY` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `rutara_culture` → `baganda_culture`; din: `nyasaye_religion` → `bantu_religion` |
| `BOI` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `vezo_culture` → `sakalava_culture`; din: `fomba_gasy_religion` → `bantu_religion` |
| `BSG` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `rutara_culture` → `baganda_culture`; din: `nyasaye_religion` → `bantu_religion` |
| `BTS` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `betsimisaraka_culture` → `sakalava_culture`; din: `fomba_gasy_religion` → `bantu_religion` |
| `BUG` | renk, renk2, açıklama, zorluk, din | din: `cwezi_religion` → `bantu_religion` |
| `BUU` | renk, renk2, açıklama, zorluk | — |
| `KIT` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `rutara_culture` → `baganda_culture`; din: `cwezi_religion` → `bantu_religion` |
| `KRW` | renk, renk2, kültür, açıklama, zorluk | kültür: `nyamwezi_culture` → `baganda_culture` |
| `LDU` | renk, renk2, kültür, açıklama, zorluk | kültür: `chewa_culture` → `sena_culture` |
| `MBA` | renk, renk2, açıklama, zorluk | — |
| `MIR` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `merina_culture` → `sakalava_culture`; din: `fomba_gasy_religion` → `bantu_religion` |
| `MKU` | renk, renk2, açıklama, zorluk | — |
| `MLI` | renk, renk2, kültür, açıklama, zorluk | kültür: `yemeni_culture` → `swahili_culture` |
| `MNB` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `vezo_culture` → `sakalava_culture`; din: `fomba_gasy_religion` → `bantu_religion` |
| `MRA` | renk, renk2, kültür, açıklama, zorluk | kültür: `chewa_culture` → `sena_culture` |
| `NKO` | renk, renk2, kültür, açıklama, zorluk | kültür: `rutara_culture` → `baganda_culture` |
| `PTE` | renk, renk2, kültür, açıklama, zorluk | kültür: `yemeni_culture` → `swahili_culture` |
| `RWA` | renk, renk2, açıklama, zorluk | — |
| `SEN` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `sena_culture` → `bengali`; din: `bantu_religion` → `mahayana` |
| `SFA` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `swahili_culture` → `sena_culture`; din: `sunni` → `bantu_religion` |
| `SKA` | renk, renk2, açıklama, zorluk, din | din: `fomba_gasy_religion` → `bantu_religion` |
| `TBK` | renk, renk2, kültür, açıklama, zorluk | kültür: `rukwa_culture` → `sena_culture` |
| `UBH` | renk, renk2, açıklama, zorluk | — |
| `YAK` | renk, renk2, açıklama, zorluk | — |
| `ZAN` | renk, renk2, kültür, açıklama, zorluk | kültür: `matuumbi_culture` → `swahili_culture` |
| `ZMW` | renk, renk2, zorluk | — |
| `ZZB` | renk, renk2, açıklama, zorluk | — |

### `balkans.txt` — 19 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `ACH` | renk, renk2, kültür, açıklama, zorluk | kültür: `french` → `lombard` |
| `ALB` | renk, renk2, açıklama, zorluk | — |
| `ATH` | renk, renk2, kültür, açıklama, zorluk | kültür: `catalan` → `french` |
| `BOS` | renk, renk2, açıklama, zorluk, din | din: `bosnian_church` → `slavic_polytheism` |
| `BUL` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `bulgarian` → `bolghar_culture`; din: `orthodox` → `tengri` |
| `BYZ` | renk, renk2, açıklama, zorluk, din, birim rengi 0, birim rengi 1, birim rengi 2 | din: `orthodox` → `chalcedonism` |
| `CAR` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `slovene` → `danube_bavarian`; din: `catholic` → `chalcedonism` |
| `CEP` | renk, renk2, kültür, açıklama, zorluk | kültür: `french` → `lombard` |
| `CLI` | renk, açıklama, zorluk | — |
| `CRO` | renk, renk2, açıklama, zorluk, din | din: `catholic` → `slavic_polytheism` |
| `CRT` | renk2, kültür, açıklama, zorluk, din | kültür: `venetian` → `greek_culture`; din: `catholic` → `chalcedonism` |
| `EPI` | renk, renk2, açıklama, zorluk, din | din: `orthodox` → `chalcedonism` |
| `KNI` | renk2, kültür, açıklama, zorluk | kültür: `french` → `languedocien` |
| `LAT` | renk, renk2, açıklama, zorluk, tarihsel | — |
| `NAX` | renk, renk2, kültür, açıklama, zorluk | kültür: `venetian` → `lombard` |
| `NEO` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `catalan` → `greek_culture`; din: `catholic` → `chalcedonism` |
| `RAG` | renk, renk2, açıklama, zorluk | — |
| `SER` | renk, renk2, açıklama, din | din: `orthodox` → `slavic_polytheism` |
| `THE` | renk, renk2, kültür, açıklama, zorluk, tarihsel, din | kültür: `greek_culture` → `piedmontese`; din: `orthodox` → `catholic` |

### `anatolia.txt` — 17 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `AHI` | renk, renk2, açıklama, zorluk, din | din: `shia` → `sunni` |
| `AYD` | renk, açıklama, zorluk | — |
| `BHT` | renk, renk2, açıklama, zorluk, din | din: `yazidism` → `sunni` |
| `BIT` | renk, renk2, açıklama, zorluk | — |
| `CIL` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `armenian_culture` → `syriac_culture`; din: `miaphysite` → `hellenism_religion` |
| `CND` | renk, açıklama, zorluk | — |
| `CYP` | renk, kültür, açıklama, zorluk, din | kültür: `poitevin` → `greek_culture`; din: `catholic` → `chalcedonism` |
| `DUL` | renk, açıklama, zorluk, din | din: `shia` → `sunni` |
| `ERE` | renk, açıklama, zorluk | — |
| `GRM` | renk, açıklama, zorluk | — |
| `HMD` | renk, renk2, açıklama, zorluk | — |
| `HSN` | renk, kültür, açıklama, zorluk | kültür: `kurdish_culture` → `turkish_culture` |
| `KAR` | renk, açıklama, zorluk | — |
| `MEN` | renk, açıklama, zorluk | — |
| `TEK` | renk, renk2, açıklama, zorluk | — |
| `TRE` | renk, açıklama, zorluk, din | din: `orthodox` → `chalcedonism` |
| `TUR` | renk, açıklama, zorluk, birim rengi 0, birim rengi 1, birim rengi 2 | — |

### `aridoamerica.txt` — 11 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `ACO` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `keres_culture` → `ancestral_pueblo_culture`; din: `kachina_religion` → `iroquoian_totemism` |
| `CAD` | renk, renk2, açıklama, zorluk, din | din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `DNE` | renk, renk2, açıklama, zorluk, din | din: `dene_shamanism` → `iroquoian_totemism` |
| `HHK` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `hohokam_culture` → `pima_culture`; din: `cahita_religion` → `iroquoian_totemism` |
| `ISL` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `keres_culture` → `ancestral_pueblo_culture`; din: `kachina_religion` → `iroquoian_totemism` |
| `KER` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `keres_culture` → `ancestral_pueblo_culture`; din: `kachina_religion` → `iroquoian_totemism` |
| `OHK` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `tanoan_culture` → `ancestral_pueblo_culture`; din: `kachina_religion` → `iroquoian_totemism` |
| `PIM` | renk, renk2, açıklama, zorluk, din | din: `cahita_religion` → `iroquoian_totemism` |
| `TST` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `tanoan_culture` → `ancestral_pueblo_culture`; din: `kachina_religion` → `iroquoian_totemism` |
| `YAQ` | renk, renk2, açıklama, zorluk, din | din: `cahita_religion` → `iroquoian_totemism` |
| `ZNI` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `zuni_culture` → `ancestral_pueblo_culture`; din: `kachina_religion` → `iroquoian_totemism` |

### `canadian.txt` — 11 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `AGW` | renk, renk2, kültür, açıklama, zorluk | kültür: `attignawantan_culture` → `attigneenongnahac_culture` |
| `ARN` | renk, renk2, kültür, açıklama, zorluk | kültür: `arendaronon_culture` → `attigneenongnahac_culture` |
| `ATG` | renk, renk2, açıklama, zorluk | — |
| `MLS` | renk, renk2, açıklama, zorluk, din | din: `midewiwin_religion` → `iroquoian_totemism` |
| `MSG` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `missisage_culture` → `ojibwe_culture`; din: `midewiwin_religion` → `iroquoian_totemism` |
| `ODW` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `odawa_culture` → `ojibwe_culture`; din: `midewiwin_religion` → `iroquoian_totemism` |
| `OJI` | renk, renk2, açıklama, zorluk, din | din: `midewiwin_religion` → `iroquoian_totemism` |
| `OSG` | renk, renk2, kültür, açıklama, zorluk | kültür: `osheaga_culture` → `stadaconan_culture` |
| `STD` | renk, renk2, açıklama, zorluk | — |
| `TIO` | renk, renk2, açıklama, zorluk | — |
| `TRT` | renk, renk2, kültür, açıklama, zorluk | kültür: `taontaenrat_culture` → `attigneenongnahac_culture` |

### `_scandinavia.txt` — 10 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `BJA` | renk, renk2, kültür, açıklama, zorluk | kültür: `bjarmian` → `nenets_culture` |
| `DAN` | renk, renk2, açıklama, zorluk, din, birim rengi 0, birim rengi 1, birim rengi 2 | din: `catholic` → `norse` |
| `FIN` | renk, renk2, açıklama, zorluk, birim rengi 0, birim rengi 1, birim rengi 2 | — |
| `GRL` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `icelandic` → `inuit_culture`; din: `catholic` → `lutheran` |
| `ICE` | renk, renk2, açıklama, zorluk, din | din: `catholic` → `norse` |
| `KVE` | renk, renk2, kültür, açıklama, zorluk | kültür: `kvens` → `finnish` |
| `NOR` | renk, renk2, zorluk, din | din: `catholic` → `norse` |
| `SMI` | renk, renk2, açıklama, zorluk, din, birim rengi 0, birim rengi 1, birim rengi 2 | din: `sapmi_shamanism` → `muinaisusko` |
| `SWE` | renk, renk2, din, birim rengi 0, birim rengi 1, birim rengi 2 | din: `catholic` → `norse` |
| `TAV` | renk, renk2, kültür, açıklama, zorluk | kültür: `tavastian` → `finnish` |

### `andes.txt` — 8 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `CHM` | renk, renk2, açıklama, zorluk | — |
| `CRA` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `charka_culture` → `aimara_culture`; din: `mororuma_religion` → `inti` |
| `CSU` | renk, renk2, açıklama, zorluk | — |
| `CYA` | renk, renk2, açıklama, zorluk | — |
| `ICM` | renk, renk2, kültür, açıklama, zorluk | kültür: `ychsma_culture` → `aimara_culture` |
| `PCJ` | renk, renk2, açıklama, zorluk | — |
| `QTO` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `quitu_culture` → `cara_culture`; din: `pi_religion` → `inti` |
| `WAN` | renk, renk2, kültür, açıklama, zorluk | kültür: `wanka_culture` → `inka_culture` |

### `central_north_america.txt` — 8 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `ANL` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `tiou_culture` → `tunica_culture`; din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `CSQ` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `yazoo_culture` → `tunica_culture`; din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `KIA` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `kitkehaki_culture` → `tsawi_culture`; din: `great_plains_shamanism` → `iroquoian_totemism` |
| `KSP` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `kichesipirini_culture` → `chalahgawtha_culture`; din: `midewiwin_religion` → `iroquoian_totemism` |
| `KTK` | renk, renk2, açıklama, zorluk, din | din: `great_plains_shamanism` → `iroquoian_totemism` |
| `MIK` | renk, renk2, açıklama, zorluk, din | din: `midewiwin_religion` → `iroquoian_totemism` |
| `NST` | renk, renk2, açıklama, zorluk, din | din: `mississippian_ceremonial` → `iroquoian_totemism` |
| `PCH` | renk, renk2, açıklama, zorluk, din | din: `mississippian_ceremonial` → `iroquoian_totemism` |

### `arabia.txt` — 6 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `ANZ` | renk, renk2, açıklama, zorluk, din | din: `sunni` → `south_arabian_polytheism` |
| `DWS` | renk, renk2, açıklama, zorluk | — |
| `MDA` | renk, renk2, açıklama, zorluk, din | din: `shia` → `sunni` |
| `OMA` | renk, renk2, açıklama, zorluk, din | din: `ibadi` → `south_arabian_polytheism` |
| `YAS` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `kaliji_culture` → `bahrani_culture`; din: `sunni` → `south_arabian_polytheism` |
| `YEM` | renk, renk2, açıklama, zorluk, din | din: `sunni` → `judaism` |

### `baltics.txt` — 6 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `KRL` | renk, renk2, açıklama, zorluk | — |
| `KUR` | renk, renk2, kültür, açıklama, zorluk | kültür: `german_baltic` → `latvian` |
| `LIT` | renk, açıklama, zorluk | — |
| `LIV` | renk, renk2, açıklama, zorluk, birim rengi 0, birim rengi 1, birim rengi 2 | — |
| `RIG` | renk, renk2, açıklama, zorluk | — |
| `TEU` | renk, açıklama, zorluk, birim rengi 0, birim rengi 1, birim rengi 2 | — |

### `crescent.txt` — 4 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `ARD` | renk, renk2, açıklama, zorluk | — |
| `FDL` | renk2, kültür, açıklama, zorluk | kültür: `bedouin_culture` → `najdi_culture` |
| `JAL` | renk, renk2, açıklama, zorluk, din | din: `sunni` → `shia` |
| `KOJ` | renk, açıklama, zorluk, tarihsel | — |

### `brasil.txt` — 3 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `AVA` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `ava_culture` → `burmese_culture`; din: `tunpa_religion` → `theravada` |
| `TPA` | renk, renk2, açıklama, zorluk, din | din: `namandu_religion` → `muisca_religion` |
| `TPQ` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `tupiniquim_culture` → `tupinamba_culture`; din: `namandu_religion` → `muisca_religion` |

### `carpathia.txt` — 3 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `HUN` | renk, zorluk, din, birim rengi 0, birim rengi 1, birim rengi 2 | din: `catholic` → `tengri` |
| `TRA` | renk, kültür, açıklama, zorluk, din | kültür: `hungarian` → `wallachian`; din: `catholic` → `tengri` |
| `WAL` | renk, renk2, açıklama, zorluk, din | din: `orthodox` → `chalcedonism` |

### `egypt.txt` — 3 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `FZA` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `toubou_culture` → `eastern_amazigh`; din: `sunni` → `bantu_religion` |
| `MAM` | renk, renk2, açıklama, zorluk | — |
| `TRP` | renk, renk2, kültür, açıklama, zorluk | kültür: `libyan_arabic_culture` → `zenati` |

### `chaco.txt` — 2 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `CUA` | renk, renk2, açıklama, zorluk, din | din: `tunpa_religion` → `muisca_religion` |
| `MPC` | renk, renk2, açıklama, zorluk, din | din: `tain_feyentun_religion` → `muisca_religion` |

### `colombia.txt` — 2 etiket

| Etiket | Farklı alanlar | Kültür/din (vanilla → et) |
|---|---|---|
| `TAI` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `tayrona_culture` → `muisca_culture`; din: `naoma_religion` → `muisca_religion` |
| `ZIP` | renk, renk2, açıklama, zorluk | — |

## Ek B — 103 mod-içi kayıp (erken override kazanıyordu)

Bu anahtarlarda `et_countries`, aynı-yol override'a yeniliyordu; override vanilla kopyası olduğu için etkin değer çoğunlukla vanilla'ydı. Ok yönü **override → et_countries**.

### `east_asia.txt` (silinen override) — 63 etiket

| Etiket | Farklı alanlar | Kültür/din (override → et) |
|---|---|---|
| `AKM` | renk, renk2, açıklama, zorluk | — |
| `AKT` | renk, renk2, kültür, açıklama, zorluk | kültür: `touhoku_culture` → `saigoku_culture` |
| `AMD` | renk, renk2, açıklama, zorluk, din | din: `tibetan_buddhism` → `bon` |
| `ANU` | renk, renk2, açıklama, zorluk | — |
| `ASA` | renk, renk2, açıklama, zorluk | — |
| `BZU` | renk, renk2, açıklama, zorluk | — |
| `CBA` | renk, renk2, kültür, açıklama, zorluk | kültür: `tougoku_culture` → `saigoku_culture` |
| `CDL` | renk, renk2, açıklama, zorluk, din | din: `mahayana` → `bimoism` |
| `CHE` | renk, renk2, kültür, açıklama, zorluk, tarihsel | kültür: `chu_culture` → `jianghuai_culture` |
| `CHG` | renk, renk2, açıklama, zorluk | — |
| `CHH` | renk, renk2, kültür, açıklama, zorluk | kültür: `tai_lu_culture` → `khon_muang_culture` |
| `CHI` | renk, renk2, kültür, zorluk, din, birim rengi 0, birim rengi 1, birim rengi 2 | kültür: `mongolian_culture` → `yan_culture`; din: `tibetan_buddhism` → `sanjiao` |
| `CSH` | renk, açıklama, zorluk, tarihsel | — |
| `CSK` | renk, renk2, açıklama, zorluk | — |
| `CXI` | renk, renk2, kültür, açıklama, zorluk, tarihsel | kültür: `shu_culture` → `zhongyuan_culture` |
| `DDI` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `dai_culture` → `khitan`; din: `satsana_phi` → `tengri` |
| `DRG` | renk, renk2, açıklama, zorluk | — |
| `DTE` | renk, renk2, kültür, açıklama, zorluk | kültür: `touhoku_culture` → `saigoku_culture` |
| `GUG` | renk, renk2, açıklama, zorluk | — |
| `HSK` | renk, renk2, açıklama, zorluk | — |
| `HTK` | renk, renk2, kültür, açıklama, zorluk | kültür: `tougoku_culture` → `saigoku_culture` |
| `IKE` | renk, renk2, açıklama, zorluk | — |
| `IMG` | renk, renk2, kültür, açıklama, zorluk | kültür: `tougoku_culture` → `saigoku_culture` |
| `ISK` | renk, renk2, açıklama, zorluk | — |
| `ITO` | renk, renk2, açıklama, zorluk | — |
| `JAP` | renk, renk2, zorluk | — |
| `KKC` | renk, renk2, kültür, açıklama, zorluk | kültür: `kyushu_culture` → `saigoku_culture` |
| `KOR` | renk, renk2, din | din: `mahayana` → `sanjiao` |
| `KTB` | renk, renk2, açıklama, zorluk | — |
| `LJG` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `nashi_culture` → `yi_culture`; din: `dongba_religion` → `bimoism` |
| `LTN` | renk, renk2, açıklama, zorluk | — |
| `MIO` | renk, renk2, açıklama, zorluk, din | din: `hmongism` → `bimoism` |
| `MMA` | renk, renk2, kültür, açıklama, zorluk | kültür: `tai_nua_culture` → `khon_muang_culture` |
| `MMI` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `saigoku_culture` → `cahokia_culture`; din: `shinto` → `iroquoian_totemism` |
| `MNG` | renk, açıklama, zorluk, tarihsel | — |
| `MRI` | renk, renk2, açıklama, zorluk | — |
| `NIT` | renk, renk2, kültür, açıklama, zorluk | kültür: `tougoku_culture` → `saigoku_culture` |
| `NVK` | renk, renk2, açıklama, zorluk, din | din: `tungusic_shamanism` → `ainu_religion` |
| `ODA` | renk, renk2, açıklama, zorluk | — |
| `OGS` | renk, renk2, kültür, açıklama, zorluk | kültür: `tougoku_culture` → `saigoku_culture` |
| `OIR` | renk, renk2, açıklama, zorluk, tarihsel | — |
| `ORQ` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `oroqen_culture` → `jurchen_culture`; din: `tungusic_shamanism` → `tengri` |
| `OTM` | renk, renk2, kültür, açıklama, zorluk | kültür: `kyushu_culture` → `saigoku_culture` |
| `OUC` | renk, renk2, açıklama, zorluk | — |
| `SBA` | renk, renk2, kültür, açıklama, zorluk | kültür: `touhoku_culture` → `saigoku_culture` |
| `SHI` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `jurchen_culture` → `afghan_culture`; din: `tungusic_shamanism` → `mahayana` |
| `SIB` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `sibe_culture` → `jurchen_culture`; din: `tungusic_shamanism` → `tengri` |
| `SKK` | renk, renk2, kültür, açıklama, zorluk | kültür: `sikkim_culture` → `ngalop_culture` |
| `SMZ` | renk, renk2, kültür, açıklama, zorluk | kültür: `kyushu_culture` → `saigoku_culture` |
| `SOU` | renk, renk2, kültür, açıklama, zorluk | kültür: `kyushu_culture` → `saigoku_culture` |
| `STK` | renk, renk2, kültür, açıklama, zorluk | kültür: `tougoku_culture` → `saigoku_culture` |
| `SZH` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `tujia_culture` → `hmong_culture`; din: `nuo_religion` → `bimoism` |
| `TIB` | renk, renk2, açıklama, zorluk, din | din: `tibetan_buddhism` → `bon` |
| `TIM` | renk, kültür, açıklama, zorluk, tarihsel | kültür: `khorezmian_culture` → `uzbek_culture` |
| `TKD` | renk, renk2, kültür, açıklama, zorluk | kültür: `tougoku_culture` → `saigoku_culture` |
| `TKI` | renk, renk2, kültür, açıklama, zorluk | kültür: `tougoku_culture` → `saigoku_culture` |
| `TMN` | renk, renk2, açıklama, zorluk, din | din: `mahayana` → `muism` |
| `UES` | renk, renk2, kültür, açıklama, zorluk | kültür: `tougoku_culture` → `saigoku_culture` |
| `UTN` | renk, renk2, kültür, açıklama, zorluk | kültür: `tougoku_culture` → `saigoku_culture` |
| `WUU` | renk, açıklama, zorluk, tarihsel | — |
| `YMN` | renk, renk2, kültür, açıklama, zorluk | kültür: `tougoku_culture` → `saigoku_culture` |
| `YMT` | renk, renk2, açıklama, zorluk, tarihsel | — |
| `YUA` | renk, renk2, açıklama, zorluk, tarihsel | — |

### `british_isles.txt` (silinen override) — 21 etiket

| Etiket | Farklı alanlar | Kültür/din (override → et) |
|---|---|---|
| `CET` | renk, renk2, açıklama, zorluk | — |
| `CNN` | renk, renk2, açıklama, zorluk | — |
| `CRN` | renk, renk2, açıklama, zorluk, din, birim rengi 0, birim rengi 1, birim rengi 2 | din: `catholic` → `chalcedonism` |
| `DMS` | renk, renk2, açıklama, zorluk | — |
| `ENG` | renk, renk2, kültür, açıklama, zorluk, birim rengi 0, birim rengi 1, birim rengi 2 | kültür: `english` → `anglo_saxon` |
| `FLY` | renk, renk2, açıklama, zorluk, din | din: `catholic` → `druidism` |
| `KID` | renk, renk2, kültür, açıklama, zorluk | kültür: `anglo_irish` → `irish` |
| `LEI` | renk, renk2, açıklama, zorluk | — |
| `LOI` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `norse_gael` → `norwegian`; din: `catholic` → `norse` |
| `MCM` | renk, renk2, açıklama, zorluk, din | din: `catholic` → `druidism` |
| `MNN` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `norse_gael` → `highland`; din: `catholic` → `chalcedonism` |
| `MTH` | renk, renk2, açıklama, zorluk, din | din: `catholic` → `druidism` |
| `NOL` | renk, renk2, kültür, açıklama, zorluk, din, birim rengi 0, birim rengi 1, birim rengi 2 | kültür: `northumbrian` → `anglo_saxon`; din: `catholic` → `chalcedonism` |
| `ORD` | renk, renk2, kültür, açıklama, zorluk | kültür: `anglo_irish` → `irish` |
| `SCO` | renk, renk2, kültür, açıklama, zorluk, din, birim rengi 0, birim rengi 1, birim rengi 2 | kültür: `scottish` → `highland`; din: `catholic` → `chalcedonism` |
| `SLN` | renk, renk2, açıklama, zorluk | — |
| `THO` | renk, renk2, açıklama, zorluk | — |
| `TRY` | renk, renk2, açıklama, zorluk, din | din: `catholic` → `druidism` |
| `TYR` | renk, renk2, açıklama, zorluk, din | din: `catholic` → `druidism` |
| `ULS` | renk, renk2, açıklama, zorluk | — |
| `WLS` | renk, renk2, kültür, açıklama, zorluk, din, birim rengi 0, birim rengi 1, birim rengi 2 | kültür: `english` → `welsh`; din: `catholic` → `druidism` |

### `bengal.txt` (silinen override) — 11 etiket

| Etiket | Farklı alanlar | Kültür/din (override → et) |
|---|---|---|
| `AHO` | renk, renk2, açıklama, zorluk | — |
| `DGL` | renk, renk2, kültür, açıklama, zorluk | kültür: `dhivehi_culture` → `sinhalese` |
| `DTI` | renk, renk2, kültür, açıklama, zorluk | kültür: `kumaoni` → `newar_culture` |
| `GWL` | renk, renk2, açıklama, zorluk, din | din: `hindu` → `mahayana` |
| `JNT` | renk, renk2, açıklama, zorluk, din | din: `hindu` → `bimoism` |
| `KHS` | renk, renk2, kültür, açıklama, zorluk | kültür: `khas_culture` → `newar_culture` |
| `KMA` | renk, renk2, açıklama, zorluk, din | din: `hindu` → `mahayana` |
| `KMN` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `kumaoni` → `garhwali`; din: `hindu` → `mahayana` |
| `KTU` | renk, renk2, açıklama, zorluk | — |
| `LUR` | renk, renk2, kültür, açıklama, zorluk | kültür: `bengali` → `khasi_culture` |
| `LWA` | renk, renk2, kültür, açıklama, zorluk, din | kültür: `limbu_culture` → `newar_culture`; din: `hindu` → `mahayana` |

### `caucasus.txt` (silinen override) — 8 etiket

| Etiket | Farklı alanlar | Kültür/din (override → et) |
|---|---|---|
| `ALN` | renk, renk2, açıklama, zorluk | — |
| `ARM` | renk, renk2, açıklama, zorluk | — |
| `AVR` | renk, renk2, açıklama, zorluk, din | din: `sunni` → `tengri` |
| `CIR` | renk, renk2, açıklama, zorluk, tarihsel, din | din: `orthodox` → `tengri` |
| `GEO` | renk, renk2, açıklama, din | din: `orthodox` → `chalcedonism` |
| `IME` | renk, renk2, açıklama, zorluk | — |
| `KCN` | renk, renk2, açıklama, zorluk | — |
| `SME` | renk, renk2, açıklama, zorluk, din | din: `orthodox` → `chalcedonism` |

## Ek C — 132 mod-içi kayıp (et zaten kazanıyordu)

Bu anahtarlarda etkin değer zaten `et_countries` idi; silinen override tanımları yalnızca dosya kirliliğiydi. Kültür/din değerleri değişmez.

- **`india.txt`** — 31: `BGK`, `BND`, `BST`, `CHD`, `DHU`, `DLH`, `GLI`, `GWA`, `HAD`, `HSL`, `IDR`, `JFN`, `JLW`, `JNG`, `JSL`, `KGR`, `KJA`, `KLH`, `KSH`, `MEW`, `MRW`, `ORI`, `PLT`, `PTN`, `RDY`, `RJI`, `RTP`, `SND`, `TNK`, `VIJ`, `VND`
- **`south_east_asia.txt`** — 28: `ARK`, `BPR`, `BVK`, `DAI`, `HSE`, `HSI`, `KAL`, `KED`, `KHM`, `KTG`, `KUY`, `LAV`, `LGK`, `LIG`, `LNA`, `MKA`, `MLB`, `MNI`, `MYA`, `PAH`, `PEG`, `PHY`, `SAG`, `SNG`, `SUK`, `TNG`, `VTN`, `WAS`
- **`france.txt`** — 26: `ALE`, `ALS`, `AMG`, `ANJ`, `AQN`, `AUV`, `BAR`, `BER`, `BOU`, `BRI`, `BUR`, `CHP`, `DAU`, `FOI`, `FRA`, `GNV`, `GUY`, `LOR`, `MIE`, `NEV`, `NRM`, `ORL`, `PIC`, `PRO`, `SAV`, `TOU`
- **`horn_of_africa.txt`** — 23: `ABW`, `ADA`, `AFA`, `AJU`, `ALO`, `BTI`, `DAJ`, `DAM`, `DAW`, `DHK`, `ENN`, `ETH`, `GJJ`, `GLE`, `HDY`, `HRL`, `IFA`, `JRN`, `MAK`, `MDI`, `MED`, `SOA`, `WAR`
- **`maghreb.txt`** — 14: `ALG`, `DJE`, `FEZ`, `GBS`, `MOR`, `MRK`, `MZB`, `SLE`, `SOS`, `TET`, `TFL`, `TGT`, `TLE`, `TUN`
- **`lowlands.txt`** — 10: `BRB`, `FLA`, `FRI`, `HAI`, `HOL`, `LIE`, `LIM`, `LUX`, `NAM`, `UTR`

## Ek D — 17 düzenlemenin tam değerleri

| Etiket | Dosya | Alan | Vanilla | Override | `et_countries` |
|---|---|---|---|---|---|
| `DGL` | `bengal.txt` | din | `sunni` | `hindu` | `hindu` |
| `KTU` | `bengal.txt` | din | `tibetan_buddhism` | `hindu` | `hindu` |
| `CNN` | `british_isles.txt` | din | `catholic` | `druidism` | `druidism` |
| `DMS` | `british_isles.txt` | kültür | `anglo_irish` | `irish` | `irish` |
| `DMS` | `british_isles.txt` | din | `catholic` | `druidism` | `druidism` |
| `LEI` | `british_isles.txt` | din | `catholic` | `druidism` | `druidism` |
| `ULS` | `british_isles.txt` | kültür | `anglo_irish` | `irish` | `irish` |
| `ULS` | `british_isles.txt` | din | `catholic` | `druidism` | `druidism` |
| `ALN` | `caucasus.txt` | din | `orthodox` | `alan_paganism` | `alan_paganism` |
| `ARM` | `caucasus.txt` | din | `miaphysite` | `armenian_religion` | `armenian_religion` |
| `DRG` | `east_asia.txt` | din | `tibetan_buddhism` | `bon` | `bon` |
| `BUR` | `france.txt` | kültür | `burgundian` | `burgundione` | `burgundione` |
| `BUR` | `france.txt` | din | `catholic` | `germanic_polytheism` | `germanic_polytheism` |
| `MDI` | `horn_of_africa.txt` | din | `sunni` | `waaqeffanna_religion` | `waaqeffanna_religion` |
| `GLI` | `india.txt` | din | `shia` | `hindu` | `hindu` |
| `SND` | `india.txt` | din | `shia` | `hindu` | `hindu` |
| `FRI` | `lowlands.txt` | din | `catholic` | `germanic_polytheism` | `germanic_polytheism` |
| `MZB` | `maghreb.txt` | kültür | `mozabite` | `zenati` | `zenati` |
| `MZB` | `maghreb.txt` | din | `ibadi` | `berber_polytheism` | `berber_polytheism` |
| `SOS` | `maghreb.txt` | din | `sunni` | `berber_polytheism` | `berber_polytheism` |
| `KED` | `south_east_asia.txt` | din | `sunni` | `hindu` | `hindu` |
