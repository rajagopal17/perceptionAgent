import os
from dotenv import load_dotenv

import asyncio
from google import genai
import time
import json
from structures.models import DecisionInput, DecisionResult
# Load environment variables from .env file
load_dotenv()



# Access your API key and initialize Gemini client correctly
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_plan(decision_input: DecisionInput) -> DecisionResult:
    """
    Generates a plan using using LLM (Gemini) based on the structured perception.
    """
  
    perception = decision_input.perception
    tool_description = decision_input.tool_description

    tool_context = f"you have access to the following tools: {tool_description}"
    prompt = f""" you have access to the following tools {tool_context}.
                  your task is to solve user query step by step using the tools.

    
    user query: {perception.query}
    user intent: {perception.intent}
    user entities: {"'".join(perception.entities)}
                """
    response = client.models.generate_content(
                         model = "gemini-2.0-flash", contents=prompt)
    
    raw      = response.text.strip()
    return DecisionResult(raw.strip())

## Example usage


    
    

                                     

