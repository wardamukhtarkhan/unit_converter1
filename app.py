import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Smart Unit Converter", page_icon="🔄")

# Define unit conversion factors
unit_types = {
    'length': {
        'meters': 1,
        'kilometers': 1000,
        'centimeters': 0.01,
        'millimeters': 0.001,
        'miles': 1609.34,
        'yards': 0.9144,
        'feet': 0.3048,
        'inches': 0.0254
    },
    'weight': {
        'kilograms': 1,
        'grams': 0.001,
        'milligrams': 0.000001,
        'pounds': 0.453592,
        'ounces': 0.0283495,
        'tons': 1000
    },
    'temperature': {
        'celsius': 'C',
        'fahrenheit': 'F',
        'kelvin': 'K'
    },
    'speed': {
        'meters/second': 1,
        'kilometers/hour': 0.277778,
        'miles/hour': 0.44704,
        'feet/second': 0.3048,
        'knots': 0.514444
    }
}

# Simple CSS
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("Unit Converter")

# Unit type selector
unit_type = st.selectbox("Select Unit Type", options=list(unit_types.keys()))

# Create columns for input and output
col1, col2, col3 = st.columns([4, 1, 4])

with col1:
    from_value = st.number_input("From Value", value=0.0)
    from_unit = st.selectbox("From Unit", options=list(unit_types[unit_type].keys()), key="from")

with col2:
    if st.button("⇄"):
        if 'last_from' not in st.session_state:
            st.session_state.last_from = from_value
            st.session_state.last_unit_from = from_unit

with col3:
    to_unit = st.selectbox("To Unit", options=list(unit_types[unit_type].keys()), key="to")

# Conversion function
def convert_temperature(value, from_unit, to_unit):
    # Convert to Celsius first
    if from_unit == 'celsius':
        celsius = value
    elif from_unit == 'fahrenheit':
        celsius = (value - 32) * 5/9
    else:  # kelvin
        celsius = value - 273.15
    
    # Convert from Celsius to target unit
    if to_unit == 'celsius':
        return celsius
    elif to_unit == 'fahrenheit':
        return (celsius * 9/5) + 32
    else:  # kelvin
        return celsius + 273.15

# Perform conversion
if from_value is not None:
    if unit_type == 'temperature':
        result = convert_temperature(from_value, from_unit, to_unit)
        formula = f"{from_value}°{unit_types[unit_type][from_unit]} → {result:.2f}°{unit_types[unit_type][to_unit]}"
    else:
        from_factor = unit_types[unit_type][from_unit]
        to_factor = unit_types[unit_type][to_unit]
        result = (from_value * from_factor) / to_factor
        formula = f"{from_value} {from_unit} = {result:.4f} {to_unit}"
    
    # Display result and formula
    st.success(f"Result: {result:.4f} {to_unit}")
    st.info(formula)
