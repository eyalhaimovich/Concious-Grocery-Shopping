import tkinter as tk
from tkinter import *
from tkinter import ttk
import requests


#API code
import sys

import json

"""
Define a food class and use API at https://fdc.nal.usda.gov/api-guide.html
to find food and retrieve food information
"""

API_KEY = "jyAqilW3drrzghDxACXD2KhJmdDljsgC3NNaCcas" #https://fdc.nal.usda.gov/api-spec/fdc_api.html
class FoodItem:
    """
    params:
        str: name;
        list: macros [protein, fat, carbs, calories]
    """
    def __init__(self, name, macros):
        self.name = name
        self.macros = macros

    def __str__(self):
        return (f"Name: {self.name}"
                f"\nMacros:"
                f"\n\tCalories: {self.macros[3]}"
                f"\n\tProtein: {self.macros[0]}"
                f"\n\tFat: {self.macros[1]}"
                f"\n\tCarbs: {self.macros[2]}")


def callAPI(id, key):
    """
    call the FDC API using food ID/name and apiKey
    :param id: food id
    :param key: apiKey
    :return: macroValues
    """

    api_url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={key}&query={id}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()

        #TODO: FIND AND ADD UNITS TO EACH MACRO AND SAY PER HOW MUCH (i.e. serving size / 100grams)

        # way to remove excess data-- can adjust as needed
        # currently important part is only using foods with dataType 'SR Legacy'
        food_items = []
        wanted_keys = ['fdcId', 'dataType', 'foodNutrients', 'foodCategory']
        for item in data['foods']:
            if item.get('dataType') == 'SR Legacy':
                new_dict = {}
                # populate dict only with wanted keys
                for key in wanted_keys:
                    if key in item:
                        new_dict[key] = item[key]
                # append filtered dict to list
                food_items.append(new_dict)

        # do it again to only keep macros from 'foodNutrients', can add vitamins etc. if wanted
        macro_ids = {'protein': 1003, 'fat': 1004, 'carbs': 1005, 'calories': 1008}  # global IDs for each macro
        wanted_keys = ['nutrientId', 'nutrientName', 'unitName', 'value']
        for item in food_items:
            nutrients = []
            for eachDict in item['foodNutrients']:
                new_dict = {}
                if eachDict.get('nutrientId') in macro_ids.values():
                    for key in wanted_keys:
                        if key in eachDict:
                            new_dict[key] = eachDict[key]
                    nutrients.append(new_dict)
            item['foodNutrients'] = nutrients

        # getting macro values
        allMacros = []
        for item in food_items:
            macroValues = [0] * 4
            for eachDict in item['foodNutrients']:
                nutrient_id = eachDict['nutrientId']
                value = eachDict['value']
                if nutrient_id == macro_ids['protein']:
                    macroValues[0] = value
                elif nutrient_id == macro_ids['fat']:
                    macroValues[1] = value
                elif nutrient_id == macro_ids['carbs']:
                    macroValues[2] = value
                elif nutrient_id == macro_ids['calories']:
                    macroValues[3] = value
            allMacros.append(macroValues)
        print("All database entries for", id)
        print("Protein|Fat|Carbs|Calories")
        for i in allMacros:
            print(i)
        return macroValues
    else:
        print("Request failed with status code:", response.status_code)

def main():#its a function to not interfere with the GUI code for testing
    # using eggplant from: https://fdc.nal.usda.gov/fdc-app.html#/food-details/2636702/nutrients
    eggplant_id = "2636702"  # specific item
    food_name = "milk"  # generic item from database

    # get macros by name or ID from API
    macros = callAPI(food_name, API_KEY)
    # use item name & macros to create a Food object
    eggplant = FoodItem(food_name, macros)
    # print food object's __str__
    print(eggplant)

    # Typical ways to call API by id/name
    # api_url_name = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={food_name}'
    # api_url_id = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={food_id}'

    # manual inputs
    # chicken = FoodItem("Chicken", 100, [20, 1, 5])
    # print(chicken)


def show_text_field(): #function to display text to console and in text field
    #shows text in console
    print("Food item: %s\n"  % (food_text_area.get(1.0, "end-1c" )))
    content = food_entry.get()
    food_text_area.insert(END, content + "\n")
 
def get_quote(): #function to test text output from an API to text field
    r = requests.get('https://api.quotable.io/random')
    data = r.json()
    quote = data['content']
    food_text_area.delete('1.0', END)
    food_text_area.insert(END, quote)  
 
def use_backend(): #uses back_end code to retrieve the values 
    r = food_entry.get()
    output = callAPI(r, API_KEY)
    food_text_area.delete('1.0', END)
    food_text_area.insert(END, output)

if __name__ == "__main__":
    window = Tk()
    window.title("Concious Grocery Shopping")
    window.geometry("600x600")

    label1 = tk.Label(window,text="Enter Food Item: ", bg='light green')

    #widget for user input
    food_entry = tk.Entry(window)

    #area to display text
    food_text_area=Text(window, height=25, width=50)

    #grid organizing
    label1.grid(row=1, column=1, padx=10, pady=10)
    food_text_area.grid(row = 3, column=2, padx=10, pady=15)
    food_entry.grid(row=1, column =2, padx=10, pady=10)

    btn = tk.Button(window, text='Show', fg = 'Black', bg = 'cornflower blue', command=use_backend)
    btn.grid(row = 4, column=2)

     
    window.mainloop()


'''
Steps for app:
type a search term
submit search term
use string input to query api for food item
api code runs the search
returns data
data is sent through tkinter for ouptut

'''