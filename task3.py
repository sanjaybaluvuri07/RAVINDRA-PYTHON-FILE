
from decimal import Decimal, ROUND_HALF_UP

# Illustrative payment policy
SENIOR_AGE = 60
SENIOR_DISCOUNT = Decimal("0.10")
LOW_INCOME_DISCOUNT = Decimal("0.20")
STAFF_DISCOUNT = Decimal("0.15")
MAX_DISCOUNT = Decimal("0.20")


def money(amount):
    return Decimal(str(amount)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )


def classify_patient(age, low_income, staff):
    if low_income:
        return "Low-Income Patient"
    elif age >= SENIOR_AGE:
        return "Senior Citizen"
    elif staff:
        return "Staff Patient"
    else:
        return "General Patient"


def calculate_billing(consultation, diagnostic, treatment,
                      age, low_income, staff):

    # Validate charges
    charges = [consultation, diagnostic, treatment]

    if any(charge < 0 for charge in charges):
        raise ValueError("Charges cannot be negative.")

    if not any(charge > 0 for charge in charges):
        raise ValueError("At least one charge must be positive.")

    if not isinstance(age, int) or isinstance(age, bool) or not 0 <= age <= 120:
        raise ValueError("Age must be an integer between 0 and 120.")

    if not all(isinstance(flag, bool)
               for flag in (low_income, staff)):
        raise ValueError("Eligibility flags must be True or False.")

    # Calculate gross bill
    gross_bill = money(
        consultation + diagnostic + treatment
    )

    # Determine eligible concessions
    eligible_discounts = []

    if age >= SENIOR_AGE:
        eligible_discounts.append(
            ("Senior Citizen", SENIOR_DISCOUNT)
        )

    if low_income:
        eligible_discounts.append(
            ("Low-Income", LOW_INCOME_DISCOUNT)
        )

    if staff:
        eligible_discounts.append(
            ("Staff", STAFF_DISCOUNT)
        )

    # Apply the highest eligible concession
    if eligible_discounts:
        concession_name, discount_rate = max(
            eligible_discounts, key=lambda item: item[1]
        )
    else:
        concession_name = "None"
        discount_rate = Decimal("0.00")

    discount_rate = min(discount_rate, MAX_DISCOUNT)
    discount_amount = money(gross_bill * discount_rate)
    net_bill = money(gross_bill - discount_amount)

    # Classify patient
    category = classify_patient(age, low_income, staff)

    # Display bill
    print("\n========== HOSPITAL BILL ==========")
    print(f"Consultation Charges : Rs. {money(consultation):.2f}")
    print(f"Diagnostic Charges   : Rs. {money(diagnostic):.2f}")
    print(f"Treatment Charges    : Rs. {money(treatment):.2f}")
    print("-----------------------------------")
    print(f"Gross Bill           : Rs. {gross_bill:.2f}")
    print(f"Patient Classification: {category}")
    print(f"Concession Applied   : {concession_name}")
    print(f"Discount Rate        : {discount_rate * 100}%")
    print(f"Discount Amount      : Rs. {discount_amount:.2f}")
    print(f"Final Payable        : Rs. {net_bill:.2f}")
    print("===================================")

    return {
        "gross_bill": gross_bill,
        "classification": category,
        "discount": discount_amount,
        "net_bill": net_bill,
    }


# Main program
if __name__ == "__main__":
    try:
        print("HOSPITAL BILLING SYSTEM")

        consultation = Decimal(input("Enter consultation charges: "))
        diagnostic = Decimal(input("Enter diagnostic charges: "))
        treatment = Decimal(input("Enter treatment charges: "))

        age = int(input("Enter patient age: "))

        low_income_input = input(
            "Is the patient verified as low-income? (yes/no): "
        ).strip().lower()

        staff_input = input(
            "Is the patient a verified staff member? (yes/no): "
        ).strip().lower()

        if low_income_input not in ("yes", "no"):
            raise ValueError("Enter yes or no for low-income status.")

        if staff_input not in ("yes", "no"):
            raise ValueError("Enter yes or no for staff status.")

        calculate_billing(
            consultation,
            diagnostic,
            treatment,
            age,
            low_income_input == "yes",
            staff_input == "yes"
        )

    except (ValueError, TypeError) as error:
        print("Billing Error:", error)
