#!/usr/bin/env python

import subprocess

command = ['scp', 'nagiospi.local:/usr/local/nagios/var/status.dat', '/home/pi/nagios_data']
process = subprocess.Popen(command)

file = '/home/pi/nagios_data/status.dat'
