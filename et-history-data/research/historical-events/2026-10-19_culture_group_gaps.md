# Kültür Grubu Boşlukları — 19 Ekim 2026

`culture_group_gaps_remaining` görevinin kapanış kaydı. 17 Ekim WS3
denetiminde işaretlenen grupsuz kültürlerin ardıl eşleştirmeleri
tamamlandı; kararlar bakımcı onayıyla uygulandı. Önceki not:
`2026-10-17_culture_graph_audit.md`. Plan: `README.md`.

## Yöntem

- Tarama: `Extended Timeline/in_game/common/cultures/*.txt` içindeki her üst
  düzey kültür bloğunda `culture_groups` alanı denetlendi (eksik veya boş
  işaretlendi).
- Ölçüt (17 Ekim notuyla aynı): antik kültür, ardılının vanilla grubuna
  bağlanır; yalnız vanilla grup kimlikleri kullanılır.
- Kimlik doğrulaması: kültürün kendi dosyası, ülke araştırma kayıtları
  (`et-history-data/countries/`) ve aynı dil ailesindeki gruplu kardeşler.
- Karar noktaları bakımcıya soruldu (pannonian, illyrian, hunnic, fallback
  seti, apache kimliği, jukun, Doğu Asya istisnaları); tümü önerilen hat
  üzerinden onaylandı.

## Uygulanan atamalar

| Kültür | Dosya | Sonra | Gerekçe (vanilla ardıl) |
|---|---|---|---|
| `pannonian` | `et_balkans.txt` | `carpathian_group` | Slovak/Macar ardılları; dosyadaki `dacian`/`thracian` deseni |
| `illyrian` | `et_balkans.txt` | `slavic_group`, `south_slavic_group` | `macedonian` deseni; Arnavut hattının vanilla grubu yok |
| `tocharian` | `et_persian.txt` | `turkic_group` | Turfan/Kuça lokasyonlarında `uyghur_culture` |
| `pyu` | `et_south_east_asia.txt` | `tibeto_burman_group` | Pyu→Bamar hattı; vanilla `burmese_culture` |
| `pear` | `et_south_east_asia.txt` | `austroasiatic_group` | Pearik kolu; vanilla `khmer_culture` |
| `hunnic` | `et_turkic.txt` | `turkic_group`, `steppe_group` | Bulgar/Kazar ardıl hattı + bozkır şemsiyesi (vanilla Tatar deseni) |
| `jukun` | `et_subsaharan.txt` | `volta_niger_group` | Kwararafa; vanilla `benue`/`bantoid` (Benue-Kongo) komşu hattı |
| `apache` | `et_missing.txt` | `nadene_group` | Na-Dene hattı; kültür APA'nın 58 CE Apache yorumunda kullanılıyor |
| `bantu` | `et_missing.txt` | `bantu_group` | MOZA yer tutucusu; vanilla `swahili`/`kongo` |
| `garjati` | `et_missing.txt` | `indian_group`, `indo_aryan_group` | Garjat/Odia; vanilla `orissan`/`halbi` (`oriya_language`) |
| `tepic` | `et_missing.txt` | `yutonahua_group` | Tepic/Xalisco; vanilla `naayeri`/`huichol`/`totorame` hattı |
| `kanek_culture` | `et_missing.txt` | `maya_group` | Itza/Maya; vanilla `yucatec_culture`/`mam_culture` |
| `jinhan` | `east_asia.txt` | `japanese_group` | Aynı dosyadaki `kumaso`/`saeki`/`koshibito` (japanese_language) deseni |
| `yupighyt_culture` | `east_asia.txt` | `yupik_group` | Vanilla Yupik kardeşleri (`chugash`, `kaniag`, `unalaska`, `atka`) |

Bırakılan: `arvanite` (`et_missing.txt`) grupsuz kaldı — Arnavut hattının
vanilla'da grup kimliği yok ve kültür hiçbir setup/pop kaydında
kullanılmıyor; gerekçe bu notta. `et_missing.txt` fallback setinin kalanı
onaylanan politikayla bağlandı.

## 17 Ekim notuna düzeltme

17 Ekim taraması her dosyanın **ilk bloğunu** ayrıştırıcı hatasıyla atlamış:
`et_subsaharan.txt`'in ilk bloğu `jukun` ve `et_turkic.txt`'in ilk bloğu
`hunnic` bu yüzden o notta hiç listelenmemişti ("kalan 37" aslında 39'du).
Aynı hata `et_missing.txt` (`missing_culture`) ve `east_asia.txt`
(`korean_culture`) ilk bloklarında görünmez kaldı çünkü ikisi de grupluydu.
Bu turda iki kayıt da kapatıldı; ilk-blok hatası kalıcı denetime eklenen
"grupsuz kültür" kontrolüyle telafi edildi.

## Bulgular ve sınırlar

- `apache`: kültür yalnız APA ülkesinde kullanılıyor. APA araştırma kaydı
  58 CE'de kültürü ve başkenti Apache yorumuna çeviriyor (`liinabaha`,
  Arizona); vanilla dönemi ise Apalachee (Florida, `apalachee_culture`).
  Etiketin çift kimliği veri katmanında açık kalem olarak duruyor; grup
  seçimi Apache hattını izler, Apalachee popları vanilla kültürünü
  kullanmaya devam eder.
- `jukun` adı vanilla `jukun_culture` (Avustralya, Nyulnyulan) ile
  karışabilir; lokasyon şablonu (`location_templates.txt:26082`) doğru
  anahtarı (`jukun_culture`) kullanıyor — çakışma yok, doğrulandı.
- Doğu Asya kümesi dil-kardeş taramasıyla yeniden denetlendi: 26 kayıttan
  `jinhan` ve `yupighyt_culture` dışındaki 24'ünün dil ailesinde gruplu
  kardeşi yok (ainu, ryukyu, hmong, lamut, çukotko-kamçatka, yukagir ve
  Sibirya kolları); vanilla'da da `ainu_culture` ve `ryukyu_culture`
  grupsuz.
- `tepic` ve `kanek_culture` kullanımları ülke katmanında vanilya dışı
  eşleşmeler taşıyor (MMM/XAL ve Maya popları); grup kararı kültürün kendi
  kimliğinden verildi, bu eşleşmeler ayrı veri kalemidir.

## Doğrulama

- Grupsuz tarama: 39 → 25 (24 Doğu Asya izolesi + `arvanite`); kalanların
  tümü kasıtlı ve gerekçeli.
- Kalıcı denetim genişletildi: `script-token-audit.py` artık mod kültür
  dosyalarındaki grupsuz blokları da tarar; izin listesi bu nottaki 25
  kasıtlı kaydı içerir ve liste dışı yeni bir grupsuz kültür denetimi
  düşürür.
- Tam tarama: 108 dosya, 0 çözülemeyen token.
- `2026-10-19_vanilla_key_shadow_audit.md` din sayısı 482 → 480
  düzeltildi (güncel tarama değeri).

## Sınırlar

- Ardıl eşleştirmeleri bölge, dil hattı ve vanilla kardeş kanıtına dayanır;
  yeni birincil kaynak eklenmedi (bu bir kültür grafiği kararıdır, olay
  kaydı değildir).
- `arvanite` ve Doğu Asya kümesi oyun içi asimilasyon testine girmedi;
  Test B kapsamı dışındadır.
