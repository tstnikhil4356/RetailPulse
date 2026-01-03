import streamlit as st
import polars as pl
import plotly.express as px

st.title("🛒 RetailPulse - Customer Segmentation Dashboard")

# Load RFM data
rfm = pl.read_csv('data/processed/rfm_scores.csv')

# Display summary
st.header("📊 Customer Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Customers", f"{len(rfm):,}")
with col2:
    st.metric("Avg RFM Score", f"{rfm['RFM_score'].mean():.0f}")
with col3:
    st.metric("Top Spenders", f"${rfm['monetary'].sum():,.0f}")

# Show data
st.header("📋 Customer Scores")
st.dataframe(rfm.head(20))

# RFM Score Distribution
st.header("📈 RFM Score Distribution")
fig = px.histogram(rfm.to_pandas(), x='RFM_score', nbins=30,
                   title='Customer Distribution by RFM Score')
st.plotly_chart(fig)

# Customer Segments
st.header("👥 Customer Segments")

# Define segments based on RFM score
def segment_customer(score):
    if score >= 12000:
        return "Champions"
    elif score >= 9000:
        return "Loyal"
    elif score >= 6000:
        return "Potential"
    elif score >= 3000:
        return "At Risk"
    else:
        return "Lost"

rfm = rfm.with_columns(
    pl.col('RFM_score').map_elements(segment_customer, return_dtype=pl.Utf8).alias('segment')
)

# Show segment counts
segment_counts = rfm.group_by('segment').agg(pl.len().alias('count'))
fig2 = px.pie(segment_counts.to_pandas(), values='count', names='segment',
              title='Customer Segments')
st.plotly_chart(fig2)