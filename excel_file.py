import csv

# Read and process the results
with open(r"Data/RESULT.txt", 'r') as file:
    lines = file.readlines()

# Clean up the data
cleaned_data = []
for line in lines:
    parts = line.split(',')
    parts = [part.strip(': ').strip() for part in parts]
    if len(parts) >= 7:  # Ensure there are enough parts to process
        cleaned_data.append(parts)

# Extract unique subject codes
unique_subject_codes = set()
for parts in cleaned_data:
    subject_code = parts[2]
    unique_subject_codes.add(subject_code)

# Define the subject credits dynamically
subject_credits = {code: 3 for code in unique_subject_codes}  # Default credit value

# Update specific subject credits if known
subject_credits.update({
    "21CS61": 3, "21CS62": 4, "21IS63": 3, "21ISL66": 1, "21ISMP67": 2, "21INT68": 3,
    "21IM652": 3, "21CS644": 3, "21IS643": 3
})

subject_codes = list(subject_credits.keys())

# Create a dictionary to hold the student data
students = {}

for parts in cleaned_data:
    name = parts[0]
    usn = parts[1]
    subject_code = parts[2]
    internal_marks = parts[4]
    external_marks = parts[5]
    total_marks = parts[6]
    
    if usn not in students:
        students[usn] = {"name": name, "subjects": {}}
    
    students[usn]["subjects"][subject_code] = (internal_marks, external_marks, total_marks)

# Create the header row
header = ["Student Name", "Student USN", "Section"]
subject_header = ["", "", ""]

for code in subject_codes:
    subject_header.extend([code, "", "", ""])
    header.extend(["IA-Marks", "Externals", "Total", "Class"])

header.append("GPA")
subject_header.append("")

# Function to check if a string is a valid integer
def is_valid_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

# Function to calculate grade points
def calculate_grade_point(marks):
    if not is_valid_int(marks):
        return 0
    marks = int(marks)
    if marks >= 90 and marks <= 100:
        return 10
    elif marks >= 80 and marks < 90:
        return 9
    elif marks >= 70 and marks < 80:
        return 8
    elif marks >= 60 and marks < 70:
        return 7
    elif marks >= 50 and marks < 60:
        return 6
    elif marks >= 45 and marks < 50:
        return 5
    elif marks >= 40 and marks < 45:
        return 4
    else:
        return 0

# Function to determine the class based on total marks
def determine_class(total_marks):
    if not is_valid_int(total_marks):
        return "FAIL"
    total_marks = int(total_marks)
    if total_marks < 40:
        return "FAIL"
    elif total_marks < 50:
        return "P SC"
    elif total_marks < 60:
        return "SC"
    elif total_marks < 70:
        return "FC"
    else:
        return "FCD"

# Write the data to a CSV file
with open(r"Data/Marks.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(subject_header)
    writer.writerow(header)
    
    for usn, data in students.items():
        row = [data["name"], usn, "A"]  # Assuming section "A" for all
        total_grade_points = 0
        total_credits = 0
        
        for code in subject_codes:
            if code in data["subjects"]:
                internal, external, total = data["subjects"][code]
                row.extend([internal, external, total])
                grade_point = calculate_grade_point(total)
                total_grade_points += grade_point * subject_credits[code]
                total_credits += subject_credits[code]
                class_result = determine_class(total)
                row.append(class_result)
            else:
                row.extend(["", "", "", ""])
        
        gpa = round(total_grade_points / total_credits, 2) if total_credits > 0 else 0
        row.append(gpa)
        writer.writerow(row)