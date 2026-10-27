
def classify_student(average):
    """Illustrative performance classification."""
    if average >= 90:
        return "Excellent"
    elif average >= 75:
        return "Very Good"
    elif average >= 60:
        return "Good"
    elif average >= 40:
        return "Average"
    else:
        return "Needs Improvement"


def analyze_student(name, scores, pass_mark=40):
    """
    scores format:
    {
        "Mathematics": [60, 70, 80],
        "Science": [45, 40, 35]
    }
    Each list contains scores from consecutive examinations.
    """

    if not name.strip():
        raise ValueError("Student name cannot be empty.")

    if not scores:
        raise ValueError("At least one subject is required.")

    if not 0 <= pass_mark <= 100:
        raise ValueError("Pass mark must be between 0 and 100.")

    subject_results = {}
    all_scores = []

    for subject, marks in scores.items():
        if not subject.strip():
            raise ValueError("Subject name cannot be empty.")

        if len(marks) < 2:
            raise ValueError(
                f"{subject}: Enter at least two examination scores."
            )

        if any(
            not isinstance(mark, (int, float))
            or isinstance(mark, bool)
            or not 0 <= mark <= 100
            for mark in marks
        ):
            raise ValueError(
                f"{subject}: Scores must be between 0 and 100."
            )

        first_score = marks[0]
        latest_score = marks[-1]
        improvement = latest_score - first_score

        average = sum(marks) / len(marks)

        if improvement > 0:
            trend = "Improved"
        elif improvement < 0:
            trend = "Declined"
        else:
            trend = "Unchanged"

        # A subject is consistently weak if every exam score
        # is below the pass mark.
        consistently_weak = all(
            mark < pass_mark for mark in marks
        )

        subject_results[subject] = {
            "scores": marks,
            "average": average,
            "first_score": first_score,
            "latest_score": latest_score,
            "improvement": improvement,
            "trend": trend,
            "weak": consistently_weak,
        }

        all_scores.extend(marks)

    overall_average = sum(all_scores) / len(all_scores)
    classification = classify_student(overall_average)

    print("\n========== STUDENT REPORT ==========")
    print(f"Student name       : {name}")
    print(f"Overall average    : {overall_average:.2f}%")
    print(f"Classification     : {classification}")

    print("\n========== SUBJECT ANALYSIS ==========")

    for subject, result in subject_results.items():
        print(f"\nSubject: {subject}")
        print(f"Exam scores        : {result['scores']}")
        print(f"Subject average    : {result['average']:.2f}")
        print(f"First exam score   : {result['first_score']}")
        print(f"Latest exam score  : {result['latest_score']}")
        print(f"Score change       : {result['improvement']:+.2f}")
        print(f"Trend              : {result['trend']}")

        if result["weak"]:
            print("Warning            : Consistently weak subject")

    weak_subjects = [
        subject
        for subject, result in subject_results.items()
        if result["weak"]
    ]

    print("\n========== SUMMARY ==========")

    if weak_subjects:
        print("Consistently weak subjects:")
        for subject in weak_subjects:
            print("-", subject)
    else:
        print("No consistently weak subjects identified.")

    improved = [
        subject for subject, result in subject_results.items()
        if result["trend"] == "Improved"
    ]

    declined = [
        subject for subject, result in subject_results.items()
        if result["trend"] == "Declined"
    ]

    print("Improved subjects :", ", ".join(improved) or "None")
    print("Declined subjects :", ", ".join(declined) or "None")

    return {
        "student": name,
        "overall_average": overall_average,
        "classification": classification,
        "subjects": subject_results,
        "weak_subjects": weak_subjects,
        "improved_subjects": improved,
        "declined_subjects": declined,
    }


def main():
    print("STUDENT PERFORMANCE TREND ANALYSIS")

    try:
        name = input("Enter student name: ").strip()

        number_of_subjects = int(
            input("Enter number of subjects: ")
        )

        number_of_exams = int(
            input("Enter number of examinations: ")
        )

        if number_of_subjects <= 0 or number_of_exams < 2:
            raise ValueError(
                "Subjects must be positive and at least two exams are required."
            )

        pass_mark = float(
            input("Enter subject pass mark (0-100): ")
        )

        scores = {}

        for i in range(number_of_subjects):
            subject = input(
                f"\nEnter subject {i + 1} name: "
            ).strip()

            if subject in scores:
                raise ValueError("Duplicate subject name.")

            marks = []

            for exam in range(number_of_exams):
                mark = float(input(
                    f"  Examination {exam + 1} score: "
                ))
                marks.append(mark)

            scores[subject] = marks

        analyze_student(name, scores, pass_mark)

    except ValueError as error:
        print("Input error:", error)


if __name__ == "__main__":
    main()
