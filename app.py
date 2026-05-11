import streamlit as st
import pandas as pd
from data import get_census_data, get_fred_data, calculate_roi

st.set_page_config(page_title="StateROI", layout="wide")

st.title("StateROI — Real Estate Investment Analyzer")
st.subheader("Ranking all 50 U.S. states by projected investment ROI")

with st.spinner("Loading data..."):
    census_df = get_census_data()
    fred_df = get_fred_data()
    df = calculate_roi(census_df, fred_df)

# fix duplicate state column
df = df.loc[:, ~df.columns.duplicated()]

top_state = df.iloc[0]["state"]
top_score = round(df.iloc[0]["roi_score"], 4)

st.metric("Top State", top_state)
st.metric("Top ROI Score", top_score)

st.dataframe(df, use_container_width=True)

st.bar_chart(df.set_index("state")["roi_score"])