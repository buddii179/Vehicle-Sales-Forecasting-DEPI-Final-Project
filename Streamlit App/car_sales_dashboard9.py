import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Car Sales Dashboard", layout="wide")
sns.set(style="whitegrid")

st.title("🚗 Car Sales Dashboard")

@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()  # Remove extra spaces
    # Rename Price column if needed
    if 'Price' in df.columns and 'car_prices' not in df.columns:
        df.rename(columns={'Price': 'car_prices'}, inplace=True)
    # Convert Date column to datetime, handle errors by coercing
    if 'Date' in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    else:
        st.error("CSV file missing 'Date' column.")
        st.stop()
    return df.dropna(subset=["Date"])

def find_and_rename_lat_lon(df):
    possible_lat_names = ['latitude', 'lat', 'latitudes']
    possible_lon_names = ['longitude', 'long', 'lng', 'lon', 'longitudes']

    lat_col = None
    lon_col = None

    for col in df.columns:
        if col.lower() in possible_lat_names:
            lat_col = col
            break

    for col in df.columns:
        if col.lower() in possible_lon_names:
            lon_col = col
            break

    if lat_col and lon_col:
        df = df.rename(columns={lat_col: 'Latitude', lon_col: 'Longitude'})
    else:
        lat_col, lon_col = None, None

    return df, lat_col, lon_col

uploaded_file = st.file_uploader("Upload your car sales CSV file", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)

    if df.empty:
        st.error("Uploaded file does not contain valid 'Date' data.")
        st.stop()

    # Check required columns
    required_cols = ['Brand', 'Model', 'car_prices']
    for col in required_cols:
        if col not in df.columns:
            st.error(f"CSV file must contain '{col}' column.")
            st.stop()

    # Sidebar filters
    st.sidebar.header("Filters")

    # Brands filter
    brands = df['Brand'].unique()
    selected_brands = st.sidebar.multiselect("Select Brand(s)", brands, default=brands)

    filtered_df = df[df['Brand'].isin(selected_brands)]

    if filtered_df.empty:
        st.warning("No data available for the selected brands.")
        st.stop()

    # Date range filter
    min_date = filtered_df["Date"].min().date()
    max_date = filtered_df["Date"].max().date()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Validate date_range
    if not (isinstance(date_range, (list, tuple)) and len(date_range) == 2):
        st.error("Please select a valid date range.")
        st.stop()

    start_date, end_date = date_range

    if start_date > end_date:
        st.error("Start date cannot be after end date.")
        st.stop()

    # Make sure start_date and end_date are timezone naive
    start_date = pd.to_datetime(start_date).tz_localize(None)
    end_date = pd.to_datetime(end_date).tz_localize(None)

    filtered_df = filtered_df[(filtered_df["Date"] >= start_date) &
                              (filtered_df["Date"] <= end_date)]

    if filtered_df.empty:
        st.warning("No data available for the selected date range.")
        st.stop()

    # Aggregation frequency
    freq = st.sidebar.selectbox("Aggregation Frequency", options=["Weekly", "Monthly"], index=0)
    resample_rule = 'W' if freq == "Weekly" else 'M'

    # Summary
    st.subheader("📋 Summary")
    total_sales = filtered_df["car_prices"].sum()
    total_records = len(filtered_df)
    st.markdown(f"- **Total Sales:** ${total_sales:,.2f}")
    st.markdown(f"- **Number of Records:** {total_records}")
    st.markdown(f"- **Date Range:** {start_date.date()} to {end_date.date()}")

    # Sales Over Time
    st.subheader(f"📈 Total {freq} Car Sales")
    sales_over_time = filtered_df.resample(resample_rule, on="Date")["car_prices"].sum()
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    sales_over_time.plot(ax=ax1, marker='o')
    ax1.set_ylabel("Total Sales ($)")
    ax1.set_xlabel("Date")
    ax1.set_title(f"Total Car Sales Over Time ({freq})")
    ax1.grid(True)
    st.pyplot(fig1)

    # Sales Growth %
    st.subheader("📊 Sales Growth Percentage Over Time")
    sales_pct_change = sales_over_time.pct_change().fillna(0) * 100
    fig_growth, ax_growth = plt.subplots(figsize=(10, 4))
    sales_pct_change.plot(ax=ax_growth, marker='o', color='orange')
    ax_growth.set_ylabel("Sales Growth (%)")
    ax_growth.set_xlabel("Date")
    ax_growth.set_title(f"Sales Growth Percentage Over Time ({freq})")
    ax_growth.axhline(0, color='gray', linestyle='--')
    st.pyplot(fig_growth)

    # Top Brands
    st.subheader("🏆 Top Brands by Total Sales")
    brand_sales = filtered_df.groupby("Brand")["car_prices"].sum().sort_values(ascending=False)
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(x=brand_sales.values, y=brand_sales.index, ax=ax2, palette="viridis")
    ax2.set_xlabel("Total Sales ($)")
    ax2.set_ylabel("Brand")
    ax2.set_title("Top Brands by Total Sales")
    st.pyplot(fig2)

    # Average Car Price
    st.subheader("💰 Average Car Price by Brand")
    avg_price = filtered_df.groupby("Brand")["car_prices"].mean().sort_values(ascending=False)
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.barplot(x=avg_price.values, y=avg_price.index, ax=ax3, palette="magma")
    ax3.set_xlabel("Average Price ($)")
    ax3.set_ylabel("Brand")
    ax3.set_title("Average Car Price by Brand")
    st.pyplot(fig3)

    # Popular Models
    st.subheader("🚘 Most Popular Car Models")
    model_counts = filtered_df["Model"].value_counts().head(10)
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.barplot(x=model_counts.values, y=model_counts.index, ax=ax4, palette="coolwarm")
    ax4.set_xlabel("Number of Sales")
    ax4.set_ylabel("Model")
    ax4.set_title("Top 10 Most Popular Car Models")
    st.pyplot(fig4)

    # Price Distribution
    st.subheader("📊 Car Price Distribution")
    fig5, ax5 = plt.subplots(figsize=(10, 4))
    sns.histplot(filtered_df["car_prices"], bins=20, kde=True, ax=ax5, color='skyblue')
    ax5.set_xlabel("Price ($)")
    ax5.set_title("Distribution of Car Prices")
    st.pyplot(fig5)

    # Correlation Heatmap
    st.subheader("📈 Correlation Heatmap")
    numeric_cols = filtered_df.select_dtypes(include='number').columns
    if len(numeric_cols) >= 2:
        corr = filtered_df[numeric_cols].corr()
        fig_corr, ax_corr = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax_corr)
        st.pyplot(fig_corr)
    else:
        st.info("Not enough numeric columns for correlation heatmap.")

    # Map Visualization
    st.subheader("🗌️ Sales Locations Map")
    filtered_df, lat_col, lon_col = find_and_rename_lat_lon(filtered_df)
    if lat_col and lon_col:
        map_df = filtered_df[['Latitude', 'Longitude', 'car_prices']].dropna(subset=['Latitude', 'Longitude'])
        if map_df.empty:
            st.info("No valid latitude and longitude data for map visualization.")
        else:
            map_df = map_df.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'})
            st.map(map_df[['latitude', 'longitude']])
    else:
        st.info("Latitude and Longitude columns not found for map visualization.")

    # Export
    st.subheader("📥 Export Filtered Data")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="filtered_car_sales.csv",
        mime="text/csv",
    )

else:
    st.warning("Please upload a CSV file to continue.")
