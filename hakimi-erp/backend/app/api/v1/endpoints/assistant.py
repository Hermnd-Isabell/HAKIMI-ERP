from fastapi import APIRouter, HTTPException

from app.schemas.assistant import ChatReply, ChatRequest
from app.schemas.base import ResponseModel
from app.services import assistant_service

router = APIRouter()


@router.post("/chat", response_model=ResponseModel[ChatReply])
async def chat(request: ChatRequest):
    """In-app assistant chat endpoint.

    Answers navigation / feature / workflow questions about the website.
    Read-only: it never mutates business data.
    """
    try:
        result = await assistant_service.chat(
            message=request.message,
            history=[item.model_dump() for item in request.history],
            current_path=request.current_path,
        )
    except RuntimeError as exc:
        # e.g. LLM_API_KEY not configured
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # LLM API errors, network issues, etc.
        raise HTTPException(status_code=502, detail=f"LLM request failed: {exc}") from exc

    return ResponseModel(data=ChatReply(**result))
