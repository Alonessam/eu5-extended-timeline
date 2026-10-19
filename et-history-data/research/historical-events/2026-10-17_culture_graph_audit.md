# Kültür Grafiği Denetimi (WS3) — 17 Ekim 2026

Mısır pilotunun ilk adımı olarak mod kültür dosyalarındaki grup/dil hattı
boşlukları tarandı; bulgular ve uygulanan düzeltmeler bu dosyadadır. Geçiş
kayıtları: `2026-10-17_egypt_culture_transition.yml`. Plan: `README.md`.

## Yöntem

- Tarama: `Extended Timeline/in_game/common/cultures/*.txt` içindeki her
  kültür bloğunda `culture_groups` alanı denetlendi (boş alan veya alanın hiç
  olmaması işaretlendi).
- Geçerlilik: grup kimlikleri vanilla
  `game/in_game/common/culture_groups/00_culture_groups.txt` listesiyle ve
  ardıl kültürlerin vanilla tanımlarıyla karşılaştırıldı.
- Ölçüt: 58→1837 hattında ardılı olan antik kültür, ardılının (modern
  kimliğin) grubuna bağlanır — mevcut ev deseni: `germanic` → `german_group`,
  `slavic` → `slavic_group`, `ancient_greek` → `greek_group`,
  `bedouin` → `arabic_group`.

## Uygulanan düzeltmeler

| Kültür | Dosya | Önce | Sonra | Gerekçe |
|---|---|---|---|---|
| `kushite` | `et_egypt.txt` | boş | `nilosahelian_group` | Ardıl Nubya kültürleri (vanilla `nubian`, `nuba`, `nyimang`, `toubou`) bu grupta |
| `old_egyptian` | `et_egypt.txt` | boş | `arabic_group` | Modern Mısır kimlikleri (`lower_egyptian_culture`, `upper_egyptian_culture`) `arabic_group` üyesi; Arapçalaşma akışına ivme |
| `gallian` | `et_celtic.txt` | `celtic_group`, `continental_celtic_group` | + `french_group` | Plan §3'te tespit edilen Galya→Fransız hattı boşluğu; `germanic` → `german_group` deseni |

Notlar:

- `old_egyptian` için alternatif olarak mod tanımlı yeni bir `egyptian_group`
  değerlendirildi; tek üyeli grup motor etkisi üretmeyeceği ve vanilla
  `coptic_culture` zaten grupsuz olduğu için reddedildi. Değişiklik tek
  satırdır ve geri alınabilir.
- `helleno_egyptian` zaten `greek_group` üyesi; Yunan-Mısırlı toplulukların
  zamanla `coptic_culture`/`lower_egyptian_culture` hattına emilmesi olay
  katmanı işidir (kayıt: `egypt_helleno_egyptian_absorption`).
- `gallian` düzeltmesi Mısır pilotu kapsamı dışındadır; plan §3'te
  işaretlendiği için aynı turda yapıldı.

## Taramada işaretlenen kalan kayıtlar

Toplam 39 işaret: 26'sı `east_asia.txt` kümesi, 13'ü diğer dosyalar. Bu turda
Mısır'la ilgili 2 kayıt (`kushite`, `old_egyptian`) düzeltildi; kalan 37 kayıt
aşağıda önceliklendirildi.

**Doğu Asya kümesi — 26 kayıt, öncelik dışı.** `ainu_culture`, `ryukyu_culture`,
`emishi`, `jinhan`, Çukotka/Yukagir kültürleri gibi çoğunlukla izole dil
ailesi kültürleri. Örnekleme gösterdi ki vanilla da `ainu_culture` ve
`ryukyu_culture` için grup tanımlamıyor; bu küme desen gereği grupsuz. Büyük
blok kültürleri etkilemiyor.

**Balkan hattı — `pannonian`, `illyrian` (`et_balkans.txt`).** Ardıl
eşleştirmesi veri turu gerektiriyor (Pannonya → Karpat/Macar hattı, İlirya →
Arnavut hattı adayları). Backlog: `culture_group_gaps_remaining`.

**Pers ve Güneydoğu Asya — `tocharian` (`et_persian.txt`), `pyu`, `pear`
(`et_south_east_asia.txt`).** Tohar (tükendi/karıştı; aday: turkic hattı) ve
Pyu/Pear (Birmanya/Mon-Khmer) kararları aynı backlog maddesindedir.

**`et_missing.txt` fallback seti — `apache`, `bantu`, `garjati`, `tepic`,
`arvanite`, `kanek_culture`.** `missing_language` tabanlı yer tutucular; grup
atamasından önce kimliklerinin netleşmesi gerekir (fallback politikası ayrı
iş).

## Dil notları

- Mod dilleri `egyptian_language` ve `meroitic_language` aile (`family`)
  alanısız ve isim listeleri TODO durumunda. Vanilla `coptic_language` de
  aile alanı taşımıyor; tutarlılık için şimdilik değiştirilmedi. Aile eklemek
  vanilla dil dosyalarını override etmeyi gerektirir (bakım riski) — açık iş.
- `arabic_group` eşleştirmesinin oyun içi etkisi çoğunlukla geç dönemde
  görünür (Arap hanedanları Mısır'a yerleşince asimilasyon ivmesi); 58 CE
  başlangıcında etkileşim ihmal edilebilir.

## Sınırlar

Tarama mod dosyalarıyla sınırlıdır ve sezgisel bir blok ayrıştırıcı kullanır;
vanilla ardıl tanımları elle örneklendi. İki örnekle (ainu, ryukyu) Doğu Asya
kümesinin grupsuzluğunun vanilla deseni olduğu doğrulandı; kümenin tamamı tek
tek doğrulanmadı.

## Güncelleme (19 Ekim 2026)

Tarama her dosyanın ilk bloğunu atlamış: `et_subsaharan.txt`'in ilk bloğu
`jukun` ve `et_turkic.txt`'in ilk bloğu `hunnic` bu notta hiç
işaretlenmemişti (kalan sayısı 37 değil 39'du). Kapanış turunda 14 kültür
vanilla ardıl gruplarına bağlandı; Doğu Asya kümesi dil-kardeş taramasıyla
yeniden denetlendi ve iki istisna (`jinhan`, `yupighyt_culture`) bulundu.
Kalan 25 kayıt (24 Doğu Asya izolesi + `arvanite`) kasıtlı grupsuzdur.
Ayrıntılar: `2026-10-19_culture_group_gaps.md`.
