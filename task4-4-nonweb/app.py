# SWE40006 - Software Deployment and Evolution
# Task 4.4 - Non-Web-Based Docker Application
# Student Result Analyzer

def calculate_grade(mark):
    if mark >= 80:
        return "HD"
    elif mark >= 70:
        return "D"
    elif mark >= 60:
        return "C"
    elif mark >= 50:
        return "P"
    else:
        return "N"


def main():
    print("=" * 55)
    print("       SWE40006 STUDENT RESULT ANALYZER")
    print("       Task 4.4 - Non-Web Docker App")
    print("=" * 55)

    students = [
        {"name": "Aisha", "mark": 86},
        {"name": "Daniel", "mark": 74},
        {"name": "Mei Ling", "mark": 68},
        {"name": "Arun", "mark": 55},
        {"name": "Sarah", "mark": 42},
    ]

    print("\nSTUDENT RESULTS")
    print("-" * 55)
    print(f"{'Student':<20}{'Mark':<15}{'Grade':<10}")
    print("-" * 55)

    total = 0
    passed = 0

    for student in students:
        mark = student["mark"]
        grade = calculate_grade(mark)

        total += mark

        if mark >= 50:
            passed += 1

        print(f"{student['name']:<20}{mark:<15}{grade:<10}")

    average = total / len(students)
    highest = max(students, key=lambda x: x["mark"])
    lowest = min(students, key=lambda x: x["mark"])

    print("-" * 55)
    print("\nRESULT SUMMARY")
    print(f"Total Students : {len(students)}")
    print(f"Passed         : {passed}")
    print(f"Failed         : {len(students) - passed}")
    print(f"Average Mark   : {average:.2f}")
    print(f"Highest Mark   : {highest['name']} ({highest['mark']})")
    print(f"Lowest Mark    : {lowest['name']} ({lowest['mark']})")

    print("\n" + "=" * 55)
    print("Analysis completed successfully inside Docker.")
    print("=" * 55)


if __name__ == "__main__":
    main()