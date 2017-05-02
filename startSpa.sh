#! /bin/sh
cd /home/dad/poolSpa
sudo nohup python poolSpaPage.py &
sudo nohup python mqttSub.py &

