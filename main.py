from models.problem_analysis import ProblemAnalysis
from services.ai_service import understand_problem, select_system_data, analyze_system_data
from collectors.system_collector import collect_system_data, display_system_data
import asyncio

async def main():

    print("\n                    SYSTEM ANALYSIS")
    print("_" * 55)

    while True:

        print("\nEnter your issue:", end=" ")
        problem = input().strip()

        problem1 = ProblemAnalysis()
        problem1.problem = problem

        try:
            analysis = await understand_problem(problem1.problem)

        except Exception as error:
            print("\nGemini is temporarily unavailable.")
            print(f"Error: {type(error).__name__}")
            print("Please try again later.")
            continue

        if analysis is None:
            print("\nUnable to understand the problem right now.")
        elif isinstance(analysis, ProblemAnalysis):

            print("\nProblem")
            print(analysis.problem)

            print("\nAreas")
            print(", ".join(analysis.areas))

            print("\nInvestigation")
            for item in analysis.investigation:
                print(f"• {item}")

            required_data = await select_system_data(
                analysis.problem,
                analysis.investigation
            )

            if required_data is None:
                print("\nUnable to determine required system data.")
            else:
                print("\nRequired Data")

                for item in required_data:
                    print(f"• {item}")

                system_data = collect_system_data(required_data)

                display_system_data(system_data)

                analysis_result = await analyze_system_data(
                    analysis.problem,
                    analysis.investigation,
                    system_data
                )

                print("\nAnalysis")

                if isinstance(analysis_result, dict):
                    print(analysis_result["summary"])

                    print("\nFindings")
                    for finding in analysis_result["findings"]:
                        print(f"• {finding}")

                    print("\nLikely Cause")
                    print(analysis_result["likely_cause"])

                else:
                    print("System analysis could not be completed.")
        else:
            print(analysis)

        print("\n1. Another Issue")
        print("2. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            continue

        elif choice == "2":
            print("\nThanks for using!")
            break

        else:
            print("\nEnter a valid choice.")


if __name__ == "__main__":
    asyncio.run(main())