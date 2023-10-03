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
        list of lists: macros [protein, fat, carbs, calories]
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


def callAPI(name, key):
    """
    call the FDC API using food ID/name and apiKey
    :param name: food name
    :param key: apiKey
    :return: macroValues
    """

    # get data from USDA database
    # TODO NEED TO GET MORE SPECIFIC DATA USING QUERIES SUCH AS &dataType=Foundation'
    api_url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={key}&query={name}&dataType=Foundation'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()

        # remove excess data keys, can adjust as needed
        wanted_keys = ['description', 'fdcId', 'dataType', 'foodNutrients', 'foodCategory']  # keys holding useful information
        food_items = filter_food_items(data, wanted_keys)

        '''for i in food_items:
            item = i['foodNutrients']
            for j in item:
                print(j)'''

        # remove excess nutrient data from 'foodNutrients', can add vitamins etc. as needed
        macro_ids = {'protein': 1003, 'fat': 1004, 'carbs': 1005, 'calories': 2048}  # global IDs for each macro calories = 1008 for SR Legacy, 2048 for Foundation
        wanted_keys = ['nutrientId', 'nutrientName', 'unitName', 'value']  # keys holding useful information
        food_items = filter_nutrients(food_items, wanted_keys, macro_ids)

        # get macro values for each food item
        # TODO: Might want to add "unit" to macros later to have a list of floats instead of strings
        list_of_macros = get_macros(food_items, macro_ids)

        # combine name of food with its macros
        possible_foods_dict = set_food_output(food_items, list_of_macros)

        return possible_foods_dict

    else:
        print("Request failed with status code:", response.status_code)


def filter_food_items(data, keys):
    """
    :param data: original data pull from API
    :param keys: list of keys to retain from data
    :return: food_items sorted data by list of keys
    """
    food_items = []
    for item in data['foods']:
        if item.get('dataType') == 'Foundation':  # 'SR Legacy', 'Foundation', 'Branded'
            new_dict = {}
            # populate dict only with wanted keys
            for key in keys:
                if key in item:
                    new_dict[key] = item[key]
            # append filtered dict to list
            food_items.append(new_dict)

    return food_items


def filter_nutrients(items, keys, macro_ids):
    """
    :param items: list of food item dicts
    :param keys: list of wanted keys from each dict
    :param macro_ids: list of wanted ids from nutrients (Protein: 1003, etc.)
    :return: items, updated with filtered data
    """
    for item in items:
        nutrients = []
        for eachDict in item['foodNutrients']:
            new_dict = {}
            if eachDict.get('nutrientId') in macro_ids.values():
                for key in keys:
                    if key in eachDict:
                        new_dict[key] = eachDict[key]
                nutrients.append(new_dict)
        item['foodNutrients'] = nutrients

    return items


def get_macros(food_items, macro_ids):
    """
    :param food_items: list of food item dicts
    :param macro_ids: list of wanted ids from nutrients (Protein: 1003, etc.)
    :return: list_of_macros: list of macros for each food item
    """
    list_of_macros = []
    for item in food_items:
        macro_values = [0] * 4
        for eachDict in item['foodNutrients']:
            nutrient_id = eachDict['nutrientId']
            value = eachDict['value']
            unit = eachDict['unitName']
            if nutrient_id == macro_ids['protein']:
                macro_values[0] = str(value) + ' ' + unit
            elif nutrient_id == macro_ids['fat']:
                macro_values[1] = str(value) + ' ' + unit
            elif nutrient_id == macro_ids['carbs']:
                macro_values[2] = str(value) + ' ' + unit
            elif nutrient_id == macro_ids['calories']:
                macro_values[3] = str(value) + ' ' + unit
        list_of_macros.append(macro_values)

    return list_of_macros


def set_food_output(food_items, list_of_macros):
    dict_of_foods = {}
    i = 0
    for each_food in food_items:
        dict_of_foods[each_food['description']] = list_of_macros[i]
        i += 1
    return dict_of_foods


# example eggplant from: https://fdc.nal.usda.gov/fdc-app.html#/food-details/2636702/nutrients
# eggplant_id = "2636702"  # specific item
food_name = "apple"  # generic item from database

# get macros by name or ID from API
foods_from_database = callAPI(food_name, API_KEY)

# create a list of Food objects
foodItems = []
for name, macros in foods_from_database.items():
    foodItems.append(FoodItem(name, macros))
# print each food macro
for food in foodItems:
    print(food, "\n")

# Typical ways to call API by id/name
# api_url_name = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={food_name}'
# api_url_id = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={food_id}'
