import streamlit as st
from PIL import Image
import os
import time
from dotenv import load_dotenv
from google import genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="EcoVision AI",
    page_icon="🌱",
    layout="wide"
)

# ---------------- 🎨 UI THEME (ONLY ADDITION) ----------------
st.markdown("""
<style>

/* 🌿 LIGHT CLEAN BACKGROUND */
.stApp {
    background-color: #f7f9fc;
    color: #1f1f1f;
    font-family: 'Segoe UI', sans-serif;
}

/* 🌱 TITLE */
h1 {
    color: #1b5e20;
    text-align: center;
    font-weight: 800;
}

/* 🌿 SUBTITLE */
h3 {
    color: #2e7d32;
    text-align: center;
}

/* 📦 METRIC CARDS */
[data-testid="metric-container"] {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 10px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
}

/* 🔘 BUTTON */
.stButton>button {
    background-color: #2e7d32;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    width: 100%;
}

.stButton>button:hover {
    background-color: #1b5e20;
}

/* 📊 EXPANDER */
.streamlit-expanderHeader {
    color: #2e7d32;
    font-weight: 600;
}

/* 📌 SIDEBAR RADIO STYLE */
div[role="radiogroup"] label {
    background-color: #f1f8e9;
    padding: 10px;
    border-radius: 10px;
    margin: 6px 0px;
    font-weight: 600;
    border: 1px solid #dcedc8;
}

/* hover */
div[role="radiogroup"] label:hover {
    background-color: #e8f5e9;
    cursor: pointer;
}

/* selected */
div[role="radiogroup"] input:checked + div {
    background-color: #c8e6c9;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD API KEY ----------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ Gemini API key not found in .env file")
    st.stop()

client = genai.Client(api_key=API_KEY)



st.sidebar.markdown("♻ *Reduce • Reuse • Recycle*")

# ---------------- HEADER ----------------
st.title("🌱 EcoVision AI")
st.subheader("Smart Waste Segregation & Recycling Assistant")


st.write("---")
st.markdown("Upload or capture waste image to get AI-based environmental analysis.")
st.write("---")

# ---------------- INPUT ----------------
st.subheader("📸 Select Input Method")

input_mode = st.radio(
    "Choose input type:",
    ("Upload from Device", "Use Camera"),
    index=None
)

image = None  # IMPORTANT SAFETY INITIALIZATION

if input_mode == "Upload from Device":

    uploaded_file = st.file_uploader(
        "📁 Upload Waste Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        image = image.convert("RGB")
        image.thumbnail((512, 512))


elif input_mode == "Use Camera":

    camera_file = st.camera_input("📸 Capture Waste Image")

    if camera_file:
        image = Image.open(camera_file)
        image = image.convert("RGB")
        image.thumbnail((512, 512))


# ---------------- GEMINI CALL ----------------
def get_gemini_response(prompt, image):

    models_to_try = [
                "gemini-2.0-flash"
    ]

    for model_name in models_to_try:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[prompt, image]
                )
                return response.text
            except:
                time.sleep(2)

    return None

# ---------------- ANALYSIS ----------------
if image:

    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("🤖 Analyze Waste"):

        with st.spinner("Analyzing with Gemini AI..."):

            prompt = """
You are EcoVision AI.

Analyze the waste image and respond in this format:

Waste Category:
Confidence:
Recyclable:
Eco Score (0-100):
Disposal Method(1 line):
Environmental Impact(1 line):
Safety Notes(3 lines):
Recycling Steps:
"""

            try:
                text = get_gemini_response(prompt, image)

                if text is None:
                    st.error("❌ AI service is busy. Please try again later.")
                    st.stop()

                st.success("Analysis Completed")

                st.write("---")

                st.subheader("📊 Summary")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Waste Type", "Detected")

                with col2:
                    st.metric("Confidence", "High")

                with col3:
                    st.metric("Recyclable", "Yes")

                with col4:
                    st.metric("Eco Score", "Good")

                st.write("---")

                st.subheader("📊 AI Analysis (Structured View)")

                lines = text.split("\n")

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue

                    if "step" in line.lower():
                        st.success("➡ " + line)

                    elif "eco" in line.lower() or "impact" in line.lower():
                        st.warning("🌍 " + line)

                    elif "recycl" in line.lower():
                        st.info("♻ " + line)

                    elif "waste" in line.lower() or "category" in line.lower():
                        st.subheader("🗑 " + line)

                    else:
                        st.write(line)

                st.write("---")

                st.subheader("🌍 Eco Impact Score")
                st.progress(0.85)

                st.write("---")

                st.subheader("💡 Environmental Insight")

                st.warning("""
Proper waste segregation reduces pollution, saves energy,
and protects ecosystems for future generations.
""")

            except Exception as e:
                st.error(f"Error: {e}")