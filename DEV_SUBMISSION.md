---
title: "ClientRadar AI: Freelance Lead Arbitrage Engine with SerpApi & Gemma 2"
published: true
tags: devchallenge, hf26challenge, hacktoberfest, ai
canonical_url: https://github.com/AshrafGalaxy/ClientRadar
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12)*

# ClientRadar AI: Real-Time Freelance Lead Arbitrage Engine 💸

*Participating in **Best Use of SerpApi** and **Best Use of Gemma**.*

---

## 1. What I Built
**ClientRadar AI** is an autonomous client discovery and proposal generation engine built for independent technical contractors, freelance developers, and boutique agencies.

Freelancers lose an estimated 10-15 hours every week scanning job boards, checking Reddit threads, filtering out low-paying clients, and writing custom proposals from scratch. 

ClientRadar automates this pipeline end-to-end:
1. **Live Opportunity Discovery & Deep-Linking:** Connects to **SerpApi's** Google Jobs engine to harvest fresh, high-ticket freelance and contract roles in real time, automatically resolving direct application deep-links across LinkedIn, Indeed, and ZipRecruiter.
2. **Multi-Tier Viability & Risk Audit:** Ingests the unstructured brief into Google's open-weight **Gemma 2** (`google/gemma-2-2b-it`), scoring client viability ($0-100$) across Scope Clarity (35 pts), Budget Transparency (35 pts), and Timeline Realism (30 pts) while flagging red flags (e.g. scope-creep indicators, equity-only offers).
3. **Contextual Proposal Studio:** Gemma 2 generates bespoke proposals tailored to specific contractor strategies (*Direct Technical*, *Rapid MVP 48-Hour Kickoff*, or *Strategic Agency Retainer*) complete with one-click clipboard copying and Markdown download.

---

## 2. Who Would Pay For This? (The Side Hustle Thesis)
* **Target Market:** Freelance software engineers, independent AI specialists, and agency operators.
* **Pricing Model:** Micro-SaaS at **$29/month**.
* **The ROI Equation:** A single won contract pays for more than 5 years of the software subscription. Freelancers immediately recoup their investment by converting hours of manual searching into actionable client conversations.
* **Unit Economics Advantage:** Running open-weight models (Gemma 2) paired with SerpApi enables near 100% gross profit margins, avoiding the per-token cost penalties of closed LLM APIs.

---

## 3. How SerpApi Powers This Build
Traditional LLMs cannot search the live web reliably without expensive, proprietary browsing wrappers. SerpApi acts as the real-time sensory layer of ClientRadar:
- **Direct Google Jobs Extraction:** Queries the `google_jobs` engine dynamically for niche contract terms without maintaining fragile, site-specific HTML scrapers.
- **Structured Normalization:** Transmutes unstructured search data across LinkedIn, Indeed, and ZipRecruiter into clean, reliable JSON objects containing titles, descriptions, and direct URLs.
- **Zero Scraping Infrastructure:** Eliminates the operational overhead of proxy rotation and CAPTCHA solving.

---

## 4. Why Open Innovation & Open-Weight Models Matter
Building ClientRadar on proprietary, closed APIs creates fatal operational liabilities:

1. **Unit Economics & Margin Preservation:** Scanning dozens of listings and running in-depth prompt analysis creates high token consumption. Proprietary API fees rapidly erode micro-SaaS margins. Running **Gemma 2** on low-cost compute or local Ollama instances preserves near **100% gross profit margins**.
2. **Confidentiality & Data Sovereignty:** Freelancers frequently evaluate client descriptions containing confidential features or competitive strategies. Open-weight models guarantee that sensitive client data is never transmitted to closed third-party providers for commercial retraining.
3. **No Vendor Lock-In:** Independent builders retain total control over model quantization, latency parameters, and prompt design without fear of sudden API deprecations or policy shifts.

---

## 5. Tech Stack & Integration
- **Live Search & Job Data:** [SerpApi](https://serpapi.com/)
- **Open-Weight AI Model:** Google Gemma 2 (`google/gemma-2-2b-it`)
- **Frontend & App Logic:** Python, Streamlit
- **License:** Open Source (MIT)

---

## 6. Code Repository & Demonstration
- **GitHub Repository:** [https://github.com/AshrafGalaxy/ClientRadar](https://github.com/AshrafGalaxy/ClientRadar)
- **Live Application Workflow:**
  1. Input target technical keywords (e.g., `FastAPI Backend Freelance`).
  2. Click **Scan for Qualified Leads** to pull live market opportunities via SerpApi.
  3. Click **Generate Proposal with Gemma 2** to review client risk factors and copy a ready-to-send technical bid.
