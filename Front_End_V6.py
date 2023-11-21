# Import the Required libraries
import copy
import os
from tkinter import *
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap import *
import tkinter.font as font
from back_end import *


def call_backend(event=None):
    """
   when called fills listbox up with items retrieved from back_end.py
   """
    global api_foods
    api_foods = callAPI(API_KEY, food_entry.get(), food_category_val.get())
    # for food in api_foods:
    # TODO FILTER DUPLICATES
    api_food_listbox.delete(0, END)
    for food in api_foods:
        api_food_listbox.insert('end', food.APIprint())


def set_expiration_date(event=None):
    """
   setting expiration dates
   """
    # popup
    if inventory_food_listbox.curselection():
        popup = Toplevel(frame2)
        popup.geometry("500x500")
        popup.title("Expiration Date")
        popup_label = Label(popup)
        label_text = "Enter expiration date: "
        popup_label.grid(row=1, column=2, padx=2, pady=2)
        popup_label.config(text=label_text)
        # date widget
        # expire_cal = DateEntry(popup, width=12, background='DarkOrange4',
        # foreground='white', borderwidth=2, year=2023)
        expire_cal = tb.DateEntry(popup, dateformat="%m/%d/%y", bootstyle='primary')
        expire_cal.grid(row=1, column=3, padx=2, pady=2)

        # function to set date for food item
        def submit_and_close(event=None):
            index = int(inventory_food_listbox.curselection()[0])
            inventory_food_list[index].setDate(expire_cal.entry.get())  # get date chosen from calendar widget
            writeToJson(inventory_food_list)
            inventory_food_listbox.delete(index)
            inventory_food_listbox.insert(index, inventory_food_list[index])
            color = set_expiration_status(inventory_food_list[index])
            inventory_food_listbox.itemconfig(index, fg=color)
            popup.destroy()  # Close the popup

        submit_btn = tk.Button(popup, text="Submit Date", command=submit_and_close)
        submit_btn.grid(row=2, column=3, padx=2, pady=2)
        popup.bind('<Return>', submit_and_close)


def set_expiration_status(food):
    if food.getDate() != '':
        food_date = datetime.strptime(food.getDate(), "%m/%d/%y").date()
        difference = (food_date - datetime.now().date()).days
        if difference < 0:
            return 'red'
        elif difference < 3:
            return '#FFD700'
    return 'white'


# -----Functions to control Inventory ------
def cart_to_inventory():
    """
    send items in cart to inventory and clear cart
    """
    if len(shopping_cart_food_list) > 0:
        for food in shopping_cart_food_list:
            in_inv = False
            for current_food in inventory_food_list:
                if current_food.getId() == food.getId():
                    current_food.addQuantity(food.getQuantity())
                    id_index = inventory_food_list.index(current_food)
                    inventory_food_listbox.delete(id_index)
                    inventory_food_listbox.insert(id_index, inventory_food_list[id_index])
                    in_inv = True
                    break
            if not in_inv:
                inventory_food_listbox.insert("end", food)
                color = set_expiration_status(food)
                inventory_food_listbox.itemconfig('end', fg=color)
                new_food = copy.deepcopy(food)
                inventory_food_list.append(new_food)

        shopping_cart_food_list.clear()
        shopping_cart_listbox.delete(0, tk.END)
        writeToJson(inventory_food_list)
        messagebox.showinfo("Alert!", "Shopping cart submitted!")
    else:
        messagebox.showwarning("Warning!", "Shopping cart is empty!")


def json_to_inventory():
    foods = readJson()
    for food in foods:
        inventory_food_list.append(food)
        inventory_food_listbox.insert('end', food)
        color = set_expiration_status(food)
        inventory_food_listbox.itemconfig('end', fg=color)


def clear_inventory(event=None):
    inventory_food_list.clear()
    inventory_food_listbox.delete(0, tk.END)
    clearJson()


def delete_item_from_inventory(event=None):
    """delete item from shopping cart"""
    if inventory_food_listbox.curselection():
        index = int(inventory_food_listbox.curselection()[0])
        inventory_food_list.pop(index)
        inventory_food_listbox.delete(index)
        delFromJson(index)


# ----Functions to move items between cart and search results ------

def add_item(event=None):
    """insert item into shopping cart"""
    if api_food_listbox.curselection():
        index = int(api_food_listbox.curselection()[0])
        food_id = api_foods[index].getId()
        for food in shopping_cart_food_list:
            if food_id == food.getId():
                id_index = shopping_cart_food_list.index(food)
                shopping_cart_food_list[id_index].addQuantity(1)
                shopping_cart_listbox.delete(id_index)
                shopping_cart_listbox.insert(id_index, shopping_cart_food_list[id_index])
                return
        # Create a copy of the food object to avoid modifying the original in api_foods
        new_food = copy.deepcopy(api_foods[index])
        shopping_cart_food_list.append(new_food)  # put food obj in cart food list
        shopping_cart_listbox.insert('end', new_food)  # add to listbox


def delete_item_from_cart(event=None):
    """delete item from shopping cart"""
    if shopping_cart_listbox.curselection():
        index = int(shopping_cart_listbox.curselection()[0])
        if shopping_cart_food_list[index].getQuantity() > 1:
            shopping_cart_food_list[index].removeQuantity(1)
            shopping_cart_listbox.delete(index)
            shopping_cart_listbox.insert(index, shopping_cart_food_list[index])
            shopping_cart_listbox.selection_set(index)
        else:
            shopping_cart_food_list.pop(index)
            shopping_cart_listbox.delete(index)
            shopping_cart_listbox.selection_set(index)


# store food objects
shopping_cart_food_list = []
inventory_food_list = []
# Create an instance of tkinter frame or window
win = Window(themename='superhero')
# Set the size of the window
win.geometry("1920x1080")
# win.state("zoomed")
# win.resizable(0, 0)
# set title and logo
win.title("Conscious Grocery Shopping")
win.iconbitmap("icon.ico")
# Add Frames
frame = Frame(win)
frame2 = Frame(win)


def change_to_search():
    frame.pack(fill='both', expand=1)
    frame2.pack_forget()


def change_to_inventory():
    frame2.pack(fill=X, expand=0)
    frame.pack_forget()


# Create style objects for buttons
sto = Style()
st1 = Style()
st2 = Style()
st3 = Style()
st4 = Style()
# configure styles for buttons
sto.configure('W.TButton', font=('Arial', 18, 'underline'))
st1.configure('C.success.TButton', font=('Arial', 14))
st2.configure('A.TButton', font=('Arial', 14))
st3.configure('D.danger.TButton', font=('Arial', 14))
st4.configure('E.warning.TButton', font=('Arial', 14))
# create side panel buttons
Button(frame, text="Go to Inventory",
       command=change_to_inventory, style='W.TButton').grid(row=0, column=0, padx=15)
Button(frame2, text="Go to Search",
       command=change_to_search, style='W.TButton').grid(row=0, column=0, padx=15)

# load the start screen
change_to_search()

'''---SEARCH WINDOW---'''

# Title for search window
banner = Label(frame,
               text="Hey there! Welcome to Conscious Grocery Shopping!", font='Helvetica 22 bold', )
banner.grid(row=0, column=1, padx=200, pady=10, columnspan=4)
# Entry label for search
entry_Label = Label(frame, text="Enter Food Item: ", font='Aerial 18')
entry_Label.grid(row=2, column=1, padx=(50, 0), pady=50, sticky='w')
# Entry widget for search
food_entry = tb.Entry(frame, font=20)
food_entry.grid(row=2, column=1, padx=(250, 0), pady=10, sticky='e')
food_entry.bind("<Return>", call_backend)

# Food Category OptionMenu
food_category_val = tk.StringVar()
food_category_val.set("All Categories")
option_menu = tk.OptionMenu(frame, food_category_val, *food_categories)
option_menu.grid(row=2, column=3, padx=(50, 0), pady=10, sticky='w')
# Search Button
search_btn = Button(frame, text='Search', style='C.success.TButton', command=call_backend)
search_btn.grid(row=2, column=3, padx=(50, 0), pady=10)
# export button
export_btn = Button(frame, text="Finalize Cart", style='E.warning.TButton', command=cart_to_inventory)
export_btn.grid(row=2, column=3, padx=10, sticky='e')
# API_Food_Listbox title
api_label = Label(frame, text="Search Results ", font='Arial 16', foreground='orange')
api_label.grid(row=4, column=1, columnspan=2, pady=(5, 20))
# Shopping cart title
shopping_cart_label = Label(frame, text="Shopping Cart ", font='Arial 16', foreground='orange')
shopping_cart_label.grid(row=4, column=3, columnspan=2, pady=(5, 20))
# ListBox Labels
food_name_label1 = Label(frame, text="Food Name", font='Arial 14')
food_name_label1.grid(row=5, column=1, padx=(20, 0), pady=5, sticky='w')
calorie_label1 = Label(frame, text="Calories", font='Arial 14')
calorie_label1.grid(row=5, column=1, padx=(350, 0), pady=5)
food_name_label2 = Label(frame, text="Food Name", font='Arial 14')
food_name_label2.grid(row=5, column=3, padx=(50, 250), pady=5, sticky='w')
calorie_label2 = Label(frame, text="Calories", font='Arial 14')
calorie_label2.grid(row=5, column=3, padx=(350, 100), pady=5)
quantity_label = Label(frame, text="Quantity", font='Arial 14')
quantity_label.grid(row=5, column=3, pady=5, sticky='e')
# API Search Result Listbox
api_food_listbox = Listbox(frame, height=30, width=60, font="TkFixedFont")
api_food_listbox.grid(row=6, column=1, padx=10, columnspan=2)
api_food_listbox.bind("<Double 1>", add_item)
# Shopping Cart Listbox
shopping_cart_listbox = Listbox(frame, height=30, width=60, font="TkFixedFont")
shopping_cart_listbox.grid(row=6, column=3, padx=5, columnspan=2)
shopping_cart_listbox.bind("<Double 1>", delete_item_from_cart)

# Add item to cart button
add_item_btn = Button(frame, text="Add Item to Cart", style='A.TButton', command=add_item)
add_item_btn.grid(row=7, column=1, padx=(150, 0), pady=15)
# Button to delete item from shopping cart
delete = Button(frame, text="Remove Item from Cart", style='D.danger.TButton', command=delete_item_from_cart)
delete.grid(row=7, column=3, padx=(150, 0), pady=15)

'''---INVENTORY WINDOW---'''

# configure the grid layout
frame2.columnconfigure(2, weight=4)
frame2.columnconfigure(1, weight=3)
# inventory window title
inventory_Title = Label(frame2, text="Your Current Pantry Items", font='Helvetica 22 bold')
inventory_Title.grid(row=0, column=1, pady=10)
# ListBox Labels
food_name_label = Label(frame2, text="Food Name", font='Arial 14')
food_name_label.grid(row=1, column=1, padx=(350, 0), pady=(50, 0), sticky='w')
calorie_label = Label(frame2, text="Calories", font='Arial 14')
calorie_label.grid(row=1, column=1, padx=(80, 0), pady=(50, 0))
quantity_label = Label(frame2, text="Quantity", font='Arial 14')
quantity_label.grid(row=1, column=1, padx=(300, 0), pady=(50, 0))
expiration_label = Label(frame2, text="Expiration Date", font='Arial 14')
expiration_label.grid(row=1, column=1, padx=(600, 0), pady=(50, 0))
# Current Items Listbox
inventory_food_listbox = Listbox(frame2, height=30, width=75, font="TkFixedFont")
inventory_food_listbox.grid(row=2, column=1, pady=15, rowspan=3)
inventory_food_listbox.bind("<Double 1>", set_expiration_date)

# Expiration date button
expire_date_btn = tb.Button(frame2, text="Set Expiration Date", style='A.TButton',
                            command=set_expiration_date)
expire_date_btn.grid(row=2, column=1, padx=(1050, 0), pady=(80, 0))

# delete item button
del_from_inv_btn = tb.Button(frame2, text="Delete item", style='E.warning.TButton',
                             command=delete_item_from_inventory)
del_from_inv_btn.grid(row=2, column=1, padx=(970, 0), pady=(200, 0))
# clear inventory button
clr_inv_btn = Button(frame2, text="Clear Inventory", style='D.danger.TButton', command=clear_inventory)
clr_inv_btn.grid(row=3, column=1, padx=(1010, 0), pady=(0, 330))

json_to_inventory()

win.mainloop()
