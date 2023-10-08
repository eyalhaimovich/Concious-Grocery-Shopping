import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox

# API code
import sys
import requests
import json

from back_end import *

API_KEY = "jyAqilW3drrzghDxACXD2KhJmdDljsgC3NNaCcas"


# functions for application
def use_backend():  # uses back_end code to retrieve the values
    r = food_Search.get()
    print("Typed food: {}".format(food_Search.get()))
    output = callAPI(r, API_KEY)
    food_text_area.delete('1.0', END)
    food_text_area.insert(END, output)


def option_view():
    print("Selected Option: {}".format(value.get()))
    food_text_area.insert(END, value.get())
    return None


# GUI begins here
if __name__ == "__main__":
    # Main window for application
    window = tk.Tk()
    window.title("Conscious Grocery Shopping")
    window.geometry("800x600")
    # parent window for the tabs
    parentTab = ttk.Notebook(window)

    #  tabs
    search_Tab = ttk.Frame(parentTab)
    shopping_Cart = ttk.Frame(parentTab)
    inventory = ttk.Frame(parentTab)

    #  ////SEARCH TAB//// for food search
    parentTab.add(search_Tab, text='Search')
    searchLabel = ttk.Label(search_Tab, text="Search for Food Here")

    enterLabel = tk.Label(search_Tab, text="Enter Food Item: ", bg='light green')

    # widget for user input
    food_Search = tk.Entry(search_Tab)

    # area to display text
    food_text_area = Text(search_Tab, state='disabled', height=25, width=50)

    #  option menu configuration
    food_categories = ['Baked Products', 'Beef Products', 'Beverages', 'Cereal Grains and Pasta',
                       'Dairy and Egg products', 'Fats and Oils', 'Finfish and Shellfish Products',
                       'Fruits and Fruit Juices', 'Legumes and Legume products', 'Nut and Seed Products',
                       'Pork Products',
                       'Poultry Products', 'Restaurant Foods', 'Sausages and Luncheon Meats',
                       'Soups, Sauces, and Gravies',
                       'Spices and Herbs', 'Sweets', 'Vegetables and Vegetable Products']
    value = tk.StringVar(search_Tab)
    # default value
    value.set("Select an option")
    option_menu = tk.OptionMenu(search_Tab, value, *food_categories)

    # button for text entry and dropdown menu submission
    dual_btn = Button(search_Tab, text='Submit', command=lambda: [use_backend(), option_view()])

    # grid organizing
    searchLabel.grid(row=1, column=1, padx=5, pady=5)
    enterLabel.grid(row=2, column=1, padx=10, pady=10)
    food_Search.grid(row=2, column=2, padx=10, pady=10)
    option_menu.grid(row=2, column=3)
    dual_btn.grid(row=2, column=4, padx=10, pady=10)
    food_text_area.grid(row=3, column=2, padx=10, pady=15)
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||

    #  ////SHOPPING CART TAB////
    parentTab.add(shopping_Cart, text='Shopping Cart')
    ttk.Label(shopping_Cart, state='disabled', text="Shopping Cart")
    # area to display text
    item = Text(shopping_Cart, height=25, width=50)
    item.grid(row=3, column=2, padx=10, pady=15)

    #  ////INVENTORY TAB////
    parentTab.add(inventory, text='Current Inventory')

    inventory_Title = ttk.Label(inventory, text="Your Current Pantry Items at Home")
    inventory_Title.grid(row=1, padx=5, pady=5)
    # text box
    current_items = Text(inventory, state='disabled', height=25, width=50)
    current_items.grid(row=3, column=2, padx=10, pady=10)


    #  display the tabs in the window
    parentTab.pack(expand=1, fill="both")
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
