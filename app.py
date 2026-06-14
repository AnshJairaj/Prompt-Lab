import streamlit as st
import json
import time
from groq import Groq
from cases import CASES
from utils import evaluate_prompt, get_prompt_tips, score_prompt_quality

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Prompt Engineering Lab",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Root variables */
:root {
    --primary: #005B8E;
    --primary-light: #0077BB;
    --accent: #FF6B35;
    --accent-soft: #FF6B3515;
    --success: #22C55E;
    --warning: #F59E0B;
    --danger: #EF4444;
    --bg: #0A0F1E;
    --surface: #111827;
    --surface2: #1A2236;
    --border: #1E2D45;
    --text: #E8EDF5;
    --text-muted: #7A8BA0;
    --tata-blue: #005B8E;
    --tata-orange: #FF6B35;
}

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text) !important;
}

/* Main container */
.main .block-container {
    padding: 1.5rem 2rem !important;
    max-width: 1400px !important;
}

/* ── Hero Banner ─────────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, #005B8E 0%, #003A5C 40%, #1A0533 100%);
    border: 1px solid #0077BB40;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, #FF6B3515 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: #FF6B3520;
    border: 1px solid #FF6B3550;
    color: #FF6B35;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    color: #fff;
    line-height: 1.2;
    margin: 0 0 0.5rem 0;
}
.hero-sub {
    font-size: 1rem;
    color: #A0B4C8;
    margin: 0;
    max-width: 600px;
}

/* ── Case Cards ──────────────────────────────────────────── */
.case-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.6rem;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
}
.case-card:hover {
    border-color: var(--primary-light);
    background: var(--surface2);
}
.case-card.active {
    border-color: var(--accent);
    background: var(--surface2);
}
.case-card .case-num {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 4px;
}
.case-card .case-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text);
}
.case-card .case-dept {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 2px;
}

/* ── Section Panels ──────────────────────────────────────── */
.panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.panel-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 6px;
}
.panel-title::before {
    content: '';
    display: inline-block;
    width: 3px;
    height: 12px;
    background: var(--accent);
    border-radius: 2px;
}

/* ── Info Chips ──────────────────────────────────────────── */
.info-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 0.8rem;
}
.chip {
    background: #0077BB15;
    border: 1px solid #0077BB30;
    color: #6BB8E8;
    font-size: 0.72rem;
    padding: 3px 10px;
    border-radius: 20px;
    font-weight: 500;
}
.chip-orange {
    background: #FF6B3512;
    border: 1px solid #FF6B3530;
    color: #FF9B6E;
}

/* ── Output Box ──────────────────────────────────────────── */
.output-box {
    background: #060D1A;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.88rem;
    line-height: 1.7;
    color: #CBD5E1;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 520px;
    overflow-y: auto;
}

/* ── Score Meter ─────────────────────────────────────────── */
.score-ring {
    text-align: center;
    padding: 1rem;
}
.score-number {
    font-size: 3rem;
    font-weight: 700;
    line-height: 1;
}
.score-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 4px;
}
.score-bar-bg {
    background: var(--border);
    border-radius: 4px;
    height: 6px;
    margin: 6px 0;
}
.score-bar-fill {
    border-radius: 4px;
    height: 6px;
}

/* ── Tips Box ────────────────────────────────────────────── */
.tip-box {
    background: #F59E0B08;
    border: 1px solid #F59E0B25;
    border-left: 3px solid #F59E0B;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font-size: 0.82rem;
    color: #D4A84B;
    margin-bottom: 0.6rem;
    line-height: 1.5;
}

/* ── Metric Cards ────────────────────────────────────────── */
.metric-row {
    display: flex;
    gap: 10px;
    margin-bottom: 1rem;
}
.metric-card {
    flex: 1;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.8rem;
    text-align: center;
}
.metric-val {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent);
}
.metric-lbl {
    font-size: 0.65rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 2px;
}

/* ── Buttons ─────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px #005B8E50 !important;
}

/* textarea */
.stTextArea textarea {
    background: #060D1A !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--primary-light) !important;
    box-shadow: 0 0 0 2px #0077BB20 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 8px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 6px !important;
    color: var(--text-muted) !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
}
.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: white !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface2) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-weight: 500 !important;
}

/* Select box */
.stSelectbox select, div[data-baseweb="select"] {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

/* Divider */
hr {
    border-color: var(--border) !important;
    margin: 1.2rem 0 !important;
}

/* Success / Error messages */
.stSuccess { background: #22C55E10 !important; border-color: #22C55E40 !important; }
.stError   { background: #EF444410 !important; border-color: #EF444440 !important; }
.stWarning { background: #F59E0B10 !important; border-color: #F59E0B40 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }

/* Progress bar */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%) !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Session State ────────────────────────────────────────────────────────────
defaults = {
    "api_key": "",
    "selected_case": 0,
    "prompt_history": [],
    "last_output": "",
    "last_score": None,
    "total_runs": 0,
    "best_score": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
        <div style='font-size:2rem; margin-bottom:4px;'>⚡</div>
        <div style='font-size:1.1rem; font-weight:700; color:#E8EDF5;'>Prompt Lab</div>
        <div style='font-size:0.7rem; color:#7A8BA0; letter-spacing:0.1em; text-transform:uppercase;'>
            Tata Steel · AI Initiative
        </div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    # API Key
    st.markdown("**🔑 Groq API Key**")
    api_key_input = st.text_input(
        "Enter your Groq API key",
        value=st.session_state.api_key,
        type="password",
        placeholder="gsk_...",
        label_visibility="collapsed"
    )
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.success("✓ API key saved", icon="✅")

    with st.expander("📖 How to get a Groq API key"):
        st.markdown("""
        1. Go to [console.groq.com](https://console.groq.com)
        2. Sign up / Log in (free)
        3. Click **API Keys** in the sidebar
        4. Click **Create API Key**
        5. Copy & paste it above

        > **Free tier:** 6,000 tokens/min  
        > **Model used:** `llama-3.3-70b-versatile`
        """)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Model selector
    st.markdown("**🤖 Model**")
    model_choice = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"],
        label_visibility="collapsed"
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # Stats
    st.markdown("**📊 Your Session Stats**")
    col1, col2 = st.columns(2)
    col1.metric("Runs", st.session_state.total_runs)
    col2.metric("Best Score", f"{st.session_state.best_score}/100")
    
    if st.session_state.prompt_history:
        avg = sum(h["score"] for h in st.session_state.prompt_history if h["score"]) / max(1, len([h for h in st.session_state.prompt_history if h["score"]]))
        st.metric("Avg Score", f"{avg:.0f}/100")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Navigation
    st.markdown("**📂 Cases**")
    for i, case in enumerate(CASES):
        is_active = st.session_state.selected_case == i
        border = "#FF6B35" if is_active else "#1E2D45"
        bg = "#1A2236" if is_active else "#111827"
        if st.button(
            f"{'▶ ' if is_active else ''}{case['icon']} {case['title']}",
            key=f"nav_{i}",
            use_container_width=True,
        ):
            st.session_state.selected_case = i
            st.session_state.last_output = ""
            st.session_state.last_score = None
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.prompt_history = []
        st.session_state.total_runs = 0
        st.session_state.best_score = 0
        st.rerun()


# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">🏭 Tata Steel · Internship Project · Powered by Groq</div>
    <div class="hero-title">AI Prompt Engineering Lab</div>
    <p class="hero-sub">
        Master prompt engineering through real corporate scenarios — from HR and procurement to IT support.
        Write better prompts. Get scored. Improve. Repeat.
    </p>
</div>
""", unsafe_allow_html=True)


# ─── Main Content ─────────────────────────────────────────────────────────────
case = CASES[st.session_state.selected_case]

# ── Case Header
col_icon, col_info = st.columns([1, 8])
with col_icon:
    st.markdown(f"<div style='font-size:3.5rem; text-align:center; padding-top:6px'>{case['icon']}</div>", unsafe_allow_html=True)
with col_info:
    st.markdown(f"""
    <div>
        <div style='font-size:0.65rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:#FF6B35; margin-bottom:4px;'>
            CASE {st.session_state.selected_case + 1} OF {len(CASES)} · {case['department']}
        </div>
        <div style='font-size:1.6rem; font-weight:700; color:#E8EDF5;'>{case['title']}</div>
        <div style='font-size:0.9rem; color:#7A8BA0; margin-top:4px;'>{case['subtitle']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📋 Brief", "✍️ Write & Test", "📊 Analysis", "📜 History"])

# ════════════════════════════════════════════════════════
# TAB 1: BRIEF
# ════════════════════════════════════════════════════════
with tab1:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        # Business Case
        st.markdown(f"""
        <div class="panel">
            <div class="panel-title">Business Case</div>
            <p style='font-size:0.88rem; color:#CBD5E1; line-height:1.7; margin:0;'>{case['business_case']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Objective
        st.markdown(f"""
        <div class="panel">
            <div class="panel-title">🎯 Objective — What AI Must Do</div>
        """, unsafe_allow_html=True)
        for obj in case["objectives"]:
            st.markdown(f"""
            <div style='display:flex; align-items:flex-start; gap:8px; margin-bottom:6px;'>
                <span style='color:#FF6B35; margin-top:2px;'>▸</span>
                <span style='font-size:0.85rem; color:#CBD5E1;'>{obj}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Input
        st.markdown(f"""
        <div class="panel">
            <div class="panel-title">📥 Input — Available to AI</div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="info-chips">', unsafe_allow_html=True)
        for inp in case["inputs"]:
            st.markdown(f'<span class="chip">{inp}</span>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    with col_right:
        # Expected Output
        st.markdown(f"""
        <div class="panel">
            <div class="panel-title">📤 Expected Output Format</div>
        """, unsafe_allow_html=True)
        for out in case["expected_output"]:
            st.markdown(f"""
            <div style='display:flex; align-items:flex-start; gap:8px; margin-bottom:6px;'>
                <span style='color:#22C55E; font-size:0.8rem; margin-top:2px;'>✓</span>
                <span style='font-size:0.85rem; color:#CBD5E1;'>{out}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Scenario Context
        st.markdown(f"""
        <div class="panel" style='border-color:#0077BB30; background:linear-gradient(135deg,#111827,#0A1628);'>
            <div class="panel-title">📌 Scenario Context</div>
            <p style='font-size:0.85rem; color:#A0C4E8; line-height:1.7; margin:0; font-style:italic;'>{case['scenario']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Difficulty chips
        st.markdown(f"""
        <div class="panel">
            <div class="panel-title">⚙️ Prompt Requirements</div>
            <div class="info-chips">
        """, unsafe_allow_html=True)
        for tag in case["tags"]:
            st.markdown(f'<span class="chip chip-orange">{tag}</span>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# TAB 2: WRITE & TEST
# ════════════════════════════════════════════════════════
with tab2:
    col_editor, col_output = st.columns([1, 1], gap="large")

    with col_editor:
        st.markdown("""
        <div class="panel-title" style='margin-bottom:0.4rem;'>✍️ Your Prompt</div>
        """, unsafe_allow_html=True)

        # Sample toggle
        show_hint = st.toggle("💡 Show starter template", value=False)
        if show_hint:
            st.code(case["starter_prompt"], language="text")
            st.caption("👆 Use this as inspiration — don't just copy it!")

        user_prompt = st.text_area(
            "Write your prompt",
            height=320,
            placeholder=f"Write a detailed prompt for the {case['title']} scenario...\n\nTips:\n• Be specific about the role you want AI to play\n• Define the input data format\n• Specify the exact output format\n• Add constraints and tone guidelines",
            label_visibility="collapsed"
        )

        # Context input
        with st.expander("📎 Add Context / Sample Data (optional)"):
            context_data = st.text_area(
                "Paste sample data here (resume, vendor quote, etc.)",
                height=150,
                placeholder=case["sample_context"],
                label_visibility="collapsed"
            )

        # Temperature
        temperature = st.slider("🌡️ Temperature (creativity)", 0.0, 1.0, 0.3, 0.05)
        
        run_col, clear_col = st.columns([3, 1])
        with run_col:
            run_btn = st.button("⚡ Run Prompt", use_container_width=True, type="primary")
        with clear_col:
            if st.button("🔄 Clear", use_container_width=True):
                st.session_state.last_output = ""
                st.session_state.last_score = None
                st.rerun()

    with col_output:
        st.markdown("""
        <div class="panel-title" style='margin-bottom:0.4rem;'>🤖 AI Response</div>
        """, unsafe_allow_html=True)

        if run_btn:
            if not st.session_state.api_key:
                st.error("⚠️ Please enter your Groq API key in the sidebar first.")
            elif not user_prompt.strip():
                st.warning("📝 Please write a prompt first.")
            else:
                with st.spinner("⚡ Running on Groq..."):
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        
                        # Build messages
                        system_msg = f"""You are an expert AI assistant helping with corporate HR and business tasks at Tata Steel.
You are responding to a prompt for the following scenario: {case['title']} — {case['department']}.
Business context: {case['business_case']}
Respond in a structured, professional format as specified by the user's prompt.
Always be thorough, practical, and business-focused."""
                        
                        user_content = user_prompt
                        if context_data and context_data.strip():
                            user_content += f"\n\n--- CONTEXT / SAMPLE DATA ---\n{context_data}"
                        
                        response = client.chat.completions.create(
                            model=model_choice,
                            messages=[
                                {"role": "system", "content": system_msg},
                                {"role": "user", "content": user_content}
                            ],
                            temperature=temperature,
                            max_tokens=2048,
                        )
                        
                        output = response.choices[0].message.content
                        st.session_state.last_output = output
                        
                        # Score the prompt
                        score_data = score_prompt_quality(user_prompt, case)
                        st.session_state.last_score = score_data
                        
                        # Update stats
                        st.session_state.total_runs += 1
                        if score_data["total"] > st.session_state.best_score:
                            st.session_state.best_score = score_data["total"]
                        
                        # Save to history
                        st.session_state.prompt_history.append({
                            "case": case["title"],
                            "prompt": user_prompt[:200] + "..." if len(user_prompt) > 200 else user_prompt,
                            "output": output[:300] + "...",
                            "score": score_data["total"],
                            "timestamp": time.strftime("%H:%M:%S"),
                        })
                        
                        st.success(f"✅ Response generated! Prompt score: **{score_data['total']}/100**")

                    except Exception as e:
                        err = str(e)
                        if "401" in err or "invalid_api_key" in err.lower():
                            st.error("❌ Invalid API key. Please check your Groq API key in the sidebar.")
                        elif "rate_limit" in err.lower():
                            st.error("⏳ Rate limit hit. Wait a moment and try again.")
                        else:
                            st.error(f"❌ Error: {err}")

        if st.session_state.last_output:
            st.markdown(f'<div class="output-box">{st.session_state.last_output}</div>', unsafe_allow_html=True)
            
            dl_col, copy_col = st.columns(2)
            with dl_col:
                st.download_button(
                    "⬇️ Download Response",
                    data=st.session_state.last_output,
                    file_name=f"response_{case['title'].replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        else:
            st.markdown("""
            <div style='
                background:#060D1A;
                border:1px dashed #1E2D45;
                border-radius:10px;
                padding:3rem 2rem;
                text-align:center;
                color:#3A4A5A;
            '>
                <div style='font-size:2.5rem; margin-bottom:12px;'>🤖</div>
                <div style='font-size:0.9rem;'>Your AI response will appear here</div>
                <div style='font-size:0.75rem; margin-top:8px; color:#2A3A4A;'>
                    Write a prompt on the left and click "Run Prompt"
                </div>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# TAB 3: ANALYSIS
# ════════════════════════════════════════════════════════
with tab3:
    if st.session_state.last_score is None:
        st.markdown("""
        <div style='
            text-align:center;
            padding:4rem 2rem;
            background:#111827;
            border:1px dashed #1E2D45;
            border-radius:12px;
        '>
            <div style='font-size:2.5rem;'>📊</div>
            <div style='color:#3A4A5A; margin-top:12px; font-size:0.9rem;'>
                Run a prompt first to see your detailed analysis
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        score_data = st.session_state.last_score
        total = score_data["total"]
        
        # Score colour
        if total >= 80:
            color = "#22C55E"
            grade = "A"
            grade_label = "Expert"
        elif total >= 60:
            color = "#F59E0B"
            grade = "B"
            grade_label = "Proficient"
        elif total >= 40:
            color = "#FF6B35"
            grade = "C"
            grade_label = "Developing"
        else:
            color = "#EF4444"
            grade = "D"
            grade_label = "Beginner"

        score_col, breakdown_col = st.columns([1, 2], gap="large")
        
        with score_col:
            st.markdown(f"""
            <div class="panel" style='text-align:center;'>
                <div class="panel-title" style='justify-content:center;'>Prompt Score</div>
                <div style='
                    font-size:5rem;
                    font-weight:800;
                    color:{color};
                    line-height:1;
                    margin: 0.5rem 0;
                '>{total}</div>
                <div style='font-size:1rem; color:#7A8BA0;'>/ 100</div>
                <div style='
                    display:inline-block;
                    background:{color}20;
                    border:1px solid {color}50;
                    color:{color};
                    font-size:0.85rem;
                    font-weight:600;
                    padding:4px 16px;
                    border-radius:20px;
                    margin-top:10px;
                '>Grade {grade} — {grade_label}</div>
            </div>
            """, unsafe_allow_html=True)

            # Criteria bars
            st.markdown('<div class="panel"><div class="panel-title">Criteria Breakdown</div>', unsafe_allow_html=True)
            for criterion, val in score_data["criteria"].items():
                pct = val * 5  # each out of 20
                bar_color = "#22C55E" if pct >= 70 else "#F59E0B" if pct >= 50 else "#EF4444"
                st.markdown(f"""
                <div style='margin-bottom:10px;'>
                    <div style='display:flex; justify-content:space-between; font-size:0.75rem; margin-bottom:3px;'>
                        <span style='color:#CBD5E1;'>{criterion}</span>
                        <span style='color:{bar_color}; font-weight:600;'>{val}/20</span>
                    </div>
                    <div class="score-bar-bg">
                        <div class="score-bar-fill" style='width:{pct}%; background:{bar_color};'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with breakdown_col:
            # Tips
            tips = get_prompt_tips(score_data, case)
            st.markdown('<div class="panel"><div class="panel-title">💡 Improvement Tips</div>', unsafe_allow_html=True)
            for tip in tips:
                st.markdown(f'<div class="tip-box">{tip}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Evaluation details
            eval_text = evaluate_prompt(user_prompt if 'user_prompt' in dir() else "", case)
            st.markdown(f"""
            <div class="panel">
                <div class="panel-title">🔍 Detailed Evaluation</div>
                <div style='font-size:0.84rem; color:#A0B4C8; line-height:1.8;'>{eval_text}</div>
            </div>
            """, unsafe_allow_html=True)

            # Checklist
            st.markdown('<div class="panel"><div class="panel-title">✅ Prompt Checklist</div>', unsafe_allow_html=True)
            checklist = [
                ("Role / Persona defined", "role" in (user_prompt.lower() if 'user_prompt' in dir() else "")),
                ("Clear task description", len(user_prompt) > 50 if 'user_prompt' in dir() else False),
                ("Input format specified", any(w in (user_prompt.lower() if 'user_prompt' in dir() else "") for w in ["input", "data", "resume", "information"])),
                ("Output format specified", any(w in (user_prompt.lower() if 'user_prompt' in dir() else "") for w in ["output", "format", "provide", "generate", "list", "table"])),
                ("Constraints/tone set", any(w in (user_prompt.lower() if 'user_prompt' in dir() else "") for w in ["professional", "formal", "concise", "brief", "detailed", "tone"])),
                ("Context provided", len(user_prompt) > 150 if 'user_prompt' in dir() else False),
            ]
            for label, passed in checklist:
                icon = "✅" if passed else "❌"
                color = "#22C55E" if passed else "#EF4444"
                st.markdown(f"""
                <div style='display:flex; align-items:center; gap:10px; margin-bottom:5px;'>
                    <span>{icon}</span>
                    <span style='font-size:0.82rem; color:{"#CBD5E1" if passed else "#7A8BA0"};'>{label}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# TAB 4: HISTORY
# ════════════════════════════════════════════════════════
with tab4:
    if not st.session_state.prompt_history:
        st.markdown("""
        <div style='text-align:center; padding:4rem; background:#111827; border:1px dashed #1E2D45; border-radius:12px;'>
            <div style='font-size:2rem;'>📜</div>
            <div style='color:#3A4A5A; margin-top:12px;'>No history yet — run some prompts!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Summary metrics
        scores = [h["score"] for h in st.session_state.prompt_history if h["score"]]
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="metric-val">{len(st.session_state.prompt_history)}</div>
                <div class="metric-lbl">Total Runs</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">{max(scores) if scores else 0}</div>
                <div class="metric-lbl">Best Score</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">{sum(scores)//len(scores) if scores else 0}</div>
                <div class="metric-lbl">Avg Score</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">{len(set(h['case'] for h in st.session_state.prompt_history))}</div>
                <div class="metric-lbl">Cases Tried</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # History table
        for i, h in enumerate(reversed(st.session_state.prompt_history)):
            score = h["score"]
            color = "#22C55E" if score >= 80 else "#F59E0B" if score >= 60 else "#EF4444"
            with st.expander(f"#{len(st.session_state.prompt_history)-i} · {h['case']} · Score: {score}/100 · {h['timestamp']}"):
                col_p, col_o = st.columns(2)
                with col_p:
                    st.markdown("**Prompt**")
                    st.markdown(f'<div style="background:#060D1A;padding:10px;border-radius:8px;font-size:0.82rem;color:#CBD5E1;">{h["prompt"]}</div>', unsafe_allow_html=True)
                with col_o:
                    st.markdown("**Response Preview**")
                    st.markdown(f'<div style="background:#060D1A;padding:10px;border-radius:8px;font-size:0.82rem;color:#A0C4E8;">{h["output"]}</div>', unsafe_allow_html=True)

        # Export
        export_data = json.dumps(st.session_state.prompt_history, indent=2)
        st.download_button(
            "⬇️ Export History as JSON",
            data=export_data,
            file_name="prompt_lab_history.json",
            mime="application/json"
        )
