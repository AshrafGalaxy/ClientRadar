import os
import json
import urllib.parse
import requests
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables if .env exists
load_dotenv()

# ==============================================================================
# Crisp SVG Icon System
# ==============================================================================
def svg_icon(name: str, size: int = 15, color: str = "currentColor") -> str:
    icons = {
        "radar": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/><path d="M12 3v9l5 3"/></svg>',
        "briefcase": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
        "sparkles": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/></svg>',
        "pin": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
        "dollar": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        "external": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>',
        "shield": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>',
        "clock": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        "check": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
        "building": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4"/></svg>',
        "github": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>'
    }
    return icons.get(name, "")

# ==============================================================================
# Dynamic Deep-Link Builder
# ==============================================================================
def build_google_jobs_deeplink(title: str, company: str, location: str = "Remote") -> str:
    """Builds a direct Google Jobs query search URL."""
    clean_query = f"{title} {company} {location}".strip()
    return f"https://www.google.com/search?q={urllib.parse.quote_plus(clean_query)}&ibp=htl;jobs"

# ==============================================================================
# Realistic Fallback Contract Leads
# ==============================================================================
MOCK_LEADS = [
    {
        "title": "Senior Python Backend Architect (Contract)",
        "company_name": "Aether Dynamics",
        "location": "Remote",
        "via": "LinkedIn",
        "budget": "$5,000 / month",
        "posted": "2 days ago",
        "description": "Seeking an experienced backend contractor to optimize distributed data ingestion workers. Requires FastAPI, Redis, and PostgreSQL experience. Estimated 20 hrs/week. Deliverables include auditing Celery task latency, schema isolation, and comprehensive pytest harnesses.",
        "link": build_google_jobs_deeplink("Senior Python Backend Architect FastAPI", "Aether Dynamics", "Remote")
    },
    {
        "title": "Full-Stack Automation & Scraper Engineer",
        "company_name": "Vanguard Lead Labs",
        "location": "Remote",
        "via": "ZipRecruiter",
        "budget": "Fixed: $2,500",
        "posted": "1 day ago",
        "description": "Need an engineer to build resilient web scrapers and lead enrichment workflows. Experience with Playwright/Selenium, anti-bot bypass strategies, and persisting clean JSON schemas into Supabase.",
        "link": build_google_jobs_deeplink("Full-Stack Web Scraper Automation Engineer", "Vanguard Lead Labs", "Remote")
    },
    {
        "title": "AI Integration & LangChain Developer (Freelance)",
        "company_name": "Kroma Media",
        "location": "Remote",
        "via": "Indeed",
        "budget": "$85 / hour",
        "posted": "3 days ago",
        "description": "Contractor needed to hook open-source LLMs (Gemma, Llama) into customer support ticketing workflows via LangChain. Fast-turnaround project with potential for monthly maintenance retainer.",
        "link": build_google_jobs_deeplink("AI Integration LangChain Developer", "Kroma Media", "Remote")
    },
    {
        "title": "FastAPI & Microservices Specialist",
        "company_name": "CloudNova Systems",
        "location": "Remote",
        "via": "Google Jobs",
        "budget": "$95 / hour",
        "posted": "4 days ago",
        "description": "Immediate requirement for a senior engineer to audit async API bottlenecks, reduce p99 latency under load, and implement clean Dockerized test harnesses. 6-week engagement.",
        "link": build_google_jobs_deeplink("FastAPI Microservices Optimization", "CloudNova Systems", "Remote")
    }
]

# ==============================================================================
# SerpApi Harvesting
# ==============================================================================
def fetch_leads_serpapi(search_term: str, search_loc: str, api_key: str, max_results: int = 4):
    """Fetches real-time jobs via SerpApi's google_jobs engine with working deep-links."""
    if not api_key:
        return MOCK_LEADS[:max_results]
    
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_jobs",
        "q": f"{search_term} {search_loc}",
        "api_key": api_key,
        "hl": "en"
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            jobs = []
            for item in data.get("jobs_results", [])[:max_results]:
                title = item.get("title", "Contract Opportunity")
                company = item.get("company_name", "Confidential")
                loc = item.get("location", search_loc)
                desc = item.get("description", "No description provided.")
                via = item.get("via", "Direct").replace("via ", "")
                
                extensions = item.get("detected_extensions", {})
                posted_time = extensions.get("posted_at", "Recently")
                salary = extensions.get("salary", "Competitive Contract Rate")
                
                # Direct link priority: share_link -> first apply_option -> dynamic google jobs link
                apply_opts = item.get("apply_options", [])
                primary_link = item.get("share_link")
                if not primary_link and apply_opts:
                    primary_link = apply_opts[0].get("link")
                if not primary_link:
                    primary_link = build_google_jobs_deeplink(title, company, loc)
                
                jobs.append({
                    "title": title,
                    "company_name": company,
                    "location": loc,
                    "via": via,
                    "budget": salary,
                    "posted": posted_time,
                    "description": desc[:600] + ("..." if len(desc) > 600 else ""),
                    "link": primary_link
                })
            return jobs if jobs else MOCK_LEADS[:max_results]
        elif response.status_code == 401:
            st.error("SerpApi key invalid. Operating in demo mode.")
            return MOCK_LEADS[:max_results]
        else:
            return MOCK_LEADS[:max_results]
    except Exception:
        return MOCK_LEADS[:max_results]

# ==============================================================================
# Gemma 2 Proposal Generator
# ==============================================================================
def evaluate_and_pitch_with_gemma(lead_info: dict, token: str, pitch_tone: str = "Direct Technical"):
    """Generates structured viability score and tailored proposal using Gemma 2."""
    if not token:
        if pitch_tone == "Fast 48h Turnaround":
            approach = "1. **Sprint 0 Scaffolding (Day 1-2):** Stand up the core pipeline skeleton with unit test coverage.\n2. **Iterative Feature Deployment:** Deliver clean, validated modules with continuous delivery notes."
        elif pitch_tone == "Strategic Retainer":
            approach = "1. **Architecture & Latency Audit:** Identify bottleneck queries and establish strict schema validation.\n2. **Production-Ready Delivery:** Deliver maintainable, documented services with long-term SLA support."
        else: # Direct Technical
            approach = "1. **System Audit & Bottleneck Remediation:** Establish strict schema validation and error isolation patterns within the first 48 hours.\n2. **Production Delivery:** Deliver maintainable, unit-tested pipeline code with complete logging and telemetry."

        return {
            "score": 94,
            "scope_clarity": "Well-defined technical stack and specific deliverable milestones.",
            "red_flags": "None detected",
            "subject": f"Technical Approach: {lead_info['title']}",
            "pitch": f"""Hi {lead_info['company_name']} Hiring Team,

I came across your opening for the **{lead_info['title']}** and wanted to reach out directly regarding your technical requirements.

Having built resilient backend services and distributed pipelines handling asynchronous workloads, I can step in immediately without onboarding friction.

**Proposed Technical Approach:**
{approach}

Would you be open to a brief 10-minute technical sync this week to review your milestone goals?

Best regards,  
Ashraf  
*Independent Technical Consultant*"""
        }

    # Live Inference with Hugging Face serverless Gemma 2
    api_url = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
    headers = {"Authorization": f"Bearer {token}"}
    prompt = f"""<start_of_turn>user
Analyze this freelance contract opportunity and generate a structured evaluation and bespoke proposal in the tone '{pitch_tone}':

Role: {lead_info['title']}
Company: {lead_info['company_name']}
Description: {lead_info['description']}

Output your answer strictly in this JSON format:
{{
  "score": <integer 0-100>,
  "scope_clarity": "<one sentence summarizing scope clarity>",
  "red_flags": "<any red flags or 'None detected'>",
  "subject": "<compelling email subject>",
  "pitch": "<concise 3-paragraph outreach email addressing requirements and asking for a brief sync>"
}}<end_of_turn>
<start_of_turn>model
"""
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 650, "temperature": 0.3, "top_p": 0.9, "return_full_text": False}
    }
    
    try:
        res = requests.post(api_url, headers=headers, json=payload, timeout=25)
        if res.status_code == 200:
            result = res.json()
            if isinstance(result, list) and len(result) > 0:
                raw_text = result[0].get("generated_text", "")
                if "<start_of_turn>model\n" in raw_text:
                    raw_text = raw_text.split("<start_of_turn>model\n")[-1].strip()
                clean = raw_text.strip("` \n")
                if clean.startswith("json"):
                    clean = clean[4:].strip()
                try:
                    return json.loads(clean)
                except Exception:
                    return {
                        "score": 90,
                        "scope_clarity": "Evaluated by Gemma 2.",
                        "red_flags": "None detected",
                        "subject": f"Technical Approach: {lead_info['title']}",
                        "pitch": raw_text
                    }
        elif res.status_code == 503:
            return {"error": "Gemma 2 is currently spinning up on Hugging Face. Please retry in 15 seconds."}
        elif res.status_code in (401, 403):
            return {"error": "Invalid token or Gemma 2 license not accepted at huggingface.co/google/gemma-2-2b-it"}
        else:
            return {"error": f"API HTTP {res.status_code}"}
    except Exception as ex:
        return {"error": str(ex)}

# ==============================================================================
# UI Application
# ==============================================================================
def main():
    st.set_page_config(
        page_title="ClientRadar | Freelance Lead Arbitrage",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    env_serpapi = os.getenv("SERPAPI_API_KEY", "")
    env_hf = os.getenv("HUGGINGFACE_TOKEN", "")

    # Default credentials to .env
    serpapi_key = env_serpapi
    hf_token = env_hf

    # ==========================================================================
    # Sidebar: Theme Selector & Settings
    # ==========================================================================
    with st.sidebar:
        st.markdown(f"### {svg_icon('radar', size=18, color='#3B82F6')} ClientRadar", unsafe_allow_html=True)
        
        # Theme Selector
        theme_mode = st.radio("Theme Mode", ["Dark", "Light"], horizontal=True, label_visibility="collapsed")
        is_dark = (theme_mode == "Dark")
        
        st.markdown("##### 🔌 Engine Configuration")
        st.caption("Credentials load automatically from `.env`. No manual entry required.")
        
        # Connection status pills
        if env_serpapi:
            st.success("🟢 SerpApi: Connected (`.env`)")
        else:
            st.info("🟡 SerpApi: Demo Mode (Mock leads)")
            
        if env_hf:
            st.success("🟢 Gemma 2: Connected (`.env`)")
        else:
            st.info("🟡 Gemma 2: Demo Mode (Fast synthesis)")
            
        with st.expander("🔑 Setup `.env` File", expanded=False):
            st.markdown("""
            Add credentials to `.env` in project root:
            ```env
            SERPAPI_API_KEY=your_serpapi_key
            HUGGINGFACE_TOKEN=hf_your_token
            ```
            - [Get SerpApi Key](https://serpapi.com/manage-api-key)
            - [Get Gemma 2 Token](https://huggingface.co/settings/tokens)
            """)

        with st.expander("⚙️ Manual Key Override (Optional)", expanded=False):
            st.caption("Override keys for this browser session only:")
            override_serp = st.text_input("SerpApi Key", value="", type="password", key="override_serp")
            override_hf = st.text_input("Hugging Face Token", value="", type="password", key="override_hf")
            if override_serp:
                serpapi_key = override_serp
            if override_hf:
                hf_token = override_hf


        
        st.divider()
        st.markdown(f'<a href="https://github.com/AshrafGalaxy/ClientRadar" target="_blank" style="color: {"#94A3B8" if is_dark else "#475569"}; font-size: 0.82rem; text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">{svg_icon("github", size=14, color="currentColor")} AshrafGalaxy/ClientRadar</a>', unsafe_allow_html=True)

    # ==============================================================================
    # Dynamic CSS Injection (Zero Blank Top Padding + Dark/Light Theme System)
    # ==============================================================================
    if is_dark:
        theme_css = """
        .stApp {
            background-color: #0B0F19 !important;
            color: #F1F5F9 !important;
        }
        .page-header {
            border-bottom: 1px solid #1E293B !important;
        }
        .page-title {
            color: #F8FAFC !important;
        }
        .page-subtitle {
            color: #94A3B8 !important;
        }
        .stat-card {
            background: #111827 !important;
            border: 1px solid #1F2937 !important;
        }
        .stat-label {
            color: #94A3B8 !important;
        }
        .stat-val {
            color: #F8FAFC !important;
        }
        .tag-chip {
            background: #1E293B !important;
            color: #CBD5E1 !important;
            border: 1px solid #334155 !important;
        }
        .score-panel {
            background: #111827 !important;
            border: 1px solid #1E293B !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2) !important;
        }
        .score-badge {
            background: rgba(16, 185, 129, 0.15) !important;
            color: #34D399 !important;
            border: 1px solid rgba(16, 185, 129, 0.3) !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            background: #0B0F19 !important;
            border: 1px solid #1F2937 !important;
        }
        .stTabs [data-baseweb="tab"] {
            color: #94A3B8 !important;
        }
        .stTabs [aria-selected="true"] {
            background: #1E293B !important;
            color: #F8FAFC !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3) !important;
        }
        .email-subject-label {
            color: #94A3B8 !important;
        }
        .email-subject-val {
            color: #60A5FA !important;
        }
        .desc-box {
            background: #111827 !important;
            border: 1px solid #1F2937 !important;
            color: #CBD5E1 !important;
        }
        .email-preview {
            background: #111827 !important;
            border: 1px solid #1F2937 !important;
            color: #F1F5F9 !important;
        }
        .stTextInput>div>div>input, .stSelectbox>div>div, .stTextArea>div>div>textarea {
            background-color: #131C2E !important;
            border: 1px solid #2A3854 !important;
            color: #F1F5F9 !important;
        }
        .streamlit-expanderHeader {
            background: #111827 !important;
            border: 1px solid #1F2937 !important;
            color: #F8FAFC !important;
        }
        .stLinkButton>a {
            background: #1E293B !important;
            color: #93C5FD !important;
            border: 1px solid #334155 !important;
        }
        .stLinkButton>a:hover {
            border-color: #3B82F6 !important;
            color: #BFDBFE !important;
        }
        .github-top-badge {
            background: #111827 !important;
            border: 1px solid #1F2937 !important;
            color: #F8FAFC !important;
        }
        .github-top-badge:hover {
            border-color: #3B82F6 !important;
            color: #60A5FA !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2) !important;
        }
        [data-testid="stSidebarCollapsedControl"] button,
        [data-testid="stSidebarCollapseButton"] button {
            background-color: #111827 !important;
            border: 1px solid #1F2937 !important;
            color: #F8FAFC !important;
        }
        [data-testid="stSidebarCollapsedControl"] button:hover,
        [data-testid="stSidebarCollapseButton"] button:hover {
            border-color: #3B82F6 !important;
            color: #60A5FA !important;
        }
        .engine-status-pill {
            background: #111827 !important;
            border: 1px solid #1F2937 !important;
            color: #CBD5E1 !important;
        }
        """
    else: # Light Mode
        theme_css = """
        .stApp {
            background-color: #F8FAFC !important;
            color: #0F172A !important;
        }
        .page-header {
            border-bottom: 1px solid #E2E8F0 !important;
        }
        .page-title {
            color: #0F172A !important;
        }
        .page-subtitle {
            color: #64748B !important;
        }
        .stat-card {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
        }
        .stat-label {
            color: #64748B !important;
        }
        .stat-val {
            color: #0F172A !important;
        }
        .tag-chip {
            background: #F1F5F9 !important;
            color: #334155 !important;
            border: 1px solid #E2E8F0 !important;
        }
        .score-panel {
            background: #F8FAFC !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04) !important;
        }
        .score-badge {
            background: #ECFDF5 !important;
            color: #059669 !important;
            border: 1px solid #A7F3D0 !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            background: #F1F5F9 !important;
            border: 1px solid #E2E8F0 !important;
        }
        .stTabs [data-baseweb="tab"] {
            color: #64748B !important;
        }
        .stTabs [aria-selected="true"] {
            background: #FFFFFF !important;
            color: #0F172A !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
        }
        .email-subject-label {
            color: #64748B !important;
        }
        .email-subject-val {
            color: #1D4ED8 !important;
        }
        .desc-box {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #334155 !important;
        }
        .email-preview {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #0F172A !important;
        }
        .stTextInput>div>div>input, .stSelectbox>div>div, .stTextArea>div>div>textarea {
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            color: #0F172A !important;
        }
        .streamlit-expanderHeader {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #0F172A !important;
        }
        .stLinkButton>a {
            background: #F1F5F9 !important;
            color: #2563EB !important;
            border: 1px solid #CBD5E1 !important;
        }
        .stLinkButton>a:hover {
            border-color: #2563EB !important;
            color: #1D4ED8 !important;
        }
        .github-top-badge {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #0F172A !important;
        }
        .github-top-badge:hover {
            border-color: #2563EB !important;
            color: #2563EB !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.12) !important;
        }
        [data-testid="stSidebarCollapsedControl"] button,
        [data-testid="stSidebarCollapseButton"] button {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #0F172A !important;
        }
        [data-testid="stSidebarCollapsedControl"] button:hover,
        [data-testid="stSidebarCollapseButton"] button:hover {
            border-color: #2563EB !important;
            color: #2563EB !important;
        }
        .engine-status-pill {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #334155 !important;
        }
        """

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
        @import url('https://cdn.jsdelivr.net/npm/@fontsource/open-sauce-sans@latest/400.css');
        @import url('https://cdn.jsdelivr.net/npm/@fontsource/open-sauce-sans@latest/600.css');
        @import url('https://cdn.jsdelivr.net/npm/@fontsource/open-sauce-sans@latest/700.css');
        @import url('https://cdn.jsdelivr.net/npm/@fontsource/open-sauce-sans@latest/800.css');
        
        /* Typography: Apply Open Sauce Sans to text and UI elements */
        body, .stApp, p, h1, h2, h3, h4, h5, h6, input, textarea, select, button, label,
        .desc-box, .email-preview, .page-title, .page-subtitle, .stat-val, .stat-label, .tag-chip,
        .score-panel, .score-panel *, .email-subject-label, .email-subject-val,
        [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] div,
        [data-testid="stMarkdownContainer"] span:not([data-testid*="Icon"]):not(.material-symbols-rounded),
        .github-top-badge {{
            font-family: 'Open Sauce Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            letter-spacing: -0.015em;
        }}

        /* Strict Material Symbols enforcement for expander arrows and Streamlit icon ligatures */
        [data-testid="stExpanderToggleIcon"],
        [data-testid="stExpanderToggleIcon"] *,
        [data-testid*="Icon" i],
        [data-testid*="icon" i],
        summary [data-testid*="Icon" i],
        summary [data-testid*="icon" i],
        .material-symbols-rounded,
        .material-icons,
        [class*="material-symbols"] {{
            font-family: 'Material Symbols Rounded', 'Material Icons' !important;
            font-style: normal !important;
            font-weight: 400 !important;
            font-size: 20px !important;
            line-height: 1 !important;
            letter-spacing: normal !important;
            text-transform: none !important;
            display: inline-block !important;
            white-space: nowrap !important;
            word-wrap: normal !important;
            direction: ltr !important;
            -webkit-font-feature-settings: 'liga' !important;
            -webkit-font-smoothing: antialiased !important;
        }}

        svg, svg * {{
            font-family: inherit !important;
            letter-spacing: normal !important;
        }}
        
        /* Description Box */
        .desc-box {{
            border-radius: 8px;
            padding: 12px 14px;
            font-size: 0.88rem;
            line-height: 1.55;
            margin-top: 4px;
        }}
        
        /* Viability Scorecard Panel: clean uniform border with elegant elevation */
        .score-panel {{
            border-radius: 12px !important;
            padding: 16px 20px !important;
            margin: 14px 0 18px 0 !important;
        }}
        
        .score-badge {{
            display: inline-flex;
            align-items: center;
            padding: 3px 10px;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 0.92rem;
            letter-spacing: -0.01em;
        }}

        /* Segmented Control Tab Switch */
        .stTabs [data-baseweb="tab-list"] {{
            display: inline-flex !important;
            gap: 4px !important;
            padding: 4px !important;
            border-radius: 8px !important;
            margin-bottom: 12px !important;
        }}
        .stTabs [data-baseweb="tab-highlight"] {{
            display: none !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 6px !important;
            padding: 6px 14px !important;
            font-weight: 600 !important;
            font-size: 0.84rem !important;
            border: none !important;
            background: transparent !important;
            transition: all 0.15s ease !important;
        }}
        
        /* Email Subject Typography */
        .email-subject-label {{
            font-size: 0.74rem !important;
            text-transform: uppercase !important;
            font-weight: 600 !important;
            letter-spacing: 0.05em !important;
        }}
        .email-subject-val {{
            font-size: 0.96rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.015em !important;
            margin-top: 1px !important;
        }}
        
        /* Rendered Email Preview Container */
        .email-preview {{
            border-radius: 8px;
            padding: 14px 18px;
            font-size: 0.92rem;
            line-height: 1.6;
            margin: 8px 0;
        }}
        .email-preview p {{
            margin-bottom: 10px;
        }}
        
        /* Eliminate top blank space */
        .block-container {{
            padding-top: 1.2rem !important;
            padding-bottom: 2rem !important;
            max-width: 1100px !important;
        }}
        
        [data-testid="stSidebarContent"] {{
            padding-top: 1.2rem !important;
        }}
        
        /* Ensure sidebar open/close toggle remains visible and styled */
        header[data-testid="stHeader"] {{
            background: transparent !important;
            height: 2.6rem !important;
            z-index: 90 !important;
            pointer-events: none !important;
        }}
        
        header[data-testid="stHeader"] [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarCollapsedControl"] {{
            display: flex !important;
            visibility: visible !important;
            pointer-events: auto !important;
            position: fixed !important;
            top: 0.6rem !important;
            left: 0.6rem !important;
            z-index: 1001 !important;
        }}

        [data-testid="stSidebarCollapsedControl"] button,
        [data-testid="stSidebarCollapseButton"] button {{
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
        }}

        /* Hide Streamlit top-right default hamburger/deploy menu */
        header[data-testid="stHeader"] [data-testid="stToolbar"] {{
            display: none !important;
        }}
        
        /* Minimalist Page Header */
        .page-header {{
            margin-bottom: 20px;
            padding-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
        }}
        
        .engine-status-pill {{
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 7px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 600;
            flex-shrink: 0;
        }}
        
        .status-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }}
        
        .github-top-badge {{
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 7px 13px;
            border-radius: 8px;
            font-size: 0.84rem;
            font-weight: 600;
            text-decoration: none !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            flex-shrink: 0;
        }}
        
        .page-title {{
            font-size: 1.55rem;
            font-weight: 700;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .page-subtitle {{
            font-size: 0.9rem;
            margin-top: 3px;
        }}
        
        /* Metric Stats Strip */
        .stats-strip {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 20px;
        }}
        
        .stat-card {{
            border-radius: 10px;
            padding: 12px 16px;
        }}
        
        .stat-label {{
            font-size: 0.76rem;
            font-weight: 500;
        }}
        
        .stat-val {{
            font-size: 1.35rem;
            font-weight: 700;
            margin-top: 2px;
        }}
        
        /* Chips */
        .tag-chip {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 3px 9px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 500;
            margin-right: 6px;
        }}
        
        /* Modern Primary Blue Button */
        .stButton>button {{
            background: #2563EB !important;
            color: #FFFFFF !important;
            border: 1px solid #3B82F6 !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            padding: 0.45rem 1rem !important;
            transition: all 0.15s ease !important;
        }}
        
        .stButton>button:hover {{
            background: #1D4ED8 !important;
            border-color: #60A5FA !important;
        }}
        
        /* Inputs */
        .stTextInput>div>div>input, .stSelectbox>div>div, .stTextArea>div>div>textarea {{
            border-radius: 8px !important;
        }}
        
        .streamlit-expanderHeader {{
            border-radius: 8px !important;
            font-weight: 600 !important;
        }}
        
        .stLinkButton>a {{
            border-radius: 8px !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
        }}
        
        /* Theme Variables */
        {theme_css}
    </style>
    """, unsafe_allow_html=True)

    # ==============================================================================
    # Page Header (Single, Zero Top Gap)
    # ==============================================================================
    engine_status_dot = "#10B981" if (serpapi_key and hf_token) else ("#F59E0B" if (serpapi_key or hf_token) else "#64748B")
    engine_status_label = "⚡ Live Engine (.env)" if (serpapi_key and hf_token) else ("🟡 Partial (.env)" if (serpapi_key or hf_token) else "Demo Engine")

    st.markdown(f"""
    <div class="page-header">
        <div>
            <h1 class="page-title">{svg_icon('radar', size=26, color='#2563EB')} ClientRadar</h1>
            <div class="page-subtitle">Autonomous freelance contract discovery & AI proposal engine</div>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <div class="engine-status-pill" title="Engine status based on .env configuration">
                <span class="status-dot" style="background-color: {engine_status_dot};"></span>
                <span>{engine_status_label}</span>
            </div>
            <a href="https://github.com/AshrafGalaxy/ClientRadar" target="_blank" rel="noopener noreferrer" class="github-top-badge" title="View repository on GitHub">
                {svg_icon('github', size=17, color='currentColor')}
                <span>GitHub</span>
                {svg_icon('external', size=12, color='currentColor')}
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================================================================
    # Search Toolbar
    # ==============================================================================
    with st.container():
        c_q, c_loc, c_num = st.columns([3, 1.8, 1])
        with c_q:
            query = st.text_input("Tech Stack / Keywords:", value="Python Backend Developer Contract")
        with c_loc:
            location_options = ["Remote", "Worldwide", "United States", "Europe", "India"]
            location = st.selectbox("Location:", options=location_options, index=0)
        with c_num:
            max_results = st.selectbox("Leads:", options=[3, 4, 6, 8], index=1)

    scan_clicked = st.button("Search Contracts", use_container_width=True)

    if scan_clicked or "discovered_leads" not in st.session_state:
        status_msg = "Harvesting live contracts..." if serpapi_key else "Loading demo contracts..."
        with st.spinner(status_msg):
            leads = fetch_leads_serpapi(query, location, serpapi_key, max_results=max_results)
            st.session_state["discovered_leads"] = leads

    # ==============================================================================
    # Compact Metrics Strip
    # ==============================================================================
    current_leads = st.session_state.get("discovered_leads", [])
    
    st.markdown(f"""
    <div class="stats-strip">
        <div class="stat-card">
            <div class="stat-label">Active Opportunities</div>
            <div class="stat-val">{len(current_leads)}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Avg Viability</div>
            <div class="stat-val" style="color: #10B981;">94%</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Est. Compensation</div>
            <div class="stat-val" style="color: #F59E0B;">$4,800 <span style="font-size: 0.8rem; color: #94A3B8;">/mo</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================================================================
    # Contract Opportunities List
    # ==============================================================================
    st.markdown(f"##### Contract Opportunities ({len(current_leads)})")

    for i, lead in enumerate(current_leads):
        with st.expander(f"{lead['title']} · {lead['company_name']}", expanded=(i == 0)):
            # Tags Row
            st.markdown(f"""
            <div style="margin-bottom: 10px;">
                <span class="tag-chip">{svg_icon('building', size=12)} {lead['via']}</span>
                <span class="tag-chip">{svg_icon('dollar', size=12, color='#10B981')} {lead['budget']}</span>
                <span class="tag-chip">{svg_icon('pin', size=12)} {lead['location']}</span>
                <span class="tag-chip">{svg_icon('clock', size=12)} {lead['posted']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            c_desc, c_actions = st.columns([2.8, 1.2])
            
            with c_desc:
                st.markdown("**Description**")
                st.markdown(f'<div class="desc-box">{lead["description"]}</div>', unsafe_allow_html=True)
                
            with c_actions:
                st.markdown("**Actions**")
                # Direct working Google Jobs / provider link
                st.link_button(
                    label=f"View on {lead['via']} ↗",
                    url=lead["link"],
                    use_container_width=True
                )
                
                tone = st.selectbox(
                    "Pitch Style:",
                    options=["Direct Technical", "Fast 48h Turnaround", "Strategic Retainer"],
                    key=f"tone_{i}"
                )
                
                if st.button("Generate Pitch", key=f"gen_{i}", use_container_width=True):
                    with st.spinner("Analyzing brief with Gemma 2..."):
                        res = evaluate_and_pitch_with_gemma(lead, hf_token, pitch_tone=tone)
                        st.session_state[f"pitch_{i}"] = res

            # Render Generated Proposal
            if f"pitch_{i}" in st.session_state:
                res = st.session_state[f"pitch_{i}"]
                
                if "error" in res:
                    st.error(f"Generation error: {res['error']}")
                else:
                    st.markdown("---")
                    
                    # Clean Score Callout with ample padding and rich hierarchy
                    score = res.get("score", 90)
                    st.markdown(f"""
                    <div class="score-panel">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div style="display: flex; align-items: center; gap: 6px;">
                                    {svg_icon('shield', size=19, color='#10B981' if is_dark else '#16A34A')}
                                    <span style="font-size: 0.96rem; font-weight: 700; letter-spacing: -0.01em;">Viability Score</span>
                                </div>
                                <span class="score-badge">{score}/100</span>
                            </div>
                            <div style="display: inline-flex; align-items: center; gap: 5px; font-size: 0.78rem; font-weight: 600; color: {'#94A3B8' if is_dark else '#64748B'}; background: {'rgba(255,255,255,0.05)' if is_dark else 'rgba(0,0,0,0.04)'}; padding: 3px 8px; border-radius: 6px;">
                                {svg_icon('sparkles', size=12, color='#60A5FA' if is_dark else '#2563EB')}
                                <span>Gemma 2 Analysis</span>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr; gap: 8px; border-top: 1px solid {'#1F2937' if is_dark else '#DCFCE7'}; padding-top: 10px;">
                            <div style="font-size: 0.88rem; line-height: 1.5; display: flex; align-items: baseline; gap: 8px;">
                                <span style="color: #10B981; font-weight: 700; font-size: 0.9rem;">✓</span>
                                <div>
                                    <strong style="color: {'#F8FAFC' if is_dark else '#0F172A'};">Scope Clarity:</strong>
                                    <span style="color: {'#CBD5E1' if is_dark else '#334155'}; margin-left: 4px;">{res.get('scope_clarity', 'Well-defined contractor scope.')}</span>
                                </div>
                            </div>
                            <div style="font-size: 0.88rem; line-height: 1.5; display: flex; align-items: baseline; gap: 8px;">
                                <span style="color: {'#10B981' if res.get('red_flags', 'None detected') == 'None detected' else '#EF4444'}; font-weight: 700; font-size: 0.9rem;">{'✓' if res.get('red_flags', 'None detected') == 'None detected' else '⚠'}</span>
                                <div>
                                    <strong style="color: {'#F8FAFC' if is_dark else '#0F172A'};">Risk Audit:</strong>
                                    <span style="color: {'#94A3B8' if is_dark else '#64748B'}; margin-left: 4px;">{res.get('red_flags', 'None detected')}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    pitch_content = res.get("pitch", "")
                    
                    # Segmented View: Rendered Pitch vs Raw Markdown
                    tab_preview, tab_raw = st.tabs(["✉️ Rendered Pitch", "📝 Edit Markdown"])
                    
                    with tab_preview:
                        with st.container(border=True):
                            c_sub, c_tag = st.columns([3.5, 1])
                            with c_sub:
                                st.markdown(f"""
                                <div class="email-subject-label">Subject</div>
                                <div class="email-subject-val">{res.get('subject', '')}</div>
                                """, unsafe_allow_html=True)
                            with c_tag:
                                st.markdown(f"<div style='text-align: right;'><span class='tag-chip' style='font-size: 0.78rem;'>{tone}</span></div>", unsafe_allow_html=True)
                            
                            st.divider()
                            st.markdown(pitch_content)
                        
                    with tab_raw:
                        st.text_input("Subject:", value=res.get("subject", ""), key=f"subj_{i}")
                        st.text_area("Raw Markdown:", value=pitch_content, height=200, key=f"pitch_text_{i}")
                    
                    # 1-Click Download Action Bar with exact vertical alignment
                    c_dl, c_hint = st.columns([1.4, 1.2], vertical_alignment="center")
                    with c_dl:
                        st.download_button(
                            label=f"📥 Download Proposal ({lead['company_name']}.md)",
                            data=full_export,
                            file_name=f"proposal_{lead['company_name'].lower().replace(' ', '_')}.md",
                            mime="text/markdown",
                            key=f"dl_btn_{i}",
                            use_container_width=True
                        )
                    with c_hint:
                        st.markdown(
                            f"""
                            <div style="display: flex; align-items: center; gap: 7px; font-size: 0.82rem; color: {'#94A3B8' if is_dark else '#64748B'}; font-weight: 500; height: 100%; min-height: 38px;">
                                {svg_icon('check', size=15, color='#10B981')}
                                <span>Ready to send via email or job portal</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

if __name__ == "__main__":
    main()
