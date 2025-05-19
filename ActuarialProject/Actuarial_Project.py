import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import lifelib as lib

st.set_page_config(page_title="Data Uploader & Cleaner", layout="wide")
st.title("📊 Data Preparation App")
st.markdown("Upload your dataset (CSV, Excel, or JSON) to begin data analysis.")

# File uploader
uploaded_file = st.file_uploader("Upload a data file", type=["csv", "xlsx", "xls", "json"])


# Define function to load data
@st.cache_data
def load_data(file):
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        elif file.name.endswith((".xlsx", ".xls")):
            return pd.read_excel(file)
        elif file.name.endswith(".json"):
            return pd.read_json(file)
        else:
            return None
    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
        return None


# Load and display data
if uploaded_file:
    df = load_data(uploaded_file)
    st.session_state["uploaded_df"] = df
    if df is not None:
        st.success("✅ File uploaded and read successfully!")
        st.subheader("📌 Dataset Preview")
        st.dataframe(df.head())

        st.subheader("🧹 Data Cleaning Options")

        # Drop rows with missing values
        if st.checkbox("Drop rows with any missing values"):
            df = df.dropna()

        # Convert column to datetime
        date_cols = df.select_dtypes(include='object').columns
        if len(date_cols) > 0:
            col_to_convert = st.selectbox("Convert a column to datetime (optional):",
                                          options=["None"] + list(date_cols))
            if col_to_convert != "None":
                df[col_to_convert] = pd.to_datetime(df[col_to_convert], errors='coerce')

        # Display basic stats
        st.subheader("📈 Basic Data Overview")
        st.write("Shape:", df.shape)
        st.write("Column Types:")
        st.write(df.dtypes)
        st.write("Summary Statistics:")
        st.write(df.describe(include='all'))

        # Export cleaned data
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Cleaned Data", data=csv, file_name="cleaned_data.csv", mime="text/csv")
    else:
        st.warning("⚠️ Unable to load data. Please check your file format.")
else:
    st.info("Default Table is Mortality Table with 5% Interest Rate")

