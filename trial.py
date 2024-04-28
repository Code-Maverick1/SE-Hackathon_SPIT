import google.generativeai as genai
from typing import Any
from PIL import Image
import json

# Paste your raw API key here
GOOGLE_API_KEY = "AIzaSyCUJcWsR2sMQxO_SsWw6vvZ3qx-6E7mcGU"
def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def initialize_gemini_model2():
    # Configure the API key
    genai.configure(api_key=GOOGLE_API_KEY)

    # Initialize the generative model
    model2 = genai.GenerativeModel('gemini-pro-vision')

    return model2

def initialize_gemini_model():
    # Configure the API key
    genai.configure(api_key=GOOGLE_API_KEY)

    # Initialize the generative model
    model = genai.GenerativeModel('gemini-pro')

    return model


# Now you can use gemini_model to generate content or perform other operations.

class Person():
    def __init__(self,weight=75 , cuisine = None, activity = None,calories = None , diet_restrictions=None,  custom_meal=None,is_veg='veg',allergies=None , body_type = None,days='Monday'):
        self.weight = weight
        self.calories = calories
        self.diet_restrictions = diet_restrictions
        self.custom_meal = custom_meal
        self.is_veg = is_veg
        self.allergies = allergies
        self.body_type = body_type
        self.days = days
        self.cuisine = cuisine
        self.activity  = activity
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return {"weight" : self.weight,
                "calories" : self.calories,
                "diet_restrictions" : self.diet_restrictions,
                "is_veg" : self.is_veg,
                "allergies" : self.allergies,
                "body_type" : self.body_type,
                "days" : self.days,
                "cuisine" : self.cuisine,
                "activity" : self.activity
                 }

days = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]
body_type = [
    'Weight Loss',
    'Weight Gain',
    'Muscle Gain'
]

def water_intake(activity,weight):
    if(activity.lower() == 'high'):
        return weight*0.03
    elif(activity.lower() == "moderate"):
        return weight*0.03 + 0.4
    else:
        return weight*0.03 + 1
    

def generate_mealplan(model, person):
    def generate_mealplan_prompt(person):
        person = person()
        prompt = "Give me a meal plan with the following considerations:\n"
        prompt += f"Weight = {person['weight']} "
        if person.get("calories") is not None:
            prompt += f"Calories = {person['calories']}"
        if person.get("diet_restrictions") is not None:
            prompt += f". Got my diet restrictions as = {person['diet_restrictions']} "
        if person.get("is_veg") is not None:
            prompt += f". I need only {person['is_veg']} food"
        if person.get("allergies") is not None:
            prompt += f". Got some allergies as {person['allergies']}"
        if person.get("body_type") is not None:
            prompt += f". Got my goal to {person['body_type']}."
        if person.get("custom_meal") is not None:
            prompt += f". Add {person['custom_meal']} to the meal plan for me."
        if person.get("days") != 'Monday':
            prompt += f" Set my day to {person['days']}."
        if person.get('cuisine') is not None:
            prompt += f" I want this type of cuisine:- {person['cuisine']} "
        # prompt += f" And dont give ingredients or instructions for receipe but generate only meal plan"
        return prompt
    

    # Generate prompt
    prompt = generate_mealplan_prompt(person)

    # Generate meal plan using the model
    response = model.generate_content(prompt)

    # Extract and return the meal plan from the response
    meal_plan = response.candidates[0].content.parts[0].text
    return meal_plan

# Example person object
my_person = {
    'weight': 75,
    'calories': 1203,
    'diet_restrictions': 'gluten free',
    'custom_meal' : 'mango',
    'days': 'Sunday',
    'is_veg': 'Non-Veg',
}

# Example usage
# meal_plan = generate_mealplan(model, my_person)
# print(meal_plan)
person = None
def person_loader():
    return load_json('data.json')

def image_prompt(person = person, img_path = None):
  person = person_loader()
  img = Image.open(img_path)

  # Construct the prompt with specific health-related criteria
  prompt = f"I have a meal with the following considerations:\n"
  prompt += f"- Weight: {person['weight']}\n"

  # Add specific dietary information
  if person["allergies"] is not None:
    prompt += f"- Allergies: {person['allergies']}\n"
  if person["body_type"] is not None:
    prompt += f"- Body type: {person['body_type']}\n"
  if person["is_veg"] is not None:
    prompt += f"- Dietary preference: {person['is_veg']}\n"
  if person["diet_restrictions"] is not None:
    prompt += f"- Diet restrictions: {person['diet_restrictions']}\n"

  # Add specific health-related criteria
  prompt += "- Health considerations:\n"
  prompt += "- Low in saturated fats\n"
  prompt += "- High in fiber\n"
  prompt += "- Rich in vitamins and minerals\n"
  prompt += "- Balanced macronutrient composition\n"

  # Add a question for Gemini API
  prompt += "Based on these criteria, is this meal healthy for me? Give the response in only 20 words"

  # Generate content using the model
  model2 = initialize_gemini_model2()
  response = model2.generate_content([prompt, img], stream=True)
  response.resolve()
  
  # Extract the response text
  response_text = response.candidates[0].content.parts[0].text
  return (response_text)

