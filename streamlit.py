import streamlit as st
import requests
import uuid

st.set_page_config(page_title="AI Chatbot", layout="centered")
st.title("AI Chatbot")

# We create one session ID per Streamlit run
# (This ensures conversation memory works)
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

session_id = st.session_state.session_id

user_input = st.chat_input("Ask something...")

if user_input:
    payload = {
        "sessionId": session_id,
        "message": user_input
    }

    response = requests.post(
        "https://rahulsiddhu200528.app.n8n.cloud/webhook-test/5b5249d1-86af-4066-be82-510562045f9e",
        json=payload
    )

    # Parse bot reply
    try:
        bot_reply = response.json().get("response", response.json())
    except:
        bot_reply = "Error: Server didn't return JSON"

    # Show messages
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        st.write(bot_reply)
