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
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Kompres padding utama Streamlit supaya tiap page lebih ringkas & minim scroll */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.5rem;
    }

    /* Header styling (compact) */
    .dashboard-header {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 0.9rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 0.6rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
    .dashboard-header h1 {
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .dashboard-header p {
        color: #a8b2d1;
        font-size: 0.8rem;
        margin: 0.15rem 0 0 0;
        font-weight: 300;
    }

    /* KPI Cards (compact) */
    .kpi-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid rgba(100, 120, 200, 0.2);
        border-radius: 12px;
        padding: 0.7rem 0.8rem;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.15);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(100, 120, 200, 0.25);
    }
    .kpi-label {
        color: #8892b0;
        font-size: 0.68rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.25rem;
    }
    .kpi-value {
        color: #ccd6f6;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 0.15rem;
    }
    .kpi-delta-up {
        color: #3B82F6;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .kpi-delta-down {
        color: #3B82F6;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* AI Insight Box (compact) */
    .ai-insight-box {
        background: linear-gradient(135deg, #0d1b2a 0%, #1b2838 50%, #1a1a2e 100%);
        border: 1px solid rgba(100, 255, 218, 0.15);
        border-left: 4px solid #3B82F6;
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        margin: 0.4rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    .ai-insight-box h4 {
        color: #3B82F6;
        font-size: 0.9rem;
        font-weight: 700;
        margin: 0 0 0.4rem 0;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .ai-insight-box p, .ai-insight-box li {
        color: #a8b2d1;
        font-size: 0.78rem;
        line-height: 1.35;
    }
    .ai-insight-box ul {
        margin: 0.3rem 0;
        padding-left: 1.1rem;
    }

    /* Section Headers (compact) */
    .section-header {
        color: #ccd6f6;
        font-size: 0.95rem;
        font-weight: 700;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid rgba(100, 255, 218, 0.3);
        margin-bottom: 0.4rem;
    }

    /* Big Highlight Section Header (untuk chart paling penting) */
    .section-header-hero {
        color: #ccd6f6;
        font-size: 1.15rem;
        font-weight: 800;
        padding-bottom: 0.4rem;
        border-bottom: 3px solid #3B82F6;
        margin-bottom: 0.4rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a2e 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #ccd6f6;
    }

    /* Tabs - dibuat lebih jelas & tebal agar teks tab terlihat tegas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 22px;
        font-weight: 700;
        font-size: 0.95rem;
    }
    .stTabs [data-baseweb="tab"] p {
        font-size: 0.95rem !important;
        font-weight: 700 !important;
    }

    /* Hide default metric styling */
    [data-testid="stMetricValue"] {
        font-size: 0 !important;
    }
    [data-testid="stMetric"] {
        display: none;
    }

    /* Divider (compact) */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(100, 255, 218, 0.3), transparent);
        margin: 0.5rem 0;
        border: none;
    }

    /* Rapatkan jarak antar elemen Streamlit secara umum */
    .stPlotlyChart {
        margin-bottom: -0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# COLOR PALETTE
# =========================
COLORS = {
    "primary": "#3B82F6",
    "secondary": "#60A5FA",
    "accent": "#93C5FD",
    "success": "#3B82F6",
    "danger": "#3B82F6",
    "warning": "#3B82F6",
    "bg_dark": "#0F172A",
    "text_light": "#F8FAFC",
}

COLOR_SEQUENCE = [
    "#1E3A8A", "#1E40AF", "#1D4ED8", "#2563EB",
    "#3B82F6", "#60A5FA", "#93C5FD", "#BFDBFE",
    "#DBEAFE"
]

PLOTLY_TEMPLATE = "plotly_dark"

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_excel("Dataset_bersih.xlsx")
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

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.markdown("## Filter Dashboard")
st.sidebar.markdown("---")

# Date filter
st.sidebar.markdown("##### Rentang Tanggal")
start_date = st.sidebar.date_input(
    "Tanggal Mulai", df["order_date"].min()
)
end_date = st.sidebar.date_input(
    "Tanggal Akhir", df["order_date"].max()
)

st.sidebar.markdown("---")

# Category filter
st.sidebar.markdown("##### Kategori Produk")
all_categories = sorted(df["product_category"].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Pilih Kategori",
    options=all_categories,
    default=[],
    placeholder="Semua Kategori"
)

# Province filter
st.sidebar.markdown("##### Provinsi")
all_provinces = sorted(df["customer_province"].unique().tolist())
selected_provinces = st.sidebar.multiselect(
    "Pilih Provinsi",
    options=all_provinces,
    default=[],
    placeholder="Semua Provinsi"
)

# Payment method filter
st.sidebar.markdown("##### Metode Pembayaran")
all_payments = sorted(df["payment_method"].unique().tolist())
selected_payments = st.sidebar.multiselect(
    "Pilih Metode",
    options=all_payments,
    default=[],
    placeholder="Semua Metode"
)

# Brand tier filter
st.sidebar.markdown("##### Brand Tier")
all_tiers = sorted(df["brand_tier"].unique().tolist())
selected_tiers = st.sidebar.multiselect(
    "Pilih Tier",
    options=all_tiers,
    default=[],
    placeholder="Semua Tier"
)

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
        return '<span style="color: #8892b0; font-size: 0.8rem;">— Tidak ada data sebelumnya</span>'
    arrow = "▲" if delta >= 0 else "▼"
    is_good = (delta >= 0 and not invert) or (delta < 0 and invert)
    css_class = "kpi-delta-up" if is_good else "kpi-delta-down"
    return f'<span class="{css_class}">{arrow} {abs(delta):.1f}%</span>'

# =========================
# HEADER (kecil, tetap tampil di semua page sebagai konteks judul dashboard)
# =========================
st.markdown("""
<div class="dashboard-header">
    <h1>📊 Shopnesia Executive Dashboard</h1>
    <p>Dashboard Analitik Bisnis E-Commerce — Data Driven Insights</p>
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
    <h4>🧠 Ringkasan Insight</h4>
    <p>Berdasarkan analisis <b>{total_ord:,} transaksi</b> dengan total revenue <b>Rp {total_rev:,.0f}</b>, berikut temuan utama:</p>
    <ul>
        <li><b>Kategori unggulan:</b> <em>{top_cat}</em> menyumbang <b>{top_cat_pct:.1f}%</b> dari total revenue, dengan subkategori terlaris <em>{top_sub}</em>.</li>
        <li><b>Pasar terbesar:</b> <em>{top_prov}</em> mendominasi dengan <b>{top_prov_pct:.1f}%</b> revenue.</li>
        <li><b>Segmen pelanggan:</b> Kelompok usia <em>{top_age} tahun</em> berkontribusi <b>{top_age_pct:.1f}%</b> revenue. Pelanggan perempuan menghasilkan <b>{female_pct:.1f}%</b> dari total revenue.</li>
        <li><b>Loyalitas:</b> <b>{repeat_pct:.1f}%</b> pelanggan melakukan pembelian berulang — menunjukkan retensi yang {"sangat baik" if repeat_pct > 70 else "baik" if repeat_pct > 50 else "perlu ditingkatkan"}.</li>
        <li><b>Tren bulanan:</b> Revenue bulan terakhir <b>{trend_text}</b> dibanding bulan sebelumnya.</li>
        <li><b>Operasional:</b> Rata-rata pengiriman <b>{avg_delivery:.1f} hari</b>. Tingkat retur <b>{ret_rate:.1f}%</b> dengan alasan terbanyak "<em>{top_return_reason}</em>" ({top_return_count:,} kasus).</li>
        <li><b>Pembayaran:</b> <em>{top_payment}</em> paling populer ({top_payment_pct:.1f}% revenue). Diskon <b>{best_disc}%</b> menghasilkan rata-rata revenue per transaksi tertinggi.</li>
    </ul>
    <p style="color: #3B82F6; font-size: 0.8rem; margin-top: 0.8rem;">💡 <b>Rekomendasi:</b> Fokuskan promosi pada segmen usia {top_age} tahun di wilayah {top_prov}. Tingkatkan kualitas kontrol untuk mengurangi retur akibat "{top_return_reason}". Pertimbangkan strategi diskon di kisaran {best_disc}% untuk memaksimalkan revenue.</p>
</div>
"""
    return summary


# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Ringkasan Eksekutif",
    "📈 Performa Penjualan",
    "👥 Analitik Pelanggan",
    "⚙️ Operasional",
    "📢 Marketing & Pembayaran"
])

# ==================================================
# TAB 1 — Ringkasan Eksekutif
# ==================================================
with tab1:

    # =========================
    # KPI CARDS — hanya tampil di sini (Ringkasan Eksekutif), tidak diulang di tab lain
    # =========================
    kpi_cols = st.columns(6)

    kpi_data = [
        ("💰 Total Revenue", f"Rp {total_revenue:,.0f}", delta_revenue, False),
        ("🛒 Total Pesanan", f"{total_orders:,}", delta_orders, False),
        ("👤 Pelanggan Unik", f"{total_customers:,}", delta_customers, False),
        ("📦 Rata-rata Pesanan", f"Rp {avg_order_value:,.0f}", None, False),
        ("↩️ Tingkat Retur", f"{return_rate:.2f}%", delta_return, True),
        ("⭐ Rating Rata-rata", f"{avg_rating:.2f}/5.0", delta_rating, False),
    ]

    for col, (label, value, delta, invert) in zip(kpi_cols, kpi_data):
        delta_html = format_delta(delta, invert) if delta is not None else format_delta(None)
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # AI Summary — insight paling penting, tampil penuh tanpa perlu klik
    st.markdown(generate_ai_summary(filtered_df), unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Revenue Trend — dibuat paling besar/prominen di dashboard utama
    st.markdown('<div class="section-header-hero">📈 Tren Revenue Bulanan</div>',
                unsafe_allow_html=True)

    monthly_rev = (
        filtered_df
        .groupby("month")["revenue"]
        .sum()
        .sort_index()
        .reset_index()
    )

    fig = px.area(
        monthly_rev, x="month", y="revenue",
        labels={"month": "Bulan", "revenue": "Revenue (Rp)"},
        color_discrete_sequence=["#3B82F6"],
        template=PLOTLY_TEMPLATE,
        text=monthly_rev["revenue"].apply(lambda x: f"Rp {x:,.0f}")
    )
    fig.update_traces(
        fill="tozeroy",
        fillcolor="rgba(59, 130, 246, 0.15)",
        line=dict(width=4),
        mode="lines+markers+text",
        marker=dict(size=9, color="#3B82F6", line=dict(width=2, color="#0a192f")),
        textposition="top center",
        textfont=dict(size=12, color="#ccd6f6")
    )
    fig.update_layout(
        yaxis_tickformat=",",
        yaxis_tickprefix="Rp ",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#8892b0", size=13),
        height=340,
        margin=dict(t=40, b=40)
    )
    st.plotly_chart(fig, width="stretch")

    # Two columns: Province + Category
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">🗺️ Top 10 Provinsi (Revenue)</div>',
                    unsafe_allow_html=True)

        province_rev = (
            filtered_df
            .groupby("customer_province")["revenue"]
            .sum()
            .sort_values(ascending=True)
            .tail(10)
            .reset_index()
        )

        fig = px.bar(
            province_rev, x="revenue", y="customer_province",
            orientation="h",
            color="revenue",
            color_continuous_scale=["#0F172A", "#3B82F6"],
            labels={"customer_province": "Provinsi", "revenue": "Revenue (Rp)"},
            template=PLOTLY_TEMPLATE,
            text=province_rev["revenue"].apply(lambda x: f"Rp {x:,.0f}")
        )
        fig.update_traces(textposition="outside", textfont=dict(size=11))
        fig.update_layout(
            xaxis_tickformat=",",
            xaxis_tickprefix="Rp ",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            coloraxis_showscale=False,
            height=260,
            margin=dict(t=10, b=30)
        )
        st.plotly_chart(fig, width="stretch")

    with col2:
        st.markdown('<div class="section-header">🏷️ Revenue per Kategori</div>',
                    unsafe_allow_html=True)

        category_rev = (
            filtered_df
            .groupby("product_category")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig = px.pie(
            category_rev,
            names="product_category", values="revenue",
            color_discrete_sequence=COLOR_SEQUENCE,
            template=PLOTLY_TEMPLATE,
            hole=0.45
        )
        fig.update_traces(
            textposition="outside",
            textinfo="label+percent",
            textfont_size=12,
            marker=dict(line=dict(color="#0a192f", width=2))
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            height=260,
            margin=dict(t=10, b=30),
            showlegend=False
        )
        st.plotly_chart(fig, width="stretch")

    # Monthly Summary Table
    st.markdown('<div class="section-header">📋 Ringkasan Bulanan</div>',
                unsafe_allow_html=True)

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
    monthly_summary.columns = ["Bulan", "Revenue (Rp)", "Jumlah Pesanan", 
                                "Pelanggan Unik", "Rating Rata-rata", "Tingkat Retur (%)"]
    monthly_summary["Tingkat Retur (%)"] = (monthly_summary["Tingkat Retur (%)"] * 100).round(2)
    monthly_summary["Rating Rata-rata"] = monthly_summary["Rating Rata-rata"].round(2)
    monthly_summary["Revenue (Rp)"] = monthly_summary["Revenue (Rp)"].apply(lambda x: f"Rp {x:,.0f}")

    st.dataframe(
        monthly_summary,
        width="stretch",
        hide_index=True,
        height=200
    )

# ==================================================
# TAB 2 — Performa Penjualan
# ==================================================
with tab2:

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">🏷️ Revenue per Kategori</div>',
                    unsafe_allow_html=True)

        category_rev = (
            filtered_df
            .groupby("product_category")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig = px.bar(
            category_rev,
            x="product_category", y="revenue",
            color="product_category",
            color_discrete_sequence=COLOR_SEQUENCE,
            labels={"product_category": "Kategori", "revenue": "Revenue (Rp)"},
            template=PLOTLY_TEMPLATE,
            text=category_rev["revenue"].apply(lambda x: f"Rp {x:,.0f}")
        )
        fig.update_traces(textposition="outside", textfont=dict(size=11))
        fig.update_layout(
            yaxis_tickformat=",",
            yaxis_tickprefix="Rp ",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            showlegend=False,
            height=260,
            margin=dict(t=10, b=30)
        )
        st.plotly_chart(fig, width="stretch")

    with col2:
        st.markdown('<div class="section-header">🏅 Revenue per Brand Tier</div>',
                    unsafe_allow_html=True)

        brand_rev = (
            filtered_df
            .groupby("brand_tier")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig = px.bar(
            brand_rev,
            x="brand_tier", y="revenue",
            color="brand_tier",
            color_discrete_sequence=["#1E3A8A", "#3B82F6", "#93C5FD"],
            labels={"brand_tier": "Brand Tier", "revenue": "Revenue (Rp)"},
            template=PLOTLY_TEMPLATE,
            text=brand_rev["revenue"].apply(lambda x: f"Rp {x:,.0f}")
        )
        fig.update_traces(textposition="outside", textfont=dict(size=11))
        fig.update_layout(
            yaxis_tickformat=",",
            yaxis_tickprefix="Rp ",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            showlegend=False,
            height=260,
            margin=dict(t=10, b=30)
        )
        st.plotly_chart(fig, width="stretch")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">📦 Top 10 Subkategori Produk</div>',
                    unsafe_allow_html=True)

        sub_rev = (
            filtered_df
            .groupby("product_subcategory")["revenue"]
            .sum()
            .sort_values(ascending=True)
            .tail(10)
            .reset_index()
        )

        fig = px.bar(
            sub_rev, x="revenue", y="product_subcategory",
            orientation="h",
            color="revenue",
            color_continuous_scale=["#0F172A", "#3B82F6"],
            labels={"product_subcategory": "Subkategori", "revenue": "Revenue (Rp)"},
            template=PLOTLY_TEMPLATE,
            text=sub_rev["revenue"].apply(lambda x: f"Rp {x:,.0f}")
        )
        fig.update_traces(textposition="outside", textfont=dict(size=11))
        fig.update_layout(
            xaxis_tickformat=",",
            xaxis_tickprefix="Rp ",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            coloraxis_showscale=False,
            height=260,
            margin=dict(t=10, b=30)
        )
        st.plotly_chart(fig, width="stretch")

    with col4:
        st.markdown('<div class="section-header">📅 Revenue per Hari dalam Seminggu</div>',
                    unsafe_allow_html=True)

        dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow_labels = {
            "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
            "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
        }

        dow_rev = (
            filtered_df
            .groupby("day_of_week")["revenue"]
            .sum()
            .reindex(dow_order)
            .reset_index()
        )
        dow_rev["day_of_week"] = dow_rev["day_of_week"].map(dow_labels)

        fig = px.bar(
            dow_rev, x="day_of_week", y="revenue",
            color="revenue",
            color_continuous_scale=["#0F172A", "#3B82F6"],
            labels={"day_of_week": "Hari", "revenue": "Revenue (Rp)"},
            template=PLOTLY_TEMPLATE,
            text=dow_rev["revenue"].apply(lambda x: f"Rp {x:,.0f}")
        )
        fig.update_traces(textposition="outside", textfont=dict(size=11))
        fig.update_layout(
            yaxis_tickformat=",",
            yaxis_tickprefix="Rp ",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            coloraxis_showscale=False,
            height=260,
            margin=dict(t=10, b=30)
        )
        st.plotly_chart(fig, width="stretch")

    # Average Order Value Trend
    st.markdown('<div class="section-header">📈 Tren Rata-rata Nilai Pesanan (AOV)</div>',
                unsafe_allow_html=True)

    aov_trend = (
        filtered_df
        .groupby("month")
        .agg(aov=("revenue", "mean"))
        .sort_index()
        .reset_index()
    )

    fig = px.line(
        aov_trend, x="month", y="aov",
        markers=True,
        labels={"month": "Bulan", "aov": "AOV (Rp)"},
        color_discrete_sequence=["#3B82F6"],
        template=PLOTLY_TEMPLATE,
        text=aov_trend["aov"].apply(lambda x: f"Rp {x:,.0f}")
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8), textposition="top center", textfont=dict(size=10))
    fig.update_layout(
        yaxis_tickformat=",",
        yaxis_tickprefix="Rp ",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#8892b0"),
        height=230,
        margin=dict(t=20, b=40)
    )
    st.plotly_chart(fig, width="stretch")


# ==================================================
# TAB 3 — Analitik Pelanggan
# ==================================================
with tab3:

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">🚻 Revenue per Gender</div>',
                    unsafe_allow_html=True)

        gender_rev = (
            filtered_df
            .groupby("customer_gender")["revenue"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            gender_rev,
            names="customer_gender", values="revenue",
            color_discrete_sequence=["#1E40AF", "#60A5FA"],
            template=PLOTLY_TEMPLATE,
            hole=0.5
        )
        fig.update_traces(
            textposition="inside",
            textinfo="label+percent",
            textfont_size=14,
            marker=dict(line=dict(color="#0a192f", width=2))
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            height=240,
            margin=dict(t=10, b=30)
        )
        st.plotly_chart(fig, width="stretch")

    with col2:
        st.markdown('<div class="section-header">🎂 Revenue per Kelompok Usia</div>',
                    unsafe_allow_html=True)

        age_rev = (
            filtered_df
            .groupby("age_group", observed=True)["revenue"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            age_rev, x="age_group", y="revenue",
            color="age_group",
            color_discrete_sequence=COLOR_SEQUENCE,
            labels={"age_group": "Kelompok Usia", "revenue": "Revenue (Rp)"},
            template=PLOTLY_TEMPLATE,
            text=age_rev["revenue"].apply(lambda x: f"Rp {x:,.0f}")
        )
        fig.update_traces(textposition="outside", textfont=dict(size=11))
        fig.update_layout(
            yaxis_tickformat=",",
            yaxis_tickprefix="Rp ",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            showlegend=False,
            height=240,
            margin=dict(t=10, b=30)
        )
        st.plotly_chart(fig, width="stretch")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">🔁 Analisis Loyalitas Pelanggan</div>',
                    unsafe_allow_html=True)

        cust_orders = (
            filtered_df
            .groupby("customer_id")["order_id"]
            .nunique()
            .reset_index()
        )
        cust_orders.columns = ["customer_id", "jumlah_pesanan"]

        def classify_loyalty(n):
            if n == 1: return "1 Pesanan"
            elif n <= 5: return "2-5 Pesanan"
            elif n <= 10: return "6-10 Pesanan"
            else: return "10+ Pesanan"

        cust_orders["segmen"] = cust_orders["jumlah_pesanan"].apply(classify_loyalty)
        loyalty_counts = cust_orders["segmen"].value_counts().reset_index()
        loyalty_counts.columns = ["Segmen", "Jumlah"]

        # Reorder
        order_map = {"1 Pesanan": 0, "2-5 Pesanan": 1, "6-10 Pesanan": 2, "10+ Pesanan": 3}
        loyalty_counts["sort_key"] = loyalty_counts["Segmen"].map(order_map)
        loyalty_counts = loyalty_counts.sort_values("sort_key").drop(columns="sort_key")

        fig = px.pie(
            loyalty_counts,
            names="Segmen", values="Jumlah",
            color_discrete_sequence=["#1E3A8A", "#2563EB", "#60A5FA", "#BFDBFE"],
            template=PLOTLY_TEMPLATE,
            hole=0.45
        )
        fig.update_traces(
            textposition="outside",
            textinfo="label+percent",
            marker=dict(line=dict(color="#0a192f", width=2))
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            height=240,
            margin=dict(t=10, b=30),
            showlegend=False
        )
        st.plotly_chart(fig, width="stretch")

    with col4:
        st.markdown('<div class="section-header">🏙️ Top 10 Kota (Revenue)</div>',
                    unsafe_allow_html=True)

        city_rev = (
            filtered_df
            .groupby("customer_city")["revenue"]
            .sum()
            .sort_values(ascending=True)
            .tail(10)
            .reset_index()
        )

        fig = px.bar(
            city_rev, x="revenue", y="customer_city",
            orientation="h",
            color="revenue",
            color_continuous_scale=["#0F172A", "#3B82F6"],
            labels={"customer_city": "Kota", "revenue": "Revenue (Rp)"},
            template=PLOTLY_TEMPLATE,
            text=city_rev["revenue"].apply(lambda x: f"Rp {x:,.0f}")
        )
        fig.update_traces(textposition="outside", textfont=dict(size=11))
        fig.update_layout(
            xaxis_tickformat=",",
            xaxis_tickprefix="Rp ",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            coloraxis_showscale=False,
            height=240,
            margin=dict(t=10, b=30)
        )
        st.plotly_chart(fig, width="stretch")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Top Customers
    st.markdown('<div class="section-header">🏆 Top 10 Pelanggan</div>',
                unsafe_allow_html=True)

    top_customer = (
        filtered_df
        .groupby("customer_id")
        .agg(
            Total_Revenue=("revenue", "sum"),
            Jumlah_Pesanan=("order_id", "nunique"),
            Rata2_Rating=("rating", "mean"),
            Provinsi=("customer_province", "first"),
            Kota=("customer_city", "first")
        )
        .sort_values("Total_Revenue", ascending=False)
        .head(10)
        .reset_index()
    )
    top_customer.columns = [
        "ID Pelanggan", "Total Revenue (Rp)", "Jumlah Pesanan",
        "Rating Rata-rata", "Provinsi", "Kota"
    ]
    top_customer["Rating Rata-rata"] = top_customer["Rating Rata-rata"].round(2)
    top_customer["Total Revenue (Rp)"] = top_customer["Total Revenue (Rp)"].apply(
        lambda x: f"Rp {x:,.0f}"
    )

    st.dataframe(top_customer, width="stretch", hide_index=True)


# ==================================================
# TAB 4 — Operasional
# ==================================================
with tab4:

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">↩️ Tingkat Retur per Kategori</div>',
                    unsafe_allow_html=True)

        return_cat = (
            filtered_df
            .groupby("product_category")["is_returned"]
            .mean()
            .reset_index()
        )
        return_cat["is_returned"] *= 100

        fig = px.bar(
            return_cat.sort_values("is_returned", ascending=False),
            x="product_category", y="is_returned",
            color="is_returned",
            color_continuous_scale=["#3B82F6", "#93C5FD"],
            labels={"product_category": "Kategori", "is_returned": "Tingkat Retur (%)"},
            template=PLOTLY_TEMPLATE,
            text=return_cat.sort_values("is_returned", ascending=False)["is_returned"].apply(lambda x: f"{x:.1f}%")
        )
        fig.update_traces(textposition="outside", textfont=dict(size=11))
        fig.update_layout(
            yaxis_ticksuffix="%",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            coloraxis_showscale=False,
            height=260,
            margin=dict(t=10, b=30)
        )
        st.plotly_chart(fig, width="stretch")

    with col2:
        st.markdown('<div class="section-header">🚚 Hari Pengiriman vs Rating</div>',
                    unsafe_allow_html=True)

        delivery_rating = (
            filtered_df
            .groupby("delivery_days")
            .agg(
                rating_avg=("rating", "mean"),
                count=("order_id", "count")
            )
            .reset_index()
            .sort_values("delivery_days")
        )

        # Line chart lebih relevan untuk menunjukkan tren/hubungan dua variabel
        # kontinu-ordinal (hari pengiriman vs rating) dibanding bar chart.
        # Ukuran marker merepresentasikan volume pesanan (jumlah data pendukung).
        fig = px.line(
            delivery_rating,
            x="delivery_days", y="rating_avg",
            markers=True,
            labels={
                "delivery_days": "Hari Pengiriman",
                "rating_avg": "Rating Rata-rata"
            },
            color_discrete_sequence=["#3B82F6"],
            template=PLOTLY_TEMPLATE,
            text=delivery_rating["rating_avg"].apply(lambda x: f"{x:.2f}")
        )
        fig.update_traces(
            line=dict(width=3),
            marker=dict(
                size=(delivery_rating["count"] / delivery_rating["count"].max() * 18 + 6),
                line=dict(width=1, color="#0a192f")
            ),
            textposition="top center",
            textfont=dict(size=10)
        )
        fig.update_layout(yaxis_range=[0, 5.5])
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            height=260,
            margin=dict(t=10, b=30)
        )
        st.plotly_chart(fig, width="stretch")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">📉 Alasan Retur</div>',
                    unsafe_allow_html=True)

        returns_only = filtered_df[filtered_df["is_returned"] == True]

        if not returns_only.empty:
            return_reasons = (
                returns_only
                .groupby("return_reason")
                .agg(
                    Jumlah=("order_id", "count"),
                    Revenue_Hilang=("revenue", "sum")
                )
                .sort_values("Jumlah", ascending=False)
                .reset_index()
            )

            fig = px.bar(
                return_reasons,
                x="return_reason", y="Jumlah",
                color="Revenue_Hilang",
                color_continuous_scale=["#3B82F6", "#93C5FD"],
                labels={"return_reason": "Alasan Retur", "Jumlah": "Jumlah Kasus"},
                template=PLOTLY_TEMPLATE,
                text=return_reasons["Jumlah"]
            )
            fig.update_traces(textposition="outside", textfont=dict(size=11))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#8892b0"),
                coloraxis_colorbar_title="Revenue Hilang",
                height=260,
                margin=dict(t=10, b=30)
            )
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Tidak ada retur pada periode ini.")

    with col4:
        st.markdown('<div class="section-header">⭐ Distribusi Rating</div>',
                    unsafe_allow_html=True)

        # Rating bersifat diskrit (mis. 1-5), sehingga bar chart atas jumlah per
        # nilai rating lebih relevan & mudah dibaca dibanding histogram ber-bin.
        rating_counts = (
            filtered_df["rating"]
            .round(0)
            .value_counts()
            .sort_index()
            .reset_index()
        )
        rating_counts.columns = ["rating", "jumlah"]

        fig = px.bar(
            rating_counts, x="rating", y="jumlah",
            color_discrete_sequence=["#3B82F6"],
            labels={"rating": "Rating", "jumlah": "Jumlah Pesanan"},
            template=PLOTLY_TEMPLATE,
            text="jumlah"
        )
        fig.update_traces(textposition="outside", textfont=dict(size=11))
        fig.update_layout(
            xaxis=dict(dtick=1),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            height=260,
            margin=dict(t=10, b=30)
        )
        st.plotly_chart(fig, width="stretch")

    # Delivery distribution
    st.markdown('<div class="section-header">📦 Distribusi Hari Pengiriman</div>',
                unsafe_allow_html=True)

    fig = px.histogram(
        filtered_df, x="delivery_days",
        nbins=30,
        color_discrete_sequence=["#3B82F6"],
        labels={"delivery_days": "Hari Pengiriman", "count": "Jumlah Pesanan"},
        template=PLOTLY_TEMPLATE
    )
    fig.update_layout(
        yaxis_title="Jumlah Pesanan",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#8892b0"),
        height=230,
        margin=dict(t=20, b=40)
    )
    st.plotly_chart(fig, width="stretch")


# ==================================================
# TAB 5 — Marketing & Pembayaran
# ==================================================
with tab5:

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">💳 Revenue per Metode Pembayaran</div>',
                    unsafe_allow_html=True)

        payment = (
            filtered_df
            .groupby("payment_method")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig = px.pie(
            payment,
            names="payment_method", values="revenue",
            color_discrete_sequence=COLOR_SEQUENCE,
            template=PLOTLY_TEMPLATE,
            hole=0.45
        )
        fig.update_traces(
            textposition="outside",
            textinfo="label+percent",
            marker=dict(line=dict(color="#0a192f", width=2))
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            height=260,
            margin=dict(t=10, b=30),
            showlegend=False
        )
        st.plotly_chart(fig, width="stretch")

    with col2:
        st.markdown('<div class="section-header">🏷️ Diskon vs Revenue</div>',
                    unsafe_allow_html=True)

        fig = px.scatter(
            filtered_df.sample(min(3000, len(filtered_df)), random_state=42),
            x="discount_percent", y="revenue",
            trendline="ols",
            color_discrete_sequence=["#3B82F6"],
            opacity=0.4,
            labels={"discount_percent": "Diskon (%)", "revenue": "Revenue (Rp)"},
            template=PLOTLY_TEMPLATE
        )
        fig.update_traces(
            selector=dict(mode="lines"),
            line=dict(color="#3B82F6", width=3)
        )
        fig.update_layout(
            yaxis_tickformat=",",
            yaxis_tickprefix="Rp ",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            height=260,
            margin=dict(t=10, b=30)
        )
        st.plotly_chart(fig, width="stretch")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">💵 Revenue per Rentang Diskon</div>',
                    unsafe_allow_html=True)

        disc_rev = (
            filtered_df
            .groupby("discount_percent")
            .agg(
                Revenue_Total=("revenue", "sum"),
                Revenue_Rata2=("revenue", "mean"),
                Jumlah_Pesanan=("order_id", "count")
            )
            .reset_index()
        )

        fig = px.bar(
            disc_rev,
            x="discount_percent", y="Revenue_Total",
            color="Revenue_Rata2",
            color_continuous_scale=["#0F172A", "#3B82F6"],
            labels={
                "discount_percent": "Diskon (%)",
                "Revenue_Total": "Total Revenue (Rp)",
                "Revenue_Rata2": "Rata-rata Revenue"
            },
            template=PLOTLY_TEMPLATE
        )
        fig.update_layout(
            yaxis_tickformat=",",
            yaxis_tickprefix="Rp ",
            xaxis_dtick=5,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            height=260,
            margin=dict(t=10, b=30)
        )
        st.plotly_chart(fig, width="stretch")

    with col4:
        st.markdown('<div class="section-header">↩️ Tingkat Retur per Diskon</div>',
                    unsafe_allow_html=True)

        disc_return = (
            filtered_df
            .groupby("discount_percent")["is_returned"]
            .mean()
            .reset_index()
        )
        disc_return["is_returned"] *= 100

        fig = px.line(
            disc_return,
            x="discount_percent", y="is_returned",
            markers=True,
            labels={
                "discount_percent": "Diskon (%)",
                "is_returned": "Tingkat Retur (%)"
            },
            color_discrete_sequence=["#3B82F6"],
            template=PLOTLY_TEMPLATE
        )
        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=10, line=dict(width=2, color="#0a192f"))
        )
        fig.update_layout(
            yaxis_ticksuffix="%",
            xaxis_dtick=5,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#8892b0"),
            height=260,
            margin=dict(t=10, b=30)
        )
        st.plotly_chart(fig, width="stretch")

    # Yearly comparison
    st.markdown('<div class="section-header">📆 Perbandingan Revenue Tahunan</div>',
                unsafe_allow_html=True)

    yearly_data = filtered_df.copy()
    yearly_data["_year"] = yearly_data["order_date"].dt.year
    yearly_data["_month"] = yearly_data["order_date"].dt.month
    yearly_rev = (
        yearly_data
        .groupby(["_year", "_month"])["revenue"]
        .sum()
        .reset_index()
    )
    yearly_rev.columns = ["Tahun", "Bulan", "Revenue"]
    yearly_rev["Tahun"] = yearly_rev["Tahun"].astype(str)

    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun",
        7: "Jul", 8: "Ags", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des"
    }
    yearly_rev["Bulan_Label"] = yearly_rev["Bulan"].map(month_names)

    fig = px.line(
        yearly_rev,
        x="Bulan_Label", y="Revenue",
        color="Tahun",
        markers=True,
        color_discrete_sequence=["#1E3A8A", "#2563EB", "#60A5FA", "#BFDBFE"],
        labels={"Bulan_Label": "Bulan", "Revenue": "Revenue (Rp)"},
        template=PLOTLY_TEMPLATE
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=7))
    fig.update_layout(
        yaxis_tickformat=",",
        yaxis_tickprefix="Rp ",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#8892b0"),
        height=260,
        margin=dict(t=20, b=40)
    )
    st.plotly_chart(fig, width="stretch")


# =========================
# FOOTER
# =========================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #8892b0; font-size: 0.8rem;">
    <p>📊 <b>Shopnesia Executive Dashboard</b> — Data Analytics & Visualization</p>
    <p style="font-size: 0.7rem; color: #4a5568;">Dibuat dengan Streamlit & Plotly | Data periode 2021-2023</p>
</div>
""", unsafe_allow_html=True)
