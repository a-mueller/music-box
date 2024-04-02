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
import mfrc522
import alarm
import os

# RFID card reader
spi_rfid = busio.SPI(board.GP18, board.GP19, board.GP16) #clock, mosi, miso
rfid = mfrc522.MFRC522(spi_rfid, board.GP28, board.GP17)

while True:
    (status, tag_type) = rfid.request(rfid.REQIDL)
    if status == rfid.OK:
        (stat, raw_uid) = rfid.anticoll()
        while (stat == rfid.OK):
            uid = "0x" + "%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            path = "/sd/" + "%02x%02x%02x%02x.wav" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            print("uuid: "+uid)
            time.sleep(1)
            (stat, raw_uid) = rfid.anticoll()
        print("not ok anticoll")
    else:
        print("not ok requidl")
    time.sleep(1)

