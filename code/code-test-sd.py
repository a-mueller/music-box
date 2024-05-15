import time
import array
import math
import audiocore
import board
import audiobusio
import busio
import digitalio
import storage
import adafruit_sdcard
import alarm
import os

print("Running music box")

# SPI for the SD card
spi_sd = busio.SPI(clock = board.GP10, MOSI = board.GP11, MISO = board.GP12) #clock, mosi, miso
# Select pin for the SD card
sd_select = digitalio.DigitalInOut(board.GP9)
# SD card lib
sdcard = adafruit_sdcard.SDCard(spi_sd, sd_select)

while True:
  try:
    # mount the sd card to /sd
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    break
  except:
    print("Error mounting SD card")
    time.sleep(1)


try:
    os.stat("/sd/unknown_card.wav")
    print("file exists")
except:
    print("file error")




