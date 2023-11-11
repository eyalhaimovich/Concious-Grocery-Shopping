
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
from back_end import *
from datetime import datetime
import sqlite3
import csv


# get current day
curr_day = datetime.now()
curr_date = curr_day.strftime("%m/%d/%Y")


def load_data():
    """Load data from previous session into the inventory"""

    # connect to database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    current_items.delete(0, tk.END)
    # Select items from database
    cursor.execute("SELECT foodName, expiration FROM Food_Data")
    # Fetch all items in query
    items = cursor.fetchall()
    # insert into current_items listbox
    for row in items:
        current_items.insert(tk.END, row)
    conn.commit()
    conn.close()


def call_backend(event=None):
    """
    when called fills listbox up with items retrieved from back_end.py
    """
    global api_foods
    api_foods = callAPI(API_KEY, food_entry.get(), food_category_val.get())
    food_listbox.delete(0, END)
    for food in api_foods:
        food_listbox.insert('end', food)

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
    """insert item into shopping cart"""
    if food_listbox.curselection():
        index = int(food_listbox.curselection()[0])
        cart_foods.append(api_foods[index])  # put food obj in cart food list
        shopping_Cart.insert('end', api_foods[index])  # add to listbox


def delete_item_from_cart(event=None):
    """delete item from shopping cart"""
    if shopping_Cart.curselection():
        index = int(shopping_Cart.curselection()[0])
        cart_foods.pop(index)
        shopping_Cart.delete(index)


def delete_item_from_inventory(event=None):
    """delete item from shopping cart"""
    if current_items.curselection():
        index = int(current_items.curselection()[0])
        inventory_foods.pop(index)
        current_items.delete(index)


def set_expiration_date(event=None):
    """
    setting expiration dates
    """
    # popup
    if current_items.curselection():
        popup = Toplevel(inventory)
        popup.geometry("500x500")
        popup.title("Expiration Date")
        popup_label = Label(popup)
        label_text = "Enter expiration date: "
        popup_label.grid(row=1, column=2, padx=2, pady=2)
        popup_label.config(text=label_text)
        # date widget
        expire_cal = DateEntry(popup, width=12, background='DarkOrange4',
                               foreground='white', borderwidth=2, year=2023)
        expire_cal.grid(row=1, column=3, padx=2, pady=2)

        # function to set date for food item
        def submit_and_close(event=None):
            index = int(current_items.curselection()[0])
            inventory_foods[index].setDate(expire_cal.get())  # get date chosen from calendar widget
            current_items.delete(index)
            current_items.insert(index, inventory_foods[index])
            popup.destroy()  # Close the popup
        submit_btn = tk.Button(popup, text="Submit Date", command=submit_and_close)
        submit_btn.grid(row=2, column=3, padx=2, pady=2)
        popup.bind('<Return>', submit_and_close)

def insert_into_database():
    """Create table and insert data into database"""
    # open connection to database
    conn = sqlite3.connect('data.db')
    # Create table
    table_create_query = ('CREATE TABLE IF NOT EXISTS Food_Data '
                          '(foodName TEXT, expiration TEXT)')

    conn.execute(table_create_query)
    # create csv file
    write_csv()
    # read csv
    file = open('food_data_info.csv')
    contents = csv.reader(file)
    # insert query
    data_insert_query = 'INSERT INTO Food_Data(foodName, expiration) VALUES (?, ?)'
    cursor = conn.cursor()
    # insert multiple rows of data into database
    cursor.executemany(data_insert_query, contents)
    # commit changes to database
    conn.commit()
    # close connection to database
    conn.close()


def write_csv():
    """turn the inventory_foods list into a csv"""
    # nest inventory_foods into a list for sqlite
    nested_list = []
    for i, foods in enumerate(inventory_foods):
        nested_list.append([inventory_foods[i].name, inventory_foods[i].date])
    print(nested_list)
    with open('food_data_info.csv', 'w', newline='') as infile:
        # write list to csv
        writer = csv.writer(infile)
        writer.writerows(nested_list)


def export_list():
    """
    send items in cart to inventory and clear cart
    """
    # TODO check if list is not empty: COMPLETE
    lb_size = shopping_Cart.size()
    if lb_size != 0:
        for item in shopping_Cart.get(0, END):
            current_items.insert("end", item)
        inventory_foods.extend(cart_foods)
        cart_foods.clear()
        shopping_Cart.delete(0, tk.END)
        # TODO NOTIFY USER CART HAS BEEN SUBMITTED
        messagebox.showinfo("Alert!", "Shopping cart submitted!")
    else:
        messagebox.showwarning("Warning!", "Shopping cart is empty!")


'''GUI Begins Here'''
if __name__ == "__main__":
    # store food objects
    cart_foods = []
    inventory_foods = []
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
    # TODO ADD 'ENTER' BUTTON FUNCTIONALITY FOR SEARCH BAR AND SUBMITTING EXPIRATION DATE: COMPLETE
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
    food_entry.bind("<Return>", call_backend)
    # Search Listbox
    food_listbox = Listbox(search_Tab, height=45, width=90,
                           bg="white", fg="orange", activestyle='none')
    food_listbox.grid(row=2, column=1, rowspan=2, padx=10, pady=10)
    food_listbox.bind("<Double 1>", add_item)
    # "More Details" Button Config
    show_details_btn = Button(search_Tab, text='Show Selected', command=open_popup)
    show_details_btn.grid(row=4, column=1, pady=10)
    # Cart Listbox
    shopping_Cart = Listbox(search_Tab, height=45, width=90)
    shopping_Cart.grid(row=2, column=3, rowspan=2, padx=10, pady=10)
    shopping_Cart.bind("<Double 1>", delete_item_from_cart)
    # Button to add item to shopping cart
    add_item_btn = Button(search_Tab, text=">>>>>", command=add_item)
    add_item_btn.grid(row=3, column=2, padx=10, pady=0, sticky="n")
    # Button to delete item from shopping cart
    delete = Button(search_Tab, text="<<<<<", command=delete_item_from_cart)
    delete.grid(row=3, column=2, padx=10, pady=50, sticky="n")
    # send whole list to inventory
    export_btn = Button(search_Tab, text="Submit list to inventory", command=export_list)
    export_btn.grid(row=4, column=3, padx=10, pady=10)

    '''INVENTORY TAB GUI'''
    parentTab.add(inventory, text='Current Inventory')
    inventory_Title = ttk.Label(inventory, text="Your Current Pantry Items at Home")
    inventory_Title.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    # Currents items Listbox
    current_items = Listbox(inventory, height=45, width=90)
    current_items.grid(row=2, column=1, rowspan=2, padx=10, pady=10)
    current_items.bind("<Double 1>", set_expiration_date)
    # expiration date button
    expire_date_btn = Button(inventory, text="Set Expiration Date", command=set_expiration_date)
    expire_date_btn.grid(row=2, column=2, padx=10, pady=10, sticky='s')

    # delete item button
    del_from_inv_btn = Button(inventory, text="Delete item from Inventory", command=delete_item_from_inventory)
    del_from_inv_btn.grid(row=3, column=2, padx=10, pady=10, sticky="n")

    # button for creating csv file for data storage
    csv_btn = Button(inventory, text="Save List", command=insert_into_database)
    csv_btn.grid(row=3, column=3, padx=10, pady=10)

    #  display the tabs in the window
    parentTab.pack(expand=1, fill="both")
    # load_data()
    window.mainloop()
