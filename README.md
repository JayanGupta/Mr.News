# 📰 Mr.News — Automated Research Report Generator

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Gemini](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash-purple)
![BeautifulSoup](https://img.shields.io/badge/Web%20Scraping-BeautifulSoup-green)
![Reports](https://img.shields.io/badge/Export-DOCX%20%7C%20PDF-orange)

> A structured research automation system that collects information from the web, analyzes it using large language models, and generates **well-structured research reports with both technical analysis and simplified explanations**.

---

# 📂 Repository Overview

This project implements a **data pipeline for automated research generation**, combining search, content extraction, LLM analysis, and report generation.

The system is designed to transform a **simple topic query into a comprehensive research document** with structured sections suitable for analysts, students, and decision-makers.

---

# ⚙️ Research Pipeline

The application follows a multi-stage pipeline:

### 1. 🔎 Multi-Query Web Search
The system generates **multiple query variations** to capture different perspectives of a topic, including:

- Features and capabilities
- Recent news and developments
- Financial or market implications
- Competitive comparisons
- Criticisms or limitations

Search results are retrieved using **DuckDuckGo**, eliminating the need for paid APIs.

---

### 2. 🌐 Content Extraction
Top results are automatically scraped and processed using **BeautifulSoup** and **lxml** to extract meaningful text while removing unnecessary HTML elements.

This stage converts raw webpages into **clean research-ready text corpora**.

---

### 3. 🧠 Large Language Model Analysis
All extracted content is passed to **Gemini 2.5 Flash** in a single optimized prompt to produce a structured analysis.

The model synthesizes information across multiple sources to generate:

- Technical insights
- Comparative analysis
- Key findings and implications

---

### 4. 📑 Structured Report Generation

The final output consists of **three complementary sections**:

#### 🔬 Expert Research Report
A deep technical analysis including:

- Key concepts
- Benchmarks
- Comparisons
- Industry positioning
- Structured tables

#### 📖 Plain English Guide
The same insights re-explained using:

- Simple language
- Analogies
- Minimal technical jargon

Designed for **non-technical readers**.

#### 📋 Executive Summary
A concise overview including:

- Key takeaways
- Quick evaluation
- Final verdict

---

# 🗂️ Project Structure
Mr.News/
│
├── app.py # Streamlit UI + research pipeline
├── requirements.txt # Python dependencies
├── .gitignore
│
└── core/
├── init.py
├── searcher.py # Multi-query web search + scraping
├── prompts.py # LLM prompt templates
├── analyzer.py # Gemini API client and retry logic
└── report_builder.py # DOCX and PDF report generation


---

# 🧰 Tech Stack

| Layer | Technology |
|------|-------------|
| Interface | Streamlit |
| Language Model | Gemini 2.5 Flash |
| Search Engine | DuckDuckGo |
| Web Scraping | BeautifulSoup + lxml |
| Report Generation | python-docx, ReportLab |
| Language | Python |

---

# 📊 System Capabilities

| Feature | Description |
|------|-------------|
| Automated Research | Generates complete research reports from a single topic |
| Multi-Source Analysis | Aggregates insights from multiple web sources |
| Dual Explanation | Technical research + simplified explanation |
| Structured Output | Cleanly formatted DOCX and PDF reports |
| Interactive UI | Streamlit interface for quick usage |

---

# 🚀 Getting Started

### Prerequisites

Ensure the following are installed:

```bash
pip install -r requirements.txt
```
You will also need a Gemini API key.

Get one from:

https://aistudio.google.com/

Run the Application
```bash
streamlit run app.py
```
Steps:

Enter your Gemini API key in the sidebar

Input a research topic

Click Research

Download the generated DOCX or PDF report

📌 Example Topics

You can generate reports on topics such as:

1. Claude AI
2. ChatGPT
3. Quantum Computing
4. Nvidia GPUs
5. Autonomous Vehicles
6. Open Source LLMs

👨‍💻 Author

Jayan Gupta
Data Scientist | Machine Learning | AI Systems
