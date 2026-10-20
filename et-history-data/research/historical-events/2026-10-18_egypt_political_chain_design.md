# Mısır Siyasi Olay Zinciri — Tasarım Notu (Faz 1 / WS4, Parti 1)

**Tarih:** 18 Ekim 2026 · **Hat:** Mısır (siyasi katman) · **Durum:** Parti 1
uygulandı (`et_culture.8`–`.16` + `et_egypt_occupier_pulse`); Test B bekliyor.
**Veri temeli:** `2026-10-18_egypt_political_timeline.yml` (9 kayıt).
**Kalite kuralları:** `README.md` bölüm 6. **Numara rezervasyonu:** Mısır
`.1`–`.49` (siyasi zincir `.8`'den devam eder).

Bu not, Mısır'ın 215–969 arasındaki siyasi aktörlerini (Roma, Sasani işgali,
Râşidûn, Emevî, Abbasi, Tolun, İhşid, Fâtımî ve Bizans karşı saldırısı)
sahip-bağımsız pulse mimarisi üzerinden oyuna bağlar. Kültür zinciri v1
(`2026-10-17_egypt_event_design.md`) halk dönüşümünü işler; bu zincir
yöneten/elinde tutan aktörün siyasi kararlarını işler.

## 1. Olay tablosu

| ID | Etiket | Pencere | Çapa | Kayıt | Nabız |
|---|---|---|---|---|---|
| `.8` | ROM | 214–217 | alexandria (sahip) | egypt_caracalla_alexandria_215 | yıllık |
| `.9` | ERA | 618–630 | alexandria/cairo/aswan (sahip veya kontrol) | egypt_sasanian_occupation_618_629 | işgalci |
| `.10` | RASH | 639–650 | alexandria/cairo/aswan | egypt_arab_conquest_and_fustat_641 | yıllık |
| `.11` | UMAY | 700–712 | alexandria/cairo/aswan | egypt_arabic_chancery_reform_706 | yıllık |
| `.12` | ABBA | 825–835 | alexandria/cairo/aswan | egypt_bashmurite_revolts_831_832 | yıllık |
| `.13` | EGY | 866–880 | alexandria/cairo/aswan | egypt_tulunid_autonomy_868_905 | yıllık |
| `.14` | EGY | 933–945 | alexandria/cairo/aswan | egypt_ikhshidid_rule_935_969 | yıllık |
| `.15` | FATI | 968–978 | alexandria/cairo/aswan | egypt_fatimid_conquest_and_cairo_969_973 | yıllık |
| `.16` | BYZ | 644–647 | alexandria (sahip veya kontrol) | egypt_byzantine_counterattack_645_646 | işgalci |

## 2. Mimari

- Her olay kendi `tag`, pencere, çapa ve `has_variable` kilidini taşır; çift
  ateşleme yoktur (aynı yıl içinde ikinci nabız da tetiklense kilit tutar).
- Sahip olayları mevcut `et_egypt_yearly_pulse` listesindedir (`.1`–`.5` ile
  aynı nabız); işgalci olayları yeni `et_egypt_occupier_pulse` listesindedir.
- İşgalci nabzı `trigger = { OR = { controls = location:... } }` çapalarına
  bakar: eyaleti sahiplenmeden elinde tutan ülkenin (ERA 618–629, BYZ 645–646)
  olaylarını ateşler. Nabız `yearly_country_pulse` içine eklenmiştir (vanilla
  "mod may only add" kuralı).
- Etkiler görünür ve hafiftir: `add_prestige` (`prestige_mild_*`) ve
  `add_stability`; parti 1'de pop etkisi yoktur. Tarihsel seçenek
  `historical_option = yes` ile işaretlidir; alternatifler dengeli/cezalı
  varyantlardır.

## 3. Bağımlılıklar ve varsayımlar

- `.9` ve `.16`, state katmanının 618–628 (ERA) ve 645–646 (BYZ) kontrol
  pencerelerine bağlıdır; pencere oyunda yoksa olaylar sessizce ateşlenmez
  (zararsız) ve Test B bunu ölçer.
- `.8` yalnızca ROM sahibi içindir; Roma dışı dönemlerin siyasi anlatısı
  parti 2+'ya bırakılmıştır (58–618 Roma eyaleti kültür zincirinde temsil
  edilir).
- `.10`–`.15`, etiket geçişlerinin state katmanınca üretilmesini bekler
  (RASH → UMAY → ABBA → EGY → FATI sırası). Etiketler `et_countries.txt`
  üzerinden mod içinde tanımlıdır.
- Irak/Şam odaklı etiketlerin (UMAY, ABBA) Mısır'ı elde tuttuğu pencereler
  state katmanı verisine dayanır; veriyle çelişki görülürse önce veri
  düzeltilir (sessiz override yok).

## 4. Parti 2+ ve açık boşluklar

- Palmyra 269/270–272: `PALM` ülke dosyası var, Mısır lokasyon katmanında
  PALM penceresi yok; olay yazılmadı (`egypt_state_layer_palmyra_270_272`).
- Fâtımî sonrası: Eyyûbî (1171), Memlûk (1250), Osmanlı (1517), Fransız
  işgali (1798–1801; FRA işgalci nabzına eklenecek), Muhammed Ali (1805),
  İngiliz işgali (1882), 1919, 1952 ve cumhuriyet
  (`egypt_political_chain_batch2`).
- AIA (1958–1971) ve `EGYP - Egypt.yml` ayrımı ayrı bir veri işi olarak
  duruyor (1958–1971 Mısır temsili).

## 5. Test protokolü (Test B eki)

1. `change_date` ile 214/618/639/700/825/866/933/968/644 yıllarına git;
   ilgili etikete geç ve `event_probabilities` + `test_event_trigger` ile
   `.8`–`.16` tetiklerini doğrula.
2. State katmanı aktifken işgalci nabzı için ERA 618–628 (alexandria
   `controls`) ve BYZ 645–646 senaryolarını ayrıca ateşle; nabız listelerinin
   çift ateşlemediğini `has_variable` üzerinden kontrol et (`.9` ve `.16`
   yalnızca işgalci nabzındadır; `.8` ve `.10`–`.15` yalnızca yıllık nabızda).
3. `error.log`'da mod satırı olmamalı; olay kartları EN/TR okunmalı.

## 6. İzlenebilirlik

- Kayıtlar: `2026-10-18_egypt_political_timeline.yml` (9 kayıt; belirsizlikler
  `confidence` ve kaynak `caveat` alanlarındadır).
- Kaynaklar (yeni): wiki_caracalla, wiki_sasanian_conquest_egypt, wiki_fustat,
  wiki_bashmurian_revolts, wiki_tulunid_dynasty, wiki_ikhshidid_dynasty,
  wiki_fatimid_conquest_egypt, wiki_al_walid_i.
- Lokalizasyon: `et_culture_events_l_english.yml` / `_turkish.yml`
  (`.8`–`.16` anahtarları); Nübya bloğundaki literal `?` mojibake'i aynı gün
  onarıldı (commit bcfe27f).
- Olaylar: `Extended Timeline/in_game/events/et_culture_events.txt`
  (`.7`'den sonraki blok); nabızlar: `on_action/et_history_pulses.txt`.
- Backlog: UPDATE 23 (origin/main senkronu sonrası yeniden numaralandı) +
  `egypt_state_layer_palmyra_270_272` + `egypt_political_chain_batch2`;
  `et_culture_outcome_token_normalization` 19 Ekim'de UPDATE 16 ile kapandı
  (13 `outcome = good` → `positive`; `research/backlog.yml`).
