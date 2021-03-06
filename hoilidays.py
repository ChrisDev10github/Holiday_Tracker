from ctypes.wintypes import DWORD
import datetime
import json
from threading import local
from attr import attributes
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from datetime import timedelta
from datetime import datetime as dt



# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------

#task in demo
@dataclass
class Holiday:
    name:str
    date: datetime
#    DTFormat = '%Y-%m-%d'

      
#    def __init__(self,name, date):
#        #Your Code Here  
#        self.name = name
#        self.date = dt.strptime(date,'%Y-%m-%d')

       
    
    def __str__ (self):
        # String output
        # Holiday output when printed.
        return f'{self.name}, {self.date}'


    #need accept onmly date time
    
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------

#calender in demo
#return with keys being holiday
#know how to access Holiday List 

class HolidayList:

    #DTFormat = '%Y-%m-%d'
    
    def __init__(self):
       self.innerHolidays = []
   
    def addHoliday(self,holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
        #dateadd = holidayObj.date
        #dateaddfinal = dateadd.DTFormat
        addition = Holiday(holidayObj.name,dt.strptime(holidayObj.date,'%Y-%m-%d'))
        self.innerHolidays.append(addition)
        print("Successfully added the holiday")
        #print(self.innerHolidays)           #testing


    def findHoliday(self,HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday                #maybe lambda
        
        for holiday in self.innerHolidays:
            if(holiday.date == Date and HolidayName == holiday.name):
                print("The Holiday is in the calender")
                return holiday
        if(holiday.date != Date and HolidayName != holiday.name):
            return None

        #local_holiday = Holiday(HolidayName,Date)
        #if local_holiday in self.innerHolidays:
        #    for i in range(0,len(self.innerHolidays)):
        #        if self.innerHolidays[i] == local_holiday:
        #            return local_holiday
        #else:
        #    print("The Holiday is not in the calender")

    def removeHoliday(self,HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
        
        #if self.findHoliday(HolidayName, Date) == None:
        remove_local_holiday = self.findHoliday(HolidayName,dt.strptime(Date,'%Y-%m-%d'))
        if remove_local_holiday == None:
            print("That holiday is not in our record, try again :)")
        else:
            self.innerHolidays.remove(remove_local_holiday)
            print("Successfully removed the holiday")

            
    def read_json(self,filelocation):
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.
        print("This must be a Json File")
        f=open(filelocation)
        h_Dict = json.load(f)               #might be loads
        dictList = h_Dict["holidays"]
        for hol in dictList:
            addH = Holiday(hol["name"],hol["date"])
            #print(addH.date)
            #print(type(addH.date.year))
            self.addHoliday(addH)
        f.close()
        print("Successfully Added Holidays")
        


    def save_to_json(self,filelocation):
        # Write out json file to selected file.

        #Formatting style to the holidays json
        f = open(filelocation,"w")
        h_list=[]
        for i in range(0,len(self.innerHolidays)):
            holiday_dict = {}
            #getting names and dates => putting into holiday_dict
            h_name = self.innerHolidays[i].name
            h_date = self.innerHolidays[i].date
            holiday_dict["name"] = h_name
            holiday_dict["date"] = h_date
            h_list.append(holiday_dict)


        #adding into a json dictionary and dump
        json_dict={}
        json_dict["holidays"] = h_list
        json.dump(json_dict,f,default=str)
        f.close()
        print("Successfully Saved Changes")
        

    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     

        #the holidays are in td tags except the date which is in th tags with class nw
        #urls for each year differ by /year at the end
        #url2020 = https://www.timeanddate.com/holidays/us/2020
        #url2021 = https://www.timeanddate.com/holidays/us/2021
        #url2022 = https://www.timeanddate.com/holidays/us/
        #url2023 = https://www.timeanddate.com/holidays/us/2023
        #url2024 = https://www.timeanddate.com/holidays/us/2024

        years={'2020','2021','2022','2023','2024'}
        DTFormat = '%Y-%m-%d'

        for year in years:
            try:
                html = f'https://www.timeanddate.com/holidays/us/{year}'
                url = requests.get(html)
                html_soup = BeautifulSoup(url, 'html.parser')
                #table = html_soup.find('table',attrs = {'id':'holidays-table'})    #one layer too high in html?
                table = html_soup.find('tbody', attrs={'id':'holidays-table'})
                #print(table)       weird id attribute
                tablerow = table.find_all('tr')
                attributes = tablerow.find_all('td')        #everything but date
                for row in tablerow:
                    #date
                    tabledate = year + ', ' + row.find('th',attrs={'class':'nw'}).string            #date is in th tags

                    datetimedata = datetime.strptime(tabledate, '%Y, %m %d').date()
            
            except:
                print("Error accesing information")


                #if tabledate != None:
                #    tabledatestr = tabledate.text        #?
                #name of holiday
                #tablenameholiday = row.find('a')
                #if tablenameholiday != None:
                #    tablenameholidaystr = tablenameholiday.text


                #html_formal='%b %d %Y'
                #date_datetime=datetime(f"{tabledatestr} {year}",html_formal)
                #checking if holiday is already in list and if not add it 

                #if self.findHoliday(tablenameholidaystr,date_datetime) == None:
                #    insert_holiday = Holiday(tablenameholidaystr,date_datetime)
                #    self.addHoliday(insert_holiday)



    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        totalholiday = len(self.innerHolidays)     
        return totalholiday
    
    def filter_holidays_by_week(self,year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list       
        # return your holidays

        #filter_year = list(filter(lambda x: x.date.isocalendar().year == year, self.innerHolidays))           #originally had list(filter)
        #filter_week=list(filter(lambda x:int(x.date.strftime('%U'))==week_number,filter_year))           #originally had list(filter)
        filter_week = list(filter(lambda x: x.date.isocalendar()[1] == week_number and x.date.year == int(year), self.innerHolidays))
        #print(filter_week)
        return filter_week

    def displayHolidaysInWeek(self,holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week.             #lambda maybe
        # * Remember to use the holiday __str__ method.   
        #print(holidayList)
        for day in holidayList:
            print(str(day))      

    def getWeather(self):
        # Convert weekNum to range between two days (2 digits 1-52)
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.


        #date = datetime.date(2022, 1,1) + timedelta(weeks=weekNum)          #sunday of the weeknumber (the last day of the week)

        try:

            url = "https://community-open-weather-map.p.rapidapi.com/forecast"          #Given

            querystring = {"q":"san francisco,us"}                                      #Given

            headers = {                                                                 #Given
	        "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
	        "X-RapidAPI-Key": "032495499cmsh87a7f851860036ap143e00jsn16c55b0cdc5f"
            }

            #requests
            response = requests.request("GET", url, headers=headers, params=querystring)        #Given
            info = response.json()

            #add to weather list
            weather_List = {}
            for i in range(5):  #5 day forecast (using 5 day 3 hr incrament forecast)
                #weather_List.append(info['list'][8*i]['weather'][0]['description'])    
                weather_List[dt.strptime(info['list'][8*i]['dt_txt'],'%Y, %m %d')] = info['list'][8*i]['weather'][0]['description']

            #print(weather_List)
        
            return weather_List

        except:
            print('There was an error accessing weather api')

        
    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        
        currentyr = datetime.datetime.today().isocalendar().year        
        currentweek = datetime.datetime.today().isocalendar().week

        dates = []
        currentday = datetime.datetime.today()      #todays date
        dates.append(currentday)
        for i in range(1,5):                            #the previous 4 days
            previousday = currentday+timedelta(days=i)
            dates.append(previousday)

        currentweeknum = currentday.isocalendar()[1]
        fhlist = self.filter_holidays_by_week(currentyr,currentweeknum)
        #holidays_in_week = self.displayHolidaysInWeek(fhlist)

        if len(fhlist) == 0:
            print("No current holidays")
        else:

            question = str(input('Would you like to see this weeks weather [y/n]: '))
            if question == 'y':
                weather_List = self.getWeather()

                print(weather_List)
                print(fhlist)
                for i in range(0,len(fhlist)):
                    
                    print(f'{fhlist[i].name} {fhlist[i].date} {weather_List[fhlist[i].date]}')
            else:
                for i in range(0,len(dates)):
                    print(f'{fhlist}  {dates[i]}')




def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 

    
    ListofHolidays = HolidayList()      #1
    ListofHolidays.read_json('holidays.json') #2
    #ListofHolidays.scrapeHolidays()     #3

    UserChoosing = True

    while UserChoosing == True:
        print('''
                Holiday Menu
                ================
                1. Add a Holiday
                2. Remove a Holiday
                3. Save Holiday List
                4. View Holidays
                5. Exit''')
        choice = int(input('What do you want to do. [1-5]: '))

        if choice == 1:
            name = str(input("What is the holiday name: "))
            date = input("What is the holiday date year-month-day?: ")
            add = Holiday(name,date)
            ListofHolidays.addHoliday(add)

        if choice == 2:
            name = str(input("What is the holiday name: "))
            date = input("What is the holiday date year-month-day?: ")
            ListofHolidays.removeHoliday(name,date)

        if choice == 3:
            ListofHolidays.save_to_json('Updated_HolidayList.json')
        
        if choice == 4:
            year = str(input("What year do you want: "))
            week = str(input("What week number [1-52] or [type 0 for current week]: "))
            if week == '0' or week=='':
                ListofHolidays.viewCurrentWeek()
            else:
                f_list = ListofHolidays.filter_holidays_by_week(year,int(week))
                #print(f_list)
                ListofHolidays.displayHolidaysInWeek(f_list)

        if choice == 5:
            print("You are exiting goodbye")
            UserChoosing = False



if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





