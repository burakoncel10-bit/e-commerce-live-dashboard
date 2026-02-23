import pandas as pd
import numpy as np
from datetime import datetime
import random
import time
import os

CSV_FILE = 'data/ecommerce_sales_data.csv'

# Kategori ve ürünler aynen (generate_data.py referanslı)
categories = {
    'Elektronik': ['Laptop', 'Akıllı Telefon', 'Kulaklık', 'Monitör', 'Klavye', 'Mouse', 'Tablet', 'Akıllı Saat'],
    'Giyim': ['Tişört', 'Pantolon', 'Ceket', 'Kazak', 'Gömlek', 'Ayakkabı', 'Spor Ayakkabı', 'Mont'],
    'Ev & Yaşam': ['Kahve Makinesi', 'Robot Süpürge', 'Halı', 'Masa', 'Sandalye', 'Lamba', 'Mutfak Robotu'],
    'Spor': ['Dambıl', 'Yoga Matı', 'Koşu Bandı', 'Spor Çantası', 'Bisiklet', 'Kamp Çadırı']
}

regions = ['Marmara', 'Ege', 'İç Anadolu', 'Akdeniz', 'Karadeniz', 'Doğu Anadolu', 'Güneydoğu Anadolu']
payment_methods = ['Kredi Kartı', 'Banka Kartı', 'Havale/EFT', 'Kapıda Ödeme']
return_reasons = ['Beden Uymadı', 'Kusurlu Ürün', 'Vazgeçtim', 'Görselden Farklı', 'Geç Teslimat']

base_prices = {
    'Elektronik': (500, 40000),
    'Giyim': (100, 2000),
    'Ev & Yaşam': (300, 15000),
    'Spor': (100, 10000)
}

def generate_single_order(last_order_id_num):
    """Tek bir rastgele e-ticaret sipariş satırı üretir."""
    order_id = f"ORD-{last_order_id_num + 1}"
    customer_id = f"CUST-{random.randint(1000, 6000)}"
    
    # Şu anki tam zamanlı tarih/saati alıyor, sipariş şu saniyede geldi.
    order_date = datetime.now()
    
    category = random.choice(list(categories.keys()))
    product = random.choice(categories[category])
    
    unit_price = round(random.uniform(base_prices[category][0], base_prices[category][1]), 2)
    quantity = random.randint(1, 4) if category != 'Elektronik' else random.randint(1, 2)
    
    discount = round(random.uniform(0, 0.20), 2) if random.random() > 0.7 else 0.0
    total_price = round((unit_price * quantity) * (1 - discount), 2)
    
    region = random.choices(regions, weights=[0.4, 0.15, 0.15, 0.1, 0.08, 0.07, 0.05])[0]
    payment_method = random.choices(payment_methods, weights=[0.6, 0.2, 0.1, 0.1])[0]
    
    # Ortalama %5 iade varsayalım ancak bu anlık üretildiği için genellikle iade edilmemiş olarak düşer 
    # (iade daha sonradan gelir ama simülasyon için şimdilik false yapalım, %2 ihtimal iade doğsun)
    is_returned = random.random() < 0.02
    return_reason = random.choice(return_reasons) if is_returned else None
    
    rating = random.randint(3, 5) if not is_returned else random.randint(1, 3)
    
    # Veri sözlüğü
    new_data = {
        'Sipariş ID': [order_id],
        'Müşteri ID': [customer_id],
        'Sipariş Tarihi': [order_date.strftime('%Y-%m-%d %H:%M:%S')],
        'Kategori': [category],
        'Ürün': [product],
        'Birim Fiyat': [unit_price],
        'Adet': [quantity],
        'İndirim Oranı': [discount],
        'Toplam Tutar': [total_price],
        'Bölge': [region],
        'Ödeme Yöntemi': [payment_method],
        'İade Durumu': [is_returned],
        'İade Nedeni': [return_reason],
        'Müşteri Puanı': [rating]
    }
    
    return pd.DataFrame(new_data)

def start_bot():
    print("=======================================")
    print("--- CANLI SİPARİŞ SİMÜLATÖRÜ BAŞLATILDI ---")
    print("=======================================")
    print(f"Bağlı Veritabanı (CSV): {CSV_FILE}")
    
    if not os.path.exists(CSV_FILE):
        print("HATA: Ana CSV dosyası bulunamadı. Lütfen önce generate_data.py'yi çalıştırın.")
        return
        
    try:
        while True:
            # 1. Her seferinde dosyayı okuyup en son ID'yi buluyoruz ki sequential gelsin.
            # Performans için sadece son 5 satırı tail ile okuyoruz (pandas ile biraz yorucu olabilir 
            # ancak 15K satırda sorun yaratmaz)
            try:
                # Tüm veriyi bellekte tutmamak daha iyi ama basitlik için okuyoruz
                df = pd.read_csv(CSV_FILE)
                # En son sipariş ID numarasını bul "ORD-12345" -> 12345
                last_id_str = str(df.iloc[-1]['Sipariş ID'])
                last_order_id_num = int(last_id_str.split('-')[1])
                
                # 2. Yeni sipariş üret
                new_order_df = generate_single_order(last_order_id_num)
                
                # 3. CSV dosyasına Append (Ekleme) modunda ekle (header yazmadan)
                new_order_df.to_csv(CSV_FILE, mode='a', header=False, index=False)
                
                # Terminalde güzel bir log görünümü
                time_str = new_order_df.iloc[0]['Sipariş Tarihi']
                price = new_order_df.iloc[0]['Toplam Tutar']
                prod = new_order_df.iloc[0]['Ürün']
                reg = new_order_df.iloc[0]['Bölge']
                cat = new_order_df.iloc[0]['Kategori']
                
                # Giyim vb kategoriye göre ikon atayalım
                icon = "[+]"
                if cat == "Elektronik": icon = "[E]"
                elif cat == "Giyim": icon = "[G]"
                elif cat == "Spor": icon = "[S]"
                elif cat == "Ev & Yaşam": icon = "[Y]"
                
                print(f"[{time_str}] YENİ SİPARİŞ {icon} | {reg: <15} | {prod: <20} | TL {price:,.2f}")
                
            except Exception as e:
                print(f"Beklenmeyen bir hata oluştu: {e}")
            
            # 4. 3 ile 8 saniye rastgele bir süre bekle ve tekrarla (Gerçekçilik için)
            wait_time = random.uniform(3.0, 8.0)
            time.sleep(wait_time)
            
    except KeyboardInterrupt:
        print("\n🛑 Sipariş Simülatörü Durduruldu.")

if __name__ == "__main__":
    start_bot()
