import pandas as pd
import numpy as np
import os
import random

def create_messy_data(num_rows=150):
    # Ensure directory exists
    os.makedirs("Test1", exist_ok=True)
    
    data = {
        'patient_id': range(1001, 1001 + num_rows),
        'gender': np.random.choice(['M', 'F', 'Male', 'female', 'm', 'F '], num_rows),
        'height_cm': np.random.randint(150, 200, num_rows),
        'notes': ['Routine checkup' for _ in range(num_rows)]
    }
    
    # 1. Create Mixed Date Formats
    # ~50% Day-First (e.g., 31/01/2020)
    # ~30% ISO (2020-01-31)
    # ~20% US/Other (01/31/2020)
    dates = []
    for _ in range(num_rows):
        y = random.randint(1950, 2000)
        m = random.randint(1, 12)
        d = random.randint(1, 28)
        
        r = random.random()
        if r < 0.5:
            dates.append(f"{d}/{m}/{y}")
        elif r < 0.8:
            dates.append(f"{y}-{m:02d}-{d:02d}")
        else:
            dates.append(f"{m}/{d}/{y}")
    data['dob'] = dates

    # 2. Create Mixed Weight Formats
    # Clean numbers, "kg" suffix, "lbs" suffix
    weights = []
    for _ in range(num_rows):
        base = random.randint(50, 100)
        r = random.random()
        if r < 0.6:
            weights.append(str(base))
        elif r < 0.8:
            weights.append(f"{base}kg")
        else:
            weights.append(f"{int(base*2.2)} lbs")
    data['weight_raw'] = weights

    df = pd.DataFrame(data)
    
    # Save CSV
    csv_path = os.path.join("Test1", "raw_extract.csv")
    df.to_csv(csv_path, index=False)
    print(f"Generated messy mock data at: {csv_path}")

if __name__ == "__main__":
    create_messy_data()
