# Concious Grocery Shopping - APCV498
This project will develop a computer application for improving the grocery shopping experience. 
The application will allow users to input foods and recipes into a shopping list. 
Upon completion of the list, the app will show the nutrition provided by the shopping list.
It will offer notifications of food expiration dates, present nutritional information in a pie chart,
and keep history of previous groceries; allowing reuse for the next shopping trip.

## Features:
        Requirements:
            Store user inputted data.
            Utilize a database for food nutritional content and expiration dates.
            Allow users to add, rename, and edit customized foods and grocery lists.
            Notify the user when food items are about to expire.
            UI must be simple to use and display the grocery data aesthetically.
            Notify the user if current groceries do not meet set nutritional goals.
##  Dos:
    GUI:
        tkinter (themes?) https://www.youtube.com/watch?v=mop6g-c5HEY
        PyQt5/6 
        Electron / webapp (web design made into a downloadable app) https://github.com/python-eel/Eel
    User Inputs:
        str: food
        int/float: quantity of food
        int: how low long should this shopping trip last
        float: TDEE how many calories should eat per day/week (diet goals)
    Food Class: 
        below values should ideally be found in a database API 
        https://fdc.nal.usda.gov/api-guide.html
        https://www.eatbydate.com/
        str: food name 
        str: expiration date (cooked / raw) 
        ints: calories, fat, carbs, protein
    Reminders/UI/Storage:
        Upcoming Expiration date (should/can we do this on a Desktop application?)
        Display macros for day/week maybe as a nice piechart
        Local Storage for retaining grocery data
    Disribution:
        (idea for converting app to setup wizard) https://www.youtube.com/watch?v=p3tSLatmGvU


### IDEALLY HAVE FUNCTIONING APP BY WEEK 8

## Week 1 Meeting Goals:
    FRONT END:
    Set up basic GUI
        * Enough to see what's going on for now
        * Food input, Food quantity, submit button to save food & qauntaity in backend.

    BACK END:
    Set up Python file & API
        * Make a class for foodType 
        * Connect to database: https://fdc.nal.usda.gov/api-guide.html

## Week 2 Meeting:
    COMPLETED:
        Base API data parsing into wanted vairables / desired output
        Base GUI created and connected parsed API to show as output on the GUI
    MEETING:
        Decided on look for GUI (added template look image to gitHub)
        Decided (mostly) on needed variables to pull from API:
            Data Cateogry, food description, Serving size (100g)
        Expiration dates start by manual input by user, later add template food recommendations (AI?)
    NEXT WEEK:
        FRONT END:
            Set up the 3 tabs (bottom of template img)
            buttons for search, food category, search, food item pop up.
            General work on UI to reach decided functionality
            -- Figure out how to send user click to return item id to back end
        BACK END:
            Seperate functions to callAPI for different purposes: 
                filter foodNutrition to relevant data only
                fliter by dataType to SR Legacy only
                search by foodcategory chosen by user
                new API call to return only specific item (by ID probably) when user clicks item

## Week 3 Meeting:
    BACK END:
        Satisfactory Functionality
        Add option FoodCategory (default 'all') for user to choose
        Figure out way to sort the food items
        *FOR NOW WE'LL BE FOCUSING ON FRONT END*
    FRONT END:
        Outputting each food on it's own line in format name : [macros]
            (adjust the output in back_end FoodItem __str__) * Eyal
        Don't let users edit in textbox - Look into other ways to display food items * Christina
## 10/22/23
    BACK END:
        Possibly add calendar event functions to back_end if it makes sense to do so. 
    FRONT END:
        Look into/research Tkcalendar library for expiraton date event reminders
            --Create option for users to add an expiration date manually for a food item

        General work on GUI improvements
## 10/28/23
    COMPLETED:
        Date Entry widget created to add dates to food items
        GUI improvements on Search/Shopping Cart window
    NEXT TASKS: 
        FRONT END:
            Issues to solve: 
                * When adding a date to a food item in current inventory,
                    it will append date to end of string instead of replacing or updating the date.
                ex: Apple  35 Calories 10/28/23 10/29/23 10/28/23... and so on.
            Create function to save current inventory of foods to a text file
                -- Create function so the file can be "uploaded" back into the app.
            Create reminders for the expiration dates
                --Have code check if expiration date(s) are current date or not
                --Alert user if a food expires on current day or in the coming days
            GUI improvements and styling