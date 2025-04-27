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


# Define a custom exception for perception layer errors
class PerceptionError(Exception):
    """Custom exception for errors occurring in the perception layer."""
    pass


def extract_intent(perception_input: PerceptionInput) -> PerceptionResult:
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
    if not perception_input or not perception_input.query:
        raise ValueError("Input query cannot be empty.")

    query = perception_input.query

    # Construct the prompt for the LLM to extract intent
    prompt = f"""You are an intelligent assistant.
Your task is to analyze user queries and extract the primary intent and entities behind them.
Return the response as a python dictionary with the following keys:
- "intent": The primary intent of the user query[ex: get_weather, book_flight, get_news, send_email, etc].
- "entities": A list of entities mentioned in the query [ex:"India","Times Square","gmail", etc].  
Output only the dictionary in a single line without any additional text or explanation. 
Do not wrap the output in '''json any other format.    

User Query: "{query}"

Identified Intent:"""

    try:
        # Make the API call to Gemini
        response = client.models.generate_content(model = "gemini-2.0-flash", contents=prompt)

        # Basic validation of the response structure
        # Accessing response.text directly is simpler if available and suitable
        if not hasattr(response, 'text') or not response.text:
             # Fallback check via candidates if .text is not reliable or empty
             if not response.candidates or not response.candidates[0].content or not response.candidates[0].content.parts:
                 raise PerceptionError("Gemini response was empty or malformed.")
             # If .text was empty/missing, try getting text from candidates
             extracted_intent = response.candidates[0].content.parts[0].text.strip()
        else:
             extracted_intent = response.text.strip() # Prefer .text if available

        if not extracted_intent:
             raise PerceptionError("Gemini returned an empty intent string.")

        # Create and return the result object
        result = PerceptionResult(
            user_input=query,
            intent=extracted_intent,
            entities= None# Assuming the intent extraction does not require entities, so we set it to None
            # entities field remains None by default as we are only extracting intent here
        )
        return result

    # Handle specific API errors from Google
    except google_exceptions.GoogleAPIError as e:
        # Log the error details if needed: print(f"Google API Error: {e}")
        raise PerceptionError(f"Gemini API error during intent extraction: {e}") from e
    # Handle potential network errors or timeouts (might be caught by GoogleAPIError too)
    except asyncio.TimeoutError as e:
        raise PerceptionError("Request to Gemini timed out during intent extraction.") from e
    # Handle other potential exceptions during the process
    except Exception as e:
        # Log the error details if needed: print(f"Unexpected Error: {e}")
        raise PerceptionError(f"An unexpected error occurred during intent extraction: {e}") from e

# Example Usage (optional, for testing within this file)
if __name__ == "__main__":
    test_query = "we are visiting Germany and Belgium next week. Can you suggest some places to visit?"
    test_input = PerceptionInput(query=test_query)

    try:
        perception_result = extract_intent(test_input)
        print(f"Original Query: {perception_result.user_input}")
        print(f"Extracted Intent: {perception_result.intent}")
        print(f"Entities: {perception_result.entities}") # Will be None

    except ValueError as ve:
        print(f"Input Error: {ve}")
    except PerceptionError as pe:
        print(f"Perception Error: {pe}")
    except ConnectionError as ce:
        print(f"Initialization Error: {ce}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")




 

    

