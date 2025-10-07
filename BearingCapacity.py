
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

settlement = False

idx = st.sidebar.number_input("Enter the angle of internal friction (0–50):", min_value=0, max_value=50, step=1)
shape = st.sidebar.selectbox("Select the footing with a given dimension:", options=["Strip", "Circular", "Square", "Rectangular"])
if shape == "Strip":
  B= st.sidebar.number_input("Enter the footing width (m.):", min_value=0.5, step=0.5)
  Sc = Sq = Sγ = 1.0
elif shape == "Square":
  B= st.sidebar.number_input("Enter the footing width (m.):", min_value=0.5, step=0.5)
  L = B
  Sc = 1.3 
  Sq= 1.0
  Sγ = 0.8
elif shape == "Circular":
  B= st.sidebar.number_input("Enter the footing diameter (m.):", min_value=0.5, step=0.5)
  Sc = 1.3 
  Sq= 1.0
  Sγ = 0.6
elif shape == "Rectangular":
  B= st.sidebar.number_input("Enter the footing Width (m.):", min_value=0.5, step=0.5)
  L= st.sidebar.number_input("Enter the footing Length (m.):", min_value=0.5, step=0.5)
  Sc = round(1.0 +0.3*(B/L),2)
  Sq= 1.0
  Sγ = round(1-0.2*(B/L),2)

c = st.sidebar.number_input("Enter cohesion (kPa):", min_value=0, step=10)
γ_s = st.sidebar.number_input("Unit weight of soil γ_s (kN/m³)", value=18.0, step=1.0, format="%.2f")
γ_sat = st.sidebar.number_input("Unit weight of saturated soil γ_sat (kN/m³)", value=18.0, step=1.0, format="%.2f")
d_f = st.sidebar.number_input("Foundation depth d_f (m)", min_value=0.0, value=0.00, step=0.1, format="%.2f")
d_wt = st.sidebar.number_input("Depth of Water Table (m)", min_value=0.0, value=50.00, step=0.1, format="%.2f")
FS= st.sidebar.number_input("Factor of Safety", value=2.0, step=0.5, format="%.1f")
st.sidebar.write(f"")
if shape == "Rectangular" or shape == "Square":
  settlement = st.sidebar.toggle("Do you want to compute for the settlement?")

if settlement:
  P = st.sidebar.number_input("Total axial load P (kN):", value=200.0, step=10.0, format="%.2f")
  u = st.sidebar.number_input("Poisson's Ratio u: ", value=0.05, step=0.01, format="%.2f")
  E = st.sidebar.number_input("Modulus of Elasticity E (MPa):", value=15.00, step=0.10, format="%.2f")
  I = st.sidebar.number_input("Influence Factor:", value=0.88, step=0.01, format="%.2f")
  H = st.sidebar.number_input("Thickness of stratum/clay H (m.):", value=1.0, step=0.1, format="%.2f")
  d_c = st.sidebar.number_input("Depth at the top of the stratum/clay (m.):", value=1.0, step=0.1, format="%.2f")
  γ_c = st.sidebar.number_input("Unit weight of saturated clay γ_c (kN/m³)", value=18.0, step=1.0, format="%.2f")
  if d_c < d_wt:
    st.sidebar.caption("Clay layer is partly not saturated:") 
    γ_cd = st.sidebar.number_input("Unit weight of unsaturated clay (kN/m³)", value=18.0, step=1.0, format="%.2f")
  Cc = st.sidebar.number_input("Compression Index Cc *(set to zero if LL is given)*:", value=0.5, step=0.05, format="%.2f")
  if Cc==0:
    LL = st.sidebar.number_input("Liquid Limit (LL):", value=20.0, step=1.0, format="%.2f")
    Cc= round(0.009*(LL-10),2)
    st.sidebar.write(f"*Cc: {Cc:.2f}*")  
  eo= st.sidebar.number_input("Initial void ratio eo:", value=1.0, step=0.1, format="%.2f")
  cons = st.sidebar.toggle("Normally Consolidated?")
  if not cons:
    Cs = st.sidebar.number_input("Swell Index Cs:", value=0.5, step=0.05, format="%.2f")
    Pc= st.sidebar.number_input("Pre-consolidated Pressure Pc (kPa):", value=100.00, step=10.0, format="%.2f")


# Define arrays
#idx = list(range(0, 51))

idx = int(idx)
Nc = [
  5.70,  6.00,  6.30,  6.62,  6.97,  7.34,  7.73,  8.15,  8.60,  9.09,
  9.61, 10.16, 10.76, 11.41, 12.11, 12.86, 13.68, 14.60, 15.62, 16.56,
 17.70, 18.92, 20.27, 21.75, 23.36, 25.13, 27.09, 29.14, 31.61, 34.24,
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

Nc= Nc[idx]
Nq= Nq[idx]
Nγ= Nγ[idx]


st.subheader("Terzaghi Bearing Capacity Equation")
st.write(f"*For Φ = {idx}, the bearing capacity factors are:*")
st.write(f"Nc = {Nc}")
st.write(f"Nq = {Nq}")
st.write(f"Nγ = {Nγ}")
st.write(f"")
st.write(f"*For {shape}, the shape factors are:*")
st.write(f"Sc = {Sc}")
st.write(f"Sq = {Sq}")
st.write(f"Sγ = {Sγ}")
st.write(f"")

if d_wt < d_f+B:
  st.write(f"*Considering the effect of the water table:*")
  if d_wt < d_f:  
    st.write(f"*Since the water table is above the footing:*")
    γ = γ_sat -9.81
    q = γ_s* d_wt+ γ* (d_f-d_wt)
  elif d_wt == d_f:
    st.write(f"*Since the water table is at the footing:*")
    γ = γ_sat -9.81
    q = γ_s* d_wt
  elif d_wt > d_f and d_wt < d_f+B:
    st.write(f"*Since the water table is less than B = {B} meters below the footing:*")
    q = γ_s* d_f
    H = 0.5*B*math.tan(math.radians(45+idx/2))
    γ = γ_s*(d_wt-d_f)/ (H**2)*(2*H-(d_wt-d_f))+(γ_sat -9.81)/(H**2)*(H-(d_wt-d_f))**2
    st.write(f"H = {H:.2f} m.")
else:
  q= γ_s * d_f
  γ = γ_s
st.write(f"q = {q:.2f} kPa")
st.write(f"γ = {γ:.2f} kN/m3")
st.write(f"")
st.write(f"Using the **Terzaghi Bearing Capacity Equation:**")
qu = c*Nc*Sc + q*Nq*Sq + 0.5*B*γ*Nγ*Sγ
qa = qu/FS
st.write(f"The ultimate bearing capacity is **qu = {qu:.2f} kPa.**")
st.write(f"The safe bearing capacity is **qa = {qa:.2f} kPa.**")

if settlement:
  st.subheader("Foundation Settlement")
  st.write(f"**IMMEDIATE SETTLEMENT**")
  pf = P / (B*L)
  st.write(f"Net pressure is **p = {pf:.2f} kPa.**")
  Hi= pf * B* (1-u**2)/(E)*I
  st.write(f"The immediate settlement is **ΔHi = {Hi:.2f} mm.**")
  st.write(f"")
  st.write(f"**PRIMARY CONSOLIDATED SETTLEMENT**")
  if d_wt<d_c:
    Po = γ_s*d_wt + (d_c-d_wt)*(γ_sat-9.81)+ (H/2)*(γ_c-9.81)
  elif d_wt < d_c + H:
    Po = γ_s*d_c + (d_wt-d_c)*γ_cd + (d_c + H - d_wt) * γ_c
  else:
    Po = γ_s*d_c + γ_cd * H

  st.write(f"Initial vertical effective soil stress at the clay's mid-height **7.2Po = {Po:.2f} kPa.**")
  st.write(f"*Solving for ΔP*")
  zt = d_c - d_f
  zm = d_c + H/2 - d_f
  zb = d_c + H - d_f
  st.write(f"zt = {zt:.2f} m., zm = {zm:.2f} m., and zb = {zb:.2f} m.")
  Pt= P/((B+zt)*(L+zt))
  Pm= P/((B+zm)*(L+zm))
  Pb= P/((B+zb)*(L+zb))
  st.write(f"Pt = {Pt:.2f} kPa, Pm = {Pm:.2f} kPa, and Pb = {Pb:.2f} kPa")
  ΔP = (Pt + Pb + 4*Pm)/ 6
  Pf= Po + ΔP
  st.write(f"The soil surcharge is ** ΔP = {ΔP:.2f} kPa.**")
  st.write(f"Final vertical effective soil stress of the clay ** Pf = {Pf:.2f} kPa.**")
  st.write(f"")
  if cons:
    st.write(f"*For normally consolidated soil:*")
    Hpc = H*1000 * Cc / (1 + eo) * math.log10(Pf/Po)

  st.write(f"The primary consolidated settlement is ** ΔHpc = {Hpc:.2f} mm.**")
  
  

