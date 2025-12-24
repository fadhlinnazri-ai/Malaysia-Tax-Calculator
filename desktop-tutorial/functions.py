import pandas as pd
import os

# ------------------------------
# VERIFY USER
# ------------------------------
def verify_user(ic_number, password):
    """Check if IC has 12 digits and password matches last 4 digits."""
    
    # dictionary example (required)
    user_info = {
        "ic": ic_number,
        "password": password
    }

    if len(ic_number) == 12 and password == ic_number[-4:]:
        return True
    return False


# ------------------------------
# CALCULATE TAX
# ------------------------------
def calculate_tax(income, tax_relief):
    """Calculate Malaysian tax using simplified bracket."""

    chargeable_income = income - tax_relief
    if chargeable_income <= 0:
        return 0  # no tax if income becomes negative

    # list of tuples (required)
    tax_brackets = [
        (5000, 0.00),
        (20000, 0.01),
        (35000, 0.03),
        (50000, 0.06),
        (70000, 0.11),
        (100000, 0.19),
        (999999999, 0.24)
    ]

    tax = 0
    last_limit = 0

    # tuple unpacking (limit, rate)
    for limit, rate in tax_brackets:
        if chargeable_income > limit:
            tax += (limit - last_limit) * rate
            last_limit = limit
        else:
            tax += (chargeable_income - last_limit) * rate
            break

    return round(tax, 2)


# ------------------------------
# SAVE TO CSV
# ------------------------------
def save_to_csv(data, filename="tax_records.csv"):
    """Save or append data to CSV."""
    df = pd.DataFrame([data])  # list containing dictionary

    if not os.path.exists(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)


# ------------------------------
# READ FROM CSV
# ------------------------------
def read_from_csv(filename="tax_records.csv"):
    """Return DataFrame if CSV exists else None."""
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return None



