import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Eco Awareness",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Environmental Awareness")

st.subheader("Understanding Waste Impact on Environment")

st.write("---")

# ---------------- DATA ----------------
data = [
    ["Plastic", "Harmful to oceans & wildlife", "Yes (Recyclable)"],
    ["Paper", "Biodegradable, low impact", "Yes (Recyclable)"],
    ["Glass", "Non-toxic but long-lasting", "Yes (Fully Recyclable)"],
    ["Metal", "Mining causes pollution, but recyclable", "Yes (Highly Recyclable)"],
    ["E-Waste", "Highly toxic (lead, mercury)", "Yes (Special recycling needed)"],
    ["Organic", "Biodegradable, eco-friendly", "Compostable"],
    ["Chemical Waste", "Severely toxic to soil & water", "Limited / Specialized"]
]

df = pd.DataFrame(data, columns=["Waste Type", "Environmental Impact", "Recyclability"])

# ---------------- TABLE ----------------
st.table(df)

st.write("---")

# ---------------- SIMPLE INFO SECTION ----------------
st.subheader("⚠ Key Environmental Insights")

col1, col2 = st.columns(2)

with col1:
    st.error("Plastic, E-waste and Chemicals are most harmful if mismanaged")

with col2:
    st.success("Organic and Paper waste are least harmful when handled properly")

st.write("---")

# ---------------- FOOTER MESSAGE ----------------
st.info("""
♻ Proper waste segregation reduces pollution  
🌱 Helps in recycling and reuse  
🌍 Protects ecosystems and biodiversity  
""")
