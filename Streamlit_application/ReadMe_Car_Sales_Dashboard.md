# Car Sales Dashboard with Streamlit

## Overview
This is a web-based dashboard built using **Streamlit** that allows users to upload and analyze car sales data. The app provides interactive filters, various visualizations, and statistics to explore car sales trends, prices, and performance by brand and model.

---

## Features
- **File Upload**: Upload a CSV file with car sales data.
- **Filters**:
  - Select brands to focus on.
  - Filter by date range.
- **Visualizations**:
  - Sales over time (weekly/monthly).
  - Sales growth percentage.
  - Top selling brands.
  - Average car price by brand.
  - Most popular car models.
  - Car price distribution.
  - Correlation heatmap for numeric features.
  - Sales locations on a map (if latitude/longitude available).
- **Data Export**: Download the filtered data as a CSV file.

---

## Installation
1. Clone this repo or copy the `Streamlit_Application.py` file.
2. Install dependencies:
```bash
pip install streamlit pandas seaborn matplotlib
```
3. Run the Streamlit app:
```bash
streamlit run Streamlit_Application.py
```

---

## Code Explanation
### 1. **Imports & Configuration**
```python
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
```
- Load essential libraries for UI, data, and plots.

```python
st.set_page_config(page_title="Car Sales Dashboard", layout="wide")
st.title("🚗 Car Sales Dashboard")
```
- Sets up a wide layout and a page title.

---

### 2. **Load and Clean Data**
```python
@st.cache_data
def load_data(file):
```
- Loads CSV, removes whitespace in columns.
- Renames `Price` to `car_prices` if applicable.
- Converts `Date` column to datetime.
- Stops if `Date` is missing.

---

### 3. **Latitude/Longitude Handling**
```python
def find_and_rename_lat_lon(df):
```
- Standardizes column names for map plotting.

---

### 4. **UI Components**
```python
uploaded_file = st.file_uploader(...)
```
- Upload a `.csv` file.
- Check for required columns: `Brand`, `Model`, `car_prices`.

**Sidebar Filters**:
- Multiselect for brands.
- Date range input.
- Aggregation frequency: weekly or monthly.

---

### 5. **Visualizations**
1. **Sales Over Time** – total car sales per week or month.
2. **Sales Growth %** – percentage change between periods.
3. **Top Brands** – bar chart of brands with highest total sales.
4. **Average Car Price** – average price by brand.
5. **Popular Models** – top 10 most frequent models.
6. **Price Distribution** – histogram with KDE overlay.
7. **Correlation Heatmap** – numeric relationships.
8. **Map Visualization** – location of sales.

---

### 6. **Export Filtered Data**
```python
st.download_button(...)
```
- Download the displayed data as a CSV.

---

## Usage Tips
- Ensure your CSV contains columns like `Brand`, `Model`, `Price`, and `Date`.
- Include location data (`Latitude`, `Longitude`) for map support.
- Use sidebar filters to interactively explore your dataset.

---

## License
MIT

---

## Author
Built with ❤ by Gaafer Gouda
