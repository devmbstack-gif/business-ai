import base64
import json
import logging
from typing import Any, Optional

from openai import OpenAI

from app.config.settings import get_settings
from app.core.exceptions import OpenAIServiceError

logger = logging.getLogger(__name__)
settings = get_settings()

ANALYSIS_SYSTEM_PROMPT = """You are an expert Upwork job analyst and freelance business strategist.
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
  "proposal_text": "A winning Upwork proposal. Human tone. No emojis. No generic AI phrases. Client-focused. Professional but conversational."
}

Scoring factors: payment verification, client spending, proposal count, hire rate, connect cost, budget, complexity, competition.
Be realistic and practical. Write proposals that sound like a skilled freelancer wrote them."""

PROPOSAL_SYSTEM_PROMPT = """You are a top-performing Upwork freelancer writing a proposal.
Write a human, personalized, client-focused proposal.

Rules:
- Sound natural, not robotic
- No generic openings like "I am writing to express my interest"
- No emojis
- No excessive dashes or bullet spam
- Address the client's specific needs
- Show understanding of the project
- Keep it concise and professional
- Make it unique and plagiarism-free

Return ONLY valid JSON:
{
  "proposal_text": "The full proposal text"
}"""


class OpenAIService:
    def __init__(self):
        if not settings.openai_api_key:
            raise OpenAIServiceError("OpenAI API key is not configured")
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def _parse_json_response(self, content: str) -> dict[str, Any]:
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[-1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("```", 1)[0]
        return json.loads(cleaned)

    def _build_user_message(
        self,
        job_description: str,
        client_info: dict[str, Any],
        screenshot_text: Optional[str] = None,
    ) -> str:
        parts = [
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
            messages: list[dict[str, Any]] = [
                {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
            ]

            if screenshot_path and not screenshot_text:
                with open(screenshot_path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode("utf-8")
                ext = screenshot_path.lower().split(".")[-1]
                mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
                messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self._build_user_message(job_description, client_info),
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:{mime};base64,{image_data}"},
                            },
                        ],
                    }
                )
            else:
                messages.append(
                    {
                        "role": "user",
                        "content": self._build_user_message(
                            job_description, client_info, screenshot_text
                        ),
                    }
                )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=4096,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            if not content:
                raise OpenAIServiceError("Empty response from OpenAI")

            result = self._parse_json_response(content)
            result["ai_provider_used"] = "openai"
            return result

        except OpenAIServiceError:
            raise
        except Exception as exc:
            logger.error("OpenAI analysis failed: %s", exc)
            raise OpenAIServiceError(str(exc)) from exc

    def generate_proposal(
        self,
        job_description: str,
        client_info: dict[str, Any],
        analysis_context: Optional[dict[str, Any]] = None,
        freelancer_profile: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        try:
            user_content = [
                "JOB DESCRIPTION:",
                job_description,
                "",
                "CLIENT INFO:",
                json.dumps(client_info, indent=2),
            ]
            if analysis_context:
                user_content.extend(["", "ANALYSIS CONTEXT:", json.dumps(analysis_context, indent=2)])
            if freelancer_profile:
                user_content.extend(["", "FREELANCER PROFILE:", json.dumps(freelancer_profile, indent=2)])

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": PROPOSAL_SYSTEM_PROMPT},
                    {"role": "user", "content": "\n".join(user_content)},
                ],
                temperature=0.8,
                max_tokens=2048,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            if not content:
                raise OpenAIServiceError("Empty proposal response from OpenAI")

            result = self._parse_json_response(content)
            result["ai_provider_used"] = "openai"
            return result

        except OpenAIServiceError:
            raise
        except Exception as exc:
            logger.error("OpenAI proposal generation failed: %s", exc)
            raise OpenAIServiceError(str(exc)) from exc

    def extract_text_from_image(self, screenshot_path: str) -> str:
        try:
            with open(screenshot_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")
            ext = screenshot_path.lower().split(".")[-1]
            mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Extract all visible text from this Upwork job screenshot. Return plain text only.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:{mime};base64,{image_data}"},
                            },
                        ],
                    }
                ],
                max_tokens=2048,
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            logger.error("OpenAI OCR failed: %s", exc)
            raise OpenAIServiceError(str(exc)) from exc
