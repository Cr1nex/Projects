import mariadb
my_connection = mariadb.connect(host="localhost",user="root",password="",database="hospital_management",port=3306)
my_cursor = my_connection.cursor()
"""find the city of the employees in the IT department ."""


my_cursor.execute("""
CREATE TABLE IF NOT EXISTS Doctor(
                  dr_code INT PRIMARY KEY,
                  Name VARCHAR(50),
                  Fname VARCHAR(50),
                  Gender CHAR(1),
                  Address VARCHAR(255),
                  designation VARCHAR(50)
                  );
                    """)


my_cursor.execute("""
CREATE TABLE IF NOT EXISTS Staff(
                  staff_id INT PRIMARY KEY,
                  dr_code INT,
                  Gender CHAR(1),
                  Address VARCHAR(255),
                  Cel VARCHAR(20),
                  Name VARCHAR(50),
                  Dept VARCHAR(50),
                  FOREIGN KEY (dr_code)
                  REFERENCES Doctor(dr_code)
                  );
                    """)

my_cursor.execute("""
CREATE TABLE IF NOT EXISTS Patient(
                  pat_id INT PRIMARY KEY,
                  Name VARCHAR(50),
                  Fname VARCHAR(50),
                  Gender CHAR(1),
                  Address VARCHAR(255),
                  Tel VARCHAR(20),
                  dr_code INT,
                  FOREIGN KEY (dr_code)
                  REFERENCES Doctor(dr_code)
                  );
                    """)

my_cursor.execute("""
CREATE TABLE IF NOT EXISTS Patientdiagnosis(
                  DiagNo INT PRIMARY KEY,
                  Diagdetails VARCHAR(255),
                  Remark VARCHAR(255),
                  Diagdate DATE,
                  Other VARCHAR(255),
                  pat_id INT,
                  FOREIGN KEY (pat_id)
                  REFERENCES Patient(pat_id)
                  );
                    """)


my_cursor.execute("""
CREATE TABLE IF NOT EXISTS Bill(
                  Billno INT PRIMARY KEY,
                  Patname VARCHAR(50),
                  Drname VARCHAR(50),
                  Datetime DATE,
                  Amount DECIMAL(10, 2),
                  pat_id INT,
                  FOREIGN KEY (pat_id)
                  REFERENCES Patient(pat_id)
                  );
                    """)


print("Tables created succesfully")



doctors = [
    (1, "John", "Doe", "M", "123 Elm St", "Cardiologist"),
    (2, "Jane", "Smith", "F", "456 Oak St", "Pediatrician"),
    (3, "Emily", "Clark", "F", "789 Maple Ave", "Orthopedic"),
    (4, "Michael", "Brown", "M", "101 Pine Rd", "Neurologist"),
    (5, "Sarah", "Davis", "F", "202 Cedar Blvd", "Dermatologist")
]

my_cursor.executemany("INSERT INTO Doctor VALUES (?, ?, ?, ?, ?, ?)", doctors)


patients = [
    (1, "Alice", "Taylor", "F", "55 Lake View", "1234567890", 1),
    (2, "Bob", "Miller", "M", "98 Hilltop Lane", "1234567891", 2),
    (3, "Charlie", "Anderson", "M", "22 Meadow Dr", "1234567892", 3),
    (4, "Diana", "Thomas", "F", "33 Valley Rd", "1234567893", 4),
    (5, "Edward", "Jones", "M", "44 Sunset Ave", "1234567894", 5),
    (6, "Fiona", "White", "F", "11 Sunshine St", "1234567895", 1),
    (7, "George", "Brown", "M", "77 Starlight Blvd", "1234567896", 2),
    (8, "Hannah", "Harris", "F", "66 Greenway", "1234567897", 3),
    (9, "Ian", "Clarkson", "M", "88 Birchwood Dr", "1234567898", 4),
    (10, "Jackie", "Stewart", "F", "99 Riverbend", "1234567899", 5)
]

my_cursor.executemany("INSERT INTO Patient VALUES (?, ?, ?, ?, ?, ?, ?)", patients)


diagnoses = [
    (1, "Flu", "Recovering", "2024-01-15", "Take Rest", 1),
    (2, "Fracture", "Under Treatment", "2024-02-10", "Apply cast", 2),
    (3, "Migraine", "Severe", "2024-03-05", "Prescribed meds", 3),
    (4, "Allergy", "Mild", "2024-04-20", "Avoid allergen", 4),
    (5, "Diabetes", "Chronic", "2024-05-30", "Monitor sugar", 5),
    (6, "Flu", "Recovering", "2024-01-16", "Take Rest", 6),
    (7, "Fracture", "Under Treatment", "2024-02-11", "Apply cast", 7),
    (8, "Migraine", "Severe", "2024-03-06", "Prescribed meds", 8),
    (9, "Allergy", "Mild", "2024-04-21", "Avoid allergen", 9),
    (10, "Diabetes", "Chronic", "2024-05-31", "Monitor sugar", 10)
]

my_cursor.executemany("INSERT INTO Patientdiagnosis VALUES (?, ?, ?, ?, ?, ?)", diagnoses)


bills = [
    (1, "Alice Taylor", "John Doe", "2024-01-16", 500.00, 1),
    (2, "Bob Miller", "Jane Smith", "2024-02-12", 1200.50, 2),
    (3, "Charlie Anderson", "Emily Clark", "2024-03-07", 750.75, 3),
    (4, "Diana Thomas", "Michael Brown", "2024-04-22", 300.00, 4),
    (5, "Edward Jones", "Sarah Davis", "2024-05-01", 900.20, 5)
]

my_cursor.executemany("INSERT INTO Bill VALUES (?, ?, ?, ?, ?, ?)", bills)

staff = [
    (1, 1, "F", "123 Tech St", "9876543210", "Nancy Wilson", "IT"),
    (2, 2, "M", "456 Care Rd", "9876543211", "Peter Carter", "Nursing"),
    (3, 3, "M", "789 Admin St", "9876543212", "Steve Adams", "Administration"),
    (4, 4, "F", "101 Innovation Blvd", "9876543213", "Laura Lee", "IT"),
    (5, 5, "M", "202 Maintenance Ln", "9876543214", "Paul Grant", "Maintenance")
]

my_cursor.executemany("INSERT INTO Staff VALUES (?, ?, ?, ?, ?, ?, ?)", staff)

my_cursor.execute("""
                SELECT d.Name AS Doctor_Name, p.Name AS Patient_Name
                FROM Doctor d LEFT JOIN Patient p ON d.dr_code = p.dr_code
""")



for row in my_cursor:
    print(f"Doctor: {row[0]}, Patient: {row[1]}")



my_cursor.execute("""
                SELECT p.Name AS Patient_Name, d.Name AS Doctor_Name, SUM(b.Amount) AS Total_Debt
                FROM Patient p
                JOIN Doctor d ON p.dr_code = d.dr_code
                JOIN Bill b ON p.pat_id = b.pat_id
                WHERE b.Amount > 100
                GROUP BY p.pat_id, d.Name
""")



for row in my_cursor:
    print(f"Patient: {row[0]}, Doctor: {row[1]}, Total Debt: {row[2]}")


my_cursor.execute("""
                SELECT d.Name AS Doctor_Name, COUNT(p.pat_id) AS Total_Patients
                FROM Doctor d
                LEFT JOIN Patient p ON d.dr_code = p.dr_code
                GROUP BY d.dr_code
""")



for row in my_cursor:
    print(f"Doctor: {row[0]}, Total Patients: {row[1]}")


my_connection.close()



























