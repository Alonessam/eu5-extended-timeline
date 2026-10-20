# Vanilla Anahtar Gölge Raporu (offline) — 2026-10-20

`vanilla_key_shadow_review` tamamlanmış görünüyordu; ancak 18 Ekim 2026 log'undaki `Duplicated key ... will not be created` satırları, niyet edilen bazı mod tanımlarının oyuna hiç girmediğini gösterdi. Bu rapor, oyunu çalıştırmadan ilgili tüm DB'lerde aynı üst düzey anahtarı tanımlayan dosyaları karşılaştırır ve kazananı listeler.

Üretici: `et-history-data/scripts/shadow-audit.py` (offline, stdlib). Yeniden üretmek için repo kökünden `python et-history-data/scripts/shadow-audit.py` çalıştırın.

## Yöntem

- Kural: aynı DB içinde aynı üst düzey anahtar birden fazla dosyada tanımlıysa, göreli dosya yolunun alfabetik sırasında **önce gelen** tanım yüklenir; sonraki tanım oluşturulmaz. 18 Ekim log'undaki dört bağımsız vaka (aramaic, gothic, coptic, miaphysite) bu kuralı doğrular.
- Aynı göreli yola sahip mod dosyası vanilla dosyasını birebir değiştirir; bu dosyalar rakip sayılmadı ve aşağıda kasıtlı override olarak listelendi.
- İçerik karşılaştırması: blok gövdesi yorumlardan ve boşluktan arındırılıp birebir karşılaştırılır. `aynı` = kaybedilen tanım kazananla özdeş (zararsız); `farklı` = mod deltası gerçekten kayıp.
- Kapsam: dil, kültür, din, kültür grubu, din grubu, dil ailesi ve `setup/countries`. `common/on_action` ayrı ele alındı (blok birleşimi kuralı).
- İç içe alan (field) çakışmaları kapsam dışıdır; 18 Ekim'deki `et_german.txt` seli bu sınıftaydı ve UPDATE 19 ile giderildi.

## Özet

| DB | Vanilla dosya | Mod dosya | Aynı-yol override | Gölgelenen anahtar | Ölü | Yaşayan | Mod-içi | Vanilla-içi |
|---|---|---|---|---|---|---|---|---|
| `common/languages` | 53 | 10 | 2 | 2 | 1 | 1 | 0 | 0 |
| `common/cultures` | 52 | 23 | 5 | 1 | 1 | 0 | 0 | 0 |
| `common/religions` | 29 | 13 | 0 | 3 | 1 | 2 | 0 | 0 |
| `common/culture_groups` | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| `common/religion_groups` | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| `common/language_families` | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| `setup/countries` | 45 | 11 | 10 | 663 | 174 | 254 | 235 | 0 |
| **Toplam** | 182 | 60 | 17 | 669 | 177 | 257 | 235 | 0 |

## Bilinen dokuz yeniden tanım

| Anahtar | DB | Kazanan | Kaybeden | Sonuç | Not |
|---|---|---|---|---|---|
| `coptic_culture` | common/cultures | `common/cultures/egypt.txt` | `common/cultures/et_egypt.txt` (mod, farklı) | ÖLÜ (vanilla kazandı) |  |
| `haixi_culture` | common/cultures | — | — | çakışma yok (tek tanım) | Mod tanımı yükleniyor |
| `hurga_culture` | common/cultures | — | — | çakışma yok (tek tanım) | Mod tanımı yükleniyor |
| `aramaic_language` | common/languages | `common/languages/00_crescent.txt` | `common/languages/00_et_mesopotamian.txt` (mod, farklı) | ÖLÜ (vanilla kazandı) |  |
| `gothic_language` | common/languages | `common/languages/00_et_germany.txt` | `common/languages/00_germany.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |  |
| `alan_paganism` | common/religions | `common/religions/et_caucasus.txt` | `common/religions/folk_european.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |  |
| `hellenism_religion` | common/religions | `common/religions/et_roman.txt` | `common/religions/folk_european.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |  |
| `miaphysite` | common/religions | `common/religions/christian.txt` | `common/religions/et_christianity.txt` (mod, farklı) | ÖLÜ (vanilla kazandı) |  |
| `yearly_country_pulse` | on_action | — | — | ÖZEL: blok birleşimi | Aşağıdaki on_action notu |

Denetim notu 20 Ekim 2026'da düzeltildi: `coptic_culture`, `miaphysite` ve `aramaic_language` artık ÖLÜ işaretli; bu üç delta oyuna girmiyor. `gothic_language`, `alan_paganism` ve `hellenism_religion` YAŞIYOR; `haixi/hurga` tek tanımlı; `yearly_country_pulse` on_action istisnası.

## Dil, kültür, din ve grup çakışmaları (tam liste)

| DB | Anahtar | Kazanan | Kaybeden | Sonuç |
|---|---|---|---|---|
| `common/languages` | `aramaic_language` | `common/languages/00_crescent.txt` (vanilla) | `common/languages/00_et_mesopotamian.txt` (mod, farklı) | ÖLÜ (vanilla kazandı) |
| `common/languages` | `gothic_language` | `common/languages/00_et_germany.txt` (mod) | `common/languages/00_germany.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |
| `common/cultures` | `coptic_culture` | `common/cultures/egypt.txt` (vanilla) | `common/cultures/et_egypt.txt` (mod, farklı) | ÖLÜ (vanilla kazandı) |
| `common/religions` | `alan_paganism` | `common/religions/et_caucasus.txt` (mod) | `common/religions/folk_european.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |
| `common/religions` | `hellenism_religion` | `common/religions/et_roman.txt` (mod) | `common/religions/folk_european.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |
| `common/religions` | `miaphysite` | `common/religions/christian.txt` (vanilla) | `common/religions/et_christianity.txt` (mod, farklı) | ÖLÜ (vanilla kazandı) |

## Setup: ölü kalan mod tanımları (vanilla kazandı)

174 anahtarda mod tanımı yüklenmiyor. Aşağıda kaybeden mod dosyasına göre gruplanmıştır; parantez içi kazanan vanilla dosyasıdır. `*` işaretli satırlarda kaybedilen tanım kazananla **birebir aynı** (zararsız), işaretsizlerde içerik farklı (gerçek delta kaybı).

- **`setup/countries/et_countries.txt`** — 174 kayıp: ACH (`balkans.txt`), ACO (`aridoamerica.txt`), AGW (`canadian.txt`), AHI (`anatolia.txt`), ALB (`balkans.txt`), ANL (`central_north_america.txt`), ANZ (`arabia.txt`), APA (`eastcoast.txt`), ARD (`crescent.txt`), ARN (`canadian.txt`), ATG (`canadian.txt`), ATH (`balkans.txt`), ATK (`east_africa.txt`), ATM (`east_africa.txt`), AVA (`brasil.txt`), AYD (`anatolia.txt`), BAA (`east_africa.txt`), BDK (`eastcoast.txt`), BHT (`anatolia.txt`), BIT (`anatolia.txt`), BJA (`_scandinavia.txt`), BNY (`east_africa.txt`), BOI (`east_africa.txt`), BOS (`balkans.txt`), BSG (`east_africa.txt`), BTS (`east_africa.txt`), BUG (`east_africa.txt`), BUL (`balkans.txt`), BUU (`east_africa.txt`), BYZ (`balkans.txt`), CAD (`aridoamerica.txt`), CAR (`balkans.txt`), CEP (`balkans.txt`), CFQ (`eastcoast.txt`), CHC (`eastcoast.txt`), CHK (`eastcoast.txt`), CHM (`andes.txt`), CIL (`anatolia.txt`), CLG (`eastcoast.txt`), CLI (`balkans.txt`), CND (`anatolia.txt`), COO (`eastcoast.txt`), COW (`eastcoast.txt`), CRA (`andes.txt`), CRO (`balkans.txt`), CRT (`balkans.txt`), CSQ (`central_north_america.txt`), CSU (`andes.txt`), CUA (`chaco.txt`), CYA (`andes.txt`), CYP (`anatolia.txt`), DAN (`_scandinavia.txt`), DNE (`aridoamerica.txt`), DUL (`anatolia.txt`), DWS (`arabia.txt`), EPI (`balkans.txt`), ERE (`anatolia.txt`), ERI (`eastcoast.txt`), FDL (`crescent.txt`), FIN (`_scandinavia.txt`), FZA (`egypt.txt`), GRL (`_scandinavia.txt`), GRM (`anatolia.txt`), HAT (`eastcoast.txt`), HHK (`aridoamerica.txt`), HMD (`anatolia.txt`), HSN (`anatolia.txt`), HUN (`carpathia.txt`), ICE (`_scandinavia.txt`), ICM (`andes.txt`), ISL (`aridoamerica.txt`), JAL (`crescent.txt`), JOA (`eastcoast.txt`), KAR (`anatolia.txt`), KER (`aridoamerica.txt`), KIA (`central_north_america.txt`), KIT (`east_africa.txt`), KKA (`eastcoast.txt`), KNI (`balkans.txt`), KOJ (`crescent.txt`), KPK (`eastcoast.txt`), KRL (`baltics.txt`), KRW (`east_africa.txt`), KSK (`eastcoast.txt`), KSP (`central_north_america.txt`), KTK (`central_north_america.txt`), KUR (`baltics.txt`), KVE (`_scandinavia.txt`), LAT (`balkans.txt`), LDU (`east_africa.txt`), LIT (`baltics.txt`), LIV (`baltics.txt`), MAM (`egypt.txt`), MBA (`east_africa.txt`), MCG (`eastcoast.txt`), MCN (`eastcoast.txt`), MDA (`arabia.txt`), MEN (`anatolia.txt`), MIK (`central_north_america.txt`), MIR (`east_africa.txt`), MKU (`east_africa.txt`), MLI (`east_africa.txt`), MLS (`canadian.txt`), MNB (`east_africa.txt`), MPC (`chaco.txt`), MRA (`east_africa.txt`), MSC (`eastcoast.txt`), MSG (`canadian.txt`), MSK (`eastcoast.txt`), NAX (`balkans.txt`), NCZ (`eastcoast.txt`), NEO (`balkans.txt`), NKO (`east_africa.txt`), NOR (`_scandinavia.txt`), NST (`central_north_america.txt`), OCT (`eastcoast.txt`), ODW (`canadian.txt`), OHK (`aridoamerica.txt`), OJI (`canadian.txt`), OMA (`arabia.txt`), ONN (`eastcoast.txt`), ONO (`eastcoast.txt`), ONY (`eastcoast.txt`), OSG (`canadian.txt`), PCH (`central_north_america.txt`), PCJ (`andes.txt`), PEO (`eastcoast.txt`), PIM (`aridoamerica.txt`), PQT (`eastcoast.txt`), PTE (`east_africa.txt`), QTO (`andes.txt`), QUZ (`eastcoast.txt`), RAG (`balkans.txt`), RIG (`baltics.txt`), RWA (`east_africa.txt`), SEN (`east_africa.txt`), SER (`balkans.txt`), SFA (`east_africa.txt`), SKA (`east_africa.txt`), SMI (`_scandinavia.txt`), STD (`canadian.txt`), SWE (`_scandinavia.txt`), TAI (`colombia.txt`), TAV (`_scandinavia.txt`), TBK (`east_africa.txt`), TEK (`anatolia.txt`), TEU (`baltics.txt`), THE (`balkans.txt`), TIO (`canadian.txt`), TPA (`brasil.txt`), TPQ (`brasil.txt`), TRA (`carpathia.txt`), TRE (`anatolia.txt`), TRP (`egypt.txt`), TRT (`canadian.txt`), TST (`aridoamerica.txt`), TUR (`anatolia.txt`), UBH (`east_africa.txt`), UNA (`eastcoast.txt`), WAL (`carpathia.txt`), WAN (`andes.txt`), WMG (`eastcoast.txt`), WRO (`eastcoast.txt`), WZZ (`eastcoast.txt`), YAK (`east_africa.txt`), YAQ (`aridoamerica.txt`), YAS (`arabia.txt`), YEM (`arabia.txt`), YMS (`eastcoast.txt`), ZAN (`east_africa.txt`), ZIP (`colombia.txt`), ZMW (`east_africa.txt`), ZNI (`aridoamerica.txt`), ZZB (`east_africa.txt`)

## Setup: mod-içi çakışmalar

235 anahtarda modun iki dosyası aynı anahtarı tanımlıyor; erken sıralanan kazanıyor, içerik modda kalıyor. `*` = kaybedilen tanım kazananla birebir aynı; işaretsizlerde iki mod dosyası **farklı değer** taşıyor (tekilleştirme gerekir).

- **`setup/countries/et_countries.txt`** — 103 anahtar, 103 tanesi farklı değerli: AHO (`bengal.txt`), AKM (`east_asia.txt`), AKT (`east_asia.txt`), ALN (`caucasus.txt`), AMD (`east_asia.txt`), ANU (`east_asia.txt`), ARM (`caucasus.txt`), ASA (`east_asia.txt`), AVR (`caucasus.txt`), BZU (`east_asia.txt`), CBA (`east_asia.txt`), CDL (`east_asia.txt`), CET (`british_isles.txt`), CHE (`east_asia.txt`), CHG (`east_asia.txt`), CHH (`east_asia.txt`), CHI (`east_asia.txt`), CIR (`caucasus.txt`), CNN (`british_isles.txt`), CRN (`british_isles.txt`), CSH (`east_asia.txt`), CSK (`east_asia.txt`), CXI (`east_asia.txt`), DDI (`east_asia.txt`), DGL (`bengal.txt`), DMS (`british_isles.txt`), DRG (`east_asia.txt`), DTE (`east_asia.txt`), DTI (`bengal.txt`), ENG (`british_isles.txt`), FLY (`british_isles.txt`), GEO (`caucasus.txt`), GUG (`east_asia.txt`), GWL (`bengal.txt`), HSK (`east_asia.txt`), HTK (`east_asia.txt`), IKE (`east_asia.txt`), IME (`caucasus.txt`), IMG (`east_asia.txt`), ISK (`east_asia.txt`), ITO (`east_asia.txt`), JAP (`east_asia.txt`), JNT (`bengal.txt`), KCN (`caucasus.txt`), KHS (`bengal.txt`), KID (`british_isles.txt`), KKC (`east_asia.txt`), KMA (`bengal.txt`), KMN (`bengal.txt`), KOR (`east_asia.txt`), KTB (`east_asia.txt`), KTU (`bengal.txt`), LEI (`british_isles.txt`), LJG (`east_asia.txt`), LOI (`british_isles.txt`), LTN (`east_asia.txt`), LUR (`bengal.txt`), LWA (`bengal.txt`), MCM (`british_isles.txt`), MIO (`east_asia.txt`), MMA (`east_asia.txt`), MMI (`east_asia.txt`), MNG (`east_asia.txt`), MNN (`british_isles.txt`), MRI (`east_asia.txt`), MTH (`british_isles.txt`), NIT (`east_asia.txt`), NOL (`british_isles.txt`), NVK (`east_asia.txt`), ODA (`east_asia.txt`), OGS (`east_asia.txt`), OIR (`east_asia.txt`), ORD (`british_isles.txt`), ORQ (`east_asia.txt`), OTM (`east_asia.txt`), OUC (`east_asia.txt`), SBA (`east_asia.txt`), SCO (`british_isles.txt`), SHI (`east_asia.txt`), SIB (`east_asia.txt`), SKK (`east_asia.txt`), SLN (`british_isles.txt`), SME (`caucasus.txt`), SMZ (`east_asia.txt`), SOU (`east_asia.txt`), STK (`east_asia.txt`), SZH (`east_asia.txt`), THO (`british_isles.txt`), TIB (`east_asia.txt`), TIM (`east_asia.txt`), TKD (`east_asia.txt`), TKI (`east_asia.txt`), TMN (`east_asia.txt`), TRY (`british_isles.txt`), TYR (`british_isles.txt`), UES (`east_asia.txt`), ULS (`british_isles.txt`), UTN (`east_asia.txt`), WLS (`british_isles.txt`), WUU (`east_asia.txt`), YMN (`east_asia.txt`), YMT (`east_asia.txt`), YUA (`east_asia.txt`)
- **`setup/countries/france.txt`** — 26 anahtar, 26 tanesi farklı değerli: ALE (`et_countries.txt`), ALS (`et_countries.txt`), AMG (`et_countries.txt`), ANJ (`et_countries.txt`), AQN (`et_countries.txt`), AUV (`et_countries.txt`), BAR (`et_countries.txt`), BER (`et_countries.txt`), BOU (`et_countries.txt`), BRI (`et_countries.txt`), BUR (`et_countries.txt`), CHP (`et_countries.txt`), DAU (`et_countries.txt`), FOI (`et_countries.txt`), FRA (`et_countries.txt`), GNV (`et_countries.txt`), GUY (`et_countries.txt`), LOR (`et_countries.txt`), MIE (`et_countries.txt`), NEV (`et_countries.txt`), NRM (`et_countries.txt`), ORL (`et_countries.txt`), PIC (`et_countries.txt`), PRO (`et_countries.txt`), SAV (`et_countries.txt`), TOU (`et_countries.txt`)
- **`setup/countries/horn_of_africa.txt`** — 23 anahtar, 23 tanesi farklı değerli: ABW (`et_countries.txt`), ADA (`et_countries.txt`), AFA (`et_countries.txt`), AJU (`et_countries.txt`), ALO (`et_countries.txt`), BTI (`et_countries.txt`), DAJ (`et_countries.txt`), DAM (`et_countries.txt`), DAW (`et_countries.txt`), DHK (`et_countries.txt`), ENN (`et_countries.txt`), ETH (`et_countries.txt`), GJJ (`et_countries.txt`), GLE (`et_countries.txt`), HDY (`et_countries.txt`), HRL (`et_countries.txt`), IFA (`et_countries.txt`), JRN (`et_countries.txt`), MAK (`et_countries.txt`), MDI (`et_countries.txt`), MED (`et_countries.txt`), SOA (`et_countries.txt`), WAR (`et_countries.txt`)
- **`setup/countries/india.txt`** — 31 anahtar, 31 tanesi farklı değerli: BGK (`et_countries.txt`), BND (`et_countries.txt`), BST (`et_countries.txt`), CHD (`et_countries.txt`), DHU (`et_countries.txt`), DLH (`et_countries.txt`), GLI (`et_countries.txt`), GWA (`et_countries.txt`), HAD (`et_countries.txt`), HSL (`et_countries.txt`), IDR (`et_countries.txt`), JFN (`et_countries.txt`), JLW (`et_countries.txt`), JNG (`et_countries.txt`), JSL (`et_countries.txt`), KGR (`et_countries.txt`), KJA (`et_countries.txt`), KLH (`et_countries.txt`), KSH (`et_countries.txt`), MEW (`et_countries.txt`), MRW (`et_countries.txt`), ORI (`et_countries.txt`), PLT (`et_countries.txt`), PTN (`et_countries.txt`), RDY (`et_countries.txt`), RJI (`et_countries.txt`), RTP (`et_countries.txt`), SND (`et_countries.txt`), TNK (`et_countries.txt`), VIJ (`et_countries.txt`), VND (`et_countries.txt`)
- **`setup/countries/lowlands.txt`** — 10 anahtar, 10 tanesi farklı değerli: BRB (`et_countries.txt`), FLA (`et_countries.txt`), FRI (`et_countries.txt`), HAI (`et_countries.txt`), HOL (`et_countries.txt`), LIE (`et_countries.txt`), LIM (`et_countries.txt`), LUX (`et_countries.txt`), NAM (`et_countries.txt`), UTR (`et_countries.txt`)
- **`setup/countries/maghreb.txt`** — 14 anahtar, 14 tanesi farklı değerli: ALG (`et_countries.txt`), DJE (`et_countries.txt`), FEZ (`et_countries.txt`), GBS (`et_countries.txt`), MOR (`et_countries.txt`), MRK (`et_countries.txt`), MZB (`et_countries.txt`), SLE (`et_countries.txt`), SOS (`et_countries.txt`), TET (`et_countries.txt`), TFL (`et_countries.txt`), TGT (`et_countries.txt`), TLE (`et_countries.txt`), TUN (`et_countries.txt`)
- **`setup/countries/south_east_asia.txt`** — 28 anahtar, 28 tanesi farklı değerli: ARK (`et_countries.txt`), BPR (`et_countries.txt`), BVK (`et_countries.txt`), DAI (`et_countries.txt`), HSE (`et_countries.txt`), HSI (`et_countries.txt`), KAL (`et_countries.txt`), KED (`et_countries.txt`), KHM (`et_countries.txt`), KTG (`et_countries.txt`), KUY (`et_countries.txt`), LAV (`et_countries.txt`), LGK (`et_countries.txt`), LIG (`et_countries.txt`), LNA (`et_countries.txt`), MKA (`et_countries.txt`), MLB (`et_countries.txt`), MNI (`et_countries.txt`), MYA (`et_countries.txt`), PAH (`et_countries.txt`), PEG (`et_countries.txt`), PHY (`et_countries.txt`), SAG (`et_countries.txt`), SNG (`et_countries.txt`), SUK (`et_countries.txt`), TNG (`et_countries.txt`), VTN (`et_countries.txt`), WAS (`et_countries.txt`)

## Setup: mod lehine sonuçlanan çakışmalar (özet)

254 anahtarda mod tanımı kazanıyor; kaybeden taraf çoğunlukla alfabetik olarak sonra gelen vanilla bölge dosyası. Tam liste gerekmiyorsa bu tablo yeterli; ayrıntı için script'in `--out` çıktısı yeniden üretilebilir.

| Kaybeden vanilla dosyası | Anahtar |
|---|---|
| `setup/countries/north_germany.txt` | 38 |
| `setup/countries/south_germany.txt` | 32 |
| `setup/countries/west_africa.txt` | 32 |
| `setup/countries/italy.txt` | 30 |
| `setup/countries/indonesia.txt` | 26 |
| `setup/countries/mesoamerica.txt` | 26 |
| `setup/countries/russia.txt` | 14 |
| `setup/countries/persia.txt` | 13 |
| `setup/countries/polynesia.txt` | 12 |
| `setup/countries/poland.txt` | 11 |
| `setup/countries/iberia.txt` | 10 |
| `setup/countries/steppes.txt` | 4 |
| `setup/countries/kongo.txt` | 4 |
| `setup/countries/siberia.txt` | 1 |
| `setup/countries/south_africa.txt` | 1 |

## Kasıtlı aynı-yol override dosyaları

Bu dosyalar vanilla ile aynı göreli yola sahip olduğu için vanilla kopyası yüklenmez; gölge karşılaştırmasına dahil edilmedi.

- `common/languages`: `00_great_britain.txt`, `00_mongolia.txt`
- `common/cultures`: `baltic.txt`, `british.txt`, `east_asia.txt`, `greek.txt`, `netherlands.txt`
- `setup/countries`: `bengal.txt`, `british_isles.txt`, `caucasus.txt`, `east_asia.txt`, `france.txt`, `horn_of_africa.txt`, `india.txt`, `lowlands.txt`, `maghreb.txt`, `south_east_asia.txt`

## on_action özel durumu

`common/on_action` diğer DB'ler gibi ilk-tanım-kazanır kuralına tabi değil: mod, mevcut bir vanilla on action'a yalnızca `on_actions` bloğu ekleyebiliyor (mod dosyasındaki not ve EU5 wiki kuralı). 18 Ekim log'unda `yearly_country_pulse` için hiç `Duplicated key` satırı yok; bu da blok birleşimini doğruluyor.

- Vanilla: `common/on_action/country_yearly.txt`
- Mod: `common/on_action/et_history_pulses.txt` — `yearly_country_pulse` bloğu + yeni `et_egypt_yearly_pulse`

## Doğrulama: 18 Ekim log'undaki dört satır

```
Duplicated key aramaic_language will not be created from file: common/languages/00_et_mesopotamian.txt:26
Duplicated key gothic_language will not be created from file: common/languages/00_germany.txt:676
Duplicated key coptic_culture will not be created from file: common/cultures/et_egypt.txt:48
Duplicated key miaphysite will not be created from file: common/religions/et_christianity.txt:108
```

Raporun dört anahtar için bulduğu kazanan/kaybeden eşleşmesi bu satırlarla birebir uyuşuyor. Log satırları hata değil, bilgi düzeyindedir; Test B raporunda bu sınıf bilgi olarak kalmalı.

## Sınırlar

- Anahtar karşılaştırması üst düzey bloklarla sınırlıdır; iç içe alan çakışmaları ve sözdizimi hataları kapsam dışıdır.
- Dosya sırası göreli yolun bayt sırasına göre modellendi; oyunun kullandığı sıralama büyük/küçük harf duyarsızsa istisna çıkabilir (mevcut dosya adları küçük harf).
- İçerik karşılaştırması yorumları ve boşlukları yok sayar; anlamsal eşdeğerliği değil birebir gövde eşitliğini ölçer.

## Sonraki adım

Ölü tanımlar için üç yol var: (1) tanımı rakipten önce sıralanacak bir dosyaya taşımak, (2) vanilla dosyasıyla aynı adlı tam override kullanmak, (3) deltayı silip vanilla davranışını kabul etmek. Karar verilmeden veri değiştirilmemeli; Test B log'u bu satırları bilgi sınıfında beklemeli.
