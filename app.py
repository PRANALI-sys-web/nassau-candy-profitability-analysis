import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(layout="wide")
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

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='font-size:30px;font-weight:700;margin-bottom:0px;'>
📊 Nassau Candy Product Profitability Dashboard
</h1>
""", unsafe_allow_html=True)

st.markdown("""
#### 📈 Business Problem

This interactive dashboard analyzes the profitability of Nassau Candy products by examining sales, profit, regional performance, product categories, and key business metrics.

The objective is to help stakeholders identify high-performing products, profitable regions, and opportunities to improve business decisions through data-driven insights.
""")

st.markdown("""
**🛠️ Tech Stack:** Python | Streamlit | Pandas | Matplotlib
""")

df = pd.read_csv("clean_nassau_candy_data.csv")

df["Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100
df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

st.sidebar.title("🎛️ Dashboard Filters")

st.sidebar.markdown("---")

st.sidebar.info(
    "Use the filters below to explore the Nassau Candy sales and profitability data."
)

division_filter = st.sidebar.selectbox(
    "Select Division",
    ["All"] + sorted(df["Division"].dropna().unique().tolist())
)

if division_filter != "All":
    df = df[df["Division"] == division_filter]

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
    yaxis_title="Gross Profit"
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
    title_x=0.5,
    xaxis_title="Region",
    yaxis_title="Gross Profit"
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Top 10 Profitable Products")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🌍 Profit by Region")
    st.plotly_chart(fig2, use_container_width=True)


# =========================
# UNITS VS PROFIT
# =========================
st.subheader("📈 Units vs Profit Relationship")

fig3, ax3 = plt.subplots(figsize=(8,3.8))

ax3.scatter(df["Units"], df["Gross Profit"], alpha=0.6)

style_plot(ax3)

ax3.set_xlabel("Units Sold")
ax3.set_ylabel("Gross Profit")
ax3.set_title("Units vs Profit")

plt.tight_layout()

st.pyplot(fig3, use_container_width=True)

# =========================
# KPI SECTION
# =========================
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"${df['Sales'].sum():,.0f}"
)

col2.metric(
    "📈 Total Profit",
    f"${df['Gross Profit'].sum():,.0f}"
)

col3.metric(
    "📦 Units Sold",
    f"{int(df['Units'].sum()):,}"
)

col4.metric(
    "📊 Avg Margin",
    f"{df['Margin %'].mean():.2f}%"
)

# Division Performance
st.subheader("Division Performance")

if df.empty:
    st.warning("No data available")
else:
    division_profit = df.groupby("Division")["Gross Profit"].sum()
    division_margin = df.groupby("Division")["Margin %"].mean()

    fig4, ax4 = plt.subplots(figsize=(8,4))
    division_profit.plot(kind="bar", ax=ax4)
    ax4.set_title("Profit by Division")
    st.pyplot(fig4)

    fig5, ax5 = plt.subplots(figsize=(8,4))
    division_margin.plot(kind="bar", ax=ax5)
    ax5.set_title("Margin % by Division")
    st.pyplot(fig5)

st.subheader("Pareto Analysis (Top Profit Contributors)")

if df.empty:
    st.warning("No data available")
else:
    pareto = df.groupby("Product Name")["Gross Profit"].sum().sort_values(ascending=False).head(10)

    # cumulative %
    pareto_cum = pareto.cumsum() / pareto.sum() * 100

    fig, ax1 = plt.subplots(figsize=(10,5))

    # Bar chart (Profit)
    ax1.bar(pareto.index, pareto.values)
    ax1.set_ylabel("Profit")
    ax1.set_xticklabels(pareto.index, rotation=45, ha='right')

    # Line chart (Cumulative %)
    ax2 = ax1.twinx()
    ax2.plot(pareto.index, pareto_cum, color='red', marker='o')
    ax2.set_ylabel("Cumulative %")

    # ✅ Fix duplicate ticks
    ax2.set_yticks([0, 20, 40, 60, 80, 100])
    ax2.set_ylim(0, 100)

    # 80% line
    ax2.axhline(80, linestyle='--', color='green', label='80% Threshold')
    ax2.legend()

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    st.pyplot(fig)

st.subheader("Cost vs Sales Analysis")

if df.empty:
    st.warning("No data available")
else:
    fig7, ax7 = plt.subplots(figsize=(8,4))
    ax7.scatter(df["Cost"], df["Sales"])
    ax7.set_xlabel("Cost")
    ax7.set_ylabel("Sales")
    ax7.set_title("Cost vs Sales")
    st.pyplot(fig7)

date_range = st.sidebar.date_input("Select Date Range", [])

margin_filter = st.sidebar.slider("Select Min Margin %", 0, 100, 0)
df = df[df["Margin %"] >= margin_filter]

product_search = st.sidebar.text_input("Search Product")

if product_search:
    df = df[df["Product Name"].str.contains(product_search, case=False)]
