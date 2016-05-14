from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

#rsishifts url
login_url='https://www.rsishifts.com'
     
#login form keys
username_key='ctl00$RootContent$txtUsername'
password_key='ctl00$RootContent$txtPassword'
    
def login_handler(browser,employee_info):
    browser.open(login_url)
    login_form=browser.get_form(id='form1')
    login_form[username_key]=employee_info['username']
    login_form[password_key]=employee_info['password']
    browser.submit_form(login_form)
    
##employee schedule maintained in single row in schedule view; employee identified
##by employee's name in upper case
def find_schedule(browser,employee_name):
    schedule_table=browser.find_all('tr')
    employee_name_all_caps=employee_name.upper()
    for i in range(1,len(schedule_table)):
        row_header=schedule_table[i].find(class_='RowHeader').text.strip()
        if (row_header==employee_name_all_caps):
            return schedule_table[i].find_all(class_='Cell')
    return False

def convert_shift_to_int(shift):
    shift=''.join(shift.find(class_='Shift').find_all(text=True,recursive=False)).strip()
    shift=map(int, re.findall(r'\d+',shift))
    return shift
    
def convert_shift_to_datetime(shift_date,shift):
    shift=convert_shift_to_int(shift)
    shift_start_hour=shift[0]
    shift_end_hour=shift[1]
    if (shift_start_hour<shift_end_hour):
        shift_start_hour+=12
    shift_end_hour+=12
    shift_start=shift_date+timedelta(hours=shift_start_hour)
    shift_end=shift_date+timedelta(hours=shift_end_hour)
    formatted_shift={}
    formatted_shift['shift_start']=shift_start
    formatted_shift['shift_end']=shift_end
    return formatted_shift
    
def convert_schedule_to_datetime(start_of_week,schedule):
    month,day,year=map(int,start_of_week.split('/'))
    start_of_week_dt=datetime(year,month,day,0,0,0)
    formatted_schedule=[]
    day_offset=0
    for shift in schedule:
        if (len(shift.contents)==1):
            formatted_schedule.append(None)
        else:
            shift_date=start_of_week_dt+timedelta(days=day_offset)
            formatted_schedule.append(convert_shift_to_datetime(shift_date,shift))
        day_offset+=1
    return formatted_schedule
            
def get_schedule(employee_info,shift_period):
    browser=RoboBrowser(parser='lxml')
    login_handler(browser,employee_info)
    
    start_of_week=shift_period['start_of_week']
    end_of_week=shift_period['end_of_week']
    browser.open('https://www.rsishifts.com/Schedules/SchedulePrintByUser.aspx?'
            'StartDate='+start_of_week+'&EndDate='+end_of_week)
    
    employee_name=employee_info['employee_name']
    schedule=find_schedule(browser,employee_name)
    if (schedule):
        return convert_schedule_to_datetime(start_of_week,schedule)
    else:
        return False
    
    
    
    
    
    
    
    