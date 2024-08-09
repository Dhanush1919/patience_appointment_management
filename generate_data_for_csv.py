import csv
import random
from faker import Faker

# Initialize the Faker object
fake = Faker()

# Sample data to choose from
doctors = [
    "Robert Franco", "Christopher Flores", "Cynthia Gamble",
    "Adam Boyer", "Patty Green", "Evan McCarthy", "Sophia Reese",
    "John Clarkson", "Megan Grey", "Sara Hendricks"
]

departments = [
    "Cardiology", "Neurology", "Pediatrics", "Dermatology",
    "Orthopedics", "Oncology", "Urology", "Gastroenterology",
    "Ophthalmology", "Radiology"
]

statuses = ["Completed", "Cancelled", "Scheduled", "No Show"]

# Function to generate a unique Appointment ID
def generate_appointment_id(start_id, count):
    return [f"A{str(i).zfill(4)}" for i in range(start_id, start_id + count)]

# Generate 100 records
appointment_ids = generate_appointment_id(1001, 100)
data = []

for appointment_id in appointment_ids:
    record = [
        appointment_id,
        fake.name(),  # Random patient name
        fake.date_this_decade(),  # Random appointment date within the last decade
        fake.time(),  # Random appointment time
        random.choice(doctors),  # Random doctor
        random.choice(departments),  # Random department
        random.choice(statuses)  # Random status
    ]
    data.append(record)

# Write the data to a CSV file
with open("appointments.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Appointment_ID", "Patient_Name", "Appointment_Date", "Appointment_Time", "Doctor", "Department", "Status"])
    writer.writerows(data)

print("CSV file 'appointments.csv' with 100 records has been generated.")
