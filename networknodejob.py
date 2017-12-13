#! /usr/bin/env python

import os
import subprocess

import datetime
import speedtest
import requests
import settings

nodeDestination = settings.destinationServer
nodeUsername = settings.username
nodePassword = settings.password


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

# todo - add if wlan or ethernet
# todo - add gateway IP address and ping that too
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

# todo - define what these numbers are - kbps, mbps, mbs, etc
downspeed = s.download()
upspeed = s.upload()
print("----Speed Test Results------")
print("downspeend ", downspeed)
print("upload test ", upspeed)

payload = {'node_name': nodeDestination + "/networkconnectivity/networkNodes/" + nodeUUID +  "/",
            'ip_address': internal_ip,
            'external_ip': external_ip,
            'timestamp': time,
            'ping': averagePing,
            'ping_destination':hostname,
            'downspeed': downspeed,
            'upspeed': upspeed
    }

# todo: if any field is blank it will silently fail, ie, if IP isn't found - need to handle that or log
r = requests.post(nodeDestination + '/networkconnectivity/networkData/', auth=(nodeUsername, nodePassword), data=payload)

print(r.text)