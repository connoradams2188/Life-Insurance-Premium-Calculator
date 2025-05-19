import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import lifelib as lib

st.set_page_config(page_title="Premium Calculator", layout="wide")
st.title("Data Table Visualization Page")
if "uploaded_df" in st.session_state:
    df = st.session_state(["uploaded_df"])
else:
    df = pd.read_csv("ActuarialProject/MortTable.csv")
    interest_rate = 0.05
    v = 1 / (1 + interest_rate)


selected_insurance_plans = st.multiselect('Select Insurance Plan:',options=['Whole Life Insurance',
        '5-Year Deferred Whole Life Insurance','10-Year Term Insurance','20-Year Term Insurance','10-Year Deferred Whole Life Insurance',
        '20-Year Deferred Whole Life Insurance'],default='Whole Life Insurance')
selected_age = st.slider('Select Age:',20,100)
selected_benefit = st.slider('Select Benefit (Lump Sum for Life Insurance):',0,1000000,step=1000)
desired_yield = st.number_input("Enter the Desired Profit Margin(%):", step=1) / 100
yield_ratio = desired_yield + 1

def calculate_nsp_with_table(df, age, benefit, plan_name):
    row = df[df['x'] == age]

    if row.empty:
        return None

    if plan_name == 'Whole Life Insurance':
        Ax_value = row['Ax'].values[0]
        äx_value = row['äx'].values[0]
        nsp = benefit * (Ax_value / äx_value)
    elif plan_name == '10-Year Term Insurance':
        Ax_value = row['Ax:1̅0̅|'].values[0]
        äx_value = row['äx:1̅0̅|'].values[0]
        nsp = benefit * (Ax_value / äx_value)
    elif plan_name == '20-Year Term Insurance':
        Ax_value = row['Ax:2̅0̅|'].values[0]
        äx_value = row['äx:2̅0̅|'].values[0]
        nsp = benefit * (Ax_value / äx_value)
    elif plan_name == '5-Year Deferred Whole Life Insurance':
        Ax_value = df[df['x'] == (age + 5)]['Ax'].values[0]
        nex_value = row['5Ex'].values[0]
        DAx_value = Ax_value * nex_value
        äx_value = row['äx'].values[0]
        nsp = (DAx_value * benefit)/ äx_value
    elif plan_name == '10-Year Deferred Whole Life Insurance':
        Ax_value = df[df['x'] == (age + 10)]['Ax'].values[0]
        nex_value = row['10Ex'].values[0]
        DAx_value = Ax_value * nex_value
        äx_value = row['äx'].values[0]
        nsp = (DAx_value * benefit) / äx_value
    elif plan_name == '20-Year Deferred Whole Life Insurance':
        Ax_value = df[df['x'] == (age + 20)]['Ax'].values[0]
        nex_value = row['20Ex'].values[0]
        DAx_value = Ax_value * nex_value
        äx_value = row['äx'].values[0]
        nsp = (DAx_value * benefit) / äx_value

    else:
        return None


    return round(nsp, 2)


# Calculate premiums
premiums = {}
for plan in selected_insurance_plans:
    if "Whole Life" in plan:
        premiums[plan] = calculate_nsp_with_table(df, selected_age, selected_benefit, plan) * yield_ratio
    elif "10-Year Term" in plan:
        premiums[plan] = calculate_nsp_with_table(df, selected_age, selected_benefit, plan) * yield_ratio
    elif "20-Year Term" in plan:
        premiums[plan] = calculate_nsp_with_table(df, selected_age, selected_benefit, plan) * yield_ratio

# Display results
st.subheader("Annual Premium Calculation Results")
for plan, premium in premiums.items():
    st.write(f"**{plan}**: ${premium:,.2f}")
