from models.problem_analysis import ProblemAnalysis
from services.ai_service import understand_problem, select_system_data, analyze_system_data
from collectors.system_collector import collect_system_data, display_system_data

print("\n                    SYSTEM ANALYSIS")
print("_" * 55)

while True:
    print("\nProblem")
    problem = input("Enter your issue: ").strip()
    
    problem1 = ProblemAnalysis()
    problem1.problem = problem
    analysis = understand_problem(problem1.problem)

    if isinstance(analysis, ProblemAnalysis):
        print("\nProblem")
        print(analysis.problem)

        print("\nAreas")
        print(", ".join(analysis.areas))
        
        print("\nInvestigation")
        for item in analysis.investigation:
            print(f"• {item}")

        required_data = select_system_data(
            analysis.problem,
            analysis.investigation
        )

        print("\nRequired Data")

        for item in required_data:
            print(f"• {item}")

        system_data = collect_system_data(required_data)

        display_system_data(system_data)

        analysis_result = analyze_system_data(
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
            print(analysis_result)

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
        print("Enter valid choice.")
