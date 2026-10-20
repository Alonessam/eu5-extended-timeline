# Vanilla Anahtar Gölge Denetimi (WS3) — 19 Ekim 2026

`vanilla_key_shadow_review` maddesinin kapanış kaydıdır: `et_` önekli eklemeli
mod dosyalarının vanilla'da zaten tanımlı anahtarları yeniden tanımlayıp
tanımlamadığı ve her yeniden tanımın vanilla içeriğini koruyup korumadığı
denetlendi. Yöntem, kalan kayıtlar ve uygulanan düzeltmeler bu dosyadadır.
Kalıcı tarama: `et-history-data/scripts/script-token-audit.py`.

> **Düzeltme (20 Ekim 2026):** Bu denetim tanımları statik olarak karşılaştırdı;
> hangi kopyanın oyuna yüklendiğini doğrulamıyordu. Geçerli kural: aynı DB
> içinde göreli dosya yolu alfabetik sırasında **önce gelen** tanım kazanır,
> sonraki tanım oluşturulmaz; aynı adlı mod dosyası vanilla'yı birebir
> değiştirir. Yükleme sırasını uygulayan offline denetim
> (`scripts/shadow-audit.py`; rapor
> `2026-10-20_vanilla_shadow_report.md`) dokuz kayıttan üçünün **ölü** olduğunu
> gösterdi: `coptic_culture`, `miaphysite`, `aramaic_language`; bu deltalar
> oyuna hiç girmiyordu. **Aynı gün uygulanan taşıma:** üç delta bloğu
> rakibinden önce sıralanan dosyalara taşındı (`00_et_egypt.txt`,
> `00_et_christianity.txt`, `00_aramaic.txt`) ve rapor yeniden üretildiğinde
> üçü de YAŞIYOR. Aşağıdaki tablonun karar sütunları taşıma sonrası durumu
> gösterir. Aynı kural `setup/countries` için de geçerliydi:
> `et_countries.txt` 174 tanımda vanilla'ya, 103 tanımda erken sıralanan
> aynı-yol override'a yeniliyordu; 132 override tanımı da `et_countries`'e
> kaybediyordu. **20 Ekim ikinci düzeltme:** `et_countries.txt` →
> `00_et_countries.txt` (tek otorite) ve 10 aynı-yol bölge override'ı silindi;
> ayrıntı `2026-10-20_setup_authority_report.md`. Setup artık 0 ölü /
> 0 mod-içi çakışma gösteriyor.

## Yöntem

- Kapsam: `Extended Timeline/in_game` ve `main_menu` altındaki tüm `.txt`
  dosyaları (denetimde 108 hedef) ve eklemeli dosya gölge taraması (48
  eklemeli dosya).
- Dışlama: vanilla ile aynı adlı 7 dosya (`cultures/baltic.txt`,
  `cultures/british.txt`, `cultures/east_asia.txt`, `cultures/greek.txt`,
  `cultures/netherlands.txt`, `languages/00_great_britain.txt`,
  `languages/00_mongolia.txt`) kasıtlı tam override kabul edildi; gölge
  taraması yalnızca eklemeli dosyalarla sınırlandı.
- Ad alanı: anahtarlar yalnızca aynı `common` alt dizininde karşılaştırıldı.
  Örnek yanlış pozitif: `oracle` dini (`common/religions`) ile `oracle` bina
  anahtarı (`common/building_types`) farklı ad alanlarıdır.
- Ölçüt: kalan her yeniden tanım ya "vanilla kopyası + belgelenmiş delta"
  olarak korunur ya da kaldırılıp vanilla tanımının yüklenmesi sağlanır.

## Kalan yeniden tanımlar (9) ve delta'ları

| Anahtar | Mod dosyası | Karar | Delta / gerekçe |
|---|---|---|---|
| `coptic_culture` | `cultures/00_et_egypt.txt` | YAŞIYOR (20 Ekim taşındı) | `culture_groups = { arabic_group }` eklendi; ardıl Mısır kimlikleriyle aynı hat (UPDATE 3) — `et_egypt.txt`'ten taşındı, artık mod kazanıyor |
| `haixi_culture` | `cultures/et_1_3_east_asia.txt` | Korundu (tek tanım) | Vanilla 1.3 tanımının birebir kopyası; aynı adlı `east_asia.txt` override'ı gizlediği için geri yüklendi |
| `hurga_culture` | `cultures/et_1_3_east_asia.txt` | Korundu (tek tanım) | Aynı gerekçe; birebir kopya |
| `aramaic_language` | `languages/00_aramaic.txt` | YAŞIYOR (20 Ekim taşındı) | Vanilla gövde + `# ET ancient Aramaic (58 CE)` isimleri; eksik `color`, `family`, `dynasty_names`, `lowborn` geri geldi — `00_et_mesopotamian.txt`'ten taşındı, artık mod kazanıyor |
| `gothic_language` | `languages/00_et_germany.txt` | YAŞIYOR (doğrulandı) | Vanilla gövde + özel `color = rgb{ 20 100 154 }`; `fallback = german_language` geri geldi; boş isim listeleri kaldırıldı |
| `yearly_country_pulse` | `on_action/et_history_pulses.txt` | Korundu (on_action istisnası) | Vanilla `yearly_country_pulse` on action'ına eklenen `on_actions = { et_egypt_yearly_pulse }` bloğu; vanilla kuralı (mod mevcut bir on action'a yalnızca blok ekleyebilir) dosya içinde not edilmiş |
| `alan_paganism` | `religions/et_caucasus.txt` | YAŞIYOR (doğrulandı) | `group = folk_caucasian_group` (artık tanımlı); `army_cavalry_power` → `army_light_cavalry_power` düzeltmesi |
| `hellenism_religion` | `religions/et_roman.txt` | YAŞIYOR (doğrulandı) | `enable = 9999.1.1` yok; 58 CE başlangıcında Helenizm'in açık olması bilinçli |
| `miaphysite` | `religions/00_et_christianity.txt` | YAŞIYOR (20 Ekim taşındı) | `language = coptic_language` eklendi (UPDATE 3) — `et_christianity.txt`'ten taşındı, artık mod kazanıyor |

Kaldırılan ve yeniden adlandırılanlar:

| Anahtar | Mod dosyası | Karar | Gerekçe |
|---|---|---|---|
| `french_group` | `culture_groups/et_culture_groups.txt` | Kaldırıldı | Vanilla'da zaten tanımlı boş grubun birebir yinelenmesi; mod tanımı silindi |
| `burgundian` | `cultures/et_german.txt` | Yeniden adlandırıldı | `burgundii` oldu: antik Cermen kavmi. Vanilla Fransız `burgundian` yeniden yükleniyor; `et_culture.108` artık `culture:burgundii` kullanıyor; EN/TR loc eklendi (in_game + main_menu) |

`burgundian` için mod kurulum referansları (`00_et_countries.txt`: BAR/LOR/NEV,
`france.txt`: AUX/NEV/TON) ortaçağ Fransız ülkeleridir ve artık vanilla
tanımına çözülür — 58 CE kurulumunda bu etiketler yok.

## Aynı taramada düzeltilen komşu kusurlar

- `folk_caucasian_group` üç dinde referans ediliyordu (`georgian_religion`,
  `armenian_religion`, `alan_paganism`) ama hiçbir yerde tanımlı değildi;
  `religion_groups/et_religion_groups.txt`'e `folk_mesopotamian_group`
  deseniyle eklendi (`color = rgb {120 150 90}`, `convert_slaves_at_start`,
  `allow_rgo_slave_demand`). EN/TR adları `et_religion_l_*.yml` dosyalarına
  işlendi (her iki ağaçta).
- `army_cavalry_power` vanilla'da yok: `et_caucasus.txt` ve `et_uralic.txt`
  `army_light_cavalry_power` oldu (geçerli çift: `army_light_cavalry_power` /
  `army_heavy_cavalry_power`).
- `global_build_buildings_cost` vanilla'da yok: `et_christianity.txt`'teki 4
  din (chalcedonism, arianism, presbyterian, anabaptist)
  `global_build_buildings_efficiency = 0.05` oldu (maliyet −%5 → verim +%5).
- `trade_efficiency` vanilla'da yok: `et_egyptian.txt` (2) ve
  `et_folk_european.txt` (1) `selling_efficiency` oldu — vanilla dinler
  `small_trade_efficiency_bonus` adlı değeri bu anahtarla kullanıyor
  (ör. `folk_european.txt`, `zoroastrian.txt`).
- `berber` kültürünün `berber_group` grubu tanımsızdı; vanilla
  `eastern_amazigh` deseniyle `amazigh_group maghrebi_group` oldu.
- `et_uralic.txt` satır 2'deki ikinci BOM (dosya başındaki gerçek BOM'un
  ardından gelen boş satırda) kaldırıldı; BOM sayısı 2 → 1.

## Doğrulama

- Kalıcı denetim genişletildi: din grubu, kültür grubu ve
  `definition_modifier` anahtarları artık taranıyor. Geçerli modifier kümesi
  `main_menu/common/modifier_type_definitions` (2436), ikon tanımları ve
  vanilla `definition_modifier` kullanımlarının birleşimidir (2453).
- Tam tarama: 108 dosya, 0 çözülemeyen token (2267 kültür, 480 din, 214
  kültür grubu, 32 din grubu).
- Tüm düzenlenen dosyalar BOM + CRLF düzenini koruyor; `et_uralic.txt`
  BOM sayısı 1, `et_culture_groups.txt` ve `et_religion_groups.txt` yeni
  sonlarında da bu düzeni sürdürüyor.
- Gölge taraması: 48 eklemeli dosya; yukarıdaki 9 kayıt dışında anahtar
  kesişmesi yok.
- Yükleme sırası denetimi (20 Ekim 2026): `scripts/shadow-audit.py` dil,
  kültür, din, gruplar, dil aileleri ve `setup/countries` DB'lerini kapsayacak
  şekilde yazıldı; rapor `2026-10-20_vanilla_shadow_report.md`. Üç yeniden
  tanım ölü çıktı; aynı gün `00_et_egypt.txt`, `00_et_christianity.txt` ve
  `00_aramaic.txt` dosyalarına taşınarak düzeltildi (rapor taşıma sonrası:
  dil/kültür/dinde ölü 0). `haixi/hurga` tek tanım olduğu için yükleniyor;
  `yearly_country_pulse` on_action blok birleşimi istisnası (log'da çakışma
  satırı yok).

## Sınırlar

- Gölge taraması eklemeli `.txt` dosyalarındaki üst düzey anahtarları
  karşılaştırır; gövde farkları yalnızca işaretlenen kayıtlar için elle
  incelendi. Aynı adlı override dosyalar kapsam dışıdır (kasıtlı tam
  override kabul edildi).
- Denetim, loc anahtarlarını taramaz; `burgundii` ve din grubu adları için
  eklenen EN/TR kayıtları elle doğrulandı.
- `vandalic_language` (`00_et_germany.txt`) gölge kapsamı dışında yeni bir
  anahtardır; isim listeleri `#TODO` ve `fallback` alanı yok. Bu turda
  dokunulmadı; ayrı bir dil-verisi turu gerektirir (`gothic_language` için
  eklenen `fallback = german_language` deseni örnek alınabilir).
