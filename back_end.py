import sys
import requests
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
                unit = eachDict['unitName']
                if nutrient_id == macro_ids['protein']:
                    macroValues[0] = str(value) + ' ' + unit
                elif nutrient_id == macro_ids['fat']:
                    macroValues[1] = str(value) + ' ' + unit
                elif nutrient_id == macro_ids['carbs']:
                    macroValues[2] = str(value) + ' ' + unit
                elif nutrient_id == macro_ids['calories']:
                    macroValues[3] = str(value) + ' ' + unit
            allMacros.append(macroValues)

        return macroValues
    else:
        print("Request failed with status code:", response.status_code)


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
