from typing import List, Optional

from pydantic import BaseModel, Field


class ChatHistoryItem(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    history: List[ChatHistoryItem] = Field(default_factory=list)
    current_path: Optional[str] = None


class NavigationTarget(BaseModel):
    label: str
    route: str


class ChatStep(BaseModel):
    """One scripted execution step shown by the demo assistant."""

    icon: str
    text: str


class ChatReply(BaseModel):
    reply: str
    navigation: Optional[NavigationTarget] = None
    suggestions: List[str] = Field(default_factory=list)
    steps: List[ChatStep] = Field(default_factory=list)
