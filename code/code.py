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

print("Running music box")

# SPI for the SD card
spi_sd = busio.SPI(clock = board.GP10, MOSI = board.GP11, MISO = board.GP12) #clock, mosi, miso
# Select pin for the SD card
sd_select = digitalio.DigitalInOut(board.GP13)
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

# RFID card reader
spi_rfid = busio.SPI(board.GP18, board.GP19, board.GP16) #clock, mosi, miso
rfid = mfrc522.MFRC522(spi_rfid, board.GP28, board.GP17)


# I2S audio output & amp
amp_power = digitalio.DigitalInOut(board.GP26)
amp_power.switch_to_output()
audio = audiobusio.I2SOut(bit_clock=board.GP20, word_select=board.GP21, data=board.GP22)

# Make sure the amp is powered
amp_power.value = True


while True:
  (status, tag_type) = rfid.request(rfid.REQIDL)
  if status == rfid.OK:
    (stat, raw_uid) = rfid.anticoll()
    if (stat == rfid.OK):
      uid = "0x" + "%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
      path = "/sd/" + "%02x%02x%02x%02x.wav" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
      try:
        os.stat(path)
      except:
        path = "/unknown_card.wav"

      print("Playing path: "+path)

      with open(path, "rb") as wave_file:
        wave = audiocore.WaveFile(wave_file)
        audio.play(wave)
        while (audio.playing and stat == rfid.OK):
          time.sleep(0.5)
          (stat, raw_uid) = rfid.anticoll()

        print("Stopping audio path: "+path)
        audio.stop()
  #
  #   while (stat == rfid.OK):
  #     uid = "0x" + "%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
  #     path = "/sd/" + "%02x%02x%02x%02x.wav" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
  #     print("uuid: "+uid)
  #     time.sleep(1)
  #     (stat, raw_uid) = rfid.anticoll()
  #   print("not ok anticoll")
  # else:
  #   print("not ok requidl")
  time.sleep(1)



