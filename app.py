import pymysql


# 1. Database Connection
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="8419",
        database="PowerGrid",
        cursorclass=pymysql.cursors.DictCursor
    )


# 2. Function to Add a New Bill with Alphabet Validation
def add_bill():
    # Validation loop for name
    while True:
        name = input("Enter Customer Name: ")
        if name.isalpha():  # Condition: Only enter alphabets
            break
        print("Invalid input! Please enter alphabets only (no numbers or spaces).")

    meter = input("Enter Meter Number: ")
    units = int(input("Enter Units Consumed: "))
    total = units * 5

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO energy_bills (customer_name, meter_number, units_consumed, total_bill) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, meter, units, total))
            conn.commit()
            print(f"\nSuccessfully added bill for {name}!")
    finally:
        conn.close()


# 3. Function to Delete a Bill
def delete_bill():
    meter = input("Enter the Meter Number of the bill you want to delete: ")

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Check if meter exists first
            sql_check = "SELECT * FROM energy_bills WHERE meter_number = %s"
            cursor.execute(sql_check, (meter,))
            result = cursor.fetchone()

            if result:
                sql_delete = "DELETE FROM energy_bills WHERE meter_number = %s"
                cursor.execute(sql_delete, (meter,))
                conn.commit()
                print(f"\nBill with Meter Number {meter} has been deleted.")
            else:
                print("\nNo bill found with that Meter Number.")
    finally:
        conn.close()


# 4. Function to View All Bills
def view_bills():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM energy_bills")
            rows = cursor.fetchall()

            print("\n--- ENERGY BILLING DASHBOARD ---")
            print(f"{'Name':<15} {'Meter':<10} {'Units':<10} {'Amount':<10}")
            print("-" * 45)
            for row in rows:
                print(
                    f"{row['customer_name']:<15} {row['meter_number']:<10} {row['units_consumed']:<10} ₹{row['total_bill']:<10}")
    finally:
        conn.close()


# 5. Main Menu Loop
def main():
    while True:
        print("\n1. View All Bills")
        print("2. Add New Bill")
        print("3. Delete a Bill")  # Added new option
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            view_bills()
        elif choice == '2':
            add_bill()
        elif choice == '3':
            delete_bill()  # Call the delete function
        elif choice == '4':
            print("Exiting program...")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()