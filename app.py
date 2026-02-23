import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import os
import datetime

st.set_page_config(
    page_title="Executive Dashboard V2.2",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- AYDINLIK KURUMSAL (Web Sitesi) CSS TASARIMI ---
st.markdown("""
<style>
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #0f172a;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Kurumsal KPI Kart Tasarımı */
    .corp-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: left;
        margin-bottom: 20px;
        transition: all 0.2s ease;
    }
    .corp-card:hover { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }

    .kpi-title {
        color: #64748b;
        font-size: 0.90rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    .kpi-value {
        color: #0f172a;
        font-size: 2.5rem;
        font-weight: 800;
    }
    
    .kpi-trend { font-size: 0.9rem; margin-top: 8px; font-weight: 500;}
    .trend-up { color: #10b981;  background-color:#d1fae5; padding: 2px 6px; border-radius: 4px; }
    .trend-down { color: #ef4444; background-color:#fee2e2; padding: 2px 6px; border-radius: 4px; }
    
    .corp-header {
        font-size: 2.2rem;
        font-weight: 900;
        color: #1e293b;
        margin-bottom: 0px;
        padding-bottom: 5px;
    }
    .corp-subheader {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 30px;
        font-weight: 400;
    }
    
    /* Canlı Akış Container'ı (Hafif gri) */
    .feed-container {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        height: 400px;
        overflow-y: auto;
    }
    .feed-item {
        border-left: 4px solid #3b82f6;
        padding-left: 15px;
        margin-bottom: 15px;
        padding-bottom: 15px;
        border-bottom: 1px solid #f1f5f9;
        background-color: #f8fafc;
        border-radius: 4px;
        padding-top: 5px;
        padding-right: 5px;
    }
    .feed-time { font-size: 0.8rem; color: #64748b; font-weight: 600;}
    .feed-desc { font-size: 1.05rem; color: #1e293b; font-weight: 600; margin-top: 4px;}
    .feed-price { font-size: 1rem; color: #10b981; font-weight: 700; float: right;}
    
    /* Streamlit Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 4px 4px 0px 0px;
        background-color: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-bottom: none;
        padding: 0px 20px;
        color: #475569;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        color: #2563eb;
        border-top: 3px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# 2. Canlı Yenileme 
st_autorefresh(interval=8 * 1000, key="ecommerce_v22_refresh")

CSV_FILE = 'data/ecommerce_sales_data.csv'

@st.cache_data(ttl=2)
def load_live_data():
    try:
        df = pd.read_csv(CSV_FILE)
        df['Sipariş Tarihi'] = pd.to_datetime(df['Sipariş Tarihi'], format='mixed')
        
        # Karlılık oranlarını tekrar hesaplayalım (Ham veri sadece fiyat içeriyordu)
        margin_rates = {'Elektronik': 0.15, 'Giyim': 0.40, 'Ev & Yaşam': 0.25, 'Spor': 0.30}
        df['Karlılık Oranı'] = df['Kategori'].map(margin_rates)
        df['Net Kâr'] = df['Toplam Tutar'] * df['Karlılık Oranı']
        df['Satış Saati'] = df['Sipariş Tarihi'].dt.hour
        
        return df, None
    except Exception as e:
        return pd.DataFrame(), str(e)

df, err_msg = load_live_data()

st.markdown('<div class="corp-header">💼 İş Zekası Yönetim Paneli V2.2</div>', unsafe_allow_html=True)
st.markdown('<div class="corp-subheader">Gerçek Zamanlı E-Ticaret Performansı, Kâr Analizi ve Müşteri Eğilimleri</div>', unsafe_allow_html=True)

if df.empty:
    st.error(f"E-Ticaret Verisi Okunamadı. Hata: {err_msg}")
    st.stop()


# ---------------- KPI (TEPE VERİLERİ) ----------------
# Dinamik filtreme için referans tarihleri
last_date = df['Sipariş Tarihi'].max().date()
yesterday = last_date - datetime.timedelta(days=1)

# Bugün (Son Gün) ve Dün filtreleri
df_today = df[df['Sipariş Tarihi'].dt.date == last_date]
df_yesterday = df[df['Sipariş Tarihi'].dt.date == yesterday]

def calculate_delta(current, previous):
    if previous == 0: return 0
    return ((current - previous) / previous) * 100

# 1. Metrik: Ciro
today_rev = df_today['Toplam Tutar'].sum()
yesterday_rev = df_yesterday['Toplam Tutar'].sum()
rev_delta = calculate_delta(today_rev, yesterday_rev)

# 2. Metrik: Kâr
today_profit = df_today['Net Kâr'].sum()
yesterday_profit = df_yesterday['Net Kâr'].sum()
prof_delta = calculate_delta(today_profit, yesterday_profit)

# 3. Metrik: Sipariş
today_ord = len(df_today)
yesterday_ord = len(df_yesterday)
ord_delta = calculate_delta(today_ord, yesterday_ord)

# 4. Metrik: AOV (Ortalama Sepet)
today_aov = today_rev / today_ord if today_ord > 0 else 0
yesterday_aov = yesterday_rev / yesterday_ord if yesterday_ord > 0 else 0
aov_delta = calculate_delta(today_aov, yesterday_aov)

col1, col2, col3, col4 = st.columns(4)

def kpi_card(col, title, value, delta, prefix="₺", suffix=""):
    trend_class = "trend-up" if delta >= 0 else "trend-down"
    arrow = "↑" if delta >= 0 else "↓"
    with col:
        st.markdown(f"""
        <div class="corp-card">
            <div class="kpi-title">{title} (BUGÜN)</div>
            <div class="kpi-value">{prefix}{value:,.0f}{suffix}</div>
            <div class="kpi-trend"><span class="{trend_class}">{arrow} %{abs(delta):.1f} (Düne Göre)</span></div>
        </div>
        """, unsafe_allow_html=True)

kpi_card(col1, "BRÜT CİRO", today_rev, rev_delta)
kpi_card(col2, "NET KÂR (MARJ)", today_profit, prof_delta)
kpi_card(col3, "SİPARİŞ GEÇİŞİ", today_ord, ord_delta, prefix="", suffix=" Adet")
kpi_card(col4, "AOV (SEP. TUT.)", today_aov, aov_delta)


# ---------------- SEKME (TABS) YAPISI ----------------
tab1, tab2, tab3 = st.tabs(["📈 Büyüme ve Genel Özet", "💰 Kârlılık ve Sepet Analizi", "⏱️ Canlı Operasyon Merkezi"])

# -- TAB 1: BÜYÜME VE GENEL ÖZET --
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([6,4])
    
    with c1:
        st.markdown("##### 🚀 Kategori Bazlı Büyüme (Satış Hacmi)")
        cat_df = df_today.groupby('Kategori')['Toplam Tutar'].sum().reset_index().sort_values(by='Toplam Tutar', ascending=True)
        fig_cat = px.bar(cat_df, y='Kategori', x='Toplam Tutar', orientation='h', text_auto='.2s', 
                         color='Toplam Tutar', color_continuous_scale='Blues')
        fig_cat.update_layout(plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0), font=dict(family="Inter", color="#475569"))
        st.plotly_chart(fig_cat, use_container_width=True)

    with c2:
        st.markdown("##### 🏆 Günün Trend Ürünleri (Top 5)")
        top_products = df_today.groupby('Ürün').agg({'Toplam Tutar':'sum', 'Birim Fiyat':'count'}).reset_index()
        top_products.columns = ['Ürün', 'Ciro (₺)', 'Satış Adedi']
        top_products = top_products.sort_values(by='Ciro (₺)', ascending=False).head(5)
        st.dataframe(top_products, use_container_width=True, hide_index=True)


# -- TAB 2: KARLILIK ANALİZİ --
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    t2_c1, t2_c2 = st.columns(2)
    
    with t2_c1:
        st.markdown("##### ⚖️ Ciro vs Net Kâr Değerlendirmesi (Kategorik)")
        profit_cat = df.groupby('Kategori')[['Toplam Tutar', 'Net Kâr']].sum().reset_index()
        fig_prof = go.Figure()
        fig_prof.add_trace(go.Bar(x=profit_cat['Kategori'], y=profit_cat['Toplam Tutar'], name='Brüt Ciro', marker_color='#cbd5e1'))
        fig_prof.add_trace(go.Bar(x=profit_cat['Kategori'], y=profit_cat['Net Kâr'], name='Net Kâr', marker_color='#3b82f6'))
        fig_prof.update_layout(barmode='group', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Inter", color="#475569"))
        st.plotly_chart(fig_prof, use_container_width=True)
        
    with t2_c2:
        st.markdown("##### 🗺️ Bölgesel Net Kâr (Isı Alanı)")
        reg_prof = df.groupby('Bölge')['Net Kâr'].sum().reset_index()
        fig_reg = px.pie(reg_prof, values='Net Kâr', names='Bölge', hole=0.5, color_discrete_sequence=px.colors.sequential.Blues_r)
        fig_reg.update_traces(textposition='inside', textinfo='percent+label')
        fig_reg.update_layout(margin=dict(t=0, b=0))
        st.plotly_chart(fig_reg, use_container_width=True)


# -- TAB 3: CANLI OPERASYON MERKEZİ (BOT İZLEME) --
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    t3_c1, t3_c2 = st.columns([7, 3])
    
    with t3_c1:
        st.markdown("##### 🕒 Günlük Sipariş Yoğunluğu (Saatlik Heatmap Analizi)")
        # Sadece bugünün verisinde saatlik siparişleri grupla
        hourly_df = df_today.groupby('Satış Saati')['Sipariş ID'].count().reset_index()
        hourly_df.columns = ['Saat (0-24)', 'Sipariş Adedi']
        
        # Eğer henüz o saatte işlem yoksa 0 yazsın
        all_hours = pd.DataFrame({'Saat (0-24)': range(0, 24)})
        hourly_df = pd.merge(all_hours, hourly_df, on='Saat (0-24)', how='left').fillna(0)
        
        fig_hour = px.line(hourly_df, x='Saat (0-24)', y='Sipariş Adedi', markers=True, 
                          line_shape='spline')
        fig_hour.update_traces(line=dict(color='#2563eb', width=3), fillcolor='rgba(37, 99, 235, 0.1)', fill='tozeroy')
        fig_hour.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(tickmode='linear', tick0=0, dtick=1))
        st.plotly_chart(fig_hour, use_container_width=True)

    with t3_c2:
        st.markdown("##### ⚡ Canlı Sisteme Düşen Siparişler")
        st.markdown("<div class='feed-container'>", unsafe_allow_html=True)
        
        latest_orders = df.sort_values(by='Sipariş Tarihi', ascending=False).head(15)
        for i, row in latest_orders.iterrows():
            t = row['Sipariş Tarihi'].strftime("%H:%M:%S")
            cat = row['Kategori']
            prod = row['Ürün']
            price = row['Toplam Tutar']
            reg = row['Bölge']
            
            icon = "🛒"
            if cat == "Elektronik": icon = "💻"
            elif cat == "Giyim": icon = "👔"
            elif cat == "Spor": icon = "⚽"
            elif cat == "Ev & Yaşam": icon = "🛋️"
            
            feed_html = f"""
            <div class="feed-item">
                <span class="feed-price">₺{price:,.2f}</span>
                <div class="feed-time">{t} - {reg}</div>
                <div class="feed-desc">{icon} {prod}</div>
            </div>
            """
            st.markdown(feed_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
