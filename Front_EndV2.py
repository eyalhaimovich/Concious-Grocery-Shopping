from back_end import *
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox

def insert_list():
    item = display1.get(display1.curselection())
    display.insert('end', item)

'''delete item in shopping cart'''
def delete_item():
    remove = display.curselection()
    display.delete(remove)


def display_food_items():
    output = callAPI(API_KEY, food_var.get(), food_category_val.get())
    show_text_field(output)

def call_backend():
    # food_string = food_entry.get()
    output = callAPI(API_KEY, food_var.get(), food_category_val.get())
    display1.delete(0, END)
    for i in output:
        display1.insert('end', i)


def show_text_field(output):  # function to display text to console and in text field
    food_text_area.configure(state="normal")
    food_text_area.delete('1.0', END)
    for item in output:
        food_text_area.insert(END, item)
        # TODO insert add to cart on right side +- from cart
    food_text_area.configure(state="disabled")
# pop up for more details
def open_popup():
    popup = Toplevel(shopping_Cart)
    popup.geometry("400x200")
    popup.title("Food Details")
    # indices = display1.curselection()
    # Label(popup, text=indices)
    show = Label(popup)
    show.grid(row=1, column=2, padx=2, pady=2)
    show.config(text=display1.get(ANCHOR))
    pop_btn = Button(popup, text="Add Item", command=insert_list)
    close_btn = Button(popup, text="Close", command=popup.destroy)
    pop_btn.grid(row=2, column=2, padx=2.5, pady=5)
    close_btn.grid(row=2, column=3, padx=2.5, pady=5)

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
    #food_text_area = Text(search_Tab, height=20, width=80, state='disabled')
    '''Option Menu Configuration'''
    food_category_val = tk.StringVar()
    food_category_val.set("All Categories")
    # food category menu
    option_menu = tk.OptionMenu(search_Tab, food_category_val, *food_categories)
    option_menu.grid(row=2, column=2)

    '''ListBox Text display Configuration'''
    # food_text_area = Text(search_Tab, state='disabled', height=25, width=20)
    display1 = Listbox(search_Tab, height=25, width=65)
    display1.grid(row=3, column=2, padx=10, pady=10)

    # grid organizing
    '''food_entry_label.grid(row=1, column=1, padx=10, pady=10)
    food_text_area.grid(row=3, column=2, padx=10, pady=15)
    '''
    food_entry.grid(row=1, column=2, padx=10, pady=10)
   # submit_btn = Button(search_Tab, text='Submit', command=display_food_items)
    # submit_btn.grid(row=1, column=3, padx=10, pady=10)
    #search button
    dual_btn = Button(search_Tab, text='Submit', command=call_backend)
    dual_btn.grid(row=2, column=4, padx=10, pady=10)

    #  ////SHOPPING CART TAB////
    parent_tab.add(shopping_Cart, text='Shopping Cart')
    ttk.Label(shopping_Cart, state='disabled', text="Shopping Cart")
    # area to display text
    # listbox
    display = Listbox(shopping_Cart, height=25, width=50)
    display.grid(row=3, column=2, padx=10, pady=10)
    btnSC = Button(shopping_Cart, text="Submit")
    btnSC.grid(row=3, column=3, padx=10, pady=10)
    delete = Button(shopping_Cart, text="Delete Item", command=delete_item)
    delete.grid(row=4, column=3, padx=10, pady=10)

    #  ////INVENTORY TAB////
    parent_tab.add(inventory, text='Current Inventory')

    inventory_Title: Label = ttk.Label(inventory, text="Your Current Pantry Items at Home")
    inventory_Title.grid(row=1, padx=5, pady=5)
    # text box
    current_items = Text(inventory, state='disabled', height=25, width=50)
    current_items.grid(row=3, column=2, padx=10, pady=10)

    #  display the tabs in the window
    parent_tab.pack(expand=1, fill="both")
    window.mainloop()