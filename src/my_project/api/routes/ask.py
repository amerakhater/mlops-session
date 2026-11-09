from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from my_project.api.deps import get_openai_service
from my_project.schemas.ask import AskRequest, AskResponse
from my_project.services.openai_service import LLMServiceError, OpenAIService

router = APIRouter(prefix="/ask", tags=["openai"])


@router.post("", response_model=AskResponse)
def ask(
    payload: AskRequest,
    service: Annotated[OpenAIService, Depends(get_openai_service)],
):
    try:
        return service.ask(payload.question)
    except LLMServiceError as exc:
        raise HTTPException(
            status.HTTP_502_BAD_GATEWAY, f"OpenAI error: {exc}"
        ) from exc
