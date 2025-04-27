import os
from dotenv import load_dotenv

import asyncio
from google import genai
import re
from models import PerceptionInput, PerceptionResult
from google.api_core import exceptions as google_exceptions
load_dotenv()

# Access your API key and initialize Gemini client correctly
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)





def extract_intent(input: PerceptionInput) -> PerceptionResult:
    """
    Extracts the user's intent from the input query using the Gemini LLM.

    Args:
        perception_input: An object containing the user's query.

    Returns:
        A PerceptionResult object containing the original query and the extracted intent.

    Raises:
        PerceptionError: If there's an issue during the API call or processing the response.
        ValueError: If the input query is empty or None.
    """


    user_question = input.query

    # Construct the prompt for the LLM to extract intent
    prompt = f"""You are an intelligent assistant.
Your task is to analyze user queries and extract the primary intent and entities behind them.
Return the response as a python dictionary with the following keys:
- "intent": The primary intent of the user query[ex: get_weather, book_flight, get_news, send_email, etc].
- "entities": A list of entities mentioned in the query [ex:"India","Times Square","gmail", etc]. 
-  "Geography": The name of the continent in which the entity is located [ex: USA is in NorthAmerica, etc] 
Output only the dictionary in a single line without any additional text or explanation. 
Do not wrap the output in '''json any other format.                    

User Query: "{user_question}"   

Identified Intent:"""   
    response = client.models.generate_content(model = "gemini-2.0-flash", contents=prompt)
    extract_intent =response.candidates[0].content.parts[0].text.strip()
    result = PerceptionResult(query=user_question, intent=extract_intent,entities=None,geography=None)
    return extract_intent


# Example usage of function:

test_input = PerceptionInput(query="Orangutans are found in Indonesia only and chimpanzees are found in Kenya")
result = extract_intent(test_input)
print(result)



    


                                              
    
    

    




