import combo

from back_end import *
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox


def show_text_field():  # function to display text to console and in text field
    # shows text in console
    print("Food item: %s\n" % (food_text_area.get(1.0, "end-1c")))
    content = food_entry.get()
    food_text_area.insert(END, content + "\n")


def get_quote():  # function to test text output from an API to text field
    r = requests.get('https://api.quotable.io/random')
    data = r.json()
    quote = data['content']
    food_text_area.delete('1.0', END)
    food_text_area.insert(END, quote)


def use_backend():  # uses back_end code to retrieve the values
    r = food_entry.get()
    output = callAPI(r, API_KEY)
    food_text_area.delete('1.0', END)
    food_text_area.insert(END, output)


def dropdown_menu(event):
    selection = combo.get()
    messagebox.showinfo(
        title="New Selection",
        message=f"Selected option: {selection}"
    )


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Concious Grocery Shopping")
    window.geometry("800x600")
    parent_tab = ttk.Notebook(window)

    #  tabs
    search_Tab = ttk.Frame(parent_tab)
    shopping_Cart = ttk.Frame(parent_tab)
    inventory = ttk.Frame(parent_tab)

    #  ////SEARCH TAB////
    parent_tab.add(search_Tab, text='Search')
    ttk.Label(search_Tab, text="Search for Food Here")

    label1 = tk.Label(search_Tab, text="Enter Food Item: ", bg='light green')

    # widget for user input
    food_entry = tk.Entry(search_Tab)

    # area to display text
    food_text_area = Text(search_Tab, height=25, width=50)

    #  option menu configuration
    food_categories = ["Baby Foods", "Baked Products", "Beef Products", "Beverages", "Breakfast Cereals",
                       "Cereal Grains and Pastas", "Dairy and Egg Products", "Fast Foods", "Fats and Oils",
                       "Finfish and Shellfish Products", "Fruits and Fruit Juices", "Poultry Products"]
    value = tk.StringVar(search_Tab)
    # default value
    value.set("Select an option")
    option_menu = tk.OptionMenu(search_Tab, value, *food_categories)
    option_menu.grid(row=2, column=2)
    #  console print for debug

    def option_view():
        print("Selected Option: {}".format(value.get()))
        food_text_area.insert(END, value.get())
        return None


    # grid organizing
    label1.grid(row=1, column=1, padx=10, pady=10)
    food_text_area.grid(row=3, column=2, padx=10, pady=15)
    food_entry.grid(row=1, column=2, padx=10, pady=10)

    #btn = tk.Button(search_Tab, text='Search', fg='Black', bg='cornflower blue', command=use_backend)
    #btn.grid(row=1, column=4, padx=10)
    dual_btn = Button(search_Tab, text='Submit', command=lambda: [use_backend(), option_view()])
    dual_btn.grid(row=1, column=3, padx=10, pady=10)
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||

    #  ////SHOPPING CART TAB////
    parent_tab.add(shopping_Cart, text='Shopping Cart')
    ttk.Label(shopping_Cart, text="Shopping Cart")
    # area to display text
    food_text_area = Text(shopping_Cart, height=25, width=50)
    food_text_area.grid(row=3, column=2, padx=10, pady=15)

    #  Inventory Tab
    parent_tab.add(inventory, text='Current Inventory')

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
data is sent through tkinter for ouptut

'''
