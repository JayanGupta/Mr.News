# 📰 Mr.News

**AI-Powered Expert Research Reporter** — search any topic, get a full expert-level research report with plain English explanations, downloadable as DOCX or PDF.

---

## What It Does

Enter any topic (e.g. *"Claude"*, *"ChatGPT"*, *"Quantum Computing"*) and Mr.News will:

1. **Search** 12+ query variants across DuckDuckGo (features, news, financials, controversies, comparisons)
2. **Scrape** and extract content from top results
3. **Analyze** everything with Gemini AI in a single optimized call
4. **Generate** three report sections:
   - 🔬 **Expert Research** — deep technical analysis with tables, benchmarks, and competitive landscape
   - 📖 **Plain English Guide** — the same content re-explained with simple analogies and zero jargon
   - 📋 **Executive Summary** — TL;DR with ratings and verdict
5. **Export** as DOCX and/or PDF with professional formatting

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

3. Enter your [Gemini API key](https://aistudio.google.com/) in the sidebar
4. Type a topic and click **Research**

---

## Project Structure

```
Mr.News/
├── app.py                  # Streamlit UI and pipeline
├── requirements.txt        # Python dependencies
├── .gitignore
└── core/
    ├── __init__.py
    ├── searcher.py         # Web search + content scraping
    ├── prompts.py          # Gemini prompt templates
    ├── analyzer.py         # Gemini API client + retry logic
    └── report_builder.py   # DOCX and PDF report generation
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| AI Model | Gemini 2.5 Flash |
| Search | DuckDuckGo (no API key needed) |
| Scraping | BeautifulSoup + lxml |
| DOCX | python-docx |
| PDF | ReportLab |

---

## Requirements

- Python 3.9+
- Gemini API key (free tier works — 20 requests/day)
- Internet connection

---

**Built by Jayan**
