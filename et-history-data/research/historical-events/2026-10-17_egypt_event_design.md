# Mısır Pilotu — Olay Tasarım Notu (Faz 1 / WS4)

**Tarih:** 17 Ekim 2026 · **Hat:** Mısır (paralel pilot) · **Durum:** v1
scriptlendi; **Test A geçti** (17 Ekim 2026: `et_culture.9000` ve Galya `.101`
oyun içinde ateşlendi, `error.log`'da mod satırı yok — kanıt bölüm 5). Zincir
doğrulaması (Test B, console protokolü) sırada. Samet'in inceleme commit'i (`f3d304d`) payları spec'e hizaladı; son-kimlik anahtarlarının sahipliği **ikinci incelemede karara bağlandı** (17 Ekim 2026): vanilla içerik korunur, deltasız mod kopyaları geri alındı (bölüm 7, kararlar 7–8). Numara mutabakatı sağlandı:
Galya pilotu `.101`–`.103` olarak ayrıldı.

**Veri temeli:** `2026-10-17_egypt_culture_transition.yml` (11 kayıtlı geçiş).
**Kalite kuralları:** `README.md` bölüm 6. **Doğrulama kaynağı:** kurulu EU5
1.3.x vanilla dosyaları (bölüm 9'da dosya:satır kanıtları).

Bu not, Mısır pilotunun olay zincirini oyun içi davranışa çevirir: hangi
olaylar, hangi pencerelerde, hangi koşullarla ateşlenir; hangi pop
dönüşümlerini yapar; hangi localization anahtarlarını kullanır. İzlenebilirlik
kuralı gereği her olay bir veya daha fazla kayda bağlanır; kaynağı zayıf
kayıtlar (helleno emilmesi) bu turda **scriptlenmez**.

## 1. Hedeflenen dönüşümler

| Katman | 58 başlangıcı | Ara | 1837 hedefi |
|---|---|---|---|
| Din | `egyptian_polytheism` | `miaphysite` (Kıptî/Oryantal Ortodoks) | `islam` çoğunluk + ~%10 `miaphysite` azınlık |
| Kültür | `old_egyptian` | `coptic_culture` (kimlik) | `lower_egyptian_culture` / `upper_egyptian_culture` + Kopt azınlık |
| Nübye (ek) | `kushite` | `nubian` + Hristiyanlaşma | Nübya'da Hristiyan Nubya krallıkları mirası |
| Yunan (helleno) | `helleno_egyptian` | — (kaynak zayıf) | **Bu turda script yok** — kayıt `pending` kalır |

Hedef oran: Memlûk dönemi sonunda Müslüman/Hristiyan oranı kaba **10:1**
(islamization_waves kaydı). Zincir bu orana kademeli dalgalarla yaklaşır;
kesin paylar test sonrası kalibre edilir (bölüm 7, karar 4).

## 2. Ateşleme mimarisi (doğrulanmış)

### 2.1 Neden DHE değil?

- Vanilla'daki `dynamic_historical_event` bloklarının **tamamı** `tag` zorunlu
  kullanır (3235/3235 blok tarandı; tag'siz yok). Mısır'ın sahibi 58→1837
  arasında simülasyona göre değişir (Roma → kim fethederse); sabit tag listesi
  bu projede kırılgandır.
- Çözüm: `yearly_country_pulse`'a bağlanan **dar koşullu alt-pulse**.
  Sahip-bağımsız çalışır: bölgeyi elinde tutan her devlet kendi zincirini
  yürütür. (EU5 Wiki, "Modding on actions": *"Only a new on_actions block can
  be added to existing on actions."*)

### 2.2 Vanilla deseni (kanıt)

```txt
# country_yearly.txt:911-914 — dar koşullu pulse deseni
yearly_flavor_nav_pulse = {
	trigger = { owns = location:olite }
	events = { flavor_nav.60 }
}
```

- Ucuza çalışan dış koşul, pahalı olay trigger'larını 300+ ülke için atlar
  (vanilla'nın kendi optimizasyon yorumu, `country_yearly.txt:5-7`).
- Olaylar kendi trigger'larını taşır; `country_yearly.txt:926-929` örneği
  pencere koşulunu olay yerine pulse trigger'ında `current_year >= 1520` ile
  gösterir. Bizde pencere koşulları **olay içinde** olacak (olay başına farklı
  pencereler var).

### 2.3 Yeni dosya: `Extended Timeline/in_game/common/on_action/et_history_pulses.txt`

Modda henüz `on_action/` klasörü **yok**; bu dosya ilk olacak. Modun kendi
on_action tanımı yalnız `on_actions` bloğu ekler; vanilla'ya başka blok
eklenmez (wiki kuralı).

```txt
# Extended Timeline — bölgesel tarihsel olay nabızları (dar koşullu alt-pulse
# deseni; baz alınan vanilla: in_game/common/on_action/country_yearly.txt).
# Şablon/plan: et-history-data/research/historical-events/README.md

yearly_country_pulse = {
	on_actions = {
		et_egypt_yearly_pulse
	}
}

et_egypt_yearly_pulse = {
	# Ucuz dış koşul: ülkenin Mısır'da ayağı var mı?
	trigger = {
		OR = {
			owns = location:alexandria
			owns = location:cairo
			owns = location:aswan
		}
	}
	events = {
		et_culture.1
		et_culture.2
		et_culture.3
		et_culture.4
		et_culture.5
	}
}
```

- `location:cairo` / `location:aswan` anahtarları bölge tanımından doğrulandı
  (`map_data/definitions.txt:5337-5352`). Gerekirse testte `asyut`/`qus` çapa
  olarak eklenir.
- İleride Galya ve diğer bölgeler kendi alt-pulse'larını **aynı dosyaya**
  ekleyebilir (Samet ile koordinasyon: çakışmayı önlemek için tek dosya).

### 2.4 Pop dönüşümü aracı: `split_pop`

Kademeli dönüşümün anahtarı **oransal ayrıştırma**: eşleşen pop'un yalnız bir
kesri ayrılıp yeni din/kültüre geçer, kalan aynı kalır.

- Doğrulama: `split_pop` vanilla'da 221 yerde (219'u `fraction`lı);
  aynı desen Mısır'ın Kıptîleri için vanilyada birebir var:
  `flavor_MAM.txt:2606-2688` ("Converting the Copts",
  `fraction = 0.2 religion = religion:sunni`, `area:lower_egypt_area`).
- Kültür parametresi de destekli: `fraction = 0.20 culture = culture:greek_culture`
  (`flavor_BYZ.txt:1934`); `type = pop_type:clergy` kombinasyonu
  (`000_johan_debug.txt:1190-1194`).
- Toplu (`change_pop_culture`/`change_pop_religion`) yalnız gerekirse; pilot
  kademeli paylarla yürür (kalite kuralı 6: performans + kademelilik).

### 2.5 Bölge kapsamı ve koşullar

- Bölge: `lower_egypt_area` (Alexandria, Cairo, Pelusium...) ve
  `upper_egypt_area` (Asyut, Qus, Aswan...) —
  `map_data/definitions.txt:5337-5352`; kapsam kalıbı:
  `every_owned_location = { limit = { area = area:lower_egypt_area } every_pop = { ... } }`
  (`flavor_MAM.txt:2663-2676` birebir desen).
- Pencere: `current_year >= X` / `<= Y` (`country_yearly.txt:927`).
- Sahip dini: `religion.group = religion_group:muslim`
  (`country_yearly.txt:940` ülke kapsamında doğrulandı).
- Tekilleştirme: `fire_only_once` **kullanılmaz** — Mısır birden çok devlet
  arasında bölünürse her sahip kendi zincirini yürütmelidir. Onun yerine ülke
  değişkeni: trigger'da `NOT = { has_variable = et_egypt_... }`, seçeneklerde
  `set_variable = { name = et_egypt_... }` (`flavor_MAM.txt:2702-2707` deseni;
  süresiz işaret için `days` yok). *(Olay ateşleme + değişken davranışı
  test B'de doğrulanacak.)*
- Din/kültür oranı fonksiyonları (`religion_percentage_in_country` vb.) yalnız
  **ülke geneli** ölçer; Roma gibi dev sahiplerde Mısır payı küçük kalacağından
  zincir ağırlıklı olarak değişkenlerle sürülür. Bölge oranı gerekirse
  `any_location_in_area = { count > N ... }` deseni kullanılır
  (`flavor_MAM.txt:2631-2637`).

### 2.6 Anahtar envanteri (hepsi mevcut — yeni anahtar gerekmiyor)

| Anahtar | Tür | Kaynak | Not |
|---|---|---|---|
| `egyptian_polytheism` | din | mod (`et_egyptian.txt:1`) | 58 kurulumunda Mısır popları bu dinde |
| `miaphysite` | din | vanilla (`christian.txt:365`) + mod (`et_christianity.txt:108`) | `enable` yok → 58'den itibaren kullanılabilir; mod bloğu = vanilla birebir + `language = coptic_language` (bölüm 7, karar 7) |
| `chalcedonism` | din | mod (`et_christianity.txt:2`) | `enable = 2.1.1` → 58'de açık (Melkit hattı) |
| `islam` | din | mod (`et_muslim.txt:2`) | `group = muslim` |
| `old_egyptian` → `coptic_culture` → `lower/upper_egyptian_culture` | kültür | mod + vanilla | WS3 düzeltmeleriyle grup bağları hazır |
| `kushite` → `nubian` | kültür | mod + vanilla | `nilosahelian_group` |
| `clergy_estate`, `dhimmi_estate` | estate | vanilla | MAM deseninde kullanılıyor; mod uyumu test edilecek |

## 3. Olay zinciri — 5 çekirdek olay

**Ortak ilkeler:**

1. Her olay, bir veya daha fazla WS1 kaydına bağlanır (bölüm 8 tablosu).
2. Her olayın iki seçeneği vardır:
   **(a) tarihsel** (`historical_option = yes`; AI bunu seçer) → dönüşüm +
   zincir işareti; **(b) direniş/yavaşlatma** → küçük dönüşüm payı, zinciri
   ilerletmez. Böylece oyuncu kararı diverjinansa dönüşür; hiçbir dönüşüm
   sessizce zorlanmaz.
3. Ateşleme: yalnız `et_egypt_yearly_pulse` üzerinden (DHE bloğu **yok**).
4. Metinler EN + TR; `historical_info` kaynağı özetler.

**Uygulama notları (v1 — scriptle eşitlenen sapmalar, 17 Ekim 2026):**

- **Tekilleştirme iki katmanlı:** her olay `immediate` bloğunda ateş anında
  `et_egypt_N_fired` işaretçisini kurar (oyuncu seçim beklerken pulse ikinci
  popup açamaz); seçim sonuçları ayrı değişkenlerdir (`et_egypt_christ_1`,
  `..._coptic`, `..._islam_1`, `..._islam_2`, `..._arabized` + `*_resist`).
  Bölüm 2.5'teki "trigger'da `NOT has_variable`" ilkesi bu iki katmanla
  uygulanır.
- **.1:** dönüşüm limitine `culture = culture:old_egyptian` süzgeci eklendi
  (Mısır bölgelerinde yaşayan Beja vb. topluluklar kapsam dışı). Direniş payı
  iki bölgede de `0.05`.
- **.2:** (i) **din tamamlama adımı eklendi** — putperest `old_egyptian`
  poplarda Delta `0.45` / Yukarı Mısır `0.35` → `miaphysite` (kayıt:
  Hristiyanlaşma 4.–5. yy'da çoğunluk; ilk dalga tek başına düşük kalıyordu).
  (ii) **kimlik geçişi kesirsiz uygulandı**: `miaphysite` + `old_egyptian`
  popların **tamamı** `coptic_culture`'a geçer. Gerekçe: sınıflama tutarlılığı —
  Hristiyan = Kopt (vanilla 1337 görünümü); kesirli geçiş kalıcı "Hristiyan ama
  Eski Mısırlı" pop yığını bırakıyordu. (iii) **direniş payı spec'e hizalandı:** Delta/Yukarı Mısır `0.15`/`0.15` (Samet, `f3d304d`; v1 scriptte `0.05` idi).
- **.3:** pencere `650–1100` yapıldı (kayıt: vilayet dönemi erken
  İslamlaşma; fetih sonrası tıkanmayı önlemek için esnetildi); dönüşüm limitine putperest kalıntı OR'u ve kültür süzgeci
  (`old_egyptian`/`coptic_culture`) eklendi — direniş rotasında bile İslamlaşma
  tutarlı ilerler. Direniş payı `0.05`/`0.05`.
- **.4:** limit genişletmesi .3 ile aynı; paylar `0.60`/`0.50`, direniş `0.10`.
- **.5:** limit `religion = islam` **ve** kültür OR'u {`coptic_culture`,
  `old_egyptian`}; direniş Delta `0.25` / Yukarı Mısır `0.15` — senkron çözüldü (17 Ekim 2026 ikinci inceleme: script spec'e geri alındı; bölüm 7, karar 8).
- **Son-kimlik anahtarları — ikinci inceleme (17 Ekim 2026, bölüm 7 karar 7):** `f3d304d` kopyaları denetlendi; deltasız olanlar geri alındı — `arabic_language`, `coptic_language` (`00_et_african.txt`) ve `lower/upper_egyptian_culture` (`et_egypt.txt`) artık **vanilla tanımlarıyla** yüklenir (7 Arapça diyalekti, isim havuzları, `opinions`/`goods_demand_modifier` geri geldi). Deltalılar vanilla birebir + delta olarak kaldı: `coptic_culture` (+`arabic_group`; `et_egypt.txt:45-64`) ve `miaphysite` (+`language = coptic_language`; `et_christianity.txt:106-143`).
- **custom_tooltip deseni:** dönüşüm efektleri, vanilla MAM/SWE deseniyle
  (`flavor_MAM.txt:2661-2677`) `custom_tooltip` bloğunun **içine** yazıldı
  (görünüm + yürütme birebir vanilla).
- **Nübya (`.6`/`.7`) bu sürümde yok** — bölüm 7 karar 3 bekliyor.
- **`et_culture.9000`** test olayı: Test A (17 Ekim 2026) geçti; zincir
  doğrulaması (Test B) geçince emekliye ayrılır.

### et_culture.1 — "Nil'de Yeni Bir Şafak" / "A New Dawn on the Nile"

*Hristiyanlaşma I — kentler ve Delta önde (tahmini pencere: 200–500).*

- **Kayıt:** `egypt_christianization_rise`.
- **Trigger:** `current_year >= 200`, `current_year <= 500`,
  `NOT = { has_variable = et_egypt_christ_1 }`,
  `NOT = { has_variable = et_egypt_christ_resist }`.
- **Etki (tarihsel):** Delta için `fraction = 0.30`,
  Yukarı Mısır için `fraction = 0.15` — hedef `religion = religion:miaphysite`,
  kaynak `religion = religion:egyptian_polytheism`.
  `set_variable = { name = et_egypt_christ_1 }`; clergy estate hafif olumlu.
- **Etki (direniş):** `fraction = 0.05`; `et_egypt_christ_resist` işareti;
  hafif stability/clergy maliyeti. Zincir burada durur (diverjinans).
- **Notlar:** Sahibin devlet dini koşulu aranmaz — imparatorluk putperestken
  halk Hristiyanlaştı (tarihsel gerçek). Dönüşüm hedefi doğrudan `miaphysite`;
  451 ayrımının Melkit tarafı (`chalcedonism`) bu olayda dönüştürülmez
  (`egypt_chalcedon_split_451` kaydı metin düzeyinde işlenir).
  Opsiyonel süs: ayrılan payın küçük bir kısmı `type = pop_type:clergy`
  (vanilla johan debug deseni) — test edilir.

### et_culture.2 — "Kıptî Kimliği" / "The Coptic Identity"

*Kimlik kayması: aynı nüfus, yeni ad (tahmini pencere: 300–600).*

- **Kayıt:** `egypt_coptic_emergence_and_continuity`
  (+ metinde `egypt_chalcedon_split_451`).
- **Trigger:** `has_variable = et_egypt_christ_1`,
  `current_year >= 300`, `current_year <= 600`,
  `NOT = { has_variable = et_egypt_coptic }`.
- **Etki (tarihsel):** `culture = culture:old_egyptian` **ve**
  `religion = religion:miaphysite` poplar için: Delta `fraction = 0.55`,
  Yukarı Mısır `fraction = 0.40` → `culture = culture:coptic_culture`;
  `set_variable = { name = et_egypt_coptic }`.
- **Etki (direniş):** `fraction = 0.15`; zincir ilerlemez.
- **Not:** Bu bir göç/dönüşüm değil, **süreklilik içinde kimlik** değişimidir
  (kayıt: yazı ve din eksenli). Hristiyanlaşmamış `old_egyptian` poplar
  kimlik değiştirmez — resimde kalır, asimilasyon motoru kendi işini yapar.

### et_culture.3 — "Zimmi Yılları" / "The Years of the Dhimma"

*İslamlaşma I — vilayet dönemi (tahmini pencere: 650–1100).*

- **Kayıtlar:** `egypt_islamization_waves`; bağlam:
  `egypt_arab_conquest_639_642` (fetih **zorlanmaz**, bkz. karar 1),
  `egypt_arabic_administration_700` (metin).
- **Trigger:** sahip `religion.group = religion_group:muslim`,
  `current_year >= 650`, `current_year <= 1100`,
  `NOT = { has_variable = et_egypt_islam_1 }` (+ `..._resist`).
- **Etki (tarihsel):** `religion = religion:miaphysite` poplar için
  Delta `fraction = 0.30`, Yukarı Mısır `fraction = 0.15` →
  `religion = religion:islam`; `set_variable = { name = et_egypt_islam_1 }`;
  dhimmi/clergy estate dengesi (MAM deseni).
- **Etki (direniş):** `fraction = 0.05` + işaret; zincir ilerlemez.
- **Notlar:** Müslüman egemenlik **hiç oluşmazsa olay hiç ateşlenmez** —
  koşullu pencere, zorlama yok (diverjinans). Diverjinans uyumu için
  putperest kalıntıyı da dönüştürmek gerekirse kaynak limitine
  `OR = { religion = religion:egyptian_polytheism }` eklenir (test aşamasında
  değerlendirilir; kayıt Hristiyan dönüşümünü belgeler).

### et_culture.4 — "On Kala Bir" / "Ten to One"

*İslamlaşma II — çoğunluk dalgası (tahmini pencere: 1000–1400).*

- **Kayıt:** `egypt_islamization_waves` (Fâtımî ve bilhassa 14. yy Memlûk
  dalgası; 10:1 hedefi).
- **Trigger:** `has_variable = et_egypt_islam_1`, sahip
  `religion.group = religion_group:muslim`, `current_year >= 1000`,
  `current_year <= 1400`, `NOT = { has_variable = et_egypt_islam_2 }`.
- **Etki (tarihsel):** Delta `fraction = 0.60`, Yukarı Mısır
  `fraction = 0.50` → `religion = religion:islam`;
  `set_variable = { name = et_egypt_islam_2 }`.
- **Etki (direniş):** `fraction = 0.10`.
- **Not (kalibrasyon):** İki dalga sonrası kaba kalıntı: Delta ~%28,
  Yukarı Mısır ~%42. Hedef 10:1'e yaklaşmak için (i) vanilla organik dönüşüm
  katkısı, (ii) gerekirse pencere sonunda küçük bir **denge dalgası** (.4b,
  ör. 1400–1600). Karar test verisiyle verilir (bölüm 7, karar 4).

### et_culture.5 — "Dilin Sessiz Değişimi" / "The Quiet Language Shift"

*Arapçalaşma — kültür kayması (tahmini pencere: 950–1450).*

- **Kayıtlar:** `egypt_coptic_spoken_decline` (+ `egypt_arabic_administration_700`
  çerçevesi: "şehirler önce" — kademe metinde işlenir).
- **Trigger:** `has_variable = et_egypt_islam_1`, `current_year >= 950`,
  `current_year <= 1450`, `NOT = { has_variable = et_egypt_arabized }`.
- **Etki (tarihsel):** `culture = culture:coptic_culture` **ve**
  `religion = religion:islam` poplar için: Delta `fraction = 0.75` →
  `culture = culture:lower_egyptian_culture`; Yukarı Mısır `fraction = 0.55` →
  `culture = culture:upper_egyptian_culture`; `set_variable = { name = et_egypt_arabized }`.
- **Etki (direniş):** `fraction = 0.25`.
- **Not:** Hristiyan Koptlar `coptic_culture`'da kalır (kimlik korunur);
  hedef 1837 görünümü: Kıptî azınlık + Müslüman Arap-Mısırlı çoğunluk.
  Kalan Müslüman-Kopt poplar dil geçişinin kuşak aldığını temsil eder.

### N?bya eki (Faz 1'e al?nd? ? b?l?m 7 karar 3, 20 Ekim 2026)

?nc?l do?rulamas? 20 Ekim 2026'da yap?ld?: harita alan? `nubia_proper_area`
(nobatia/makuria/suakin eyaletleri) mevcut; 58 CE kurulumunda MERO bu alan? ve
`faras`, `dongola`, `qasr_ibrim` ?apalar?n? tutuyor; kushite n?fus 23 konumda 195
birimlik; `nubian` k?lt?r? vanilla, `kushite` k?lt?r? modun `et_egypt.txt`
dosyas?nda (`nilosahelian_group` ba?l?); `meroitic_language` modda tan?ml?.

- **et_culture.6 ? "Mero?'nin Sessizli?i"** (pencere 300?450):
  `area:nubia_proper_area` i?inde `kushite` ? `nubian`, `fraction = 0.60`.
  Direni? dal?: `fraction = 0.15` ve zincir de?i?keni yaz?lmaz.
  Kay?t: `kush_meroe_collapse_and_nubian_successors`.
- **et_culture.7 ? "Nobatia'n?n Vaftizi"** (pencere 536?700):
  `nubian`/`kushite` + `egyptian_polytheism` ? `miaphysite`, `fraction = 0.60`
  (kasaba dalgas?). Direni?: `fraction = 0.10`.
- **et_culture.8 ? "Hristiyan K?yler"** (pencere 700?900):
  kalan n?fustan `fraction = 0.80` ? `miaphysite` (k?y dalgas?). Direni?:
  `fraction = 0.10`.
- Pulse: `et_nubia_yearly_pulse`, ?apa `owns = location:faras` (M?s?r pulse'?
  gibi sahibinden ba??ms?z; b?lgeyi devralan devlet zinciri s?rd?r?r).
- Zincir de?i?kenleri: `et_nubia_6` ? `.7` ? `.8`; direni? dal? hi?bir zincir
  de?i?keni yazmad??? i?in sonraki olay tetiklenmez (M?s?r'daki `_resist`
  de?i?kenlerinden farkl? olarak okunmayan de?i?ken b?rakmaz).
- Yerelle?tirme: EN/TR 21 yeni anahtar (`.6`/`.7`/`.8` ba?l?k, g?vde, tarih
  notu, iki se?enek ad? ve iki ipucu).

### M?s?r dengeleme dalgas? ? et_culture.9 (b?l?m 7 karar 4, 20 Ekim 2026)

Statik hesap (58 CE kurulumundaki `old_egyptian` + `egyptian_polytheism` n?fusu:
Delta 3.468, Yukar? M?s?r 1.309) ?imdiki dalgalar?n sonunda **1:3,2**
M?sl?man-Hristiyan oran? veriyor; kayd?n hedefi (Meml?k d?nemi sonunda yakla??k
10:1) i?in bir dengeleme ad?m? gerekiyor. Tasarlanan notta ?ng?r?len `.4b`
dalgas? olarak uyguland?:

- **et_culture.9 ? "The Mamluk Wave"** (pencere 1300?1500): kalan Hristiyan ve
  putperest n?fustan Delta `fraction = 0.65`, Yukar? M?s?r `fraction = 0.55`
  ? `islam`. Direni?: 0,10 / 0,10.
- Zincir: `has_variable = et_egypt_islam_2` (yani `.4` tarihsel se?ene?i se?ilirse
  ate?lenir; direni? dal? zinciri durdurur).
- Tahmini sonu?: Delta %90 M?sl?man / %8,6 Hristiyan, Yukar? M?s?r %81 / %9,3;
  birle?ik oran ? 1:9,7 ? kayd?n 10:1 hedefine yak?n. Paylar kalibrasyon
  d??mesidir: Test B pano okumas? farkl? sonu? verirse yaln?zca bu iki say?
  de?i?ir.

### Kapsam dışı (bilinçli)

- **`egypt_helleno_egyptian_absorption`:** kaynak ihtiyac? 20 Ekim 2026'da
  kapand? (Papaconstantinou 2012, Cromwell 2021; `confidence: medium`, tarihlendirme
  c. 650-800) ama olay yine yaz?lm?yor: 58 CE kurulumunda Grek?e konu?ulan M?s?r
  n?fusu yok. Kurulum karar? `egypt_helleno_egyptian_population` g?revinde.
- **Fetihlerin kendisi** (Roma → Arap dönemi devlet değişimleri): devlet
  katmanı; bu pilot pop dönüşümüne odaklanır (kalite kuralı 3).

## 4. Localization anahtarları

Mevcut dosyalara eklenir:
`Extended Timeline/in_game/localization/english/et_culture_events_l_english.yml`
ve `.../turkish/et_culture_events_l_turkish.yml`.

| Anahtar kalıbı | İçerik |
|---|---|
| `et_culture.N.title` | Olay başlığı |
| `et_culture.N.desc` | Gövde metni (dönemin dili, 2-4 cümle) |
| `et_culture.N.historical_info` | Kaynak özeti + kayıt kimliği referansı |
| `et_culture.N.a` / `.b` | Seçenek adları (tarihsel / direniş) |
| `et_culture.N.a.tt` / `.b.tt` | `custom_tooltip` etki özetleri |

Taslak başlıklar (EN/TR): .1 "A New Dawn on the Nile" / "Nil'de Yeni Bir
Şafak" · .2 "The Coptic Identity" / "Kıptî Kimliği" · .3 "The Years of the
Dhimma" / "Zimmi Yılları" · .4 "Ten to One" / "On Kala Bir" · .5 "The Quiet
Language Shift" / "Dilin Sessiz Değişimi".

`et_culture.9000` test olayı ve loc anahtarları, zincir oyun içi doğrulamayı
geçtikten sonra kaldırılır.

## 5. Test planı

- **Aşama A — şablon doğrulaması (kullanıcı):** ✓ **17 Ekim 2026'da geçti.**
  Kanıt: 58 başlangıcı ROM oyununda test olayı `et_culture.9000` **ve** Galya
  olayı `et_culture.101` ateşlendi (ortak iskelet: events dosyası + loc + DHE
  penceresi). Aynı oturumun `error.log`'unda (`logs/error.log`, 477 KB,
  17 Ekim 19:38) modumuza ait **tek satır yok**. Not: BOM uyarıları
  `debug.log`'a yazılıyor; aynı turda 57 mod dosyasına eksik BOM eklendi.
- **Aşama B — zincir doğrulaması (sıradaki; console protokolü hazır):** EU5
  console komut listesi doğrulandı (wiki 1.3): `event`, `test_event_trigger`,
  `event_probabilities` (yearly_country_pulse dökümü), `change_date`,
  `tick_day`, `Log.ClearErrorLog`. Geçici pencere yaması gereksizleşti.
  Tek oturumluk koşum takımı: `2026-10-19_test_b_protocol.md`.
  Protokol:
  1. Kaydet; `Log.ClearErrorLog`; `event_probabilities yearly_country_pulse`
     → `error.log`'da `et_egypt_yearly_pulse` dökümü (kanca kanıtı).
  2. Pencere mantığı: 58'de `test_event_trigger et_culture.1` (beklenen:
     FAIL, yıl < 200) → `change_date 250` → tekrar (beklenen: PASS).
  3. Doğal ateşleme: 250'de yıl sınırını geçir (`tick_day`; gerekirse hız
     5'te oynat) → `.1` popup → **tarihsel** (`christ_1`); ardından
     `test_event_trigger et_culture.1` FAIL (immediate işaretçi —
     tekilleştirme kanıtı).
  4. `change_date 350`: `.2` doğal ateşlenir → **tarihsel** (`coptic`;
     `old_egyptian`+`miaphysite` → `coptic_culture` panoda doğrulanır).
     Ara kaydet/yükle: değişken kalıcılığı.
  5. Sahip-kapısı: ROM pagan; `test_event_trigger et_culture.3` FAIL (muslim
     grubu yok). Etkiler `event et_culture.3` ile zorlanır (**tarihsel**;
     `islam_1`). Opsiyonel güçlü kanıt: console `religion islam` → `.3`
     trigger'ı PASS (test kaydında; sonra geri alınır).
  6. `change_date 1100` → `.4` **doğal** (islam_1 + pencere) → **tarihsel**
     (`islam_2`); `change_date 1200` → `.5` **doğal** → **tarihsel**
     (`arabized`). Kapanış: `event_probabilities` tekrarı (`.1`–`.5`
     değillenmiş görünür), `error.log` temiz, panoda nihai görünüm (islam
     çoğunluk + Kıptî azınlık + Mısır kültürleri).
- **Aşama C — hızlandırılmış uzun gözlem (opsiyonel):** 58→700; Mısır
  panosunda kademeli değişim; başkaca ülkelerde yan etki yok; performans
  notu (yıllık pulse + bölgesel `every_pop` sınırlı — kalite kuralı 6).
- **Kabul kriterleri:** 5 olay ateşlenir; din ve kültür zincirleri hedeflenen
  yönlerde ilerler; direniş dalı zinciri durdurur; hiçbir seçenek sessizce
  zorlanmaz; localization görünür; log temiz.

## 6. Uygulama dosya planı (iş sırası)

1. **YENİ** `Extended Timeline/in_game/common/on_action/et_history_pulses.txt`
   (bölüm 2.3 iskeleti).
2. **GÜNCELLE** `Extended Timeline/in_game/events/et_culture_events.txt` —
   `et_culture.1`–`.5` (+ onaylanırsa `.6`–`.7`).
3. **GÜNCELLE** localization EN/TR (bölüm 4).
4. Test A → Test B → (gerekirse kalibrasyon) → Test C.
5. Zincir doğrulanınca `et_culture.9000` emekli; README/backlog senkronu.

**Durum:** 1?3 ? (17 Ekim 2026). 4: Test A ?; Test B ko?um tak?m? haz?r
(`2026-10-19_test_b_protocol.md`), ko?um s?rada. 5: Test B ge?ince (9000 emeklili?i + kay?t senkronu).
6: 20 Ekim 2026 ? N?bya eki (`.6`?`.8`), M?sl?man dengeleme dalgas? (`.9`), kay?t
status konvansiyonu ve 58 CE kurulum onar?m? (biti? durumu `upper_egyptian_culture`
s?z?nt?s? + kopyalanm?? pop bloklar?) tamamland?; b?l?m 7'deki 1?5 numaral?
kararlar kapand?.

Numara rezervasyonu (Samet ile mutabakat — **sağlandı**): Mısır `.1`–`.49`,
Galya `.100`–`.149` (Galya `.101`–`.103` yürürlükte), sonraki bölgeler `.150`+.

## 7. Açık kararlar (maintainer)

1. **Fetih derecesi ? KAPANDI (20 Ekim 2026):** Ko?ullu pencereler + sahiplik
   ko?ulu; fetihler ve M?sl?man egemenli?in olu?mas? **zorlanmaz**. Gerek?e:
   `.3`teki `religion.group = religion_group:muslim` kap?s? bilin?li bir sahip
   ko?uludur (tasar?m notu b?l?m 3, `.3`); zincirin ilgili dal? o sahip
   belirmedi?inde hi? ate?lenmez, diverjinans bilin?li bir tercihtir. Ayn?
   mant?k Galya zincirinde de ge?erlidir (DHE band?: yaln?zca ROM/FRAN/FRA).
2. **Oyuncu se?ene?i deseni ? KAPANDI (20 Ekim 2026):** Her olayda tarihsel +
   direni?; direni? dal? zincir de?i?kenini **yazmaz**, b?ylece sonraki olay
   tetiklenmez ve zincir orada durur (M?s?r'da ayn? desen; N?bya'da da ayn?
   uygulama, okunmayan `_resist` de?i?keni b?rak?lmad?). AI tarihsel se?ene?i
   oynar.
3. **N?bya eki ? KAPANDI (20 Ekim 2026):** Faz 1'e al?nd? ve uyguland?
   (`.6`/`.7`/`.8` + `et_nubia_yearly_pulse`); ?nc?l do?rulamas? yap?ld? (b?l?m 3,
   N?bya eki).
4. **Oran kalibrasyonu ? KAPANDI (20 Ekim 2026), paylar test verisiyle:** 58 CE
   kurulumundan statik hesap yap?ld?: mevcut dalgalar 1:3,2 veriyor, hedef 10:1;
   bu y?zden Meml?k dalgas? `et_culture.9` (1300?1500, 0,65 / 0,55) eklendi ve
   tahmini oran ? 1:9,7'ye ??k?yor. **A??k paylar kalibrasyon d??mesidir:**
   Test B pano okumas? farkl? sonu? verirse yaln?zca `.9`un iki say?s? de?i?ir,
   zincirin yap?s? de?i?mez.
5. **Hellno kayd? ? KAYNAK KAPANDI (20 Ekim 2026), script kurulum karar?
   bekliyor:** ?ki akademik kaynak eklendi (Papaconstantinou 2012, Cromwell 2021);
   g?ven art? `low` ? `medium`, tarihlendirme `c. 700-1100` ? `c. 650-800`
   (Grek?e topluluk dili olarak 7.-8. y?zy?lda geriliyor; sonras?nda ayin ve
   maliye dili olarak s?r?p kal?yor). Olay yine yaz?lm?yor: 58 CE kurulumunda
   Grek?e konu?ulan M?s?r n?fusu **yok** (`06_pops.txt`te 0 `helleno_egyptian`;
   M?s?r `old_egyptian` + Yahudi az?nl?k). Kurulum karar?
   `egypt_helleno_egyptian_population` g?revinde.
6. ~~Galya numaralandırma mutabakatı~~ **sağlandı** (17 Ekim 2026): Samet
   Galya olaylarını `.101`–`.103`'e taşıdı; Mısır `.1`–`.49`, Galya
   `.100`–`.149` fiilen yürürlükte.

7. **Mısır anahtarlarının mod sahipliği — KARAR VERİLDİ (17 Ekim 2026, ikinci
   inceleme; oyunun bekası önceliği):** Samet'in `f3d304d` ile mod'a aldığı kopyalar
   tek tek denetlendi. Modun yerleşik implicit-override deseni (dosya adları
   vanilla'dan sonra sıralanır; `REPLACE:` yok) gereği bu kopyalar vanilla içeriğini
   gölgeleyebiliyordu. **Deltası olmayan, yalnız içerik kaybettiren kopyalar geri
   alındı:** `arabic_language` (7 diyalekt — modun kendi `et_muslim` dini ve ~30
   vanilla kültür satırı referans veriyor — ve isim listeleri), `coptic_language`
   (isim listeleri), `lower/upper_egyptian_culture` (`opinions`,
   `goods_demand_modifier`, geçerli gfx tag'leri) ve `miaphysite`'ın sadeleştirilmiş
   hali (otosefal patrikhane, kanonizasyon, `religious_aspects = 3`). **Gerçek
   deltalar vanilla birebir + delta olarak kaldı:** `coptic_culture` = vanilla içerik
   + `culture_groups = { arabic_group }` (vanilla Koptî'yi grubusuz bırakıyor;
   zincirde Koptî→Mısır kimlik geçişi aynı grupta yürür) ve `miaphysite` = vanilla
   blok + `language = coptic_language`. Yeni kopyaların başındaki yorumlar kaynağı ve
   senkron sorumluluğunu belirtir; her iki override semantiğinde de güvenli (kopyalar
   birebir, deltalar açık). Geri alınan bloklardaki geçersiz culture tag'leri
   (`middle_eastern_gfx`, `arabic_gfx`) böylece düştü; `helleno_egyptian`
   (`et_egypt.txt:35`) ve `et_missing` kalanları `invalid_culture_gfx_tags` görevinde.
8. **`.5` direniş senkronu — ÇÖZÜLDÜ (17 Ekim 2026):** Script spec'e geri alındı:
   direniş Delta `0.25` / Yukarı Mısır `0.15` (kuzey-güney gradyanı spec'teki gibi).
   Not ve script senkron; bölüm 3 uygulama notu güncel.

## 8. İzlenebilirlik: kayıt → olay

| Kayıt | Olay | Durum |
|---|---|---|
| `egypt_58ce_population_baseline` | (zincirin başlangıç varsayımı) | applied (zaten) |
| `egypt_christianization_rise` | `et_culture.1` | planlandı |
| `egypt_coptic_emergence_and_continuity` | `et_culture.2` | planlandı |
| `egypt_chalcedon_split_451` | `.1`/`.2` metin (`historical_info`); doğrudan pop etkisi yok | metin düzeyi |
| `egypt_arab_conquest_639_642` | zorlanmaz — devlet katmanı (Faz 3 fetih politikası) | kapsam dışı |
| `egypt_arabic_administration_700` | `.5` kademesi ("şehirler önce") + metin | planlandı |
| `egypt_islamization_waves` | `.3` + `.4` | planlandı |
| `egypt_coptic_spoken_decline` | `.5` | planlandı |
| `egypt_helleno_egyptian_absorption` | — (kaynak zayıf) | bekliyor |
| `kush_meroe_collapse_and_nubian_successors` | `.6` (ek) | öneri |
| `nubia_christianization_543` | `.7` (ek) | öneri |

Scriptler yazılıp test geçince ilgili kayıtların `integration.status` alanları
`pending → applied`'a çekilir (hedef dosya: `events/et_culture_events.txt` +
`on_action/et_history_pulses.txt`).

## 9. Kanıt dizini (vanilla 1.3.x)

- `in_game/common/on_action/country_yearly.txt:894-914` — dar koşullu
  alt-pulse desenleri (`owns = location:X`, `location:X = { owner = ROOT }`).
- `country_yearly.txt:926-940` — `current_year` koşulu; ülke kapsamında
  `religion.group = religion_group:christian` kullanımı.
- `in_game/events/DHE/flavor_MAM.txt:2606-2688` — Kıptî dönüşümü deseni:
  bölge kapsamı, `split_pop fraction`, estate etkileri, `has_variable`.
- `flavor_MAM.txt:2702-2707` — `set_variable = { name = ... }` (süreli).
- `in_game/events/DHE/flavor_BYZ.txt:1934` — `split_pop ... culture`.
- `in_game/events/debug/000_johan_debug.txt:1190-1194` — `split_pop` +
  `type = pop_type:clergy`; `:1185-1196` lokasyon kapsamı.
- `in_game/map_data/definitions.txt:5337-5352` — Mısır alt/üst bölge ve
  lokasyon anahtarları.
- `in_game/common/religions/christian.txt:365-399` — `miaphysite`
  (`enable` yok → 58'den itibaren).
- EU5 Wiki, "On action" — modlama kuralı: mevcut on action'a yalnız yeni
  `on_actions` bloğu eklenir.
- Tarama sonuçları (yerel): DHE blokları 3235/3235 `tag`li; `split_pop`
  221 kullanım (frekans dağılımı: fraction 219 / religion 206 / culture 17 /
  type 15); `on_action` klasöründe 206 isim, dosyalar arası çift tanım yok.
