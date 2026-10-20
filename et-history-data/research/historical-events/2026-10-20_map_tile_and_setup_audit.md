# Harita Karosu, Şehir Setup ve Başkent Eşleme Denetimi — 20 Ekim 2026

58 CE şehir batch'inin (74 kayıt) ve Abbasi başkentlerinin oyun verisiyle
denetimi: karo (tile) eşlemesi, `town_setup` değerleri ve başkent konum
anahtarları. Hepsi çevrimdışı, kurulu EU5 1.3.x harita ve kurulum verisine
karşı doğrulandı.

## 1. Karo (tile) eşlemeleri

| Yer | Karo | Kesinlik |
|---|---|---|
| Rodos | `rodos` (rodos_province) | birebir — karo adı yerin adı |
| Pataliputra (Paithan) | `patna` (patna_province) | birebir — antik Pataliputra bugünkü Patna |
| Memfis | karşılığı yok | yaklaşık: `damanhur` (Delta batı kıyısı, ~40 km) |
| Berenike (Kızıl Deniz) | karşılığı yok | yaklaşık: `suakin` (çok daha güneyde, kaba) |
| İstahr (Istakhr) | karşılığı yok | yaklaşık: `isfahan` (~40 km kuzeybatı) |
| Yangzhou / Guangling | `yangzhou` (Shaanxi) ve `guangling` (Shanxi) **homonym** | eşleşme yok: aynı adlı karolar başka eyaletlerde; aşağı Yangtze `wuxian` (Wu/Suzhou) ile temsil ediliyor |

Homonym denetimi: `changan` (Guangxi köyü) ile `jingzhao` (Han başkenti)
karışması 17 Ekim'de düzeltildi ve kayıt notuna geçti. Kalan homonymler
`yangzhou_shaanxi_province` ve `yuzhou_shanxi_province`; karo yeniden adlandırma
ertelendi (görev kabulü), mesafeler kayıt notlarında belgelendi.

Önceden yaklaşık işaretlenen ve kayıt notunda duran karolar: Petra → `maan`,
Artaxata → `yerevan`, Taxila → `rawalpindi`, Kyrene → `al_bayda`, Chang'an →
`jingzhao`, Linzi → `yidu_qingzhou`, Kartaca → `tunis`, Korkai →
`thoothukudi`, Muziris → `kodungallur`. Bunlar 58 CE batch'inin notlarında
ayrı ayrı geçiyor; bu denetimde yeni bir yaklaşık bulunmadı.

## 2. `town_setup` değerleri

- Vanilla `main_menu/setup/start/07_cities_and_buildings.txt`: 1.019 şehir,
  114 farklı `town_setup` değeri.
- Modun 58 CE şehir dosyası: 140 şehir, 38 farklı değer — **38'in 38'i
  vanilla'da tanımlı** (uydurma setup id yok).
- 74 kaydın araştırma hedefleri (`locations/...` dosyaları) 58.2.1 bloğunda
  `city: {rank: ...}` ve `market: yes` taşıyor; `town_setup` id oyun tarafında
  (şehir dosyası, açıklama yorumuyla) duruyor.

Sonuç: araştırma katmanına ayrı bir `setup` alanı eklemek gerekmiyor —
oyun tarafındaki 58 CE setup'ları doğrulanmış vanilla değerler.

## 3. Abbasi başkentleri

- `baghdad` (baghdad_province) ve `samarra` (samarra_province) gerçek karolar.
- Ülke dosyası (`countries/ABBA - Abbasid.yml`) şu anahtarları taşıyordu:
  762.7.30 `baghdad`, 796.1.1 `raqqa`, 809.1.1 `baghdad`, 836.1.1 **`tikrit`**,
  892.1.1 `baghdad`.
- **Bulgu:** 836–892 Abbasi başkenti (Samarra), aynı eyaletteki farklı bir
  yerleşim (`tikrit`) ile temsil ediliyordu; anahtar `samarra` olarak
  düzeltildi.
- 762'nin günü (30 Temmuz) EU4 aktarımından geliyor; kayıt yıl hassasiyetini
  koruyor ve notta belirtildi.
- 58 CE'de `baghdad` karosu Seleucia-Ctesiphon okumasını taşıyor; 762
  kuruluşu önceki yerleşimleri silmiyor (kayıt notuna işlendi).

Uygulama etkisi: değişen veri yalnızca araştırma katmanındaki ülke
dosyasıdır; modun 58 CE kurulumunda ABBA bloğu başkentsizdir (58 CE'de Abbasi
devleti yok), bu yüzden oyun tarafında değişiklik yoktur.

## 4. Kalan iş

- Berenike ve Memfis için yaklaşık karo seçimi, bu iki yer 58 CE şehir
  batch'ine girmiyorsa gerekmiyor; girerse not yaklaşıklığıyla birlikte
  yazılmalı.
- Karo yeniden adlandırmaları (Yangzhou/Guangling homonymleri) ertelendi.
