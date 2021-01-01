#!/bin/bash

# script to subset nagios data to just the key lines to get host status information

sed -n '/{\|}\|host_name\|current_state/p' /usr/local/nagios/var/status.dat > /home/pi/nagios_data/status_subset.dat
