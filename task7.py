
def reconcile_inventory(products):
    results = []

    print("\n========== INVENTORY RECONCILIATION ==========")

    for product in products:
        name = product["name"]
        opening = product["opening"]
        incoming = product["incoming"]
        dispatched = product["dispatched"]
        closing = product["closing"]
        minimum_stock = product["minimum_stock"]

        # Validate inventory quantities
        quantities = [
            opening, incoming, dispatched, closing, minimum_stock
        ]

        if any(not isinstance(q, int) or isinstance(q, bool)
               or q < 0 for q in quantities):
            raise ValueError(
                f"Invalid quantity for product: {name}"
            )

        if dispatched > opening + incoming:
            raise ValueError(
                f"Dispatched quantity exceeds available stock for {name}"
            )

        # Calculate expected closing stock
        expected_closing = opening + incoming - dispatched

        # Compare expected and actual closing stock
        discrepancy = closing - expected_closing

        if discrepancy == 0:
            status = "MATCHED"
        elif discrepancy > 0:
            status = "EXCESS STOCK"
        else:
            status = "STOCK SHORTAGE"

        # Replenishment based on actual closing stock
        replenishment = max(0, minimum_stock - closing)

        results.append({
            "name": name,
            "opening": opening,
            "incoming": incoming,
            "dispatched": dispatched,
            "expected_closing": expected_closing,
            "actual_closing": closing,
            "discrepancy": discrepancy,
            "status": status,
            "minimum_stock": minimum_stock,
            "replenishment": replenishment
        })

        print(f"\nProduct: {name}")
        print(f"Opening stock       : {opening}")
        print(f"Incoming quantity   : {incoming}")
        print(f"Dispatched quantity : {dispatched}")
        print(f"Expected closing    : {expected_closing}")
        print(f"Actual closing      : {closing}")
        print(f"Discrepancy         : {discrepancy}")
        print(f"Reconciliation      : {status}")
        print(f"Minimum stock level : {minimum_stock}")
        print(f"Replenishment needed: {replenishment}")

    # Summary
    matched = sum(r["status"] == "MATCHED" for r in results)
    excess = sum(r["status"] == "EXCESS STOCK" for r in results)
    shortage = sum(r["status"] == "STOCK SHORTAGE" for r in results)
    total_replenishment = sum(r["replenishment"] for r in results)

    print("\n========== SUMMARY ==========")
    print(f"Products checked       : {len(results)}")
    print(f"Matched products       : {matched}")
    print(f"Excess stock products  : {excess}")
    print(f"Shortage products      : {shortage}")
    print(f"Total replenishment    : {total_replenishment} units")

    return results


def main():
    print("WAREHOUSE INVENTORY RECONCILIATION")

    products = []

    try:
        count = int(input("Enter number of products: "))

        if count <= 0:
            raise ValueError("Number of products must be positive.")

        for i in range(count):
            print(f"\nEnter details for product {i + 1}")

            name = input("Product name: ").strip()
            if not name:
                raise ValueError("Product name cannot be empty.")

            opening = int(input("Opening stock: "))
            incoming = int(input("Incoming quantity: "))
            dispatched = int(input("Dispatched quantity: "))
            closing = int(input("Actual closing stock: "))
            minimum_stock = int(input("Minimum stock level: "))

            products.append({
                "name": name,
                "opening": opening,
                "incoming": incoming,
                "dispatched": dispatched,
                "closing": closing,
                "minimum_stock": minimum_stock
            })

        reconcile_inventory(products)

    except ValueError as error:
        print("Input error:", error)


if __name__ == "__main__":
    main()
