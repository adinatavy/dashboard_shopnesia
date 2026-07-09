# =========================
# START OF FILE tugas_dashboard.py
# =========================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Shopnesia Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700;800&display=swap');

    /* Global */
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #F9F6F2;
        color: #2E3710;
    }

    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.1rem;
    }

    /* Header styling (premium forest/moss gradient - extra compact) */
    .dashboard-header {
        background: linear-gradient(135deg, #2E3710 0%, #38470B 50%, #6E8722 100%);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.4rem;
        box-shadow: 0 4px 12px rgba(56, 71, 11, 0.12);
    }
    .dashboard-header h1 {
        color: #F9F6F2;
        font-size: 1.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .dashboard-header p {
        color: #F1D6AB;
        font-size: 0.7rem;
        margin: 0.1rem 0 0 0;
        font-weight: 300;
    }

    /* KPI Cards container styling */
    div[data-testid="element-container"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid rgba(241, 214, 171, 0.6) !important;
        border-radius: 12px !important;
        background-color: #ffffff !important;
        padding: 0.8rem 1.0rem !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.015) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease !important;
    }
    div[data-testid="element-container"] > div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(56, 71, 11, 0.06) !important;
        border-color: #38470B !important;
    }
    .kpi-label {
        color: #A0855B;
        font-size: 0.62rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value-container {
        display: flex;
        align-items: baseline;
        gap: 6px;
    }
    .kpi-badge-up {
        background-color: rgba(93, 112, 42, 0.12);
        color: #5D702A;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
    }
    .kpi-badge-down {
        background-color: rgba(192, 92, 92, 0.12);
        color: #C05C5C;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
    }

    /* AI Insight Box (soft sand tint card - compact) */
    .ai-insight-box {
        background: linear-gradient(135deg, #FAF8F4 0%, #F5F1E8 100%);
        border: 1px solid rgba(241, 214, 171, 0.25);
        border-left: 4px solid #38470B;
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        margin: 0.2rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.01);
    }
    .ai-insight-box h4 {
        color: #38470B;
        font-size: 0.8rem;
        font-weight: 700;
        margin: 0 0 0.2rem 0;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    .ai-insight-box p, .ai-insight-box li {
        color: #2E3710;
        font-size: 0.72rem;
        line-height: 1.3;
    }
    .ai-insight-box ul {
        margin: 0.2rem 0;
        padding-left: 1rem;
    }

    /* Section Headers */
    .section-header {
        color: #2E3710;
        font-size: 0.8rem;
        font-weight: 700;
        padding-bottom: 0.2rem;
        border-bottom: 1.5px solid #F1D6AB;
        margin-bottom: 0.3rem;
    }

    /* Big Highlight Section Header */
    .section-header-hero {
        color: #2E3710;
        font-size: 0.9rem;
        font-weight: 800;
        padding-bottom: 0.2rem;
        border-bottom: 2px solid #38470B;
        margin-bottom: 0.3rem;
    }

    /* Sidebar modern layout */
    section[data-testid="stSidebar"] {
        background-color: #F9F6F2 !important;
        border-right: 1px solid rgba(56, 71, 11, 0.08) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.02) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #2E3710;
    }

    /* Sidebar custom button-navigation styling */
    div[data-testid="stSidebar"] div.stButton {
        margin-bottom: -6px !important;
    }
    div[data-testid="stSidebar"] div.stButton > button {
        background-color: #ffffff !important;
        border: 1px solid rgba(56, 71, 11, 0.12) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        color: #2E3710 !important;
        font-weight: 600 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        height: auto !important;
        font-size: 0.85rem !important;
        width: 100% !important;
    }
    div[data-testid="stSidebar"] div.stButton > button:hover {
        border-color: #38470B !important;
        background-color: #FAF8F4 !important;
        transform: translateY(-2px) translateX(3px) !important;
        box-shadow: 0 4px 12px rgba(56, 71, 11, 0.08) !important;
        color: #38470B !important;
    }
    /* Selected/Active button page style (primary type) */
    div[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #38470B 0%, #2E3710 100%) !important;
        border-color: #38470B !important;
        color: #F9F6F2 !important;
        box-shadow: 0 4px 14px rgba(56, 71, 11, 0.22) !important;
        font-weight: 700 !important;
    }
    div[data-testid="stSidebar"] div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #38470B 0%, #2E3710 100%) !important;
        color: #F9F6F2 !important;
        transform: translateY(-2px) translateX(3px) !important;
        box-shadow: 0 4px 14px rgba(56, 71, 11, 0.22) !important;
    }

    /* Hide default metric styling */
    [data-testid="stMetricValue"] {
        font-size: 0 !important;
    }
    [data-testid="stMetric"] {
        display: none;
    }

    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(56, 71, 11, 0.2), transparent);
        margin: 0.3rem 0;
        border: none;
    }

    /* Plotly Chart adjustments */
    .stPlotlyChart {
        margin-bottom: -0.5rem;
    }

    /* ========================================= */
    /* TAMBAHAN UX BORDER UNTUK FITUR MULTISELECT */
    /* ========================================= */
    /* Kondisi Normal (belum diklik): Border abu-abu/hijau tipis */
    div[data-baseweb="select"] > div {
        border: 1px solid rgba(56, 71, 11, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    
    /* Kondisi Aktif (saat diklik): Border hijau tebal */
    div[data-baseweb="select"] > div:focus-within {
        border: 2px solid #38470B !important;
    }
    /* ========================================= */

</style>
""", unsafe_allow_html=True)

# =========================
# COLOR PALETTE
# =========================
COLORS = {
    "primary": "#38470B",
    "secondary": "#A0855B",
    "accent": "#F1D6AB",
    "success": "#5D702A",
    "danger": "#C05C5C",
    "warning": "#F1D6AB",
    "bg_dark": "#2E3710",
    "text_light": "#F9F6F2",
}

COLOR_SEQUENCE = [
    "#38470B", "#A0855B", "#F1D6AB", "#5E702F",
    "#826A45", "#D1B484", "#8CA052", "#B89C6F",
    "#E8D2AF"
]

PLOTLY_TEMPLATE = "plotly_white"

def format_compact_rp(val):
    if val >= 1e9:
        return f"Rp {val/1e9:.2f} M"
    elif val >= 1e6:
        return f"Rp {val/1e6:.1f} Jt"
    elif val >= 1e3:
        return f"Rp {val/1e3:.0f} Rb"
    return f"Rp {val:.0f}"

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset_bersih.csv")
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["revenue"] = df["final_price"] * df["quantity"]

    bins = [0, 24, 34, 44, 54, 100]
    labels = ["<25", "25-34", "35-44", "45-54", "55+"]
    df["age_group"] = pd.cut(
        df["customer_age"], bins=bins, labels=labels
    )

    df["product_category"] = df["product_category"].replace({
        "Asesoris": "Aksesoris",
        "Aksesories": "Aksesoris",
        "Atasaan": "Atasan"
    })

    # ---- Bersihkan duplikasi / redundansi metode pembayaran ----
    # Sebelumnya pakai exact-match dictionary — masih bisa lolos kalau ada
    # variasi penulisan lain (mis. nama brand e-wallet seperti OVO/GoPay/DANA,
    # atau "Cash on Delivery (COD)"). Sekarang pakai keyword-matching supaya
    # semua varian yang MEREPRESENTASIKAN metode yang sama ikut tergabung,
    # bukan cuma yang teksnya persis sama.
    def normalize_payment(raw):
        s = str(raw).strip().lower()

        # E-Wallet: tulisan umum + nama-nama brand dompet digital populer di Indonesia
        ewallet_keywords = [
            "e-wallet", "ewallet", "e wallet", "e_wallet", "digital wallet",
            "dompet digital", "ovo", "gopay", "go-pay", "go pay", "dana",
            "shopeepay", "shopee pay", "linkaja", "link aja", "sakuku",
            "doku", "jenius pay", "astrapay", "isaku"
        ]
        if any(k in s for k in ewallet_keywords):
            return "E-Wallet"

        # COD: semua variasi "bayar di tempat" / cash on delivery
        cod_keywords = [
            "cod", "cash on delivery", "cash-on-delivery",
            "bayar di tempat", "bayar ditempat", "bayar tempat", "tunai di tempat"
        ]
        if any(k in s for k in cod_keywords):
            return "COD"

        # Kartu Kredit
        if any(k in s for k in ["credit card", "kartu kredit", "kredit"]):
            return "Kartu Kredit"

        # Kartu Debit
        if any(k in s for k in ["debit card", "kartu debit", "debit"]):
            return "Kartu Debit"

        # Transfer Bank
        if any(k in s for k in ["bank transfer", "transfer bank", "va bank", "virtual account", "transfer"]):
            return "Transfer Bank"

        # QRIS
        if "qris" in s:
            return "QRIS"

        # Fallback: rapikan kapitalisasi saja, tidak diubah kategorinya
        return str(raw).strip().title()

    df["payment_method"] = df["payment_method"].apply(normalize_payment)

    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["year"] = df["order_date"].dt.year
    df["day_of_week"] = df["order_date"].dt.day_name()

    return df

df = load_data()

# Helper to generate sparkline data
def get_sparkline_data(df_spark, value_col, date_col="order_date", agg_func="sum"):
    grouped = df_spark.groupby(df_spark[date_col].dt.to_period("W"))
    if agg_func == "sum":
        series = grouped[value_col].sum()
    elif agg_func == "count":
        series = grouped[value_col].count()
    elif agg_func == "nunique":
        series = grouped[value_col].nunique()
    elif agg_func == "mean":
        series = grouped[value_col].mean()
    else:
        series = grouped[value_col].sum()
    
    series.index = series.index.to_timestamp()
    return series

# Initialize session state for navigation
if "active_page" not in st.session_state:
    st.session_state.active_page = "📊 Ringkasan Performa"

with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0px 5px 0px; margin-bottom: 12px; border-bottom: 1px solid rgba(249, 246, 242, 0.15);">
        <h1 style="color: #F9F6F2; font-weight: 900; font-size: 1.6rem; margin: 0; letter-spacing: -0.5px; background: linear-gradient(45deg, #39470B, #8CA052); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">SHOPNESIA</h1>
        <p style="color: #39470B; font-size: 0.65rem; margin: 2px 0 0 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Executive Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section-header" style="margin-bottom: 10px;">Navigasi Halaman</div>', unsafe_allow_html=True)
    
    # Custom Modern Button Cards Navigation
    if st.button(
        "📊 Ringkasan Performa", 
        use_container_width=True, 
        key="btn_page_1", 
        type="primary" if st.session_state.active_page == "📊 Ringkasan Performa" else "secondary"
    ):
        st.session_state.active_page = "📊 Ringkasan Performa"
        st.rerun()

    if st.button(
        "🔍 Analisis Pasar", 
        use_container_width=True, 
        key="btn_page_2", 
        type="primary" if st.session_state.active_page == "🔍 Analisis Pasar & Ops" else "secondary"
    ):
        st.session_state.active_page = "🔍 Analisis Pasar & Ops"
        st.rerun()

    if st.button(
        "💡 Insight Eksekutif", 
        use_container_width=True, 
        key="btn_page_3", 
        type="primary" if st.session_state.active_page == "💡 Insight Eksekutif" else "secondary"
    ):
        st.session_state.active_page = "💡 Insight Eksekutif"
        st.rerun()

# Map page selection for the rest of the application routing
with st.sidebar:
    st.markdown('<div class="sidebar-section-header" style="margin-top: 15px;">Filter Dashboard</div>', unsafe_allow_html=True)
    
    selected_dates = st.date_input(
        "Rentang Tanggal",
        value=(df["order_date"].min().date(), df["order_date"].max().date())
    )
    if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    elif isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 1:
        start_date = selected_dates[0]
        end_date = selected_dates[0]
    else:
        start_date = df["order_date"].min().date()
        end_date = df["order_date"].max().date()

    all_categories = sorted(df["product_category"].unique().tolist())
    selected_categories = st.multiselect(
        "Kategori Produk",
        options=all_categories,
        default=[],
        placeholder="Semua Kategori"
    )

    all_provinces = sorted(df["customer_province"].unique().tolist())
    selected_provinces = st.multiselect(
        "Provinsi",
        options=all_provinces,
        default=[],
        placeholder="Semua Provinsi"
    )

    all_payments = sorted(df["payment_method"].unique().tolist())
    selected_payments = st.multiselect(
        "Metode Pembayaran",
        options=all_payments,
        default=[],
        placeholder="Semua Metode"
    )

    all_tiers = sorted(df["brand_tier"].unique().tolist())
    selected_tiers = st.multiselect(
        "Brand Tier",
        options=all_tiers,
        default=[],
        placeholder="Semua Tier"
    )
# Map page selection for the rest of the application routing
page = st.session_state.active_page

# =========================
# APPLY FILTERS
# =========================
if start_date > end_date:
    st.error("Tanggal mulai tidak boleh lebih besar dari tanggal akhir!")
    st.stop()

filtered_df = df[
    (df["order_date"] >= pd.to_datetime(start_date)) &
    (df["order_date"] <= pd.to_datetime(end_date))
]

if selected_categories:
    filtered_df = filtered_df[
        filtered_df["product_category"].isin(selected_categories)
    ]
if selected_provinces:
    filtered_df = filtered_df[
        filtered_df["customer_province"].isin(selected_provinces)
    ]
if selected_payments:
    filtered_df = filtered_df[
        filtered_df["payment_method"].isin(selected_payments)
    ]
if selected_tiers:
    filtered_df = filtered_df[
        filtered_df["brand_tier"].isin(selected_tiers)
    ]

# Check empty data
if filtered_df.empty:
    st.warning("Tidak ada data yang sesuai dengan filter. Silakan ubah filter Anda.")
    st.stop()

# =========================
# CALCULATE KPI + DELTA
# =========================
date_range = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
prev_start = pd.to_datetime(start_date) - timedelta(days=date_range + 1)
prev_end = pd.to_datetime(start_date) - timedelta(days=1)

prev_df = df[
    (df["order_date"] >= prev_start) &
    (df["order_date"] <= prev_end)
]
# Apply same non-date filters to previous period
if selected_categories:
    prev_df = prev_df[prev_df["product_category"].isin(selected_categories)]
if selected_provinces:
    prev_df = prev_df[prev_df["customer_province"].isin(selected_provinces)]
if selected_payments:
    prev_df = prev_df[prev_df["payment_method"].isin(selected_payments)]
if selected_tiers:
    prev_df = prev_df[prev_df["brand_tier"].isin(selected_tiers)]

total_revenue = filtered_df["revenue"].sum()
total_orders = len(filtered_df)
total_customers = filtered_df["customer_id"].nunique()
return_rate = filtered_df["is_returned"].mean() * 100
avg_rating = filtered_df["rating"].mean()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

# Previous period
prev_revenue = prev_df["revenue"].sum() if not prev_df.empty else 0
prev_orders = len(prev_df) if not prev_df.empty else 0
prev_customers = prev_df["customer_id"].nunique() if not prev_df.empty else 0
prev_return = prev_df["is_returned"].mean() * 100 if not prev_df.empty else 0
prev_rating = prev_df["rating"].mean() if not prev_df.empty else 0

def calc_delta(current, previous):
    if previous == 0:
        return None
    return ((current - previous) / previous) * 100

delta_revenue = calc_delta(total_revenue, prev_revenue)
delta_orders = calc_delta(total_orders, prev_orders)
delta_customers = calc_delta(total_customers, prev_customers)
delta_return = calc_delta(return_rate, prev_return)
delta_rating = calc_delta(avg_rating, prev_rating)

def format_delta(delta, invert=False):
    """Format delta with arrow. invert=True means lower is better (e.g., return rate)."""
    if delta is None:
        return ""
    arrow = "▲" if delta >= 0 else "▼"
    is_good = (delta >= 0 and not invert) or (delta < 0 and invert)
    css_class = "kpi-badge-up" if is_good else "kpi-badge-down"
    return f'<span class="{css_class}">{arrow} {abs(delta):.1f}%</span>'

# =========================
# HEADER (kecil, tetap tampil di semua page sebagai konteks judul dashboard)
# =========================
st.markdown("""
<div class="dashboard-header">
    <h1>Shopnesia Executive Dashboard</h1>
    <p>Dashboard Analitik Bisnis E-Commerce | Data Driven Insights</p>
</div>
""", unsafe_allow_html=True)

# Catatan: KPI cards TIDAK dirender di sini lagi.
# KPI hanya ditampilkan sekali di dalam Tab 1 "Ringkasan Eksekutif"
# supaya tidak redundan dan tidak memakan ruang di tab lain.

# =========================
# AI INSIGHT GENERATOR
# =========================
def generate_ai_summary(fdf):
    """Generate data-driven insight summary (simulating LLM output)."""

    total_rev = fdf["revenue"].sum()
    total_ord = len(fdf)

    # Top category
    cat_rev = fdf.groupby("product_category")["revenue"].sum().sort_values(ascending=False)
    top_cat = cat_rev.index[0]
    top_cat_pct = (cat_rev.iloc[0] / total_rev * 100)

    # Top province
    prov_rev = fdf.groupby("customer_province")["revenue"].sum().sort_values(ascending=False)
    top_prov = prov_rev.index[0]
    top_prov_pct = (prov_rev.iloc[0] / total_rev * 100)

    # Top subcategory
    sub_rev = fdf.groupby("product_subcategory")["revenue"].sum().sort_values(ascending=False)
    top_sub = sub_rev.index[0]

    # Gender split
    gender_rev = fdf.groupby("customer_gender")["revenue"].sum()
    female_pct = gender_rev.get("Female", 0) / total_rev * 100

    # Age group
    age_rev = fdf.groupby("age_group", observed=True)["revenue"].sum().sort_values(ascending=False)
    top_age = str(age_rev.index[0])
    top_age_pct = (age_rev.iloc[0] / total_rev * 100)

    # Return analysis
    ret_rate = fdf["is_returned"].mean() * 100
    returns_only = fdf[fdf["is_returned"] == True]
    if not returns_only.empty:
        top_return_reason = returns_only["return_reason"].value_counts().index[0]
        top_return_count = returns_only["return_reason"].value_counts().iloc[0]
    else:
        top_return_reason = "N/A"
        top_return_count = 0

    # Monthly trend
    monthly_rev = fdf.groupby(fdf["order_date"].dt.to_period("M"))["revenue"].sum()
    if len(monthly_rev) >= 2:
        last_month_rev = monthly_rev.iloc[-1]
        prev_month_rev = monthly_rev.iloc[-2]
        monthly_change = ((last_month_rev - prev_month_rev) / prev_month_rev * 100)
        trend_text = f"naik {monthly_change:.1f}%" if monthly_change >= 0 else f"turun {abs(monthly_change):.1f}%"
    else:
        trend_text = "stabil"

    # Best delivery
    avg_delivery = fdf["delivery_days"].mean()

    # Discount insight
    disc_rev = fdf.groupby("discount_percent")["revenue"].mean()
    best_disc = disc_rev.sort_values(ascending=False).index[0]

    # Repeat customers
    cust_orders = fdf.groupby("customer_id")["order_id"].nunique()
    repeat_pct = (cust_orders > 1).sum() / len(cust_orders) * 100

    # Payment
    pay_rev = fdf.groupby("payment_method")["revenue"].sum().sort_values(ascending=False)
    top_payment = pay_rev.index[0]
    top_payment_pct = pay_rev.iloc[0] / total_rev * 100

    summary = f"""
<div class="ai-insight-box">
    <h4>Ringkasan Insight</h4>
    <p>Berdasarkan analisis <b>{total_ord:,} transaksi</b> dengan total revenue <b>Rp {total_rev:,.0f}</b>, berikut temuan utama:</p>
    <ul>
        <li><b>Kategori unggulan:</b> <em>{top_cat}</em> menyumbang <b>{top_cat_pct:.1f}%</b> dari total revenue, dengan subkategori terlaris <em>{top_sub}</em>.</li>
        <li><b>Pasar terbesar:</b> <em>{top_prov}</em> mendominasi dengan <b>{top_prov_pct:.1f}%</b> revenue.</li>
        <li><b>Segmen pelanggan:</b> Kelompok usia <em>{top_age} tahun</em> berkontribusi <b>{top_age_pct:.1f}%</b> revenue. Pelanggan perempuan menghasilkan <b>{female_pct:.1f}%</b> dari total revenue.</li>
        <li><b>Loyalitas:</b> <b>{repeat_pct:.1f}%</b> pelanggan melakukan pembelian berulang, menunjukkan retensi yang {"sangat baik" if repeat_pct > 70 else "baik" if repeat_pct > 50 else "perlu ditingkatkan"}.</li>
        <li><b>Tren bulanan:</b> Revenue bulan terakhir <b>{trend_text}</b> dibanding bulan sebelumnya.</li>
        <li><b>Operasional:</b> Rata-rata pengiriman <b>{avg_delivery:.1f} hari</b>. Tingkat retur <b>{ret_rate:.1f}%</b> dengan alasan terbanyak "<em>{top_return_reason}</em>" ({top_return_count:,} kasus).</li>
        <li><b>Pembayaran:</b> <em>{top_payment}</em> paling populer ({top_payment_pct:.1f}% revenue). Diskon <b>{best_disc}%</b> menghasilkan rata-rata revenue per transaksi tertinggi.</li>
    </ul>
    <p style="color: #3B82F6; font-size: 0.8rem; margin-top: 0.8rem;"><b>Rekomendasi:</b> Fokuskan promosi pada segmen usia {top_age} tahun di wilayah {top_prov}. Tingkatkan kualitas kontrol untuk mengurangi retur akibat "{top_return_reason}". Pertimbangkan strategi diskon di kisaran {best_disc}% untuk memaksimalkan revenue.</p>
</div>
"""
    return summary


# Navigation is now at the top of the sidebar

# ==================================================
# TAB 1 — Performa Keuangan & Produk
# ==================================================
if page == "📊 Ringkasan Performa":
    # KPI CARDS
    # Prepare sparkline series
    spark_revenue = get_sparkline_data(filtered_df, "revenue", agg_func="sum")
    spark_orders = get_sparkline_data(filtered_df, "order_id", agg_func="count")
    spark_customers = get_sparkline_data(filtered_df, "customer_id", agg_func="nunique")

    # For average order value
    grouped_week = filtered_df.groupby(filtered_df["order_date"].dt.to_period("W"))
    spark_aov = grouped_week.apply(lambda x: x["revenue"].sum() / len(x) if len(x) > 0 else 0)
    spark_aov.index = spark_aov.index.to_timestamp()

    spark_return = get_sparkline_data(filtered_df, "is_returned", agg_func="mean") * 100
    spark_rating = get_sparkline_data(filtered_df, "rating", agg_func="mean")

    kpi_cols = st.columns(6)
    kpi_data = [
        ("Total Revenue", f"Rp {total_revenue:,.0f}", delta_revenue, False, spark_revenue),
        ("Total Pesanan", f"{total_orders:,}", delta_orders, False, spark_orders),
        ("Pelanggan Unik", f"{total_customers:,}", delta_customers, False, spark_customers),
        ("Rata-rata Pesanan", f"Rp {avg_order_value:,.0f}", None, False, spark_aov),
        ("Tingkat Retur", f"{return_rate:.2f}%", delta_return, True, spark_return),
        ("Rating Rata-rata", f"{avg_rating:.2f}/5.0", delta_rating, False, spark_rating),
    ]

    for col, (label, value, delta, invert, spark_series) in zip(kpi_cols, kpi_data):
        with col:
            with st.container(border=True):
                # Delta badge styling
                delta_badge = ""
                spark_color = "#38470B"  # default moss green
                if delta is not None:
                    arrow = "▲" if delta >= 0 else "▼"
                    is_good = (delta >= 0 and not invert) or (delta < 0 and invert)
                    badge_class = "kpi-badge-up" if is_good else "kpi-badge-down"
                    delta_badge = f'<span class="{badge_class}">{arrow} {abs(delta):.1f}%</span>'
                    spark_color = "#5D702A" if is_good else "#C05C5C"

                # HTML layout for label and value + delta badge
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: flex-start; width: 100%;">
                    <div class="kpi-label">{label}</div>
                    {delta_badge}
                </div>
                <div class="kpi-value-container" style="margin-top: 5px; margin-bottom: 5px;">
                    <span class="kpi-value" style="font-size: 1.05rem; font-weight: 800; color: #2E3710;">{value}</span>
                </div>
                """, unsafe_allow_html=True)

                # Plotly sparkline
                if spark_series is not None and not spark_series.empty:
                    fig_spark = px.line(spark_series, x=spark_series.index, y=spark_series.values, color_discrete_sequence=[spark_color])
                    fig_spark.update_layout(
                        showlegend=False,
                        xaxis_visible=False,
                        yaxis_visible=False,
                        margin=dict(l=0, r=0, t=2, b=2),
                        height=25,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        hovermode=False
                    )
                    fig_spark.update_traces(line=dict(width=1.5))
                    st.plotly_chart(fig_spark, use_container_width=True, config={'displayModeBar': False})

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header-hero">Tren Revenue Bulanan</div>', unsafe_allow_html=True)
    monthly_rev = filtered_df.groupby("month")["revenue"].sum().sort_index().reset_index()
    fig = px.area(
        monthly_rev, x="month", y="revenue",
        labels={"month": "Bulan", "revenue": "Revenue"},
        color_discrete_sequence=["#38470B"],
        template=PLOTLY_TEMPLATE
    )
    fig.update_traces(
        fill="tozeroy",
        fillcolor="rgba(56, 71, 11, 0.15)",
        line=dict(width=3),
        mode="lines+markers",
        marker=dict(size=7, color="#38470B", line=dict(width=1, color="#ffffff"))
    )
    fig.update_layout(
        yaxis_tickformat=",",
        yaxis_tickprefix="Rp ",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#7A6A4E", size=9),
        height=400,
        margin=dict(t=20, b=20, l=75, r=10)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header-hero">Revenue per Kategori Produk</div>', unsafe_allow_html=True)
    category_rev = filtered_df.groupby("product_category")["revenue"].sum().sort_values(ascending=False).reset_index()
    fig = px.bar(
        category_rev, x="product_category", y="revenue",
        color="product_category",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"product_category": "Kategori", "revenue": "Revenue"},
        template=PLOTLY_TEMPLATE,
        text=category_rev["revenue"].apply(format_compact_rp)
    )
    fig.update_traces(textposition="outside", textfont=dict(size=9))
    fig.update_layout(
        yaxis_tickformat=",",
        yaxis_tickprefix="Rp ",
        yaxis_range=[0, category_rev["revenue"].max() * 1.15],
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#7A6A4E", size=9),
        showlegend=False,
        height=400,
        margin=dict(t=20, b=20, l=75, r=10)
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# TAB 2 — Analisis Pasar & Operasional
# ==================================================
elif page == "🔍 Analisis Pasar & Ops":
    st.markdown('<div class="section-header">Top 10 Provinsi (Revenue)</div>', unsafe_allow_html=True)
    province_rev = filtered_df.groupby("customer_province")["revenue"].sum().sort_values(ascending=True).tail(10).reset_index()
    fig = px.bar(
        province_rev, x="revenue", y="customer_province",
        orientation="h",
        color="revenue",
        color_continuous_scale=["#F1D6AB", "#38470B"],
        labels={"customer_province": "Provinsi", "revenue": "Revenue"},
        template=PLOTLY_TEMPLATE,
        text=province_rev["revenue"].apply(format_compact_rp)
    )
    fig.update_traces(textposition="outside", textfont=dict(size=9))
    fig.update_layout(
        xaxis_tickformat=",",
        xaxis_tickprefix="Rp ",
        xaxis_range=[0, province_rev["revenue"].max() * 1.15],
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#7A6A4E", size=9),
        coloraxis_showscale=False,
        height=400,
        margin=dict(t=10, b=20, l=100, r=10)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Kelompok Usia Pelanggan</div>', unsafe_allow_html=True)
    age_rev = filtered_df.groupby("age_group", observed=True)["revenue"].sum().reset_index()
    fig = px.bar(
        age_rev, x="age_group", y="revenue",
        color="age_group",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"age_group": "Kelompok Usia", "revenue": "Revenue"},
        template=PLOTLY_TEMPLATE,
        text=age_rev["revenue"].apply(format_compact_rp)
    )
    fig.update_traces(textposition="outside", textfont=dict(size=9))
    fig.update_layout(
        yaxis_tickformat=",",
        yaxis_tickprefix="Rp ",
        yaxis_range=[0, age_rev["revenue"].max() * 1.15],
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#7A6A4E", size=9),
        showlegend=False,
        height=400,
        margin=dict(t=10, b=20, l=75, r=10)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Tingkat Retur per Kategori</div>', unsafe_allow_html=True)
    return_cat = filtered_df.groupby("product_category")["is_returned"].mean().reset_index()
    return_cat["is_returned"] *= 100
    fig = px.bar(
        return_cat.sort_values("is_returned", ascending=False),
        x="product_category", y="is_returned",
        color="is_returned",
        color_continuous_scale=["#FAF8F4", "#38470B"],
        labels={"product_category": "Kategori", "is_returned": "Retur (%)"},
        template=PLOTLY_TEMPLATE,
        text=return_cat.sort_values("is_returned", ascending=False)["is_returned"].apply(lambda x: f"{x:.1f}%")
    )
    fig.update_traces(textposition="outside", textfont=dict(size=9))
    fig.update_layout(
        yaxis_ticksuffix="%",
        yaxis_range=[0, return_cat["is_returned"].max() * 1.15],
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#7A6A4E", size=9),
        coloraxis_showscale=False,
        height=400,
        margin=dict(t=10, b=20, l=40, r=10)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Hari Pengiriman vs Rating</div>', unsafe_allow_html=True)
    delivery_rating = filtered_df.groupby("delivery_days").agg(rating_avg=("rating", "mean"), count=("order_id", "count")).reset_index().sort_values("delivery_days")
    fig = px.line(
        delivery_rating, x="delivery_days", y="rating_avg",
        markers=True,
        labels={"delivery_days": "Hari Pengiriman", "rating_avg": "Rating"},
        color_discrete_sequence=["#38470B"],
        template=PLOTLY_TEMPLATE,
        text=delivery_rating["rating_avg"].apply(lambda x: f"{x:.2f}")
    )
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=(delivery_rating["count"] / delivery_rating["count"].max() * 12 + 4), line=dict(width=1, color="#ffffff")),
        textposition="top center",
        textfont=dict(size=9)
    )
    fig.update_layout(
        yaxis_range=[1, 5.5],
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#7A6A4E", size=9),
        height=400,
        margin=dict(t=10, b=20, l=40, r=10)
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# TAB 3 — Insight Eksekutif
# ==================================================
elif page == "💡 Insight Eksekutif":
    st.markdown(generate_ai_summary(filtered_df), unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Ringkasan Bulanan</div>', unsafe_allow_html=True)

    # Filter state tracking to detect filter changes
    current_filters = (
        str(start_date),
        str(end_date),
        tuple(selected_categories),
        tuple(selected_provinces),
        tuple(selected_payments),
        tuple(selected_tiers)
    )

    if "last_filters" not in st.session_state or st.session_state.last_filters != current_filters:
        st.session_state.last_filters = current_filters

        monthly_summary = (
            filtered_df
            .groupby("month")
            .agg(
                Revenue=("revenue", "sum"),
                Pesanan=("order_id", "count"),
                Pelanggan=("customer_id", "nunique"),
                Rating_Rata2=("rating", "mean"),
                Retur_Persen=("is_returned", "mean")
            )
            .sort_index()
            .reset_index()
        )
        monthly_summary.columns = ["Bulan", "Revenue", "Jumlah Pesanan", "Pelanggan Unik", "Rating Rata-rata", "Tingkat Retur (%)"]
        monthly_summary["Tingkat Retur (%)"] = (monthly_summary["Tingkat Retur (%)"] * 100).round(2)
        monthly_summary["Rating Rata-rata"] = monthly_summary["Rating Rata-rata"].round(2)

        st.session_state.monthly_summary_data = monthly_summary
        st.session_state.monthly_summary_page = 1

    # Control Panel: Sort & Pagination controls
    col_sort_1, col_sort_2, col_page = st.columns([2.5, 1.5, 2])

    with col_sort_1:
        sort_col = st.selectbox(
            "Urutkan Berdasarkan",
            options=["Bulan", "Revenue", "Jumlah Pesanan", "Pelanggan Unik", "Rating Rata-rata", "Tingkat Retur (%)"],
            index=0,
            key="sort_col_select"
        )
    with col_sort_2:
        sort_order = st.selectbox(
            "Arah Urutan",
            options=["Ascending", "Descending"],
            index=0,
            key="sort_order_select"
        )

    # Apply Sorting before paging and formatting
    monthly_summary = st.session_state.monthly_summary_data
    ascending_bool = (sort_order == "Ascending")
    monthly_summary_sorted = monthly_summary.sort_values(by=sort_col, ascending=ascending_bool)

    # Expander to edit row values dynamically
    with st.expander(":material/edit: Edit Nilai Baris (Ubah Data Tabel)"):
        col_edit_1, col_edit_2, col_edit_3 = st.columns(3)
        with col_edit_1:
            month_to_edit = st.selectbox(
                "Pilih Bulan", 
                options=monthly_summary_sorted["Bulan"].tolist(), 
                key="edit_month_select"
            )
        with col_edit_2:
            col_to_edit = st.selectbox(
                "Pilih Kolom untuk Diubah",
                options=["Revenue", "Jumlah Pesanan", "Pelanggan Unik", "Rating Rata-rata", "Tingkat Retur (%)"],
                key="edit_col_select"
            )
        with col_edit_3:
            current_row = monthly_summary_sorted[monthly_summary_sorted["Bulan"] == month_to_edit]
            if not current_row.empty:
                current_val = current_row[col_to_edit].values[0]
            else:
                current_val = 0.0

            if col_to_edit in ["Jumlah Pesanan", "Pelanggan Unik"]:
                new_val = st.number_input(f"Nilai Baru ({col_to_edit})", value=int(current_val), step=1, key="edit_val_input")
            elif col_to_edit == "Revenue":
                new_val = st.number_input(f"Nilai Baru ({col_to_edit})", value=float(current_val), step=100000.0, key="edit_val_input")
            else:
                new_val = st.number_input(f"Nilai Baru ({col_to_edit})", value=float(current_val), step=0.01, key="edit_val_input")

        if st.button("Simpan Perubahan", icon=":material/save:", key="save_edit_button"):
            # Update the original df in session state
            idx = st.session_state.monthly_summary_data[st.session_state.monthly_summary_data["Bulan"] == month_to_edit].index[0]
            st.session_state.monthly_summary_data.at[idx, col_to_edit] = new_val
            st.success(f"Berhasil mengubah {col_to_edit} untuk bulan {month_to_edit}!")
            st.rerun()

    # Format fields for display
    display_df = monthly_summary_sorted.copy()
    display_df["Revenue"] = display_df["Revenue"].apply(lambda x: f"Rp {x:,.0f}" if isinstance(x, (int, float)) else str(x))

    # Pagination logic
    total_rows = len(display_df)
    rows_per_page = 10
    total_pages = max(1, ((total_rows - 1) // rows_per_page) + 1)

    if st.session_state.monthly_summary_page > total_pages:
        st.session_state.monthly_summary_page = total_pages

    with col_page:
        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)  # Spacer
        sub_col1, sub_col2, sub_col3 = st.columns([1, 2, 1])
        with sub_col1:
            prev_btn = st.button("", icon=":material/chevron_left:", key="prev_page", disabled=(st.session_state.monthly_summary_page == 1))
            if prev_btn:
                st.session_state.monthly_summary_page -= 1
                st.rerun()
        with sub_col2:
            st.markdown(f"<div style='text-align: center; font-size: 0.8rem; margin-top: 5px; font-weight: 600;'>Hal {st.session_state.monthly_summary_page} / {total_pages}</div>", unsafe_allow_html=True)
        with sub_col3:
            next_btn = st.button("", icon=":material/chevron_right:", key="next_page", disabled=(st.session_state.monthly_summary_page == total_pages))
            if next_btn:
                st.session_state.monthly_summary_page += 1
                st.rerun()

    # Slice for current page
    start_idx = (st.session_state.monthly_summary_page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    paginated_df = display_df.iloc[start_idx:end_idx]

    # Calculate optimal height to display up to 10 rows without internal scrollbars
    optimal_height = (len(paginated_df) + 1) * 35 + 3

    st.dataframe(
        paginated_df,
        use_container_width=True,
        hide_index=True,
        height=optimal_height
    )