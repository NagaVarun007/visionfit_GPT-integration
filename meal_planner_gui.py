import streamlit as st
import json
import os
import yaml
import openai

# Load API Key
with open('keys.yaml', 'r') as file:
    api_key = yaml.safe_load(file)["openai_key"]

# Set environment variable for OpenAI
os.environ["OPENAI_API_KEY"] = api_key

# Initialize OpenAI Client
client = openai.OpenAI()

# Streamlit UI
st.title("AI-Powered Meal Planner")

num_days = st.slider("Select number of days", 1, 7, 7)
vegetarian = st.checkbox("Vegetarian Meals Only")
time_limit = st.number_input("Max Preparation Time (minutes)", min_value=10, max_value=60, value=30)

if st.button("Generate Meal Plan"):
    
    # Define messages BEFORE using them
    messages = [
        {
            "role": "system",
            "content": f"""You are an AI meal planner. Always respond with a structured JSON format. 

# Response Format:
[
    {{
        "day": "Monday",
        "dish_name": "Example Dish",
        "ingredients": ["Ingredient 1", "Ingredient 2"],
        "ingredient_quantity": [100, 200],
        "ingredient_unit": ["grams", "ml"],
        "ingredient_cost": [1.5, 0.5],
        "preparation_steps": ["Step 1", "Step 2"]
    }},
    ...
]

Meal plan should be for {num_days} days.
{'Ensure all meals are vegetarian.' if vegetarian else ''}
Each meal should take at most {time_limit} minutes to prepare.
"""
        },
        {
            "role": "user",
            "content": "Generate a meal plan."
        }
    ]
    
    # Ensure messages is defined BEFORE using it in API call
    MAX_RETRIES = 3
    meal_plan = None

    for attempt in range(MAX_RETRIES):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        raw_response = response.choices[0].message.content.strip()
        st.write(f"Attempt {attempt + 1}: Raw Response:", raw_response)  # Debugging

        if not raw_response:
            st.warning(f"Attempt {attempt + 1}: Empty response, retrying...")
            continue

        try:
            meal_plan = json.loads(raw_response)
            break  # Exit loop if successful
        except json.JSONDecodeError:
            st.warning(f"Attempt {attempt + 1}: Invalid JSON, retrying...")
            meal_plan = None

    if not meal_plan:
        st.error("Failed to generate a valid meal plan after multiple attempts.")
        st.stop()

    # Display Meal Plan
    st.write("### Generated Meal Plan:")
    st.json(meal_plan)

    # Download Button
    st.download_button("Download Meal Plan", json.dumps(meal_plan, indent=4), "meal_plan.json", "application/json")
