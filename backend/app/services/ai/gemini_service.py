import json
import logging
from typing import Any, Optional

import google.generativeai as genai

from app.config.settings import get_settings
from app.core.exceptions import GeminiServiceError

logger = logging.getLogger(__name__)
settings = get_settings()

ANALYSIS_PROMPT = """You are an expert Upwork job analyst and freelance business strategist.
Analyze the job posting and client data to help freelancers decide whether to bid.

Return ONLY valid JSON with this exact structure:
{
  "extracted_job_info": "Brief summary of job title, skills needed, budget hints, timeline",
  "success_score": 0-100 number,
  "bid_decision": "recommended_to_bid" | "bid_with_caution" | "skip_this_job",
  "bid_reasoning": "Clear explanation in plain English",
  "connect_strategy": {
    "minimum_connects": number,
    "recommended_connects": number,
    "maximum_connects": number,
    "warning": "Optional warning message or null"
  },
  "competition_analysis": {
    "proposal_count": number or null,
    "competition_level": "low" | "medium" | "high" | "very_high",
    "visibility_chance": "Description of visibility odds",
    "recommended_submission_timing": "When to submit the proposal"
  },
  "client_analysis": {
    "trust_level": "trusted" | "moderate_risk" | "high_risk",
    "payment_verified": true/false/null,
    "total_spending": number or null,
    "hiring_history": "Summary of hiring patterns",
    "active_jobs_info": "Info about current activity",
    "review_history": "Summary of client reputation signals",
    "summary": "Overall client quality assessment"
  },
  "proposal_text": "A winning Upwork proposal. Human tone. No emojis. No generic AI phrases."
}

Be realistic. Score 0-100 based on all provided factors."""

PROPOSAL_PROMPT = """Write a winning Upwork proposal. Human tone. Client-focused. No emojis. No robotic language.
Return ONLY valid JSON: {"proposal_text": "the proposal"}"""


class GeminiService:
    def __init__(self):
        if not settings.gemini_api_key:
            raise GeminiServiceError("Gemini API key is not configured")
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)

    def _parse_json_response(self, content: str) -> dict[str, Any]:
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[-1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("```", 1)[0]
            cleaned = cleaned.strip()
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
        return json.loads(cleaned)

    def _build_prompt(
        self,
        job_description: str,
        client_info: dict[str, Any],
        screenshot_text: Optional[str] = None,
    ) -> str:
        parts = [
            ANALYSIS_PROMPT,
            "",
            "JOB DESCRIPTION:",
            job_description,
            "",
            "CLIENT INFORMATION:",
            json.dumps(client_info, indent=2),
        ]
        if screenshot_text:
            parts.extend(["", "SCREENSHOT EXTRACTED TEXT:", screenshot_text])
        return "\n".join(parts)

    def analyze_job(
        self,
        job_description: str,
        client_info: dict[str, Any],
        screenshot_path: Optional[str] = None,
        screenshot_text: Optional[str] = None,
    ) -> dict[str, Any]:
        try:
            prompt = self._build_prompt(job_description, client_info, screenshot_text)
            content_parts: list[Any] = [prompt]

            if screenshot_path:
                import pathlib

                image_path = pathlib.Path(screenshot_path)
                if image_path.exists():
                    uploaded = genai.upload_file(str(image_path))
                    content_parts.append(uploaded)

            response = self.model.generate_content(content_parts)
            text = response.text
            if not text:
                raise GeminiServiceError("Empty response from Gemini")

            result = self._parse_json_response(text)
            result["ai_provider_used"] = "gemini"
            return result

        except GeminiServiceError:
            raise
        except Exception as exc:
            logger.error("Gemini analysis failed: %s", exc)
            raise GeminiServiceError(str(exc)) from exc

    def generate_proposal(
        self,
        job_description: str,
        client_info: dict[str, Any],
        analysis_context: Optional[dict[str, Any]] = None,
        freelancer_profile: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        try:
            parts = [
                PROPOSAL_PROMPT,
                "",
                "JOB DESCRIPTION:",
                job_description,
                "",
                "CLIENT INFO:",
                json.dumps(client_info, indent=2),
            ]
            if analysis_context:
                parts.extend(["", "CONTEXT:", json.dumps(analysis_context, indent=2)])
            if freelancer_profile:
                parts.extend(["", "FREELANCER:", json.dumps(freelancer_profile, indent=2)])

            response = self.model.generate_content("\n".join(parts))
            text = response.text
            if not text:
                raise GeminiServiceError("Empty proposal from Gemini")

            result = self._parse_json_response(text)
            result["ai_provider_used"] = "gemini"
            return result

        except GeminiServiceError:
            raise
        except Exception as exc:
            logger.error("Gemini proposal failed: %s", exc)
            raise GeminiServiceError(str(exc)) from exc

    def extract_text_from_image(self, screenshot_path: str) -> str:
        try:
            import pathlib

            image_path = pathlib.Path(screenshot_path)
            uploaded = genai.upload_file(str(image_path))
            response = self.model.generate_content(
                [
                    "Extract all visible text from this Upwork job screenshot. Return plain text only.",
                    uploaded,
                ]
            )
            return response.text or ""
        except Exception as exc:
            logger.error("Gemini OCR failed: %s", exc)
            raise GeminiServiceError(str(exc)) from exc
