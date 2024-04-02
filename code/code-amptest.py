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


amp_power = digitalio.DigitalInOut(board.GP26)
amp_power.switch_to_output()


# I2S audio output
audio = audiobusio.I2SOut(bit_clock=board.GP20, word_select=board.GP21, data=board.GP22)

# Make sure the amp is powered
amp_power.value = True

with open("/unknown_card.wav", "rb") as wave_file:
    wave = audiocore.WaveFile(wave_file)
    audio.play(wave)
    while audio.playing:
        time.sleep(0.5)
    audio.stop()

amp_power.value = False

