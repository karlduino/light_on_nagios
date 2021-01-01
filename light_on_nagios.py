#!/usr/bin/env python3

import os
import subprocess

nagios_server = 'nagiospi.local'
nagios_dir = '/usr/local/nagios/var'
nagios_file = 'status.dat'
local_dir = '/home/pi/nagios_data'


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

# run the stuff
scp_result = copy_nagios_file(nagios_server, nagios_dir, nagios_file, local_dir)
print(scp_result)
