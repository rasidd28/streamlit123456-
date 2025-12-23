import streamlit as st
import requests
import uuid
import json
import time
from typing import Generator

# Page configuration
st.set_page_config(
    page_title="NIRF Ranking Improvement Advisor",
    page_icon="🎓",
    layout="centered"
)

# Custom CSS for animations and styling
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 10px;
    }
    .metric-card {
        background: transparent;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Title with icon
st.markdown("# 🎓 NIRF Ranking Improvement Advisor")
st.markdown("*Analyzing gaps, providing insights, and suggesting improvements*")
st.divider()

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

session_id = st.session_state.session_id

# Sidebar with information
with st.sidebar:
    st.markdown("### 📊 Focus Areas")
    st.markdown("""
    - **Teaching & Learning Resources** (TLR)
    - **Research & Professional Practice** (RP)
    - **Graduation Outcomes** (GO)
    - **Outreach & Inclusivity** (OI)
    - **Perception** (PR)
    """)
    
    st.divider()
    st.markdown("### 💡 How to Use")
    st.markdown("""
    1. Ask about specific NIRF parameters
    2. Request gap analysis
    3. Get actionable suggestions
    4. Discuss implementation strategies
    """)
    
    if st.button("🔄 Clear Chat History"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def parse_bot_response(response_data):
    """Parse and validate the bot response from various JSON formats"""
    try:
        if isinstance(response_data, dict):
            if "response" in response_data: return response_data["response"]
            elif "message" in response_data: return response_data["message"]
            elif "output" in response_data: return response_data["output"]
            elif "text" in response_data: return response_data["text"]
            else: return json.dumps(response_data, indent=2)
        elif isinstance(response_data, str):
            try:
                parsed = json.loads(response_data)
                return parse_bot_response(parsed)
            except json.JSONDecodeError:
                return response_data
        return str(response_data)
    except Exception as e:
        return f"⚠️ Error parsing response: {str(e)}"

def stream_response(text: str) -> Generator[str, None, None]:
    """Simulate streaming"""
    words = text.split()
    for word in words:
        yield word + " "
        time.sleep(0.02)

# Chat input
user_input = st.chat_input("Ask about NIRF ranking improvements...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # INCREASED TIMEOUT AND ROBUST ERROR HANDLING
        with st.spinner("🤔 Analyzing deep NIRF metrics (this may take a minute)..."):
            try:
                payload = {
                    "sessionId": session_id,
                    "message": user_input,
                    "context": "NIRF ranking improvement analysis"
                }
                
                # UPDATED: Timeout set to 180 seconds as requested
                response = requests.post(
                    "https://ronni123.app.n8n.cloud/webhook-test/37b860de-9c3b-4e77-85b5-54bd05c0771f",
                    json=payload,
                    timeout=180 
                )
                
                if response.status_code == 200:
                    bot_reply = parse_bot_response(response.json())
                    full_response = ""
                    for chunk in stream_response(bot_reply):
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error(f"⚠️ Server error ({response.status_code}). Please try again.")

            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out after 3 minutes. The analysis is taking longer than expected. Please try a more specific question.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

# Welcome message
if len(st.session_state.messages) == 0:
    st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1f77b4;">👋 Welcome to NIRF Ranking Advisor!</h3>
            <p>I can help you identify weaknesses and suggest strategies for improvement.</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.divider()
st.markdown(f"<div style='text-align: center; color: #666; font-size: 0.8em;'>Session: {session_id}</div>", unsafe_allow_html=True)


