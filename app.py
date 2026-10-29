"""
Meeting Notes Summarizer — v3
Turn Conversations Into Action.
Powered by NVIDIA Nemotron via Ollama (local) or Nebius Token Factory (cloud).
"""

import os
import re
import urllib.request
import urllib.error
import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be the very first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Meeting AI — Turn Conversations Into Action",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
/* ── Google Font ──────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Base reset ───────────────────────────────────────────── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── App background ───────────────────────────────────────── */
.stApp {
    background: radial-gradient(ellipse at 15% 0%,  #0d1b3e 0%,
                                                     #0a0f1e 55%,
                                                     #060912 100%);
    color: #e2e8f0;
}

/* ── Hide default chrome ──────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2.5rem;
    max-width: 900px;
}

/* ── Sidebar ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1f45 0%, #080e22 100%);
    border-right: 1px solid rgba(99,179,237,0.10);
}
[data-testid="stSidebar"] > div { padding-top: 0; }

/* ── Sidebar radio labels ─────────────────────────────────── */
[data-testid="stSidebar"] .stRadio label { color: #a0aec0 !important; font-size: 0.85rem; }
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    color: #cbd5e0; font-weight: 500;
}

/* ── Glass card ───────────────────────────────────────────── */
.glass-card {
    background: rgba(13, 27, 62, 0.55);
    border: 1px solid rgba(99,179,237,0.16);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    margin-bottom: 1.1rem;
    box-shadow: 0 4px 28px rgba(0,0,0,0.4);
}

/* ── Hero banner ──────────────────────────────────────────── */
.hero {
    background: linear-gradient(135deg, #162d6e 0%, #0e1f4f 50%, #09152f 100%);
    border: 1px solid rgba(99,179,237,0.22);
    border-radius: 20px;
    padding: 2rem 2.4rem 1.75rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(99,179,237,0.12) 0%, transparent 68%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-eyebrow {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #63b3ed;
    margin: 0 0 0.45rem;
}
.hero-title {
    font-size: 1.85rem;
    font-weight: 800;
    color: #f0f4ff;
    margin: 0 0 0.4rem;
    letter-spacing: -0.6px;
    line-height: 1.2;
}
.hero-sub {
    font-size: 0.92rem;
    color: #8bafd4;
    margin: 0;
    line-height: 1.55;
}

/* ── Section label above textarea ────────────────────────── */
.field-label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #8bafd4;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 0.35rem;
}

/* ── Primary button ───────────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4338ca, #6366f1) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.01em !important;
    padding: 0.72rem 1.6rem !important;
    box-shadow: 0 4px 18px rgba(99,102,241,0.45) !important;
    transition: all 0.18s ease !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 24px rgba(99,102,241,0.65) !important;
    filter: brightness(1.08) !important;
}
.stButton > button[kind="primary"]:active { filter: brightness(0.96) !important; }

/* ── Secondary / ghost buttons ────────────────────────────── */
.stButton > button:not([kind="primary"]) {
    background: rgba(99,179,237,0.08) !important;
    border: 1px solid rgba(99,179,237,0.28) !important;
    border-radius: 10px !important;
    color: #90cdf4 !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    transition: all 0.18s ease !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: rgba(99,179,237,0.18) !important;
    border-color: rgba(99,179,237,0.5) !important;
}

/* ── Download button ──────────────────────────────────────── */
.stDownloadButton > button {
    background: rgba(72,187,120,0.10) !important;
    border: 1px solid rgba(72,187,120,0.32) !important;
    border-radius: 10px !important;
    color: #68d391 !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    transition: all 0.18s ease !important;
}
.stDownloadButton > button:hover {
    background: rgba(72,187,120,0.2) !important;
    border-color: rgba(72,187,120,0.55) !important;
}

/* ── Textarea ─────────────────────────────────────────────── */
.stTextArea textarea {
    background: rgba(6,9,18,0.75) !important;
    border: 1px solid rgba(99,179,237,0.22) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', ui-monospace, monospace !important;
    font-size: 0.875rem !important;
    line-height: 1.6 !important;
    resize: vertical !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.55) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
    outline: none !important;
}
.stTextArea label { display: none !important; }   /* hidden; we use custom label */

/* ── Result section cards ─────────────────────────────────── */
.s-card {
    border-radius: 14px;
    padding: 1.1rem 1.4rem 0.9rem;
    margin-bottom: 0.85rem;
    position: relative;
}
.s-card.blue   { background: rgba(99,179,237,0.07); border-left: 3px solid #63b3ed; }
.s-card.green  { background: rgba(72,187,120,0.07); border-left: 3px solid #68d391; }
.s-card.amber  { background: rgba(246,173,85,0.07);  border-left: 3px solid #f6ad55; }
.s-card.purple { background: rgba(183,148,244,0.07); border-left: 3px solid #b794f4; }

.s-title {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    margin: 0 0 0.55rem;
    display: flex; align-items: center; gap: 0.45rem;
}
.s-title.blue   { color: #90cdf4; }
.s-title.green  { color: #9ae6b4; }
.s-title.amber  { color: #fbd38d; }
.s-title.purple { color: #d6bcfa; }

/* ── Empty-state placeholder ──────────────────────────────── */
.empty-state {
    text-align: center;
    padding: 3rem 2rem;
    color: #4a5568;
}
.empty-state .icon { font-size: 3rem; margin-bottom: 0.75rem; }
.empty-state p { font-size: 0.9rem; margin: 0; }

/* ── Token / meta badge ───────────────────────────────────── */
.meta-row {
    display: flex; flex-wrap: wrap; gap: 0.5rem;
    margin-top: 0.9rem; align-items: center;
}
.meta-pill {
    display: inline-flex; align-items: center; gap: 0.3rem;
    background: rgba(99,179,237,0.08);
    border: 1px solid rgba(99,179,237,0.18);
    border-radius: 20px;
    padding: 0.22rem 0.7rem;
    font-size: 0.75rem;
    color: #8bafd4;
}
.meta-pill strong { color: #90cdf4; }

/* ── Status dot ───────────────────────────────────────────── */
.status-row {
    display: flex; align-items: center; gap: 0.5rem;
    font-size: 0.8rem; color: #8bafd4;
    margin-top: 0.3rem;
}
.dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.dot.green  { background: #48bb78; box-shadow: 0 0 6px #48bb78; }
.dot.red    { background: #fc8181; box-shadow: 0 0 6px #fc8181; }
.dot.gray   { background: #718096; }

/* ── Sidebar model pill ───────────────────────────────────── */
.model-pill {
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 8px;
    padding: 0.45rem 0.65rem;
    font-size: 0.72rem;
    color: #a5b4fc;
    font-family: ui-monospace, monospace;
    word-break: break-all;
    line-height: 1.4;
    margin-top: 0.4rem;
}

/* ── Sidebar section header ───────────────────────────────── */
.sb-section {
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: #4a5568; margin: 0.3rem 0 0.5rem;
}

/* ── Word count / hint text ───────────────────────────────── */
.hint { font-size: 0.73rem; color: #4a5568; text-align: right; margin-top: -0.4rem; }

/* ── Alerts ───────────────────────────────────────────────── */
.stAlert { border-radius: 12px !important; }

/* ── Divider ──────────────────────────────────────────────── */
hr { border-color: rgba(99,179,237,0.10) !important; margin: 1rem 0 !important; }

/* ── Expander ─────────────────────────────────────────────── */
details > summary { color: #90cdf4 !important; font-size: 0.83rem !important; font-weight: 500 !important; }

/* ── Scrollbar (webkit) ───────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,179,237,0.25); border-radius: 3px; }
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS  — DO NOT change model name or endpoints
# ─────────────────────────────────────────────────────────────────────────────
OLLAMA_MODEL   = "hf.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB:Q4_K_M"
OLLAMA_BASE    = "http://localhost:11434/v1/"
OLLAMA_HEALTH  = "http://localhost:11434"          # plain GET to check liveness
NEBIUS_MODEL   = "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"
NEBIUS_BASE    = "https://api.tokenfactory.nebius.com/v1/"

SAMPLE_TRANSCRIPT = """\
Alice (PM): Good morning everyone. Let's kick off the Q4 planning meeting.
The main agenda is the product launch scheduled for November 30th.

Bob (Engineering): The backend API is 90% done. I need two more days to
finish the payment module. Should be ready by October 31st.

Priya (Design): UI mockups are approved. I'll hand off the final assets
to the dev team by October 29th.

Carlos (QA): Once assets are in, I can start integration testing on
November 1st. I'll need at least two weeks for a thorough test cycle.

Alice: So if QA finishes by November 15th, we have two weeks of buffer
before the launch. Let's set November 15th as the QA sign-off deadline.

Bob: Agreed. I'll also document the API endpoints by November 5th for
the frontend team.

Priya: I'll prepare the design system documentation alongside Bob's API
docs — also by November 5th.

Alice: Great. Next steps: Bob finishes payment module by Oct 31st,
Priya hands off assets Oct 29th, QA starts Nov 1st and signs off by
Nov 15th. I'll schedule a pre-launch review meeting for November 18th.
Any blockers?

Carlos: No blockers from QA side.
Bob: All clear from engineering.
Priya: Same from design.

Alice: Perfect. Meeting adjourned.\
"""

SYSTEM_PROMPT = """\
You are an expert meeting analyst.

Summarize the supplied meeting transcript in simple, professional English.

Use exactly these four section headings (keep the numbering):

## 1. Key Discussion Points
List the main topics discussed as bullet points.

## 2. Decisions Made
List the decisions and agreements reached as bullet points.

## 3. Action Items
For each task, use this exact format:
- [Owner] – [Task] (Deadline: [date or 'Not specified'])
Include every action item mentioned, even if the deadline is not specified.

## 4. Next Steps
List follow-up activities and upcoming meetings as bullet points.

Rules:
- Be concise; avoid repeating information.
- Use bullet points for every item.
- Do NOT invent names, dates, decisions, or tasks.
- Write "Not specified" when important details are missing.
- Preserve the meaning of the original transcript exactly.\
"""

SECTION_CONFIGS = [
    {
        "key":     "Key Discussion Points",
        "pattern": r"##\s*1\.\s*Key Discussion Points(.*?)(?=##\s*2\.|$)",
        "icon":    "💬",
        "color":   "blue",
        "title":   "Key Discussion Points",
    },
    {
        "key":     "Decisions Made",
        "pattern": r"##\s*2\.\s*Decisions Made(.*?)(?=##\s*3\.|$)",
        "icon":    "✅",
        "color":   "green",
        "title":   "Decisions Made",
    },
    {
        "key":     "Action Items",
        "pattern": r"##\s*3\.\s*Action Items(.*?)(?=##\s*4\.|$)",
        "icon":    "📋",
        "color":   "amber",
        "title":   "Action Items",
    },
    {
        "key":     "Next Steps",
        "pattern": r"##\s*4\.\s*Next Steps(.*?)$",
        "icon":    "🚀",
        "color":   "purple",
        "title":   "Next Steps",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def check_ollama_liveness() -> bool:
    """
    Perform a real HTTP GET to the Ollama root endpoint.
    Returns True only if Ollama responds within 2 seconds.
    This is an honest connectivity check — no fake status.
    """
    try:
        with urllib.request.urlopen(OLLAMA_HEALTH, timeout=2) as resp:
            return resp.status < 500
    except Exception:
        return False


@st.cache_data(ttl=30, show_spinner=False)
def cached_ollama_status() -> bool:
    """Cache the Ollama health result for 30 s to avoid probing on every widget interaction."""
    return check_ollama_liveness()


def get_client(selected_provider: str) -> OpenAI:
    """
    Return a cached OpenAI-compatible client for the chosen provider.
    Session-state cache avoids re-creating the client on every rerun.
    """
    cache_key = f"_ai_client_{selected_provider}"
    if cache_key not in st.session_state:
        if selected_provider == "Ollama (Local)":
            st.session_state[cache_key] = OpenAI(
                base_url=OLLAMA_BASE,
                api_key="ollama",      # Ollama ignores this but the SDK requires a non-empty value
                timeout=300.0,
                max_retries=0,
            )
        else:
            api_key = os.environ.get("NEBIUS_API_KEY", "")
            if not api_key:
                raise ValueError(
                    "NEBIUS_API_KEY environment variable is not set.\n\n"
                    "Open PowerShell and run:\n"
                    "  $env:NEBIUS_API_KEY = 'your_key_here'\n"
                    "Then restart the app."
                )
            st.session_state[cache_key] = OpenAI(
                api_key=api_key,
                base_url=NEBIUS_BASE,
                timeout=90.0,
                max_retries=1,
            )
    return st.session_state[cache_key]


def parse_sections(text: str) -> dict:
    """Extract the four named sections from the AI markdown response."""
    result = {}
    for cfg in SECTION_CONFIGS:
        m = re.search(cfg["pattern"], text, re.DOTALL | re.IGNORECASE)
        result[cfg["key"]] = m.group(1).strip() if m else ""
    return result


def render_result_card(icon: str, title: str, color: str, content: str) -> None:
    """Render a coloured result card header, then the markdown content below it."""
    st.markdown(
        f'<div class="s-card {color}">'
        f'<p class="s-title {color}">{icon}&nbsp;&nbsp;{title}</p>'
        f"</div>",
        unsafe_allow_html=True,
    )
    if content:
        st.markdown(content)
    else:
        st.markdown(
            "<p style='color:#4a5568;font-size:0.85rem;font-style:italic;'>"
            "Nothing found for this section.</p>",
            unsafe_allow_html=True,
        )


def clipboard_button(text: str, label: str = "📋 Copy Summary") -> None:
    """Inline JS copy-to-clipboard — works on localhost and https:// origins."""
    safe = (
        text.replace("\\", "\\\\")
            .replace("`", "\\`")
            .replace("$", "\\$")
            .replace("\r", "")
    )
    components.html(
        f"""
        <button id="cb-btn"
            onclick="
                navigator.clipboard.writeText(`{safe}`)
                    .then(()=>{{
                        document.getElementById('cb-btn').textContent='✅ Copied!';
                        setTimeout(()=>document.getElementById('cb-btn').textContent='{label}',2200);
                    }})
                    .catch(()=>alert('Copy failed — please select and copy manually.'));
            "
            style="
                background:rgba(99,179,237,0.10);
                border:1px solid rgba(99,179,237,0.32);
                border-radius:10px;
                color:#90cdf4;
                font-family:Inter,sans-serif;
                font-size:0.85rem;font-weight:500;
                padding:0.48rem 1rem;
                cursor:pointer;width:100%;
                transition:background 0.18s,border-color 0.18s;
            "
            onmouseover="this.style.background='rgba(99,179,237,0.2)';this.style.borderColor='rgba(99,179,237,0.5)';"
            onmouseout="this.style.background='rgba(99,179,237,0.10)';this.style.borderColor='rgba(99,179,237,0.32)';"
        >{label}</button>
        """,
        height=50,
    )


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # ── Logo / brand ──────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center;padding:1.4rem 0 0.8rem;">
            <div style="font-size:2.8rem;line-height:1;">🎙️</div>
            <div style="font-size:1.05rem;font-weight:800;color:#e2e8f0;
                        letter-spacing:-0.3px;margin-top:0.3rem;">
                Meeting&nbsp;AI
            </div>
            <div style="font-size:0.72rem;color:#4a5568;margin-top:0.1rem;">
                Turn Conversations Into Action
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Provider selector ─────────────────────────────────────────
    st.markdown("<p class='sb-section'>AI Provider</p>", unsafe_allow_html=True)
    provider = st.radio(
        label="ai_provider",
        options=["Ollama (Local)", "Nebius Token Factory"],
        index=0,
        label_visibility="collapsed",
    )

    # ── Active model badge ────────────────────────────────────────
    active_model = OLLAMA_MODEL if provider == "Ollama (Local)" else NEBIUS_MODEL
    st.markdown(
        f"<div class='model-pill'>{active_model}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

    # ── Ollama live status indicator ──────────────────────────────
    if provider == "Ollama (Local)":
        ollama_up = cached_ollama_status()
        if ollama_up:
            st.markdown(
                "<div class='status-row'>"
                "<span class='dot green'></span>"
                "<span>Ollama reachable on localhost:11434</span>"
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='status-row'>"
                "<span class='dot red'></span>"
                "<span>Ollama not detected — see setup below</span>"
                "</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-size:0.72rem;color:#4a5568;margin-top:0.25rem;'>"
                "Status refreshes every 30 s.</p>",
                unsafe_allow_html=True,
            )
    else:
        nebius_key_set = bool(os.environ.get("NEBIUS_API_KEY", ""))
        if nebius_key_set:
            st.markdown(
                "<div class='status-row'>"
                "<span class='dot green'></span>"
                "<span>NEBIUS_API_KEY detected</span>"
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='status-row'>"
                "<span class='dot red'></span>"
                "<span>NEBIUS_API_KEY not set</span>"
                "</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── How to use ────────────────────────────────────────────────
    with st.expander("ℹ️ How to use"):
        st.markdown(
            """
1. **Choose provider** — Ollama (local) or Nebius (cloud)
2. Paste or load a meeting transcript
3. Click **✨ Summarize Meeting**
4. Review the four summary sections
5. Copy or download the result
            """,
        )

    # ── Ollama setup guide ────────────────────────────────────────
    with st.expander("🖥️ Ollama Setup"):
        st.markdown(
            f"""
**1. Install Ollama**  
Download from [ollama.ai](https://ollama.ai) and install.

**2. Pull the model**
```
ollama pull {OLLAMA_MODEL}
```

**3. Start the server**
```
ollama serve
```

The green status dot above confirms Ollama is running.
            """,
        )

    # ── Nebius setup guide ────────────────────────────────────────
    with st.expander("☁️ Nebius API Setup"):
        st.markdown(
            """
**1.** Sign in at [tokenfactory.nebius.com](https://tokenfactory.nebius.com)  
**2.** Create an API key  
**3.** Set it before starting the app:

```powershell
# Windows PowerShell
$env:NEBIUS_API_KEY = "your_key"
```
```bash
# macOS / Linux
export NEBIUS_API_KEY="your_key"
```
            """,
        )

    # ── Sidebar footer ────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center;font-size:0.68rem;color:#2d3748;
                    padding-top:1rem;border-top:1px solid rgba(99,179,237,0.07);
                    margin-top:1rem;">
            MIT License &nbsp;·&nbsp; Meeting AI v3.0
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────────────────────────────────────

# ── Hero banner ───────────────────────────────────────────────────────────────
provider_display = "Ollama · Local Nemotron" if provider == "Ollama (Local)" else "Nebius · Cloud Nemotron"
st.markdown(
    f"""
    <div class="hero">
        <p class="hero-eyebrow">🎙️ AI Meeting Assistant</p>
        <p class="hero-title">Turn Conversations Into Action</p>
        <p class="hero-sub">
            Paste any meeting transcript and get a structured AI summary in seconds —
            key points, decisions, action items, and next steps.
            &nbsp;<span style="opacity:0.45">|</span>&nbsp;
            <span style="color:#6baed4;">{provider_display}</span>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Input card ────────────────────────────────────────────────────────────────
# Row: field label + sample button (right-aligned)
lbl_col, btn_col = st.columns([6, 1])
with lbl_col:
    st.markdown(
        "<p class='field-label'>📄 Meeting Transcript</p>",
        unsafe_allow_html=True,
    )
with btn_col:
    if st.button("📄 Sample", help="Load a sample Q4 planning transcript"):
        st.session_state["_transcript"] = SAMPLE_TRANSCRIPT
        st.rerun()

# Initialise transcript session key
if "_transcript" not in st.session_state:
    st.session_state["_transcript"] = ""

# Text area — key drives the widget value; on_change syncs edits back
def _sync_transcript():
    st.session_state["_transcript"] = st.session_state["_ta_widget"]

transcript_value = st.session_state["_transcript"]

transcript = st.text_area(
    label="Meeting transcript input",
    label_visibility="collapsed",
    value=transcript_value,
    height=270,
    placeholder=(
        "Paste your meeting transcript here…\n\n"
        "Example:\n"
        "Alice: We need to finish the website by Friday.\n"
        "Bob: I'll complete the homepage by Wednesday.\n"
        "Priya: I'll test everything by Thursday."
    ),
    key="_ta_widget",
    on_change=_sync_transcript,
)

# Live word / char count
w = len(transcript.split()) if transcript.strip() else 0
c = len(transcript)
st.markdown(
    f"<p class='hint'>{w:,} words &nbsp;·&nbsp; {c:,} characters</p>",
    unsafe_allow_html=True,
)

# ── Summarize button ──────────────────────────────────────────────────────────
st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
summarize_btn = st.button(
    "✨ Summarize Meeting",
    type="primary",
    use_container_width=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# SUMMARIZATION LOGIC  (unchanged from working version)
# ─────────────────────────────────────────────────────────────────────────────
if summarize_btn:
    if not transcript.strip():
        st.warning(
            "⚠️  Please paste your meeting transcript before summarizing.",
        )
    else:
        model = OLLAMA_MODEL if provider == "Ollama (Local)" else NEBIUS_MODEL

        try:
            client = get_client(provider)

            with st.spinner(f"Analysing transcript with {provider}…"):
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system",  "content": SYSTEM_PROMPT},
                        {
                            "role": "user",
                            "content": "Summarize these meeting notes:\n\n" + transcript.strip(),
                        },
                    ],
                    temperature=0.2,
                    max_tokens=1200,
                )

            summary = (response.choices[0].message.content or "").strip()

            if not summary:
                st.error(
                    "🤖 The AI returned an empty response. "
                    "Please try again. If the problem persists, "
                    "try a shorter transcript."
                )
            else:
                st.session_state["meeting_summary"]  = summary
                st.session_state["summary_provider"] = provider
                st.session_state["summary_usage"]    = (
                    response.usage.model_dump() if response.usage else None
                )

        except ValueError as exc:
            st.error(f"🔑 Configuration error: {exc}")
        except Exception as exc:
            st.error(f"🚨 Unable to generate summary: {exc}")
            if provider == "Ollama (Local)":
                st.info(
                    "**Ollama troubleshooting:**\n"
                    "- Is Ollama running? Try `ollama serve` in a terminal.\n"
                    f"- Is the model pulled? Run: `ollama pull {OLLAMA_MODEL}`\n"
                    "- Local inference can take 1–3 minutes on CPU — please be patient.\n"
                    "- Check the sidebar status indicator for live connectivity."
                )
            else:
                st.info(
                    "**Nebius troubleshooting:**\n"
                    "- Check that `NEBIUS_API_KEY` is set correctly.\n"
                    "- Verify your internet connection.\n"
                    "- Confirm the model is available in your Token Factory account.\n"
                    "- Check usage limits at tokenfactory.nebius.com."
                )

# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY DISPLAY
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.get("meeting_summary"):
    summary       = st.session_state["meeting_summary"]
    used_provider = st.session_state.get("summary_provider", "AI")
    usage         = st.session_state.get("summary_usage")

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Results header row
    h_col, p_col = st.columns([5, 2])
    with h_col:
        st.markdown(
            "<h2 style='color:#e2e8f0;font-size:1.25rem;font-weight:700;"
            "margin:0;letter-spacing:-0.3px;'>📊 Meeting Summary</h2>",
            unsafe_allow_html=True,
        )
    with p_col:
        st.markdown(
            f"<div style='text-align:right;padding-top:0.2rem;'>"
            f"<span style='font-size:0.75rem;color:#4a5568;'>Generated via&nbsp;</span>"
            f"<span style='font-size:0.75rem;color:#90cdf4;font-weight:600;'>{used_provider}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

    # ── Parse and render 4 section cards ──────────────────────────
    sections = parse_sections(summary)
    any_parsed = any(v for v in sections.values())

    if any_parsed:
        for cfg in SECTION_CONFIGS:
            render_result_card(
                icon    = cfg["icon"],
                title   = cfg["title"],
                color   = cfg["color"],
                content = sections.get(cfg["key"], ""),
            )
    else:
        # Fallback: raw markdown in a glass card (in case heading format differs)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown(summary)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Actions: copy + download ───────────────────────────────────
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    a_col1, a_col2 = st.columns(2)
    with a_col1:
        clipboard_button(summary)
    with a_col2:
        st.download_button(
            label            = "⬇️ Download as Markdown",
            data             = summary,
            file_name        = "meeting_summary.md",
            mime             = "text/markdown",
            use_container_width = True,
        )

    # ── Token usage ────────────────────────────────────────────────
    if usage:
        p_tok = usage.get("prompt_tokens",     0)
        c_tok = usage.get("completion_tokens", 0)
        t_tok = usage.get("total_tokens",      0)
        st.markdown(
            f"<div class='meta-row'>"
            f"<span class='meta-pill'>🔢 Prompt <strong>{p_tok:,}</strong></span>"
            f"<span class='meta-pill'>✍️ Completion <strong>{c_tok:,}</strong></span>"
            f"<span class='meta-pill'>∑ Total <strong>{t_tok:,}</strong></span>"
            f"</div>",
            unsafe_allow_html=True,
        )

else:
    # ── Empty state — shown before any summary is generated ────────
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="empty-state">
            <div class="icon">📝</div>
            <p style="font-size:1rem;font-weight:600;color:#2d3748;margin-bottom:0.4rem;">
                No summary yet
            </p>
            <p>Paste a meeting transcript above and click<br>
               <strong style="color:#6366f1;">✨ Summarize Meeting</strong> to get started.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
