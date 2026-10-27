
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import math

# Illustrative parking policy (INR)
VEHICLE_RATES = {
    "bike": Decimal("10"),
    "car": Decimal("30"),
    "truck": Decimal("50"),
}

# Rates per hour
OVERNIGHT_SURCHARGE = Decimal("20")
DAILY_LIMITS = {
    "bike": Decimal("100"),
    "car": Decimal("300"),
    "truck": Decimal("500"),
}

# Illustrative penalties
LOST_TICKET_PENALTY = Decimal("200")
INVALID_EXIT_PENALTY = Decimal("100")

TIME_FORMAT = "%Y-%m-%d %H:%M"
CENT = Decimal("0.01")


def money(amount):
    return Decimal(str(amount)).quantize(
        CENT, rounding=ROUND_HALF_UP
    )


def parse_time(value):
    try:
        return datetime.strptime(value, TIME_FORMAT)
    except ValueError:
        raise ValueError(
            "Invalid time. Use YYYY-MM-DD HH:MM."
        )


def calculate_parking_fee(
    entry_time,
    exit_time,
    vehicle_type,
    lost_ticket=False
):
    vehicle_type = vehicle_type.strip().lower()

    if vehicle_type not in VEHICLE_RATES:
        raise ValueError(
            "Vehicle must be bike, car, or truck."
        )

    entry = parse_time(entry_time)
    exit = parse_time(exit_time)

    if exit < entry:
        raise ValueError(
            "Exit time cannot be earlier than entry time."
        )

    duration_seconds = (exit - entry).total_seconds()
    duration_hours = duration_seconds / 3600

    # Any started hour counts as a full hour.
    charged_hours = math.ceil(duration_hours)

    # Charge for each started parking day.
    # A short stay still incurs at least one hour's fee.
    charged_days = max(1, math.ceil(charged_hours / 24))

    hourly_rate = VEHICLE_RATES[vehicle_type]
    daily_limit = DAILY_LIMITS[vehicle_type]

    # Charge hourly, capped at the daily limit.
    regular_fee = money(
        min(hourly_rate * charged_hours,
            daily_limit * charged_days)
    )

    # An overnight surcharge applies if parking crosses
    # midnight at least once.
    overnight_count = (
        exit.date() - entry.date()
    ).days

    overnight_fee = money(
        OVERNIGHT_SURCHARGE * overnight_count
    )

    # Apply overnight fees separately from the regular cap.
    total_fee = money(regular_fee + overnight_fee)

    penalty = Decimal("0.00")

    if lost_ticket:
        penalty += LOST_TICKET_PENALTY

    total_fee = money(total_fee + penalty)

    return {
        "vehicle": vehicle_type,
        "entry": entry,
        "exit": exit,
        "duration_hours": duration_hours,
        "charged_hours": charged_hours,
        "charged_days": charged_days,
        "regular_fee": regular_fee,
        "overnight_fee": overnight_fee,
        "penalty": money(penalty),
        "total_fee": total_fee,
    }


def print_receipt(result):
    print("\n========== PARKING RECEIPT ==========")
    print(f"Vehicle type       : {result['vehicle'].title()}")
    print(f"Entry time         : {result['entry']}")
    print(f"Exit time          : {result['exit']}")
    print(f"Actual duration    : {result['duration_hours']:.2f} hours")
    print(f"Charged hours      : {result['charged_hours']}")
    print(f"Charged days       : {result['charged_days']}")
    print(f"Regular parking fee: Rs. {result['regular_fee']:.2f}")
    print(f"Overnight fee      : Rs. {result['overnight_fee']:.2f}")
    print(f"Penalty            : Rs. {result['penalty']:.2f}")
    print("-------------------------------------")
    print(f"TOTAL AMOUNT       : Rs. {result['total_fee']:.2f}")
    print("=====================================")


def main():
    print("SMART PARKING FEE MANAGEMENT")

    try:
        vehicle = input(
            "Vehicle type (bike/car/truck): "
        ).strip()

        entry = input(
            "Entry time (YYYY-MM-DD HH:MM): "
        ).strip()

        exit_time = input(
            "Exit time (YYYY-MM-DD HH:MM): "
        ).strip()

        lost_ticket_input = input(
            "Lost ticket? (yes/no): "
        ).strip().lower()

        if lost_ticket_input not in ("yes", "no"):
            raise ValueError("Enter yes or no for lost ticket.")

        result = calculate_parking_fee(
            entry,
            exit_time,
            vehicle,
            lost_ticket=(lost_ticket_input == "yes")
        )

        print_receipt(result)

    except ValueError as error:
        print("Input error:", error)


if __name__ == "__main__":
    main()
