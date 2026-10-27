
import math


def calculate_attendance(attended, conducted):
    if conducted < 0 or attended < 0:
        raise ValueError("Class counts cannot be negative.")
    if attended > conducted:
        raise ValueError("Attended classes cannot exceed classes conducted.")
    if conducted == 0:
        return 0.0

    return (attended / conducted) * 100


def minimum_classes_needed(attended, conducted, threshold):
    """
    Minimum consecutive classes that must ALL be attended
    to reach the eligibility threshold.
    """
    if not 0 <= threshold <= 100:
        raise ValueError("Threshold must be between 0 and 100.")

    if conducted < 0 or attended < 0 or attended > conducted:
        raise ValueError("Invalid attendance counts.")

    if conducted == 0 and attended != 0:
        raise ValueError("Invalid attendance records.")

    # Already eligible
    if calculate_attendance(attended, conducted) >= threshold:
        return 0

    # If every future class is attended:
    # (attended + n) / (conducted + n) >= threshold / 100
    if threshold == 100:
        return None if attended < conducted else 0

    required = (
        threshold * conducted - 100 * attended
    ) / (100 - threshold)

    return max(0, math.ceil(required))


def future_scenario(attended, conducted, future_classes,
                    future_attended, threshold):
    """Calculate attendance after a future set of classes."""
    if future_classes < 0 or future_attended < 0:
        raise ValueError("Future class counts cannot be negative.")

    if future_attended > future_classes:
        raise ValueError(
            "Future attended classes cannot exceed future classes."
        )

    final_attended = attended + future_attended
    final_conducted = conducted + future_classes

    percentage = calculate_attendance(
        final_attended, final_conducted
    )

    return {
        "future_classes": future_classes,
        "future_attended": future_attended,
        "final_attended": final_attended,
        "final_conducted": final_conducted,
        "percentage": percentage,
        "eligible": percentage >= threshold,
    }


def main():
    print("ATTENDANCE RECOVERY CALCULATOR")

    try:
        attended = int(input("Classes attended so far: "))
        conducted = int(input("Total classes conducted: "))
        threshold = float(input("Required attendance percentage: "))

        if attended < 0 or conducted < 0 or attended > conducted:
            raise ValueError("Invalid current attendance counts.")

        if not 0 <= threshold <= 100:
            raise ValueError("Threshold must be between 0 and 100.")

        current = calculate_attendance(attended, conducted)
        needed = minimum_classes_needed(
            attended, conducted, threshold
        )

        print("\n========== CURRENT STATUS ==========")
        print(f"Classes attended : {attended}")
        print(f"Classes conducted: {conducted}")
        print(f"Current attendance: {current:.2f}%")
        print(f"Eligibility threshold: {threshold:.2f}%")

        if current >= threshold:
            print("Status: Eligible")
            print("Additional consecutive classes needed: 0")
        elif needed is None:
            print("Status: Threshold cannot be reached by finite attendance.")
        else:
            print("Status: Below threshold")
            print(f"Minimum consecutive classes to attend: {needed}")

        # Evaluate future attendance scenarios
        print("\n========== FUTURE SCENARIOS ==========")

        future_total = int(input("Number of future classes to evaluate: "))

        if future_total < 0:
            raise ValueError("Future classes cannot be negative.")

        scenarios = [
            ("Attend all", future_total),
            ("Attend 75%", math.floor(future_total * 0.75)),
            ("Attend 50%", math.floor(future_total * 0.50)),
            ("Miss all", 0),
        ]

        for name, future_attended in scenarios:
            result = future_scenario(
                attended,
                conducted,
                future_total,
                future_attended,
                threshold,
            )

            print(f"\nScenario: {name}")
            print(
                f"Future attendance: "
                f"{future_attended}/{future_total}"
            )
            print(
                f"Final attendance: "
                f"{result['final_attended']}/"
                f"{result['final_conducted']}"
            )
            print(f"Final percentage: {result['percentage']:.2f}%")
            print(
                "Eligibility:",
                "Eligible" if result["eligible"] else "Not eligible"
            )

    except ValueError as error:
        print("Input error:", error)


if __name__ == "__main__":
    main()
