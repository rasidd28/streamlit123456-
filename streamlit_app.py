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

# Initialize session state with enhanced tracking
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "session_start" not in st.session_state:
    st.session_state.session_start = datetime.now()

session_id = st.session_state.session_id

# Enhanced Sidebar
with st.sidebar:
    st.markdown("### 📊 NIRF Parameters")
    
    # Parameter weightages
    with st.expander("🔍 Parameter Weights", expanded=False):
        st.markdown("""
        - **TLR**: 30% (Teaching, Learning & Resources)
        - **RP**: 30% (Research & Professional Practice)
        - **GO**: 20% (Graduation Outcomes)
        - **OI**: 10% (Outreach & Inclusivity)
        - **PR**: 10% (Perception)
        """)
    
    st.divider()
    
    # Quick action buttons
    st.markdown("### ⚡ Quick Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📈 TLR Tips", use_container_width=True):
            st.session_state.messages.append({
                "role": "user", 
                "content": "Give me actionable tips to improve TLR score"
            })
            st.rerun()
    
    with col2:
        if st.button("🔬 RP Guide", use_container_width=True):
            st.session_state.messages.append({
                "role": "user", 
                "content": "How to improve Research & Professional Practice score?"
            })
            st.rerun()
    
    if st.button("🎯 GO Strategy", use_container_width=True):
        st.session_state.messages.append({
            "role": "user", 
            "content": "What strategies can improve Graduation Outcomes?"
        })
        st.rerun()
    
    st.divider()
    
    # Session statistics
    st.markdown("### 📊 Session Stats")
    st.metric("Queries Asked", st.session_state.query_count)
    
    session_duration = datetime.now() - st.session_state.session_start
    minutes = int(session_duration.total_seconds() / 60)
    st.metric("Session Duration", f"{minutes} min")
    
    st.divider()
    
    # Clear chat button with confirmation
    if st.button("🔄 Clear Chat History", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.query_count = 0
        st.session_state.session_start = datetime.now()
        st.rerun()
    
    st.divider()
    st.caption(f"Session ID: `{session_id[:8]}...`")

# Main content area with columns
col_main, col_info = st.columns([2, 1])

with col_info:
    st.markdown("""
        <div class="info-box">
            <h4>💡 Pro Tips</h4>
            <ul>
                <li>Be specific about your institution</li>
                <li>Mention current rankings if known</li>
                <li>Ask about specific parameters</li>
                <li>Request comparative analysis</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Example queries
    with st.expander("📝 Example Queries", expanded=False):
        st.markdown("""
        - "Analyze TLR parameters for IIT Madras"
        - "How to improve research publications?"
        - "Compare my institute with top 10"
        - "What are quick wins for ranking?"
        - "Industry collaboration strategies"
        """)

with col_main:
    # Display chat history
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def parse_bot_response(response_data):
    """Enhanced parsing with better formatting"""
    try:
        # Case 1: structured NIRF JSON
        if isinstance(response_data, dict) and "data" in response_data:
            insights = []

            for item in response_data["data"]:
                for category, details in item.items():
                    institute = details.get("institute_name", "Institute")
                    points = details.get("factual_points", [])

                    insights.append(f"### 📊 {category.upper()} Analysis - {institute}\n")

                    if category.lower() == "rpc" or category.lower() == "rp":
                        insights.append(
                            '<div class="success-box">'
                            "<strong>🔬 Research & Professional Practice - Key Priority</strong><br/>"
                            "This parameter contributes 30% to your NIRF ranking."
                            "</div>\n"
                        )
                        insights.append("#### 🎯 Recommended Improvements:\n")
                        insights.append(
                            "1. **Industry Collaboration**: Increase industry-sponsored research projects by 25%\n"
                            "2. **Grant Applications**: Encourage faculty to apply for multi-agency grants (DST, SERB, DBT)\n"
                            "3. **PhD Output**: Improve PhD graduation rate - target 15+ per year\n"
                            "4. **Consultancy Revenue**: Convert consultancy work into high-value funded projects (₹10L+)\n"
                            "5. **Publications**: Focus on Q1 journals and high-impact conferences\n"
                            "6. **Patents**: File and publish at least 5 patents annually\n"
                        )

                    elif category.lower() == "tlr":
                        insights.append(
                            '<div class="info-box">'
                            "<strong>👨‍🏫 Teaching, Learning & Resources</strong>"
                            "</div>\n"
                        )
                        insights.append("#### 🎯 Action Items:\n")
                        insights.append(
                            "1. **Faculty-Student Ratio**: Maintain 1:15 or better\n"
                            "2. **Permanent Faculty**: Increase percentage of permanent faculty to 75%+\n"
                            "3. **Infrastructure**: Upgrade laboratory and computing facilities\n"
                            "4. **Digital Resources**: Subscribe to premium e-journals and databases\n"
                            "5. **Expenditure**: Increase per-student expenditure on teaching-learning\n"
                        )

                    elif category.lower() == "go":
                        insights.append(
                            '<div class="success-box">'
                            "<strong>🎓 Graduation Outcomes - 20% Weightage</strong>"
                            "</div>\n"
                        )
                        insights.append("#### 🎯 Strategies:\n")
                        insights.append(
                            "1. **Placements**: Target 85%+ placement rate with median salary ₹6L+\n"
                            "2. **Higher Studies**: Track and report students pursuing MS/PhD\n"
                            "3. **Entrepreneurship**: Support student startups and count as outcomes\n"
                            "4. **Alumni Tracking**: Implement robust alumni database system\n"
                            "5. **Career Services**: Strengthen training and placement cell\n"
                        )

                    elif category.lower() == "oi":
                        insights.append(
                            '<div class="info-box">'
                            "<strong>🌍 Outreach & Inclusivity</strong>"
                            "</div>\n"
                        )
                        insights.append("#### 🎯 Focus Areas:\n")
                        insights.append(
                            "1. **Gender Diversity**: Increase female enrollment to 30%+\n"
                            "2. **Regional Diversity**: Admit students from diverse states (15+ states)\n"
                            "3. **Economic Support**: Provide scholarships to economically weaker sections\n"
                            "4. **Facilities**: Ensure differently-abled friendly infrastructure\n"
                            "5. **Community Engagement**: Organize outreach programs and workshops\n"
                        )

                    elif category.lower() == "pr":
                        insights.append(
                            '<div class="warning-box">'
                            "<strong>👁️ Perception - Often Overlooked!</strong>"
                            "</div>\n"
                        )
                        insights.append("#### 🎯 Visibility Boosters:\n")
                        insights.append(
                            "1. **Publications**: Ensure visibility in peer-reviewed journals\n"
                            "2. **Rankings**: Participate in domain-specific rankings and competitions\n"
                            "3. **MOOCs**: Develop and offer online courses on NPTEL/Swayam\n"
                            "4. **Events**: Host national conferences and hackathons\n"
                            "5. **Media**: Increase media presence and research highlights\n"
                            "6. **Alumni**: Strengthen alumni network and testimonials\n"
                        )

                    if points:
                        insights.append("\n#### 📋 Reference Data Points:\n")
                        for i, p in enumerate(points[:5], 1):
                            insights.append(f"{i}. {p}\n")

                    insights.append("\n---\n")

            return "\n".join(insights)

        # Case 2: normal text response
        if isinstance(response_data, dict):
            return (response_data.get("response") or 
                    response_data.get("message") or 
                    response_data.get("output") or 
                    response_data.get("text") or 
                    json.dumps(response_data, indent=2))

        if isinstance(response_data, str):
            try:
                parsed = json.loads(response_data)
                return parse_bot_response(parsed)
            except:
                return response_data

        return str(response_data)

    except Exception as e:
        return f'<div class="warning-box">⚠️ Parsing error: {str(e)}</div>'

def stream_response(text: str) -> Generator[str, None, None]:
    """Smooth streaming animation"""
    words = text.split()
    for word in words:
        yield word + " "
        time.sleep(0.015)

# Chat input
with col_main:
    user_input = st.chat_input("💬 Ask about NIRF ranking improvements...")

    if user_input:
        st.session_state.query_count += 1
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            with st.spinner("🔍 Analyzing NIRF metrics and generating insights..."):
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
                            message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)
                        
                        message_placeholder.markdown(full_response, unsafe_allow_html=True)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                        
                        # Success notification
                        st.success("✅ Analysis complete!")
                        
                    else:
                        error_msg = f'<div class="warning-box">⚠️ Server returned status code {response.status_code}. Please try again.</div>'
                        message_placeholder.markdown(error_msg, unsafe_allow_html=True)

                except requests.exceptions.Timeout:
                    error_msg = '<div class="warning-box">⏱️ Request timed out after 3 minutes. The analysis is taking longer than expected. Please try a more specific query.</div>'
                    message_placeholder.markdown(error_msg, unsafe_allow_html=True)
                    
                except requests.exceptions.ConnectionError:
                    error_msg = '<div class="warning-box">🔌 Connection error. Please check your internet connection and try again.</div>'
                    message_placeholder.markdown(error_msg, unsafe_allow_html=True)
                    
                except Exception as e:
                    error_msg = f'<div class="warning-box">❌ An unexpected error occurred: {str(e)}</div>'
                    message_placeholder.markdown(error_msg, unsafe_allow_html=True)

    # Welcome message
    if len(st.session_state.messages) == 0:
        st.markdown("""
            <div class="metric-card">
                <h2 style="color: white; margin-top: 0;">👋 Welcome to NIRF Ranking Advisor!</h2>
                <p style="font-size: 1.1em; margin-bottom: 0;">
                    I'm your AI assistant for NIRF ranking improvement strategies. I can help you:
                </p>
                <ul style="font-size: 1em; line-height: 1.8;">
                    <li>🔍 Analyze specific NIRF parameters</li>
                    <li>📊 Identify gaps in current performance</li>
                    <li>💡 Suggest actionable improvement strategies</li>
                    <li>📈 Provide benchmark comparisons</li>
                    <li>🎯 Create customized action plans</li>
                </ul>
                <p style="margin-top: 15px; font-size: 0.95em; opacity: 0.9;">
                    Ask me anything about improving your institution's NIRF ranking!
                </p>
            </div>
        """, unsafe_allow_html=True)

# Footer
with col_main:
    st.divider()
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    
    with footer_col1:
        st.caption(f"🔐 Session: `{session_id[:12]}...`")
    with footer_col2:
        st.caption(f"💬 Queries: {st.session_state.query_count}")
    with footer_col3:
        st.caption(f"⏱️ Started: {st.session_state.session_start.strftime('%H:%M')}")
