"""Streamlit Web UI for the LinkedIn Post Agent."""

import os
import uuid
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq

from linkedin_post_agent.config import get_model_name

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="LinkedIn Post Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for rich aesthetics
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #0A66C2 0%, #00A0DC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #5E6E82;
        margin-bottom: 1.5rem;
    }
    .post-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        font-size: 1.05rem;
        line-height: 1.6;
        color: #1E293B;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        white-space: pre-wrap;
    }
    .badge-approved {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_post" not in st.session_state:
    st.session_state.current_post = None
if "is_published" not in st.session_state:
    st.session_state.is_published = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Sidebar Configuration
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png", width=50)
    st.title("⚙️ Settings")
    
    api_key_env = os.getenv("GROQ_API_KEY", "")
    api_key_input = st.text_input(
        "Groq API Key",
        value=api_key_env,
        type="password",
        help="Get your key at console.groq.com",
    )
    
    selected_model = st.selectbox(
        "Groq Model",
        options=[
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "mixtral-8x7b-32768",
        ],
        index=0,
    )
    
    temperature = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.7, 0.05)
    
    st.divider()
    st.caption("Human-in-the-Loop AI Workflow with LangGraph & Groq")
    if st.button("🔄 Reset Workflow", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_post = None
        st.session_state.is_published = False
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

# Main Title Header
st.markdown('<div class="main-header">🤖 LinkedIn Post Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Human-in-the-loop AI post generation with iterative revision cycles</div>', unsafe_allow_html=True)

# Step 1: Topic Prompt Input
if not st.session_state.messages:
    st.subheader("1. What topic would you like to post about?")
    default_prompt = "Write an engaging LinkedIn post about how AI Agents are transforming software engineering and content creation."
    user_topic = st.text_area("Post Topic / Prompt", value=default_prompt, height=100)
    
    if st.button("🚀 Generate Draft Post", type="primary", use_container_width=True):
        if not api_key_input:
            st.error("Please provide a Groq API Key in the sidebar.")
        else:
            with st.spinner("Generating post with Groq LLM..."):
                try:
                    llm = ChatGroq(
                        model=selected_model,
                        api_key=api_key_input,
                        temperature=temperature,
                    )
                    initial_msg = HumanMessage(content=user_topic)
                    response = llm.invoke([initial_msg])
                    
                    st.session_state.messages = [initial_msg, response]
                    st.session_state.current_post = response.content
                    st.session_state.is_published = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating post: {str(e)}")

# Step 2: Post Review & Human Feedback Loop
else:
    if st.session_state.is_published:
        st.balloons()
        st.success("🎉 LinkedIn post approved and published successfully!")
        st.markdown('<span class="badge-approved">Status: Published</span>', unsafe_allow_html=True)
        st.divider()
        st.markdown(f'<div class="post-card">{st.session_state.current_post}</div>', unsafe_allow_html=True)
        
        st.write("")
        if st.button("✨ Create Another Post", type="primary"):
            st.session_state.messages = []
            st.session_state.current_post = None
            st.session_state.is_published = False
            st.rerun()
    else:
        st.subheader("2. Review Generated Draft")
        st.markdown(f'<div class="post-card">{st.session_state.current_post}</div>', unsafe_allow_html=True)
        st.write("")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("✅ Approve & Publish", type="primary", use_container_width=True):
                st.session_state.is_published = True
                st.rerun()
                
        with col2:
            st.caption("Need changes? Request revisions below.")
            
        st.divider()
        st.subheader("3. Human Feedback & Revisions")
        feedback = st.text_input(
            "What would you like to improve?",
            placeholder="e.g., Make it punchier, add 3 hashtags, and shorten the opening.",
        )
        
        if st.button("🔄 Regenerate with Feedback", use_container_width=True):
            if not feedback.strip():
                st.warning("Please enter revision feedback before regenerating.")
            else:
                with st.spinner("Revising post based on your feedback..."):
                    try:
                        llm = ChatGroq(
                            model=selected_model,
                            api_key=api_key_input,
                            temperature=temperature,
                        )
                        feedback_msg = HumanMessage(
                            content=f"Please revise the LinkedIn post using this feedback:\n{feedback}"
                        )
                        st.session_state.messages.append(feedback_msg)
                        
                        response = llm.invoke(st.session_state.messages)
                        st.session_state.messages.append(response)
                        st.session_state.current_post = response.content
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error revising post: {str(e)}")

        # Conversation History Expander
        with st.expander("📜 View Full State & Message History"):
            for idx, msg in enumerate(st.session_state.messages):
                role = "User" if isinstance(msg, HumanMessage) else "Assistant"
                st.write(f"**{idx+1}. {role}:**")
                st.info(msg.content)
