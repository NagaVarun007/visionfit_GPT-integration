import json
import yaml
import os
import openai

# Load API Key
with open('keys.yaml', 'r') as file:
    api_key = yaml.safe_load(file)["openai_key"]

# Set environment variable for OpenAI
os.environ["OPENAI_API_KEY"] = api_key

# Initialize OpenAI Client
client = openai.OpenAI()

# Define prompt

messages = [
    {
        "role": "system",
        "content": """You are an AI meal planner. Always respond with a structured JSON format. 

# Response Format:
[
    {
        "day": "Monday",
        "dish_name": "Example Dish",
        "ingredients": ["Ingredient 1", "Ingredient 2"],
        "ingredient_quantity": [100, 200],
        "ingredient_unit": ["grams", "ml"],
        "ingredient_cost": [1.5, 0.5],
        "preparation_steps": ["Step 1", "Step 2"]
    },
    ...
]

If you cannot generate a meal plan, respond with:
{"error": "API request failed"}
"""
    },
    {
        "role": "user",
        "content": "Generate a meal plan for the next 7 days."
    }


]

# Implement Retry Logic
MAX_RETRIES = 3
meal_plan = None

for attempt in range(MAX_RETRIES):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    raw_response = response.choices[0].message.content.strip()
    
    try:
        meal_plan = json.loads(raw_response)  # Try parsing response as JSON
        print("Successfully parsed JSON!")
        break  # Exit loop if successful
    except json.JSONDecodeError:
        print(f"Retry {attempt + 1}/{MAX_RETRIES}: Invalid JSON, retrying...")
        meal_plan = None

# If after all retries, the response is still invalid
if not meal_plan:
    print("Failed to generate a valid JSON response after multiple attempts.")
    exit(1)

# Save to file if valid
with open("meal_plan.json", "w") as f:
    json.dump(meal_plan, f, indent=4)

print("Meal plan generated successfully and saved to 'meal_plan.json'!")
