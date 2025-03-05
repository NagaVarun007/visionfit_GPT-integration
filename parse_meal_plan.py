import json
import pandas as pd

# Load meal plan
with open("meal_plan.json", "r") as f:
    meal_plan = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(meal_plan)

# Save as CSV for easy readability
df.to_csv("meal_plan.csv", index=False)

print("Meal plan saved to meal_plan.csv!")
