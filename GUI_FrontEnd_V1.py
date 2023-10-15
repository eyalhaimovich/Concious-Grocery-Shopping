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
def call_backend():
    food_string = food_Search.get()
    output = callAPIbyId(food_string, API_KEY)
    display1.delete(0, END)
    '''for i in output:
        display1.insert('end', i)'''
    display1.insert('end', output)

def option_view():
    print("Selected Option: {}".format(value.get()))
    food_text_area.insert(END, value.get())
    return None


def open_popup():
    popup = Toplevel(shopping_Cart)
    popup.geometry("400x200")
    popup.title("Food Details")
    show = Label(popup)
    show.grid(row=1, column=2, padx=2, pady=2)
    show.config(text=display1.get(ANCHOR))
    pop_btn = Button(popup, text="Add Item", command=insert_list)
    close_btn = Button(popup, text="Close", command=popup.destroy)
    pop_btn.grid(row=2, column=2, padx=2.5, pady=5)
    close_btn.grid(row=2, column=3, padx=2.5, pady=5)


def insert_list():
    add_item = display1.get(display1.curselection())
    display.insert('end', add_item)


def delete_item():
    remove = display.curselection()
    display.delete(remove)

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
    food_text_area = Text(search_Tab, state='disabled', height=25, width=20)
    display1 = Listbox(search_Tab, height=25, width=65)
    display1.grid(row=3, column=2, padx=10, pady=10)

    # configure selection event
    display1btn = Button(search_Tab, text='More Details', command=open_popup)
    display1btn.grid(row=4, column=1, pady=10)
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
    dual_btn = Button(search_Tab, text='Submit', command=lambda: [call_backend(), option_view()])

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
    # listbox
    display = Listbox(shopping_Cart, height=25, width=50)
    display.grid(row=3, column=2, padx=10, pady=10)
    btnSC = Button(shopping_Cart, text="Submit")
    btnSC.grid(row=3, column=3, padx=10, pady=10)
    delete = Button(shopping_Cart, text="Delete Item", command=delete_item)
    delete.grid(row=4, column=3, padx=10, pady=10)

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
