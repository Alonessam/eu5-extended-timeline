# Kapsam Bağlantısı Düzeltmesi — 20 Ekim 2026

18 Ekim Test B tabanındaki 103 `Invalid scope types ... link: location`
satırının kök nedeni: olay dosyasındaki konum karşılaştırmaları
`location = location:X` biçimindeydi. Bu biçimde sol taraf `location` kapsam
bağlantısıdır; olay hedefi karşılaştırması için geçerli değildir. Vanilla
biçim `this = location:X`. UPDATE 19 (`a718859`, 19 Ekim 2026) 103 satırın
tamamını `this = location:X` yaptı; başka bir olay sözdizimi değişikliği
gerekmedi.

## Kanıt

- Taban log: `et-history-data/tests/2026-10-19_2329_18oct_baseline/after/debug.log`.
  103 `Invalid scope types ... link: location` satırı; ilk 10161, son 10277;
  kaynak satırları 702-2086.
- Taban logun 103 kaynak satırı `a718859^` dosyasıyla karşılaştırıldı:
  103/103 satır `location = location:X`; 0 istisna.
- `git show a718859 -- Extended Timeline/in_game/events/et_culture_events.txt`
  tam olarak 103 `location = location:X` silmesi ve 103 `this = location:X`
  eklemesi gösterir (206 değişen satır). Taban logun 103 hatası bu 103 eski
  bağlantıya bire bir karşılık gelir.
- Aynı `this = location:` biçimi vanillada geçerlidir:
  `flavor_BUL.txt:56-67` (every_owned_location efekti) ve
  `flavor_ENG.txt:6128-6136` (custom_tooltip içindeki limit).

## Cascade hipotezi neden elendi

Taban logda ilk kapsam hatası (702), `et_culture.101`'in 673. satırındaki
`outcome = good` enum hatasının hemen ardından geliyor; bu ilk bakışta bir
parse-state cascade'i gibi görünüyordu. Ancak:

- 103 kapsam hatası, dosyadaki 103 eski `location = location:X` satırının
  tamamıdır; `git show a718859` bunu bire bir doğrular.
- Kapsam hataları yalnızca enum hatası olan olaylarda değil, `outcome =
  neutral` olan olaylarda da vardır (`.105`, `.107`, `.108`, `.111`, `.114`,
  `.117`). Enum hatası olan bazı olaylarda (`.102`, `.119`) konum listesi
  olmadığı için 0 kapsam hatası vardır.
- 13 enum hatası ayrı bir kusurdur: `outcome = good` geçersizdir; UPDATE 16
  (`9494668`) bunları `positive` yaptı. Kapsam hatasının nedeni değildir.

## Güncel durum ve doğrulama

Güncel dosyada 0 `outcome = good`, 13 `outcome = positive`, 0
`location = location:` ve 103 `this = location:` satırı var. Beklenen: bir
sonraki Test B logunda 0 kapsam hatası.

20 Ekim 13:49 ana menü smoke logu (890 KB) bu doğrulama için kullanılamaz:
log `pdx_persistent_reader` satırı içermiyor ve veritabanı yüklemesine
ulaşmadan kesiliyor. Test B kampanyası gerekli.

Kabul: Test B logunda `Invalid scope types ... et_culture_events.txt` satırı 0;
`test-b-report.py` ilgili satırı 0 gösterir. Eğer hata kalırsa kalan satırlar
tek tek incelenmelidir.
