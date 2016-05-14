from get_schedule import get_schedule
from export_to_ics import export_to_ics

#login stuff
username='username'
password='password'

#used to find row in schedule
employee_name='employee name'

#shift period (week), in 'd/m/yyyy'
start_of_week='5/9/2016'
end_of_week='5/15/2016'

def main():
    employee_info={'username':username,'password':password,'employee_name':employee_name}
    shift_period={'start_of_week':start_of_week,'end_of_week':end_of_week}
    schedule=get_schedule(employee_info,shift_period)
    if (schedule):
        export_to_ics(schedule,start_of_week,end_of_week)
    else:
        print employee_name+' not found'
        
main()