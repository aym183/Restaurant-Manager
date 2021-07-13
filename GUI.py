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


# This rather long dictionary contaning entries for each ORDER ID which is first assigned to 0. Once user with that ORDER ID places an order, the value is replaced with the total of their order 
# For each customer, ORDER ID is uniqueu
order_history = {'100': 0, '101': 0, '102': 0,  '103': 0,  '104': 0, '105': 0, '106': 0, '107': 0,'108': 0,'109': 0,'110': 0,
 '111': 0,'112': 0,'113': 0,'114': 0,'115': 0,'116': 0,'117': 0, '118': 0, '119': 0, '120':0,
 '121': 0, '122': 0, '123': 0,'124': 0, '125': 0,'126': 0,'127': 0,'128': 0,'129': 0,'130': 0,
 '131': 0,'132': 0,'133': 0,'134': 0,'135': 0,'136': 0,'137': 0,'138': 0,'139': 0,'140': 0,
 '141': 0,'142': 0, '143': 0,'144': 0,'145': 0,'146': 0,'147': 0,'148': 0,'149': 0,'150': 0,
 '151': 0,'152': 0,'153': 0,'154': 0,'155': 0,'156': 0,'157': 0,'158': 0,'159': 0,'160': 0,
 '161': 0,'162': 0,'163': 0,'164': 0,'165': 0,'166': 0,'167': 0,'168': 0,'169': 0,'170': 0,
 '171': 0,'172': 0,'173': 0,'174': 0,'175': 0,'176': 0,'177': 0,'178': 0,'179': 0,'180': 0,
 '181': 0,'182': 0,'183': 0,'184': 0,'185': 0,'186': 0,'187': 0,'188': 0,'189': 0,'190': 0,
 '191': 0,'192': 0,'193': 0,'194': 0,'195': 0,'196': 0,'197': 0,'198': 0,'199': 0,'200': 0,
 '201': 0,'202': 0,'203': 0,'204': 0,'205': 0,'206': 0,'207': 0,'208': 0,'209': 0,'210': 0,
 '211': 0,'212': 0,'213': 0,'214': 0,'215': 0,'216': 0,'217': 0,'218': 0,'219': 0,'220': 0,
 '221': 0,'222': 0,'223': 0,'224': 0,'225': 0,'226': 0,'227': 0,'228': 0,'229': 0,'230': 0,
 '231': 0,'232': 0,'233': 0,'234': 0,'235': 0,'236': 0,'237': 0,'238': 0,'239': 0,'240': 0,
 '241': 0,'242': 0,'243': 0,'244': 0,'245': 0,'246': 0,'247': 0,'248': 0,'249': 0,'250': 0,
 '251': 0,'252': 0,'253': 0,'254': 0,'255': 0,'256': 0,'257': 0,'258': 0,'259': 0,'260': 0,
 '261': 0,'262': 0,'263': 0,'264': 0,'265': 0,'266': 0,'267': 0,'268': 0,'269': 0,'270': 0,
 '271': 0,'272': 0,'273': 0,'274': 0,'275': 0,'276': 0,'277': 0,'278': 0,'279': 0,'280': 0,
 '281': 0,'282': 0,'283': 0,'284': 0,'285': 0,'286': 0,'287': 0,'288': 0,'289': 0,'290': 0,
 '291': 0,'292': 0,'293': 0,'294': 0,'295': 0,'296': 0,'297': 0,'298': 0,'299': 0,'300': 0,
 '301': 0,'302': 0,'303': 0,'304': 0,'305': 0,'306': 0,'307': 0,'308': 0,'309': 0,'310': 0,
 '311': 0,'312': 0,'313': 0,'314': 0,'315': 0,'316': 0,'317': 0,'318': 0,'319': 0,'320': 0,
 '321': 0,'322': 0,'323': 0,'324': 0,'325': 0,'326': 0,'327': 0,'328': 0,'329': 0,'330': 0,
 '331': 0,'332': 0,'333': 0,'334': 0,'335': 0,'336': 0,'337': 0,'338': 0,'339': 0,'340': 0,
 '341': 0,'342': 0,'343': 0,'344': 0,'345': 0,'346': 0,'347': 0,'348': 0,'349': 0,'350': 0,
 '351': 0,'352': 0,'353': 0,'354': 0,'355': 0,'356': 0,'357': 0,'358': 0,'359': 0,'360': 0,
 '361': 0,'362': 0,'363': 0,'364': 0,'365': 0,'366': 0,'367': 0,'368': 0,'369': 0,'370': 0,
 '371': 0,'372': 0,'373': 0,'374': 0,'375': 0,'376': 0,'377': 0,'378': 0,'379': 0,'380': 0,
 '381': 0,'382': 0,'383': 0,'384': 0,'385': 0,'386': 0,'387': 0,'388': 0,'389': 0,'390': 0,
 '391': 0,'392': 0,'393': 0,'394': 0,'395': 0,'396': 0,'397': 0,'398': 0,'399': 0,'400': 0,
 '401': 0,'402': 0,'403': 0,'404': 0,'405': 0,'406': 0,'407': 0,'408': 0,'409': 0,'410': 0,
 '411': 0,'412': 0,'413': 0,'414': 0,'415': 0,'416': 0,'417': 0,'418': 0,'419': 0,'420': 0,
 '421': 0,'422': 0,'423': 0,'424': 0,'425': 0,'426': 0,'427': 0,'428': 0,'429': 0,'430': 0,
 '431': 0,'432': 0,'433': 0,'434': 0,'435': 0,'436': 0,'437': 0,'438': 0,'439': 0,'440': 0,
 '441': 0,'442': 0,'443': 0,'444': 0,'445': 0,'446': 0,'447': 0,'448': 0,'449': 0,'450': 0,
 '451': 0,'452': 0,'453': 0,'454': 0,'455': 0,'456': 0,'457': 0,'458': 0,'459': 0,'460': 0,
 '461': 0,'462': 0,'463': 0,'464': 0,'465': 0,'466': 0,'467': 0,'468': 0,'469': 0,'470': 0,
 '471': 0,'472': 0,'473': 0,'474': 0,'475': 0,'476': 0,'477': 0,'478': 0,'479': 0,'480': 0,
 '481': 0,'482': 0,'483': 0,'484': 0,'485': 0,'486': 0,'487': 0,'488': 0,'489': 0,'490': 0,
 '491': 0,'492': 0,'493': 0,'494': 0,'495': 0,'496': 0,'497': 0,'498': 0,'499': 0,'500': 0,
 '501': 0,'502': 0,'503': 0,'504': 0,'505': 0,'506': 0,'507': 0,'508': 0,'509': 0,'510': 0,
 '511': 0,'512': 0,'513': 0,'514': 0,'515': 0,'516': 0,'517': 0,'518': 0,'519': 0,'520': 0,
 '521': 0,'522': 0,'523': 0,'524': 0,'525': 0,'526': 0,'527': 0,'528': 0,'529': 0,'530': 0,
 '531': 0,'532': 0,'533': 0,'534': 0,'535': 0,'536': 0,'537': 0,'538': 0,'539': 0,'540': 0,
 '541': 0,'542': 0,'543': 0,'544': 0,'545': 0,'546': 0,'547': 0,'548': 0,'549': 0,'550': 0,
 '551': 0,'552': 0,'553': 0,'554': 0,'555': 0,'556': 0,'557': 0,'558': 0,'559': 0,'560': 0,
 '561': 0,'562': 0,'563': 0,'564': 0,'565': 0,'566': 0,'567': 0,'568': 0,'569': 0,'570': 0,
 '571': 0,'572': 0,'573': 0,'574': 0,'575': 0,'576': 0,'577': 0,'578': 0,'579': 0,'580': 0,
 '581': 0,'582': 0,'583': 0,'584': 0,'585': 0,'586': 0,'587': 0,'588': 0,'589': 0,'590': 0,
 '591': 0,'592': 0,'593': 0,'594': 0,'595': 0,'596': 0,'597': 0,'598': 0,'599': 0,'600': 0,
 '601': 0,'602': 0,'603': 0,'604': 0,'605': 0,'606': 0,'607': 0,'608': 0,'609': 0,'610': 0,
 '611': 0,'612': 0,'613': 0,'614': 0,'615': 0,'616': 0,'617': 0,'618': 0,'619': 0,'620': 0,
 '621': 0,'622': 0,'623': 0,'624': 0,'625': 0,'626': 0,'627': 0,'628': 0,'629': 0,'630': 0,
 '631': 0,'632': 0,'633': 0,'634': 0,'635': 0,'636': 0,'637': 0,'638': 0,'639': 0,'640': 0,
 '641': 0,'642': 0,'643': 0,'644': 0,'645': 0,'646': 0,'647': 0,'648': 0,'649': 0,'650': 0,
 '651': 0,'652': 0,'653': 0,'654': 0,'655': 0,'656': 0,'657': 0,'658': 0,'659': 0,'660': 0,
 '661': 0,'662': 0,'663': 0,'664': 0,'665': 0,'666': 0,'667': 0,'668': 0,'669': 0,'670': 0,
 '671': 0,'672': 0,'673': 0,'674': 0,'675': 0,'676': 0,'677': 0,'678': 0,'679': 0,'680': 0,
 '681': 0,'682': 0,'683': 0,'684': 0,'685': 0,'686': 0,'687': 0,'688': 0,'689': 0,'690': 0,
 '691': 0,'692': 0,'693': 0,'694': 0,'695': 0,'696': 0,'697': 0,'698': 0,'699': 0,'700': 0,
 '701': 0,'702': 0,'703': 0,'704': 0,'705': 0,'706': 0,'707': 0,'708': 0,'709': 0,'710': 0,
 '711': 0,'712': 0,'713': 0,'714': 0,'715': 0,'716': 0,'717': 0,'718': 0,'719': 0,'720': 0,
 '721': 0,'722': 0,'723': 0,'724': 0,'725': 0,'726': 0,'727': 0,'728': 0,'729': 0,'730': 0,
 '731': 0,'732': 0,'733': 0,'734': 0,'735': 0,'736': 0,'737': 0,'738': 0,'739': 0,'740': 0,
 '741': 0,'742': 0,'743': 0,'744': 0,'745': 0,'746': 0,'747': 0,'748': 0,'749': 0,'750': 0,
 '751': 0,'752': 0,'753': 0,'754': 0,'755': 0,'756': 0,'757': 0,'758': 0,'759': 0,'760': 0,
 '761': 0,'762': 0,'763': 0,'764': 0,'765': 0,'766': 0,'767': 0,'768': 0,'769': 0,'770': 0,
 '771': 0,'772': 0,'773': 0,'774': 0,'775': 0,'776': 0,'777': 0,'778': 0,'779': 0,'780': 0,
 '781': 0,'782': 0,'783': 0,'784': 0,'785': 0,'786': 0,'787': 0,'788': 0,'789': 0,'790': 0,
 '791': 0,'792': 0,'793': 0,'794': 0,'795': 0,'796': 0,'797': 0,'798': 0,'799': 0,'800': 0,
 '801': 0,'802': 0,'803': 0,'804': 0,'805': 0,'806': 0,'807': 0,'808': 0,'809': 0,'810': 0,
 '811': 0,'812': 0,'813': 0,'814': 0,'815': 0,'816': 0,'817': 0,'818': 0,'819': 0,'820': 0,
 '821': 0,'822': 0,'823': 0,'824': 0,'825': 0,'826': 0,'827': 0,'828': 0,'829': 0,'830': 0,
 '831': 0,'832': 0,'833': 0,'834': 0,'835': 0,'836': 0,'837': 0,'838': 0,'839': 0,'840': 0,
 '841': 0,'842': 0,'843': 0,'844': 0,'845': 0,'846': 0,'847': 0,'848': 0,'849': 0,'850': 0,
 '851': 0,'852': 0,'853': 0,'854': 0,'855': 0,'856': 0,'857': 0,'858': 0,'859': 0,'860': 0,
 '861': 0,'862': 0,'863': 0,'864': 0,'865': 0,'866': 0,'867': 0,'868': 0,'869': 0,'870': 0,
 '871': 0,'872': 0,'873': 0,'874': 0,'875': 0,'876': 0,'877': 0,'878': 0,'879': 0,'880': 0,
 '881': 0,'882': 0,'883': 0,'884': 0,'885': 0,'886': 0,'887': 0,'888': 0,'889': 0,'890': 0,
 '891': 0,'892': 0,'893': 0,'894': 0,'895': 0,'896': 0,'897': 0,'898': 0,'899': 0,'900': 0,
 '901': 0,'902': 0,'903': 0,'904': 0,'905': 0,'906': 0,'907': 0,'908': 0,'909': 0,'910': 0,
 '911': 0,'912': 0,'913': 0,'914': 0,'915': 0,'916': 0,'917': 0,'918': 0,'919': 0,'920': 0,
 '921': 0,'922': 0,'923': 0,'924': 0,'925': 0,'926': 0,'927': 0,'928': 0,'929': 0,'930': 0,
 '931': 0,'932': 0,'933': 0,'934': 0,'935': 0,'936': 0,'937': 0,'938': 0,'939': 0,'940': 0,
 '941': 0,'942': 0,'943': 0,'944': 0,'945': 0,'946': 0,'947': 0,'948': 0,'949': 0,'950': 0,
 '951': 0,'952': 0,'953': 0,'954': 0,'955': 0,'956': 0,'957': 0,'958': 0,'959': 0,'960': 0,
 '961': 0,'962': 0,'963': 0,'964': 0,'965': 0,'966': 0,'967': 0,'968': 0,'969': 0,'970': 0,
 '971': 0,'972': 0,'973': 0,'974': 0,'975': 0,'976': 0,'977': 0,'978': 0,'979': 0,'980': 0,
 '981': 0,'982': 0,'983': 0,'984': 0,'985': 0,'986': 0,'987': 0,'988': 0,'989': 0,'990': 0,
 '991': 0,'992': 0,'993': 0,'994': 0,'995': 0,'996': 0,'997': 0,'998': 0,'999': 0}


# Below are the classes used for the program, The first class is the Restaurant class 
# Thee second one is the Order Class which inherits the properties from the Restaurant class
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



    # This is the first nested function used. It helps manipulate each of the dropdown menus, also disabling irrelevant menus for a particular operation
    # For example, if user wants to reserve a table, the relevant dropdown menus will be modified to contain the data that the user needs for reserving the table and all the irrelevant menus and buttons will be disabled  
         
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
    
    myLabel4 = Label(root, text="Branch/ORDER ID:") 
    myLabel4.grid(row=1,column=0)



    Second_Dropdown = ttk.Combobox(root, value = [" "])
    Second_Dropdown.current = (0)
    Second_Dropdown.bind('<<ComboboxSelected>>', pick_Action )
    Second_Dropdown.grid(row=1, column=1)

    myLabel3 = Label(root, text="Table No/ Items:") 
    myLabel3.grid(row=1,column=2)

    Third_Dropdown = ttk.Combobox(root, value = [" "])
    Third_Dropdown.current = (0)
    Third_Dropdown.bind('<<ComboboxSelected>>', pick_Action )
    Third_Dropdown.grid(row=1, column=3)

    myLabel3 = Label(root, text="Quantity:") 
    myLabel3.grid(row=2,column=0)

    Fourth_Dropdown = ttk.Combobox(root, value = [" "])
    Fourth_Dropdown.current = (0)
    Fourth_Dropdown.grid(row=2, column=1)
        
        
    # This is the nested function that takes care of the adding to cart function when placing order
    # The user will have to select the ORDER ID that is given to the user once the table is reserved
    # Then select the items and quantity of it and add it to cart and click "Add To Cart"
    
    def Add_to_Cart():

        # If user doesn't select one of the options, an error message is shown
        if len(Second_Dropdown.get())== 0 or len(Third_Dropdown.get())== 0 or len(Fourth_Dropdown.get())== 0:
            messagebox.showinfo("Error", "Please fill in the boxes before proceeding")
            #len(my_combo.get())!=0 
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
        
                print(data)
        
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
        
        

    # This is the nested function that takes care of placing the order
    # After the user selects all the items they need, they click the "Place Order" button
    # Once Order Placed, The User Gets A Message Indicating Successful Order
    
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
        
            print(data)
            tax = order_history.get(Order_id_input)*0.15
            total = order_history.get(Order_id_input)
            tax_total = total + tax

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
                        
                        print("\n")
             

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
    100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199,
    200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299,
    300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 
    400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 
    500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 
    600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 
    700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 
    800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 
    900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 950, 951, 952, 953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 970, 971, 972, 973, 974, 975, 976, 977, 978, 979, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989, 990, 991, 992, 993, 994, 995, 996, 997, 998, 999, 1000
   
    ]



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

    myLabel6 = Label(root, text="   ") 
    myLabel6.grid(row=11,column=1)



    root.mainloop()

if __name__ == "__main__":
    GUI()
