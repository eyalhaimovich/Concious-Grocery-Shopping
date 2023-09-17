# Concious Grocery Shopping - APCV498
This project will develop an computer application for improving the groceryshopping experience. 
The application will allow users to input foods and recipes into a shopping list. 
Upon completion of the list, the app will show the nutrition provided by the shopping list.
It will offer notifictions of food expiration dates, present nutritional information in a piechart,
and keep history of previous groceries- allowing reuse for the next shopping trip.

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
            str: food name 
            str: expiration date (cooked / raw) 
            ints: calories, fat, carbs, protein
        Reminders/UI/Storage:
            Upcoming Expiration date (should/can we do this on a Desktop application?)
            Display macros for day/week maybe as a nice piechart
            Local Storage for retaining grocery data
        Disribution:
            (idea for converting app to setup wizard) https://www.youtube.com/watch?v=p3tSLatmGvU



