import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Nassau Candy Product Profitability Dashboard")

# Load dataset
df = pd.read_csv("clean_nassau_candy_data.csv")

st.subheader("Dataset Preview")
st.write(df.head())

# Top Products
top_products = df.groupby("Product Name")["Gross Profit"].sum().sort_values(ascending=False).head(10)

st.subheader("Top 10 Profitable Products")

fig1, ax1 = plt.subplots()
top_products.plot(kind="bar", ax=ax1)
plt.xticks(rotation=45)

st.pyplot(fig1)

# Region Profit
region_profit = df.groupby("Region")["Gross Profit"].sum()

st.subheader("Profit by Region")

fig2, ax2 = plt.subplots()
region_profit.plot(kind="bar", ax=ax2)

st.pyplot(fig2)

# Units vs Profit
st.subheader("Units vs Profit Relationship")

fig3, ax3 = plt.subplots()
ax3.scatter(df["Units"], df["Gross Profit"])

plt.xlabel("Units Sold")
plt.ylabel("Gross Profit")

st.pyplot(fig3)
