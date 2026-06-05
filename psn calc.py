import os

def calculate_psn_totals():
    filename = r"C:\Users\techb\Downloads\psn calc\psn_data.txt"
    
    # Check if the text file exists in the folder
    if not os.path.exists(filename):
        print("=" * 55)
        print(f" ERROR: '{filename}' not found!")
        print(" Please create a text file named 'psn_data.txt' in this folder")
        print(" and paste your transaction lines inside it.")
        print("=" * 55)
        return

    # Read data from file
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    gross_spending = 0.0
    refunds = 0.0
    wallet_funding = 0.0
    
    paid_item_count = 0
    free_item_count = 0

    for line in lines:
        line = line.strip()
        # Ensure the line has the expected PSN format layout
        if "AMOUNT" in line and "DESCRIPTION" in line:
            try:
                # Isolate the segment between AMOUNT and DESCRIPTION
                amount_section = line.split("AMOUNT")[1].split("DESCRIPTION")[0]
                description_section = line.split("DESCRIPTION")[1].strip().lower()

                # Clean the numerical string out of extra characters
                clean_price = (
                    amount_section.replace("$", "")
                    .replace("(", "")
                    .replace(")", "")
                    .replace("+", "")
                    .replace("-", "")
                    .strip()
                )
                price = float(clean_price)

                # Route data points into accurate transaction buckets
                if "wallet funding" in description_section or "+" in amount_section:
                    wallet_funding += price
                elif "refund" in description_section or "(" in amount_section:
                    refunds += price
                elif price == 0.0:
                    free_item_count += 1
                else:
                    gross_spending += price
                    paid_item_count += 1
            except (IndexError, ValueError):
                # Safely skip lines if corruption or unreadable symbols are hit
                continue

    net_spending = gross_spending - refunds

    # Avoid ZeroDivisionErrors by verifying counts before running division stats
    if paid_item_count > 0:
        avg_transaction = gross_spending / paid_item_count
    else:
        avg_transaction = 0.0

    # Print a clean, formatted terminal command board
    print("=" * 55)
    print("              FINAL PSN SPENDING REPORT            ")
    print("=" * 55)
    print(f" Total Paid Items Accounted : {paid_item_count}")
    print(f" Total Free Items Claimed   : {free_item_count}")
    print(f" Average Cost Per Paid Item : ${avg_transaction:.2f}")
    print("-" * 55)
    print(f" Gross Items Cost Subtotal  : ${gross_spending:.2f}")
    print(f" Total Deducted Refunds     : ${refunds:.2f}")
    print(f" NET WALLET CASH OUTFLOW    : ${net_spending:.2f}")
    print("-" * 55)
    print(f" Separate Wallet Top-Ups    : ${wallet_funding:.2f}")
    print("=" * 55)

if __name__ == "__main__":
    calculate_psn_totals()
    # Forces Windows terminal to stay open until manually dismissed
    input("\nExecution completed. Press Enter to close this window...")
