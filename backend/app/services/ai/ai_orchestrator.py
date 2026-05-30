import logging
from typing import Any, Optional

from app.core.exceptions import AIServiceError, GeminiServiceError, OpenAIServiceError
from app.services.ai.gemini_service import GeminiService
from app.services.ai.openai_service import OpenAIService

logger = logging.getLogger(__name__)


class AIOrchestrator:
    def __init__(self):
        self._openai: Optional[OpenAIService] = None
        self._gemini: Optional[GeminiService] = None

    @property
    def openai(self) -> OpenAIService:
        if self._openai is None:
            self._openai = OpenAIService()
        return self._openai

    @property
    def gemini(self) -> GeminiService:
        if self._gemini is None:
            self._gemini = GeminiService()
        return self._gemini

    def extract_screenshot_text(self, screenshot_path: Optional[str]) -> Optional[str]:
        if not screenshot_path:
            return None

        try:
            return self.gemini.extract_text_from_image(screenshot_path)
        except GeminiServiceError as gemini_error:
            logger.warning("Gemini OCR failed, trying OpenAI: %s", gemini_error)
            try:
                return self.openai.extract_text_from_image(screenshot_path)
            except OpenAIServiceError:
                return None

    def analyze_job(
        self,
        job_description: str,
        client_info: dict[str, Any],
        screenshot_path: Optional[str] = None,
    ) -> dict[str, Any]:
        screenshot_text = self.extract_screenshot_text(screenshot_path)

        try:
            logger.info("Attempting job analysis with OpenAI")
            return self.openai.analyze_job(
                job_description=job_description,
                client_info=client_info,
                screenshot_path=screenshot_path,
                screenshot_text=screenshot_text,
            )
        except OpenAIServiceError as openai_error:
            logger.warning("OpenAI failed, falling back to Gemini: %s", openai_error)
            try:
                return self.gemini.analyze_job(
                    job_description=job_description,
                    client_info=client_info,
                    screenshot_path=screenshot_path,
                    screenshot_text=screenshot_text,
                )
            except GeminiServiceError as gemini_error:
                raise AIServiceError(
                    f"Both AI providers failed. OpenAI: {openai_error}. Gemini: {gemini_error}"
                ) from gemini_error

    def generate_proposal(
        self,
        job_description: str,
        client_info: dict[str, Any],
        analysis_context: Optional[dict[str, Any]] = None,
        freelancer_profile: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        try:
            return self.openai.generate_proposal(
                job_description=job_description,
                client_info=client_info,
                analysis_context=analysis_context,
                freelancer_profile=freelancer_profile,
            )
        except OpenAIServiceError as openai_error:
            logger.warning("OpenAI proposal failed, falling back to Gemini: %s", openai_error)
            return self.gemini.generate_proposal(
                job_description=job_description,
                client_info=client_info,
                analysis_context=analysis_context,
                freelancer_profile=freelancer_profile,
            )
