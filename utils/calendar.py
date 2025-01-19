from ics import Calendar, Event
from datetime import datetime



def generate_calendar(data):
    calendar = Calendar()


    for item in data:
        if not item:
            continue  

        date, time, title = item['date'], item['time'], item['title']


        event = Event()
        event.name = title        # Parse the date
        date_object = datetime.strptime(date, "%Y-%m-%d")

        start_time, end_time = time.split(" - ")


        date_string = date_object.strftime("%Y-%m-%d")  # Convert date_object to string
        start_datetime = datetime.strptime(f"{date_string} {start_time}", "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(f"{date_string} {end_time}", "%Y-%m-%d %H:%M")


        event.begin = start_datetime
        event.end = end_datetime

        calendar.events.add(event)

    with open("schedule.ics", "w") as file:
        file.writelines(calendar)

    print("ICS file created: schedule.ics")