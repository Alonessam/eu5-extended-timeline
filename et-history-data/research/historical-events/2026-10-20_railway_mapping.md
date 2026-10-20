# Demiryolu Temsili ve Hat Eşlemesi — 20 Ekim 2026

Stockton–Darlington hattının, Rocket'un ve Rainhill denemelerinin oyun
konum anahtarlarına eşlenmesi ve "açılış olayı" ile "ulusal benimseme"
arasındaki ayrım. Harita, ilerleme (advance) ve yol türü verisi kurulu EU5
1.3.x'ten doğrulandı.

## 1. Hat eşlemesi

| Öge | Konum anahtarı | Kesinlik |
|---|---|---|
| Stockton–Darlington hattının iki ucu | `stockton` ve `darlington` (durham_province) | birebir — hattın iki ucu |
| Rocket'un üretimi (Newcastle upon Tyne) | `newcastle` (northumberland_province) | birebir |
| Rainhill denemeleri | `liverpool` | yaklaşık — Rainhill'ın karşılığı yok; en yakın karo Liverpool (~15 km) |

Hattın 1825'teki açılış kesintisi Stockton ile Darlington arasındaydı; oyun
haritasında bu iki konum aynı eyalette (durham_province) yan yana durduğu için
hat, oyunun kendi yol mekaniğiyle doğrudan kurulabilir.

## 2. Oyundaki demiryolu modeli

- `common/advances/3_road_unlocks.txt`: `railroad_advance` (age_6_revolutions,
  `steel_mill_advance` gereksinimi) `railroad` yol türünü açar.
- `common/road_types/`: `railroad` yol türü, `price_per_unit_distance =
  build_railroad` ile inşa talebine bağlıdır.
- `common/building_types/` ve `common/special_construction_demands.txt`:
  `build_railroad_demand` ile demiryolu inşası bir yapı talebi olarak modellenir.

Sonuç: demiryolu oyunda bir *yol türü + ilerleme* çiftidir; tek bir olayla
"ülusal demiryolu" verilemez.

## 3. Temsil kararı

- **Açılış olayı:** 27 Eylül 1825'te yalnızca `stockton`–`darlington`
  hattının açılması. Bu, hattın iki ucunu elinde tutan devlet için tarihli bir
  ülke olayı olarak modellenebilir (konum kapısı: `owns = location:stockton`
  veya `darlington`).
- **Ulusal benimseme:** 1830'lar-1840'lar ağı, demiryolu düzenleme yasaları
  ve bölgesel yayılma ayrı kayıt gerektirir; tek bir hattın açılışından
  çıkarılamaz. Oyun zaten `railroad_advance` ilerlemesiyle bu alanı kendi
  teknoloji ağacına bırakıyor, bu yüzden mod ulusal bir demiryolu vermemeli.
- **Teknoloji iddiası:** Bir tren ve bir lokomotif, bir bölgenin demiryolu
  teknolojisine sahip olduğunu göstermez; `rocket_manufacture` ve
  `locomotion_opening_engine` kayıtları bu yüzden uygulanmış olarak işaretlenmez.

## 4. Uygulama durumu

Galya zinciri 1789-1794 (`.118`) ile 1881 (`.119`) arasını atlar; 19. yüzyıl
demiryolu çağı zincirde bir slot olmadığı için bu kayıtlar bir sonraki içerik
işine kalır. Harita eşlemesi ve temsil kararı hazırdır; olay yazımı zincir
planına bir 19. yüzyıl dilimi eklenirse yapılabilir.
