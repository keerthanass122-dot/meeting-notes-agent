
import os
import streamlit as st
from openai import OpenAI

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Meeting Notes Summarizer",
    page_icon="📝",
    layout="centered",
)

st.title("📝 Meeting Notes Summarizer")
st.caption(
    "Turn meeting transcripts into clear summaries, "
    "decisions, action items, and next steps."
)
st.divider()

# --------------------------------------------------
# AI PROVIDER SELECTION
# --------------------------------------------------
provider = st.radio(
    "Choose your AI provider:",
    ["Ollama (Local)", "Nebius Token Factory"],
    horizontal=True,
)

# --------------------------------------------------
# MODEL CONFIGURATION
# --------------------------------------------------
if provider == "Ollama (Local)":
    MODEL = (
        "hf.co/nvidia/"
        "NVIDIA-Nemotron-3.5-Bolt-E4B-4GB:Q4_K_M"
    )

    @st.cache_resource(show_spinner=False)
    def get_client():
        return OpenAI(
            base_url="http://localhost:11434/v1/",
            api_key="ollama",
            timeout=300.0,
            max_retries=0,
        )

else:
    MODEL = "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"

    @st.cache_resource(show_spinner=False)
    def get_client():
        api_key = os.environ.get("NEBIUS_API_KEY", "")

        if not api_key:
            raise ValueError(
                "NEBIUS_API_KEY is not set. "
                "Set your Nebius API key in PowerShell "
                "and restart the app."
            )

        return OpenAI(
            api_key=api_key,
            base_url="https://api.tokenfactory.nebius.com/v1/",
            timeout=90.0,
            max_retries=1,
        )

# --------------------------------------------------
# MEETING SUMMARY INSTRUCTIONS
# --------------------------------------------------
SYSTEM_PROMPT = """
You are an expert meeting analyst.

Summarize the supplied meeting transcript in simple,
professional English.

Use these four sections:

## 1. Key Discussion Points
List the main topics discussed.

## 2. Decisions Made
List the decisions and agreements reached.

## 3. Action Items
For each task, include the responsible person and deadline
when provided in the transcript.

## 4. Next Steps
List follow-up activities and upcoming meetings.

Important rules:
- Be concise and avoid repeating information.
- Use bullet points.
- Do not invent names, dates, decisions, or tasks.
- Write "Not specified" when important details are missing.
- Preserve the meaning of the original meeting notes.
"""

# --------------------------------------------------
# MEETING TRANSCRIPT INPUT
# --------------------------------------------------
transcript = st.text_area(
    "Paste your meeting transcript or notes here:",
    height=250,
    placeholder=(
        "Alice: We need to finish the website by Friday.\n"
        "Bob: I will complete the homepage by Wednesday.\n"
        "Priya: I will test the website by Thursday.\n"
        "Alice: We will launch on Friday if testing succeeds."
    ),
)

summarize_btn = st.button(
    "✨ Summarize Meeting",
    type="primary",
    use_container_width=True,
)

# --------------------------------------------------
# SUMMARIZATION
# --------------------------------------------------
if summarize_btn:
    if not transcript.strip():
        st.warning(
            "Please paste your meeting notes before summarizing."
        )

    else:
        try:
            client = get_client()

            with st.spinner(
                f"Generating your summary using {provider}..."
            ):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT,
                        },
                        {
                            "role": "user",
                            "content": (
                                "Summarize these meeting notes:\n\n"
                                + transcript.strip()
                            ),
                        },
                    ],
                    temperature=0.2,
                    max_tokens=400,
                )

            summary = response.choices[0].message.content or ""
            summary = summary.strip()

            if not summary:
                st.error(
                    "The AI returned an empty summary. "
                    "Please try again."
                )

            else:
                st.session_state["meeting_summary"] = summary
                st.session_state["summary_provider"] = provider
                st.session_state["summary_usage"] = (
                    response.usage.model_dump()
                    if response.usage
                    else None
                )

        except Exception as exc:
            st.error(f"Unable to generate the summary: {exc}")

            if provider == "Ollama (Local)":
                st.info(
                    "Check that Ollama is running and your model "
                    "is available. Local generation may be slower "
                    "because it uses your computer's CPU."
                )
            else:
                st.info(
                    "Check your Nebius API key, internet connection, "
                    "model access, and API usage limits."
                )

# --------------------------------------------------
# DISPLAY SUMMARY AND DOWNLOAD
# --------------------------------------------------
if st.session_state.get("meeting_summary"):
    summary = st.session_state["meeting_summary"]

    st.divider()
    st.subheader("📋 Meeting Summary")
    st.markdown(summary)

    st.download_button(
        label="⬇️ Download Summary (.md)",
        data=summary,
        file_name="meeting_summary.md",
        mime="text/markdown",
        use_container_width=True,
    )

    usage = st.session_state.get("summary_usage")

    if usage:
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        total_tokens = usage.get("total_tokens", 0)

        st.caption(
            f"Tokens — prompt: {prompt_tokens} · "
            f"completion: {completion_tokens} · "
            f"total: {total_tokens}"
        )

    st.caption(
        f"Generated using: "
        f"{st.session_state.get('summary_provider', 'AI')}"
    )
