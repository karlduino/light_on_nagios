#!/usr/bin/env python3

from gpiozero import LED
import os
import subprocess
from time import sleep
from math import ceil

# wait time between checks
wait_time = 60     # in sec
startup_wait = 0.2 # in sec
blink_time=0.1     # on/off time for blinking; 0 for no blinking
max_blink=30       # max time blinking (secs)

# server/file info
nagios_server = 'nagiospi.local'
nagios_dir = '/home/pi/nagios_data'
nagios_file = 'status_subset.dat'
local_dir = '/home/pi/nagios_data'

# hosts to monitor
hosts = ['main_router', 'tv_router', 'unfinished_router']

# LED pins
green1 = 25    # (pin 22 on old raspberry pi with 13x2 layout)
red1   = 24    # (pin 18)

green2 = 23    # (pin 16)
red2   = 22    # (pin 15)

green3 = 27    # (pin 13)
red3   =  4    # (pin 7)


local_file = os.path.join(local_dir, nagios_file)


def copy_nagios_file(server, server_dir, file, local_dir):
    local_path = os.path.join(local_dir, file)
    server_path = server + ':' + os.path.join(server_dir, file)

    # check if local directory exists
    if not os.path.isdir(local_dir):
        os.mkdir(local_dir)
    
    # remove file if it exists
    if os.path.isfile(local_path):
        os.remove(local_path)
    	
    command = ['scp', server_path, local_dir]

    # don't print anything
    with open(os.devnull, 'w') as DEVNULL:
        scp_result = subprocess.call(command, stdout=DEVNULL, stderr=DEVNULL)

    # scp worked and file now exists
    return (scp_result==0 and os.path.isfile(local_path))

def get_value(string, sep):
    vec = string.strip().split(sep)
    return vec[1]

def parse_nagios_file(nagios_file, host_names):
    host_up = [False for name in host_names] 
    host_status = {}
    for host in host_names:
        host_status[host] = '-1'
   
    if not os.path.isfile(nagios_file): # if no file, assume they're all down
        return host_up

    with open(nagios_file, 'r') as filep:
        line = filep.readline()
        while line:
            if 'hoststatus' in line:
                line = filep.readline()
                while '}' not in line:
                    if 'host_name=' in line:
                        this_host=get_value(line, '=')
                    if 'current_state=' in line:
                        this_status=get_value(line, '=')

                    line = filep.readline()

                host_status[this_host] = this_status	

            line = filep.readline() 
	
    return [host_status[host]=='0' for host in host_names]


def light_if_up(host_up, green_led, red_led):
    if host_up:
        green_led.on()
        red_led.off()
    else:
        green_led.off()
        red_led.on()

def startup(leds, wait):
    for led in leds:
        led.on()
        sleep(wait)
    sleep(wait)
    for led in leds:
        led.off()
        sleep(wait)


led_green = [LED(green1), LED(green2), LED(green3)]
led_red   = [LED(red1), LED(red2), LED(red3)]

# now run everything

startup(led_green + led_red, startup_wait)

while True:
    if blink_time > 0: 
        led_green[0].blink(blink_time, blink_time, ceil(max_blink/blink_time), True)

    scp_result = copy_nagios_file(nagios_server, nagios_dir, nagios_file, local_dir)
    host_status = parse_nagios_file(local_file, hosts)
    
    for i in range(0,3):
        light_if_up(host_status[i], led_green[i], led_red[i])

    sleep(wait_time)
