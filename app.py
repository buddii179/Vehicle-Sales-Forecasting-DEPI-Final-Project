import streamlit as st
import pandas as pd
import joblib
from PIL import Image

# Load the trained model
try:
    model = joblib.load("best_xgb_pipeline.joblib")
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    st.stop()

# Dictionary of models per make
make_models = {
    'Acura': ['ILX', 'MDX', 'TSX', 'TL', 'RDX', 'ZDX', 'RL', 'RLX'],
    'Audi': ['A4', 'A6', 'Q5', 'A3', 'A8', 'Q7', 'TT', 'R8'],
    'BMW': ['3 Series', '5 Series', 'X5', 'X3', '7 Series', 'X1', 'X6'],
    'Chevrolet': ['Cruze', 'Malibu', 'Impala', 'Camaro', 'Silverado', 'Tahoe'],
    'Ford': ['Fusion', 'Focus', 'F-150', 'Mustang', 'Explorer', 'Escape'],
    'Honda': ['Accord', 'Civic', 'CR-V', 'Pilot', 'Odyssey'],
    'Hyundai': ['Sonata', 'Elantra', 'Santa Fe', 'Tucson', 'Genesis'],
    'Kia': ['Sorento', 'Optima', 'Sportage', 'Rio', 'Forte'],
    'Mercedes-Benz': ['C-Class', 'E-Class', 'S-Class', 'GLC', 'GLE'],
    'Nissan': ['Altima', 'Sentra', 'Rogue', 'Pathfinder', 'Maxima'],
    'Toyota': ['Camry', 'Corolla', 'RAV4', 'Highlander', 'Tacoma'],
    'Volkswagen': ['Jetta', 'Passat', 'Tiguan', 'Atlas', 'Golf']
}

# Page configuration
st.set_page_config(page_title="Car Price Prediction App", layout="wide")

# Custom CSS styling
st.markdown("""
<style>
.big-font {
    font-size:18px !important;
    text-align: center;
}
.header {
    color: #2a9df4;
    text-align: center;
}
.stSelectbox, .stTextInput, .stNumberInput, .stSlider {
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# Page Header
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown('<h1 class="header">Car Price Prediction App</h1>', unsafe_allow_html=True)
    st.markdown('<p class="big-font">Enter car details to predict the price using an AI model</p>', unsafe_allow_html=True)
    st.markdown("---")

# Default values for static input fields
DEFAULT_VALUES = {
    'vin': '1HGCM82633A123456',
    'trim': 'Base',
    'seller': 'Private',
    'interior': 'Black',
    'state': 'CA',
    'mmr': 15000.0  # Fixed mmr
}

# Split the interface into two columns
col1, col2 = st.columns(2)

with col1:
    st.header(" Basic Information")
    make = st.selectbox("Make", sorted(make_models.keys()), index=0)
    if make in make_models:
        model_name = st.selectbox("Model", make_models[make])
    else:
        model_name = st.text_input("Model", "Enter model")

    body = st.selectbox("Body Type", ['Sedan', 'SUV', 'Truck', 'Coupe', 'Convertible', 'Hatchback'])
    year = st.number_input("Year", min_value=1980, max_value=2025, value=2018, step=1)

with col2:
    st.header("⚙️ Technical Specifications")
    transmission = st.selectbox("Transmission", ['Automatic', 'Manual', 'CVT', 'Dual-Clutch'])
    condition = st.slider("Car Condition (1 = Worst, 5 = Best)", 1.0, 5.0, 3.0, 0.5)
    odometer = st.number_input("Odometer (Miles)", min_value=0.0, max_value=500000.0, value=50000.0, step=1000.0)
    color = st.selectbox("Exterior Color", ['White', 'Black', 'Silver', 'Gray', 'Red', 'Blue', 'Green'])

# Create DataFrame from user inputs and static values
input_df = pd.DataFrame({
    'year': [year],
    'make': [make],
    'model': [model_name],
    'trim': [DEFAULT_VALUES['trim']],
    'body': [body],
    'transmission': [transmission],
    'vin': [DEFAULT_VALUES['vin']],
    'state': [DEFAULT_VALUES['state']],
    'condition': [condition],
    'odometer': [odometer],
    'color': [color],
    'interior': [DEFAULT_VALUES['interior']],
    'seller': [DEFAULT_VALUES['seller']],
    'mmr': [DEFAULT_VALUES['mmr']]
})

# Preview input data
st.markdown("---")
st.header("📊 Input Data Preview")

expander = st.expander("Show entered data")
with expander:
    dynamic_columns = ['year', 'make', 'model', 'body', 'transmission', 'condition', 'odometer', 'color']
    st.dataframe(input_df[dynamic_columns].style.highlight_max(axis=0), use_container_width=True)

# Prediction button
st.markdown("---")
st.header(" Price Prediction")

if st.button("Predict Car Price", type="primary"):
    with st.spinner('Processing input and predicting price...'):
        try:
            prediction = model.predict(input_df)
            st.balloons()
            st.success(f"""
            ### ✅ Final Predicted Price:

            **${prediction[0]:,.2f}**

            *Based on the entered specifications*
            """)
        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
</div>
""", unsafe_allow_html=True)
