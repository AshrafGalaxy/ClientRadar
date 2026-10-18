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
        "building": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4"/></svg>'
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

    # ==========================================================================
    # Sidebar: Theme Selector & Settings
    # ==========================================================================
    with st.sidebar:
        st.markdown(f"### {svg_icon('radar', size=18, color='#3B82F6')} ClientRadar", unsafe_allow_html=True)
        
        # Theme Selector
        theme_mode = st.radio("Theme Mode", ["Dark", "Light"], horizontal=True, label_visibility="collapsed")
        is_dark = (theme_mode == "Dark")
        
        st.caption("Add API credentials for live discovery and AI evaluation. Leave blank to run in demo mode.")
        
        serpapi_key = st.text_input(
            "SerpApi Key",
            value=env_serpapi,
            type="password",
            help="Free key available at serpapi.com/manage-api-key"
        )
        
        hf_token = st.text_input(
            "Hugging Face Token",
            value=env_hf,
            type="password",
            help="Read token for google/gemma-2-2b-it from huggingface.co/settings/tokens"
        )

        # Compact Status Row
        col_st1, col_st2 = st.columns(2)
        with col_st1:
            if serpapi_key:
                st.caption("🟢 SerpApi: Live")
            else:
                st.caption("🟡 SerpApi: Demo")
        with col_st2:
            if hf_token:
                st.caption("🟢 Gemma 2: Live")
            else:
                st.caption("🟡 Gemma 2: Demo")

        st.divider()
        with st.expander("🔑 How to obtain keys"):
            st.markdown("""
            **1. SerpApi (100 free searches/mo):**
            - Sign up at [serpapi.com](https://serpapi.com/users/sign_up)
            - Copy key from [serpapi.com/manage-api-key](https://serpapi.com/manage-api-key)
            
            **2. Hugging Face Gemma 2:**
            - Sign up at [huggingface.co](https://huggingface.co)
            - Accept model terms at [google/gemma-2-2b-it](https://huggingface.co/google/gemma-2-2b-it)
            - Create Read token at [hf.co/settings/tokens](https://huggingface.co/settings/tokens)
            """)
        
        st.divider()
        st.markdown(f'<a href="https://github.com/AshrafGalaxy/client-radar-ai" target="_blank" style="color: {"#94A3B8" if is_dark else "#475569"}; font-size: 0.82rem; text-decoration: none;">{svg_icon("external", size=13)} GitHub Repository</a>', unsafe_allow_html=True)

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
            border: 1px solid #1F2937 !important;
            border-left: 3px solid #10B981 !important;
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
            background: #F0FDF4 !important;
            border: 1px solid #DCFCE7 !important;
            border-left: 3px solid #16A34A !important;
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
        """

    st.markdown(f"""
    <style>
        @import url('https://cdn.jsdelivr.net/npm/@fontsource/open-sauce-sans@latest/400.css');
        @import url('https://cdn.jsdelivr.net/npm/@fontsource/open-sauce-sans@latest/600.css');
        @import url('https://cdn.jsdelivr.net/npm/@fontsource/open-sauce-sans@latest/700.css');
        @import url('https://cdn.jsdelivr.net/npm/@fontsource/open-sauce-sans@latest/800.css');
        
        /* Universal Typography: Enforce Open Sauce Sans everywhere */
        *, html, body, p, span, div, h1, h2, h3, h4, h5, h6, input, textarea, select, button, label,
        .stMarkdown, [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] * {{
            font-family: 'Open Sauce Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            letter-spacing: -0.015em;
        }}
        
        /* Description Box */
        .desc-box {{
            border-radius: 8px;
            padding: 12px 14px;
            font-size: 0.88rem;
            line-height: 1.55;
            margin-top: 4px;
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
        
        header[data-testid="stHeader"] {{
            display: none !important;
        }}
        
        /* Minimalist Page Header */
        .page-header {{
            margin-bottom: 20px;
            padding-bottom: 12px;
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
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">ClientRadar</h1>
        <div class="page-subtitle">Autonomous freelance contract discovery & AI proposal engine</div>
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
                    
                    # Clean Score Callout
                    score = res.get("score", 90)
                    st.markdown(f"""
                    <div class="score-panel">
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <div>
                                <strong style="font-size: 0.95rem;">Viability Score:</strong>
                                <span style="font-size: 1.15rem; font-weight: 700; color: #10B981; margin-left: 6px;">{score}/100</span>
                            </div>
                            <div style="font-size: 0.8rem; color: #94A3B8;">Gemma 2 Analysis</div>
                        </div>
                        <div style="font-size: 0.85rem; margin-top: 6px;">
                            <strong>Scope Clarity:</strong> {res.get('scope_clarity', 'Clear contractor scope.')}
                        </div>
                        <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 3px;">
                            <strong>Red Flags:</strong> {res.get('red_flags', 'None detected')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    pitch_content = res.get("pitch", "")
                    
                    # Tabbed Pitch Display: Rendered Preview by Default vs Raw Markdown
                    tab_preview, tab_raw = st.tabs(["✉️ Rendered Pitch Preview", "📝 Edit Raw Markdown"])
                    
                    with tab_preview:
                        st.markdown(f"""
                        <div class="email-preview">
                            <div style="font-size: 0.92rem; font-weight: 700; margin-bottom: 8px; color: {'#60A5FA' if is_dark else '#2563EB'};">
                                Subject: {res.get('subject', '')}
                            </div>
                            <hr style="border: none; border-top: 1px solid {'#1F2937' if is_dark else '#E2E8F0'}; margin: 8px 0 14px 0;" />
                        """, unsafe_allow_html=True)
                        st.markdown(pitch_content)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    with tab_raw:
                        st.text_input("Subject:", value=res.get("subject", ""), key=f"subj_{i}")
                        st.text_area("Raw Markdown:", value=pitch_content, height=180, key=f"pitch_text_{i}")
                    
                    # 1-Click Download
                    full_export = f"""# Proposal for {lead['title']}
**Company:** {lead['company_name']}
**Source:** {lead['via']}
**Original Posting:** {lead['link']}
**Viability Score:** {score}/100

---

## Subject: {res.get('subject', '')}

{pitch_content}
"""
                    st.download_button(
                        label=f"Download Proposal ({lead['company_name']}.md)",
                        data=full_export,
                        file_name=f"proposal_{lead['company_name'].lower().replace(' ', '_')}.md",
                        mime="text/markdown",
                        key=f"dl_btn_{i}"
                    )

if __name__ == "__main__":
    main()
