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
| `common/languages` | 53 | 11 | 2 | 2 | 0 | 2 | 0 | 0 |
| `common/cultures` | 52 | 24 | 5 | 1 | 0 | 1 | 0 | 0 |
| `common/religions` | 29 | 14 | 0 | 3 | 0 | 3 | 0 | 0 |
| `common/culture_groups` | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| `common/religion_groups` | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| `common/language_families` | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| `setup/countries` | 45 | 1 | 0 | 663 | 0 | 663 | 0 | 0 |
| **Toplam** | 182 | 53 | 7 | 669 | 0 | 669 | 0 | 0 |

## Bilinen dokuz yeniden tanım

| Anahtar | DB | Kazanan | Kaybeden | Sonuç | Not |
|---|---|---|---|---|---|
| `coptic_culture` | common/cultures | `common/cultures/00_et_egypt.txt` | `common/cultures/egypt.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |  |
| `haixi_culture` | common/cultures | — | — | çakışma yok (tek tanım) | Mod tanımı yükleniyor |
| `hurga_culture` | common/cultures | — | — | çakışma yok (tek tanım) | Mod tanımı yükleniyor |
| `aramaic_language` | common/languages | `common/languages/00_aramaic.txt` | `common/languages/00_crescent.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |  |
| `gothic_language` | common/languages | `common/languages/00_et_germany.txt` | `common/languages/00_germany.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |  |
| `alan_paganism` | common/religions | `common/religions/et_caucasus.txt` | `common/religions/folk_european.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |  |
| `hellenism_religion` | common/religions | `common/religions/et_roman.txt` | `common/religions/folk_european.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |  |
| `miaphysite` | common/religions | `common/religions/00_et_christianity.txt` | `common/religions/christian.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |  |
| `yearly_country_pulse` | on_action | — | — | ÖZEL: blok birleşimi | Aşağıdaki on_action notu |

Denetim notu 20 Ekim 2026'da düzeltildi: `coptic_culture`, `miaphysite` ve `aramaic_language` yüklemede vanilla'ya yeniliyordu. Aynı gün üç delta bloğu rakibinden önce sıralanan dosyalara taşındı (`00_et_egypt.txt`, `00_et_christianity.txt`, `00_aramaic.txt`); bu rapor taşıma sonrası üretildi ve üçü de YAŞIYOR. `gothic_language`, `alan_paganism` ve `hellenism_religion` zaten yaşıyordu; `haixi/hurga` tek tanımlı; `yearly_country_pulse` on_action istisnası.

İkinci düzeltme (aynı gün, `setup/countries`): `et_countries.txt` `00_et_countries.txt` olarak yeniden adlandırıldı ve 10 aynı-yol bölge override'ı kaldırıldı. Override'lar vanilla kopyasıydı ve yalnızca 17 etiket düzenlemesi taşıyordu; bu düzenlemelerin tamamı `et_countries` ile birebir aynıydı. Böylece 663 setup tanımının tamamı moddan yükleniyor, ölü ve mod-içi çakışma kalmadı. Ayrıntı: `2026-10-20_setup_authority_report.md`.

## Dil, kültür, din ve grup çakışmaları (tam liste)

| DB | Anahtar | Kazanan | Kaybeden | Sonuç |
|---|---|---|---|---|
| `common/languages` | `aramaic_language` | `common/languages/00_aramaic.txt` (mod) | `common/languages/00_crescent.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |
| `common/languages` | `gothic_language` | `common/languages/00_et_germany.txt` (mod) | `common/languages/00_germany.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |
| `common/cultures` | `coptic_culture` | `common/cultures/00_et_egypt.txt` (mod) | `common/cultures/egypt.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |
| `common/religions` | `alan_paganism` | `common/religions/et_caucasus.txt` (mod) | `common/religions/folk_european.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |
| `common/religions` | `hellenism_religion` | `common/religions/et_roman.txt` (mod) | `common/religions/folk_european.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |
| `common/religions` | `miaphysite` | `common/religions/00_et_christianity.txt` (mod) | `common/religions/christian.txt` (vanilla, farklı) | YAŞIYOR (mod kazandı) |

## Setup: ölü kalan mod tanımları (vanilla kazandı)

Yok — tüm mod tanımları yükleniyor. (20 Ekim: `et_countries.txt` `00_et_countries.txt` olarak yeniden adlandırıldı; 174 ölü tanım canlandı.)


## Setup: mod-içi çakışmalar

Yok — 10 aynı-yol bölge override'ı kaldırıldığından mod içi çakışma kalmadı.


## Setup: mod lehine sonuçlanan çakışmalar (özet)

663 anahtarda mod tanımı kazanıyor; kaybeden taraf her zaman alfabetik olarak sonra gelen vanilla bölge dosyası. Tam liste gerekmiyorsa bu tablo yeterli; ayrıntı için script'in `--out` çıktısı yeniden üretilebilir.

| Kaybeden vanilla dosyası | Anahtar |
|---|---|
| `setup/countries/east_asia.txt` | 63 |
| `setup/countries/north_germany.txt` | 38 |
| `setup/countries/south_germany.txt` | 32 |
| `setup/countries/west_africa.txt` | 32 |
| `setup/countries/eastcoast.txt` | 31 |
| `setup/countries/india.txt` | 31 |
| `setup/countries/italy.txt` | 30 |
| `setup/countries/east_africa.txt` | 30 |
| `setup/countries/south_east_asia.txt` | 28 |
| `setup/countries/france.txt` | 26 |
| `setup/countries/indonesia.txt` | 26 |
| `setup/countries/mesoamerica.txt` | 26 |
| `setup/countries/horn_of_africa.txt` | 23 |
| `setup/countries/british_isles.txt` | 21 |
| `setup/countries/balkans.txt` | 19 |
| `setup/countries/anatolia.txt` | 17 |
| `setup/countries/maghreb.txt` | 14 |
| `setup/countries/russia.txt` | 14 |
| `setup/countries/persia.txt` | 13 |
| `setup/countries/polynesia.txt` | 12 |
| `setup/countries/aridoamerica.txt` | 11 |
| `setup/countries/canadian.txt` | 11 |
| `setup/countries/bengal.txt` | 11 |
| `setup/countries/poland.txt` | 11 |
| `setup/countries/iberia.txt` | 10 |
| `setup/countries/_scandinavia.txt` | 10 |
| `setup/countries/lowlands.txt` | 10 |
| `setup/countries/caucasus.txt` | 8 |
| `setup/countries/central_north_america.txt` | 8 |
| `setup/countries/andes.txt` | 8 |
| `setup/countries/arabia.txt` | 6 |
| `setup/countries/baltics.txt` | 6 |
| `setup/countries/crescent.txt` | 4 |
| `setup/countries/steppes.txt` | 4 |
| `setup/countries/kongo.txt` | 4 |
| `setup/countries/brasil.txt` | 3 |
| `setup/countries/egypt.txt` | 3 |
| `setup/countries/carpathia.txt` | 3 |
| `setup/countries/chaco.txt` | 2 |
| `setup/countries/colombia.txt` | 2 |
| `setup/countries/siberia.txt` | 1 |
| `setup/countries/south_africa.txt` | 1 |

## Kasıtlı aynı-yol override dosyaları

Bu dosyalar vanilla ile aynı göreli yola sahip olduğu için vanilla kopyası yüklenmez; gölge karşılaştırmasına dahil edilmedi.

- `common/languages`: `00_great_britain.txt`, `00_mongolia.txt`
- `common/cultures`: `baltic.txt`, `british.txt`, `east_asia.txt`, `greek.txt`, `netherlands.txt`

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

Bu satırlar taşıma öncesi 18 Ekim oturumunun kanıtıdır; adı geçen dosya her satırda kaybedendir. Taşıma sonrası rapor aramaic, coptic ve miaphysite için kazananı moda çevirdi (kaybeden artık vanilla: 00_crescent.txt, egypt.txt, christian.txt); gothic_language aynı kaldı. Yeni Test B logunda bu üç satırın dosya adı değişecek, satır sayısı değişmeyecek. Log satırları hata değil, bilgi düzeyindedir; Test B raporunda bu sınıf bilgi olarak kalmalı.

## Sınırlar

- Anahtar karşılaştırması üst düzey bloklarla sınırlıdır; iç içe alan çakışmaları ve sözdizimi hataları kapsam dışıdır.
- Dosya sırası göreli yolun bayt sırasına göre modellendi; oyunun kullandığı sıralama büyük/küçük harf duyarsızsa istisna çıkabilir (mevcut dosya adları küçük harf).
- İçerik karşılaştırması yorumları ve boşlukları yok sayar; anlamsal eşdeğerliği değil birebir gövde eşitliğini ölçer.

## Sonraki adım

Dil, kültür ve din deltaları 20 Ekim'de taşıma yöntemiyle düzeltildi. `setup/countries` de aynı gün tek-otorite birleştirmesiyle düzeltildi: `et_countries.txt` → `00_et_countries.txt`, 10 yedek override silindi. Rapor artık 0 ölü ve 0 mod-içi çakışma gösteriyor. Kalan iş: Test B'nin tek oturumda çalıştırılıp `Duplicated key` satırlarının bilgi sınıfında doğrulanması ve `00_et_countries.txt` otoritesinin yeni log'da teyit edilmesi.
