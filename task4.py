
from decimal import Decimal, ROUND_HALF_UP

# Illustrative mobile plans; charges are in INR.
PLANS = [
    {
        "name": "Basic",
        "price": Decimal("199"),
        "validity": 28,
        "data_gb": Decimal("2"),
        "call_minutes": 300,
        "sms": 100,
        "extra_data_rate": Decimal("50"),  # per excess GB
        "extra_call_rate": Decimal("0.50"),  # per minute
        "extra_sms_rate": Decimal("0.20"),  # per SMS
    },
    {
        "name": "Smart",
        "price": Decimal("299"),
        "validity": 28,
        "data_gb": Decimal("10"),
        "call_minutes": 1000,
        "sms": 300,
        "extra_data_rate": Decimal("30"),
        "extra_call_rate": Decimal("0.40"),
        "extra_sms_rate": Decimal("0.15"),
    },
    {
        "name": "Unlimited",
        "price": Decimal("499"),
        "validity": 56,
        "data_gb": Decimal("30"),
        "call_minutes": 2000,
        "sms": 500,
        "extra_data_rate": Decimal("20"),
        "extra_call_rate": Decimal("0.30"),
        "extra_sms_rate": Decimal("0.10"),
    },
]


def money(value):
    return Decimal(str(value)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )


def evaluate_plan(plan, data_usage, call_usage, sms_usage,
                  required_validity, budget):

    # Reject plans that violate hard constraints.
    if plan["validity"] < required_validity:
        return None

    if plan["price"] > budget:
        return None

    # Calculate excess usage.
    excess_data = max(
        Decimal("0"), data_usage - plan["data_gb"]
    )
    excess_calls = max(0, call_usage - plan["call_minutes"])
    excess_sms = max(0, sms_usage - plan["sms"])

    # Data excess is charged per GB, including fractional GB.
    data_charge = excess_data * plan["extra_data_rate"]
    call_charge = Decimal(excess_calls) * plan["extra_call_rate"]
    sms_charge = Decimal(excess_sms) * plan["extra_sms_rate"]

    excess_total = money(data_charge + call_charge + sms_charge)
    total_cost = money(plan["price"] + excess_total)

    return {
        "name": plan["name"],
        "base_price": plan["price"],
        "validity": plan["validity"],
        "excess_data_gb": excess_data,
        "excess_calls": excess_calls,
        "excess_sms": excess_sms,
        "data_charge": money(data_charge),
        "call_charge": money(call_charge),
        "sms_charge": money(sms_charge),
        "excess_total": excess_total,
        "total_cost": total_cost,
        "within_budget": total_cost <= budget,
    }


def optimize_plans(data_usage, call_usage, sms_usage,
                   required_validity, budget):

    # Validate user input.
    if not isinstance(data_usage, Decimal) or not data_usage.is_finite() or data_usage < 0:
        raise ValueError("Data usage must be a non-negative Decimal.")

    if not isinstance(call_usage, int) or isinstance(call_usage, bool) or call_usage < 0:
        raise ValueError("Call minutes must be a non-negative integer.")

    if not isinstance(sms_usage, int) or isinstance(sms_usage, bool) or sms_usage < 0:
        raise ValueError("SMS usage must be a non-negative integer.")

    if not isinstance(required_validity, int) or isinstance(required_validity, bool) or required_validity <= 0:
        raise ValueError("Required validity must be a positive integer.")

    budget = Decimal(str(budget))
    if not budget.is_finite() or budget < 0:
        raise ValueError("Budget must be a non-negative amount.")

    results = []

    for plan in PLANS:
        result = evaluate_plan(
            plan, data_usage, call_usage, sms_usage,
            required_validity, budget
        )

        if result is not None:
            results.append(result)

    # A plan is eligible only if the final cost is within budget.
    eligible = [
        result for result in results
        if result["within_budget"]
    ]

    print("\n========== PLAN COMPARISON ==========")

    if not results:
        print("No plans meet the validity and base-price constraints.")
        return None

    for result in results:
        status = (
            "ELIGIBLE" if result["within_budget"]
            else "EXCEEDS BUDGET"
        )

        print(f"\nPlan: {result['name']} [{status}]")
        print(f"Base price       : Rs. {result['base_price']:.2f}")
        print(f"Validity         : {result['validity']} days")
        print(f"Excess data      : {result['excess_data_gb']} GB")
        print(f"Excess call mins : {result['excess_calls']}")
        print(f"Excess SMS       : {result['excess_sms']}")
        print(f"Data excess cost : Rs. {result['data_charge']:.2f}")
        print(f"Call excess cost : Rs. {result['call_charge']:.2f}")
        print(f"SMS excess cost  : Rs. {result['sms_charge']:.2f}")
        print(f"Total excess cost: Rs. {result['excess_total']:.2f}")
        print(f"Total cost       : Rs. {result['total_cost']:.2f}")

    print("\n========== OPTIMAL PLAN ==========")

    if not eligible:
        print("No plan satisfies all constraints, including total budget.")
        return None

    # Lowest total cost; base price breaks ties.
    best = min(
        eligible,
        key=lambda result: (
            result["total_cost"],
            result["base_price"]
        )
    )

    print(f"Recommended plan : {best['name']}")
    print(f"Total cost       : Rs. {best['total_cost']:.2f}")
    print(f"Budget           : Rs. {money(budget):.2f}")
    print(f"Remaining budget : Rs. {money(budget - best['total_cost']):.2f}")

    return best


if __name__ == "__main__":
    try:
        print("MOBILE PLAN COST OPTIMIZER")

        data_usage = Decimal(input("Expected data usage (GB): "))
        call_usage = int(input("Expected call minutes: "))
        sms_usage = int(input("Expected SMS count: "))
        required_validity = int(input("Minimum validity (days): "))
        budget = Decimal(input("Maximum total budget (Rs.): "))

        optimize_plans(
            data_usage,
            call_usage,
            sms_usage,
            required_validity,
            budget
        )

    except (ValueError, TypeError) as error:
        print("Input error:", error)
