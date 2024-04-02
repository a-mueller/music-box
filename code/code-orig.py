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


amp_power = digitalio.DigitalInOut(board.GP20)
amp_power.switch_to_output()
 


# RFID card reader
# spi_rfid = busio.SPI(board.GP18, board.GP19, board.GP16) #clock, mosi, miso
# rfid = mfrc522.MFRC522(spi_rfid, board.GP28, board.GP17)

if alarm.wake_alarm != None:
  # This means we were woken up from deep sleep, just check if there is a card and go back to sleep if not
  (status, tag_type) = rfid.request(rfid.REQIDL)
  if status != rfid.OK:
    rfid.power_off()
    amp_power.value = False
    # go back to deep sleep
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 2)
    # Exit the program, and then deep sleep until the alarm wakes us.
    alarm.exit_and_deep_sleep_until_alarms(time_alarm)
    

# SPI for the SD card
spi_sd = busio.SPI(clock = board.GP2, MOSI = board.GP0, MISO = board.GP3) #clock, mosi, miso
# Select pin for the SD card
sd_select = digitalio.DigitalInOut(board.GP1)
# SD card lib
sdcard = adafruit_sdcard.SDCard(spi_sd, sd_select)
# mount the sd card to /sd
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# I2S audio output
audio = audiobusio.I2SOut(bit_clock=board.A0, word_select=board.A1, data=board.MOSI)


# Make sure the amp is powered
amp_power.value = True

no_card_count = 0

while no_card_count < 100:
  (status, tag_type) = rfid.request(rfid.REQIDL)

  if status == rfid.OK:
    (stat, raw_uid) = rfid.anticoll()
    if stat == rfid.OK:
      no_card_count = 0
      uid = "0x" + "%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
      path = "/sd/" + "%02x%02x%02x%02x.wav" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
      try:
        os.stat(path)
      except:
        path = "/unknown_card.wav"
        
      #print("found card: "+uid)
      with open(path, "rb") as wave_file:
        wave = audiocore.WaveFile(wave_file)
        audio.play(wave)
        card_missing_count = 0
        while audio.playing:
          time.sleep(0.5)
          (st, t) = rfid.request(rfid.REQIDL)
          if st == rfid.OK:
            card_missing_count = 0
          else:
            card_missing_count += 1
            
          if (card_missing_count > 3):  
            break
                                                 
        audio.stop()
  else:
    no_card_count += 1
    time.sleep(0.1)
    

# go back to deep sleep
rfid.power_off()
amp_power.value = False
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 2)
# Exit the program, and then deep sleep until the alarm wakes us.
alarm.exit_and_deep_sleep_until_alarms(time_alarm)


