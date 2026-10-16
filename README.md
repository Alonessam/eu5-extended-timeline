# 🌍 Europa Universalis V: Extended Timeline — Historical Overhaul & Turkish Localization

Bu proje, **Europa Universalis V (EU5)** için **M.S. 58 (58 AD)** başlangıç tarihinden itibaren Antik Çağ ve sonrası dünyayı tarihsel gerçekliğe uygun şekilde yeniden inşa eden kapsamlı bir **Tarihsel Revizyon (Historical Overhaul)** ve **%100 Türkçe Yerelleştirme** projesidir.

---

## ✨ Neler Yapıldı / Öne Çıkan Özellikler

### 1. 🏛️ Kapsamlı M.S. 58 (58 AD) Din ve Demografi Revizyonu
- **Anakronik İnançların Temizlenmesi:** Haritada 1337 yılından kalma tüm Orta Çağ ve sonrası inançlar (*Katolik, Ortodoks, Sünni, Şii, Nesturilik, Yezidilik, Maniheizm, Katarlık, Valdenslik, Bosna Kilisesi, Pavlikanlık, Dürzilik, Tibet Budizmi*) tamamen temizlenerek M.S. 1. yüzyıl gerçekliğine dönüştürüldü.
- **Bölgesel Tarihsel Doğrulama (5.206 Pop Bloğu & 1.642 Lokasyon):**
  - **Cermanya:** Sahte Roma paganizmi ve Güney Asya atamaları temizlendi; Cermen kabileleri (*Cherusci, Hermunduri, Alamanni, Saxons vb.*) gerçek `germanic_polytheism` inancına ve Cermen kabile kültürlerine kavuşturuldu.
  - **Daçya (`DACI`):** Anakronik Slav kültürü ve Slav paganizmi kaldırılarak, Daçya Krallığı toprakları tarihsel `dacian` kültürü ve `zamolxism` (Zalmoksis) inancıyla güncellendi.
  - **İrlanda & Britanya:** Kelt kabileleri `druidism` ve `brythonic_polytheism` inancına döndürüldü.
  - **Kuzey Afrika & Sahra:** Oyuna yeni **`berber_polytheism` (Berberi Çoktanrıcılığı)** dini eklendi; Garamantlar (`GARA`), Gaetulyalılar (`GAET`) ve Mauri (`MOOR`) kabilelerine tanımlandı.
  - **Afrika Boynuzu & Nubya:** Somali, Afar ve Agav halkları Kuşitik `waaqeffanna_religion` inancına; Nubya ve Beja kabileleri ise `egyptian_polytheism` (Amon/Apedemak) inancına bağlandı.

### 2. 👑 Antik Yönetim Şablonları, Savaşlar ve Diplomasi
- **Yeni Hükümet Şablonları:**
  - `et_chinese_monarchy` (Han Hanedanı merkezi bürokratik imparatorluk modeli)
  - `et_indian_monarchy` (Kuşan, Satavahana ve Tamil krallıkları için Dharmik monarşi)
  - `et_nomadic_horde` (Hiung-nu, Sarmatlar ve Alanlar için bozkır göçebe konfederasyonu)
  - `et_tribal_federation` (Cermen ve Kelt kabile federasyonları)
  - `et_ancient_republic` (Akdeniz antik cumhuriyetleri)
- **M.S. 58 Roma-Part Savaşı (`16_wars.txt`):** İmparator Nero dönemi Roma İmparatorluğu (`ROM`) ile I. Vologases yönetimindeki Part İmparatorluğu (`PRTH`) ve Ermenistan (`ARM`) arasındaki tarihsel savaş eklendi.
- **Motor Kararlılığı:** 58 AD başlangıç tarihinde yaşanan `divide-by-zero` (sıfıra bölme) çökme hatası ve eksik başlangıç dosyaları (`04_dynasties.txt` - `27_armies.txt`) tamamen onarıldı.

### 3. 🇹🇷 %100 Türkçe Yerelleştirme Paketi
- 18 dil dosyası ve **33.790 çeviri anahtarından** oluşan, `UTF-8 with BOM` standardında eksiksiz Türkçe ve İngilizce yerelleştirme paketi inşa edildi.
- Tüm ülke adları, sıfatları, antik kültürler, diller, dinler ve bölgeler Türkçeye kazandırıldı; ekranda `_` ile görünen bozuk metinler tamamen giderildi.

---

## 🛠️ Kurulum (Geliştiriciler ve Oyuncular İçin)

1. Depoyu bilgisayarınıza klonlayın:
   ```powershell
   git clone https://github.com/Alonessam/eu5-extended-timeline.git "$env:USERPROFILE\Desktop\Eu5 mod"
   ```
2. Modu oyuna doğrudan bağlamak için PowerShell'i **Yönetici Olarak** açıp aşağıdaki sembolik bağlantı (Junction) komutunu çalıştırın:
   ```powershell
   cmd /c mklink /J "$env:USERPROFILE\Documents\Paradox Interactive\Europa Universalis V\mod\Extended Timeline" "$env:USERPROFILE\Desktop\Eu5 mod\Extended Timeline"
   ```

---

## 🤝 Atıf ve Teşekkür (Credits & Attribution)

- **Geliştirme ve Tarihsel Revizyon Ekibi:** [Alonessam (Samet Furkan Bülüç)](https://github.com/Alonessam) & Ekip Arkadaşları
- **Orijinal Altyapı Teşekkürü (Base Mod Credit):** Bu proje, [Extended Timeline](https://github.com/Extended-Timeline/Extended-Timeline-EU5) ekibinin EU4/EU5 için oluşturduğu temel harita ve ülke çatısı üzerine inşa edilmiş bağımsız bir tarihsel revizyon (Overhaul) ve Türkçe uyarlama çalışmasıdır. Temel mod altyapısı için orijinal Extended Timeline geliştiricilerine teşekkür ederiz.
