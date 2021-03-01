![Upcycle camera](https://github.com/johnpeart/upcycle-camera/blob/main/README/banner.png?raw=true)

# Upcycle Camera

**A Raspberry Pi project. Upcycling an old camera with an HQ Camera sensor and touchscreen display.**

## About

I wanted to build my own camera, making use of the [HQ Camera module](https://www.raspberrypi.org/products/raspberry-pi-high-quality-camera/) for the Raspberry Pi. 

This repository contains information about the hardware and software I used to create my very own "Upcycle Camera".

## Hardware


### Camera body 

Let's start with the camera body: an original [Kodak Brownie Cresta](https://camerapedia.fandom.com/wiki/Kodak_Brownie_Cresta). I bought this for about £5 on eBay in an auction. 

I gutted the body, removing any internal components and removed the original lens. I also cut away the rear and a chunk from the centre-bottom of the case. I also drilled a new hole to house a new (digital!) shutter button. All this created enough room for the new, upgraded components.

### Electronics

For the electronics, I've used:

- [Raspberry Pi 4B](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) – though any B-sized Raspberry Pi should work in this size camera body
- [Raspberry Pi HQ Camera](https://www.raspberrypi.org/products/raspberry-pi-high-quality-camera/) – paired with a cheap attachable lens from Amazon
- [PiSugar 2 Pro](http://pisugar.com) – to provide external power when out and about
- [Waveshare 4.3" Capacitive Touch Display for Raspberry Pi, DSI Interface, 800×480](https://www.waveshare.com/4.3inch-DSI-LCD.htm) – to show the new camera interface

## Software

- Raspberry Pi OS Lite
    - xinit unclutter
    - lightdm 
    - openbox 
    - tint2
- Python 3
    - [picamera](http://picamera.readthedocs.io)
    - [tkinter](https://docs.python.org/3/library/tkinter.html)
    - [guizero](https://lawsie.github.io/guizero/)
    - [Pillow](https://pillow.readthedocs.io/en/stable/)
    - [gpiozero](https://gpiozero.readthedocs.io/en/stable/)

## Usage

### Install required packages for the camera app

I started with a clean install of Raspbery Pi OS (née Raspbian Buster). You could also use the desktop version, but I'm keeping things light! To install all of the required software packages, you can use these two commands:

```
sudo apt-get install python3-pip python-picamera python3-picamera python3-gpiozero python3-tk libopenjp2-7 libtiff5 lightdm openbox obconf menu obmenu feh tint2 xfce4-panel xinit unclutter
```

```
sudo pip3 install pillow guizero
```

This will install PIP, the required Python libraries for the camera, GPIO pins and GUI, and the necessary libraries for displaying a slimmed down desktop environment and window manager.

### Install the battery software

After a failed attempt to get the PiJuice battery system working, I switched to the [PiSugar 2 Pro]. With this software installed, you get a little web server that allows you to see and control battery functions over a local network connection. The camera app pings this server to check the battery level every minute or so.

Install the software with: 

`curl http://cdn.pisugar.com/release/Pisugar-power-manager.sh | sudo bash`

### Give the `pi` user `root` privileges 

To make sure you have the ability to write and execute the programme in the desktop environment you'll create, add add the default `pi` user to `root`.

```
sudo su
adduser pi root
adduser pi sudo
adduser pi netdev 
adduser pi users
```

I found that the `pi` was already a member of these groups by default, but it's worth double checking!

Edit `/etc/sudoers` file in your preferred editor – e.g. `sudo nano /etc/sudoers`

Amend the file to look like this:

```
# User privilege specification
root	ALL=(ALL:ALL) ALL

# Allow members of group sudo 
# to execute any command
%sudo	ALL=(ALL:ALL) ALL

# add this below
pi ALL=(ALL) NOPASSWD: ALL
```

### Create the desktop environment

Next you'll want to make sure you tell the OS to boot into the desktop environment.

Run `sudo raspi-config` and navigate to `3 Boot Options` / `B1 Desktop / Cli` and choose `B2 Console Autologin`.

Edit `rc.local` in your preferred editor – e.g. `sudo nano /etc/rc.local`. 

At the end, **before** `exit 0` add `startx &`. Close the file when you're done.

> **WARNING**: It is very important you put the commands in `rc.local` **before** the `exit 0`!

Edit `xinitrc` in your preferred editor – e.g. `sudo nano /etc/X11/xinit/xinitrc`

Comment this line (add a hash to the start)

```
# . /etc/X11/xsession
```

Add this line to start openbox:

```
exec openbox-session
```

Close this file when you're done.

### Run apps on start up

Next you need to tell Openbox which programmes to run when it's finished loading by adding your programs with `autostart`.

```
sudo nano /etc/xdg/openbox/autostart
```

Add your commands so that it runs:

1. `tint2` – for creating a dock from which you can load programmes. You'll want to reference the custom set up file in this directory so that it adds an icon that loads this app
2. `unclutter` – to hide the mouse pointer on the touch screen
3. the camera app

```
tint2 -c /home/pi/hqcamera/tint2.conf &
unclutter -idle 0 &
/home/pi/hqcamera/main.py & # << This is the Python app
```

> **IMPORTANT:** End all commands with `&` or they will prevent the others from loading.

### Create a folder for your photos

Next you will need to create a directory called `photos` in your `pi` home folder to store images in.

```
mkdir $HOME/photos
```

Now if you `sudo reboot`, the desktop environment should load along with the camera interface. You should see something like this: 


![Upcycle camera](https://github.com/johnpeart/upcycle-camera/blob/main/README/screenshot.png?raw=true)

### Save some power

You may want to additionally turn off some hardware features to save some power. I chose to switch off the HDMI ports and USB ports as they're not used.

#### Turn off USB power

Turn off the USB ports (and thus stop them using any power!) with the following command:

```
echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/unbind
```

Switch `unbind` to `bind` to turn them back on.

#### Turn off HDMI power

Turn off the HDMI ports (and thus stop them using any power!) with the following command:

```
sudo /opt/vc/bin/tvservice -o
```

Switch `-o` to `-p` to turn them back on.

> https://learn.pi-supply.com/make/how-to-save-power-on-your-raspberry-pi/ 


## Acknowledgements

Tips on setting up the desktop environment – [Bristol Watch](http://www.bristolwatch.com/rpi/rpi_openbox.htm)
Tips on power saving – [Pi Supply](https://learn.pi-supply.com/make/how-to-save-power-on-your-raspberry-pi/)