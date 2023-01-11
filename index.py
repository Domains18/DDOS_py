import subprocess
import re
import csv 
import os
import time
import shutil
from datetime import datetime

#create empty list
active_wireless_networks = []

def check_for_essid(essid, lst):
    check_status = True
    if(len(lst) == 0):
        return check_status
    for item in lst:
        if essid in item["ESSID"]:
            check_status = False
    return check_status


# Basic user interface
print(" To Whom Much is Given, Much is Expected")

if not 'SUDO_UID' in os.environ.keys():
    print("Please run this script with sudo")
    exit()
    
for file_name in os.listdir():
    if ".csv" in file_name:
        directory = os.getcwd()
        try:
            os.mkdir(directory + "/old_csv")
        except:
            print("Directory already exists")
        timestamp = datetime.now()
        shutil.move(file_name, directory + "/old_csv" + str(timestamp) + "-" + file_name)
        
wlan_pattern = re.compile("wlan[0-9] +")
check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode("utf-8"))

# wifi adapter == false
if len(check_wifi_result) == 0:
    print("No wifi adapter found")
    exit()

print("Available wifi adapters: ")
for index, item in enumerate(check_wifi_result):
    print(f"{index + 1}. {item.strip()}")
    