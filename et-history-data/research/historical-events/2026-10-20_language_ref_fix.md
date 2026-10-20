# Dil Referansı Adreslenebilirliği ve Sınıf-1 Düzeltmesi — 20 Ekim 2026

18 Ekim Test B tabanında kalan 13 sınıf-1 `Failed to read key reference`
satırının (7 anahtar) kök nedeni ve 20 Ekim düzeltmesi. Kalıcı runtime
denetimi: `et-history-data/scripts/test-b-report.py` (sınıf-1'i artık beklenen
sıfır olarak sınıflar).

## Kök neden

EU5'te `common/languages/*.txt` içindeki bir üst dil bloğu, dolu bir
`dialects = { ... }` bloğu taşıyorsa culture/religion `language =` alanında
**adreslenemez**. Böyle bir anahtar yalnızca dil grubu düğümüdür; oyunun dil
veritabanına kaydolan adreslenebilir anahtarlar şunlardır:

- `dialects` bloğu olmayan veya boş olan düz dil anahtarları,
- bir dilin doğrudan `dialects` çocuğu olan lehçe anahtarları,
- kendi adıyla bir varsayılan lehçe taşıyan üst dil anahtarları
  (`french_language`, `greek_language` gibi).

Kanıt: vanilla 528 üst düzey dil bloğu ve 612 adreslenebilir anahtar
içeriyor; 2.087 culture `language =` referansının tamamı bu üç sınıftan
birine düşer ve hiçbiri kendi adlı lehçesi olmayan dolu bir üst dil
anahtarını göstermez. Modun kendi `gaulish_language`, `akkadian_language`
gibi dolu üst dilleri de doğrudan referans edilmez; kültürler
`gaulish_dialect`, `assyrian_dialect` gibi lehçeleri kullanır. Boş
`dialects = {}` blokları düz dil sayılır (`tocharian_language`,
`saka_language`, `pictish_language` zaten hatasız referans ediliyor).

## Düzeltilen 13 satır / 7 anahtar

| Dosya / kültür veya din | Eski | Yeni | Gerekçe |
|---|---|---|---|
| `et_french.txt` / `gallo_roman` | `latin_language` | `roman_dialect` | Latin isim havuzu; Geç Latin/Gallo-Romen için mevcut adreslenebilir lehçe |
| `et_french.txt` / `occitan` | `occitan_language` | `occitan_dialect` | Birebir lehçe |
| `et_italian.txt` / `etruscan` | `latin_language` | `roman_dialect` | Geçici: vanilla/modda Etrüsk dil verisi yok; Latin isim havuzu korunur |
| `et_italian.txt` / `roman` | `latin_language` | `roman_dialect` | Klasik Roma lehçesi |
| `et_mesopotamian.txt` / `phoenician_culture` | `phoenician_language` | `phoenician_language` | Anahtar `00_et_mesopotamian.txt` içinde kendi adlı `default = yes` lehçesiyle adreslenebilir yapıldı; Fenike isim havuzu korunur |
| `et_missing.txt` / `hubei` | `mandarin_language` | `southern_mandarin_dialect` | Hubei Güneybatı Mandarin bölgesi |
| `et_missing.txt` / `shandong_culture` | `mandarin_language` | `northern_mandarin_dialect` | Shandong kuzey Mandarin bölgesi |
| `et_missing.txt` / `xibei` | `mandarin_language` | `northern_mandarin_dialect` | Kuzeybatı Mandarin bölgesi |
| `et_missing.txt` / `brythonic` | `brythonic_language` | `briton_dialect` | 58 CE genel Briton kimliği; modun antik Briton isim havuzu |
| `et_missing.txt` / `bedouin` | `arabic_language` | `peninsular_dialect` | Vanilla Arap kültürlerinin ortak deseni |
| `et_missing.txt` / `baltic` | `baltic_language` | `western_baltic_dialect` | Curonian/Sudovian/Pruthenian deseni |
| `et_christianity.txt` / `chalcedonism` | `latin_language` | `church_dialect` | Vanilla `catholic` ve `catharism` deseni |
| `et_christianity.txt` / `arianism` | `latin_language` | `church_dialect` | Vanilla `catholic` ve `catharism` deseni |

`phoenician_language` bloğuna ayrıca `color = tyrian` (vanilla
`main_menu/common/named_colors/01_coa.txt`, Tyrian moru) ve
`family = semitic_language_family` eklendi.
Lehçe olarak `phoenician_language = { default = yes }` tanımlandı; böylece üst
anahtar kendi adlı varsayılan lehçe üzerinden çözülür ve Fenike erkek/kadın
isim havuzu korunur. `punic_dialect` `punic_culture` için ayrı kalır.

## Neden vanilla dil dosyaları override edilmedi

- `latin_language`, `occitan_language`, `mandarin_language`,
  `arabic_language` ve `baltic_language` için kendi adlı lehçe eklemek, aynı
  yollu override dosyalarının tamamını kopyalamayı gerektirirdi. Mevcut
  lehçeler hem tarihsel olarak daha doğru hem de bakım riski daha düşük.
- `brythonic_language` zaten modun aynı yollu override'ında; ancak `brythonic`
  kültürü 58 CE genel Briton kimliğidir ve modun eklediği `briton_dialect`
  antik Briton isim havuzunu taşır. Kültür bu nedenle `briton_dialect`e
  bağlandı; vanilla `language:brythonic_language` trigger semantiği
  değiştirilmedi.
- Etrüsk için vanilla/modda dil ve isim verisi yok; `roman_dialect` geçici
  olarak Latin isim havuzunu korur. Kaynaklı Etrüsk adları toplanınca ayrı
  görev açılmalı.

## Doğrulama

- Tek seferlik statik denetim: vanilla 528 üst düzey dil bloğu / 612
  adreslenebilir anahtar, 2.087 vanilla culture referansı / 0 çözülemeyen.
- 379 mod culture/religion `language =` referansı: 0 çözülemeyen.
- `script-token-audit.py`: 101 hedef, 0 çözülemeyen token.
- `test-b-report.py`: sınıf-1 artık "beklenen sıfır"; herhangi bir hit
  regresyon sayılıp çıkış kodu 1 üretir.
- Test B yeniden hazırlanmalı; 18 Ekim logu bu düzeltmeden önce alındı.

## Kalan iş

- `et_culture_events.txt` içindeki 103 `Invalid scope types ... link:
  location` satırı ayrı görevde. Aynı `this = location:` deseni vanilla
  `flavor_BUL.txt` (efekt) ve `flavor_ENG.txt` (`custom_tooltip` + `NOT`)
  içinde geçerli; statik karşılaştırma henüz farkı bulamadı, Test B'de tek
  noktadan doğrulanacak.
- 18 Ekim tabanındaki `jewish`, `berber_group` ve `folk_caucasian_group`
  bulguları bayat: `jewish` kültürü `a718859`'da eklendi; `berber_group`
  referansları mevcut `amazigh_group` / `maghrebi_group` ile değiştirildi ve
  `folk_caucasian_group` tanımlandı.
