
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

# Illustrative ATM rules
MAX_WITHDRAWAL = Decimal("10000.00")
MIN_BALANCE = Decimal("0.00")
DAILY_WITHDRAWAL_LIMIT = Decimal("20000.00")

CENT = Decimal("0.01")


def money(amount):
    return Decimal(str(amount)).quantize(
        CENT, rounding=ROUND_HALF_UP
    )


def process_transactions(initial_balance, transactions):
    balance = money(initial_balance)
    daily_withdrawn = Decimal("0.00")

    if balance < 0:
        raise ValueError("Initial balance cannot be negative.")

    transaction_log = []

    for number, transaction in enumerate(transactions, start=1):
        transaction_type = transaction.get("type", "").lower()
        amount = transaction.get("amount")

        status = "REJECTED"
        message = ""

        # Validate transaction amount
        try:
            amount = Decimal(str(amount))

            if not amount.is_finite() or amount <= 0:
                raise ValueError("Amount must be positive and finite.")

            amount = money(amount)

            if amount <= 0:
                raise ValueError("Amount must be at least Rs. 0.01.")

        except (InvalidOperation, ValueError, TypeError):
            transaction_log.append({
                "number": number,
                "type": transaction_type.upper() or "UNKNOWN",
                "amount": str(transaction.get("amount")),
                "status": status,
                "balance": balance,
                "message": "Invalid transaction amount."
            })
            continue

        if transaction_type == "deposit":
            balance = money(balance + amount)
            status = "SUCCESS"
            message = "Deposit completed."

        elif transaction_type == "withdraw":
            if amount > MAX_WITHDRAWAL:
                message = "Exceeds per-transaction withdrawal limit."

            elif daily_withdrawn + amount > DAILY_WITHDRAWAL_LIMIT:
                message = "Exceeds daily withdrawal limit."

            elif amount > balance:
                message = "Insufficient funds."

            else:
                balance = money(balance - amount)
                daily_withdrawn = money(daily_withdrawn + amount)
                status = "SUCCESS"
                message = "Withdrawal completed."

        else:
            message = "Unknown transaction type."

        transaction_log.append({
            "number": number,
            "type": transaction_type.upper() or "UNKNOWN",
            "amount": amount,
            "status": status,
            "balance": balance,
            "message": message
        })

    return {
        "initial_balance": money(initial_balance),
        "final_balance": balance,
        "total_deposits": money(sum(
            (t["amount"] for t in transaction_log
             if t["status"] == "SUCCESS"
             and t["type"] == "DEPOSIT"),
            Decimal("0.00")
        )),
        "total_withdrawals": money(sum(
            (t["amount"] for t in transaction_log
             if t["status"] == "SUCCESS"
             and t["type"] == "WITHDRAW"),
            Decimal("0.00")
        )),
        "successful": sum(
            t["status"] == "SUCCESS" for t in transaction_log
        ),
        "rejected": sum(
            t["status"] == "REJECTED" for t in transaction_log
        ),
        "transactions": transaction_log
    }


def main():
    print("ATM TRANSACTION SIMULATION")

    try:
        initial_balance = Decimal(
            input("Enter initial account balance (Rs.): ")
        )

        if not initial_balance.is_finite() or initial_balance < 0:
            raise ValueError("Initial balance must be non-negative.")

        count = int(input("Number of transactions: "))

        if count < 0:
            raise ValueError("Transaction count cannot be negative.")

        transactions = []

        for i in range(count):
            print(f"\nTransaction {i + 1}")
            transaction_type = input(
                "Type (deposit/withdraw): "
            ).strip().lower()

            amount = input("Amount (Rs.): ").strip()

            transactions.append({
                "type": transaction_type,
                "amount": amount
            })

        result = process_transactions(
            initial_balance, transactions
        )

        print("\n========== TRANSACTION HISTORY ==========")

        for t in result["transactions"]:
            print(f"\nTransaction #{t['number']}")
            print(f"Type    : {t['type']}")
            print(f"Amount  : Rs. {t['amount']}")
            print(f"Status  : {t['status']}")
            print(f"Balance : Rs. {t['balance']:.2f}")
            print(f"Message : {t['message']}")

        print("\n========== ACCOUNT SUMMARY ==========")
        print(
            f"Initial balance : Rs. "
            f"{result['initial_balance']:.2f}"
        )
        print(
            f"Total deposits  : Rs. "
            f"{result['total_deposits']:.2f}"
        )
        print(
            f"Total withdrawals: Rs. "
            f"{result['total_withdrawals']:.2f}"
        )
        print(
            f"Successful transactions: {result['successful']}"
        )
        print(
            f"Rejected transactions  : {result['rejected']}"
        )
        print(
            f"Final balance   : Rs. "
            f"{result['final_balance']:.2f}"
        )

    except (ValueError, InvalidOperation) as error:
        print("Input error:", error)


if __name__ == "__main__":
    main()
