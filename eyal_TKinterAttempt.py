import combo

from back_end import *
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox


def show_text_field(output):  # function to display text to console and in text field
    food_text_area.configure(state="normal")
    food_text_area.delete('1.0', END)
    for item in output:
        food_text_area.insert(END, item)
        # TODO insert add to cart on right side +- from cart
    food_text_area.configure(state="disabled")


def display_food_items():
    output = callAPI(API_KEY, food_var.get(), food_category_val.get())
    show_text_field(output)


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Conscious Grocery Shopping")
    window.geometry("1000x600")

    # for enabling multiple tabs in window
    parent_tab = ttk.Notebook(window)

    # initializing and adding tabs to window
    search_Tab = ttk.Frame(parent_tab)
    shopping_Cart = ttk.Frame(parent_tab)
    inventory = ttk.Frame(parent_tab)
    parent_tab.add(search_Tab, text='Search')
    parent_tab.add(shopping_Cart, text='Shopping Cart')
    parent_tab.add(inventory, text='Current Inventory')

    # search tab UI
    food_entry_label = ttk.Label(search_Tab, text="Enter Food Item: ")
    # food name StringVar
    food_var = tk.StringVar()
    food_entry = tk.Entry(search_Tab, textvariable=food_var)
    # area to display text
    food_text_area = Text(search_Tab, height=20, width=80, state='disabled')
    # food category StringVar
    food_category_val = tk.StringVar()
    food_category_val.set("All Categories")
    # food category menu
    option_menu = tk.OptionMenu(search_Tab, food_category_val, *food_categories)
    option_menu.grid(row=2, column=2)


    # grid organizing
    food_entry_label.grid(row=1, column=1, padx=10, pady=10)
    food_text_area.grid(row=3, column=2, padx=10, pady=15)
    food_entry.grid(row=1, column=2, padx=10, pady=10)

    submit_btn = Button(search_Tab, text='Submit', command=display_food_items)
    submit_btn.grid(row=1, column=3, padx=10, pady=10)
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||

    # SHOPPING CART TAB

    ttk.Label(shopping_Cart, text="Shopping Cart")
    # area to display text
    shopping_text_area = Text(shopping_Cart, height=25, width=50)
    shopping_text_area.grid(row=3, column=2, padx=10, pady=15)

    # Inventory Tab
    food_items = Text(inventory, height=25, width=50)
    food_items.grid(row=3, column=2, padx=10, pady=10)

    ttk.Label(inventory, text="Your Current Pantry Items at Home")

    parent_tab.pack(expand=1, fill="both")
    window.mainloop()

'''
Steps for app:
type a search term
submit search term
use string input to query api for food item
api code runs the search
returns data
data is sent through tkinter for output

'''
