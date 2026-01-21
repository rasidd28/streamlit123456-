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
    """Enhanced parsing with refined, structured formatting"""
    try:
        # Case 1: structured NIRF JSON
        if isinstance(response_data, dict) and "data" in response_data:
            insights = []

            for item in response_data["data"]:
                for category, details in item.items():
                    institute = details.get("institute_name", "Institute")
                    points = details.get("factual_points", [])

                    # Header with institute name
                    insights.append(f"## 📊 {category.upper()} Analysis\n")
                    insights.append(f"**Institution:** {institute}\n\n")

                    if category.lower() == "rpc" or category.lower() == "rp":
                        # Importance box
                        insights.append("> 🔬 **Research & Professional Practice - Key Priority**  \n")
                        insights.append("> This parameter contributes **30%** to your NIRF ranking.\n\n")
                        
                        # Strategic improvements section
                        insights.append("### 🎯 Strategic Improvements\n\n")
                        
                        insights.append("#### 1️⃣ Industry Collaboration\n")
                        insights.append("- Increase industry-sponsored research projects by **25%**\n")
                        insights.append("- Target partnerships with leading companies in your domain\n")
                        insights.append("- Focus on projects worth **₹10L+**\n\n")
                        
                        insights.append("#### 2️⃣ Grant Applications\n")
                        insights.append("- Encourage faculty to apply for multi-agency grants:\n")
                        insights.append("  - DST (Department of Science & Technology)\n")
                        insights.append("  - SERB (Science & Engineering Research Board)\n")
                        insights.append("  - DBT (Department of Biotechnology)\n")
                        insights.append("- Target: **5+ new grants** per year\n\n")
                        
                        insights.append("#### 3️⃣ PhD Output\n")
                        insights.append("- Current goal: Improve PhD graduation rate\n")
                        insights.append("- **Target: 15+ PhD graduates per year**\n")
                        insights.append("- Streamline thesis submission processes\n\n")
                        
                        insights.append("#### 4️⃣ Consultancy Revenue\n")
                        insights.append("- Convert consultancy work into high-value funded projects\n")
                        insights.append("- Minimum project value: **₹10L+**\n")
                        insights.append("- Document all consultancy activities properly\n\n")
                        
                        insights.append("#### 5️⃣ Publications\n")
                        insights.append("- Focus on **Q1 journals** (high impact factor)\n")
                        insights.append("- Target high-impact conferences (IEEE, ACM, Springer)\n")
                        insights.append("- Encourage interdisciplinary collaborations\n\n")
                        
                        insights.append("#### 6️⃣ Patents\n")
                        insights.append("- File and publish at least **5 patents annually**\n")
                        insights.append("- Focus on both filed and published/granted patents\n")
                        insights.append("- Provide IP awareness training to faculty\n\n")

                    elif category.lower() == "tlr":
                        insights.append("> 👨‍🏫 **Teaching, Learning & Resources**  \n")
                        insights.append("> Weightage: **30%** of total NIRF score\n\n")
                        
                        insights.append("### 🎯 Action Items\n\n")
                        
                        insights.append("#### 1️⃣ Faculty-Student Ratio\n")
                        insights.append("- Maintain optimal ratio: **1:15 or better**\n")
                        insights.append("- Recruit additional qualified faculty\n\n")
                        
                        insights.append("#### 2️⃣ Permanent Faculty\n")
                        insights.append("- Target: **75%+** permanent faculty positions\n")
                        insights.append("- Convert contractual positions to permanent\n")
                        insights.append("- Hire faculty with PhD qualifications\n\n")
                        
                        insights.append("#### 3️⃣ Infrastructure Enhancement\n")
                        insights.append("- Upgrade laboratory facilities\n")
                        insights.append("- Modernize computing infrastructure\n")
                        insights.append("- Improve library and digital resources\n\n")
                        
                        insights.append("#### 4️⃣ Digital Resources\n")
                        insights.append("- Subscribe to premium e-journals (IEEE, Springer, Elsevier)\n")
                        insights.append("- Provide access to research databases\n")
                        insights.append("- Invest in e-learning platforms\n\n")
                        
                        insights.append("#### 5️⃣ Financial Investment\n")
                        insights.append("- Increase per-student expenditure on teaching-learning\n")
                        insights.append("- Allocate budget for faculty development programs\n\n")

                    elif category.lower() == "go":
                        insights.append("> 🎓 **Graduation Outcomes**  \n")
                        insights.append("> Weightage: **20%** of total NIRF score\n\n")
                        
                        insights.append("### 🎯 Strategic Focus\n\n")
                        
                        insights.append("#### 1️⃣ Placement Excellence\n")
                        insights.append("- Target placement rate: **85%+**\n")
                        insights.append("- Median salary goal: **₹6L+ per annum**\n")
                        insights.append("- Strengthen industry partnerships\n\n")
                        
                        insights.append("#### 2️⃣ Higher Studies Tracking\n")
                        insights.append("- Track students pursuing **MS/PhD programs**\n")
                        insights.append("- Document admissions to premier institutions\n")
                        insights.append("- Maintain updated alumni database\n\n")
                        
                        insights.append("#### 3️⃣ Entrepreneurship Support\n")
                        insights.append("- Count student startups as positive outcomes\n")
                        insights.append("- Provide incubation support\n")
                        insights.append("- Offer entrepreneurship courses\n\n")
                        
                        insights.append("#### 4️⃣ Alumni Network\n")
                        insights.append("- Implement robust alumni tracking system\n")
                        insights.append("- Regular alumni engagement programs\n")
                        insights.append("- Document career progression\n\n")
                        
                        insights.append("#### 5️⃣ Career Services\n")
                        insights.append("- Strengthen Training & Placement Cell\n")
                        insights.append("- Conduct regular skill development workshops\n")
                        insights.append("- Industry mentorship programs\n\n")

                    elif category.lower() == "oi":
                        insights.append("> 🌍 **Outreach & Inclusivity**  \n")
                        insights.append("> Weightage: **10%** of total NIRF score\n\n")
                        
                        insights.append("### 🎯 Focus Areas\n\n")
                        
                        insights.append("#### 1️⃣ Gender Diversity\n")
                        insights.append("- Target female enrollment: **30%+**\n")
                        insights.append("- Create women-friendly campus environment\n")
                        insights.append("- Implement specific women support programs\n\n")
                        
                        insights.append("#### 2️⃣ Regional Diversity\n")
                        insights.append("- Admit students from **15+ different states**\n")
                        insights.append("- Promote national-level awareness campaigns\n")
                        insights.append("- Participate in centralized counseling\n\n")
                        
                        insights.append("#### 3️⃣ Economic Support\n")
                        insights.append("- Scholarships for economically weaker sections\n")
                        insights.append("- Fee waivers and financial aid programs\n")
                        insights.append("- Government scheme participation (EWS, OBC)\n\n")
                        
                        insights.append("#### 4️⃣ Accessibility\n")
                        insights.append("- Differently-abled friendly infrastructure\n")
                        insights.append("- Ramps, elevators, and assistive technologies\n")
                        insights.append("- Dedicated support cell\n\n")
                        
                        insights.append("#### 5️⃣ Community Engagement\n")
                        insights.append("- Organize outreach programs and workshops\n")
                        insights.append("- Rural and urban community initiatives\n")
                        insights.append("- Social responsibility projects\n\n")

                    elif category.lower() == "pr":
                        insights.append("> 👁️ **Perception - Often Overlooked!**  \n")
                        insights.append("> Weightage: **10%** of total NIRF score\n\n")
                        
                        insights.append("### 🎯 Visibility Enhancement\n\n")
                        
                        insights.append("#### 1️⃣ Academic Publications\n")
                        insights.append("- Ensure high visibility in peer-reviewed journals\n")
                        insights.append("- Focus on indexed publications (Scopus, Web of Science)\n")
                        insights.append("- Increase citation impact\n\n")
                        
                        insights.append("#### 2️⃣ Rankings & Recognition\n")
                        insights.append("- Participate in domain-specific rankings\n")
                        insights.append("- Win national/international competitions\n")
                        insights.append("- Host and win hackathons, coding contests\n\n")
                        
                        insights.append("#### 3️⃣ Online Courses (MOOCs)\n")
                        insights.append("- Develop courses on **NPTEL/Swayam platforms**\n")
                        insights.append("- Reach wider audience through online education\n")
                        insights.append("- Faculty as MOOC instructors\n\n")
                        
                        insights.append("#### 4️⃣ Events & Conferences\n")
                        insights.append("- Host **national/international conferences**\n")
                        insights.append("- Organize technical symposiums\n")
                        insights.append("- Student and faculty paper presentations\n\n")
                        
                        insights.append("#### 5️⃣ Media Presence\n")
                        insights.append("- Increase visibility in news media\n")
                        insights.append("- Highlight research breakthroughs\n")
                        insights.append("- Social media engagement strategy\n\n")
                        
                        insights.append("#### 6️⃣ Alumni & Employer Feedback\n")
                        insights.append("- Strengthen alumni testimonials\n")
                        insights.append("- Gather positive employer feedback\n")
                        insights.append("- Showcase successful alumni achievements\n\n")

                    # Reference data section with better formatting
                    if points:
                        insights.append("---\n\n")
                        insights.append("### 📋 Reference Data Points\n\n")
                        for i, p in enumerate(points[:6], 1):
                            # Clean and format each point
                            clean_point = p.strip()
                            insights.append(f"**{i}.** {clean_point}\n\n")

                    insights.append("---\n\n")

            return "".join(insights)

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
