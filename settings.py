# GUI SETTINGS
app = {
    
    "background": "#000000",
    "color": "#FFFFFF",
    
    "font": "ChicagoFLF"
    
}

# CAMERA SETTINGS
# Set the defaults and options
iso = [0, 100, 200, 320, 400, 500, 640, 800]
awb_modes = ["auto", "sunlight", "cloudy", "shade", "tungsten", "fluorescent", "incandescent", "flash", "horizon"]
exposure_modes = ["auto", "night", "nightpreview", "backlight", "spotlight", "sports", "snow", "beach", "verylong", "fixedfps", "antishake", "fireworks"]
image_effects = ["none", "negative", "solarize", "sketch", "denoise", "emboss", "oilpaint", "hatch", "gpen", "pastel", "watercolor", "film", "blur", "saturation", "colorswap", "washedout", "posterise", "colorpoint", "colorbalance", "cartoon", "deinterlace1", "deinterlace2"]

camera = {

    #############################
    ## SET THE CAMERA DEFAULTS ##
    #############################
    # This sets out the initial settings for the camera.
    
    "live": (2028, 1520), # width and height of the image taken in pixels. Max: 2592, 1944
    "preview": (392, 232), # width and height of the preview in pixels. Max: 2592, 1944
    
    "countdowntimer": 3,
    
    "framerate": 15, # video frame rate
    "shutter_speed": 0, # shutter speed - 0 defaults to auto
    
    "brightness": 50, # brightness of the camera. Accepts: '0' to '100'
    "contrast": 0, # contrast of the camera. Accepts: '-100' to '100'
    "iso": 0, # sets the ISO
    
    "awb_mode": 0, # auto, sunlight, cloudy, shade, tungsten, fluorescent, incandescent, flash, horizon
    "exposure_mode": 0, # auto, night, nightpreview, backlight, spotlight, sports, snow, beach, verylong, fixedfps, antishake, fireworks
    "image_effect": 0, # none, negative, solarize, sketch, denoise, emboss, oilpaint, hatch, gpen, pastel, watercolor, film, blur, saturation, colorswap, washedout, posterise, colorpoint, colorbalance, cartoon, deinterlace1, deinterlace2
    
    "orientation": 0,
    "hflip": True,
    "vflip": True,
    
    "annotate_text_size": 50
    
}