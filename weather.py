#!/usr/bin/env python
# coding: utf-8

import requests
import json
import datetime
import re
import configparser


def load_data():

    config_filename = "weather.conf"
    config = configparser.ConfigParser()
    config.read(config_filename)

    latitude = config['default']['latitude']
    longitude = config['default']['longitude']
    api_key = config['default']['api_key']

    url = f"https://api.darksky.net/forecast/{api_key}/{latitude},{longitude}"

    req = requests.get(url)

    # with open("tmp.json") as fd:
    #     data = fd.read()

    data = json.loads(req.content.decode())
    return data

def print_hourly(data=None):

    reset = "\033[m"
    black = "\033[0;30m"
    blue  = "\033[0;34m"
    green = "\033[0;32m"
    cyan  = "\033[0;36m"
    red  = "\033[0;31m"
    purple = "\033[0;35m"
    brown = "\033[0;33m"
    light_gray = "\033[0;37m"
    dark_gray = "\033[1;30m"
    light_blue = "\033[1;34m"
    light_green = "\033[1;32m"
    light_cyan = "\033[1;36m"
    light_red = "\033[1;31m"
    light_purple = "\033[1;35m"
    yellow = "\033[1;33m"
    white = "\033[1;37m"


    if data is None:
        data = load_data()

    header = "  Time               |  Summary                  |  Temp   |  Winds                   |  Precip "
    header_border = "="* len(header)

    print(white, end='')
    print(header)
    print(header_border)
    border = "-"* len(header)
    newday = re.compile("00:00:00")

    i = 0
    for hour in data['hourly']['data']:
        if i > 24:
            break
        i += 1

        time = datetime.datetime.fromtimestamp(hour['time'])
        summary = hour['summary']
        temperature = hour['temperature']
        windspeed = hour['windSpeed']
        windgust = hour['windGust']
        precip_probablity = hour['precipProbability']

        temperature = f'{temperature:0.1f}'.ljust(5)
        summary = f'{summary}'.ljust(25)
        windspeed = f'{windspeed:0.1f}'.rjust(4)
        windgust = f'{windgust:0.1f}'.rjust(5)
        precip_probablity = f'{int(precip_probablity*100):}%'.rjust(4)

        time_color = white
        sumary_color = cyan
        temperature_color = green
        windspeed_color = purple
        windspeed_color = purple
        precip_color = yellow

        output = (f" {time_color}{time} {white}|"
                  f" {sumary_color}{summary} {white}|"
                  f" {temperature_color}{temperature} F {white}|"
                  f" {windspeed_color}{windspeed} (Gusting {windgust}) MPH {white}|"
                  f" {precip_color}{precip_probablity}" )

        if newday.search(f'{time}'):
            print(border)

        print(output)

    footer_border = "-"* len(header)
    print(white, end='')
    print(footer_border, end='')
    # print(light_gray)
    print(reset)

def main():
    print_hourly()


if __name__ == "__main__":
    main()


