# 58 CE Ekonomi Katmanı: Kapsam, Yöntem ve Yol Ağı Kanıtı — 20 Ekim 2026

`ancient_economy_roads_and_town_ranks` (batch 2) ve `geographic_coverage`
görevleri için tek bir kapsam kararı. Amaç: 58 CE ekonomi katmanının ikinci
dilimini (yol komşulukları + kasaba sıralaması) ve coğrafi genişletmeyi
tanımlı, kanıtla sınırlı ve tekrarlanabilir hâle getirmek.

## 1. Konum dosyası biçimi (docs/Location Files.md)

- `roads:` — komşu konum kimlikleri listesi (`location_id: yes`). Bir yönü
  yazmak yeterlidir; karşılıklı yazıma gerek yoktur.
- `city:` — `rank` (none / town / city) ve `setup` (vanilla `town_setup`
  anahtarı). `setup` yalnızca `in_game/common/town_setups` içinde tanımlı bir
  değer olabilir; 58 CE şehir dosyasında kullanılan 38 değerin 38'i de
  vanilla'da tanımlı (20 Ekim denetimi).
- `market: yes` — pazar bayrağı.

## 2. 58 CE'de kanıtla desteklenen yol ağları

| Ağ | Kapsam | Dayanak |
|---|---|---|
| Roma sistemi | Via Domitia (118 BC), Via Aquitania (118 BC), Via Appia, Via Flaminia, Via Egnatia, Via Militaris, Britannia'da Watling Street / Fosse Way / Ermine Street, İberya'da Via de la Plata | Kent kayıtlarının kendi makaleleri; yol tarihleri açık |
| Pers Kral Yolu | Susa'dan Susa'ya kadar başkent, 80 günlük mesafe; Ktesiphon-Susa ekseni | Han dönemi ve Roma-Parça kaynakları |
| Han koridoru | Hexi Koridoru yolu, "Batı Bölgeleri" yolu (Zhang Qian sonrası), devlet yol sistemi | Çin kaynakları |
| Hindistan | Uttarapatha (Taxila-Kusinagara-Pataliputra ekseni), Deccan yolları | Hint kaynakları |
| Nil ve Kızıl Deniz | Nil vadisi yolu, deniz kıyı limanları (Alexandria, Myos Hormos, Berenike) | Mısır kaynakları |
| Trans-Sahara | Garamantian kervan rotası (MS 1. yüzyıldan itibaren) | Plinyus / Plutarkos aktarımları |

## 3. Açıkça dışlanan ağlar (ve nedeni)

- **Amerika**: 58 CE'de tekerlekli bir yol ağı yok. İnka Qhapaq Ñan 15. yüzyıl,
  Aztek ve Maya platformları ise yol ağı değil kentsel yapıdır. Bu yüzden
  Amerika'da 58 CE yol komşulukları yazılmaz; bu bilinçli bir boşluktur ve
  kayıt notunda belirtilir.
- **Boş step**: kalıcı bir yol ağı yok, sadece güzergâh izleri.
- **Asya'daki ek yollar**: "Kanatlı" hayvan kervanları için kanıt sınırlı;
  ölçülebilir bir komşuluk listesi çıkarılamadığı için yazılmaz.

## 4. Kasaba sıralaması ölçütü

1. Yerleşim bir pazar merkezi ise (`market: yes`) en az bir `town` sıralaması
   alır.
2. Nüfus, dönemin derleme tahmininin (urban-size derlemesi) yerel eşiğinin
   üstündeyse `city` sıralaması alır.
3. `setup` değeri yalnızca vanilla `town_setups` listesinden seçilir; şehrin
   coğrafyası ve çağı temsil eden bir değer seçilir (örn. Akdeniz limanı için
   `greek_city_port`, Orta Asya şehri için `central_asian_city`).
4. Tarihlendirme: 58.2.1 bloğu (batch 1'in kullandığı işaret).

## 5. Bugünkü kapsama sınırı

- **Var olan**: 74 şehir (Avrupa, Akdeniz, Yakın Doğu, Mısır, Han çekirdeği,
  Hindistan'da Patna, Mezoamerika) — kayıt, kaynak ve uygulama tam.
- **Doğrulanmış Doğu Han hükümdar tarihleri**: 20 Ekim'de hükümdar listesi
  eklendi; üç taht çıkış günü ve bir hükümdar kimliği düzeltildi (kayıt:
  `eastern_han_ruler_dates`).
- **Eksik**: Güney Asya'nın Patna dışındaki şehirleri, Sahra'n ötesindeki
  Afrika şehirleri (Mero/Nubia dışında), Amerika'daki Maya/Teotihuacan kentleri
  ve oyun haritasındaki diğer yerleşim konumları.
- **Sonraki dilimin adımları** (her konum için): (a) derlemedeki satırı bul,
  (b) `city: {rank, setup}` + `market` yaz, (c) 58.2.1 bloğunu güncelle,
  (d) yol komşuluklarını kanıtlanan ağın güzergâhına göre yaz, (e) kaydı
  `et-history-data/research/ancient/` altına ekle ve konum dosyasını doğrula.

## 6. Uygulama notu

Bu iki görev tek oturumda kapatılamayacak ölçekte veri üretimleridir
(yüzlerce konum, her biri kaynak ve güncelleme gerektirir). Bu not yöntemi ve
sınırları sabitler; kalan iş, aşağıdaki sırayla ilerleyen bir üretim listesidir:
Güney Asya → Sahra ötesi Afrika → Mezoamerika kentleri → haritadaki kalan yerleşim
konumları. Her dilim kendi kaydıyla, `wiki_urban_sizes` satırı ve yol ağı
dayanağıyla gelir.
