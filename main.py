from models.problem_analysis import ProblemAnalysis
from services.ai_service import understand_problem, select_system_data, analyze_system_data
from collectors.system_collector import collect_system_data

print("\n                    SYSTEM ANALYSIS")
print("_" * 55)

while True:
    print("\nProblem")
    problem = input("Enter your issue: ").strip()
    
    problem1 = ProblemAnalysis()
    problem1.problem = problem
    analysis = understand_problem(problem1.problem)

    if isinstance(analysis, ProblemAnalysis):
        print("\nProblem:", analysis.problem)
        print("Areas:", ", ".join(analysis.areas))
        print("Investigation:", ", ".join(analysis.investigation))

        required_data = select_system_data(
            analysis.problem,
            analysis.investigation
        )

        print("\nRequired Data:", required_data)

        system_data = collect_system_data(required_data)

        print("\nSystem Data:", system_data)

        analysis_result = analyze_system_data(
            analysis.problem,
            analysis.investigation,
            system_data
        )

        print("\nAnalysis:", analysis_result)

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
