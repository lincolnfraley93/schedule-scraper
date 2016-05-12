from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from create_ics_file import create_ics_file
#urls
login_url='https://www.rsishifts.com'

#login stuff
username='username'
password='password'

#used to find row in schedule
employee_name_all_caps='EMPLOYEE NAME'

#date info
start_of_week='5/9/2016'
end_of_week='5/15/2016'
base_date=datetime(2016,5,9,0,0,0)

            
            
#Set username&password dict
def set_login_info():
    username_key='ctl00$RootContent$txtUsername'
    password_key='ctl00$RootContent$txtPassword'
    
    login_info={}
    login_info[username_key]=username
    login_info[password_key]=password
    
    return login_info            
            
def login_handler(browser):
    login_info=set_login_info()
    browser.open(login_url)
    signup_form=browser.get_form(id='form1')
    for key, value in login_info.iteritems():
        signup_form[key]=value
    browser.submit_form(signup_form)            

def get_schedule_url():     
    return ('https://www.rsishifts.com/Schedules/SchedulePrintByUser.aspx?'
            'StartDate='+start_of_week+'&EndDate='+end_of_week)

def format_shift(offset,shift):
    shift=map(int, re.findall(r'\d+',shift))
    start_hour=shift[0]
    end_hour=shift[1]
    if (start_hour<end_hour):
        start_hour+=12
    end_hour+=12
    shift_start=base_date+timedelta(days=offset)+timedelta(hours=start_hour)
    shift_end=base_date+timedelta(days=offset)+timedelta(hours=end_hour)
    return [shift_start,shift_end]
    
#return shift start+end times as datetime object
def format_schedule(schedule):
    formatted_schedule=[]
    week=schedule.find_all(class_='Cell')
    offset=0
    for day in week:
        if (len(day.contents)==1):
            formatted_schedule.append(0)
        else:
            shift=''.join(day.find(class_='Shift').find_all(text=True,recursive=False)).strip()
            formatted_schedule.append(format_shift(offset,shift))
        offset+=1
    return formatted_schedule
 
#returns false if not found
def get_schedule(browser):
    table_rows=browser.find_all('tr')
    for i in range(1,len(table_rows)):
        row_header=table_rows[i].find(class_='RowHeader').text.strip()
        if (row_header==employee_name_all_caps):
            schedule=table_rows[i]
            return format_schedule(schedule)
    return False
                
def open_schedule_page(browser):
    login_handler(browser) 
    schedule_url=get_schedule_url()
    browser.open(schedule_url)
    
def main():
    browser=RoboBrowser(parser='lxml')
    open_schedule_page(browser)
    schedule=get_schedule(browser)
    
    if (schedule):
        print schedule
        create_ics_file(schedule,base_date)
    else:
        print employee_name_all_caps+' not found'
    
main()













