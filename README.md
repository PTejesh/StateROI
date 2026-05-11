# StateROI — Real Estate Investment ROI Analyzer

A data-driven platform that ranks all 50 U.S. states by projected real estate investment ROI using live government data.

## What it does
- Pulls housing, income, and rental data from the U.S. Census Bureau API
- Fetches national home price index data from the FRED (Federal Reserve) API
- Calculates an ROI score for each state based on rent yield and affordability
- Displays results in an interactive Streamlit dashboard with a sortable table and bar chart

## Tech Stack
Python, Pandas, Streamlit, Census API, FRED API

## How to run
```bash
pip install pandas streamlit requests
streamlit run app.py
```
