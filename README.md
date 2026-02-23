# 🚀 Live E-Commerce Business Intelligence Dashboard

Bu proje, bir E-Ticaret sitesindeki "Canlı Sipariş Akışını" simüle eden bir **Veri Boru Hattı (Data Pipeline)** ve bu verileri saniyelik olarak işleyip analiz eden modern, C-Level **Kurumsal İş Zekası (BI) arayüzünü** içerir. 

![Dashboard Teaser](https://via.placeholder.com/800x400.png?text=E-Commerce+Live+Dashboard+Preview) <!-- Buraya kendi projenizin tam ekran resmini ekleyebilirsiniz! -->

---

## 💼 Proje Amacı (Business Case)
Geleneksel "statik" veri analizleri yöneticiler için yeterli değildir. Şirketler, şu an sistemlerine ne kadar para aktığını, kâr oranlarını ve siparişlerin "anlık" kırılımını görmek isterler.

Bu projenin çözüm ürettiği temel problemler:
- Ham ciro yerine kategori kâr marjlarına dayalı **Net Kârlılık (Profitability)** hesabını sunmak.
- Düne veya bir önceki döneme kıyasla (Delta) canlı büyüme ivmesini raporlamak.
- Saniyelik verilerden saatlere yayılan **Pik (Yoğunluk) Analizi** ve **Isı Haritaları (Heatmap)** ile operasyonel içgörü yaratmak.
- "Streaming Data" (akan veri) akışında oluşan anlık siparişleri eşzamanlı ve otonom bir arayüzde (SaaS) yöneticilere ulaştırmak.

---

## 🛠️ Kullanılan Teknolojiler ve Mimari

1. **Python `live_ecommerce_bot.py` (Data Engineering)**: Sistem bu script çalışırken rastgele sipariş sepetleri, bölgeler, kategoriler ve saatler belirler; bu veriyi sonsuz bir döngüde ana CSV'ye yükler (Streaming). 
2. **Pandas & NumPy (Data Processing)**: Akan veriler saniyelik okur; tarih/zaman kurguları dönüştürülür, her sektöre özgün kâr marjı (Giyim: %40, Elektronik: %15 vb.) çarpılarak brüt hesabı net kara çevrilir.
3. **Plotly Express (Data Visualization)**: İnteraktif alan çizgileri, Bar tabanlı kâr grafikleri ve dinamik dairesel pasta dilimleri renderlanır.
4. **Streamlit (Frontend/SaaS Presentation)**: Tamamen "Autorefresh (Otonom Yenilenme)" mantığıyla yazılmıştır. Tabs (Sekmeler) mantığı ile kurumsal ve hafif gri tonlu profesyonel "Business UI" tasarımı üzerine oturtulmuştur.

---

## ⚙️ Kendi Bilgisayarınızda (Lokal) Çalıştırma

Projeyi test etmek için aşağıdaki adımları sırayla uygulayın:

**1. Depoyu klonlayıp içine girin:**
```bash
git clone https://github.com/KULLANICI_ADINIZ/ecommerce-live-dashboard.git
cd ecommerce-live-dashboard
```

**2. Kütüphaneleri kurun:**
```bash
pip install -r requirements.txt
```

**3. Arka plan Canlı Sisteminizi (Sipariş Botunu) Başlatın:**
```bash
python live_ecommerce_bot.py
```
*(Konsolda "Yeni sipariş eklendi" logunu göreceksiniz. Bot çalışmaya devam etsin.)*

**4. Yeni Bir Terminal Açıktan Sonra Arayüzü Başlatın:**
```bash
streamlit run app.py
```

Tarayıcınızda otomatik olarak otonom Web Yönetim Paneliniz `localhost:8501` adresinde açılacaktır! 

---

## 📌 Özellikler Kataloğu
- [x] Otonom veri işleme (Streamlit Autorefresh)
- [x] Sekmeli (Tabs) Yönetici Görüntüsü
- [x] Growth (Büyüme) Indikatörleri
- [x] Gerçek Zamanlı Sipariş Konsolu
- [x] Bölge ve Kâr Optimizasyonu Grafikleri

> *B.T tarafından Management Information Systems (MIS) / Data Science Portfolio projesi olarak geliştirilmiştir.*
