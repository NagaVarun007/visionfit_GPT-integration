import json
import pandas as pd

# Load meal plan
with open("meal_plan.json", "r") as f:
    meal_plan = json.load(f)

# Extract ingredients
ingredients_list = []
for meal in meal_plan:
    for i, ingredient in enumerate(meal["ingredients"]):
        ingredients_list.append({
            "ingredient": ingredient,
            "quantity": float(meal["ingredient_quantity"][i]),
            "cost": float(meal["ingredient_cost"][i]),
        })

# Create DataFrame
df = pd.DataFrame(ingredients_list)

# Summarize total quantities
shopping_list = df.groupby("ingredient").agg({"quantity": "sum", "cost": "sum"}).reset_index()

# Save shopping list
shopping_list.to_csv("shopping_list.csv", index=False)

print("Shopping list saved to shopping_list.csv!")
