import sys
import requests
import json
"""
Define a food class and use API from https://fdc.nal.usda.gov/api-guide.html
to find food items and retrieve food information
"""

API_KEY = "jyAqilW3drrzghDxACXD2KhJmdDljsgC3NNaCcas" #https://fdc.nal.usda.gov/api-spec/fdc_api.html

#  all possible parameters for food search API
"""
parameters = {
    'pageSize': 50,            # Number of results per page
    'pageNumber': 1,           # Page number
    'sortBy': 'fdcId',         # Sort results by FDC ID (or other fields)
    'sortOrder': 'asc',        # Sort order (asc or desc)
    'dataType': ['Foundation', 'SR Legacy'],  # Data type (Foundation, SR Legacy, etc.)
}
"""

# all possible food categories
food_categories = ['All Categories', 'Baked Products', 'Beef Products', 'Beverages', 'Cereal Grains and Pasta',
                   'Dairy and Egg products', 'Fats and Oils', 'Finfish and Shellfish Products',
                   'Fruits and Fruit Juices', 'Legumes and Legume products', 'Nut and Seed Products', 'Pork Products',
                   'Poultry Products', 'Restaurant Foods', 'Sausages and Luncheon Meats', 'Soups, Sauces, and Gravies',
                   'Spices and Herbs', 'Sweets', 'Vegetables and Vegetable Products']

class FoodItem:
    """
    params:
        str: name: food name = food description from database
        int: id: food id
        list of lists: macros [protein, fat, carbs, calories]
    """
    def __init__(self, name, id, macros):
        self.name = name
        self.id = id
        self.macros = macros

    def __str__(self):
        # clean up display for food names
        if len(self.name) >= 30:
            last_word = self.name[30:].split(" ")[0]
            self.name = self.name[:30] + last_word
            if self.name[-1] == ",":
                self.name = self.name[:-1]
            self.name += '...'
        food_entry = f"{self.name:<50}{round(self.macros[3])} Calories\n"
        #food_entry = f"{self.name:<50}{self.macros[3]}\t{self.macros[0]}\t{self.macros[1]}\t{self.macros[2]}\n"
        return food_entry


def callAPI(API_key, food_name, food_category = 'All Categories'):
    """
    call the FDC API using food ID/name and apiKey
    :param food_name: food name
    :param food_category: food_category = 'All'
    :param API_key: apiKey
    :return: macroValues
    TODO Add parameter for 'foodCategory?'
    """
    # get data from USDA database
    api_url = 'https://api.nal.usda.gov/fdc/v1/foods/search'
    response = requests.get(api_url,
                            # params={ **parameters} if want to include parameters dictionary
                            params={'api_key': API_key, 'query': food_name,
                                    'dataType': ['Foundation', 'SR Legacy'], 'pageSize': 500})
    if response.status_code == 200:
        data = response.json()

        '''for i in data['foods']:
            print(i['foodCategory'])'''

        # remove excess data keys, can adjust as needed
        wanted_keys = ['description', 'fdcId', 'dataType', 'foodNutrients', 'foodCategory']  # keys holding useful information
        food_items = filter_food_items(data, wanted_keys)

        '''for i in food_items:
            for j in (i['foodNutrients']):
                print(j)'''

        # remove excess nutrient data from 'foodNutrients', can add vitamins etc. as needed
        macro_names = ['Protein', 'Total lipid (fat)', 'Carbohydrate, by difference', 'Energy', 'Energy (Atwater General Factors)']
        wanted_keys = ['nutrientId', 'nutrientName', 'unitName', 'value']  # keys holding useful information
        food_items = filter_nutrients(food_items, wanted_keys, macro_names)
        food_items = filter_calories(food_items)
        if food_category != 'All Categories':
            food_items = sort_food_category(food_items, food_category)

        '''for i in food_items:
            for j in i['foodNutrients']:
                print(j)'''

        # get macro values for each food item
        # TODO: Might want to add "unit" to macros later to have a list of floats instead of strings
        list_of_macros = get_macros(food_items)

        # combine name of food with its macros
        foodItems = set_food_output(food_items, list_of_macros)

        return foodItems

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
        new_dict = {}
        # populate dict only with wanted keys
        for key in keys:
            if key in item:
                new_dict[key] = item[key]
        # append filtered dict to list
        food_items.append(new_dict)

    return food_items


def filter_nutrients(items, keys, macro_names):
    """
    :param items: list of food item dicts
    :param keys: list of wanted keys from each dict
    :param macro_names: list of wanted macro names from nutrients
    :return: items, updated to only filtered data
    """
    for item in items:
        nutrients = []
        for eachDict in item['foodNutrients']:
            new_dict = {}
            if eachDict.get('nutrientName') in macro_names:
                for key in keys:
                    if key in eachDict:
                        new_dict[key] = eachDict[key]
                nutrients.append(new_dict)
        item['foodNutrients'] = nutrients

    return items


def filter_calories(food_items):
    """
    convert kJ to KCAL
    """
    for food in food_items:
        for nutrient in food['foodNutrients']:
            if nutrient['nutrientName'] == 'Energy (Atwater General Factors)':
                nutrient['nutrientName'] = 'Energy'
            if nutrient['unitName'] == 'kJ':
                nutrient['value'] = round(nutrient['value'] / 4.184, 1)  # conv to KCAL
                nutrient['unitName'] = 'KCAL'

    return food_items


def sort_food_category(food_items, food_category):
    """
    only display items from specified foot category
    :param food_category:
    :param food_items:
    """
    '''new_food_items = []
    for food in food_items:
        print(food)
        if food['foodCategory'] in food_category:
            food_items.pop(food)
    return food_items'''

    food_items = [food for food in food_items if food['foodCategory'] in food_category]
    return food_items


def get_macros(food_items):
    """
    :param food_items: list of food item dicts
    :return: list_of_macros: list of macros for each food item
    """
    list_of_macros = []
    for item in food_items:
        macro_values = [0] * 4
        for eachDict in item['foodNutrients']:
            nutrient_name = eachDict['nutrientName']
            value = eachDict['value']
            # unit = eachDict['unitName']
            if nutrient_name == 'Protein':
                macro_values[0] = value  #  str(value) + ' ' + unit
            elif nutrient_name == 'Total lipid (fat)':
                macro_values[1] = value  #  str(value) + ' ' + unit
            elif nutrient_name == 'Carbohydrate, by difference':
                macro_values[2] = value  #  str(value) + ' ' + unit
            elif nutrient_name == 'Energy':
                macro_values[3] = value  #  str(value) + ' ' + unit
        list_of_macros.append(macro_values)

    return list_of_macros


def set_food_output(food_items, list_of_macros):
    """
    :param food_items: food item data
    :param list_of_macros: list of macros in same order as food items
    :return: list_of_foods a list of FoodItems
    """
    list_of_foods = []
    i = 0
    for each_food in food_items:
        list_of_foods.append(FoodItem(each_food['description'], each_food['fdcId'], list_of_macros[i]))
        i += 1
    return list_of_foods


# example eggplant from: https://fdc.nal.usda.gov/fdc-app.html#/food-details/2636702/nutrients
food_name = "apple"

# retrieve potential foods from food_name
foodItem_list = callAPI(API_KEY, food_name, "Fruits and Fruit Juices")
# foodItem_list = sorted(foodItem_list, key=lambda item: item.name)
# print all foods
for food in foodItem_list:
    print(food, "\n")

# print a chosen item in the list
# TODO make a more sophisticated print to show all nutrients for a specific item?
# print(foodItem_list[0])
