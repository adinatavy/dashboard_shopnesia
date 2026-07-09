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

    /* Kompres padding utama Streamlit supaya tiap page lebih ringkas & minim scroll */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.3rem;
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

    /* KPI Cards (compact & modern white cards on soft beige background) */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #F1D6AB;
        border-radius: 8px;
        padding: 0.4rem 0.5rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 12px rgba(56, 71, 11, 0.08);
        border-color: #38470B;
    }
    .kpi-label {
        color: #A0855B;
        font-size: 0.58rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.15rem;
    }
    .kpi-value {
        color: #2E3710;
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 0.1rem;
    }
    .kpi-delta-up {
        color: #5D702A;
        font-size: 0.72rem;
        font-weight: 600;
    }
    .kpi-delta-down {
        color: #C05C5C;
        font-size: 0.72rem;
        font-weight: 600;
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

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F9F6F2 0%, #F1D6AB 100%);
        border-right: 1px solid #F1D6AB;
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #2E3710;
    }

    /* Tabs - extra compact */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 6px 14px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .stTabs [data-baseweb="tab"] p {
        font-size: 0.8rem !important;
        font-weight: 700 !important;
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

# =========================
# HORIZONTAL FILTERS (TOP LEVEL)
# =========================
st.markdown('<div class="section-header">Filter Dashboard</div>', unsafe_allow_html=True)
col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns(5)

with col_f1:
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

with col_f2:
    all_categories = sorted(df["product_category"].unique().tolist())
    selected_categories = st.multiselect(
        "Kategori Produk",
        options=all_categories,
        default=[],
        placeholder="Semua Kategori"
    )

with col_f3:
    all_provinces = sorted(df["customer_province"].unique().tolist())
    selected_provinces = st.multiselect(
        "Provinsi",
        options=all_provinces,
        default=[],
        placeholder="Semua Provinsi"
    )

with col_f4:
    all_payments = sorted(df["payment_method"].unique().tolist())
    selected_payments = st.multiselect(
        "Metode Pembayaran",
        options=all_payments,
        default=[],
        placeholder="Semua Metode"
    )

with col_f5:
    all_tiers = sorted(df["brand_tier"].unique().tolist())
    selected_tiers = st.multiselect(
        "Brand Tier",
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
        return ""
    arrow = "▲" if delta >= 0 else "▼"
    is_good = (delta >= 0 and not invert) or (delta < 0 and invert)
    css_class = "kpi-delta-up" if is_good else "kpi-delta-down"
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


# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs([
    "Ringkasan Performa & Produk",
    "Analisis Pasar & Operasional",
    "Insight Eksekutif"
])

# ==================================================
# TAB 1 — Performa Keuangan & Produk
# ==================================================
with tab1:
    # KPI CARDS
    kpi_cols = st.columns(6)
    kpi_data = [
        ("Total Revenue", f"Rp {total_revenue:,.0f}", delta_revenue, False),
        ("Total Pesanan", f"{total_orders:,}", delta_orders, False),
        ("Pelanggan Unik", f"{total_customers:,}", delta_customers, False),
        ("Rata-rata Pesanan", f"Rp {avg_order_value:,.0f}", None, False),
        ("Tingkat Retur", f"{return_rate:.2f}%", delta_return, True),
        ("Rating Rata-rata", f"{avg_rating:.2f}/5.0", delta_rating, False),
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

    col1, col2 = st.columns(2)
    with col1:
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
            font=dict(family="Inter", color="#7A6A4E", size=8),
            height=200,
            margin=dict(t=20, b=20, l=75, r=10)
        )
        st.plotly_chart(fig, width='stretch')

    with col2:
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
        fig.update_traces(textposition="outside", textfont=dict(size=8))
        fig.update_layout(
            yaxis_tickformat=",",
            yaxis_tickprefix="Rp ",
            yaxis_range=[0, category_rev["revenue"].max() * 1.15],
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#7A6A4E", size=8),
            showlegend=False,
            height=200,
            margin=dict(t=20, b=20, l=75, r=10)
        )
        st.plotly_chart(fig, width='stretch')

# ==================================================
# TAB 2 — Analisis Pasar & Operasional
# ==================================================
with tab2:
    col1, col2 = st.columns(2)
    with col1:
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
        fig.update_traces(textposition="outside", textfont=dict(size=8))
        fig.update_layout(
            xaxis_tickformat=",",
            xaxis_tickprefix="Rp ",
            xaxis_range=[0, province_rev["revenue"].max() * 1.15],
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#7A6A4E", size=8),
            coloraxis_showscale=False,
            height=200,
            margin=dict(t=10, b=20, l=100, r=10)
        )
        st.plotly_chart(fig, width='stretch')

    with col2:
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
        fig.update_traces(textposition="outside", textfont=dict(size=8))
        fig.update_layout(
            yaxis_tickformat=",",
            yaxis_tickprefix="Rp ",
            yaxis_range=[0, age_rev["revenue"].max() * 1.15],
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#7A6A4E", size=8),
            showlegend=False,
            height=200,
            margin=dict(t=10, b=20, l=75, r=10)
        )
        st.plotly_chart(fig, width='stretch')

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
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
        fig.update_traces(textposition="outside", textfont=dict(size=8))
        fig.update_layout(
            yaxis_ticksuffix="%",
            yaxis_range=[0, return_cat["is_returned"].max() * 1.15],
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#7A6A4E", size=8),
            coloraxis_showscale=False,
            height=200,
            margin=dict(t=10, b=20, l=40, r=10)
        )
        st.plotly_chart(fig, width='stretch')

    with col4:
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
            textfont=dict(size=8)
        )
        fig.update_layout(
            yaxis_range=[1, 5.5],
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#7A6A4E", size=8),
            height=200,
            margin=dict(t=10, b=20, l=40, r=10)
        )
        st.plotly_chart(fig, width='stretch')

# ==================================================
# TAB 3 — Insight Eksekutif
# ==================================================
with tab3:
    st.markdown(generate_ai_summary(filtered_df), unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Ringkasan Bulanan</div>', unsafe_allow_html=True)

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
    monthly_summary["Revenue"] = monthly_summary["Revenue"].apply(lambda x: f"Rp {x:,.0f}")

    st.dataframe(
        monthly_summary,
        width='stretch',
        hide_index=True,
        height=140
    )

# (Footer removed)
