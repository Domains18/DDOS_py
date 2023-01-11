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
