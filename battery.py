# Python program that displays a toast message when battery reaches a certain level

from win10toast import ToastNotifier
toaster = ToastNotifier()

import psutil

def getpercent():
	battery = psutil.sensors_battery()
	plugged = battery.power_plugged
	percent = str(battery.percent)
	return percent

x=getpercent()
while(int(x)>30):
	pass 

toaster.show_toast("Notification","Battery below 30% !", duration=60)