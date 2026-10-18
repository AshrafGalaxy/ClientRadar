# 🎯 ClientRadar AI

> Autonomous freelance lead-arbitrage engine powered by **SerpApi** and **Google Gemma 2**.  
> Built for the Hacktoberfest open source AI challenge.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io)
[![SerpApi](https://img.shields.io/badge/SerpApi-Google%20Jobs-00C853.svg)](https://serpapi.com)
[![Gemma 2](https://img.shields.io/badge/Google-Gemma%202--2B--IT-4285F4.svg)](https://huggingface.co/google/gemma-2-2b-it)

---

## 💡 Overview
Freelancers and boutique technical consultants spend 10-15 hours every week scanning job boards, filtering low-budget listings, and drafting custom outreach pitches.

**ClientRadar AI** turns this manual grind into an autonomous, 30-second pipeline:
1. **Live Discovery & Deep-Linking**: Leverages **SerpApi's** `google_jobs` engine to harvest fresh, high-ticket tech contracts across LinkedIn, Indeed, ZipRecruiter, and company portals in real time with direct application deep-links.
2. **Multi-Tier Viability & Risk Scoring**: Google's open-weight **Gemma 2** (`google/gemma-2-2b-it`) parses the job description, evaluates Scope Clarity (35 pts), Budget Alignment (35 pts), and Timeline Realism (30 pts), while auditing for scope-creep or equity-only red flags.
3. **Custom Outreach Pitch Studio**: Gemma 2 crafts tailored proposals with selectable pitch strategies (*Direct Technical*, *Fast 48h Turnaround*, or *Strategic Retainer*) with 1-click Markdown download and clipboard copy.
4. **Minimalist Developer Interface**: Designed with crisp inline SVG icons, KPI metrics bar, and Dark/Light mode appearance styling.

---

## 🏗️ Architecture

```
               ┌───────────────────────┐
               │    Freelancer / User  │
               └──────────┬────────────┘
                          │ (Streamlit Web Dashboard)
                          ▼
             ┌─────────────────────────────┐
             │       ClientRadar Core      │
             └──────────┬──────────────┬───┘
                        │              │
        SerpApi REST API│              │Prompt Payload
       (Live Web Search)│              │(Hugging Face / Gemma 2)
                        ▼              ▼
            ┌────────────────┐   ┌──────────────────────┐
            │   Google Jobs  │   │     Google Gemma 2   │
            │  (Live Postings│   │   (Open-Weight LLM)  │
            └────────────────┘   └──────────────────────┘
```

---

## ⚡ Quickstart

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/AshrafGalaxy/ClientRadar.git
cd ClientRadar

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Credentials (Optional)
Copy `.env.example` to `.env` and fill in your keys:
```env
SERPAPI_API_KEY=your_serpapi_key_here
HUGGINGFACE_TOKEN=hf_your_token_here
```
> **Note:** ClientRadar includes an automatic **Deterministic Demo Mode**. If you leave keys blank, it runs with realistic mock leads and simulated Gemma 2 outputs for zero-friction demonstrations!

### 3. Launch the Application
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔑 How to Get API Keys

| Service | Cost | Setup Link | Instructions |
| :--- | :--- | :--- | :--- |
| **SerpApi** | Free (100 searches/mo) | [serpapi.com/manage-api-key](https://serpapi.com/manage-api-key) | Sign up and copy your Private API Key. |
| **Hugging Face Gemma 2** | Free (Serverless) | [google/gemma-2-2b-it](https://huggingface.co/google/gemma-2-2b-it) | Accept the Google Gemma license, then create a Read token at [hf.co/settings/tokens](https://huggingface.co/settings/tokens). |

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
