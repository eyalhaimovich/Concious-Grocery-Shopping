
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from back_end import *
from tkcalendar import Calendar, DateEntry

def call_backend():
    output = callAPI(API_KEY, food_entry.get(), food_category_val.get())
    food_listbox.delete(0, END)
    for i in output:
        food_listbox.insert('end', i)

def open_popup():
    popup = Toplevel(search_Tab)
    popup.geometry("400x200")
    popup.title("Food Details")
    show = Label(popup)
    show.grid(row=1, column=2, padx=2, pady=2)
    show.config(text=food_listbox.get(ANCHOR))
    pop_btn = Button(popup, text="Add Item", command=insert_list)
    close_btn = Button(popup, text="Close", command=popup.destroy)
    pop_btn.grid(row=2, column=2, padx=2.5, pady=5)
    close_btn.grid(row=2, column=3, padx=2.5, pady=5)


'''insert item into next window in shopping cart'''
def insert_list():
    item = food_listbox.get(food_listbox.curselection())
    shopping_Cart.insert('end', item)


'''delete item in shopping cart'''
def delete_item():
    remove = shopping_Cart.curselection()
    shopping_Cart.delete(remove)


def expiration_date():
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

# send items in shopping cart to inventory tab
def export_list():
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
    #  TABS
    search_Tab = ttk.Frame(parentTab)
    inventory = ttk.Frame(parentTab)
    '''Search and Shopping Cart Window'''
    parentTab.add(search_Tab, text='Search')
    # Search window label config
    search_Label = ttk.Label(search_Tab, text="Search for Food Here")
    search_Label.grid(row=1, column=1, padx=5, pady=5)
    # Food entry label config
    entry_Label = tk.Label(search_Tab, text="Enter Food Item: ", bg='light green')
    entry_Label.grid(row=2, column=1, padx=10, pady=10)
    # Submit search button config
    search_btn = Button(search_Tab, text='Submit', command=call_backend)
    search_btn.grid(row=2, column=4, padx=10, pady=10)

    # widget for user input
    food_entry = tk.Entry(search_Tab)
    food_entry.grid(row=2, column=2, padx=10, pady=10)

    '''ListBox Configuration for search results'''
    food_listbox = Listbox(search_Tab, height=50, width=80)
    food_listbox.grid(row=3, column=2, padx=10, pady=10)
    # "More Details" Button Config
    show_details_btn = Button(search_Tab, text='Show Selected', command=open_popup)
    show_details_btn.grid(row=4, column=1, pady=10)

    '''option menu configuration'''
    food_category_val = tk.StringVar()
    food_category_val.set("All Categories")
    option_menu = tk.OptionMenu(search_Tab, food_category_val, *food_categories)
    option_menu.grid(row=2, column=3)

    '''ListBox Configuration for current shopping list'''
    shopping_Cart = Listbox(search_Tab, height=25, width=50)
    shopping_Cart.grid(row=3, column=4, padx=10, pady=10)
    # Button to add item to shopping cart
    add_item_btn = Button(search_Tab, text="Add Item", command=insert_list)
    add_item_btn.grid(row=3, column=5, padx=10, pady=10)
    # Delete item from shopping cart listbox
    delete = Button(search_Tab, text="Delete Item", command=delete_item)
    delete.grid(row=4, column=5, padx=10, pady=10)
    # send whole list to inventory
    export_btn = Button(search_Tab, text="Submit list to inventory", command=export_list)
    export_btn.grid(row=4, column=6, padx=10, pady=10)


    '''///CURRENT INVENTORY WINDOW CONFIGURATION///'''
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