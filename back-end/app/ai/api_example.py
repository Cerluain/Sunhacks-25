"""
Example of how to use the LLM agent as a JSON API endpoint
"""
from dotenv import load_dotenv
from app.ai.llm import chain, process_result

def query_llm_json(user_input: str) -> dict:
    """
    Query the LLM agent and return JSON response
    
    Args:
        user_input (str): The user's question
        
    Returns:
        dict: JSON response with answer and sources
    """
    # Invoke the chain with user input
    result = chain.invoke({
        "input": user_input
    })
    
    # Process the result to get LLMResponse format
    processed = process_result(result)
    
    # Convert to dict for JSON serialization
    return {
        "answer": processed.answer,  # List[str]
        "sources": [{"url": source.url} for source in processed.sources]  # List[dict]
    }