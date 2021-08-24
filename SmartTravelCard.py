# -*- coding: utf-8 -*-

# ************ SMART TRAVEL CARD ********************

"""
Created on Wed Dec 25 12:19:57 2019

@author: Swetha Manoharan
"""

# In[1]:

# import libraries
#import pandas as pd
import sqlite3 as sql
import datetime as dt
#import tkinter as tk
from dateutil.relativedelta import relativedelta

def insert_swipe_in():
    f = open("htmltraveldata_in.txt", "r")
    tmp = f.read().splitlines()
    
    if(len(tmp)==0):
        status = 'DontRead;FileEmpty'
    elif(len(tmp)>=2):
        status = tmp[2]
    else:
        status = 'ReadComplete'
    
    if status=='ReadNow':   
        travelcard_in=tmp[0]
        area_in=tmp[1]
        #print(travelcard_in)
        #print(area_in)
        
        cur.execute("INSERT INTO travel_data (Travel_card_number)VALUES(999999)")
        cur.execute("UPDATE travel_data SET travel_card_number=?, Swipe_in=? WHERE travel_card_number=999999",(travelcard_in,(area_in),))
        conn.commit()
        
        f.close()

        f = open("htmltraveldata_in.txt", "w")
        f.write('ReadComplete')
    
        cur.execute("SELECT * FROM travel_data")
        rows=cur.fetchall()
        for row in rows:
            print(row)
            print('---------')
        
    f.close()
    
def insert_swipe_out():
    f = open("htmltraveldata_out.txt", "r")
    tmp = f.read().splitlines()
    
    if(len(tmp)==0):
        status = 'DontRead;FileEmpty'
    elif(len(tmp)>=2):
        status = tmp[2]
    else:
        status = 'ReadComplete'
    
    if status=='ReadNow':   
        travelcard_out=tmp[0]
        area_out=tmp[1]
        #print(travelcard_out)
        #print(area_out)
        
        #Update Swipe out area
        cur.execute("UPDATE travel_data SET Swipe_out=? WHERE travel_card_number=?",(area_out,travelcard_out,))
        conn.commit()
        
        #calculate trip amt.
        cur.execute("SELECT Swipe_in FROM travel_data WHERE travel_card_number=?",(travelcard_out,))
        swipe_in=cur.fetchone()
        #for row in swipe_in:
       # if(swipe_in is not None):
           # print(swipe_in[0])
        
        cur.execute("SELECT Swipe_out FROM travel_data WHERE travel_card_number=?",(travelcard_out,))
        swipe_out=cur.fetchone()
        #for row in swipe_out:
        #if(swipe_out is not None):
           # print(swipe_out[0])
        
        if(swipe_in is not None):
            #swipe_in = str(swipe_in[0])+'\n'
            swipe_in=int(swipe_in[0],0)
            #print(swipe_in)
            #cur.execute("SELECT amt FROM routeinfo WHERE area="+swipe_in[0]+"")
            cur.execute("SELECT amt FROM routeinfo WHERE stops=%d" % (swipe_in))
            #cur.execute("SELECT amt FROM routeinfo WHERE area='%(area)s'",{'area':swipe_in[0]})
            
            swipe_in_fare=cur.fetchone()
            print('swipe_in_fare:%d' %swipe_in_fare)
            #if(swipe_in_fare is not None):
             #   print(swipe_in_fare[0]) 
                
         
        if(swipe_out is not None):
            #swipe_in = str(swipe_in[0])+'\n'
            swipe_out=int(swipe_out[0],0)
            #print(swipe_in)
            #cur.execute("SELECT amt FROM routeinfo WHERE area="+swipe_in[0]+"")
            cur.execute("SELECT amt FROM routeinfo WHERE stops=%d" % (swipe_out))
            #cur.execute("SELECT amt FROM routeinfo WHERE area='%(area)s'",{'area':swipe_in[0]})
            
            swipe_out_fare=cur.fetchone()
            print('swipe_out_fare:%d' %swipe_out_fare)
           # if(swipe_out_fare is not None):
               # print(swipe_in_fare[0]) 
         
            tamount = (swipe_out_fare[0])-(swipe_in_fare[0])
            print(tamount)
            cur.execute("UPDATE travel_data SET Trip_amount=? WHERE travel_card_number=?",(tamount,travelcard_out,))
            cur.execute("UPDATE travel_main2 SET Balance_amt=(Balance_amt-?) WHERE travel_card_number=?",(tamount,travelcard_out,))
            
        conn.commit()
            
        
        
        f.close() 

        f = open("htmltraveldata_out.txt", "w")
        f.write('ReadComplete')
    
        cur.execute("SELECT * FROM travel_data")
        rows=cur.fetchall()
        for row in rows:
            print(row)
            print('---------')
        
    f.close()
    
#Reloading amount
    
def re_amount():
    f = open("htmlreloadingAmount.txt", "r")
    tmp = f.read().splitlines()
    
    if(len(tmp)==0):
        status = 'DontRead;FileEmpty'
    elif(len(tmp)>=2):
        status = tmp[2]
    else:
        status = 'ReadComplete'
    
    
    if status=='ReadNow':   
        travelreload_no=tmp[0]
        reload_amt=tmp[1]
        
        cur.execute("INSERT INTO travel_reloadamt(Travel_card_number)VALUES(999999)")
        cur.execute("UPDATE travel_reloadamt SET travel_card_number=?,Reload_Amount=? WHERE travel_card_number=999999",(travelreload_no,reload_amt,))
        cur.execute("UPDATE travel_main2 SET Balance_amt=(Balance_amt+?) WHERE travel_card_number=?",(reload_amt,travelreload_no,))
        conn.commit()
        f.close()

        f = open("htmlreloadingAmount.txt", "w")
        f.write('ReadComplete')
    
        cur.execute("SELECT * FROM travel_reloadamt")
        rows=cur.fetchall()
        for row in rows:
            print(row)
            print('---------')
        
    f.close()
        
        
# In[2]:

# create main database :
conn = sql.connect("smart_travel_card.db")
cur = conn.cursor()
Card_fee_fixed=50

# create table main 
cur.execute('''create table IF NOT EXISTS travel_main2 
           ( [Travel_card_number]integer primary key,[Mobile_number]integer,[Datetime]text,[Card_fee]integer,[Loading_amount]integer,[Balance_amt]integer,[Valid_upto]date)''')
conn.commit()

#create table data
cur.execute('''create table IF NOT EXISTS travel_data
           ( [Travel_card_number]integer primary key,[Swipe_in]varchar,[Swipe_out]varchar,[Trip_amount]integer)''')
conn.commit()
 
cur.execute('''create table IF NOT EXISTS routeinfo
            ( [area]text,[stops]integer primary key,[amt]integer)''')
conn.commit()

cur.execute("SELECT area FROM routeinfo WHERE stops=1")
isRouteNone=cur.fetchone()
print(isRouteNone)
        
if(isRouteNone == None):
    cur.execute("INSERT INTO routeinfo(area,stops,amt)VALUES('RailwayStation',1,0)")
    cur.execute("INSERT INTO routeinfo(area,stops,amt)VALUES('NesavalarColony',2,10)")
    cur.execute("INSERT INTO routeinfo(area,stops,amt)VALUES('NewBusStand',3,20)")
    cur.execute("INSERT INTO routeinfo(area,stops,amt)VALUES('Pichampalayam',4,30)")
    cur.execute("INSERT INTO routeinfo(area,stops,amt)VALUES('PandiyanNagar',5,40)")
conn.commit()

cur.execute("SELECT * FROM routeinfo")
rows=cur.fetchall()
for row in rows:
    print(row)
    print('---------')

#create reloading amount
cur.execute('''create table IF NOT EXISTS travel_reloadamt
            ( [Travel_card_number]integer primary key,[Reload_Amount]integer)''')
conn.commit()    

# In[3]:
#read_travel_main = pd.read_csv(r'D:\02_Project\000_Expertise\Python_Learning\travel_main.csv')
#read_travel_main.to_sql('travel_main2',conn,if_exists='append',index=False)

#to print table
#cur.execute("SELECT * FROM routeinfo")
#rows=cur.fetchall()
#for row in rows:
#   print(row)

# particular row   
#cur.execute("SELECT * FROM travel_main2 WHERE Balance_amt = 200")
#rows=cur.fetchall()
#for row in rows:
#    print(row)
#
##single person amount
#cur.execute("SELECT Balance_amt FROM travel_main2 WHERE Travel_card_number=2")
#rows=cur.fetchone()
#for row in rows:
#    print(row)

#Print csv
#print(read_travel_main)
    
#Add new travel card 
#cur.execute("INSERT INTO travel_main2 (Travel_card_number,Mobile_number,Date,Time,Card_fee,Loading_amount,Balance_amt,Valid_upto)VALUES(7,6754387643,'3/4/2019','14:45',50,300,250,'2/4/2025')")
#rows=cur.fetchall()
#for row in rows:
 #   print(row)
    
#Debit balance after every trip
#trip_amt=50
#cur.execute("UPDATE travel_main2 set Balance_amt=(Balance_amt-?) WHERE travel_card_number=6", (trip_amt,))   
#
##Credit balance after every top up 
#load_amt=100
#cur.execute("UPDATE travel_main2 set Balance_amt=(Balance_amt+?) WHERE travel_card_number=6", (load_amt,)) 
#
##delete travel card
#delete_numb=6
#cur.execute("DELETE FROM travel_main2 WHERE travel_card_number=?",(delete_numb,))
#
##current time and date
#cur.execute("UPDATE travel_main2 set Date=? WHERE travel_card_number=7", (dt.datetime.now(),)) 

#current date
#cur.execute("UPDATE travel_main2 set Date=? WHERE travel_card_number=2",(type(dt.datetime.day),)) 
#cur.execute('''create table travel1([area]varchar,[stops] integer,[amt]integer)''')
#conn.commit()
#cur.execute("INSERT INTO travel1(area,stops,amt)VALUES('GANDHI_NAGAR',0,10)")
#cur.execute("INSERT INTO travel1(area,stops,amt)VALUES('PP_NAGAR',1,15)")
#cur.execute("INSERT INTO travel1(area,stops,amt)VALUES('PSG_NAGAR',2,20)")
#cur.execute("INSERT INTO travel1(area,stops,amt)VALUES('BSS_NAGAR',3,30)")
#cur.execute("INSERT INTO travel1(area,stops,amt)VALUES('PUBG_NAGAR',4,35)")
#cur.execute("SELECT * FROM travel1")
#rows=cur.fetchall()
#for row in rows:
#    print(row)
#stop_amt=10
#cur.execute("UPDATE travel1 set amt=(amt-?) WHERE stops=2", (stop_amt,))      
previous_mobile = 9999999999

#while 1: 
f = open("htmlwrite.txt", "r")
#print(f.read()) 
tmp = f.read().splitlines() #removes \n
#print(len(tmp))
   
if(len(tmp)==0):
    status = 'DontRead;FileEmpty'
elif(len(tmp)>=2):
    status = tmp[2]
else:
    status = 'ReadComplete'

#print(status)
#Add new travel card 
#if((mobile is not None) and (mobile != previous_mobile)):
#print(status == "ReadNow")
if(status == 'ReadNow'):
    mobile = tmp[0]
    amount = int(tmp[1])
#status1 = tmp[2]

    cur.execute("SELECT MAX(Travel_card_number) FROM travel_main2")
    lastTravelCard=cur.fetchone()
    if lastTravelCard[0] is None:
        travelcardNumber = 1
    else:
        travelcardNumber = lastTravelCard[0] + 1

    current_dt = dt.datetime.now()
    Validity_date = current_dt + relativedelta(years=5)        
        
    cur.execute("INSERT INTO travel_main2 (Travel_card_number,Card_fee,Valid_upto)VALUES(999999,50,'2/4/2025')")
    cur.execute("UPDATE travel_main2 SET Mobile_number=?, Loading_amount=?, travel_card_number=?, datetime=?, Balance_amt=?, Valid_upto=? WHERE travel_card_number=999999", (mobile,amount,travelcardNumber,current_dt,(amount-Card_fee_fixed),Validity_date,))


#print(lastTravelCard[0])
#previous_mobile = mobile
    f.close()
    
    f = open("htmlwrite.txt", "w")
    f.write('ReadComplete')
#print(f.read()) 

    cur.execute("SELECT * FROM travel_main2")
    rows=cur.fetchall()
    for row in rows:
        print(row)
    print('next card entry')
    
f.close()
insert_swipe_in()
insert_swipe_out()
re_amount()

cur.execute("SELECT * FROM travel_main2")
rows=cur.fetchall()
for row in rows:
    print(row)


#form
# =============================================================================
# def create(obj):
#     
#     cur.execute("INSERT INTO travel_main2 (Travel_card_number,Mobile_number,Date,Time,Card_fee,Loading_amount,Balance_amt,Valid_upto)VALUES(55,9894353731,'3/4/2019','14:45',50,300,250,'2/4/2025'),(,)")
#     cur.execute("SELECT * FROM travel_main2")
#     rows=cur.fetchall()
#     for row in rows:
#         print(row)
# 
# class Window: 
#     def __init__(self):
#         self.win=tk.Tk()
#         self.button()
#     #def __init__(self):
#         #self.win=tk.Tk()
#         self.entry()
#         
#     def button(self):
#         self.e = tk.Label(self.win,text='Mobile number').grid(row=0) #Self.win was missing
#         e1=tk.Entry(self.win)
#         e1.grid(row=0,column=1)
#         self.b = tk.Button(self.win, text="Register new Travel Card", command= lambda: create(self)).grid(row=0,column=2)
#         #self.b.pack()  
#         self.win.mainloop()
# =============================================================================
    
# =============================================================================
#     def entry(self):
#         self.e = tk.Label(self.win,text='Mobile number').grid(row=0) #Self.win was missing
#         e1=tk.Entry(self.win)
#         e1.grid(row=0,column=1)
#         self.win.mainloop()
# =============================================================================
#win = Window()

#master=tk.Tk()
#w=Entry(master,text='Mobile number').grid(row=0)
#w.pack()
#e1.grid(row=0,column=1)
#master.mainloop()


#read file 


       






