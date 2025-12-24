from functions import verify_user, calculate_tax, save_to_csv, read_from_csv
import pandas as pd
import os

FILENAME = "tax_records.csv"

print("===== MALAYSIAN TAX INPUT PROGRAM =====")

# ------------------------------
# REGISTRATION / LOGIN
# ------------------------------

registered_users = {}  # store ID + IC

while True:
    print("\n1. Register")
    print("2. Login")
    print("3. View Tax Records")
    print("4. Exit")
    print("5. Delete Tax Record")

    choice = input("Choose an option: ")

    # ---------------- REGISTER ----------------
    if choice == "1":
        user_id = input("Enter your User ID: ")
        ic = input("Enter your IC number (12 digits): ")

        if len(ic) != 12:
            print("IC must be exactly 12 digits!")
            continue

        registered_users[user_id] = ic
        print("Registration successful! Please login.")

    # ---------------- LOGIN ----------------
    elif choice == "2":
        user_id = input("Enter your User ID: ")
        password = input("Enter password (last 4 digits of IC): ")

        if user_id not in registered_users:
            print("User not registered.")
            continue

        ic = registered_users[user_id]

        if verify_user(ic, password):
            print("\nLogin successful!")

            income = float(input("Enter your annual income (RM): "))

            print("\n--- TAX RELIEF SECTION ---")
            ind_relief = 9000
            spouse_relief = int(input("Spouse? (0 = No, 1 = Yes): ")) * 4000
            child_count = int(input("Number of children (max 12): "))
            child_relief = min(child_count, 12) * 8000
            medical = float(input("Medical expenses (max 8000): "))
            lifestyle = float(input("Lifestyle expenses (max 2500): "))
            education = float(input("Education fees (max 7000): "))
            parent = float(input("Parental care (max 5000): "))

            total_relief = (
                ind_relief +
                spouse_relief +
                child_relief +
                min(medical, 8000) +
                min(lifestyle, 2500) +
                min(education, 7000) +
                min(parent, 5000)
            )

            tax_payable = calculate_tax(income, total_relief)

            print(f"\nTotal Relief: RM {total_relief}")
            print(f"Tax Payable: RM {tax_payable}")

            save_to_csv({
                "User ID": user_id,
                "IC": ic,
                "Income": income,
                "Tax Relief": total_relief,
                "Tax Payable": tax_payable
            }, FILENAME)

        else:
            print("Invalid login. Wrong password.")

    # ---------------- VIEW RECORDS ----------------
    elif choice == "3":
        df = read_from_csv(FILENAME)
        if df is None:
            print("No tax records found.")
        else:
            print("\n===== TAX RECORDS =====")
            print(df)

    # ---------------- EXIT ----------------
    elif choice == "4":
        print("Goodbye!")
        break

    # ---------------- DELETE TAX RECORD ----------------
    elif choice == "5":
        ic_to_delete = input("Enter IC of the record to delete: ")

        ic_to_delete = ic_to_delete.strip().replace('"', '').replace("'", "")

        df = read_from_csv(FILENAME)

        if df is None or df.empty:
            print("No tax records found.")

        else:
            df["IC"] = df["IC"].astype(str)

            if ic_to_delete not in df["IC"].values:
                print("IC not found in records.")
            else:
                df = df[df["IC"] != ic_to_delete]
                df.to_csv(FILENAME, index=False)
                print(f"Record with IC {ic_to_delete} deleted successfully.")

    # ---------------- INVALID OPTION ----------------
    else:
        print("Invalid option. Try again.")





