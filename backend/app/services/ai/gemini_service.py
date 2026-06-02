import base64
import json
import logging
from pathlib import Path
from typing import Any, Optional

import httpx

from app.config.settings import get_settings
from app.core.exceptions import GeminiServiceError

logger = logging.getLogger(__name__)
settings = get_settings()

GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"

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
        self.api_key = (settings.gemini_api_key or "").strip()
        if not self.api_key:
            raise GeminiServiceError("Gemini API key is not configured")
        self.model = settings.gemini_model.strip() or "gemini-2.0-flash"

    def _request_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key,
        }

    def _generate_content(self, parts: list[dict[str, Any]]) -> str:
        url = f"{GEMINI_API_BASE}/models/{self.model}:generateContent"
        payload = {"contents": [{"parts": parts}]}

        try:
            with httpx.Client(timeout=120.0) as client:
                response = client.post(url, headers=self._request_headers(), json=payload)
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPStatusError as exc:
            error_body = exc.response.text
            logger.error("Gemini HTTP error %s: %s", exc.response.status_code, error_body)
            if exc.response.status_code == 400 and "API key not valid" in error_body:
                raise GeminiServiceError(
                    "Gemini API key is invalid. In AI Studio, create a new key and ensure "
                    "Generative Language API is enabled for your project."
                ) from exc
            raise GeminiServiceError(f"Gemini API error: {error_body}") from exc
        except Exception as exc:
            logger.error("Gemini request failed: %s", exc)
            raise GeminiServiceError(str(exc)) from exc

        candidates = data.get("candidates") or []
        if not candidates:
            raise GeminiServiceError("Gemini returned no candidates")

        content = candidates[0].get("content") or {}
        text_parts = content.get("parts") or []
        text = "".join(part.get("text", "") for part in text_parts if isinstance(part, dict))
        if not text.strip():
            raise GeminiServiceError("Empty response from Gemini")
        return text

    def _image_part(self, image_path: str) -> dict[str, Any]:
        path = Path(image_path)
        if not path.exists():
            raise GeminiServiceError(f"Screenshot not found: {image_path}")

        suffix = path.suffix.lower()
        mime_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }
        mime_type = mime_map.get(suffix, "image/png")
        encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
        return {"inline_data": {"mime_type": mime_type, "data": encoded}}

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
            parts: list[dict[str, Any]] = [
                {"text": self._build_prompt(job_description, client_info, screenshot_text)}
            ]
            if screenshot_path and Path(screenshot_path).exists():
                parts.append(self._image_part(screenshot_path))

            text = self._generate_content(parts)
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
            prompt_parts = [
                PROPOSAL_PROMPT,
                "",
                "JOB DESCRIPTION:",
                job_description,
                "",
                "CLIENT INFO:",
                json.dumps(client_info, indent=2),
            ]
            if analysis_context:
                prompt_parts.extend(["", "CONTEXT:", json.dumps(analysis_context, indent=2)])
            if freelancer_profile:
                prompt_parts.extend(["", "FREELANCER:", json.dumps(freelancer_profile, indent=2)])

            text = self._generate_content([{"text": "\n".join(prompt_parts)}])
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
            parts = [
                {
                    "text": (
                        "Extract all visible text from this Upwork job screenshot. "
                        "Return plain text only."
                    )
                },
                self._image_part(screenshot_path),
            ]
            return self._generate_content(parts)
        except Exception as exc:
            logger.error("Gemini OCR failed: %s", exc)
            raise GeminiServiceError(str(exc)) from exc
