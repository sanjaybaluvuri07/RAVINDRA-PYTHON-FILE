
def simulate_water_tank(
    capacity,
    initial_water,
    inflows,
    outflows,
    threshold
):
    # Validate inputs
    if capacity <= 0:
        raise ValueError("Tank capacity must be positive.")

    if not 0 <= initial_water <= capacity:
        raise ValueError(
            "Initial water must be between 0 and capacity."
        )

    if not 0 <= threshold <= capacity:
        raise ValueError(
            "Threshold must be between 0 and tank capacity."
        )

    if len(inflows) != len(outflows):
        raise ValueError(
            "Inflow and outflow lists must have equal lengths."
        )

    if any(x < 0 for x in inflows + outflows):
        raise ValueError(
            "Inflow and outflow quantities cannot be negative."
        )

    water = initial_water
    first_threshold_interval = (
        0 if water >= threshold else None
    )
    overflow_total = 0
    shortage_total = 0
    results = []

    print("\n========== WATER TANK SIMULATION ==========")
    print(f"Tank capacity : {capacity} liters")
    print(f"Initial water : {initial_water} liters")
    print(f"Target threshold: {threshold} liters")

    for day, (inflow, outflow) in enumerate(
        zip(inflows, outflows), start=1
    ):
        previous_water = water

        # Calculate water before applying physical tank limits
        raw_water = previous_water + inflow - outflow

        # Detect overflow and shortage
        overflow = max(0, raw_water - capacity)
        shortage = max(0, -raw_water)

        # Actual stored water cannot exceed capacity or fall below zero
        water = min(capacity, max(0, raw_water))

        overflow_total += overflow
        shortage_total += shortage

        # Record the first interval whose ending level reaches threshold
        if (
            first_threshold_interval is None
            and water >= threshold
        ):
            first_threshold_interval = day

        if overflow > 0:
            status = "OVERFLOW"
        elif shortage > 0:
            status = "SHORTAGE"
        else:
            status = "NORMAL"

        results.append({
            "day": day,
            "inflow": inflow,
            "outflow": outflow,
            "water": water,
            "overflow": overflow,
            "shortage": shortage,
            "status": status
        })

        print(f"\nDay {day}")
        print(f"Starting water : {previous_water} L")
        print(f"Inflow         : {inflow} L")
        print(f"Outflow        : {outflow} L")
        print(f"Ending water   : {water} L")
        print(f"Overflow       : {overflow} L")
        print(f"Shortage       : {shortage} L")
        print(f"Status         : {status}")

    print("\n========== SIMULATION SUMMARY ==========")
    print(f"Final water level : {water} L")
    print(f"Total overflow    : {overflow_total} L")
    print(f"Total shortage    : {shortage_total} L")

    if first_threshold_interval is not None:
        if first_threshold_interval == 0:
            print("Threshold already reached at the start.")
        else:
            print(
                "First threshold reached at day:",
                first_threshold_interval
            )
    else:
        print("Threshold was never reached.")

    return {
        "final_water": water,
        "total_overflow": overflow_total,
        "total_shortage": shortage_total,
        "first_threshold_interval": first_threshold_interval,
        "daily_results": results
    }


def main():
    print("MULTI-DAY WATER TANK SIMULATION")

    try:
        capacity = float(input("Tank capacity (liters): "))
        initial_water = float(input("Initial water level (liters): "))
        threshold = float(input("Target water threshold (liters): "))

        days = int(input("Number of days: "))

        if days <= 0:
            raise ValueError("Number of days must be positive.")

        inflows = []
        outflows = []

        for day in range(1, days + 1):
            print(f"\nDay {day} inputs")
            inflow = float(input("Water inflow (liters): "))
            outflow = float(input("Water outflow (liters): "))

            inflows.append(inflow)
            outflows.append(outflow)

        simulate_water_tank(
            capacity,
            initial_water,
            inflows,
            outflows,
            threshold
        )

    except ValueError as error:
        print("Input error:", error)


if __name__ == "__main__":
    main()
