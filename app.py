import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Nassau Candy Product Profitability Dashboard")

# Load dataset
df = pd.read_csv("datasets/clean_nassau_candy_data.csv")

# =========================
# DATA PROCESSING
# =========================
df["Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100
df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

division_filter = st.sidebar.selectbox("Select Division", ["All"] + list(df["Division"].unique()))

if division_filter != "All":
    df = df[df["Division"] == division_filter]

# =========================
# KPI SECTION
# =========================
st.subheader("Key Performance Indicators")

total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
avg_margin = df["Margin %"].mean()
profit_per_unit = df["Profit per Unit"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"{total_sales:,.0f}")
col2.metric("Total Profit", f"{total_profit:,.0f}")
col3.metric("Avg Margin %", f"{avg_margin:.2f}%")
col4.metric("Profit per Unit", f"{profit_per_unit:.2f}")

# =========================
# DATASET PREVIEW
# =========================
st.subheader("Dataset Preview")
st.write(df.head())

# =========================
# TOP PRODUCTS
# =========================
top_products = df.groupby("Product Name")["Gross Profit"].sum().sort_values(ascending=False).head(10)

st.subheader("Top 10 Profitable Products")

fig1, ax1 = plt.subplots(figsize=(10,5))
top_products.plot(kind="bar", ax=ax1)
plt.xticks(rotation=60)
plt.tight_layout()

st.pyplot(fig1)

# =========================
# DIVISION ANALYSIS
# =========================
division_profit = df.groupby("Division")["Gross Profit"].sum()

st.subheader("Profit by Division")

fig4, ax4 = plt.subplots()
division_profit.plot(kind="bar", ax=ax4)

st.pyplot(fig4)

# =========================
# REGION PROFIT
# =========================
region_profit = df.groupby("Region")["Gross Profit"].sum()

st.subheader("Profit by Region")

fig2, ax2 = plt.subplots()
region_profit.plot(kind="bar", ax=ax2)

st.pyplot(fig2)

# =========================
# COST VS SALES
# =========================
st.subheader("Cost vs Sales Analysis")

fig5, ax5 = plt.subplots()
ax5.scatter(df["Cost"], df["Sales"])

plt.xlabel("Cost")
plt.ylabel("Sales")

st.pyplot(fig5)

# =========================
# UNITS VS PROFIT
# =========================
st.subheader("Units vs Profit Relationship")

fig3, ax3 = plt.subplots()
ax3.scatter(df["Units"], df["Gross Profit"])

plt.xlabel("Units Sold")
plt.ylabel("Gross Profit")

st.pyplot(fig3)

# =========================
# PARETO ANALYSIS
# =========================
st.subheader("Pareto Analysis (Top Profit Contributors)")

pareto = df.groupby("Product Name")["Gross Profit"].sum().sort_values(ascending=False)
pareto_cum = pareto.cumsum() / pareto.sum()

fig6, ax6 = plt.subplots()
pareto_cum.plot(ax=ax6)

plt.ylabel("Cumulative Profit %")

st.pyplot(fig6)
