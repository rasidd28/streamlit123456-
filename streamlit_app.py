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
    """Updated logic to handle structured NIRF JSON and fallback to text"""
    try:
        # Case 1: structured NIRF JSON
        if isinstance(response_data, dict) and "data" in response_data:
            insights = []

            for item in response_data["data"]:
                for category, details in item.items():
                    institute = details.get("institute_name", "Institute")
                    points = details.get("factual_points", [])

                    insights.append(f"### 📊 {category.upper()} Analysis for {institute}\n")

                    if category.lower() == "rpc":
                        insights.append(
                            "Research & Professional Practice plays a major role in NIRF ranking.\n\n"
                            "Based on the data, the following improvements are recommended:\n"
                        )
                        insights.append(
                            "- Increase **industry-sponsored research projects**\n"
                            "- Encourage **faculty to apply for multi-agency grants**\n"
                            "- Improve **PhD graduation rate per year**\n"
                            "- Convert consultancy work into **high-value funded projects**\n"
                        )

                    elif category.lower() == "tlr":
                        insights.append(
                            "- Improve faculty–student ratio\n"
                            "- Recruit permanent faculty\n"
                            "- Strengthen laboratory infrastructure\n"
                        )

                    elif category.lower() == "go":
                        insights.append(
                            "- Improve placement percentage\n"
                            "- Track higher studies data\n"
                            "- Strengthen alumni outcome reporting\n"
                        )

                    elif category.lower() == "oi":
                        insights.append(
                            "- Increase female enrollment\n"
                            "- Improve regional diversity\n"
                            "- Support economically weaker students\n"
                        )

                    elif category.lower() == "pr":
                        insights.append(
                            "- Improve national perception through publications\n"
                            "- Increase visibility in rankings, hackathons, MOOCs\n"
                            "- Strengthen alumni & employer feedback\n"
                        )

                    insights.append("\n🔍 Reference Data Used:\n")
                    for p in points[:5]:
                        insights.append(f"- {p}")

            return "\n".join(insights)

        # Case 2: normal text
        if isinstance(response_data, dict):
            return response_data.get("response") or response_data.get("message") or response_data.get("output") or response_data.get("text") or json.dumps(response_data, indent=2)

        if isinstance(response_data, str):
            try:
                # Attempt to parse nested stringified JSON
                parsed = json.loads(response_data)
                return parse_bot_response(parsed)
            except:
                return response_data

        return str(response_data)

    except Exception as e:
        return f"⚠️ Parsing error: {str(e)}"

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
        
        with st.spinner("🤔 Analyzing deep NIRF metrics (this may take a minute)..."):
            try:
                payload = {
                    "sessionId": session_id,
                    "message": user_input,
                    "context": "NIRF ranking improvement analysis"
                }
                
                response = requests.post(
                    "https://rahulllllllllllllllll.app.n8n.cloud/webhook/37b860de-9c3b-4e77-85b5-54bd05c0771f",
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
                st.error("⏱️ Request timed out after 3 minutes. The analysis is taking longer than expected.")
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
