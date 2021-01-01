#!/usr/bin/env python3

import os
import subprocess

nagios_server = 'nagiospi.local'
nagios_dir = '/usr/local/nagios/var'
nagios_file = 'status.dat'
local_dir = '/home/pi/nagios_data'

hosts = ['main_router', 'tv_router', 'unfinished_router']

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

def parse_nagios_file(nagios_file, host_names):
    host_up = [False for name in host_names] 

    if not os.path.isfile(nagios_file): # if no file, assume they're all down
        return host_up

    with open(nagios_file, 'r') as filep:
        line = filep.readline()
        while line:
            if 'hoststatus' in line:
                line = filep.readline()
                while '}' not in line:
                    if 'host_name=' in line or 'current_state=' in line:
                        print(line)
                    line = filep.readline()

            line = filep.readline() 
	
    return host_up



# run the stuff
scp_result = copy_nagios_file(nagios_server, nagios_dir, nagios_file, local_dir)
host_status = parse_nagios_file(local_file, hosts)
print(scp_result)
print(host_status)
