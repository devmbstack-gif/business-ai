from typing import Any, Optional

from app.schemas.response import ApiResponse


def success_response(data: Any = None, message: str = "Success") -> dict:
    return ApiResponse(status=True, message=message, data=data).model_dump()


def error_response(message: str, data: Any = None) -> dict:
    return ApiResponse(status=False, message=message, data=data).model_dump()
