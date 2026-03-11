"""
app.py — Mr.News: AI-Powered Expert Research Reporter
Built by Jayan | Powered by Gemini + DuckDuckGo
"""

import streamlit as st
import os
import datetime
from core.searcher import search_topic
from core.analyzer import GeminiAnalyzer
from core.report_builder import build_docx, build_pdf
from core.prompts import combined_research_prompt

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mr.News — AI Expert Research Reporter",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* ──── Clean dark background ──── */
  .stApp {
    background: #0b0f19;
    color: #cbd5e1;
  }

  /* ──── Sidebar ──── */
  [data-testid="stSidebar"] {
    background: #0f1320 !important;
    border-right: 1px solid #1e293b;
  }

  /* ──── Hero Banner ──── */
  .hero-banner {
    background: linear-gradient(135deg, #1e3a5f 0%, #1a1a2e 50%, #16213e 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 40px 36px 32px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }
  .hero-banner::before {
    content: '';
    position: absolute; top: 0; right: 0; bottom: 0; left: 0;
    background: radial-gradient(ellipse at 30% 50%, rgba(59,130,246,0.08) 0%, transparent 70%);
  }
  .hero-title {
    font-size: 2.8rem; font-weight: 800;
    color: #f8fafc; margin: 0 0 6px 0;
    letter-spacing: -1px; line-height: 1;
    position: relative;
  }
  .hero-subtitle {
    font-size: 1.05rem; color: #94a3b8;
    margin: 0; font-weight: 400;
    position: relative;
  }

  /* ──── Buttons ──── */
  .stButton > button {
    background: #3b82f6 !important;
    color: white !important;
    border: none !important;
    padding: 12px 28px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
  }
  .stButton > button:hover {
    background: #2563eb !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(59,130,246,0.3) !important;
  }

  /* ──── Steps ──── */
  .step-item {
    display: flex; align-items: center; gap: 12px;
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 10px 16px;
    margin-bottom: 6px;
    font-size: 0.9rem; color: #64748b;
  }
  .step-done {
    border-color: #166534;
    background: #052e16;
    color: #4ade80;
  }
  .step-active {
    border-color: #1d4ed8;
    background: #0c1a3d;
    color: #93c5fd;
    animation: stepPulse 2s ease-in-out infinite;
  }
  @keyframes stepPulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
  }

  /* ──── Tabs ──── */
  [data-testid="stTabs"] [role="tab"] {
    background: #111827 !important;
    border-radius: 8px 8px 0 0 !important;
    color: #64748b !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    border: 1px solid #1e293b !important;
    border-bottom: none !important;
  }
  [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #0c1a3d !important;
    color: #93c5fd !important;
    border-color: #1d4ed8 !important;
    border-bottom: 2px solid #3b82f6 !important;
  }
  [data-testid="stTabs"] [role="tabpanel"] {
    border: 1px solid #1e293b;
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 16px !important;
    background: #0f1320;
  }

  /* ──── Source cards ──── */
  .source-item {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
    font-size: 0.85rem;
  }
  .source-title { color: #e2e8f0; font-weight: 600; }
  .source-url { color: #60a5fa; font-size: 0.75rem; }

  /* ──── Download buttons ──── */
  [data-testid="stDownloadButton"] button {
    background: #1e40af !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    width: 100% !important;
  }
  [data-testid="stDownloadButton"] button:hover {
    background: #1d4ed8 !important;
  }

  /* ──── Sidebar elements ──── */
  [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown {
    color: #94a3b8 !important;
  }
  [data-testid="stSidebar"] h3 {
    color: #e2e8f0 !important;
    font-size: 1rem !important;
  }
  .sidebar-section {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 14px;
    margin-bottom: 12px;
  }

  /* ──── Inputs ──── */
  .stTextInput input, .stTextArea textarea {
    background: #111827 !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-size: 0.95rem !important;
  }
  .stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important;
  }

  /* ──── Misc ──── */
  .stAlert { border-radius: 8px !important; }
  div[data-testid="stMarkdownContainer"] h3 { color: #94a3b8; }

  /* ──── Result header ──── */
  .result-header {
    background: #052e16;
    border: 1px solid #166534;
    border-radius: 10px;
    padding: 16px 24px;
    margin: 12px 0;
  }
  .result-header h3 { color: #4ade80 !important; margin: 0 0 4px 0; }

  /* ──── Footer ──── */
  .app-footer {
    text-align: center;
    padding: 24px 0 12px 0;
    color: #475569;
    font-size: 0.82rem;
    border-top: 1px solid #1e293b;
    margin-top: 40px;
  }
  .app-footer .built-by {
    color: #64748b;
    font-weight: 600;
    font-size: 0.88rem;
  }

  /* ──── Scrollbar ──── */
  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-track { background: #0b0f19; }
  ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ─── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <p class="hero-title">Mr.News</p>
  <p class="hero-subtitle">Your AI-powered research assistant that searches the web, analyzes trending news, and generates expert-level reports with plain English explanations — all in one click.</p>
</div>
""", unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**🔑 API Key**")
    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="AIza...",
        label_visibility="collapsed",
        help="Get your key from https://aistudio.google.com/",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**📄 Export Format**")
    export_format = st.radio(
        "Format", ["DOCX + PDF", "DOCX only", "PDF only"],
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
**How it works:**
1. 🌐 Searches 12+ query variants
2. 📥 Scrapes & extracts content
3. 🧠 AI expert analysis (all-in-one)
4. 📄 Exports DOCX + PDF
""")


# ─── Main Input ───────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1.4])

with col_input:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g.  Claude,  ChatGPT,  React 19,  Quantum Computing...",
        label_visibility="collapsed",
    )

with col_btn:
    generate = st.button("🔍 Research", use_container_width=True)

st.markdown("")

# ─── Helpers ──────────────────────────────────────────────────────────────────
def _step_html(emoji, label, state="pending"):
    cls = {"done": "step-done", "active": "step-active", "pending": "step-item"}.get(state, "step-item")
    icon = {"done": "✅", "active": "⏳", "pending": "⬜"}.get(state, "⬜")
    return f'<div class="{cls}">{icon} {emoji} {label}</div>'


# ─── Generation Pipeline ──────────────────────────────────────────────────────
if generate:
    if not topic.strip():
        st.warning("⚠️ Enter a research topic.")
        st.stop()
    if not api_key.strip():
        st.error("❌ Enter your Gemini API key in the sidebar.")
        st.stop()

    steps_placeholder = st.empty()
    steps = [
        ("🌐", "Searching the web...", "active"),
        ("📥", "Extracting content...", "pending"),
        ("🧠", "AI analysis...", "pending"),
        ("📄", "Building report...", "pending"),
    ]

    def render_steps():
        html = "".join(_step_html(e, l, s) for e, l, s in steps)
        steps_placeholder.markdown(html, unsafe_allow_html=True)

    render_steps()

    try:
        # STEP 1-2: Search & scrape
        search_result = search_topic(topic)
        steps[0] = (steps[0][0], steps[0][1], "done")
        steps[1] = (steps[1][0], steps[1][1], "done")
        render_steps()

        raw_context = search_result["raw_context"]
        sources     = search_result["sources"]

        # STEP 3: Single AI call
        analyzer = GeminiAnalyzer(api_key=api_key.strip())
        steps[2] = (steps[2][0], steps[2][1], "active")
        render_steps()
        sections = analyzer.analyze(topic, raw_context)
        steps[2] = (steps[2][0], steps[2][1], "done")
        render_steps()

        # STEP 4: Build reports
        steps[3] = (steps[3][0], steps[3][1], "active")
        render_steps()

        docx_bytes = None
        pdf_bytes  = None

        if export_format in ("DOCX + PDF", "DOCX only"):
            docx_bytes = build_docx(topic, sections, sources)

        if export_format in ("DOCX + PDF", "PDF only"):
            pdf_bytes = build_pdf(topic, sections, sources)

        steps[3] = (steps[3][0], steps[3][1], "done")
        render_steps()

        # ── Results ──────────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="result-header">
          <h3>✅ Research Complete — <em>{topic}</em></h3>
          <p style="color:#94a3b8;margin:0;font-size:0.85rem;">
            {len(sources)} sources &nbsp;•&nbsp;
            {datetime.datetime.now().strftime('%H:%M, %d %b %Y')}
          </p>
        </div>
        """, unsafe_allow_html=True)

        # Downloads
        dl_cols = st.columns(2)
        with dl_cols[0]:
            if docx_bytes:
                safe = "".join(c if c.isalnum() or c in " _-" else "_" for c in topic)[:40].strip()
                st.download_button(
                    "⬇️ Download DOCX",
                    data=docx_bytes,
                    file_name=f"MrNews_{safe}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )
        with dl_cols[1]:
            if pdf_bytes:
                safe = "".join(c if c.isalnum() or c in " _-" else "_" for c in topic)[:40].strip()
                st.download_button(
                    "⬇️ Download PDF",
                    data=pdf_bytes,
                    file_name=f"MrNews_{safe}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

        st.markdown("")

        # Tabs
        tabs = st.tabs(["📋 Summary", "🔬 Expert Research", "📖 Plain English", "🌐 Sources"])

        with tabs[0]:
            st.markdown(sections.get("summary", "*No summary generated.*"))

        with tabs[1]:
            st.markdown(sections.get("expert_research", "*No expert research generated.*"))

        with tabs[2]:
            st.markdown(sections.get("plain_english", "*No plain english guide generated.*"))

        with tabs[3]:
            st.markdown(f"**{len(sources)} sources found:**")
            for src in sources[:30]:
                st.markdown(
                    f'<div class="source-item">'
                    f'<div class="source-title">🔗 {src["title"]}</div>'
                    f'<div class="source-url">{src["url"]}</div>'
                    f'<div style="color:#475569;font-size:0.78rem;margin-top:4px">{src.get("snippet","")[:140]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    except Exception as e:
        import traceback
        st.error(f"❌ Error:\n```\n{traceback.format_exc()}\n```")
        st.info("Check your Gemini API key and internet connection.")

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
  <span class="built-by">Built by Jayan</span>
</div>
""", unsafe_allow_html=True)
