"""
Conversation-based API for handling follow-up questions
"""
from dotenv import load_dotenv
from app.ai.llm import chain, process_result
from typing import List, Dict

class ConversationAPI:
    """API for handling conversational interactions with memory"""
    
    def __init__(self):
        load_dotenv()
        # The chain already has memory, so we just need to track conversation
        self.conversation_history = []
    
    def ask_question(self, user_input: str, include_history: bool = True) -> Dict:
        """
        Ask a question to the LLM agent
        
        Args:
            user_input (str): The user's question
            include_history (bool): Whether to include conversation history in response
            
        Returns:
            dict: JSON response with answer, sources, and optionally conversation history
        """
        # Invoke the chain with user input (memory is automatic)
        result = chain.invoke({
            "input": user_input
        })
        
        # Process the result to get LLMResponse format
        processed = process_result(result)
        
        # Store this interaction in our local history
        interaction = {
            "question": user_input,
            "answer": processed.answer[0] if processed.answer else "",
            "sources_count": len(processed.sources)
        }
        self.conversation_history.append(interaction)
        
        # Build response
        response = {
            "answer": processed.answer,  # List[str]
            "sources": [{"url": source.url} for source in processed.sources],  # List[dict]
            "question": user_input
        }
        
        # Include conversation history if requested
        if include_history:
            response["conversation_history"] = self.conversation_history
            
        return response
    
    def get_conversation_summary(self) -> Dict:
        """Get a summary of the conversation so far"""
        return {
            "total_questions": len(self.conversation_history),
            "conversation_history": self.conversation_history
        }
    
    def clear_conversation(self):
        """Clear the conversation history (Note: This doesn't clear the agent's memory)"""
        self.conversation_history = []