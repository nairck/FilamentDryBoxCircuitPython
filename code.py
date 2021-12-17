# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Monitor customisable temperature and humidity ranges, with an optional audible alarm tone."""
import board
import time
from math import atan2, degrees
import math as Math
import board
import adafruit_lis3mdl

from adafruit_clue import clue

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_lis3mdl.LIS3MDL(i2c)

# degreeSign = "{}".format(chr(176)) #"\N{DEGREE SIGN}"
tempHumiScale = 3
tempHumiScale2 = 5
headingScale = 2

temp_loc = 2
temp_loc_num = 3
hum_loc = 7
hum_loc_num = 8
press_loc = 14
mag_loc = 12
card_loc = 13
acc_loc = 15
gyr_loc = 16

# Set desired temperature range in degrees Celsius.
min_temperature = 19
mid1_temperature = 22
mid2_temperature = 23
max_temperature = 25

# Set desired humidity range in percent.
prime_humidity = 13
min_humidity = 20
mid1_humidity = 35
mid2_humidity = 45
max_humidity = 55

# Set desired pressure range in percent.
min_pressure = 101
mid1_pressure = 102
mid2_pressure = 103
max_pressure = 104


clue_display = clue.simple_text_display(
    title="Environmental Status", title_scale=2, text_scale=1, colors=(clue.RED,)
)



def get_heading(_sensor):

    magnet_x, magnet_y, _ = _sensor.magnetic
    angle = degrees(atan2(magnet_x, magnet_y))

    if angle < 0:
        angle += 360

    if int(angle) in range(330, 360):
        cardinalHeading = "  North   "
    elif int(angle) in range(0, 30):
        cardinalHeading = "  North   "
    elif int(angle) in range(300, 330):
        cardinalHeading = " North-West"
    elif int(angle) in range(240, 300):
        cardinalHeading = "  West    "
    elif int(angle) in range(210, 240):
        cardinalHeading = " South-West"
    elif int(angle) in range(150, 210):
        cardinalHeading = "  South   "
    elif int(angle) in range(120, 150):
        cardinalHeading = " South-East"
    elif int(angle) in range(60, 120):
        cardinalHeading = "  East    "
    elif int(angle) in range(30, 60):
        cardinalHeading = " North-East"
    else:
        cardinalHeading = "            "

    return cardinalHeading, angle




while True:

    temperature = clue.temperature - 4
    humidity = clue.humidity
    pressure = clue.pressure * 0.1

    clue_display[temp_loc].text = "Tmp:        C"
    clue_display[temp_loc_num].text = "   {:.1f}".format(temperature)
    clue_display[hum_loc].text = "Hum:        %"
    clue_display[hum_loc_num].text = "   {:.1f}".format(humidity)
    clue_display[press_loc].text = "Pressure: {:.2f} kPa".format(pressure)
    clue_display[temp_loc].scale = tempHumiScale
    clue_display[hum_loc].scale = tempHumiScale
    clue_display[temp_loc_num].scale = tempHumiScale2
    clue_display[hum_loc_num].scale = tempHumiScale2
    clue_display[press_loc].scale = 1

    if temperature < min_temperature:
        clue_display[temp_loc].color = clue.AQUA
        clue_display[temp_loc_num].color = clue.AQUA
    elif int(temperature) in range(min_temperature, mid1_temperature):
        clue_display[temp_loc].color = clue.SKY
        clue_display[temp_loc_num].color = clue.SKY
    elif int(temperature) in range(mid1_temperature, mid2_temperature):
        clue_display[temp_loc].color = clue.GREEN
        clue_display[temp_loc_num].color = clue.GREEN
    elif int(temperature) in range(mid2_temperature, max_temperature):
        clue_display[temp_loc].color = clue.GOLD
        clue_display[temp_loc_num].color = clue.GOLD
    elif temperature > max_temperature:
        clue_display[temp_loc].color = clue.ORANGE
        clue_display[temp_loc_num].color = clue.ORANGE


    if humidity < prime_humidity:
        clue_display[hum_loc].color = clue.AQUA
        clue_display[hum_loc_num].color = clue.AQUA
    elif int(humidity) in range(prime_humidity, min_humidity):
        clue_display[hum_loc].color = clue.SKY
        clue_display[hum_loc_num].color = clue.SKY
    elif int(humidity) in range(min_humidity, mid1_humidity):
        clue_display[hum_loc].color = clue.GREEN
        clue_display[hum_loc_num].color = clue.GREEN
    elif int(humidity) in range(mid1_humidity, mid2_humidity):
        clue_display[hum_loc].color = clue.GOLD
        clue_display[hum_loc_num].color = clue.GOLD
    elif int(humidity) in range(mid2_humidity, max_humidity):
        clue_display[hum_loc].color = clue.ORANGE
        clue_display[hum_loc_num].color = clue.ORANGE
    elif humidity > max_humidity:
        clue_display[hum_loc].color = clue.RED
        clue_display[hum_loc_num].color = clue.RED


    if float(pressure) < min_pressure:
        clue_display[press_loc].color = clue.CYAN
    elif float(pressure) in range(min_pressure, mid1_pressure):
        clue_display[press_loc].color = clue.GREEN
    elif float(pressure) in range(mid1_pressure, mid2_pressure):
        clue_display[press_loc].color = clue.GOLD
    elif float(pressure) in range(mid2_pressure, max_pressure):
        clue_display[press_loc].color = clue.ORANGE
    elif pressure > max_pressure:
        clue_display[press_loc].color = clue.RED
    clue.sea_level_pressure = 1025
    # clue_display[alt_loc].text = "   Altitude: {:.2f} meters".format(clue.altitude)
    # clue_display[mag_loc].text = "Magnetic: < {:.4f}  {:.4f}  {:.4f} >".format(
    #    *clue.magnetic
    # )

    cD, hD = get_heading(sensor)
    clue_display[mag_loc].scale = headingScale
    clue_display[mag_loc].color = clue.SKY
    clue_display[card_loc].color = clue.SKY
    clue_display[mag_loc].text = "Dir:{}".format(
        cD
    )
    clue_display[card_loc].text = "                              ({:.1f}deg)".format(
        hD
    )

    clue_display[acc_loc].text = "   Accel: < {:.2f} {:.2f} {:.2f} > m/s^2".format(
        *clue.acceleration
    )

    clue_display[gyr_loc].text = "    Gyro: < {:.2f} {:.2f} {:.2f} > rad/s^{a}".format(
        *clue.gyro, a="2"
    )


    clue_display.show()
