## Display router status

I'm using a raspberry pi to monitor 3 routers. Initially, I'd used ping, but I 
had already set up a separate nagios server on a separate raspberry pi, and it
seems more reliable, so here I will

- grab the status data from the other pi 

- parse it to determine the up/down status of my three routers

- light up green or red LEDs according to whether they are up or down

- I'm using an old Raspberry Pi Model B revision 2011.12. 
  The GPIO is 13x2

  - pins numbered (1,2),(3,4), ... going down
  - 3.3 power at pins 1 and 17
  - ground at pins 6, 9, 14, 20, 25
  - pin 7 = GPIO4
  - pin 13 = GPIO27
  - pin 15 = GPIO22
  - pin 16 = GPIO23
  - pin 18 = GPIO24
  - pin 22 = GPIO25
  - also a bunch more but they double for I2C, SPI, and UART

![old pi pinout](https://howto8165.files.wordpress.com/2014/08/rpi-pinout.png)

### Run in background

To run in background at startup, can use a cron job.
See [this instructable](https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/).

Run: 

```
sudo crontab -e
```

Then enter line:

```
@reboot /full/path/to/script/light_on_ping.py
```

### Challenges

- I had a problem where the script would start before the network connection had been established. 
  Fixed this by changing a setting in `raspi-config`: under "system options", there's an option 
  "network at boot", to wait for a network connection to be established before proceeding.

- My main challenge was a lot of false alarms. I thought this had to do with a weak WIFI signal 
  when I closed the cigar box I'd made to enclose the project. Seems to have been fixed by 
  using `ping response != 1` rather than `ping response == 0` as rule for success. 

### License

Released under the [MIT license](LICENSE.md).
