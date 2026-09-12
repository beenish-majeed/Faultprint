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


def select_system_data(problem: str, investigation: list[str]):
    available_data = [
        "CPU information",
        "Memory information",
        "Disk information",
        "Running processes",
        "Battery information",
        "Network information",
        "Boot and uptime information",
        "Disk partition information",
        "Temperature information"
    ]

    prompt = f"""
You are deciding what computer data should be collected
to investigate a user's problem.

User's problem:
{problem}

Investigation:
{investigation}

Available computer data:
{available_data}

Choose only the data that is relevant to investigating
the user's problem.

Return ONLY valid JSON with exactly this key:
- required_data

"required_data" must be a list containing only items
from the available computer data list.

Rules:
- Understand the meaning of the user's problem.
- Match concepts semantically.
- Do not require exact wording between the investigation
  and available data.
- Select only data that could help investigate the problem.
- Do not provide explanations or solutions.
"""

    try:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )
    except Exception as error:
        return f"Gemini data selection failed: {error}"

    response = interaction.output_text.strip()

    if response.startswith("```"):
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

    try:
        data = json.loads(response)
        return data["required_data"]
    except (json.JSONDecodeError, KeyError):
        return response

def analyze_system_data(problem: str, investigation: list[str], system_data: dict):
    prompt = f"""
You are analyzing a computer problem using actual system data.

User's problem:
{problem}

Investigation:
{investigation}

Actual system data:
{system_data}

Analyze the actual system data in the context of the user's problem.

Return ONLY valid JSON with exactly these keys:
- findings
- likely_cause

"findings" must be a list of objects.
Each object must contain:
- area
- status
- details

Rules:
- Consider only data relevant to the user's problem.
- Use the actual values in the system data.
- Determine whether each relevant area appears normal,
  problematic, or inconclusive based on the context.
- Do not use fixed percentage thresholds.
- Do not invent information that is not present.
- Do not claim something is the cause unless the data supports it.
- If the available data is insufficient, say so.
- Keep the findings concise.
- "likely_cause" must be a short explanation of the
  most likely cause, or say that it cannot be determined
  from the available data.
- Do not provide solutions yet.
- Do not include reasoning outside the JSON.
"""

    try:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )
    except Exception as error:
        return f"Gemini system analysis failed: {error}"

    response = interaction.output_text.strip()

    if response.startswith("```"):
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return response