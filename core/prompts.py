"""
prompts.py — Gemini prompt templates for Mr.News expert research pipeline.
Optimized: single combined prompt to minimize API calls (1 call instead of 3).
"""

import datetime

CURRENT_YEAR = datetime.datetime.now().year

SYSTEM_INSTRUCTION = """
You are Mr.News — an elite research analyst and field expert with 30+ years of experience,
created by Jayan Gupta. You combine the depth of a senior technical architect, the market
insight of an industry analyst, and the clarity of a world-class science communicator.

Your reports are:
- Exhaustively researched using ONLY the provided scraped data
- Technically precise with real architecture details, code patterns, and benchmarks
- Structured with clear Markdown: headings, subheadings, bullet points, tables, code blocks
- Honest — you state what is confirmed, what is speculative, and what data is missing
- Never hallucinated — if the source data doesn't cover it, you say "Not confirmed in available sources"

You write as if your report will be read by a CTO making a $10M adoption decision.
"""


def combined_research_prompt(topic: str, raw_context: str) -> str:
    """
    Single combined prompt that generates ALL three sections in one Gemini call:
    1. Expert Research Report
    2. Plain English Guide
    3. Executive Summary

    This minimizes API usage (1 call instead of 3).
    """
    return f"""
You are writing a **complete research report** on: **{topic}**

You are a field expert and analyst with 30+ years of experience. Your report should reflect
deep technical mastery, industry awareness, and analytical rigour. Every claim must be
grounded in the scraped data below.

---SCRAPED CONTEXT START---
{raw_context}
---SCRAPED CONTEXT END---

You MUST produce THREE clearly separated sections in your response, using the exact
section markers shown below. Each section serves a different audience. Write ALL three.

====================================================================
SECTION 1: EXPERT RESEARCH REPORT
====================================================================

Write a thorough, technical expert research report with the following structure.
Each subsection must be DETAILED — not surface-level. Use real data, numbers, and
specifics from the context. Include tables where appropriate.

## 🔍 What Is {topic}?

### Definition & Origin
- Clear, precise definition (2–3 sentences)
- Who created/developed it and when
- The problem it was designed to solve
- Its category/classification in the broader landscape

### Key Facts at a Glance
| Attribute | Detail |
|---|---|
| Creator / Company | |
| Launch Date | |
| Category | |
| Current Version | |
| Pricing Model | |
| Primary Users | |
(fill from context — leave "Not confirmed" for missing data)

---

## ⚡ Core Features & Capabilities

For EACH major feature, provide:
- **What it does** (technical description)
- **Why it matters** (practical impact)
- **Technical specifications** (numbers, limits, benchmarks if available)

### Feature Comparison Table
| Feature | Description | Technical Details |
|---|---|---|
(list ALL major features found in context, minimum 6 rows)

---

## 🏗️ How It Works — Technical Deep Dive

### Architecture & Technical Design
- Internal architecture (components, layers, data flow)
- Core technologies and frameworks used
- Describe the technical workflow step-by-step

### Integration & APIs
- Available APIs, SDKs, supported languages/platforms
- Authentication methods
- Rate limits or usage constraints

### Code Example or Workflow
```
(Include a realistic code snippet, CLI command, or step-by-step workflow from context.
If no code is available, describe the integration workflow in numbered steps.)
```

### Performance & Benchmarks
| Metric | Value | Context/Notes |
|---|---|---|
(fill from any benchmark data found in context)

---

## 👥 Who Uses It & Real-World Applications

### Target Users
- Primary user personas (developers, enterprises, researchers, etc.)
- Industry verticals that benefit most

### Real-World Use Cases
- At least 5 concrete, specific use cases across different domains
- Include company names or industries if mentioned in context

### Adoption & Market Position
- Market share or adoption metrics (if available)
- Notable companies or organizations using it
- Growth trends or trajectory

---

## 🚀 How to Get Started

### Setup & Prerequisites
- System requirements or prerequisites
- Account/access requirements

### Step-by-Step Quick Start
1. (Number each step clearly)
2. (Include specific commands, URLs, or actions)
3. (Through to a working first result)

### Resources & Documentation
- Official docs, tutorials, community resources
- Learning path recommendation for a newcomer

---

## ⚔️ Competitive Landscape

### Head-to-Head Comparison
| Aspect | {topic} | Competitor 1 | Competitor 2 | Competitor 3 |
|---|---|---|---|---|
| Core Strength | | | | |
| Pricing | | | | |
| Ease of Use | | | | |
| Performance | | | | |
| Community/Support | | | | |
| Best For | | | | |
(fill competitor names and data from context — at least 3 alternatives)

### When to Choose {topic} vs Alternatives
- Specific scenarios where {topic} wins
- Specific scenarios where alternatives are better

---

## ✅ Strengths & ❌ Limitations

### Strengths (Expert Assessment)
- At least 6 specific strengths, each with a brief technical justification

### Limitations & Known Issues
- At least 5 honest limitations, gotchas, or criticisms found in context
- Known bugs or pain points from user reviews

### Expert Risk Assessment
| Risk Factor | Impact Level | Mitigation |
|---|---|---|
(include vendor lock-in, scalability, cost, etc.)

---

## 📰 Latest News & Trending Developments ({CURRENT_YEAR})

Cover ALL trending news angles found in the context. Include ALL categories with data:

### Product & Technical Updates
- Recent version releases, feature launches, API changes
- Upcoming features, roadmap, beta announcements

### Financial & Business News
- Revenue figures, profitability, losses, or valuation changes
- Funding rounds, investments, business model changes

### Partnerships, Acquisitions & Deals
- Strategic partnerships or integrations
- Acquisitions, major enterprise deals

### Controversies, Challenges & Risks
- Layoffs, restructuring, leadership changes
- Lawsuits, regulatory actions, public criticism, safety concerns

### Industry Impact & Market Movement
- Market share shifts, competitive dynamics
- Analyst opinions and predictions

### Trending News Summary Table
| Date/Period | Event | Impact | Source |
|---|---|---|---|
(fill with the most significant recent events, at least 4 rows)

---

## 🎯 Expert Verdict & Recommendations

### Overall Rating
| Dimension | Rating (1–10) | Justification |
|---|---|---|
| Technical Capability | | |
| Ease of Adoption | | |
| Value for Money | | |
| Future-Proofing | | |
| Documentation & Support | | |
| Overall | | |

### Who Should Use This
- Ideal user profiles (be specific)

### Who Should NOT Use This
- Anti-patterns and misuse cases

### Final Analyst Opinion
(3–5 sentences as a 30+ year veteran giving their honest, authoritative take.)

====================================================================
SECTION 2: PLAIN ENGLISH GUIDE
====================================================================

Now re-explain EVERYTHING from Section 1 in simple language for someone with ZERO
technical background. Follow these rules:
1. Use analogies — compare every concept to everyday life
2. Use examples — show real scenarios
3. Zero jargon — explain any technical term in parentheses
4. Short sentences — under 20 words where possible
5. Conversational tone — like explaining to a friend over coffee

## 📖 Plain English Guide: {topic}

### So, What Exactly Is {topic}?
(Explain using a relatable analogy. 3–4 sentences max.)

### What Can It Actually Do?
(List main capabilities with simple real-life examples)
- **[Feature]**: Think of it like... [analogy]. For example, [scenario].

### How Does It Work? (The Simple Version)
(Step-by-step using analogies)

### Who Actually Uses This?
(List user types with relatable descriptions)

### How Would YOU Get Started?
(Simple numbered steps as if guiding a friend)

### How Does It Compare to the Competition?
(Simple opinionated comparison)

### The Good and the Not-So-Good
**👍 What's great:**
- [Simple strength]

**👎 What could be better:**
- [Simple limitation]

### What's Happening Right Now?
(All the latest news — product updates, money news, drama, deals — in simple bullets)

### The Bottom Line
(3–4 sentences: recommend it? For whom? When to skip?)

====================================================================
SECTION 3: EXECUTIVE SUMMARY
====================================================================

## 📋 Executive Summary: {topic}

### In One Sentence
(The single most important thing to know — powerful and precise)

### TL;DR — What You Need to Know
- 8–10 concise bullet points covering: what it is, who made it, key capabilities,
  who uses it, pricing, strengths, weaknesses, latest news, verdict

### Key Metrics at a Glance
| Metric | Value |
|---|---|
| Category | |
| Creator | |
| Current Version | |
| Pricing | |
| Expert Rating | /10 |
| Best For | |
| Avoid If | |

### Overall Verdict
| Dimension | Rating (1–10) |
|---|---|
| Technical Capability | |
| Ease of Use | |
| Value for Money | |
| Future-Proofing | |

### Bottom Line
(3–4 sentences: authoritative recommendation. Who should use it, who should avoid it, why.)

====================================================================
END OF REPORT
====================================================================

IMPORTANT RULES:
- Use EVERY relevant piece of information from the scraped context
- Keep the exact section markers (====... SECTION N ...) so the output can be parsed
- Section 2 must NOT copy Section 1 — it must COMPLETELY re-explain using analogies
- Be exhaustive in Section 1, concise in Sections 2 and 3
"""
