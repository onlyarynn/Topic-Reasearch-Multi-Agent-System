import streamlit as st
import time
from pipeline import run_research_pipeline

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;1,300&display=swap');

/* Global reset */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: #0a0a0f;
    color: #e8e6f0;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Main container */
.block-container {
    padding: 2rem 3rem !important;
    max-width: 1100px !important;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 2.5rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #c084fc, #818cf8, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.4rem;
}
.hero p {
    color: #6b7280;
    font-size: 0.85rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Step cards ── */
.step-card {
    background: #11111b;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.3s;
}
.step-card.active {
    border-color: #818cf8;
    box-shadow: 0 0 20px rgba(129, 140, 248, 0.1);
}
.step-card.done {
    border-color: #34d399;
    box-shadow: 0 0 20px rgba(52, 211, 153, 0.07);
}
.step-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 0.25rem;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #e8e6f0;
}
.step-icon { margin-right: 0.5rem; }

/* ── Output section ── */
.output-box {
    background: #11111b;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 1rem;
    white-space: pre-wrap;
    font-size: 0.82rem;
    line-height: 1.7;
    color: #c4c4d4;
    max-height: 320px;
    overflow-y: auto;
}

/* ── Report box ── */
.report-box {
    background: linear-gradient(135deg, #11111b, #0f0f1a);
    border: 1px solid #818cf8;
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1rem;
    font-size: 0.85rem;
    line-height: 1.85;
    color: #ddd8f0;
    white-space: pre-wrap;
}

/* ── Feedback box ── */
.feedback-box {
    background: linear-gradient(135deg, #0a1a0e, #0f1a10);
    border: 1px solid #34d399;
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1rem;
    font-size: 0.85rem;
    line-height: 1.85;
    color: #d0f0de;
    white-space: pre-wrap;
}

/* ── Section headers ── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #6b7280;
    margin: 2rem 0 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e1e2e;
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input {
    background-color: #11111b !important;
    border: 1px solid #2d2d42 !important;
    border-radius: 10px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2) !important;
}

/* ── Button overrides ── */
.stButton > button {
    background: linear-gradient(135deg, #818cf8, #c084fc) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(129, 140, 248, 0.35) !important;
}

/* ── Status badge ── */
.badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    float: right;
}
.badge-running { background: #1e2040; color: #818cf8; }
.badge-done    { background: #0d2018; color: #34d399; }
.badge-waiting { background: #1a1a1a; color: #4b5563; }

/* scrollbar */
.output-box::-webkit-scrollbar { width: 4px; }
.output-box::-webkit-scrollbar-track { background: #0a0a0f; }
.output-box::-webkit-scrollbar-thumb { background: #2d2d42; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ─── Hero ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🔬 Research Agent</h1>
    <p>Multi-Agent · Web Search · Deep Analysis · AI Reporting</p>
</div>
""", unsafe_allow_html=True)

# ─── Input Row ──────────────────────────────────────────────────────────────
col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_input(
        label="",
        placeholder="Enter a research topic  e.g. 'Latest AI breakthroughs 2025'",
        label_visibility="collapsed"
    )
with col2:
    run_btn = st.button("▶  Run", use_container_width=True)

# ─── Pipeline Steps Definition ──────────────────────────────────────────────
STEPS = [
    ("🔍", "Step 1", "Search Agent",  "Scanning the web for recent, reliable data"),
    ("📄", "Step 2", "Reader Agent",  "Scraping top URLs for deeper content"),
    ("✍️", "Step 3", "Writer Agent",  "Drafting the full research report"),
    ("🧐", "Step 4", "Critic Agent",  "Reviewing and scoring the report"),
]

def render_step(icon, label, title, desc, status="waiting"):
    badge_class = {"running": "badge-running", "done": "badge-done", "waiting": "badge-waiting"}[status]
    badge_text  = {"running": "● Running", "done": "✓ Done", "waiting": "○ Waiting"}[status]
    card_class  = {"running": "step-card active", "done": "step-card done", "waiting": "step-card"}[status]
    st.markdown(f"""
    <div class="{card_class}">
        <div class="step-label">{label} <span class="badge {badge_class}">{badge_text}</span></div>
        <div class="step-title"><span class="step-icon">{icon}</span>{title}</div>
        <div style="color:#6b7280;font-size:0.75rem;margin-top:0.2rem;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Main Logic ─────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.markdown('<div class="section-header">Pipeline Progress</div>', unsafe_allow_html=True)

        step_slots = [st.empty() for _ in STEPS]

        # Render all as waiting initially
        for i, (icon, label, title, desc) in enumerate(STEPS):
            with step_slots[i]:
                render_step(icon, label, title, desc, "waiting")

        result_placeholder = st.empty()

        try:
            # We'll run step by step with status updates
            # Step 1 active
            with step_slots[0]:
                render_step(*STEPS[0], "running")

            # Run full pipeline (it handles all steps internally)
            with st.spinner(""):
                state = run_research_pipeline(topic)

            # Mark all done progressively
            for i, (icon, label, title, desc) in enumerate(STEPS):
                with step_slots[i]:
                    render_step(icon, label, title, desc, "done")
                time.sleep(0.15)

            # ── Outputs ────────────────────────────────────────────────────
            st.markdown('<div class="section-header">Search Results</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-box">{state.get("search_results", "")}</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-header">Scraped Content</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-box">{state.get("scraped_content", "")}</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-header">Final Research Report</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="report-box">{state.get("report", "")}</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-header">Critic Feedback</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="feedback-box">{state.get("feedback", "")}</div>', unsafe_allow_html=True)

            # Download button
            st.markdown("<br>", unsafe_allow_html=True)
            full_output = f"""RESEARCH TOPIC: {topic}
{"="*60}

SEARCH RESULTS:
{state.get("search_results", "")}

SCRAPED CONTENT:
{state.get("scraped_content", "")}

FINAL REPORT:
{state.get("report", "")}

CRITIC FEEDBACK:
{state.get("feedback", "")}
"""
            st.download_button(
                label="⬇  Download Full Report",
                data=full_output,
                file_name=f"research_{topic[:30].replace(' ','_')}.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Pipeline error: {str(e)}")

else:
    # Idle state — show steps as waiting
    st.markdown('<div class="section-header">Pipeline Steps</div>', unsafe_allow_html=True)
    for icon, label, title, desc in STEPS:
        render_step(icon, label, title, desc, "waiting")