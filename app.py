"""
app.py — Streamlit web interface for SmartAgent.

Run with:
    streamlit run app.py
"""

import streamlit as st
from agent import build_agent

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SmartAgent",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Custom CSS — subtle dark-theme polish
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* ── Fonts ──────────────────────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'IBM Plex Sans', sans-serif;
        }

        /* ── Header bar ─────────────────────────────────────────────── */
        .agent-header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 18px 0 8px;
            border-bottom: 2px solid #1e293b;
            margin-bottom: 24px;
        }
        .agent-header .icon { font-size: 2rem; }
        .agent-header h1 {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 1.6rem;
            font-weight: 600;
            margin: 0;
            background: linear-gradient(90deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .agent-header .sub {
            font-size: 0.8rem;
            color: #64748b;
            margin: 0;
            font-family: 'IBM Plex Mono', monospace;
        }

        /* ── Tool badge strip ───────────────────────────────────────── */
        .tool-strip {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 20px;
        }
        .tool-badge {
            background: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 20px;
            padding: 3px 10px;
            font-size: 0.72rem;
            font-family: 'IBM Plex Mono', monospace;
            color: #94a3b8;
        }

        /* ── Chat messages ──────────────────────────────────────────── */
        [data-testid="stChatMessage"] {
            border-radius: 12px;
            padding: 4px 0;
        }

        /* ── Input box ──────────────────────────────────────────────── */
        [data-testid="stChatInput"] textarea {
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 0.95rem;
        }

        /* ── Spinner text ───────────────────────────────────────────── */
        .stSpinner > div {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.85rem;
            color: #38bdf8;
        }

        /* ── Error box ──────────────────────────────────────────────── */
        .error-box {
            background: #1c0a0a;
            border-left: 3px solid #ef4444;
            border-radius: 6px;
            padding: 10px 14px;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.82rem;
            color: #fca5a5;
        }

        /* ── Hide Streamlit branding ────────────────────────────────── */
        #MainMenu, footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="agent-header">
        <span class="icon">🤖</span>
        <div>
            <h1>SmartAgent</h1>
            <p class="sub">Groq · llama3-70b-8192 · ReAct</p>
        </div>
    </div>
    <div class="tool-strip">
        <span class="tool-badge">🔍 web_search</span>
        <span class="tool-badge">📝 write_file</span>
        <span class="tool-badge">📂 read_file</span>
        <span class="tool-badge">🧮 calculator</span>
        <span class="tool-badge">📄 summarize_text</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session state — agent & chat history
# ---------------------------------------------------------------------------
if "agent" not in st.session_state:
    with st.spinner("Initialising SmartAgent…"):
        try:
            st.session_state.agent = build_agent()
            st.session_state.init_error = None
        except Exception as e:
            st.session_state.agent = None
            st.session_state.init_error = str(e)

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------------------------
# Surface initialisation error once, then stop
# ---------------------------------------------------------------------------
if st.session_state.get("init_error"):
    st.markdown(
        f'<div class="error-box">⚠️ Failed to initialise agent:<br><br>'
        f'{st.session_state.init_error}</div>',
        unsafe_allow_html=True,
    )
    st.stop()

# ---------------------------------------------------------------------------
# Render existing chat history
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# Welcome message on first load
# ---------------------------------------------------------------------------
if not st.session_state.messages:
    with st.chat_message("assistant"):
        welcome = (
            "Hello! I'm **SmartAgent**, your AI assistant powered by Groq. "
            "I can search the web, do maths, read/write files, and summarise text. "
            "What can I help you with?"
        )
        st.markdown(welcome)

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------
if prompt := st.chat_input("Ask SmartAgent anything…"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Run agent
    with st.chat_message("assistant"):
        with st.spinner("SmartAgent is thinking…"):
            try:
                response = st.session_state.agent.invoke({"input": prompt})
                answer = response.get("output", "I couldn't generate a response.")
            except Exception as e:
                answer = None
                error_msg = str(e)

        if answer:
            st.markdown(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
        else:
            error_html = (
                f'<div class="error-box">⚠️ Agent encountered an error:<br><br>'
                f'{error_msg}</div>'
            )
            st.markdown(error_html, unsafe_allow_html=True)
            st.session_state.messages.append(
                {"role": "assistant", "content": f"⚠️ Error: {error_msg}"}
            )
