import requests
import pandas as pd

CENSUS_API_KEY = "7679476e9ab35b13c3eb6215edefdf7f801a313c"
FRED_API_KEY = "e5cf75f23c4555263fbdc15d94a42dc8"

def get_census_data():
    url = f"https://api.census.gov/data/2022/acs/acs5?get=NAME,B25064_001E,B19013_001E,B25077_001E&for=state:*&key={CENSUS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df.rename(columns={
        "NAME": "state",
        "B25064_001E": "median_rent",
        "B19013_001E": "median_income",
        "B25077_001E": "median_home_value"
    })
    df = df.drop(columns=["state_code"] if "state_code" in df.columns else [])
    return df

def get_fred_data():
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id=CSUSHPISA&api_key={FRED_API_KEY}&file_type=json"
    response = requests.get(url)
    data = response.json()
    observations = data["observations"]
    df = pd.DataFrame(observations)
    df = df[["date", "value"]]
    df = df.rename(columns={"value": "home_price_index"})
    df = df.tail(1)
    return df

def calculate_roi(census_df, fred_df):
    df = census_df.copy()
    df["median_rent"] = pd.to_numeric(df["median_rent"], errors="coerce")
    df["median_income"] = pd.to_numeric(df["median_income"], errors="coerce")
    df["median_home_value"] = pd.to_numeric(df["median_home_value"], errors="coerce")
    df["rent_yield"] = (df["median_rent"] * 12) / df["median_home_value"]
    df["affordability"] = df["median_income"] / df["median_home_value"]
    df["roi_score"] = (df["rent_yield"] * 0.6) + (df["affordability"] * 0.4)
    df = df.sort_values("roi_score", ascending=False)
    df["rank"] = range(1, len(df) + 1)
    return df[["rank", "state", "median_rent", "median_income", "median_home_value", "rent_yield", "affordability", "roi_score"]]

if __name__ == "__main__":
    census_df = get_census_data()
    fred_df = get_fred_data()
    final_df = calculate_roi(census_df, fred_df)
    print(final_df.head(10))