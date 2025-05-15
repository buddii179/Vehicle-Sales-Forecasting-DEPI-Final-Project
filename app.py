import streamlit as st
import pandas as pd
import joblib
from PIL import Image

# تحميل النموذج المدرب
try:
    model = joblib.load("best_xgb_pipeline.joblib")
except Exception as e:
    st.error(f"حدث خطأ في تحميل النموذج: {str(e)}")
    st.stop()

# قاموس يحتوي على الموديلات لكل مصنع
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

# إعداد الصفحة
st.set_page_config(page_title="🚗 تطبيق توقع أسعار السيارات", layout="wide")

# تنسيق CSS مخصص
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

# رأس الصفحة
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown('<h1 class="header">🚗 تطبيق توقع أسعار السيارات</h1>', unsafe_allow_html=True)
    st.markdown('<p class="big-font">أدخل تفاصيل السيارة للحصول على توقع السعر باستخدام نموذج الذكاء الاصطناعي</p>', unsafe_allow_html=True)
    st.markdown("---")

# القيم الثابتة للمدخلات غير الضرورية
DEFAULT_VALUES = {
    'vin': '1HGCM82633A123456',
    'trim': 'Base',
    'seller': 'Private',
    'interior': 'Black',
    'state': 'CA',
    'mmr': 15000.0  # mmr ثابت
}

# تقسيم الواجهة إلى أعمدة
col1, col2 = st.columns(2)

with col1:
    st.header("🧩 المعلومات الأساسية")
    make = st.selectbox("الصنع", sorted(make_models.keys()), index=0)
    if make in make_models:
        model_name = st.selectbox("الموديل", make_models[make])
    else:
        model_name = st.text_input("الموديل", "أدخل الموديل")

    body = st.selectbox("نوع الهيكل", ['Sedan', 'SUV', 'Truck', 'Coupe', 'Convertible', 'Hatchback'])
    year = st.number_input("سنة الصنع", min_value=1980, max_value=2025, value=2018, step=1)

with col2:
    st.header("⚙️ المواصفات الفنية")
    transmission = st.selectbox("ناقل الحركة", ['Automatic', 'Manual', 'CVT', 'Dual-Clutch'])
    condition = st.slider("حالة السيارة (1 = الأسوأ, 5 = الأفضل)", 1.0, 5.0, 3.0, 0.5)
    odometer = st.number_input("عداد المسافة (ميل)", min_value=0.0, max_value=500000.0, value=50000.0, step=1000.0)
    color = st.selectbox("لون الخارجي", ['White', 'Black', 'Silver', 'Gray', 'Red', 'Blue', 'Green'])

# إنشاء DataFrame بالإدخالات مع القيم الثابتة
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

# عرض البيانات المدخلة
st.markdown("---")
st.header("📊 معاينة البيانات")

expander = st.expander("عرض البيانات المدخلة ")
with expander:
    dynamic_columns = ['year', 'make', 'model', 'body', 'transmission', 'condition', 'odometer', 'color']
    st.dataframe(input_df[dynamic_columns].style.highlight_max(axis=0), use_container_width=True)

# زر التنبؤ
st.markdown("---")
st.header("🔮 توقع السعر")

if st.button("توقع سعر السيارة", type="primary"):
    with st.spinner('جاري معالجة البيانات وتوقع السعر...'):
        try:
            prediction = model.predict(input_df)
            st.balloons()
            st.success(f"""
            ### ✅ التوقع النهائي لسعر السيارة:

            **${prediction[0]:,.2f}**

            *بناءً على المواصفات المدخلة*
            """)
        except Exception as e:
            st.error(f"حدث خطأ أثناء التنبؤ: {str(e)}")

# تذييل
st.markdown("---")
st.markdown("""
<div class="footer">
</div>
""", unsafe_allow_html=True)
