# 🎙️ Meeting Notes Summarizer

A **polished, hackathon-ready AI meeting assistant** built with Streamlit and powered by
**NVIDIA Nemotron** models via **Nebius Token Factory** (cloud) or a local **Ollama** instance.

Paste any meeting transcript, click **Summarize Meeting**, and receive a beautifully structured
summary — key discussion points, decisions, action items, and next steps.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎨 **Premium dark UI** | Navy glass-morphism dashboard, Inter font, responsive layout |
| 🤖 **Dual AI providers** | Local Ollama (Nemotron-3.5-Bolt) or Nebius Token Factory (Nemotron-3-Nano-30B) |
| 📄 **Sample transcript** | One-click load for quick demos |
| 📊 **Structured results** | 4 colour-coded cards: Key Points, Decisions, Actions, Next Steps |
| 📋 **Copy to clipboard** | One-click copy of the full summary |
| ⬇️ **Markdown download** | Save the summary as a `.md` file |
| 🔢 **Token usage badge** | Prompt / completion / total token counts after each call |
| 🔒 **Secure key handling** | API key read from environment variable only — never in code or UI |

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/your-username/meeting-notes-agent.git
cd meeting-notes-agent
```

### 2. Create & activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Choose your AI provider

#### Option A — Nebius Token Factory (cloud, recommended)

1. Sign in at [Nebius Token Factory](https://tokenfactory.nebius.com/).
2. Navigate to **API Keys** and create a new key.
3. The app uses model `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`. Confirm it is available in your account.

> **About Nebius Token Factory**  
> Nebius Token Factory provides pay-per-token access to NVIDIA Nemotron and other frontier
> models through an OpenAI-compatible REST API — no GPU infrastructure required.

Set the API key in your shell:

```powershell
# Windows PowerShell
$env:NEBIUS_API_KEY = "your_api_key_here"
```

```bash
# macOS / Linux
export NEBIUS_API_KEY="your_api_key_here"
```

#### Option B — Ollama (local, offline)

1. Install [Ollama](https://ollama.ai).
2. Pull the Nemotron model:
   ```bash
   ollama pull hf.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB:Q4_K_M
   ```
3. Start Ollama: `ollama serve`
4. Select **Ollama (Local)** in the sidebar — no API key needed.

### 5. Run the app

```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

---

## 🗂️ Project Structure

```
meeting-notes-agent/
├── app.py            # Main Streamlit application (redesigned)
├── app_backup.py     # Original app.py backup
├── requirements.txt  # Python dependencies
├── LICENSE           # MIT License
└── README.md         # This file
```

---

## 🔧 Configuration

| Variable | Description |
|---|---|
| `NEBIUS_API_KEY` | Nebius Token Factory API key (required for cloud provider) |

---

## 🤖 Models

| Provider | Model ID |
|---|---|
| **Nebius Token Factory** | `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B` |
| **Ollama (local)** | `hf.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB:Q4_K_M` |

Both use an **OpenAI-compatible** `/chat/completions` API.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
