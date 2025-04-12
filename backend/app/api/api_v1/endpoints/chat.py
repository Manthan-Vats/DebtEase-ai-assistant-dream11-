from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.chat import ChatMessage, ChatResponse
from app.services.chat import ChatService
from app.models.user import User

router = APIRouter()
chat_service = ChatService()


@router.post("/message", response_model=ChatResponse)
def send_message(
    *,
    db: Session = Depends(deps.get_db),
    message: ChatMessage,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Send a message to the AI assistant and get a response
    """
    try:
        response = chat_service.get_response(
            message=message.content,
            user_id=current_user.id,
            db=db
        )
        return ChatResponse(
            content=response,
            message_type="assistant"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}"
        )


@router.get("/history", response_model=List[ChatMessage])
def get_chat_history(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 50
) -> Any:
    """
    Get chat history for the current user
    """
    return chat_service.get_chat_history(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
