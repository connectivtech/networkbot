#! /usr/bin/env python

import os
import subprocess

import datetime

import speedtest

import requests


hostname = "google.com" 
numberof_pings = 10
pings = subprocess.Popen(["ping","-c " +  str(numberof_pings), hostname], stdout = subprocess.PIPE)

ping_results = pings.communicate()[0]
cutpoint = ping_results.find("min/avg/max/mdev =")
minPing = ping_results[(cutpoint + 19):(cutpoint + 25)]
averagePing = ping_results[(cutpoint + 26):(cutpoint + 32)]
maxPing = ping_results[(cutpoint + 33):(cutpoint + 39)]

print("----Ping Results------")
print("minPing", minPing)
print("averagePing", averagePing)
print("maxPing", maxPing)
print("----------")


ifconfig = subprocess.Popen("/sbin/ifconfig |grep inet", stdout = subprocess.PIPE, shell=True)
ifconfig_results = ifconfig.communicate()[0]
ifconfig_cutpoint = ifconfig_results.find("inet ", 10)
internal_ip = ifconfig_results[(ifconfig_cutpoint+5):(ifconfig_cutpoint + 17)]

external_ip = subprocess.Popen("dig +short myip.opendns.com @resolver1.opendns.com", stdout = subprocess.PIPE, shell=True)
external_ip = external_ip.communicate()[0][0:-1]


print("----IP Results------")
print("internal_ip", internal_ip)
print("external_ip", external_ip)
print("----------")


time = str(datetime.datetime.now().strftime('%Y-%m-%d')) + "T" + str(datetime.datetime.now().time().strftime('%H:%M:%S'))


servers = []
s = speedtest.Speedtest()
s.get_servers(servers)
s.get_best_server()

downspeed = s.download()
upspeed = s.upload()
print("----Speed Test Results------")
print("downspeend ", downspeed)
print("upload test ", upspeed)

payload = {'node_name': "http://138.197.216.233:8000/networkconnectivity/networkNodes/536e575d-5e4c-4ddd-b61b-187d072c5aa0/",
            'ip_address': internal_ip,
            'external_ip': external_ip,
            'timestamp': time,
            'ping': averagePing,
            'ping_destination':hostname,
            'downspeed': downspeed,
            'upspeed': upspeed
    }
r = requests.post('http://138.197.216.233:8000/networkconnectivity/networkData/', auth=('admin', 'tylertime'), data=payload)
    
print(r.text)