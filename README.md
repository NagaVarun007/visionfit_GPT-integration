Add keys.yaml file
In that, enter your key:       openai_key: "your_openai_api_key_here"

chatgpt_meal_planner/
│── keys.yaml                 # API Key (gitignored)
│── requirements.txt           # Python dependencies
│── meal_planner.py            # Core logic to generate meal plans
│── parse_meal_plan.py         # Converts JSON to CSV
│── generate_shopping_list.py  # Extracts shopping list from meal plan
│── meal_plan.json             # Generated meal plan (Output)
│── meal_plan.csv              # Meal plan in tabular format (Output)
│── shopping_list.csv          # Aggregated shopping list (Output)
│── .gitignore                 # Ignore sensitive files


To run :
streamlit run meal_planner_gui.py
