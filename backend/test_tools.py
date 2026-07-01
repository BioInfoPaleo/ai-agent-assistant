import pandas as pd
df = pd.read_csv("bioprocess_data.csv")

def calculate_average(column):
    return df [column].mean()

print("Average yield:", calculate_average("yield_g_per_l"))
print("Average temp:", calculate_average("temperature_c"))
