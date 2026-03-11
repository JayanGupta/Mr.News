"""
analyzer.py — Gemini AI engine for Mr.News.
Optimized: single API call for all sections + automatic retry with backoff for 429 errors.
"""

import os
import re
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
from core.prompts import SYSTEM_INSTRUCTION, combined_research_prompt

load_dotenv()

MODEL_NAME = "gemini-2.5-flash"

# Retry config for 429 rate limit errors
MAX_RETRIES = 4
BASE_BACKOFF_SECONDS = 12


class GeminiAnalyzer:
    def __init__(self, api_key: str = None):
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError(
                "No Gemini API key provided. "
                "Either pass it in the sidebar or set GEMINI_API_KEY in your environment."
            )
        self.client = genai.Client(api_key=key)

    def _call(self, prompt: str) -> str:
        """
        Single Gemini call with automatic retry + exponential backoff for 429 errors.
        """
        for attempt in range(MAX_RETRIES + 1):
            try:
                response = self.client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.4,
                    ),
                )
                return response.text.strip()
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    if attempt < MAX_RETRIES:
                        wait_time = BASE_BACKOFF_SECONDS * (2 ** attempt)
                        time.sleep(wait_time)
                        continue
                raise

    def _parse_sections(self, raw_output: str) -> dict:
        """
        Parse the combined output into separate sections using markers.
        Falls back gracefully if markers aren't found.
        """
        sections = {
            "expert_research": "",
            "plain_english": "",
            "summary": "",
        }

        # Try to split on section markers
        sec1_pattern = r"={3,}\s*\n\s*SECTION\s*1.*?\n\s*={3,}\s*\n"
        sec2_pattern = r"={3,}\s*\n\s*SECTION\s*2.*?\n\s*={3,}\s*\n"
        sec3_pattern = r"={3,}\s*\n\s*SECTION\s*3.*?\n\s*={3,}\s*\n"
        end_pattern  = r"={3,}\s*\n\s*END\s+OF\s+REPORT\s*\n\s*={3,}"

        # Find positions
        sec1_match = re.search(sec1_pattern, raw_output, re.IGNORECASE)
        sec2_match = re.search(sec2_pattern, raw_output, re.IGNORECASE)
        sec3_match = re.search(sec3_pattern, raw_output, re.IGNORECASE)
        end_match  = re.search(end_pattern, raw_output, re.IGNORECASE)

        if sec1_match and sec2_match and sec3_match:
            # Clean extraction using markers
            sec1_start = sec1_match.end()
            sec2_start = sec2_match.end()
            sec3_start = sec3_match.end()

            sections["expert_research"] = raw_output[sec1_start:sec2_match.start()].strip()
            sections["plain_english"] = raw_output[sec2_start:sec3_match.start()].strip()

            if end_match:
                sections["summary"] = raw_output[sec3_start:end_match.start()].strip()
            else:
                sections["summary"] = raw_output[sec3_start:].strip()
        else:
            # Fallback: try splitting on ## headers
            plain_match = re.search(r"## 📖 Plain English Guide", raw_output)
            summary_match = re.search(r"## 📋 Executive Summary", raw_output)

            if plain_match and summary_match:
                sections["expert_research"] = raw_output[:plain_match.start()].strip()
                sections["plain_english"] = raw_output[plain_match.start():summary_match.start()].strip()
                sections["summary"] = raw_output[summary_match.start():].strip()
            else:
                # Last resort: put everything in expert_research
                sections["expert_research"] = raw_output
                sections["summary"] = "*(Summary could not be parsed from the combined output.)*"
                sections["plain_english"] = "*(Plain English guide could not be parsed from the combined output.)*"

        return sections

    def analyze(self, topic: str, raw_context: str, status_callback=None) -> dict:
        """
        Single Gemini call that produces all sections at once.
        Returns dict with expert_research, plain_english, and summary as Markdown strings.
        """
        if status_callback:
            status_callback("analyzing")

        raw_output = self._call(combined_research_prompt(topic, raw_context))
        return self._parse_sections(raw_output)
