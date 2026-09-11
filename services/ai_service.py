from models.problem_analysis import ProblemAnalysis
from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv("API_KEY")

client = genai.Client(api_key = api_key)

def understand_problem(problem: str):
    prompt = f"""
You are helping diagnose computer problems.

First, determine whether the user's input is a computer-related problem.

If it IS a computer-related problem:
Return ONLY valid JSON with exactly these keys:
- problem: one short sentence describing the actual problem
- areas: only relevant computer system areas
- investigation: concise, actionable checks needed to investigate the problem

Rules for computer problems:
- Be concise and specific.
- No explanations.
- No reasoning.
- No recommendations or solutions.
- Do not repeat the user's full message.
- Include only relevant areas.

If it is NOT a computer-related problem, such as a greeting,
casual conversation, or general question:
Respond normally in plain text.
Do NOT return JSON.

User's input:
{problem}
"""

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    response = interaction.output_text.strip()

    try:
        data = json.loads(response)

        analysis = ProblemAnalysis()
        analysis.problem = data["problem"]
        analysis.areas = data["areas"]
        analysis.investigation = data["investigation"]

        return analysis

    except json.JSONDecodeError:
        return response

if __name__ == "__main__":       