
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
df = pd.read_csv("BSS_Retail_Cleaned.csv")
df['salesdate'] = pd.to_datetime(df['salesdate'])
df = df[df['unitsordered'] != 0]
df['avg_price_per_unit'] = df['sales'] / df['unitsordered']

# Title
st.title("📊 Retail Sales Analysis Dashboard")

# Introduction
st.header("📌 Introduction")
st.markdown("""
This dashboard analyzes retail sales data to explore pricing patterns, quantity trends, and the relationship between bulk orders and unit pricing.
The goal is to uncover data-driven insights that can improve pricing strategies and customer segmentation.
""")

# Sidebar filter
st.sidebar.header("📅 Filter by Date Range")
min_date = df['salesdate'].min().date()
max_date = df['salesdate'].max().date()
date_range = st.sidebar.slider("Select Date Range:", min_date, max_date, (min_date, max_date))

# Filtered data
filtered_df = df[(df['salesdate'].dt.date >= date_range[0]) & 
                 (df['salesdate'].dt.date <= date_range[1])]

# Data Exploration Section
st.header("📊 Data Exploration")

# Visual 1: Price Distribution
st.subheader("Price Distribution")
fig1, ax1 = plt.subplots()
sns.histplot(filtered_df['price'], bins=30, kde=True, ax=ax1)
st.pyplot(fig1)

# Visual 2: Units Ordered vs Avg Price Per Unit
st.subheader("Units Ordered vs Avg Price Per Unit")
fig2, ax2 = plt.subplots()
sns.scatterplot(x='unitsordered', y='avg_price_per_unit', data=filtered_df, ax=ax2)
st.pyplot(fig2)

# Visual 3: Correlation Heatmap
st.subheader("Correlation Heatmap")
fig3, ax3 = plt.subplots()
corr = filtered_df[['price', 'unitsordered', 'sales', 'avg_price_per_unit']].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax3)
st.pyplot(fig3)

# Insights Section
st.header("🔍 Insights")
st.markdown("""
- The distribution of product prices is right-skewed, with most items priced at the lower end.
- A negative relationship exists between the number of units ordered and average price per unit, indicating volume discounts.
- Strong correlation is observed between units ordered and total sales, as expected.
""")

# Recommendations Section
st.header("✅ Recommendations")
st.markdown("""
- Consider offering more structured volume-based pricing to further boost high-quantity sales.
- Use price segmentation to target customer groups based on average order size.
- Monitor high-selling SKUs for potential bundling or promotion strategies.
""")
