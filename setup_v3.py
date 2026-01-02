import sqlite3
import random
import os
import pandas as pd

# 1. CLEAN SLATE
db_file = 'hospital_v3.db'
if os.path.exists(db_file):
    os.remove(db_file)
    print(f"Deleted old {db_file}...")

conn = sqlite3.connect(db_file)
c = conn.cursor()

# 2. CREATE SCHEMA
c.execute("CREATE TABLE patients (patient_id INTEGER, dob TEXT, gender TEXT)")
c.execute("CREATE TABLE visits (visit_id INTEGER, patient_id INTEGER, visit_date TEXT, weight_raw TEXT, height_cm INTEGER, notes TEXT)")

# 3. GENERATE CHAOS
patients = []
visits = []
genders = ['M', 'F', 'Male', 'Female', 'm', 'f']

print("Injecting chaos...")
for i in range(1, 151):
    # DOB: Mixed formats (ISO vs US vs EU)
    year = random.randint(1950, 2005)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    
    if i % 3 == 0:
        dob = f"{year}-{month:02d}-{day:02d}"  # ISO
    elif i % 3 == 1:
        dob = f"{month}/{day}/{year}"          # US
    else:
        dob = f"{day}/{month}/{year}"          # EU

    patients.append((i, dob, random.choice(genders)))
    
    # Weight: Mixed Units (kg vs lbs)
    w_raw = random.randint(50, 110)
    # 30% chance of 'lbs', 30% chance of 'kg', 40% chance of no unit
    rand_w = random.random()
    if rand_w < 0.3:
        w_str = f"{int(w_raw * 2.204)} lbs"
    elif rand_w < 0.6:
        w_str = f"{w_raw}kg"
    else:
        w_str = str(w_raw)
    
    # Notes: PII Leak (The HIPAA Trap)
    # 100% of rows have this leak for this test
    note = f"Patient {i} - Follow-up required." 
    
    visits.append((i+1000, i, "2023-06-15", w_str, random.randint(150, 190), note))

c.executemany("INSERT INTO patients VALUES (?,?,?)", patients)
c.executemany("INSERT INTO visits VALUES (?,?,?,?,?,?)", visits)
conn.commit()

# 4. EXTRACT TO CSV (The "Staging" Step)
# We join the tables here so your CSV has all the dirty data in one place
query = """
SELECT 
    p.patient_id, p.dob, p.gender,
    v.weight_raw, v.height_cm, v.notes
FROM visits v 
LEFT JOIN patients p ON v.patient_id = p.patient_id
"""
df = pd.read_sql(query, conn)
df.to_csv('raw_extract.csv', index=False)

conn.close()

print("\nSetup Complete.")
print(f"1. Database: '{db_file}' (Source)")
print(f"2. Extract:  'raw_extract.csv' (Dirty Staging File)")
print(f"   - Rows: {len(df)}")
print("   - Contains PII? YES")
print("   - Contains Mixed Units? YES")