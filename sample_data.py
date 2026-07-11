# Creates sample data files for TailorTrack

# ── customers.txt ──
customers = [
    "C001|Ahmed Ali|0321-4567890|42|36|44",
    "C002|Sara Khan|0312-9876543|34|28|38",
    "C003|Bilal Raza|0333-1122334|40|34|46",
    "C004|Ayesha Noor|0345-5566778|36|30|40",
    "C005|Usman Tariq|0301-9988776|44|38|48",
]

# ── orders.txt ──
orders = [
    "O001|C001|Shalwar Kameez|20/06/2025|Delivered|1500",
    "O002|C002|Bridal Lehnga|25/06/2025|In Progress|5000",
    "O003|C003|Waistcoat|22/06/2025|Ready|800",
    "O004|C004|Suit|30/06/2025|Pending|2000",
    "O005|C005|Kurta Pajama|28/06/2025|In Progress|1000",
]

# ── payments.txt ──
payments = [
    "P001|O001|3000|3000|0|Paid",
    "P002|O002|15000|5000|10000|Unpaid",
    "P003|O003|2500|2500|0|Paid",
    "P004|O004|8000|2000|6000|Unpaid",
    "P005|O005|3500|1000|2500|Unpaid",
]

def write_file(filename, lines):
    f = open(filename, "w")
    for line in lines:
        f.write(line + "\n")
    f.close()
    print("Created:", filename)

write_file("customers.txt", customers)
write_file("orders.txt",    orders)
write_file("payments.txt",  payments)

print("\nSample data created successfully!")
print("Customers : 5")
print("Orders    : 5")
print("Payments  : 5")
print("\nYou can now run tailortrack_v2.py or the CLI notebook.")
