# IN this programme we are going to create the alarmclock
from datetime import datetime
from playsound import playsound

alarm_time = input("Enter the alarm time in the format of HH:MM : ")
alarm_hour = alarm_time[0:1]
alarm_minute = alarm_time[3:]
print("Setting alarm....")

while (True):
    now = datetime.now()
    current_hour = now.strftime("%I")
    current_Minute = now.strftime("%M")

    if(alarm_hour==current_hour):
        if(alarm_minute==current_Minute):
            print("Wake up!")
            playsound('./assets/Tone.mp3')
            break

# alarm_tone = open('C:\Users\shivk\Music\Video Projects\Tone.mp3' + 'Tone.mp3')
# playsound('Tone.mp3')
