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
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stChatMessage {
        animation: slideIn 0.3s ease-out;
    }
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
        animation: fadeIn 0.5s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .pulse {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
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
if "analyzing" not in st.session_state:
    st.session_state.analyzing = False

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

# Helper function to parse and validate JSON response
def parse_bot_response(response_data):
    """Parse and validate the bot response from various JSON formats"""
    try:
        # If response is already a dict
        if isinstance(response_data, dict):
            # Check for common response keys
            if "response" in response_data:
                return response_data["response"]
            elif "message" in response_data:
                return response_data["message"]
            elif "output" in response_data:
                return response_data["output"]
            elif "text" in response_data:
                return response_data["text"]
            else:
                # Return the entire dict as formatted JSON
                return json.dumps(response_data, indent=2)
        
        # If response is a string, try to parse it
        elif isinstance(response_data, str):
            try:
                parsed = json.loads(response_data)
                return parse_bot_response(parsed)
            except json.JSONDecodeError:
                # Return as-is if not JSON
                return response_data
        
        # Fallback
        return str(response_data)
    
    except Exception as e:
        return f"⚠️ Error parsing response: {str(e)}\n\nRaw response: {response_data}"

# Streaming response generator
def stream_response(text: str) -> Generator[str, None, None]:
    """Simulate streaming by yielding words with delay"""
    words = text.split()
    for i, word in enumerate(words):
        yield word + " "
        time.sleep(0.03)  # Adjust speed here

# Chat input
user_input = st.chat_input("Ask about NIRF ranking improvements, gap analysis, or strategic suggestions...")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Display assistant response with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Show thinking animation
        with st.spinner("🤔 Analyzing..."):
            try:
                # Prepare payload
                payload = {
                    "sessionId": session_id,
                    "message": user_input,
                    "context": "NIRF ranking improvement analysis"
                }
                
                # Make API request
                response = requests.post(
                    "https://bavarchibiryni.app.n8n.cloud/webhook/37b860de-9c3b-4e77-85b5-54bd05c0771f",
                    json=payload,
                    timeout=30
                )
                
                # Check response status
                if response.status_code == 200:
                    # Parse response
                    try:
                        bot_reply = parse_bot_response(response.json())
                    except json.JSONDecodeError:
                        bot_reply = response.text
                    
                    # Stream the response
                    full_response = ""
                    for chunk in stream_response(bot_reply):
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                    
                    # Add to message history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": full_response
                    })
                    
                else:
                    error_msg = f"⚠️ Server returned status code: {response.status_code}\n\n{response.text}"
                    message_placeholder.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
            
            except requests.exceptions.Timeout:
                error_msg = "⏱️ Request timed out. Please try again."
                message_placeholder.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
            
            except requests.exceptions.ConnectionError:
                error_msg = "🔌 Connection error. Please check your internet connection."
                message_placeholder.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
            
            except Exception as e:
                error_msg = f"❌ Unexpected error: {str(e)}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Welcome message if no messages yet
if len(st.session_state.messages) == 0:
    with st.container():
        st.markdown("""
        <div class="metric-card">
            <h3>👋 Welcome to NIRF Ranking Advisor!</h3>
            <p>I can help you with:</p>
            <ul>
                <li>🔍 <b>Gap Analysis:</b> Identify weaknesses in NIRF parameters</li>
                <li>📊 <b>Data Analysis:</b> Review metrics and performance indicators</li>
                <li>💡 <b>Suggestions:</b> Get actionable improvement strategies</li>
                <li>📈 <b>Best Practices:</b> Learn from top-ranked institutions</li>
            </ul>
            <p><i>Try asking: "What are the key loopholes in our NIRF submission?" or "How can we improve our research output?"</i></p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    Session ID: <code>{}</code> | Powered by AI
</div>
""".format(session_id), unsafe_allow_html=True)
