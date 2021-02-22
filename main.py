#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import logging
from subprocess import Popen, PIPE
from tkinter import * 
from guizero import App, PushButton, Picture, info
from PIL import Image
from picamera import *
from gpiozero import Button
from signal import pause
from datetime import datetime
from time import sleep

# Import the settings
import settings

# LOGGING
# Set up error logging
logging.basicConfig(filename="/home/pi/hqcamera/log.log", filemode='w', format="%(asctime)s – %(name)s – %(levelname)s – %(message)s", level=logging.ERROR)

#########################
## NUCLEAR OPTIONS     ##
######################### 

# This function closes the app.
# The app can be restarted from the desktop if needed.
def closeApp():
    deactivateCamera() # Close the camera or the programme might not restart!
    app.destroy() # Close the app itself

# Deactivate the camera
def deactivateCamera():
    camera.close()
    print('The camera has been deactivated')
    
# Turn off the device
def turnOffDevice():
    print("Shutting down device...")
    os.system("shutdown now -h")

# Reboot the device
def rebootDevice():
    print("Restarting device...")
    os.system("shutdown now -r")
    
#########################
## BATTERY CHECK       ##
#########################

def checkBatteryLevel(icon):
    
    icon_battery = icon
    
    check = Popen("echo \"get battery\" | nc -q 0 127.0.0.1 8423", shell=True, stdout=PIPE).stdout
    output = check.read()
    output = str(output)[11:-3]
    
    batteryLevel = round(float(output))
    
    if batteryLevel >= 90:
        
        # show battery100 image
        icon_battery.value = "/home/pi/hqcamera/assets/icons/battery100.png"
        
    elif batteryLevel >= 75:
        
        # show battery75 image
        icon_battery.value = "/home/pi/hqcamera/assets/icons/battery75.png"
        
    elif batteryLevel >= 50:
        
        # show battery50 image
        icon_battery.value = "/home/pi/hqcamera/assets/icons/battery50.png"
        
    elif batteryLevel >= 25:
        
        # show battery25 image
        icon_battery.value = "/home/pi/hqcamera/assets/icons/battery25.png"
    
    elif batteryLevel > 0:
        
        # show battery10 image
        icon_battery.value = "/home/pi/hqcamera/assets/icons/battery10.png"
    
    else:
        
        icon_battery.value = "/home/pi/hqcamera/assets/icons/batteryunknownvalue.png"
        # show unknown level
        
    
    # batteryLevel = "The battery level is {}%".format(output)
    # 
    # app.info("Battery level", batteryLevel)


#########################
## SET CAM SETTINGS    ##
######################### 

# Read the current settings from settings.py 'camera' dictionary.
# This is so they can be applied to the camera preview or image captures.

def setCameraSettings(camera, mode = "live"):

    if mode == "preview":
        camera.resolution = (settings.camera["preview"]) # Maximum resolution (2592, 1944)
    else:
        camera.resolution = (settings.camera["live"])
    camera.framerate = settings.camera["framerate"]
    camera.iso = settings.iso[settings.camera["iso"]]
    camera.shutter_speed = camera.exposure_speed
    camera.brightness = settings.camera["brightness"]
    camera.contrast = settings.camera["contrast"]
    camera.awb_mode = settings.exposure_modes[settings.camera["exposure_mode"]]
    camera.exposure_mode = settings.exposure_modes[settings.camera["exposure_mode"]]
    camera.image_effect = settings.image_effects[settings.camera["image_effect"]]
    camera.hflip = settings.camera["hflip"]
    camera.vflip = settings.camera["vflip"]
    camera.rotation = settings.camera["orientation"]
    camera.annotate_text_size = settings.camera["annotate_text_size"]
    
    return camera

#########################
## CONTROL CAM PREVIEW ##
######################### 

# These functions start and stop the camera preview

def startCameraPreview():
    setCameraSettings(camera, mode = "preview")
    camera.start_preview(fullscreen=False, window=(0, 0, 400, 240))
    print('The camera preview is running')
    
def stopCameraPreview():
    camera.stop_preview()
    print('The camera preview is not running')
        
def refreshCameraPreview(msg = "Restarting camera preview..."):
    print(msg)
    startCameraPreview()
    print('Camera preview restarted!')
    
#########################
## TAKE A PICTURE      ##
######################### 

# Take a picture! Obviously...
    
def takeAPicture():

    setCameraSettings(camera, mode = "live")
    countdowntimer = settings.camera["countdowntimer"]
    
    logging.info("Running camera capture script")
    
    timestamp = datetime.now().isoformat()
    print("Set time to {}".format(timestamp))
    
    camera.start_preview(fullscreen=True)

    sleep(countdowntimer)
    
    print("Capture the photo...")
    camera.capture("/home/pi/photos/%s.jpg" % timestamp, format="jpeg", quality=100)
    print("Photo captured...")
    
    camera.stop_preview()
    print("Stop the preview.")

def pushButton():
    # Print the Orientation setting
    print("Button pressed")

    
#########################
## BRIGHTNESS SETTINGS ##
######################### 

def changeBrightness(change):
    
    if change == "up":
        if settings.camera["brightness"] >= 100:
            print("Maximum brightness set")
        else:
            settings.camera["brightness"] += 10
            refreshCameraPreview("Brightness changed. Resetting camera preview...")
    elif change == "down":
        if settings.camera["brightness"] <= 0:
            print("Minimum brightness set")
        else:
            settings.camera["brightness"] -= 10
            refreshCameraPreview("Brightness changed. Resetting camera preview...")
    elif change == "reset":
        settings.camera["brightness"] = 50
        refreshCameraPreview("Brightness changed. Resetting camera preview...")
    else:
        settings.camera["brightness"] = 50
        print("Set default brightness to 50")
        refreshCameraPreview("Brightness changed. Resetting camera preview...")
    
#######################
## CONTRAST SETTINGS ##
####################### 

def changeContrast(change):
    
    if change == "up":
        if settings.camera["contrast"] >= 100:
            print("Maximum contrast set")
        else:
            settings.camera["contrast"] += 10
            refreshCameraPreview("Contrast changed. Resetting camera preview...")
    elif change == "down":
        if settings.camera["contrast"] <= -100:
            print("Minimum contrast set")
        else:
            settings.camera["contrast"] -= 10
            refreshCameraPreview("Contrast changed. Resetting camera preview...")
    elif change == "reset":
        settings.camera["contrast"] = 0
        refreshCameraPreview("Contrast changed. Resetting camera preview...")
    else:
        settings.camera["contrast"] = 0
        print("Set default contrast to 0")
        refreshCameraPreview("Contrast changed. Resetting camera preview...")
        
#######################
## ISO SETTINGS      ##
####################### 

def changeISO(change):
    
    n = len(settings.iso) - 1 # number of items in settings list
    
    if change == "up":
        if settings.camera["iso"] >= n:
            print("Maximum ISO set")
        else:
            settings.camera["iso"] += 1
            refreshCameraPreview("ISO changed. Resetting camera preview...")
    elif change == "down":
        if settings.camera["iso"] <= 1:
            print("Minimum ISO set")
        else:
            settings.camera["iso"] -= 1
            refreshCameraPreview("ISO changed. Resetting camera preview...")   
    elif change == "auto":
        settings.camera["iso"] = 0
        refreshCameraPreview("ISO changed. Resetting camera preview...")
    else:
        settings.camera["iso"] = 0
        refreshCameraPreview("ISO changed. Resetting camera preview...")
        
###########################
## FILTER SETTINGS       ##
########################### 

# The default exposure mode is "auto" (0).
# This function increments the index value and reads the appropriate value.
# The total number of options are

def changeFilter(change):
    
    n = len(settings.image_effects) - 1 # number of items in settings list
    
    if change == "next":
        if settings.camera["image_effect"] >= n:
            settings.camera["image_effect"] = 0
            print("End of list, resetting...")
        else:
            settings.camera["image_effect"] += 1
            refreshCameraPreview("Image effect changed. Resetting camera preview...")
    elif change == "previous":
        if settings.camera["image_effect"] <= 0:
            settings.camera["image_effect"] = n
            print("Start of list, resetting...")
        else:
            settings.camera["image_effect"] -= 1
            refreshCameraPreview("Image effect changed. Resetting camera preview...")   
    elif change == "reset":
        settings.camera["image_effect"] = 0
        refreshCameraPreview("Image effect changed. Resetting camera preview...")
    else:
        settings.camera["image_effect"] = 0
        refreshCameraPreview("Image effect changed. Resetting camera preview...")
    
    # Print the Orientation setting
    print("Filter set to {}.".format(settings.image_effects[settings.camera["image_effect"]]))
    refreshCameraPreview("Filter changed. Resetting camera preview...")
    
##############################
## COUNTDOWN TIMER SETTINGS ##
############################## 

# The default timer is 2 second and can be increased to 10 seconds in 1 second increments.
# The timer dictates how long the preview displays for before the camera takes a photo.
# The minimum is 2 seconds because that's the 'warm up time' recommended in the docs.

def changeTimer(s):
    
    settings.camera["countdowntimer"] = s
    # Print the timer setting
    print("Timer set to {} second.".format(settings.camera["countdowntimer"]))
    
##########################
## ORIENTATION SETTINGS ##
########################## 

# The camera is fitted upside-down because of space, so the default is 180 degrees.

def changeOrientation(change):
    # Print the Orientation setting
    currentOrientation = settings.camera["orientation"]
    
    if change == "reset":
        settings.camera["orientation"] = 0
    elif currentOrientation == 0:
        if change == "plus":
            settings.camera["orientation"] += 90
        if change == "minus":
            settings.camera["orientation"] = 270    
    elif currentOrientation == 90:
        if change == "plus":
            settings.camera["orientation"] += 90
        if change == "minus":
            settings.camera["orientation"] -= 90        
    elif currentOrientation == 180:
        if change == "plus":
            settings.camera["orientation"] += 90
        if change == "minus":
            settings.camera["orientation"] -= 90        
    elif currentOrientation == 270:
        if change == "plus":
            settings.camera["orientation"] = 0
        if change == "minus":
            settings.camera["orientation"] -= 90
    else:
        settings.camera["orientation"] = 0
    
    print("Camera rotated to {} degrees.".format(settings.camera["orientation"]))
    
    refreshCameraPreview("Orientation changed. Resetting camera preview...")
    
    
    
    
###########################
## GRAPHICAL INTERFACE   ##
########################### 

def loadGUI(app, camera):
    
    # SETTING UP THE GUI    
    app.set_full_screen()
    
    ###################
    # Nuclear options
    btn_closeApp = PushButton(app, command=closeApp, grid=[0,0,1,3], image="/home/pi/hqcamera/assets/icons/home.png").tk.config(width=194, height=234, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#d4351c")
    btn_turnOffDevice = PushButton(app, command=turnOffDevice, grid=[1,0], image="/home/pi/hqcamera/assets/icons/shutdown.png").tk.config(width=194, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#d4351c") 
    btn_rebootDevice = PushButton(app, command=rebootDevice, grid=[1,1], image="/home/pi/hqcamera/assets/icons/reboot.png").tk.config(width=194, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#f47738") 
    # btn_deactivateCamera = PushButton(app, command=deactivateCamera, grid=[0,2], image="/home/pi/hqcamera/assets/icons/stopCamera.png").tk.config(width=194, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#d4351c")
    
    ###################
    # Battery icon
    icon_battery = Picture(app, grid=[1,4,1,2], image="/home/pi/hqcamera/assets/icons/batteryunknown.png")
    icon_battery.after(3000, checkBatteryLevel, args=[icon_battery])
    icon_battery.repeat(30000, checkBatteryLevel, args=[icon_battery])
    icon_battery.tk.config(width=194, height=154, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#000000")
    
    ###################
    # Shutter button
    btn_takeAPicture = PushButton(app, command=takeAPicture, grid=[0,3,1,3], image="/home/pi/hqcamera/assets/icons/capture.png").tk.config(width=194, height=234, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#0BD318")
    
    ###################
    # Preview toggles
    btn_startCameraPreview = PushButton(app, command=startCameraPreview, grid=[1,2], image="/home/pi/hqcamera/assets/icons/startPreview.png").tk.config(width=194, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#00703c")
    btn_stopCameraPreview = PushButton(app, command=stopCameraPreview, grid=[1,3], image="/home/pi/hqcamera/assets/icons/stopPreview.png").tk.config(width=194, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#d4351c")
    
    ######################
    # Brightness toggles
    icon_brightness = Picture(app, grid=[2,0], image="/home/pi/hqcamera/assets/icons/brightness.png").tk.config(width=158, height=74, bd=0, highlightthickness=0, bg="#000000")
    btn_brightnessReset = PushButton(app, command=changeBrightness, args=["reset"], grid=[3,0], image="/home/pi/hqcamera/assets/icons/reset.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    btn_brightnessUp = PushButton(app, command=changeBrightness, args=["up"], grid=[4,0], image="/home/pi/hqcamera/assets/icons/plus.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    btn_brightnessDown = PushButton(app, command=changeBrightness, args=["down"], grid=[5,0], image="/home/pi/hqcamera/assets/icons/minus.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    
    ######################
    # Contrast toggles
    icon_contrast = Picture(app, grid=[2,1], image="/home/pi/hqcamera/assets/icons/contrast.png").tk.config(width=158, height=74, bd=0, highlightthickness=0, bg="#000000")
    btn_contrastReset = PushButton(app, command=changeContrast, args=["reset"], grid=[3,1], image="/home/pi/hqcamera/assets/icons/reset.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    btn_contrastUp = PushButton(app, command=changeContrast, args=["up"], grid=[4,1], image="/home/pi/hqcamera/assets/icons/plus.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    btn_contrastDown = PushButton(app, command=changeContrast, args=["down"], grid=[5,1], image="/home/pi/hqcamera/assets/icons/minus.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    
    ######################
    # ISO toggles
    icon_iso = Picture(app, grid=[2,2], image="/home/pi/hqcamera/assets/icons/iso.png").tk.config(width=158, height=74, bd=0, highlightthickness=0, bg="#000000")
    btn_isoAuto = PushButton(app, command=changeISO, args=["auto"], grid=[3,2], image="/home/pi/hqcamera/assets/icons/auto.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    btn_isoUp = PushButton(app, command=changeISO, args=["up"], grid=[4,2], image="/home/pi/hqcamera/assets/icons/plus.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    btn_isoDown = PushButton(app, command=changeISO, args=["down"], grid=[5,2], image="/home/pi/hqcamera/assets/icons/minus.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    
    ######################
    # Filters toggles
    icon_iso = Picture(app, grid=[2,3], image="/home/pi/hqcamera/assets/icons/filter.png").tk.config(width=158, height=74, bd=0, highlightthickness=0, bg="#000000")
    btn_filterReset = PushButton(app, command=changeFilter, args=["reset"], grid=[3,3], image="/home/pi/hqcamera/assets/icons/reset.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    btn_filterPrevious = PushButton(app, command=changeFilter, args=["previous"], grid=[4,3], image="/home/pi/hqcamera/assets/icons/previous.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    btn_filterNext = PushButton(app, command=changeFilter, args=["next"], grid=[5,3], image="/home/pi/hqcamera/assets/icons/next.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    # btn_changeFilter = PushButton(app, command=changeFilter, grid=[3,4], image="/home/pi/hqcamera/assets/icons/btn_Camera_FiltersToggle.png").tk.config(width=198, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    
    ######################
    # Timer toggles
    icon_timer = Picture(app, grid=[2,4], image="/home/pi/hqcamera/assets/icons/timer.png").tk.config(width=158, height=74, bd=0, highlightthickness=0, bg="#000000")
    btn_timer3s = PushButton(app, command=changeTimer, args=[3], grid=[3,4], image="/home/pi/hqcamera/assets/icons/3s.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    btn_timer5s = PushButton(app, command=changeTimer, args=[5], grid=[4,4], image="/home/pi/hqcamera/assets/icons/5s.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    btn_timer10s = PushButton(app, command=changeTimer, args=[10], grid=[5,4], image="/home/pi/hqcamera/assets/icons/10s.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    
    ######################
    # Orientation toggles
    icon_orientation = Picture(app, grid=[2,5], image="/home/pi/hqcamera/assets/icons/orientation.png").tk.config(width=158, height=74, bd=0, highlightthickness=0, bg="#000000")
    btn_orientation = PushButton(app, command=changeOrientation, args=["minus"], grid=[3,5], image="/home/pi/hqcamera/assets/icons/orientminus90.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    btn_orientation = PushButton(app, command=changeOrientation, args=["reset"], grid=[4,5], image="/home/pi/hqcamera/assets/icons/orient0.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    btn_orientations = PushButton(app, command=changeOrientation, args=["plus"], grid=[5,5], image="/home/pi/hqcamera/assets/icons/orientplus90.png").tk.config(width=74, height=74, bd=0, highlightthickness=2, highlightbackground="black", activebackground="#ffdd00", bg="#666666")
    
    app.display()


if os.environ.get("DISPLAY","") == "":
    print("No display found. Using :0.0")
    os.environ.__setitem__("DISPLAY", ":0.0")

if __name__ == '__main__':
    
    try:
        # Initialise the camera hardware
        camera = PiCamera()
        logging.info("Camera activated") 
    except:
        logging.error("Cannot start camera. PiCamera may already in use by another process")
        try:
            camera.close()
        except:
            logging.error("Could not close existing instance of PiCamera. You may need to reboot the device.")
        exit(1)
        
    try:
        # Initialise the hardware button that triggers the shutter
        button_CameraCaptureButton = Button(21)
        button_CameraCaptureButton.when_pressed = takeAPicture
        logging.info("Hardware shutter button ready")   
    except:
        logging.error("Could not initialise hardware shutter button")
        exit(1)
        
    try:
        # Load the GUI
        app = App(title="Camera", layout="grid", width=800, height=480, bg=settings.app["background"])
        loadGUI(app, camera)
        logging.info("Interface loaded")   
    except:
        logging.info("Interface could not be loaded")   
