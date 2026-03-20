import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(layout="wide")

st.title("Nassau Candy Product Profitability Dashboard")

# Load dataset
df = pd.read_csv("clean_nassau_candy_data.csv")

# =========================
# DATA PROCESSING
# =========================
df["Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100
df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("Filters")

division_filter = st.sidebar.selectbox(
    "Select Division",
    ["All"] + list(df["Division"].dropna().unique())
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
st.subheader("Dataset Preview")
st.dataframe(df.head())

# =========================
# TOP PRODUCTS
# =========================
top_products = (
    df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.subheader("📊 Top 10 Profitable Products")

fig1, ax1 = plt.subplots(figsize=(12,5))

top_products.plot(kind="bar", ax=ax1, color="skyblue")

style_plot(ax1)

ax1.set_title("Top 10 Products by Profit")
ax1.set_xlabel("Product Name")
ax1.set_ylabel("Gross Profit")

plt.xticks(rotation=60, ha='right')
plt.tight_layout()

st.pyplot(fig1)

# =========================
# REGION PROFIT
# =========================
region_profit = df.groupby("Region")["Gross Profit"].sum()

st.subheader("🌍 Profit by Region")

fig2, ax2 = plt.subplots(figsize=(10,4))

region_profit.plot(kind="bar", ax=ax2, color="orange")

style_plot(ax2)

ax2.set_title("Profit Distribution by Region")
ax2.set_xlabel("Region")
ax2.set_ylabel("Gross Profit")

plt.xticks(rotation=30)
plt.tight_layout()

st.pyplot(fig2)

# =========================
# UNITS VS PROFIT
# =========================
st.subheader("📈 Units vs Profit Relationship")

fig3, ax3 = plt.subplots(figsize=(10,5))

ax3.scatter(df["Units"], df["Gross Profit"], alpha=0.6)

style_plot(ax3)

ax3.set_xlabel("Units Sold")
ax3.set_ylabel("Gross Profit")
ax3.set_title("Units vs Profit")

plt.tight_layout()

st.pyplot(fig3)

# =========================
# KPI SECTION
# =========================
st.subheader("📌 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"{df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"{df['Gross Profit'].sum():,.0f}")
col3.metric("Avg Margin %", f"{df['Margin %'].mean():.2f}%")

# Division Performance
st.subheader("Division Performance")

division_profit = df.groupby("Division")["Gross Profit"].sum()
division_margin = df.groupby("Division")["Margin %"].mean()

# Profit chart
# Margin chart

st.subheader("Pareto Analysis (Top Profit Contributors)")

st.subheader("Cost vs Sales Analysis")

date_range = st.sidebar.date_input("Select Date Range", [])

margin_filter = st.sidebar.slider("Select Min Margin %", 0, 100, 0)
df = df[df["Margin %"] >= margin_filter]

product_search = st.sidebar.text_input("Search Product")

if product_search:
    df = df[df["Product Name"].str.contains(product_search, case=False)]
