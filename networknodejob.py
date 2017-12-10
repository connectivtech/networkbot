#! /usr/bin/env python
import os
import subprocess
import requests

import httplib, urllib
import datetime

hostname = "google.com" 
numberof_pings = 1
pings = subprocess.Popen(["ping","-c " +  str(numberof_pings), hostname], stdout = subprocess.PIPE)

ping_results = pings.communicate()[0]
cutpoint = ping_results.find("min/avg/max/stddev =")
minPing = ping_results[(cutpoint + 21):(cutpoint + 27)]
averagePing = ping_results[(cutpoint + 28):(cutpoint + 34)]
maxPing = ping_results[(cutpoint + 35):(cutpoint + 41)]

print("----Ping Results------")
print("minPing", minPing)
print("averagePing", averagePing)
print("maxPing", maxPing)
print("----------")


ifconfig = subprocess.Popen("ifconfig |grep inet", stdout = subprocess.PIPE, shell=True)
ifconfig_results = ifconfig.communicate()[0]
ifconfig_cutpoint = ifconfig_results.find("inet ", 10)
internal_ip = ifconfig_results[(ifconfig_cutpoint+5):(ifconfig_cutpoint + 17)]

external_ip = subprocess.Popen("dig +short myip.opendns.com @resolver1.opendns.com", stdout = subprocess.PIPE, shell=True)
external_ip = external_ip.communicate()[0][0:-1]


print("----Ping Results------")
print("internal_ip", internal_ip)
print("external_ip", external_ip)
print("----------")


time = str(datetime.datetime.now().strftime('%Y-%m-%d')) + "T" + str(datetime.datetime.now().time().strftime('%H:%M:%S'))



payload = {'node_name': "http://127.0.0.1:8000/networkconnectivity/networkNodes/8528b423-430a-4f5b-8822-0faec53b592d/",
            'ip_address': internal_ip,
            'external_ip': external_ip,
            'timestamp': time,
            'ping': averagePing,
            'ping_destination':hostname
    }
r = requests.post('http://127.0.0.1:8000/networkconnectivity/networkData/', auth=('admin', 'tylertime'), data=payload)
    
print(r.text)