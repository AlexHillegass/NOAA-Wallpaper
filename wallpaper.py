import requests
import ctypes
from PIL import Image
from io import BytesIO
import numpy as np
import os
"""
By: Alex Hillegass
pyinstaller --onefile background.py
Must set task to run using windows Task Scheduler.
"""
NOAA = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/taw/GEOCOLOR/latest.jpg'
# PATH = os.path.dirname(os.path.abspath(__file__)) + "\\"
# USER = os.getlogin()
PATH = "C:/Users/Public/Pictures/"
NAME = "NOAA_SATELLITE_IMAGE.jpg"

RESPONSE_SUCCESS_CODE = 200     # OK response to get request
SPI_SETDESKWALLPAPER = 20       # setting index for desktop background

DESKTOP_SIZE = (1080, 3840)     # dual screened 1080 x 1920

X_SHIFT = 600                   # Shift down to cut most of the US out
Y_SHIFT = 0

def main():
    print('Retreiving image.')
    res = requests.get(NOAA, allow_redirects=True)

    if res.status_code is RESPONSE_SUCCESS_CODE:
        print('Image recieved.')
        print('Processing image.')
        # Open, process, and save. It's that easy.
        img = Image.open(BytesIO(res.content))
        # TODO: remove white lines
        img = process_image(img)

        print('Image processed.')
        print('Saving image.')
        #  TODO: check if image is saved
        img.save( PATH+NAME )

        print('Image saved.')
        print('Setting background.')
        set_background_python3_windows( PATH+NAME )
    else:
        print('ERROR: status code recieved %d.' % (res.status_code))


def process_image(img):
    """
    Convert to numpy array to crop the image. Then return it as an image
    """
    img = np.array(img)
    img = img[ X_SHIFT:X_SHIFT+DESKTOP_SIZE[0], Y_SHIFT:Y_SHIFT+DESKTOP_SIZE[1] ]

    # convert np to an image and and return
    img = Image.fromarray((img).astype(np.uint8))

    return img

def set_background_python3_windows(path):
    """
    Python 3 on Windows 10 uses this method for setting the backgound.
    """
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)

if __name__ == "__main__":
    print(PATH)
    main()