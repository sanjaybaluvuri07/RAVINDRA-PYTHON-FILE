
from decimal import Decimal, ROUND_HALF_UP

# Illustrative fare policy (amounts in INR)
DISTANCE_SLABS = [
    (Decimal("100"), Decimal("1.50")),
    (Decimal("300"), Decimal("1.30")),
    (Decimal("500"), Decimal("1.10")),
    (None, Decimal("0.90")),
]

CLASS_MULTIPLIERS = {
    "Sleeper": Decimal("1.0"),
    "AC3": Decimal("2.0"),
    "AC2": Decimal("3.0"),
    "AC1": Decimal("4.0"),
}

RESERVATION_FEES = {
    "Sleeper": Decimal("20"),
    "AC3": Decimal("40"),
    "AC2": Decimal("50"),
    "AC1": Decimal("60"),
}

# Illustrative age-based concessions
CONCESSIONS = {
    "child": Decimal("0.50"),       # Ages 5-11
    "senior": Decimal("0.40"),      # Age 60+
}

CANCELLATION_RATES = {
    "Sleeper": Decimal("0.25"),
    "AC3": Decimal("0.25"),
    "AC2": Decimal("0.30"),
    "AC1": Decimal("0.30"),
}

CENT = Decimal("0.01")


def money(amount):
    return Decimal(str(amount)).quantize(
        CENT, rounding=ROUND_HALF_UP
    )


def calculate_base_fare(distance):
    """Progressive distance slabs: each rate applies to its slab."""
    if distance <= 0:
        raise ValueError("Distance must be greater than zero.")

    remaining = Decimal(distance)
    previous_limit = Decimal("0")
    fare = Decimal("0")

    for limit, rate in DISTANCE_SLABS:
        if limit is None:
            slab_distance = remaining
        else:
            limit = Decimal(limit)
            slab_distance = min(
                remaining, limit - previous_limit
            )

        if slab_distance > 0:
            fare += slab_distance * rate
            remaining -= slab_distance

        if remaining <= 0:
            break

        if limit is not None:
            previous_limit = Decimal(limit)

    return money(fare)


def get_concession(age):
    if age < 0 or age > 120:
        raise ValueError("Age must be between 0 and 120.")

    if age < 5:
        return Decimal("1.00"), "Under 5: illustrative free fare"
    elif age < 12:
        return CONCESSIONS["child"], "Child concession"
    elif age >= 60:
        return CONCESSIONS["senior"], "Senior concession"
    else:
        return Decimal("0.00"), "No concession"


def calculate_passenger_fare(name, age, distance, travel_class):
    if travel_class not in CLASS_MULTIPLIERS:
        raise ValueError("Invalid travel class.")

    base_fare = calculate_base_fare(distance)
    class_fare = money(
        base_fare * CLASS_MULTIPLIERS[travel_class]
    )

    concession_rate, concession_label = get_concession(age)
    concession_amount = money(class_fare * concession_rate)

    discounted_fare = money(class_fare - concession_amount)
    reservation_fee = (
        Decimal("0.00")
        if age < 5
        else RESERVATION_FEES[travel_class]
    )

    total = money(discounted_fare + reservation_fee)

    return {
        "name": name,
        "age": age,
        "travel_class": travel_class,
        "base_fare": base_fare,
        "class_fare": class_fare,
        "concession_label": concession_label,
        "concession_amount": concession_amount,
        "reservation_fee": reservation_fee,
        "total": total,
    }


def calculate_cancellation(passenger, penalty_rate=None):
    """
    Illustrative cancellation policy:
    use a specified penalty rate if supplied;
    otherwise use the class-specific default.
    """
    if penalty_rate is None:
        rate = CANCELLATION_RATES[passenger["travel_class"]]
    else:
        rate = Decimal(str(penalty_rate))

    if not rate.is_finite() or not Decimal("0") <= rate <= Decimal("1"):
        raise ValueError("Penalty rate must be between 0 and 1.")

    penalty = money(passenger["total"] * rate)
    refund = money(passenger["total"] - penalty)

    return penalty, refund


def main():
    print("RAILWAY FARE AND RESERVATION CALCULATOR")

    try:
        distance = int(input("Enter journey distance in km: "))
        if distance <= 0:
            raise ValueError("Distance must be positive.")

        travel_class = input(
            "Enter class (Sleeper/AC3/AC2/AC1): "
        ).strip()

        if travel_class not in CLASS_MULTIPLIERS:
            raise ValueError("Invalid travel class.")

        count = int(input("Enter number of passengers: "))
        if count <= 0:
            raise ValueError("Passenger count must be positive.")

        passengers = []

        for i in range(count):
            print(f"\nPassenger {i + 1}")
            name = input("Name: ").strip()
            if not name:
                raise ValueError("Passenger name is required.")

            age = int(input("Age: "))

            passenger = calculate_passenger_fare(
                name, age, distance, travel_class
            )
            passengers.append(passenger)

        print("\n========== FARE SUMMARY ==========")
        grand_total = Decimal("0.00")

        for p in passengers:
            print(f"\nPassenger: {p['name']} (Age {p['age']})")
            print(f"Class fare        : Rs. {p['class_fare']:.2f}")
            print(f"Concession        : {p['concession_label']}")
            print(f"Concession amount : Rs. {p['concession_amount']:.2f}")
            print(f"Reservation fee   : Rs. {p['reservation_fee']:.2f}")
            print(f"Passenger total   : Rs. {p['total']:.2f}")
            grand_total += p["total"]

        print("\nTotal passengers :", len(passengers))
        print(f"Total reservation fare: Rs. {money(grand_total):.2f}")

        cancel = input(
            "\nCalculate cancellation refund? (yes/no): "
        ).strip().lower()

        if cancel == "yes":
            rate_input = input(
                "Enter cancellation penalty percentage (0-100), "
                "or press Enter for class default: "
            ).strip()

            penalty_rate = (
                Decimal(rate_input) / Decimal("100")
                if rate_input
                else None
            )

            total_penalty = Decimal("0.00")
            total_refund = Decimal("0.00")

            print("\n========== CANCELLATION SUMMARY ==========")

            for p in passengers:
                penalty, refund = calculate_cancellation(
                    p, penalty_rate
                )
                print(f"\nPassenger: {p['name']}")
                print(f"Cancellation penalty: Rs. {penalty:.2f}")
                print(f"Refund amount       : Rs. {refund:.2f}")

                total_penalty += penalty
                total_refund += refund

            print(f"\nTotal penalty: Rs. {money(total_penalty):.2f}")
            print(f"Total refund : Rs. {money(total_refund):.2f}")

    except (ValueError, TypeError) as error:
        print("Input error:", error)


if __name__ == "__main__":
    main()
