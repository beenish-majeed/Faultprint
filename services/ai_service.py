from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

client = genai.Client(api_key = api_key)

def understand_problem(problem :str):
    prompt = f"""
    You are helping diagnose a computer problem.

    Understand what the user actually means.
    Do not assume predefined categories.

    Determine:
    1. What the user's actual problem is.
    2. Which computer system areas may be relevant.
    3. What information should be investigated.

    User's problem:
    {problem}
    """
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input= prompt
    )
    
    return interaction.output_text