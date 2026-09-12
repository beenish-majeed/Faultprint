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

def analyze_system_data(problem: str, investigation: list[str], system_data: dict):
    prompt = f"""
You are analyzing a computer problem using actual system data.

User's problem:
{problem}

Investigation requested:
{investigation}

Actual system data:
{system_data}

Analyze the data in the context of the user's problem.

Return ONLY valid JSON with exactly these keys:
- findings
- likely_cause

"findings" must be a list of objects.
Each object must contain:
- area
- status
- details

Rules:
- Consider only the data that is relevant to the user's problem.
- Determine whether each relevant area appears normal or problematic based on the actual data and context.
- Do not use fixed percentage rules.
- Do not invent information that is not present in the system data.
- Do not claim something is the cause unless the available data supports it.
- If the data is insufficient to determine the cause, say so.
- Keep the findings concise.
- "likely_cause" should be a short explanation of the most likely cause, or say that the cause cannot be determined from the available data.
- Do not provide solutions yet.
- Do not include reasoning outside the JSON.

User problem, investigation, and system data are provided above.
"""

    try:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )
    except Exception as error:
        return f"Gemini analysis failed: {error}"

    response = interaction.output_text.strip()

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return response
