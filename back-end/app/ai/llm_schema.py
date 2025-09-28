from typing import List, Optional
from pydantic import BaseModel, Field


class Source(BaseModel):
    """Source information for LLM responses"""
    url: str = Field(..., description="URL of the source")


class LLMResponse(BaseModel):
    """Structured response from the LLM agent"""
    answer: List[str] = Field(..., description="List of answer segments")
    sources: List[Source] = Field(default_factory=list, description="Sources used in the response")


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    question: str = Field(..., description="The user's question", min_length=1, max_length=1000)
    include_history: Optional[bool] = Field(True, description="Whether to include conversation history in response")


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    question: str = Field(..., description="The original question")
    answer: List[str] = Field(..., description="List of answer segments")
    sources: List[Source] = Field(default_factory=list, description="Sources used in the response")
    conversation_history: Optional[List[dict]] = Field(None, description="Conversation history if requested")