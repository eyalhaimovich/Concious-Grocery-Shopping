import sys
import requests
import json
"""
Define a food class and use API at https://fdc.nal.usda.gov/api-guide.html
to find food and retrieve food information
"""


class FoodItem:
    """
    params:
        str: name;
        int: calories;
        list: macros [protein, fat, carbs]
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


def callAPIbyId(id, key):
    """
    call the FDC API using food ID and apiKey
    :param id: food id
    :param key: apiKey
    :return: return data for item found
    """
    api_url_id = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={key}&query={id}'
    response = requests.get(api_url_id)
    if response.status_code == 200:
        data = response.json()
        food_data = (data["foods"][0]["foodNutrients"])  # type list with 1 entry [0] pulls the dict entry out of list
        # access by list entry then dict entry within the list
        # [0],[1],[2],[3] are protein, fat, carbs, calories. rest are fiber vitamins etc.
        macroValues = [food_data[0]["value"], food_data[1]["value"], food_data[2]["value"], food_data[3]["value"]]
        return macroValues
    else:
        print("Request failed with status code:", response.status_code)


api_key = "jyAqilW3drrzghDxACXD2KhJmdDljsgC3NNaCcas" #https://fdc.nal.usda.gov/api-spec/fdc_api.html


# using eggplant from: https://fdc.nal.usda.gov/fdc-app.html#/food-details/2636702/nutrients
eggplant_id = 2636702
eggplant_name = "EGGPLANT"

# Typical ways to call API by id/name
# api_url_name = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={food_name}'
# api_url_id = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={food_id}'

# get macros by food ID from API
macros = callAPIbyId(eggplant_id, api_key)
# use item name & macros to create a Food object
eggplant = FoodItem(eggplant_name, macros)
# print food obj's __str__
print(eggplant)


# manual inputs
# chicken = FoodItem("Chicken", 100, [20, 1, 5])
# print(chicken)
