from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Source(BaseModel):
    """Source information for LLM responses"""
    url: str = Field(..., description="URL of the source")


class LLMResponse(BaseModel):
    """Structured response from the LLM agent"""
    answer: List[str] = Field(..., description="List of answer segments")
    sources: List[Source] = Field(default_factory=list, description="Sources used in the response")