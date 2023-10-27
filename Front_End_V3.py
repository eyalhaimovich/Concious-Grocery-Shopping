
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from back_end import *


def call_backend():
    """
    when called fills listbox up with items retrieved from back_end.py
    """
    output = callAPI(API_KEY, food_entry.get(), food_category_val.get())
    food_listbox.delete(0, END)
    for i in output:
        food_listbox.insert('end', i)


def open_popup():
    """
    creates pop up window
    """
    popup = Toplevel(search_Tab)
    popup.geometry("400x200")
    popup.title("Food Details")
    show = Label(popup)
    show.grid(row=1, column=2, padx=2, pady=2)
    show.config(text=food_listbox.get(ANCHOR))
    pop_btn = Button(popup, text="Add Item", command=add_item)
    close_btn = Button(popup, text="Close", command=popup.destroy)
    pop_btn.grid(row=2, column=2, padx=2.5, pady=5)
    close_btn.grid(row=2, column=3, padx=2.5, pady=5)


def add_item(event=None):
    """insert item into next window in shopping cart"""
    item = food_listbox.get(food_listbox.curselection())
    if item:
        shopping_Cart.insert('end', item)


def delete_item(event=None):
    """delete item in shopping cart"""
    remove = shopping_Cart.curselection()
    if remove:
        shopping_Cart.delete(remove)


def expiration_date():
    """
    setting expiration dates
    """
    popup = Toplevel(inventory)
    popup.geometry("300x200")
    popup.title("Expiration Date")
    popup_label = Label(popup)
    label_text = "Enter expiration date: "
    popup_label.grid(row=1, column=2, padx=2, pady=2)
    popup_label.config(text=label_text)
    expire_cal = DateEntry(popup, width=12, background='DarkOrange4',
                           foreground='white', borderwidth=2, year=2023)
    # expire_cal.get_date() gets date from DateEntry widget
    expire_cal.grid(row=1, column=3, padx=2, pady=2)
    submit_btn = Button(popup, text="Submit Date")
    submit_btn.grid(row=2, column=3, padx=2, pady=2)
    '''
    Working on changing items in list box to include the expiration date
    '''


def export_list():
    """
    send items in shopping cart to inventory tab
    """
    for item in shopping_Cart.get(0, END):
        current_items.insert("end", item)


'''GUI Begins Here'''
if __name__ == "__main__":
    # Main window for application
    window = tk.Tk()
    window.title("Conscious Grocery Shopping")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    # window.geometry(f"{screen_width}x{screen_height}")
    window.state('zoomed')
    # window.attributes("-fullscreen", True)
    # parent window for the tabs
    parentTab = ttk.Notebook(window)
    # TABS
    search_Tab = ttk.Frame(parentTab)
    inventory = ttk.Frame(parentTab)


    '''SEARCH TAB GUI'''
    parentTab.add(search_Tab, text='Search')
    # Food entry label config
    entry_Label = tk.Label(search_Tab, text="Enter Food Item: ")
    entry_Label.grid(row=1, column=1, padx=10, pady=30, sticky="w", )
    # widget for user input
    food_entry = tk.Entry(search_Tab)
    food_entry.grid(row=1, column=1, padx=120, pady=30, sticky="w")
    # food category button + variable
    food_category_val = tk.StringVar()
    food_category_val.set("All Categories")
    option_menu = tk.OptionMenu(search_Tab, food_category_val, *food_categories)
    option_menu.grid(row=1, column=1, padx=120, sticky="e")
    # Submit button
    search_btn = Button(search_Tab, text='Submit', command=call_backend)
    search_btn.grid(row=1, column=1, pady=30, sticky="e")
    # Search Listbox
    food_listbox = Listbox(search_Tab, height=30, width=50,
                           bg="white", fg="orange", activestyle='none', font="Arial")
    food_listbox.grid(row=2, column=1, rowspan=2, padx=10, pady=10)
    food_listbox.bind("<Double 1>", add_item)
    # "More Details" Button Config
    show_details_btn = Button(search_Tab, text='Show Selected', command=open_popup)
    show_details_btn.grid(row=4, column=1, pady=10)
    # Cart Listbox
    shopping_Cart = Listbox(search_Tab, height=45, width=90)
    shopping_Cart.grid(row=2, column=3, rowspan=2, padx=10, pady=10)
    shopping_Cart.bind("<Double 1>", delete_item)
    # Button to add item to shopping cart
    add_item_btn = Button(search_Tab, text=">>>>>", command=add_item)
    add_item_btn.grid(row=3, column=2, padx=10, pady=0, stick="n")
    # Button to delete item from shopping cart
    delete = Button(search_Tab, text="<<<<<", command=delete_item)
    delete.grid(row=3, column=2, padx=10, pady=50, sticky="n")
    # send whole list to inventory
    export_btn = Button(search_Tab, text="Submit list to inventory", command=export_list)
    export_btn.grid(row=4, column=3, padx=10, pady=10)

    '''INVENTORY TAB GUI'''
    parentTab.add(inventory, text='Current Inventory')

    inventory_Title: Label = ttk.Label(inventory, text="Your Current Pantry Items at Home")
    inventory_Title.grid(row=1, padx=5, pady=5)
    # Changed textbox to ListBox
    current_items = Listbox(inventory, height=25, width=75)
    current_items.grid(row=3, column=2, padx=10, pady=10)
    current_items.grid(row=3, column=2, padx=10, pady=10)
    # expiration date button config
    expire_date_btn = Button(inventory, text="Set Expiration Date", command=expiration_date)
    expire_date_btn.grid(row=3, column=3, padx=10, pady=10)

    #  display the tabs in the window
    parentTab.pack(expand=1, fill="both")
    window.mainloop()