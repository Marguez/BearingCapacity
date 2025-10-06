
# footing_app.py
import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="Bearing Capacity", layout="wide")
st.title("Bearing Capacity")

# ---------------------------
# Sidebar: Inputs
# ---------------------------
st.sidebar.header("Input parameters (SI units)")

idx = st.sidebar.number_input("Enter the angle of internal friction (0–50):", min_value=0, max_value=50, step=1)
P_D1 = st.sidebar.number_input("Dead axial load P_D1 (kN)", value=200.0, step=10.0, format="%.2f")


d_b_mm = st.sidebar.number_input("Main bar diameter d_b (mm)", min_value=6, value=16, step=1, format="%d")
cc_mm  = st.sidebar.number_input("Clear cover cc (mm)", min_value=5, value=50, step=1, format="%d")
st.sidebar.write(f"*Covering: {cc_mm + d_b_mm/2} mm.*")

# Define arrays
Φ = list(range(0, 51))

Nc = [
  5.70,  6.00,  6.30,  6.62,  6.97,  7.34,  7.73,  8.15,  8.60,  9.09,
  9.61, 10.16, 10.76, 11.41, 12.11, 12.86, 13.68, 14.60, 15.62, 16.56,
 17.69, 18.92, 20.27, 21.75, 23.36, 25.13, 27.09, 29.14, 31.61, 34.24,
 37.16, 40.41, 44.04, 48.09, 52.64, 57.75, 63.53, 70.01, 77.50, 85.97,
 95.66,106.81,119.67,134.58,151.95,172.28,196.22,224.55,258.28,298.71,
347.50
]

Nq = [
  1.00,  1.10,  1.22,  1.35,  1.49,  1.64,  1.81,  2.00,  2.21,  2.44,
  2.69,  2.98,  3.29,  3.63,  4.02,  4.45,  4.92,  5.45,  6.04,  6.70,
  7.44,  8.26,  9.19, 10.23, 11.40, 12.72, 14.21, 15.66, 17.81, 19.98,
 22.46, 25.25, 28.52, 32.23, 36.50, 41.44, 47.16, 53.80, 61.55, 70.61,
 81.27, 93.85,108.75,126.50,147.74,173.28,204.19,241.80,287.85,344.63,
415.14
]

Nγ = [
  0.00, 0.01, 0.04, 0.06, 0.10, 0.14, 0.20, 0.27, 0.35, 0.44,
  0.56, 0.69, 0.85, 1.04, 1.26, 1.52, 1.82, 2.18, 2.59, 3.07,
  3.64, 4.31, 5.09, 6.00, 7.08, 8.34, 9.84,11.73,13.70,16.18,
 19.13,22.65,26.87,31.44,38.00,45.41,54.36,65.27,78.61,95.03,
115.31,140.51,171.99,211.56,261.60,325.34,407.11,512.84,650.67,834.71,
1072.80
]



st.subheader("Corresponding Values")
st.write(f"For Φ = {Φ[idx]}")
st.write(f"Nc = {Nc[idx]}")
st.write(f"Nq = {Nq[idx]}")
st.write(f"Nγ = {Nγ[idx]}")
