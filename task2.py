
from decimal import Decimal, ROUND_HALF_UP
from math import ceil

CENT = Decimal("0.01")


def money(amount):
    return Decimal(str(amount)).quantize(
        CENT, rounding=ROUND_HALF_UP
    )


def get_nonnegative(prompt):
    value = Decimal(input(prompt))
    if not value.is_finite() or value < 0:
        raise ValueError("Amount must be a non-negative number.")
    return value


def get_positive_int(prompt):
    value = int(input(prompt))
    if value <= 0:
        raise ValueError("Value must be a positive integer.")
    return value


def calculate_event_budget(
    venue_cost,
    equipment_cost,
    catering_per_person,
    transport_per_person,
    certificate_per_person,
    expected_participants,
    sponsorship,
    registration_fee
):
    # Validate monetary inputs
    amounts = [
        venue_cost, equipment_cost, catering_per_person,
        transport_per_person, certificate_per_person,
        sponsorship, registration_fee
    ]

    if any(not amount.is_finite() or amount < 0 for amount in amounts):
        raise ValueError("All monetary amounts must be non-negative.")

    if expected_participants <= 0:
        raise ValueError("Participants must be greater than zero.")

    # Fixed and variable costs
    fixed_cost = money(venue_cost + equipment_cost)

    variable_cost_per_person = money(
        catering_per_person
        + transport_per_person
        + certificate_per_person
    )

    total_variable_cost = money(
        variable_cost_per_person * expected_participants
    )

    total_cost = money(fixed_cost + total_variable_cost)

    # Sponsorship funding
    sponsorship_shortfall = money(
        max(Decimal("0"), total_cost - sponsorship)
    )

    surplus_sponsorship = money(
        max(Decimal("0"), sponsorship - total_cost)
    )

    # Registration revenue and balance
    registration_revenue = money(
        registration_fee * expected_participants
    )

    total_funding = money(sponsorship + registration_revenue)
    balance = money(total_funding - total_cost)

    # Minimum registrations to break even
    remaining_fixed_cost = max(
        Decimal("0"), fixed_cost - sponsorship
    )

    contribution_per_person = money(
        registration_fee - variable_cost_per_person
    )

    if remaining_fixed_cost == 0:
        minimum_registrations = 0
    elif contribution_per_person <= 0:
        minimum_registrations = None
    else:
        minimum_registrations = ceil(
            remaining_fixed_cost / contribution_per_person
        )

    # Display report
    print("\n========== EVENT BUDGET ==========")
    print(f"Venue cost             : Rs. {money(venue_cost):.2f}")
    print(f"Equipment cost         : Rs. {money(equipment_cost):.2f}")
    print(f"Catering total         : Rs. {money(catering_per_person * expected_participants):.2f}")
    print(f"Transport total        : Rs. {money(transport_per_person * expected_participants):.2f}")
    print(f"Certificate total      : Rs. {money(certificate_per_person * expected_participants):.2f}")
    print("----------------------------------")
    print(f"Total event cost       : Rs. {total_cost:.2f}")
    print(f"Sponsorship            : Rs. {money(sponsorship):.2f}")
    print(f"Sponsorship shortfall  : Rs. {sponsorship_shortfall:.2f}")
    print(f"Sponsorship surplus    : Rs. {surplus_sponsorship:.2f}")
    print(f"Registration fee       : Rs. {money(registration_fee):.2f}")
    print(f"Registration revenue   : Rs. {registration_revenue:.2f}")
    print(f"Total funding          : Rs. {total_funding:.2f}")
    print(f"Budget balance         : Rs. {balance:.2f}")

    print("\n========== BREAK-EVEN ==========")
    if minimum_registrations is None:
        print("Break-even is impossible at this fee.")
        print("Increase the fee or secure more sponsorship.")
    else:
        print(f"Minimum registrations : {minimum_registrations}")

        if minimum_registrations > expected_participants:
            print("Warning: Expected attendance is insufficient.")
        else:
            print("Break-even is achievable at expected attendance.")

    return {
        "total_cost": total_cost,
        "sponsorship_shortfall": sponsorship_shortfall,
        "budget_balance": balance,
        "minimum_registrations": minimum_registrations
    }


def main():
    print("CAMPUS EVENT FINANCIAL PLANNER")
    print("Enter all monetary amounts in INR.\n")

    try:
        venue = get_nonnegative("Venue cost: Rs. ")
        equipment = get_nonnegative("Equipment cost: Rs. ")
        catering = get_nonnegative("Catering cost per person: Rs. ")
        transport = get_nonnegative("Transport cost per person: Rs. ")
        certificate = get_nonnegative("Certificate cost per person: Rs. ")

        participants = get_positive_int("Expected participants: ")

        sponsorship = get_nonnegative("Confirmed sponsorship: Rs. ")
        fee = get_nonnegative("Registration fee per person: Rs. ")

        calculate_event_budget(
            venue,
            equipment,
            catering,
            transport,
            certificate,
            participants,
            sponsorship,
            fee
        )

    except (ValueError, TypeError) as error:
        print("Input error:", error)


if __name__ == "__main__":
    main()
