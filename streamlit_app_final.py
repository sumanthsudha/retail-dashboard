
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
df = pd.read_csv("BSS_Retail_Cleaned.csv")
df['salesdate'] = pd.to_datetime(df['salesdate'])
df = df[df['unitsordered'] != 0]
df['avg_price_per_unit'] = df['sales'] / df['unitsordered']

# Title and Problem Statement
st.title("Retail Pricing and Sales Analysis Dashboard")

st.header("Project Overview")
st.markdown("""
This project explores the relationship between product pricing, units ordered, and total sales in a retail environment. 
By leveraging transactional sales data, the goal is to uncover patterns in bulk purchasing behavior and volume-based discounts, 
ultimately supporting data-driven recommendations for pricing and promotional strategies.
""")

st.subheader("Data Processing Summary")
st.markdown("""
- **Handled Missing Values**:
  - Dropped columns with more than 30% missing data.
  - Imputed missing values in numerical columns using the **median**.
  - Imputed missing values in categorical columns using the **mode**.

- **Handled Outliers**:
  - Used the **Interquartile Range (IQR)** method to detect and optionally cap extreme values.
  - Removed rows where `unitsordered` was 0 to avoid divide-by-zero errors.

- **Feature Engineering**:
  - Converted `salesdate` to datetime format for time-based filtering.
  - Created `avg_price_per_unit = sales / unitsordered` to analyze pricing efficiency.

- **Filtering Capabilities**:
  - Enabled interactive filtering by **date range** and a toggle to view **hypothesis testing results**.
""")



# Sidebar filters
st.sidebar.header("Filter Options")
min_date = df['salesdate'].min().date()
max_date = df['salesdate'].max().date()

date_range = st.sidebar.slider("Select Date Range:",
                               min_value=min_date,
                               max_value=max_date,
                               value=(min_date, max_date),
                               format="DD MMM YYYY")

show_hypothesis = st.sidebar.checkbox("Show Hypothesis Testing", value=False)

# Filter data based on date
filtered_df = df[(df['salesdate'].dt.date >= date_range[0]) & 
                 (df['salesdate'].dt.date <= date_range[1])]

# Data Exploration
st.header("Data Exploration")

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
st.header("Insights")
st.markdown("""
- Most products are priced under the median, with a right-skewed distribution.
- A clear inverse trend between quantity ordered and average unit price confirms bulk discounting.
- Units ordered and sales are strongly correlated.
""")

# Hypothesis Testing Section
if show_hypothesis:
    st.header("Hypothesis Testing")
    st.markdown("""
    **Null Hypothesis (H₀):** There is no significant difference in average price per unit for small vs. large orders.  
    **Alternative Hypothesis (H₁):** The average price per unit is lower for large orders.

    - T-Statistic: 11.598  
    - P-Value: 0.00000  

  Result: Since p < 0.05, we reject H₀. Large orders do have significantly lower average unit prices.
    """)

# Recommendations Section
st.header("Recommendations")
st.markdown("""
- Introduce tiered pricing based on order size to capitalize on bulk buyer behavior.
- Use customer segmentation to tailor discount strategies for high-volume purchasers.
- Promote best-performing SKUs in larger bundles or seasonal offers.
""")
