print("\n                  SYSTEM ANALYSIS                  ")
print("_" * 50)

while True:
    print("\nProblem")
    problem = input("Enter your issue: ").strip()

    # future: understand and analyze the problem

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