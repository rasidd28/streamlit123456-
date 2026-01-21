import streamlit as st
import requests
import uuid
import json
import time
from typing import Generator
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="NIRF Ranking Improvement Advisor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for better aesthetics
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin: 5px 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        border: 2px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        color: white;
    }
    .info-box {
        background: rgba(29, 78, 216, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #1d4ed8;
        margin: 10px 0;
    }
    .warning-box {
        background: rgba(220, 38, 38, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #dc2626;
        margin: 10px 0;
    }
    .success-box {
        background: rgba(22, 163, 74, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #16a34a;
        margin: 10px 0;
    }
    h1 {
        background: linear-gradient(120deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    </style>
""", unsafe_allow_html=True)

# Title with gradient effect
st.markdown("# 🎓 NIRF Ranking Improvement Advisor")
st.markdown("*AI-Powered Analysis for Academic Excellence*")
st.divider()

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "session_start" not in st.session_state:
    st.session_state.session_start = datetime.now()

session_id = st.session_state.session_id

# Sidebar
with st.sidebar:
    st.markdown("### 📊 NIRF Parameters")
    with st.expander("🔍 Parameter Weights", expanded=False):
        st.markdown("""
        - **TLR**: 30% (Teaching, Learning & Resources)
        - **RP**: 30% (Research & Professional Practice)
        - **GO**: 20% (Graduation Outcomes)
        - **OI**: 10% (Outreach & Inclusivity)
        - **PR**: 10% (Perception)
        """)
    st.divider()
    st.markdown("### ⚡ Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📈 TLR Tips", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Give me actionable tips to improve TLR score"})
            st.rerun()
    with col2:
        if st.button("🔬 RP Guide", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "How to improve Research & Professional Practice score?"})
            st.rerun()
    
    st.divider()
    st.metric("Queries Asked", st.session_state.query_count)
    if st.button("🔄 Clear Chat History", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.query_count = 0
        st.session_state.session_start = datetime.now()
        st.rerun()

# Logic for Parsing (The Fix)
def parse_bot_response(response_data):
    """Enhanced parsing with correct dictionary indexing"""
    try:
        if isinstance(response_data, dict) and "data" in response_data:
            insights = []

            for item in response_data["data"]:
                # --- FIXED SECTION ---
                institute = item.get("institute_name", "Institute")
                category = item.get("Nirf_category", "General")
                points = item.get("factual_points", [])
                
                # Header with institute name
                insights.append(f"## 📊 {category.upper()} Analysis\n")
                insights.append(f"**Institution:** {institute}\n\n")

                # Custom formatting based on category
                cat_lower = category.lower()
                if cat_lower in ["rpc", "rp"]:
                    insights.append("> 🔬 **Research & Professional Practice - Key Priority**\n\n")
                    insights.append("### 🎯 Strategic Improvements\n\n")
                    insights.append("#### 1️⃣ Industry Collaboration\n- Target partnerships with leading companies\n\n")
                    # (Other category specific items can stay here)
                
                elif cat_lower == "tlr":
                    insights.append("> 👨‍🏫 **Teaching, Learning & Resources**\n\n")
                
                # Reference data section
                if points:
                    insights.append("---\n### 📋 Reference Data Points\n\n")
                    for i, p in enumerate(points[:6], 1):
                        insights.append(f"**{i}.** {p.strip()}\n\n")
                
                insights.append("---\n\n")

            return "".join(insights)

        # Fallback for simple text responses
        if isinstance(response_data, dict):
            return response_data.get("response") or json.dumps(response_data, indent=2)
        
        return str(response_data)

    except Exception as e:
        return f'<div class="warning-box">⚠️ Parsing error: {str(e)}</div>'

def stream_response(text: str) -> Generator[str, None, None]:
    for word in text.split():
        yield word + " "
        time.sleep(0.015)

# Main Chat Interface
col_main, col_info = st.columns([2, 1])

with col_main:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("💬 Ask about NIRF ranking improvements...")
    if user_input:
        st.session_state.query_count += 1
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("🔍 Analyzing NIRF metrics..."):
                try:
                    payload = {"sessionId": session_id, "message": user_input}
                    response = requests.post("https://rahulllllllllllllllll.app.n8n.cloud/webhook/37b860de-9c3b-4e77-85b5-54bd05c0771f", json=payload, timeout=180)
                    
                    if response.status_code == 200:
                        bot_reply = parse_bot_response(response.json())
                        full_response = ""
                        for chunk in stream_response(bot_reply):
                            full_response += chunk
                            message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        st.error(f"Error {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {e}")

# Welcome Card
if not st.session_state.messages:
    with col_main:
        st.markdown("""
            <div class="metric-card">
                <h2>👋 Welcome to NIRF Ranking Advisor!</h2>
                <p>I can help you analyze parameters and suggest strategies to improve your academic ranking.</p>
            </div>
        """, unsafe_allow_html=True)
