import random as r
import matplotlib.pyplot as plt
from datetime import datetime 
a1=input("Enter the Admin Password of Railway Reservat:  ")
if a1=='123':
    print("Logging in...")
else:
    print("Wrong Admin PAswword")
    exit()

def train_list():
    crs.execute("SELECT * FROM Train_Details")
    data=crs.fetchall()
    for index,i in enumerate(data,start=1):
        print([index,i])

def design1():
    print('''+--------------------------------------------+
|***The List of Trains are given below***    |
+--------------------------------------------+''')

def booking():
    name=input("Enter the passenger Name:  ").upper()
    while True:
        phone=input("Enter the Phone Number:  ")
        if phone.isdigit() and len(phone)==10:
            phone=int(phone)
            break
        else:
            print("Invalid Number")
    

    while True:
        age=int(input("Enter the Age:  "))
        if age<=120 and age >0:
            break
        else:
            print("Age to too large can't insert")

    while True:
        gender=input("Enter the Gender:  ").upper()
        if gender in ['M','F']:
            break
        else:
            print("Invalid Gender")

    train_from=input("Enter the Source Station:  ").upper()
    train_to=input("Enter the Destination:   ").upper()

    qquery = f"SELECT Trn_Number, Trn_Name, Trn_Time, Sleeper, Available FROM train_details WHERE TRIM(Trn_Start_From)=%s AND TRIM(Trn_End_To)=%s"
    crs.execute(qquery, (train_from, train_to))
    trains=crs.fetchall()

    if not trains:
        print("No Train Available in this route")
        return
    else:
        print("Available Trains:  ")
        for t in trains:
            print(f"Train No: {t[0]} | Name: {t[1]} | Time: {t[2]} | Fare: {t[3]} | Seats: {t[4]}")
    train_num=input("Enter the Train Number")
    selected=None
    for i in trains:
        if str(i[0])==train_num:
            selected=i
            break

    if selected is None:
        print("Invalid Train Number")
        return
        
    if selected[4]<=0:
        print("No Seat Available")
        return

    date=input("Enter the Date of Journey  ")
        

    while True:
        email=input("Enter the Email-id:  ").lower()
        if "@" not in email or "." not in email:
            print("Invalid Email")
        else:
            break
            
    pnr=str(r.randint(1000000000,9999999999))
    fare=selected[3]
    
    
    query=f"INSERT INTO Passenger_Details VALUES ({pnr},'{name}',{phone},{age},'{gender}','{train_from}','{train_to}','{date}','{email}',{fare})"
    crs.execute(query)
    mydb.commit()

    update_query=f"UPDATE Train_details set Available = Available-1 where Trn_Number = {train_num}"
    crs.execute(update_query)
    mydb.commit()

    print("!Ticket is booked")
    print()
    print("===== TICKET =====")
    print("PNR:", pnr)
    print("Name:", name)
    print("From:", train_from)
    print("To:", train_to)
    print("Train:", selected[1]) 
    print("Fare:", fare)
    print("==================")

def cancellation():
    pnr=int(input("Enter the pnr:  "))
    quer=f"DELETE FROM Passenger_Details where Pnr_Number={pnr}"
    crs.execute(quer)
    mydb.commit()

    print("Ticket Cancelled Successfully")

def train_station():
    source=input("Enter the Source:  ")
    destination=input("Enter the destination:  ")

    queryy=f"SELECT Trn_Name, Trn_Number, Trn_Start_From, Trn_End_To, Trn_Time FROM Train_Details WHERE Trn_Start_From = '{source}' AND Trn_End_To = '{destination}'"
    crs.execute(queryy)
    results = crs.fetchall()
    for index,i in enumerate(results,start=1):
        print([index,results])

def ticket():
    pnr1 = input("Enter the PNR of train: ")
    query = "SELECT * FROM passenger_Details WHERE Pnr_Number = %s"
    values = (pnr1,)   

    crs.execute(query, values)

    result = crs.fetchall()  

    print("---------Your Ticket---------")
    print()
    for row in result:
        print("PNR:", row[0])
        print("Name:", row[1])
        print("Phone:", row[2])
        print("Age:", row[3])
        print("Gender:", row[4])
        print("Train From:", row[5])
        print("Train To:", row[6])
        print("Date:", row[7])
        print("Email:", row[8])
        print("Fare:", row[9])
        
    
        print("----------------------")
        
def fare():
    source = input("Enter Source Station: ").upper()
    destination = input("Enter Destination Station: ").upper()

    query = f"SELECT Trn_Number, Trn_Name, Sleeper FROM Train_Details WHERE Trn_Start_From='{source}' AND Trn_End_To='{destination}'"

    crs.execute(query)
    data=crs.fetchall()

    if not data:
        print("No trains available on this route")
        return

    print("\n===== Sleeper Fare Details =====\n")
    for i in data:
        print(f"Train No: {i[0]} | Train Name: {i[1]} | Sleeper Fare: ₹{i[2]}")


#analytics all function from here
def popular_routes():
        query=f"Select Train_From, Train_to, COUNT(*) from passenger_details group by Train_From, Train_to"
        crs.execute(query)
        data=crs.fetchall()

        routes = []
        for i in data:
            route = str(i[0]) + "-" + str(i[1])
            routes.append(route)

        count = []
        for i in data:
            count.append(i[2])
            
        plt.bar(routes,count,color='green')
        plt.title("Most Popular Routes")
        plt.xlabel("Routes")
        plt.ylabel("Number of Bookings")
        plt.show()

def age_distribution():
    query = "SELECT Psn_age FROM Passenger_Details"
    crs.execute(query)
    data = crs.fetchall()

    ages = []
    for i in data:
        ages.append(i[0])
        
    plt.hist(ages, bins=10, color='orange', edgecolor='black')
    plt.title("Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    plt.show()
        
def gender_ratio():
    query = "SELECT Psn_gender, COUNT(*) FROM Passenger_Details GROUP BY Psn_gender"
    crs.execute(query)
    data = crs.fetchall()

    labels = []
    sizes = []

    for i in data:
        labels.append(i[0])
        sizes.append(i[1])


    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title("Gender Ratio")
    plt.show()

def revenue_by_route():
    query = f"SELECT Train_From, Train_to, SUM(Fare) FROM Passenger_Details GROUP BY Train_From, Train_to"
    crs.execute(query)
    data=crs.fetchall()

    routes=[]
    revenue=[]

    for i in data:
        routes.append(i[0] + " → " + i[1])
        revenue.append(i[2])

    plt.bar(routes, revenue, color='skyblue')
    plt.xticks(rotation=45)
    plt.title("Revenue by Route")
    plt.xlabel("Route")
    plt.ylabel("Total Revenue")
    plt.tight_layout()
    plt.show()

def seat_availability():
    query = "SELECT Trn_Name, Available FROM Train_Details"
    crs.execute(query)
    data=crs.fetchall()

    trains=[]
    seats=[]

    for i in data:
        trains.append(i[0])
        seats.append(i[1])

    plt.bar(trains, seats, color='green')
    plt.xticks(rotation=60)
    plt.title("Seat Availability per Train")
    plt.xlabel("Train Name")
    plt.ylabel("Available Seats")
    plt.tight_layout()
    plt.show()

def fare_comparison():
    query = f"SELECT Train_From, Train_to, AVG(Fare) FROM Passenger_Details GROUP BY Train_From, Train_to"
    crs.execute(query)
    data=crs.fetchall()

    routes=[]
    fares=[]

    for i in data:
        routes.append(i[0] + " → " + i[1])
        fares.append(i[2])

    plt.plot(routes, fares, marker='o', color='blue')
    plt.xticks(rotation=90)
    plt.title("Average Fare Comparison")
    plt.xlabel("Route")
    plt.ylabel("Average Fare")
    plt.grid()
    plt.tight_layout()
    plt.show()

def bookings_by_date():
    query = f"SELECT Scheduled_Date, COUNT(*) FROM Passenger_Details GROUP BY Scheduled_Date ORDER BY Scheduled_Date"
    crs.execute(query)
    data=crs.fetchall()

    dates=[]
    bookings=[]

    for i in data:
        dates.append(str(i[0]))
        bookings.append(i[1])

    plt.plot(dates, bookings, marker='o', color='purple')
    plt.xticks(rotation=45)
    plt.title("Bookings by Date")
    plt.xlabel("Date")
    plt.ylabel("Number of Bookings")
    plt.grid()
    plt.tight_layout()
    plt.show()

def top_destinations():
    query = f"SELECT Train_to, COUNT(*) FROM Passenger_Details GROUP BY Train_to ORDER BY COUNT(*) DESC"
    crs.execute(query)
    data=crs.fetchall()

    destinations=[]
    count=[]

    for i in data:
        destinations.append(i[0])
        count.append(i[1])

    plt.bar(destinations, count, color='orange')
    plt.xticks(rotation=45)
    plt.title("Top Destinations")
    plt.xlabel("Destination")
    plt.ylabel("Number of Passengers")
    plt.tight_layout()
    plt.show()
    
while True: 
    try:
        import mysql.connector as msc
        import datetime
        import random as rd
        import pandas as pd
        import sys
        import matplotlib.pyplot as plt
  
        mydb=msc.connect(host='localhost',user='root',password='YOUR_PASSWORD')
        crs=mydb.cursor()
        #qry1='CREATE DATABASE railway'
        #crs.execute(qry1)
        qry2='USE railway'
        crs.execute(qry2)
        #qry3="CREATE TABLE Passenger_Details (Pnr_Number int(10) primary key, Psn_Name varchar(25), Psn_Ph_no varchar(10),Psn_age int(10),Psn_gender char(1),Train_From varchar(25),Train_to varchar(20),Scheduled_Date DATE ,Email_ID varchar(30), Fare int(12))"
        #crs.execute(qry3)
            
        #qry4="INSERT INTO Passenger_Details VALUES (1021959091,'MOHAN','9658256315',25,'M','AJMER','DELHI','2021-03-09','Mohan@gmail.com',720)"
        #crs.execute(qry4)
            
        #qry5="INSERT INTO Passenger_Details VALUES(1021959092,'RAHUL','9876543210',30,'M','MUMBAI','DELHI','2021-03-10','rahul@gmail.com',650)"
        #crs.execute(qry5)
            
        #qry6="INSERT INTO Passenger_Details VALUES (1021959093,'SNEHA','9123456780',22,'F','MUMBAI','JAIPUR','2021-03-10','sneha@gmail.com',600)"
        #crs.execute(qry6)
            
        #qry7="INSERT INTO Passenger_Details VALUES (1021959094,'AMIT','9988776655',35,'M','DELHI','JAIPUR','2021-03-11','amit@gmail.com',500)"
        #crs.execute(qry7)
            
        #qry8="INSERT INTO Passenger_Details VALUES (1021959095,'PRIYA','9012345678',28,'F','KOLKATA','JAIPUR','2021-03-10','priya@gmail.com',700)"
        #crs.execute(qry8)

        #qry9="INSERT INTO Passenger_Details VALUES (1021959096,'ARJUN','9090909090',40,'M','CHENNAI','BANGLORE','2021-03-12','arjun@gmail.com',450)"
        #crs.execute(qry9)

        #qry10="INSERT INTO Passenger_Details VALUES (1021959097,'KAVYA','9345678123',24,'F','CHENNAI','BANGLORE','2021-03-12','kavya@gmail.com',450)"
        #crs.execute(qry10)

        #qry11="INSERT INTO Passenger_Details VALUES (1021959098,'ROHIT','9765432180',32,'M','HYDERABAD','DELHI','2021-03-13','rohit@gmail.com',650)"
        #crs.execute(qry11)

        #qry12="CREATE TABLE Train_Details (Trn_Name varchar(25), Trn_Number int(10) primary key, Trn_Start_From varchar(25), Trn_End_To varchar(25), Trn_Time varchar(25))"
        #crs.execute(qry12)

        #qry13="INSERT INTO Train_Details VALUES('Rajdhani',10101,'DELHI','MUMBAI','05:30 AM')"
        #crs.execute(qry13)

        #qry14="INSERT INTO Train_Details VALUES('Shatabdi',10102,'DELHI','JAIPUR','03:00 PM')"
        #crs.execute(qry14)

        #qry15="INSERT INTO Train_Details VALUES('Duronto',10103,'MUMBAI','DELHI','09:00 PM')"
        #crs.execute(qry15)

        #qry16="INSERT INTO Train_Details VALUES('GaribRath',10104,'MUMBAI','DELHI','09:00 PM')"
        #crs.execute(qry16)

        #qry17="INSERT INTO Train_Details VALUES('Intercity',10105,'CHENNAI','BANGLORE','05:30 AM')"
        #crs.execute(qry17)

        #qry18="INSERT INTO Train_Details VALUES('Express1',10106,'CHENNAI','BANGLORE','03:00 PM')"
        #crs.execute(qry18)

        #qry19="INSERT INTO Train_Details VALUES('Express2',10107,'HYDERABAD','CHENNAI','09:00 PM')"
        #crs.execute(qry19)

        #qry20="INSERT INTO Train_Details VALUES('SuperFast1',10108,'KOLKATA','DELHI','09:00 PM')"
        #crs.execute(qry20)

        #qry21="INSERT INTO Train_Details VALUES('SuperFast2',10109,'KOLKATA','MUMBAI','05:30 AM')"
        #crs.execute(qry21)

        #qry22="INSERT INTO Train_Details VALUES('Passenger1',10110,'JAIPUR','DELHI','03:00 PM')"
        #crs.execute(qry22)

        #qry23="INSERT INTO Train_Details VALUES('Passenger2',10111,'JAIPUR','MUMBAI','09:00 PM')"
        #crs.execute(qry23)

        #qry24="INSERT INTO Train_Details VALUES('Mail1',10112,'DELHI','MUMBAI','05:30 AM')"
        #crs.execute(qry24)

        #qry25="INSERT INTO Train_Details VALUES('Mail2',10113,'HYDERABAD','BANGLORE','03:00 PM')"
        #crs.execute(qry25)

        #qry26="INSERT INTO Train_Details VALUES('NightExpress',10114,'DELHI','KOLKATA','09:00 PM')"
        #crs.execute(qry26)

        #qry27="INSERT INTO Train_Details VALUES('MorningStar',10115,'MUMBAI','CHENNAI','05:30 AM')"
        #crs.execute(qry27)

        #qry28="INSERT INTO Train_Details VALUES('CityLink',10116,'BANGLORE','HYDERABAD','03:00 PM')"
        #crs.execute(qry28)

        #qry29="INSERT INTO Train_Details VALUES('FastLine',10117,'DELHI','MUMBAI','03:00 PM')"
        #crs.execute(qry29)

        #qry30="INSERT INTO Train_Details VALUES('SouthExpress',10118,'CHENNAI','HYDERABAD','05:30 AM')"
        #crs.execute(qry30)

        #qry31="INSERT INTO Train_Details VALUES('EastMail',10119,'KOLKATA','DELHI','09:00 PM')"
        #crs.execute(qry31)

        mydb.commit()
            
    except Exception as e:
        print(e)



    print('''
            +=========================================+
            |           **** MAIN MENU ****           |
            +=========================================+
            |                                         |
            | 1.Ticket Booking                        |
            | 2.Train Between Station                 |
            | 3.Train List                            |
            | 4.Your Ticket                           |
            | 5.Ticket Cancellation                   |
            | 6.Fare                                  |
            | 7.Analytics                             |
            | 8.Exit                                  |
            |                                         |
            +=========================================+
        ''')

    user_input=int(input("What you want to do! "))
    if user_input==8:
        exit()
    elif user_input==3:
        design1()
        print()
        train_list()
    elif user_input==1:
        booking()
    elif user_input==5:
        cancellation()
    elif user_input==2:
        train_station()
    elif user_input==4:
        ticket()
    elif user_input==7:
        print("1. Most Popular Routes")
        print("2. Age Distribution of Passengers")
        print("3. Gender Ratio")
        print("4. Revenue by Route")
        print("5. Seat Availability per Train")
        print("6. Fare Comparison")
        print("7. Bookings by Date")
        print("8. Top Destinations")
        ask=int(input("Enter what to do"))
        if ask==1:
            popular_routes()
        elif ask==2:
            age_distribution()
        elif ask==3:
            gender_ratio()
        elif ask==4:
            revenue_by_route()
        elif ask==5:
            seat_availability()

        elif ask==6:
            fare_comparison()
        elif ask==7:
            bookings_by_date()
        elif ask==8:
            top_destinations()
        else:
            print("Sorry Invalid Input")
            
    elif user_input==6:
        fare()

    else:
        print("Invalid Input")
            
