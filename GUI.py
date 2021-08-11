'''
This is my Restaurant Management System. It has been done using Python(OOP), sqlite3, tkinter and matplotlib
It gives the user the several functionalites such as Reserving a table, Placing an Order, Checking all the reserved tables
and they can also check which items on the menu are most popular.
2 SQL TABLES USED -> Reserved (Location, TableNo, ORDERID) [Keeps the currently reserved tables in it] , ORDERS (ORDERID, Total, TaxTotal) [Places Order Queries (only customers that reserved a table , with their ORDER ID, Orders can be placed)]
'''

# Below are the imports required for this program
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
import random
import matplotlib.pyplot as plt
import numpy as np


# The dictionary that contains number of tables each Branch posseses 
No_of_Tables = {"London": 6, "Liverpool": 5, "Manchester": 8, "Berlin": 10}


# The dictionary containing price of each item
Items = {"Pizza": 30, "Pasta": 50, "Steak": 100, "Salad": 40, "Calzone": 20, "Cake": 30}


# The dictionary that counts everytime each item is being ordered. It is used later on in forming the graph for "Most Popular Items"
Items_counter = {"Pizza": 0, "Pasta": 0, "Steak": 0, "Salad": 0, "Calzone": 0, "Cake": 0}


''' This rather long dictionary contaning entries for each ORDER ID which is first assigned to 0. Once user with that ORDER ID places an order, the value is replaced with the total of their order 
    For each customer, ORDER ID is unique '''

order_history = {}

for i in range(100, 1001):
    order_history['{}'.format(i)]= 0
    
    



''' Below are the classes used for the program, The first class is the Restaurant class 
    The second one is the Order Class which inherits the properties from the Restaurant class '''
class Restaurant():
     
    def __init__(self,branch, tableNo):
        
        self.branch = branch
        self.tableNo = tableNo
        
        
class Order(Restaurant):
    
    def __init__(self, branch, tableNo):    
        super().__init__(branch, tableNo)
        
        self._orderNo = None
        self._total = 0

    #All getter/setter methods used
    def table(self):
        return self.table
    
    def get_orderNo(self):
        return self._orderNo
    
    def set_orderNo(self, value):
        self._orderNo = value
    
    def get_total(self):
        return self._total
    
    def set_total(self, value):
        self._total = value
    


# This is the main function used in the program which contains all the operations and nested functionns for sub operations
def GUI():
    
    root = Tk()
    root.title("Restaurant Manager")
    root.geometry('1250x700')
    

    my_listbox = Listbox(root, bg = 'coral', height = 30, width = 80)
    my_listbox.grid(row = 12, column =1)

    Welcome = "Hi, Welcome To The Sea Restaurant!"
    my_listbox.insert(END, Welcome)



    ''' This is the first nested function used. It helps manipulate each of the dropdown menus,
        also disabling irrelevant menus for a particular operation. For example, if user wants to reserve a
        table, the relevant dropdown menus will be modified to contain the data that the user needs for
        reserving the table and all the irrelevant menus and buttons will be disabled ''' 
         
    def pick_Action(e):
        
        if First_Dropdown.get()=="Reserve":
            Second_Dropdown.config(value = Branches)
            
            Second_Dropdown["state"]="normal"
            
            Third_Dropdown["state"]="normal"
            
            Fourth_Dropdown["state"]="disabled"
            
            All_Tables_Button["state"]="disabled"

            Add_To_Cart_Button["state"]="disabled"
            
            Place_Order_Button["state"]="disabled"
            
            Most_Popular_Items_Button["state"]="disabled"
            
            Reserve_Button["state"]="normal"

            
        
            if Second_Dropdown.get()=="London":
            
                Third_Dropdown.config(value = London_tables) 
           
            
            elif Second_Dropdown.get()=="Liverpool":
            
                Third_Dropdown.config(value = Liverpool_tables)
         
            
            elif Second_Dropdown.get()=="Manchester":
            
                Third_Dropdown.config(value = Manchester_tables)
          
            
            elif Second_Dropdown.get()=="Berlin":
            
                Third_Dropdown.config(value = Berlin_tables)
        


        
        elif First_Dropdown.get()=="Place Order":
            
            Second_Dropdown.config(value = Numbers)
            
            Third_Dropdown.config(value = Items_null)
            
            Fourth_Dropdown.config(value = Quantity)
            
            Second_Dropdown["state"]="normal"
            
            Third_Dropdown["state"]="normal"
            
            Fourth_Dropdown["state"]="normal"
            
            Place_Order_Button["state"]="normal"
            
            Add_To_Cart_Button["state"]="normal"
            
            All_Tables_Button["state"]="disabled"
            
            Reserve_Button["state"]="disabled"
            
            Most_Popular_Items_Button["state"]="disabled"


        
        
        elif First_Dropdown.get()=="See All Tables":
            
            Second_Dropdown.config(value = Branches)
            
            Second_Dropdown["state"]="normal"
            
            All_Tables_Button["state"]="normal"
            
            Third_Dropdown["state"]="disabled"
            
            Fourth_Dropdown["state"]="disabled"
            
            Reserve_Button["state"]="disabled"
            
            Add_To_Cart_Button["state"]="disabled"
            
            Place_Order_Button["state"]="disabled"
            
            Most_Popular_Items_Button["state"]="disabled"

 
        elif First_Dropdown.get()=="Most Popular Items":
            
            Second_Dropdown["state"]="disabled"
            
            Third_Dropdown["state"]="disabled"
            
            Fourth_Dropdown["state"]="disabled"
            
            All_Tables_Button["state"]="disabled"
            
            Reserve_Button["state"]="disabled"
            
            Add_To_Cart_Button["state"]="disabled"
            
            Place_Order_Button["state"]="disabled"
            
            Most_Popular_Items_Button["state"]="normal"

            
    # These are the functionalities that the user can use. Once selected, data will be manipulated
    
    Choices =[
    "Reserve",
    "Place Order",
    "See All Tables",
    "Most Popular Items"
    ]

    # Below are the specifications of the modifiable dropdown menus
    
    Action_Label = Label(root, text="Please Select An Action:") 
    Action_Label.grid(row=0,column=0)

    First_Dropdown = ttk.Combobox(root, value = Choices)
    First_Dropdown.current = (0)
    First_Dropdown.bind('<<ComboboxSelected>>', pick_Action )
    First_Dropdown.grid(row=0, column=1)
    
    Branch_OrderID_Label = Label(root, text="Branch/ORDER ID:") 
    Branch_OrderID_Label.grid(row=1,column=0)



    Second_Dropdown = ttk.Combobox(root, value = [" "])
    Second_Dropdown.current = (0)
    Second_Dropdown.bind('<<ComboboxSelected>>', pick_Action )
    Second_Dropdown.grid(row=1, column=1)

    TableNo_Items_Label = Label(root, text="Table No/ Items:") 
    TableNo_Items_Label.grid(row=1,column=2)

    Third_Dropdown = ttk.Combobox(root, value = [" "])
    Third_Dropdown.current = (0)
    Third_Dropdown.bind('<<ComboboxSelected>>', pick_Action )
    Third_Dropdown.grid(row=1, column=3)

    Quantity_Label = Label(root, text="Quantity:") 
    Quantity_Label.grid(row=2,column=0)

    Fourth_Dropdown = ttk.Combobox(root, value = [" "])
    Fourth_Dropdown.current = (0)
    Fourth_Dropdown.grid(row=2, column=1)
        
        
    ''' This is the nested function that takes care of the adding to cart function when placing order
        The user will have to select the ORDER ID that is given to the user once the table is reserved
        Then select the items and quantity of it and add it to cart and click "Add To Cart" '''
    
    def Add_to_Cart():

        # If user doesn't select one of the options, an error message is shown
        if len(Second_Dropdown.get())== 0 or len(Third_Dropdown.get())== 0 or len(Fourth_Dropdown.get())== 0:
            messagebox.showinfo("Error", "Please fill in the boxes before proceeding")
            
        else:
            conn = sqlite3.connect("Restaurant.db")
            c = conn.cursor()
            Order_id_input = Second_Dropdown.get()
            count = 0
            total = 0
         #15% tax is added to total for tax total

        # Checks the ORDERID that user selects and sees if its a valid ORDERID
            c.execute('Select * from Reserved where ORDERID = {};'.format(Order_id_input))
            conn.commit()
            data = c.fetchall()
    
       
    
            if len(data)==0:
                Mistake = "No order with that ID"
                my_listbox.insert(END, Mistake)
        
            else:
                # If  yes, then the user can place the order
                # The user needs to select all options (ORDER ID, Item and quantity all at once)
                Valid = "Valid order!"
                my_listbox.insert(END, Valid)
        
                #print(data)
        
                my_listbox.insert(END, data)
                order_input =  Third_Dropdown.get()
                quantity = Fourth_Dropdown.get()
        
                while count<int(quantity):
            
                    if order_input in Items.keys():
                        Items_counter[order_input]+=1
                        order_history[Order_id_input]+= Items.get(order_input)
                        count+=1
                Output = order_history.get(Order_id_input)    
                my_listbox.insert(END, Items_counter)
                my_listbox.insert(END, Output)
        
        

    ''' This is the nested function that takes care of placing the order
        After the user selects all the items they need, they click the "Place Order" button
        Once Order Placed, The User Gets A Message Indicating Successful Order '''
    
    def Place_Order():
        if len(Third_Dropdown.get())== 0:
            messagebox.showinfo("Error", "Please fill in the boxes before proceeding")
        else:
            conn = sqlite3.connect("Restaurant.db")
            c = conn.cursor()
            Order_id_input = Second_Dropdown.get()

            # Once order placed, The query with the ORDER ID is removed from the Reserved Table and entered into the Orders Table
    
            c.execute('Delete from Reserved where ORDERID = {};'.format(Order_id_input))
            conn.commit()
            data = c.fetchall()
   
       
   
            order_input = Third_Dropdown.get()
        
            Valid = "Order Placed!"
            my_listbox.insert(END, Valid)
        
            #print(data)
            tax = order_history.get(Order_id_input)*0.15
            total = order_history.get(Order_id_input)
            tax_total = total + tax
            total_string = "The Total is {}".format(tax_total)
            my_listbox.insert(END, total_string)
            

            # Once Order placed, it is inserted into the ORDERS table and the dictionary with the corresponding ORDERID value is changed to the total of that order
            script = 'Insert into Orders values(?,?,?);'
            c.execute(script, (Order_id_input, total, tax_total))
            conn.commit()
     
            c.execute('Select * from Orders where ORDERID = {};'.format(Order_id_input))
            conn.commit()
            data = c.fetchall()
            Valid2 = c.fetchall()
            my_listbox.insert(END, Valid2)


    
    # This is the nested function that takes care of Reserving the table for the user
    # After the user selects the "Reserve" action, they select the Branch and TableNo from the 2 enabled dropdown menus and once the Reserve button is clicked, the table is reserved

    def Reserve_table():
        if len(First_Dropdown.get()) ==0 or len(Second_Dropdown.get())==0 or len(Third_Dropdown.get()) == 0:
            messagebox.showinfo("Error", "Please fill in the boxes before proceeding")
        else:
            conn = sqlite3.connect("Restaurant.db")
            c = conn.cursor()    
    
    
            first_input = Second_Dropdown.get()
            table_input = Third_Dropdown.get()
    
    
            if first_input in No_of_Tables.keys():
       
        
                if int(table_input) <= No_of_Tables.get(first_input):
            
            
                  
                    operations = Order(first_input, table_input)
                    operations.set_orderNo(random.randint(100,1000))

             # QUERY TO CHECK IF TABLE IS ALREADY RESERVED
                    c.execute('Select * from Reserved where Location = "{}" and TableNo = {} ;'.format(first_input, table_input))
                    conn.commit()
        
                    data = c.fetchall()
                    if len(data)==0:
                
                        script = 'Insert into Reserved values(?,?,?);'
        
                        c.execute(script, (first_input, table_input, operations.get_orderNo()))
        
                        conn.commit()
                        Reservation = "Table Reserved!"
                
                        my_listbox.insert(END, Reservation)
                

                # If table already reserved, error message shown
                    else:
            
                        Error = "The table is already reserved! The table's below are reserved"
                
                        my_listbox.insert(END, Error)
                        Error2 = "Please select another table"
               
                        my_listbox.insert(END, Error2)
                        
                        #print("\n")
             

    # This is the nested function that takes care of showing the user all the reserved tables
    # After the user selects the "See All Tables" action, they select the Branch and then click the "Show All Tables" button
    
    def show_all_tables():
        if len(First_Dropdown.get())==0 or len(Second_Dropdown.get()) == 0:
            messagebox.showinfo("Error", "Please fill in the boxes before proceeding")
    
        else:
            
            first_input = Second_Dropdown.get()
                
            if first_input in No_of_Tables.keys():
                conn = sqlite3.connect("Restaurant.db")
                c = conn.cursor()
        
       
                c.execute('Select * from Reserved where Location = "{}";'.format(first_input))
                conn.commit()
                data = c.fetchall()
    
               # If no tables currently in use in that branch, Relevant Message Shown
    
                if len(data)==0:
                    No_Use = "No tables are currently in use in this branch"
                    my_listbox.insert(END, No_Use)
            
                else:
                    Use = "Here are all the tables currently being used (Location, Table Number, Order ID):" 
                    my_listbox.insert(END, Use)
                    my_listbox.insert(END, data)
            

     # This is the nested function that takes care of showing the user a bar graph of the most popular items on the menu
     # After the user selects the "Most Popular Items" action, then just click the "Most Popular Items" button and the bar graph appears in a separate window
    def most_popular_items():
    
        Food_items = []
        Selected = []
        Food_items.clear()
        Selected.clear()
        for i in Items_counter.keys():
            Food_items.append(i)
    
        for j in Items_counter.values():
            Selected.append(j)
        ypos = np.arange(len(Food_items))
        plt.xticks(ypos, Food_items)
        plt.ylabel("No Of Times Ordered")
        plt.xlabel("Items")
        plt.title("Most Popular Items")
        plt.ylim([0,30])
        plt.bar(ypos, Selected)
        plt.show()





# Lists below used for the modified dropddown menus

    Branches = [
    "London",
    "Liverpool",
    "Manchester",
    "Berlin"
    ]

    Items_null = [
    'Pizza',
    'Pasta',
    'Steak',
    'Salad',
    'Calzone',
    'Cake'
    ]
    Quantity = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10
    ]

    London_tables =[
    1,
    2,
    3,
    4,
    5,
    6
    ]

    Liverpool_tables =[
    1,
    2,
    3,
    4,
    5
    ]

    Manchester_tables =[
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8
    ]


    Berlin_tables =[
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10
    ]

    Numbers = [
    
   
    ]
    
    for i in range(100,1001):
        Numbers.append(i)



    # All buttons that are used in the program are created below

    Reserve_Button = Button(root, text="Reserve Table", command = Reserve_table ,fg="blue")
    Reserve_Button.grid(row=7, column = 1)

    All_Tables_Button = Button(root, text="Show All Tables",command = show_all_tables,  fg="blue")
    All_Tables_Button.grid(row = 7, column = 2)

    Add_To_Cart_Button = Button(root, text="Add to Cart",command = Add_to_Cart,  fg="blue")
    Add_To_Cart_Button.grid(row=9, column = 1)

    Place_Order_Button = Button(root, text="Place Order",command = Place_Order,  fg="blue")
    Place_Order_Button.grid(row=10, column = 1)
    
    Most_Popular_Items_Button = Button(root, text="Most Popular Items", command = most_popular_items, fg="blue")
    Most_Popular_Items_Button.grid(row=9, column = 2)

    Null_Label = Label(root, text="   ") 
    Null_Label.grid(row=11,column=1)



    root.mainloop()

if __name__ == "__main__":
    GUI()
