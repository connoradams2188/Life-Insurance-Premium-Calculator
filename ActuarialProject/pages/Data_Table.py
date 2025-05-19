import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import lifelib as lib

st.set_page_config(page_title="Data Table Visualization", layout="wide")
st.title("Data Table Visualization Page")
if "uploaded_df" in st.session_state:
    st.dataframe(st.session_state["uploaded_df"])
    df = st.session_state(["uploaded_df"])
else:
    df = pd.read_csv("ActuarialProject/MortTable.csv")
    st.dataframe(df)

