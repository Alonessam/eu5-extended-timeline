# Tarihsel Olaylar ve Kültür Dönüşümü Planı (M.S. 58 → 1837)

Bu doküman, 58 CE senaryosunda halkların, kültürlerin ve dinlerin tarihsel
dönüşümünü sağlayacak **olay (script) katmanının** ve buna temel olacak **veri
araştırmasının** çalışma planıdır. Projenin veri-önce ilkesi gereği her dönüşüm
önce `et-history-data` içinde kaynaklı bir kayıt olarak toplanır; mod tarafındaki
olay scriptleri yalnızca bu kayıtlara dayanılarak yazılır. Planın teknik
kısımları 17 Ekim 2026'da incelenen kurulu EU5 1.3.x dosyalarından
doğrulanmıştır; doğrulama notları bu dokümandadır.

**Durum:** Plan yayında. Pilot bölge seçimi ve ara kimlik politikası maintainer
onayı bekliyor.

**Nasıl kullanılır:** Bu doküman canlıdır; fazlar ilerledikçe güncellenir.
Katkı vermek isteyen ekip üyeleri bölüm 4'teki iş paketlerinden veya bölüm
5'teki Faz 1 kontrol listesinden başlayabilir. Yeni veri ve script işleri,
bölüm 6'daki kalite kurallarına bağlıdır.

---

## 1. Neden gerekli

- 58 CE başlangıcı, nüfusu ağırlıklı olarak antik kültür bloklarında tutuyor
  (`roman`, `germanic`, `slavic`, `gallian`, `ancient_greek`, `old_egyptian`,
  `berber`, `persian` ...). Modern kimlikler (`french`, `german`, `english`,
  `greek`, `arabic`, `turkish` ...) tanımlı fakat başlangıçta neredeyse boş.
- Motor kendiliğinden yalnızca **asimilasyon** üretir: pop'lar yönetici devletin
  ana kültürüne yakınsar. Kültürlerin **bölünmesi/ayrışması** ve yeni
  kimliklerin doğuşu kendiliğinden yoktur; asimilasyonun yönü ve hızı kültür
  grafiğine (dil, aile, grup bağları) bağlıdır.
- Sonuç: olay katmanı olmadan 58→1837 oyunu Gallia'da francien/occitan
  ayrışmasını, Mısır'da koptik→Arap dönüşümünü, Germen ve Slav kimliklerinin
  çeşitlenmesini üretmez; dünya antik bloklarda donar ya da egemen kültüre
  homojenleşir.
- Üç katmanlı model:
  1. **Kültür grafiği** — asimilasyonun yönü ve hızı (dil/aile/grup/opinion
     bağları). Kısmen mevcut; boşlukları ayrı iş kalemidir (WS3).
  2. **Tarihsel olay katmanı** — pop kültür/din dönüşümleri, göçler, dil
     kaymaları, kimlik doğuşları. **Eksik; bu planın ana konusu.**
  3. **Devlet/formable katmanı** — modern ana kültürlü devletler; asimilasyonun
     hedef alacağı taşıyıcılar. Maintainer kararıdır (WS6).

## 2. Motorda doğrulanan araçlar (EU5 1.3.x)

İncelenen kurulu oyun dosyalarından (vanilla) doğrulanan script araçları:

| Araç | İşlev | Vanilla doğrulama |
|---|---|---|
| `change_pop_culture` | Pop kültürünü değiştirir (pop kapsamı) | `in_game/events/DHE/flavor_SWE.txt:2148` — Savonian/Tavastian/Kven pop'ları `finnish` yapılıyor |
| `change_pop_religion` | Pop dinini değiştirir (pop kapsamı) | `in_game/events/debug/qa_debug.txt:164` |
| `change_culture` | Ülke ana kültürünü değiştirir | `in_game/events/wokou_events.txt:566-569` |
| `change_character_culture` | Karakter kültürünü değiştirir | efekt listesi (wiki) |
| `change_language` | Bir kültürün dilini değiştirir | efekt listesi (wiki) |
| `form_new_culture` | Cabinet action (adm, 10 yıl): ana kültürden yeni kültür oluşturur | `common/cabinet_actions/form_new_culture.txt` |
| `merge_culture_group` | Cabinet action (10 yıl): ana kültürün grubunu birleştirir | `common/cabinet_actions/merge_culture_group.txt` |
| `add_migration` / `remove_migration` | Kültür ve din parametreli göç kurar | `in_game/events/culture/culture_greek.txt:2945` |
| `add_cultural_influence` / `add_cultural_tradition` | Kültür savaşı ivmesi | efekt listesi (wiki) |
| `force_refresh_culture_and_religion` | Lokasyonun baskın kültür/dinini yeniden hesaplar | efekt listesi (wiki) |

Yollar, incelenen kurulu oyundaki vanilla dosyalara aittir.

**Şablon ve altyapı kaynakları (vanilla):**

- `in_game/events/culture/` klasörü: `cultural_event.txt`, `culture_greek.txt`,
  `culture_italian.txt`, `culture_japan.txt`, `culture_religion_events.txt`,
  `language_events.txt`, `haudenosaunee.txt` — kültür olay zincirleri için hazır
  desenler.
- `in_game/common/on_action/`: `country_yearly.txt`, `country_monthly.txt`,
  `location_pulses.txt` vb. periyodik kancalar.
- Tarih penceresi deseni:
  `dynamic_historical_event = { tag = SWE from = 1400.1.1 to = 1600.1.1 monthly_chance = 30 }`
  (`flavor_SWE.txt`, olay 43).
- Standart olay alanları: `historical_option = yes`, `fire_only_once = yes`,
  `illustration_tags`, `custom_tooltip`.

Doğrulanmış pop dönüşümü kalıbı (`flavor_SWE.42`'den sadeleştirilmiştir):

```txt
option = {
    name = ...
    custom_tooltip = { text = ... }
    every_owned_location = {
        every_pop = {
            limit = {
                OR = {
                    culture = culture:savonian
                    culture = culture:tavastian
                }
            }
            change_pop_culture = culture:finnish
        }
    }
}
```

**Bilinen sınırlar ve dikkat noktaları:**

- Script, pop'ları **mevcut kültür anahtarları** arasında taşır. Ara kimlik
  gerekiyorsa (ör. `gallo_roman`) kültür dosyalarında önceden tanımlanmalıdır;
  bu bir veri işidir.
- `form_new_culture` motor-yönetimli yeni kültür oluşturur; AI bu eylemi
  normalde yalnızca sömürge bağlamlarında kullanır. Tarihsel ayrışma bu yüzden
  olay yazımına bağlıdır.
- `every_pop` döngüleri pahalıdır: olaylar lokasyon/ülke kapsamıyla
  sınırlanmalı; toplu dönüşümler `monthly_chance` ve kademeli oranlarla zamana
  yayılmalı; test loglarıyla izlenmelidir.
- Asimilasyon sabitleri
  (`Extended Timeline/loading_screen/common/defines/00_defines.txt`,
  `ASSIMILATION_*`): aynı dil/aile/grup ve pazar dili etkileri. Olay tasarımı bu
  ivmelerle birlikte düşünülmelidir.

## 3. Mevcut durum (17 Ekim 2026)

- **Script katmanı yok.** `Extended Timeline/in_game/` klasörleri: `common`,
  `localization`, `map_data`, `setup`. `events/`, `on_action/` ve `decisions/`
  hiç yok. Bu plan yeni katmanı kurar.
- **Başlangıç pop verisi** (`main_menu/setup/start/06_pops.txt`, ~50 bin pop
  bloğu): örnek — `gallian` ~1.000, `old_egyptian` ~300, modern `french` 0. Bu
  dağılım, dönüşümün ancak olaylarla kurulabileceğini gösterir.
- **Kültür grafiği kısmi**: mod kültür dosyaları (`et_*.txt`) ve diller mevcut;
  tespit edilen boşluklar arasında `old_egyptian` ve `kushite` kültürlerinin boş
  `culture_groups` taşıması ve `gallian` ile fransız hattı arasında doğrudan bağ
  bulunmaması var. Denetim tamamlanmadı.
- **Araştırma altyapısı hazır**:
  `research/native-history-requirements/2026-10-13/societies.yml` r13–r16,
  dönüşüm kayıt disiplinini tanımlıyor: etkilenen nüfus, başlangıç/bitiş
  kimliği, yer, aralık, ölçek, mekanizma, kaynak, güven. Bu planın veri işleri
  bu şemayı kullanır.
- **Referans sürüm**: incelenen kurulu dosyalar EU5 1.3.x içeriğidir (kurulum
  klasörü adı sürümü güvenilir biçimde göstermez; içerik esas alınmıştır).

## 4. İş paketleri

**WS1 — Kültür geçiş haritası (veri, P0).**
Her antik kültür için: ardıl kimlik(ler) (ara ve/veya modern), tarih aralığı,
bölge, mekanizma (fetih, göç, şehirleşme, din, ticaret), kaynak, güven. Kayıt
formatı: `societies.yml` r13–r16 alanları + `research/README.md` kayıt alanları
(`dating`, `source_refs`, `confidence`, `integration`). Çıktı: bu klasörde
`YYYY-MM-DD_<konu>.yml` dosyaları ve insan-okur raporu.

**WS2 — Din geçiş haritası (veri, P1).**
Hristiyanlaşma, İslamlaşma, Budizm/Manikeizm yayılımı gibi dalgalar;
`change_pop_religion` olaylarının temeli.

**WS3 — Kültür grafiği tamamlama (veri + mod, P1).**
Boş `culture_groups`, dil/aile bağları, `kindred`/opinion ağları. Asimilasyon
yönü ve hızı bu bağlara bağlıdır; WS1 ile çapraz çalışır.

**WS4 — Olay prototipleri (mod, P0 pilot).**
Pilot bölgede 3–5 olaylık zincir; bölüm 2'deki desenlerle yazılır; modda
`events/` + localization iskeleti kurulur; oyun içi test edilir.

**WS5 — Mekanizma kataloğu (doküman).**
Doğrulanmış efekt imzaları, olay şablonları, performans notları, localization
anahtarları — ekip için başvuru kaynağı. Bu doküman çekirdeğidir.

**WS6 — Devlet ve cabinet pacing (maintainer).**
Modern ana kültürlü devlet/formable'lar; `form_new_culture` /
`merge_culture_group` erişim ve AI davranışı; hangi olayların hangi devleti
zorlayacağı.

**WS7 — Süreç ve kalite.**
Veri-önce kuralı, test protokolü, merge disiplini (bkz. bölüm 6).

## 5. Fazlar

- **Faz 0 (bu dosya):** Plan yayında; pilot bölge ve ara kimlik kararları
  bekleniyor.
- **Faz 1 — Pilot:** Bölge seçimi (adaylar: **Galya**, **Mısır**) → kaynaklı
  geçiş kayıtları → 3–5 olaylık zincir → oyun içi test → şablon çıkarma.
- **Faz 2 — Geç Antik ve Kavimler Göçü (200–700):** Roma çöküşü sonrası
  Latin/Romance ayrışması; Germen ve Slav yayılımı; `add_migration` dalgaları.
- **Faz 3 — Postklasik (700–1400):** Arap fetihleri ve Arapçalaşma; Türk
  göçleri; Vikingler; Hristiyanlaşma dalgaları.
- **Faz 4 — Erken Modern ve Sanayi (1400–1837):** Kimlik konsolidasyonu ve
  sömürge dönemi; başlamadan önce vanilla sistemleriyle etkileşim incelemesi
  yapılır.

Her fazın akışı: kaynaklı veri → olay tasarımı → mod uygulaması → oyun içi test
→ backlog senkronu.

**Faz 1 açılış kontrol listesi:**

- [ ] Pilot bölge kararı (maintainer) — adaylar: Galya, Mısır
- [ ] Kaynak seti toplama (`research/sources.yml` içine yeni kaynaklar)
- [ ] Geçiş kayıtları (`research/historical-events/YYYY-MM-DD_<bölge>.yml`)
- [ ] Olay tasarım notu (olaylar, pencereler, koşullar, localization anahtarları)
- [ ] Mod iskeleti: `events/` + localization; olay scriptleri
- [ ] Oyun içi test (58 başlangıcı, hızlandırılmış gözlem) ve log kontrolü

## 6. Bağlayıcı kalite kuralları

1. Kaynaksız geçiş olayı yazılmaz; her kayıtta güven düzeyi ve belirsizlik
   açıkça belirtilir.
2. Tek lokasyon veya örneklem, bölge geneli dönüşüm iddiası kuramaz
   (`societies.yml` yorum kuralları).
3. Yönetici kimliği değişimi ile halk dönüşümü ayrı kaydedilir; siyasi din
   değişimi toplu dönüşüm sayılmaz.
4. Tarihler oyun gününe zorlanmaz; pencere (aralık/dönem) yaklaşımı kullanılır.
5. Sessiz override yok: maintainer kararı esastır; anlaşmazlıklar TODO notu veya
   backlog maddesiyle iletilir.
6. Performans bütçesi: toplu `every_pop` dönüşümleri kademeli ve sınırlı
   tutulur; test loglarıyla doğrulanır.

## 7. Açık kararlar (maintainer)

- Pilot bölge: Galya mı, Mısır mı, başka mı?
- Ara kimlikler (`gallo_roman` vb.) eklenecek mi; yoksa doğrudan modern
  kimliklere mi geçilecek?
- Railroad derecesi: sabit tarihler mi, koşullu pencereler mi?
- Hangi olaylar AI'yı zorlar (fetih/göç dalgaları); hangileri serbest
  simülasyona bırakılır?
- Cabinet action erişimleri (`form_new_culture` / `merge_culture_group`)
  değiştirilecek mi?

## 8. Kaynaklar ve referanslar

- `research/native-history-requirements/2026-10-13/societies.yml` ve
  `societies.md` — r13–r16 geçiş kayıt gereksinimleri.
- `research/backlog.yml` — ilgili açık işler
  (`historical_events_and_culture_transition`, `ancient_economy_roads_and_town_ranks` vb.).
- `Extended Timeline/loading_screen/common/defines/00_defines.txt` — asimilasyon
  ve kültür sabitleri.
- Vanilla 1.3.x dosyaları: bölüm 2'deki tablo.
- EU5 Wiki: [Culture](https://eu5.paradoxwikis.com/Culture).
