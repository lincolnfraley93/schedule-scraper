from icalendar import Calendar, Event
from datetime import datetime, timedelta

def export_to_ics(schedule,start_of_week,end_of_week):
    cal=Calendar()
    cal.add('version','2.0')
    cal.add('prodid','-//python2.7//EN')
    today=datetime.today()
    for shift in schedule:
        if (shift!=None):
            shift_start=shift['shift_start']
            shift_end=shift['shift_end']
            shift_event=Event()
            uid=str(shift_start)+'-'+str(shift_end)+'@gmail.com'
            shift_event.add('uid',uid)
            shift_event.add('dtstamp',today)
            shift_event.add('dtstart',shift_start)
            shift_event.add('dtend',shift_end)
            shift_event.add('summary','Kickin Chicken')
            cal.add_component(shift_event)
    
    start_of_week=start_of_week.replace('/','')
    end_of_week=end_of_week.replace('/','')
    file_path='/file_path/'
    fname=file_path+start_of_week+'_'+end_of_week+'.ics'
    f=open(fname,'w')
    f.write(cal.to_ical())
    f.close()