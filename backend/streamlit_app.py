import streamlit as st
import requests

st.set_page_config(
    page_title="CareCircle Assistant",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 CareCircle Assistant")

st.caption(
    "Smart Healthcare Chatbot for Emergency, Queue, Appointment and Navigation Support"
)

# CHAT HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR
with st.sidebar:

    st.header("CareCircle Features")

    st.write("🚨 Emergency Detection")
    st.write("⏳ Queue Tracking")
    st.write("📅 Appointment Support")
    st.write("🧭 Hospital Navigation")
    st.write("👨‍⚕️ Doctor Recommendation")
    st.write("💳 Billing & Insurance")
    st.write("🧪 Lab Report Support")

    st.warning(
        "This chatbot does not diagnose disease or prescribe medicine."
    )

    st.divider()

    st.success("CareCircle Hospital Network")

    st.caption(
        "Providing smart healthcare assistance with queue tracking, emergency support and navigation."
    )

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()
# DISPLAY OLD CHAT
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

# IMPORTANT FIX
user_input = None

# QUICK BUTTONS
st.subheader("Quick Questions")

col1, col2 = st.columns(2)

with col1:

    if st.button("🚨 Emergency Help"):
        user_input = "I need emergency help"

    elif st.button("⏳ Queue Status"):
        user_input = "What is my queue status?"

    elif st.button("📅 Book Appointment"):
        user_input = "Book appointment"

with col2:

    if st.button("🧭 Find MRI Room"):
        user_input = "Where is MRI room?"

    elif st.button("👨‍⚕️ Find Doctor"):
        user_input = "I need heart doctor"

    elif st.button("💳 Billing Help"):
        user_input = "Do you support UPI payment?"

# CHAT INPUT
typed_input = st.chat_input("Ask CareCircle Assistant...")

if typed_input:
    user_input = typed_input

# PROCESS USER MESSAGE
if user_input:

    # USER MESSAGE
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):

        st.write(user_input)

    # API REQUEST
    try:

        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"message": user_input}
        )

        bot_reply = response.json()["reply"]

    except:

        bot_reply = (
            "Backend server is not running. "
            "Please start FastAPI server first."
        )

    # BOT RESPONSE
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": bot_reply
        }
    )

    with st.chat_message("assistant"):

        st.write(bot_reply)
