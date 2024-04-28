import streamlit as st
import pandas as pd
import numpy as np
from trial import *
from pydantic import BaseModel
import json
import subprocess

def store_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)
        
def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

class Person():
    def __init__(self,weight=60 , calories = None , activity = None ,diet_restrictions=None,  cuisine = None ,custom_meal=None,is_veg='veg',allergies=None , body_type = None,days='Monday'):
        self.weight = weight
        self.cuisine = cuisine
        self.calories = calories
        self.diet_restrictions = diet_restrictions
        self.custom_meal = custom_meal
        self.is_veg = is_veg
        self.allergies = allergies
        self.body_type = body_type
        self.days = days
        self.activity = activity
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return {"weight" : self.weight,
                "calories" : self.calories,
                "diet_restrictions" : self.diet_restrictions,
                "is_veg" : self.is_veg,
                "allergies" : self.allergies,
                "body_type" : self.body_type,
                "cuisine": self.cuisine,
                "days": self.days,
                "activity": self.activity,
                "custom_meal" : self.custom_meal
                 }

title_style = """
<style>
    .title-text {
        text-align: center;
        margin-top: 0;
        margin-bottom: auto; 
        font-size: 50px;
    }
    
    .trial-text {
        text-align: center;
        margin-top: 0;
        margin-bottom: auto; 
        font-size: 20px;
    }
    
    .navbar {
        overflow: hidden;
        background-color: #333;
    }

    .navbar a {
        float: left;
        display: block;
        color: white;
        text-align: center;
        padding: 14px 20px;
        text-decoration: none;
    }

    .navbar a:hover {
        background-color: #ddd;
        color: black;
    }

    .navbar a.active {
        background-color: #4CAF50;
        color: white;
    }
</style>
"""
person_data = None

rad = st.sidebar.radio("Navigation", ["Home Page", "Generate Your Meal", "Health Check", "Logout"])
user_data = None

if rad == "Home Page":
    page_by_img = """
    <style>
    [data-testid="stAppViewContainer"]{
    background-image: url("https://static.vecteezy.com/system/resources/previews/008/922/776/non_2x/abstract-smooth-blur-background-backdrop-for-your-design-wallpaper-template-with-color-transition-gradient-vector.jpg");
    background-size: cover;
    }

    [data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
    }

    [data-testid="stToolbar"]{
    right: 2rem;
    }
    </style>
    """
    st.markdown(page_by_img, unsafe_allow_html = True)
    st.markdown(title_style, unsafe_allow_html = True)
    st.markdown('<p class = "title-text"><strong>MealMetrics</strong></p>',unsafe_allow_html = True)
    st.markdown('<p class = "trial-text">Effortless Meal Planning Made Simple!</p>',unsafe_allow_html = True)
    st.markdown('<p class = "trial-text">Discover Personalized Meal Plans for Your Lifestyle!</p>',unsafe_allow_html = True)
    
    
if rad == "Generate Your Meal":
    page_by_img = """
    <style>
    [data-testid="stAppViewContainer"]{
    background-image: url("https://static.vecteezy.com/system/resources/previews/008/922/776/non_2x/abstract-smooth-blur-background-backdrop-for-your-design-wallpaper-template-with-color-transition-gradient-vector.jpg");
    background-size: cover;
    }

    [data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
    }

    [data-testid="stToolbar"]{
    right: 2rem;
    }
    </style>
    """
    st.markdown(page_by_img, unsafe_allow_html = True)
    st.markdown(""" # Generate Your Meal Here""", True)
    
    with st.form("user_info_form"):
        weight = st.number_input("Enter your weight(in kgs)", min_value=1, value=60)

        var_3, var_4 = st.columns(2)
        with var_3:
            body_type = st.radio("Enter your goal", ["Weight Gain", "Weight Loss", "Muscle Building"])

        with var_4:
            is_veg = st.radio("Whether you are Veg or Non-Veg", ["Veg", "Non-Veg"])

        var_5, var_6 = st.columns([1,3])
        with var_5:
            calories = st.number_input("Enter target calorie count",min_value = 0, value = 200, step = 2)
            
        with var_6:
            diet_restrictions = st.text_input("Enter any diet restrictions")
        
        var_10, var_11 = st.columns([1,3])
        with var_10:
            activity = st.radio("How active are you?",["high","moderate","low"])
            
        with var_11:
            cuisine = st.text_input("Enter your cuisine")
            
        var_8, var_9 = st.columns([1,3])
        with var_8:
            custom_meal = st.text_input("Enter custom meal")
            
        with var_9:
            allergies = st.text_input("Enter any food allergies you have")
        st.markdown('</div>', unsafe_allow_html=True)
        
        submit_button = st.form_submit_button("Submit")
        
    if submit_button:
        person_data = Person(
        weight=weight,
        calories=calories,
        diet_restrictions=diet_restrictions,
        custom_meal=custom_meal,
        cuisine=cuisine,
        activity=activity,
        is_veg=is_veg,
        allergies=allergies,
        body_type=body_type,
        )
        
        store_json(person_data(), 'data.json')
        sample_dict = person_data()
        s_weight = sample_dict["weight"]
        s_cal = sample_dict["calories"]
        s_diet_res = sample_dict["diet_restrictions"]
        s_custom_meal = sample_dict["custom_meal"]
        s_veg = sample_dict["is_veg"]
        s_cuisine = sample_dict["cuisine"]
        s_allergy = sample_dict["allergies"]
        s_body_type = sample_dict["body_type"]
        s_activity = sample_dict["activity"]
        
        if s_diet_res == "":
            s_diet_res = "None"
            
        if s_custom_meal == "":
            s_custom_meal = "None"
            
        if s_allergy == "":    
            s_allergy = "None"
            
        if s_cuisine == "":
            s_cuisine = "None"
            
        st.write("Weight = ",s_weight)
        st.write("Calories = ",s_cal)
        st.write("Diet Restrictions = ",s_diet_res)
        st.write("Cuisine = ",s_cuisine)
        st.write("Your Activity = ",s_activity)
        st.write("Custom Meal = ",s_custom_meal)
        st.write("Veg OR Non-Veg = ",s_veg)
        st.write("Allergies = ",s_allergy)
        
        user_data = person_data
        intake = water_intake(s_activity, s_weight)
        intake = round(intake, 2)
        st.markdown(f'<div style="text-align: center;"><p class="trial-text"><strong>This is the water intake expected for you per day: {intake} Litres</strong></p></div>',unsafe_allow_html = True)
        
        model = initialize_gemini_model()
        meal_plan = generate_mealplan(model, person_data)
        # Remove asterisks and spaces between letters within each word in meal plan
        # meal_plan_cleaned = [meal.replace('*', '').replace(' ', '') for meal in meal_plan]
    
        # meal_plan_str = ' '.join(meal_plan_cleaned)  # Format meal plan as a space-separated string
        print(type(meal_plan))
        st.markdown(meal_plan)
        
            
if rad == "Health Check":
    page_by_img = """
    <style>
    [data-testid="stAppViewContainer"]{
    background-image: url("https://static.vecteezy.com/system/resources/previews/008/922/776/non_2x/abstract-smooth-blur-background-backdrop-for-your-design-wallpaper-template-with-color-transition-gradient-vector.jpg");
    background-size: cover;
    }

    [data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
    }

    [data-testid="stToolbar"]{
    right: 2rem;
    }
    </style>
    """
    st.markdown(page_by_img, unsafe_allow_html = True)
    st.markdown(""" # Health Check""", True)
    img = st.file_uploader("Upload an image")
    
    if img:
        img_name = img.name
        img_name = img_name.split('.')[0]
        st.image(img, caption = f'{img_name}', width = 300)
        st.write(image_prompt(user_data, img))
        
if rad == "Logout":
    subprocess.Popen(["streamlit", "run", "start.py"])
      