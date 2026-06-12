import streamlit as st

st.set_page_config(
    page_title="Eco Quiz",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 EcoVision AI Quiz")
st.subheader("Test your Environmental Awareness")

st.write("---")

# ---------------- SCORE TRACKING ----------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = {}

# ---------------- QUESTIONS ----------------
questions = [
    {
        "q": "Which waste is biodegradable?",
        "options": ["Plastic", "Glass", "Organic", "Metal"],
        "answer": "Organic",
        "explanation": "Organic waste decomposes naturally and is eco-friendly."
    },
    {
        "q": "Which waste is most harmful to oceans?",
        "options": ["Paper", "Plastic", "Wood", "Cloth"],
        "answer": "Plastic",
        "explanation": "Plastic takes hundreds of years to degrade and harms marine life."
    },
    {
        "q": "E-waste contains which harmful substances?",
        "options": ["Sugar", "Lead & Mercury", "Water", "Salt"],
        "answer": "Lead & Mercury",
        "explanation": "E-waste contains toxic heavy metals harmful to humans and soil."
    },
    {
        "q": "Best way to manage metal waste?",
        "options": ["Burn it", "Throw in river", "Recycle", "Bury underground"],
        "answer": "Recycle",
        "explanation": "Metals are highly recyclable and save energy when reused."
    },
    {
        "q": "Which is NOT recyclable easily?",
        "options": ["Glass", "Plastic", "Paper", "Clean Metal"],
        "answer": "Plastic",
        "explanation": "Some plastics are hard to recycle and cause pollution."
    }
]

# ---------------- QUIZ UI ----------------
for i, item in enumerate(questions):

    st.subheader(f"Q{i+1}. {item['q']}")

    # ✅ NO DEFAULT SELECTION
    selected = st.radio(
        "Select your answer:",
        item["options"],
        index=None,
        key=f"q{i}"
    )

    # ---------------- SUBMIT ----------------
    if st.button(f"Submit Answer {i+1}"):

        if selected is None:
            st.warning("⚠️ Please select an answer first")
        elif i in st.session_state.answered:
            st.info("You already answered this question")
        else:
            if selected == item["answer"]:
                st.success("✅ Correct Answer!")
                st.session_state.score += 1
            else:
                st.error("❌ Wrong Answer")

            st.info(f"💡 Explanation: {item['explanation']}")

            st.session_state.answered[i] = True

    st.write("---")

# ---------------- FINAL SCORE ----------------
st.subheader("🏆 Your Score")

st.success(f"Final Score: {st.session_state.score} / {len(questions)}")

if st.session_state.score == len(questions):
    st.balloons()
    st.success("Excellent! You're an Eco Expert 🌱")
elif st.session_state.score >= 3:
    st.info("Good job! You have decent environmental awareness 👍")
else:
    st.warning("Keep learning! Try the Awareness page 🌍")
