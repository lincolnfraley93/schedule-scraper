from icalendar import Calendar, Event
from datetime import datetime, timedelta

def create_ics_file(schedule,base_date):
    cal=Calendar()
    cal.add('version','2.0')
    cal.add('prodid','-//python2.7//EN')
    today=datetime.today()
    for i in range(7):
        if (schedule[i]!=0):
            shift=schedule[i]
            shift_start=shift[0]
            shift_end=shift[1]
            
            shift_event=Event()
            shift_event.add('method','publish')
            uid=str(shift_start)+'-'+str(shift_end)+'@gmail.com'
            shift_event.add('uid',uid)
            shift_event.add('dtstamp',today)
            shift_event.add('dtstart',shift_start)
            shift_event.add('dtend',shift_end)
            shift_event.add('summary','Kickin Chicken')
            cal.add_component(shift_event)
    
    start_of_week=base_date.strftime('%Y%m%d')
    end_of_week=(base_date+timedelta(days=6)).strftime('%Y%m%d')
    file_path='/your/shifts/folder'
    fname=file_path+start_of_week+'_'+end_of_week+'.ics'
    f=open(fname,'w')
    f.write(cal.to_ical())
    f.close()
    
    
    
    
    
    
    
    
    
    
    