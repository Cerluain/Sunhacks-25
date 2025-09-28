"""
ASU Chatbot LLM Module

This module provides an AI-powered chatbot for Arizona State University
using LangChain agents with Google Gemini LLM and Tavily search integration.

Features:
- Conversational memory for follow-up questions
- Real-time web search capabilities
- Structured responses with source extraction
- ASU-specific knowledge and context
"""

from dotenv import load_dotenv
import os
from datetime import datetime
from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from app.models.llm_schemas import LLMResponse, Source
from .prompts import PROMPT_TEMPLATE
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

load_dotenv()

def get_current_date():
    """Returns current date in MM-DD-YYYY format"""
    return datetime.now().strftime("%m-%d-%Y")

# Initialize tools and LLM
tools = [TavilySearch(tavily_api_key=os.getenv("TAVILY_API_KEY"))]
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-lite-latest",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Configure prompt template with current date
current_date = get_current_date()
prompt_template = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["input", "agent_scratchpad", "tool_names", "tools", "chat_history"],
).partial(current_date=current_date)

# Initialize conversation memory
memory = ConversationBufferWindowMemory(
    k=5,  # Remember last 5 interactions
    memory_key="chat_history",
    input_key="input"
)

# Create agent and executor
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt_template,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,  # Set to True for debugging
    handle_parsing_errors=True,
    max_iterations=100,
    memory=memory,
    return_intermediate_steps=True,
)

# Main chain for processing user queries
chain = agent_executor

def process_result(result):
    """Process the agent result and convert to LLMResponse format"""
    if isinstance(result, dict) and 'output' in result:
        output_text = result['output']
        
        # Extract sources from intermediate steps
        sources = []
        if 'intermediate_steps' in result:
            for step in result['intermediate_steps']:
                # Each step is a tuple (AgentAction, observation)
                if len(step) > 1:
                    observation = step[1]
                    # Tavily returns results in a specific format
                    if isinstance(observation, dict) and 'results' in observation:
                        for search_result in observation['results']:
                            if 'url' in search_result and search_result['url']:
                                sources.append(Source(url=search_result['url']))
        
        # Create a basic LLMResponse structure
        return LLMResponse(
            answer=[output_text],  # Convert to list as per your schema
            sources=sources  # Now includes extracted URLs from searches
        )
    return result

def query_llm(user_input: str) -> LLMResponse:
    """
    Query the LLM agent with conversation memory and return structured response.
    
    Args:
        user_input (str): The user's question or input
        
    Returns:
        LLMResponse: Structured response with answer and sources
    """
    result = chain.invoke({"input": user_input})
    return process_result(result)