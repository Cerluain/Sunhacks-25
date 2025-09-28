"""
Conversation-based API for handling follow-up questions
"""
from typing import Dict, List

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request

from app.ai.llm import chain, process_result
from app.ai.llm_schema import ChatRequest, ChatResponse, Source

# Load environment variables once
load_dotenv()

router = APIRouter()


def _get_conversation_history() -> List[Dict[str, str]]:
    """Return serialized conversation history from the chain's memory."""
    history: List[Dict[str, str]] = []

    memory = getattr(chain, "memory", None)
    chat_memory = getattr(memory, "chat_memory", None) if memory else None
    messages = getattr(chat_memory, "messages", None) if chat_memory else None

    if not messages:
        return history

    for message in messages:
        role = getattr(message, "type", message.__class__.__name__.replace("Message", "").lower())
        content = getattr(message, "content", "")
        if not isinstance(content, str):
            content = str(content)
        history.append({
            "role": role,
            "content": content,
        })

    return history

async def ask_question_service(request: ChatRequest) -> ChatResponse:
    """
    Ask a question to the LLM agent (stateless)
    
    Args:
        request (ChatRequest): The chat request containing question and options
        
    Returns:
        ChatResponse: Structured response with answer and sources
    """
    try:
        # Invoke the chain with user input (LLM has its own memory)
        result = chain.invoke({
            "input": request.question
        })
        
        # Process the result to get LLMResponse format
        processed = process_result(result)
        
        # Build response with optional conversation history
        response_data = {
            "question": request.question,
            "answer": processed.answer,  # List[str]
            "sources": [Source(url=source.url) for source in processed.sources],  # List[Source]
        }
        
        if request.include_history:
            response_data["conversation_history"] = _get_conversation_history()
            
        return ChatResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest, req: Request):
    """
    Ask a question to the ASU chatbot
    
    - **question**: The question to ask (required, 1-1000 characters)
    - **include_history**: Whether to include conversation history (optional, default: True)
    
    Note: This endpoint requires authentication. User info is available via req.state.user_email and req.state.user_id
    """
    # User is already authenticated by middleware, user info available in req.state
    user_email = getattr(req.state, 'user_email', None)
    user_id = getattr(req.state, 'user_id', None)
    
    return await ask_question_service(request)