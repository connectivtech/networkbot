# Networkbot

This bot runs on rasberry pis, it checks network connectivity and sends information of that connection to the server.

To run move networknodejob.py to your pi, change your destination and admin info to your destination server. Make sure you sett that file editable with `chmod +x networknodejob.py` After that set up a cron job that tests your network at your desired frequency. I had to do `sudo crontab -e` ... probably not best practice, but here we are. My cron job looks like this: 

`*/20 * * * * /usr/bin/python /home/networknodejob.py > /home/cron.log`


