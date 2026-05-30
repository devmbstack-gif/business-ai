class AIServiceError(Exception):
    pass


class OpenAIServiceError(AIServiceError):
    pass


class GeminiServiceError(AIServiceError):
    pass


class AnalysisProcessingError(Exception):
    pass
