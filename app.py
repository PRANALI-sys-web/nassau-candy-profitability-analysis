import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide"
)
st.markdown("""
<style>

/* Main App */
.stApp{
    background-color:#F8FAFC;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background-color:#0F172A;
    width:260px !important;
    min-width:260px !important;
    max-width:260px !important;
}
/* Sidebar Labels White */
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* Main Title */
h1{
    color:#1E3A8A;
    font-weight:700;
}

/* Subheaders */
h2,h3{
    color:#2563EB;
}

/* Metric Cards */
[data-testid="metric-container"]{
    background:#FFFFFF;
    border:1px solid #E5E7EB;
    border-radius:12px;
    padding:15px;
    box-shadow:0 3px 8px rgba(0,0,0,0.08);
}
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
# 📊 Sales Performance & Profitability Dashboard

### 📈 Business Overview

This interactive dashboard analyzes Nassau Candy's sales and profitability performance 
by evaluating product performance, division-wise contribution, margins, and key business metrics.

The objective is to help stakeholders identify profitable products, understand sales trends, 
and make data-driven business decisions.

### 🔍 Key Analysis Areas

- Sales and profit performance tracking
- Division profitability comparison
- Product contribution analysis using Pareto Analysis
- Cost and sales relationship evaluation

### 🛠️ Tech Stack

Python | Streamlit | Pandas | Matplotlib

---
""")
st.markdown("""
#### 🎯 Business Problem

The dashboard analyzes the profitability of Nassau Candy products by examining sales, profit, regional performance, product categories, and key business metrics.

The objective is to help stakeholders identify high-performing products, profitable regions, and opportunities to improve business decisions through data-driven insights.

""")


df = pd.read_csv("clean_nassau_candy_data.csv")

df["Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100
df["Profit per Unit"] = df["Gross Profit"] / df["Units"]
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    errors="coerce"
)

st.sidebar.title("🎛️ Dashboard Filters")

st.sidebar.markdown("---")

st.sidebar.info(
    "Use the filters below to explore the Nassau Candy sales and profitability data."
)

division_filter = st.sidebar.selectbox(
    "Select Division",
    ["All"] + sorted(df["Division"].dropna().unique().tolist())
)


date_range = st.sidebar.date_input(
    "Select Date Range",
    []
)


margin_filter = st.sidebar.slider(
    "Select Min Margin %",
    0,
    100,
    0
)


product_search = st.sidebar.text_input(
    "Search Product"
)
if len(date_range) == 2:
    df = df[
        (df["Order Date"] >= pd.to_datetime(date_range[0])) &
        (df["Order Date"] <= pd.to_datetime(date_range[1]))
    ]



if division_filter != "All":
    df = df[df["Division"] == division_filter]


df = df[df["Margin %"] >= margin_filter]


if product_search:
    df = df[
        df["Product Name"].str.contains(
            product_search,
            case=False
        )
    ]
    
# =========================
# EXECUTIVE SUMMARY
# =========================

st.subheader("📌 Executive Summary")

total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()

top_region = (
    df.groupby("Region")["Gross Profit"]
    .sum()
    .idxmax()
)

top_division = (
    df.groupby("Division")["Gross Profit"]
    .sum()
    .idxmax()
)

top_product = (
    df.groupby("Product Name")["Gross Profit"]
    .sum()
    .idxmax()
)

avg_margin = df["Margin %"].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Total Sales", f"${total_sales:,.0f}")

with col2:
    st.metric("📈 Total Profit", f"${total_profit:,.0f}")

with col3:
    st.metric("📊 Avg Margin", f"{avg_margin:.2f}%")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("🏆 Best Region", top_region)

with col5:
    st.metric("🏢 Top Division", top_division)

with col6:
    st.metric("📦 Top Product", top_product)


# =========================
# FUNCTION: ADD BORDER
# =========================
def style_plot(ax):
    ax.set_facecolor("#f9f9f9")  # light background
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("black")   # border color
        spine.set_linewidth(1.2)

# =========================
# DATA PREVIEW
# =========================
st.subheader("📄 Dataset Preview")
st.dataframe(df.head(), height=220, use_container_width=True)
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_nassau_candy_data.csv",
    mime="text/csv"
)
# =========================
# TOP PRODUCTS
# =========================
top_products = (
    df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig1 = px.bar(
    top_products,
    x="Product Name",
    y="Gross Profit",
    color="Gross Profit",
    color_continuous_scale="Blues",
    title=None
)

fig1.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis_title="Product",
    yaxis_title="Gross Profit",
    xaxis_title_standoff=20,
    xaxis_tickangle=-45,
    margin=dict(l=20, r=20, t=20, b=80)
)


# =========================
# REGION PROFIT
# =========================
region_profit = (
    df.groupby("Region")["Gross Profit"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    region_profit,
    x="Region",
    y="Gross Profit",
    color="Gross Profit",
    color_continuous_scale="Teal",
    title=None
)

fig2.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis_title="Region",
    yaxis_title="Gross Profit",
    xaxis_title_standoff=20,
    margin=dict(l=20, r=20, t=20, b=60),
    font=dict(size=14),
    xaxis=dict(title=dict(standoff=20)),
    yaxis=dict(title=dict(standoff=10))
)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Top 10 Profitable Products")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🌍 Profit by Region")
    st.plotly_chart(fig2, use_container_width=True)

    

# =========================
# KPI SECTION
# =========================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

# Total Sales
col1.metric(
    "💰 Total Sales",
    f"${df['Sales'].sum():,.0f}"
)

# Total Profit
col2.metric(
    "📈 Total Profit",
    f"${df['Gross Profit'].sum():,.0f}"
)

# Profit Margin
profit_margin = (df['Gross Profit'].sum() / df['Sales'].sum()) * 100

col3.metric(
    "📊 Profit Margin",
    f"{profit_margin:.2f}%"
)

# Units Sold
col4.metric(
    "📦 Units Sold",
    f"{int(df['Units'].sum()):,}"
)

# Products Count
col5.metric(
    "🛒 Products",
    f"{df['Product Name'].nunique():,}"
)
# =========================
# SALES TREND ANALYSIS
# =========================

st.subheader("📈 Sales Trend Over Time")

monthly_sales = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

fig_trend, ax_trend = plt.subplots(figsize=(10,4))

x = list(range(len(monthly_sales)))

ax_trend.plot(
    x,
    monthly_sales.values,
    marker="o",
    linewidth=2
)
ax_trend.set_xticks(x)

ax_trend.set_xticklabels(
    monthly_sales.index,
    rotation=45,
    ha="center"
)

ax_trend.set_xlim(-0.5, len(x)-0.5)

ax_trend.set_xlabel("Month")
ax_trend.set_ylabel("Sales")
ax_trend.set_title("Monthly Sales Performance")

plt.tight_layout()

st.pyplot(fig_trend, use_container_width=True)

# =========================
# DYNAMIC BUSINESS INSIGHTS
# =========================

st.subheader("💡 Business Insights")

highest_sales_month = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .idxmax()
)

lowest_region = (
    df.groupby("Region")["Gross Profit"]
    .sum()
    .idxmin()
)

highest_margin_product = (
    df.groupby("Product Name")["Margin %"]
    .mean()
    .idxmax()
)

lowest_margin_product = (
    df.groupby("Product Name")["Margin %"]
    .mean()
    .idxmin()
)

col1, col2 = st.columns(2)

with col1:
    st.success(f"""
✅ **Highest Sales Month:** {highest_sales_month}

🏆 **Best Performing Region:** {top_region}

📦 **Highest Margin Product:** {highest_margin_product}
""")

with col2:
    st.warning(f"""
⚠️ **Lowest Profit Region:** {lowest_region}

📉 **Lowest Margin Product:** {lowest_margin_product}

📊 **Average Margin:** {avg_margin:.2f}%
""")

# =========================
# UNITS VS PROFIT + DIVISION PERFORMANCE
# =========================


col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Units vs Profit")

    fig3 = px.scatter(
        df,
        x="Units",
        y="Gross Profit",
        color="Division",
        hover_data=["Product Name"],
        title=None
    )

    fig3.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Units Sold",
        yaxis_title="Gross Profit"
    )

    st.plotly_chart(fig3, use_container_width=True)


with col2:
    st.subheader("📊 Division Performance")

    division_profit = (
        df.groupby("Division")["Gross Profit"]
        .sum()
        .reset_index()
    )

    fig4 = px.bar(
        division_profit,
        x="Division",
        y="Gross Profit",
        color="Gross Profit",
        color_continuous_scale="Blues",
        text_auto=".2s"
    )

    fig4.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Division",
        yaxis_title="Profit"
    )

    st.plotly_chart(fig4, use_container_width=True)

# =========================
# PARETO + COST VS SALES
# =========================
col5, col6 = st.columns(2)
with col5:
    st.subheader("📊 Pareto Analysis")

    if df.empty:
        st.warning("No data available")

    else:
        pareto = df.groupby("Product Name")["Gross Profit"].sum().sort_values(ascending=False).head(10)

        pareto_cum = pareto.cumsum() / pareto.sum() * 100

        fig, ax1 = plt.subplots(figsize=(7,4))

        ax1.bar(pareto.index, pareto.values)

        ax1.set_ylabel("Profit")
        ax1.set_xlabel("Product Name")
        ax1.set_title("Top Profit Contributors")

        ax1.set_xticks(range(len(pareto.index)))
        
        ax1.set_xticklabels(
    pareto.index,
    rotation=45,
    ha="right"
)

        ax2 = ax1.twinx()

        ax2.plot(
            pareto.index,
            pareto_cum,
            color="red",
            marker="o"
        )

        ax2.set_ylabel("Cumulative %")
        ax2.set_ylim(0,100)

        plt.tight_layout()

        st.pyplot(fig, use_container_width=True)


with col6:
    st.subheader("💰 Cost vs Sales")

    fig7 = px.scatter(
        df,
        x="Cost",
        y="Sales",
        color="Division",
        hover_data=["Product Name"],
        title=None
    )

    fig7.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Cost",
        yaxis_title="Sales"
    )

    st.plotly_chart(fig7, use_container_width=True)# ========================
st.markdown("---")
st.caption("Developed by Pranali Wakchaure | Data Analytics Portfolio Project")

