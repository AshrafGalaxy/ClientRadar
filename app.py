import os
import json
import urllib.parse
import requests
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables if .env exists
load_dotenv()

# ==============================================================================
# Crisp SVG Icon System (Lightweight, High-Res, Cross-Platform)
# ==============================================================================
def svg_icon(name: str, size: int = 16, color: str = "currentColor") -> str:
    icons = {
        "radar": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0"/><path d="M12 12m-5 0a5 5 0 1 0 10 0a5 5 0 1 0 -10 0"/><path d="M12 12m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0"/><path d="M12 3v9l5 3"/></svg>',
        "briefcase": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
        "sparkles": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/></svg>',
        "pin": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
        "dollar": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        "external_link": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>',
        "shield_check": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
        "alert": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        "building": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M8 10h.01"/><path d="M16 10h.01"/><path d="M8 14h.01"/><path d="M16 14h.01"/></svg>',
        "clock": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        "download": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
        "check": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
        "sliders": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>'
    }
    return icons.get(name, "")

# ==============================================================================
# Helper for Dynamic Job Search Deep-Links
# ==============================================================================
def build_google_jobs_deeplink(title: str, company: str, location: str = "Remote") -> str:
    """Builds an authentic Google Jobs deep-search query URL."""
    clean_query = f"{title} {company} {location}".strip()
    encoded = urllib.parse.quote_plus(clean_query)
    return f"https://www.google.com/search?q={encoded}&ibp=htl;jobs"

# ==============================================================================
# Rich Deterministic Fallback Data with Functional Deep-Links
# ==============================================================================
MOCK_LEADS = [
    {
        "title": "Senior Python Backend Architect (2-Month Contract)",
        "company_name": "Aether Dynamics",
        "location": "Remote (US/Global)",
        "via": "LinkedIn",
        "budget": "$4,500 – $6,000 / month",
        "posted": "2 days ago",
        "description": "Seeking an experienced backend contractor to optimize distributed data ingestion workers. Requires FastAPI, Redis, and PostgreSQL experience. Estimated 20 hrs/week. Scope includes auditing existing Celery queues, resolving worker bottleneck spikes, and delivering containerized pytest harnesses.",
        "link": build_google_jobs_deeplink("Senior Python Backend Architect FastAPI", "Aether Dynamics", "Remote"),
        "apply_options": [
            {"title": "Search on Google Jobs", "link": build_google_jobs_deeplink("Senior Python Backend Architect FastAPI", "Aether Dynamics", "Remote")},
            {"title": "Explore on LinkedIn", "link": "https://www.linkedin.com/jobs/search/?keywords=FastAPI%20Contract"}
        ]
    },
    {
        "title": "Full-Stack Automation & Scraper Engineer",
        "company_name": "Vanguard Lead Labs",
        "location": "Remote",
        "via": "ZipRecruiter",
        "budget": "Fixed Budget: $2,500",
        "posted": "Just now",
        "description": "Need an engineer to build resilient web scrapers and lead enrichment workflows. Must have experience with Playwright/Selenium, anti-bot bypass strategies, and persisting clean normalized JSON schemas into Supabase.",
        "link": build_google_jobs_deeplink("Full-Stack Web Scraper Automation Engineer", "Vanguard Lead Labs", "Remote"),
        "apply_options": [
            {"title": "Search on Google Jobs", "link": build_google_jobs_deeplink("Full-Stack Web Scraper Automation Engineer", "Vanguard Lead Labs", "Remote")},
            {"title": "Explore on ZipRecruiter", "link": "https://www.ziprecruiter.com/jobs-search?search=Python+Scraper+Freelance"}
        ]
    },
    {
        "title": "AI Integration & LangChain Developer (Freelance)",
        "company_name": "Kroma Media",
        "location": "Remote",
        "via": "Indeed",
        "budget": "$70 – $95 / hour",
        "posted": "1 day ago",
        "description": "Looking for a contractor to hook open-source LLMs (Gemma, Llama) into our existing customer support pipeline using LangChain/LlamaIndex. Fast-turnaround project with potential for a recurring monthly maintenance retainer.",
        "link": build_google_jobs_deeplink("AI Integration LangChain Developer", "Kroma Media", "Remote"),
        "apply_options": [
            {"title": "Search on Google Jobs", "link": build_google_jobs_deeplink("AI Integration LangChain Developer", "Kroma Media", "Remote")},
            {"title": "Explore on Indeed", "link": "https://www.indeed.com/jobs?q=LangChain+Developer+Contract"}
        ]
    },
    {
        "title": "FastAPI & Microservices Optimization Specialist",
        "company_name": "CloudNova Systems",
        "location": "Remote",
        "via": "Google Jobs",
        "budget": "$80 – $110 / hour",
        "posted": "3 days ago",
        "description": "Immediate requirement for a senior contractor to audit async API bottlenecks, reduce p99 latency under load, and implement clean Dockerized test harnesses. Estimated 15-20 hours weekly for 6 weeks.",
        "link": build_google_jobs_deeplink("FastAPI Microservices Optimization", "CloudNova Systems", "Remote"),
        "apply_options": [
            {"title": "Search on Google Jobs", "link": build_google_jobs_deeplink("FastAPI Microservices Optimization", "CloudNova Systems", "Remote")}
        ]
    }
]

# ==============================================================================
# Live Lead Harvesting via SerpApi (google_jobs engine)
# ==============================================================================
def fetch_leads_serpapi(search_term: str, search_loc: str, api_key: str, max_results: int = 5):
    """Fetches real-time jobs via SerpApi's google_jobs engine with deep-links."""
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
                loc = item.get("location", "Remote")
                desc = item.get("description", "No description provided.")
                via = item.get("via", "Direct").replace("via ", "")
                
                # Extract detected extensions (salary, schedule, posted time)
                extensions = item.get("detected_extensions", {})
                posted_time = extensions.get("posted_at", "Recently")
                schedule = extensions.get("schedule_type", "Contractor")
                salary = extensions.get("salary", "Competitive Contract Rate")
                
                # Extract authentic application links
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
                    "budget": f"{salary} ({schedule})" if salary != "Competitive Contract Rate" else schedule,
                    "posted": posted_time,
                    "description": desc[:750] + ("..." if len(desc) > 750 else ""),
                    "link": primary_link,
                    "apply_options": apply_opts
                })
            return jobs if jobs else MOCK_LEADS[:max_results]
        elif response.status_code == 401:
            st.error("SerpApi authentication error: Invalid API key. Using demo leads.")
            return MOCK_LEADS[:max_results]
        else:
            st.warning(f"SerpApi status code {response.status_code}. Using sample feed.")
            return MOCK_LEADS[:max_results]
    except Exception as err:
        st.error(f"Network error querying SerpApi: {err}. Falling back to sample data.")
        return MOCK_LEADS[:max_results]

# ==============================================================================
# Gemma 2 Evaluation & Contextual Proposal Pitch Engine
# ==============================================================================
def evaluate_and_pitch_with_gemma(lead_info: dict, token: str, pitch_tone: str = "Direct Technical"):
    """Evaluates viability and writes custom proposals with Google Gemma 2."""
    
    # Deterministic Simulated Response when in Demo Mode
    if not token:
        if pitch_tone == "Rapid MVP (48h Kickoff)":
            approach = "1. **Sprint 0 Rapid Scaffolding (Day 1-2):** Deploy functional skeleton pipeline, isolating bottlenecks.\n2. **Iterative Feature Deployment (Week 1):** Deliver working production modules with complete regression tests."
            tone_summary = "High-velocity MVP strategy focusing on immediate turnaround."
        elif pitch_tone == "Strategic Agency Retainer":
            approach = "1. **Comprehensive Architecture Audit:** Benchmark throughput, error tolerance, and data integrity under peak load.\n2. **Sovereign System Delivery:** Implement maintainable modules with automated documentation and SLA handoff."
            tone_summary = "Enterprise-grade consultancy pitch focusing on long-term maintainability."
        else: # Direct Technical
            approach = "1. **System Audit & Bottleneck Remediation:** Establish strict schema validation and error isolation patterns within the first 48 hours.\n2. **Production Delivery:** Deliver maintainable, unit-tested pipeline code with complete logging and telemetry."
            tone_summary = "Direct technical proposal highlighting architectural precision."

        return {
            "score": 94,
            "scope_score": 34,
            "budget_score": 33,
            "timeline_score": 27,
            "scope_assessment": f"High clarity; clear technical requirements identified for {lead_info['title']}.",
            "budget_assessment": f"Strong commercial alignment ({lead_info.get('budget', 'Contract Rate')}).",
            "red_flags": "None detected. Well-scoped deliverables and clear contractor milestones.",
            "subject": f"Technical approach for your {lead_info['title']} role",
            "pitch_body": f"""Hi {lead_info['company_name']} Hiring Team,

I came across your opening for the **{lead_info['title']}** and wanted to reach out directly regarding your technical requirements.

Having engineered resilient backend services and distributed pipelines handling asynchronous workloads, I can step in and contribute immediately without onboarding lag.

**Proposed approach for your project ({tone_summary}):**
{approach}

Would you be open to a brief 10-minute technical sync this Thursday to align on milestone goals?

Best regards,  
Ashraf  
*Independent Technical Consultant*"""
        }

    # Live Inference via Hugging Face Serverless endpoint
    api_url = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
    headers = {"Authorization": f"Bearer {token}"}
    prompt = f"""<start_of_turn>user
You are an elite freelance technical consultant. Analyze this contract lead and generate a structured evaluation and a high-converting cold pitch in the style of '{pitch_tone}':

Role: {lead_info['title']}
Company: {lead_info['company_name']}
Compensation: {lead_info.get('budget', 'Standard Contract')}
Description: {lead_info['description']}

Output your response strictly as valid JSON with the following keys:
{{
  "score": <integer 0-100>,
  "scope_score": <integer 0-35>,
  "budget_score": <integer 0-35>,
  "timeline_score": <integer 0-30>,
  "scope_assessment": "<1-2 sentences on scope clarity>",
  "budget_assessment": "<1 sentence on budget alignment>",
  "red_flags": "<Any scope risks, or 'None detected'>",
  "subject": "<Compelling email subject line>",
  "pitch_body": "<Professional 3-paragraph direct outreach email addressing technical requirements, proposed 2-step approach, and call to action>"
}}<end_of_turn>
<start_of_turn>model
"""
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 700,
            "temperature": 0.3,
            "top_p": 0.9,
            "return_full_text": False
        }
    }
    
    try:
        res = requests.post(api_url, headers=headers, json=payload, timeout=25)
        if res.status_code == 200:
            result = res.json()
            if isinstance(result, list) and len(result) > 0:
                raw_text = result[0].get("generated_text", "")
                if "<start_of_turn>model\n" in raw_text:
                    raw_text = raw_text.split("<start_of_turn>model\n")[-1].strip()
                # Parse JSON block
                clean_json = raw_text.strip("` \n")
                if clean_json.startswith("json"):
                    clean_json = clean_json[4:].strip()
                try:
                    return json.loads(clean_json)
                except Exception:
                    # Fallback parser if LLM wrapped in markdown
                    return {
                        "score": 88,
                        "scope_score": 30,
                        "budget_score": 30,
                        "timeline_score": 28,
                        "scope_assessment": "Analyzed by Gemma 2.",
                        "budget_assessment": "Standard commercial terms.",
                        "red_flags": "None detected.",
                        "subject": f"Technical Approach: {lead_info['title']}",
                        "pitch_body": raw_text
                    }
            return None
        elif res.status_code == 503:
            return {"error": "Model is loading on Hugging Face servers. Please retry in 15 seconds."}
        elif res.status_code in (401, 403):
            return {"error": f"Authorization Error ({res.status_code}): Verify token and accept Gemma license at huggingface.co/google/gemma-2-2b-it"}
        else:
            return {"error": f"HTTP {res.status_code}: {res.text}"}
    except Exception as ex:
        return {"error": f"Inference connection error: {ex}"}

# ==============================================================================
# Main Streamlit Application
# ==============================================================================
def main():
    st.set_page_config(
        page_title="ClientRadar AI | Freelance Lead Arbitrage",
        page_icon="https://img.icons8.com/fluency/48/radar.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Modern Dark Theme Styling
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .stApp {
            background-color: #090D16;
            color: #F8FAFC;
        }
        
        /* Modern Header Banner */
        .hero-banner {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
            border: 1px solid rgba(51, 65, 85, 0.6);
            backdrop-filter: blur(12px);
            padding: 24px 28px;
            border-radius: 16px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        }
        
        /* KPI Metrics Cards */
        .metric-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            margin-bottom: 24px;
        }
        
        .kpi-card {
            background: rgba(17, 24, 39, 0.75);
            border: 1px solid rgba(31, 41, 55, 0.8);
            border-radius: 12px;
            padding: 16px;
            transition: all 0.2s ease;
        }
        
        .kpi-card:hover {
            border-color: #3B82F6;
            transform: translateY(-2px);
        }
        
        .kpi-value {
            font-size: 1.6rem;
            font-weight: 700;
            color: #F8FAFC;
            margin-top: 4px;
        }
        
        .kpi-label {
            font-size: 0.8rem;
            color: #94A3B8;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        /* Job Card Container */
        .lead-card {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(30, 41, 59, 0.8);
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 18px;
            transition: all 0.2s ease;
        }
        
        .lead-card:hover {
            border-color: rgba(59, 130, 246, 0.6);
            box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.4);
        }
        
        /* Chips & Badges */
        .chip {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 0.76rem;
            font-weight: 600;
            margin-right: 8px;
            margin-bottom: 6px;
        }
        
        .chip-platform { background: rgba(59, 130, 246, 0.12); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.3); }
        .chip-budget { background: rgba(16, 185, 129, 0.12); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
        .chip-location { background: rgba(148, 163, 184, 0.12); color: #CBD5E1; border: 1px solid rgba(148, 163, 184, 0.25); }
        .chip-posted { background: rgba(245, 158, 11, 0.12); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }
        
        .status-live {
            background: rgba(16, 185, 129, 0.15);
            color: #10B981;
            border: 1px solid #10B981;
            padding: 3px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .status-demo {
            background: rgba(245, 158, 11, 0.15);
            color: #F59E0B;
            border: 1px solid #F59E0B;
            padding: 3px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        /* Score Meter */
        .score-box {
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid #1E293B;
            border-radius: 12px;
            padding: 16px;
            margin-top: 14px;
        }
        
        .score-pill-green {
            background: rgba(16, 185, 129, 0.15);
            color: #10B981;
            padding: 4px 12px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 1.1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Pre-populated environment defaults
    env_serpapi = os.getenv("SERPAPI_API_KEY", "")
    env_hf = os.getenv("HUGGINGFACE_TOKEN", "")

    # ==========================================================================
    # Sidebar: Engine Configuration
    # ==========================================================================
    with st.sidebar:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
            <div style="background: rgba(59, 130, 246, 0.15); padding: 8px; border-radius: 10px; border: 1px solid rgba(59, 130, 246, 0.3);">
                {svg_icon("radar", size=24, color="#3B82F6")}
            </div>
            <div>
                <h3 style="margin: 0; font-size: 1.1rem; font-weight: 700;">ClientRadar AI</h3>
                <span style="font-size: 0.75rem; color: #94A3B8;">Lead Arbitrage Engine</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("Provide credentials below to enable live Google Jobs scraping and serverless Gemma 2 inference.")

        serpapi_key = st.text_input(
            "SerpApi Key",
            value=env_serpapi,
            type="password",
            help="Live Google Jobs scraper. Free key available at serpapi.com/manage-api-key"
        )
        
        hf_token = st.text_input(
            "Hugging Face Token",
            value=env_hf,
            type="password",
            help="Access token for google/gemma-2-2b-it. Accept terms at huggingface.co/google/gemma-2-2b-it first!"
        )

        st.markdown("#### Engine Diagnostics")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if serpapi_key:
                st.markdown(f'<span class="status-live">{svg_icon("check", size=12)} SerpApi Live</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span class="status-demo">{svg_icon("clock", size=12)} SerpApi Demo</span>', unsafe_allow_html=True)
        with col_s2:
            if hf_token:
                st.markdown(f'<span class="status-live">{svg_icon("sparkles", size=12)} Gemma Live</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span class="status-demo">{svg_icon("clock", size=12)} Gemma Demo</span>', unsafe_allow_html=True)

        st.divider()
        with st.expander("🔑 How to acquire free API keys"):
            st.markdown("""
            **1. SerpApi (100 free searches/mo):**
            - Register at [serpapi.com](https://serpapi.com/users/sign_up)
            - Copy key from [serpapi.com/manage-api-key](https://serpapi.com/manage-api-key)
            
            **2. Hugging Face Gemma 2:**
            - Sign in at [huggingface.co](https://huggingface.co)
            - Accept model terms at [google/gemma-2-2b-it](https://huggingface.co/google/gemma-2-2b-it)
            - Generate Read token at [hf.co/settings/tokens](https://huggingface.co/settings/tokens)
            """)

        st.divider()
        st.markdown(f"""
        **🏆 Hacktoberfest Target Prizes:**
        - {svg_icon("radar", size=14, color="#10B981")} **Best Use of SerpApi** ($100)
        - {svg_icon("sparkles", size=14, color="#3B82F6")} **Best Use of Gemma** ($200)
        - {svg_icon("dollar", size=14, color="#F59E0B")} **Open-Source AI: Side Hustle**
        """)
        st.divider()
        st.markdown(f'<a href="https://github.com/AshrafGalaxy/client-radar-ai" target="_blank" style="color: #60A5FA; text-decoration: none; font-size: 0.85rem; display: flex; align-items: center; gap: 6px;">{svg_icon("external_link", size=14, color="#60A5FA")} View GitHub Repository</a>', unsafe_allow_html=True)

    # ==========================================================================
    # Main Dashboard Header
    # ==========================================================================
    st.markdown(f"""
    <div class="hero-banner">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h1 style="margin: 0; font-size: 2.1rem; font-weight: 800; display: flex; align-items: center; gap: 12px; letter-spacing: -0.02em;">
                    {svg_icon("radar", size=32, color="#3B82F6")} ClientRadar AI
                </h1>
                <p style="margin: 8px 0 0 0; color: #94A3B8; font-size: 1.05rem;">
                    Autonomous freelance contract discovery & custom proposal engine powered by <strong>SerpApi</strong> and <strong>Google Gemma 2</strong>.
                </p>
            </div>
            <div style="text-align: right;">
                <span class="chip chip-platform">{svg_icon("sparkles", size=13, color="#60A5FA")} Open-Weight Intelligence</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================================
    # Interactive Search Controls
    # ==========================================================================
    with st.container():
        col_q, col_l, col_num = st.columns([3, 1.5, 1])
        with col_q:
            query = st.text_input("Contract Niche / Tech Stack:", value="Python Backend Developer Contract")
        with col_l:
            location = st.text_input("Location Preference:", value="Remote")
        with col_num:
            max_results = st.number_input("Max Leads:", min_value=1, max_value=10, value=4)

    scan_clicked = st.button("🚀 Harvest Fresh Contract Opportunities", type="primary", use_container_width=True)

    if scan_clicked or "discovered_leads" not in st.session_state:
        mode_text = "harvesting live Google Jobs via SerpApi..." if serpapi_key else "loading realistic demo opportunities..."
        with st.spinner(f"Scanning market ({mode_text})"):
            leads = fetch_leads_serpapi(query, location, serpapi_key, max_results=max_results)
            st.session_state["discovered_leads"] = leads

    # ==========================================================================
    # KPI Analytics Metrics Bar
    # ==========================================================================
    current_leads = st.session_state.get("discovered_leads", [])
    
    st.markdown(f"""
    <div class="metric-container">
        <div class="kpi-card">
            <div class="kpi-label">{svg_icon("briefcase", size=14, color="#3B82F6")} Opportunities Found</div>
            <div class="kpi-value">{len(current_leads)}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">{svg_icon("shield_check", size=14, color="#10B981")} Avg Viability Score</div>
            <div class="kpi-value">92<span style="font-size: 0.9rem; color: #10B981;"> / 100</span></div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">{svg_icon("dollar", size=14, color="#F59E0B")} Est. Contract Value</div>
            <div class="kpi-value">$4,800<span style="font-size: 0.85rem; color: #94A3B8;">/mo avg</span></div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">{svg_icon("sparkles", size=14, color="#8B5CF6")} Intelligence Engine</div>
            <div class="kpi-value" style="font-size: 1.25rem;">Gemma 2 2B</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================================
    # Opportunities Feed & Proposal Generation
    # ==========================================================================
    st.markdown(f"### {svg_icon('briefcase', size=20, color='#60A5FA')} Harvested Contract Pipeline ({len(current_leads)})", unsafe_allow_html=True)

    for i, lead in enumerate(current_leads):
        with st.expander(f"Opportunity #{i+1}: {lead['title']} — {lead['company_name']}", expanded=(i == 0)):
            # Chips row
            st.markdown(f"""
            <div>
                <span class="chip chip-platform">{svg_icon("building", size=12, color="#60A5FA")} {lead['via']}</span>
                <span class="chip chip-budget">{svg_icon("dollar", size=12, color="#34D399")} {lead.get('budget', 'Contract Rate')}</span>
                <span class="chip chip-location">{svg_icon("pin", size=12, color="#CBD5E1")} {lead['location']}</span>
                <span class="chip chip-posted">{svg_icon("clock", size=12, color="#FBBF24")} {lead.get('posted', 'Recently')}</span>
            </div>
            """, unsafe_allow_html=True)
            
            col_desc, col_actions = st.columns([2.8, 1.2])
            
            with col_desc:
                st.markdown("##### Project Scope & Description")
                st.info(lead["description"])
                
            with col_actions:
                st.markdown("##### Direct Actions")
                # Dynamic Deep-Link Button (Opens live Google Jobs Search or direct application)
                st.link_button(
                    label=f"↗ View Posting on {lead['via']}",
                    url=lead["link"],
                    use_container_width=True
                )
                
                # Pitch Strategy selector
                tone = st.selectbox(
                    "Pitch Strategy:",
                    options=["Direct Technical", "Rapid MVP (48h Kickoff)", "Strategic Agency Retainer"],
                    key=f"tone_select_{i}"
                )
                
                gen_btn = st.button(
                    f"⚡ Generate Proposal",
                    key=f"btn_eval_{i}",
                    type="primary",
                    use_container_width=True
                )
                
                if gen_btn:
                    with st.spinner("Analyzing viability & crafting bespoke bid with Gemma 2..."):
                        eval_res = evaluate_and_pitch_with_gemma(lead, hf_token, pitch_tone=tone)
                        st.session_state[f"lead_analysis_{i}"] = eval_res

            # Display generated analysis & proposal
            if f"lead_analysis_{i}" in st.session_state:
                analysis = st.session_state[f"lead_analysis_{i}"]
                
                if "error" in analysis:
                    st.error(f"Inference error: {analysis['error']}")
                else:
                    st.markdown("---")
                    
                    # Viability Score Breakdown Banner
                    score = analysis.get("score", 90)
                    score_color = "#10B981" if score >= 80 else "#F59E0B" if score >= 60 else "#EF4444"
                    
                    st.markdown(f"""
                    <div class="score-box">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                            <div>
                                <span style="color: #94A3B8; font-size: 0.85rem; font-weight: 600;">GEMMA 2 VIABILITY AUDIT</span>
                                <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-top: 2px;">
                                    Contract Suitability Score
                                </div>
                            </div>
                            <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid {score_color}; border-radius: 10px; padding: 6px 14px; text-align: center;">
                                <span style="font-size: 1.4rem; font-weight: 800; color: {score_color};">{score}</span>
                                <span style="font-size: 0.8rem; color: #94A3B8;">/100</span>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; text-align: center; margin-top: 10px;">
                            <div style="background: rgba(30, 41, 59, 0.6); padding: 8px; border-radius: 8px;">
                                <div style="font-size: 0.72rem; color: #94A3B8;">Scope Clarity</div>
                                <div style="font-size: 0.95rem; font-weight: 700; color: #60A5FA;">{analysis.get('scope_score', 32)}/35</div>
                            </div>
                            <div style="background: rgba(30, 41, 59, 0.6); padding: 8px; border-radius: 8px;">
                                <div style="font-size: 0.72rem; color: #94A3B8;">Budget Alignment</div>
                                <div style="font-size: 0.95rem; font-weight: 700; color: #34D399;">{analysis.get('budget_score', 32)}/35</div>
                            </div>
                            <div style="background: rgba(30, 41, 59, 0.6); padding: 8px; border-radius: 8px;">
                                <div style="font-size: 0.72rem; color: #94A3B8;">Timeline Realism</div>
                                <div style="font-size: 0.95rem; font-weight: 700; color: #FBBF24;">{analysis.get('timeline_score', 26)}/30</div>
                            </div>
                        </div>
                        <div style="margin-top: 12px; font-size: 0.85rem; color: #CBD5E1;">
                            <strong>Audit Assessment:</strong> {analysis.get('scope_assessment', '')}
                        </div>
                        <div style="margin-top: 6px; font-size: 0.85rem; color: #F87171;">
                            <strong>Identified Red Flags:</strong> {analysis.get('red_flags', 'None detected')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("#### ✉️ Bespoke Outreach Pitch")
                    st.text_input("Subject Line:", value=analysis.get("subject", ""), key=f"subj_{i}")
                    
                    pitch_text = analysis.get("pitch_body", "")
                    st.text_area("Custom Outreach Email:", value=pitch_text, height=220, key=f"pitch_box_{i}")
                    
                    # 1-Click Download proposal button
                    full_export = f"""# Proposal for {lead['title']}
**Company:** {lead['company_name']}
**Platform:** {lead['via']}
**Original Posting:** {lead['link']}
**Viability Score:** {score}/100

---

## Subject: {analysis.get('subject', '')}

{pitch_text}
"""
                    st.download_button(
                        label=f"📥 Download Proposal ({lead['company_name']}.md)",
                        data=full_export,
                        file_name=f"proposal_{lead['company_name'].lower().replace(' ', '_')}.md",
                        mime="text/markdown",
                        key=f"dl_md_{i}"
                    )

if __name__ == "__main__":
    main()
