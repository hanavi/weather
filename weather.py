#!/usr/bin/env python
# coding: utf-8

import requests
import json
import datetime
import re
import configparser
from colorama import Fore, Back, Style
import click

import logging
import structlog
from structlog.stdlib import LoggerFactory
structlog.configure(logger_factory=LoggerFactory())

log = structlog.get_logger()
debug = log.debug
info = log.info
error = log.error


def load_data():

    config_filename = "weather.conf"
    config = configparser.ConfigParser()
    config.read(config_filename)

    latitude = config['default']['latitude']
    longitude = config['default']['longitude']
    api_key = config['default']['api_key']
    url = f"https://api.darksky.net/forecast/{api_key}/{latitude},{longitude}"

    local = config['default']['local']

    if local == "yes":
        debug("Running locally")
        with open("tmp.json") as fd:
            data = fd.read()
        data = json.loads(data)
    else:
        debug("Running over http")
        req = requests.get(url)
        data = json.loads(req.content.decode())

    return data

def print_hourly(data=None):

    header_color = Fore.WHITE

    if data is None:
        data = load_data()

    header = ("  Time               |"
              " Summary                   |"
              " Temp    |"
              " Winds                    |"
              " Precip ")

    header_border = "="* len(header)

    print(header_color, end='')
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

        time_color = Fore.WHITE
        sumary_color = Fore.CYAN
        temperature_color = Fore.GREEN
        windspeed_color = Fore.MAGENTA
        precip_color = Fore.YELLOW

        output = (
            f" {time_color}{time} {header_color}|"
            f" {sumary_color}{summary} {header_color}|"
            f" {temperature_color}{temperature} F {header_color}|"
            f" {windspeed_color}{windspeed} (Gusting {windgust}) MPH {header_color}|"
            f" {precip_color}{precip_probablity}"
        )

        if newday.search(f'{time}'):
            print(border)

        print(output)

    footer_border = "-"* len(header)
    print(header_color, end='')
    print(footer_border, end='')
    # print(light_gray)
    print(Style.RESET_ALL)



@click.command()
@click.option("-d", "--debug", is_flag=True, default=False,
              help="Show debugging info")
def main(debug):

    if (debug is True):
        logging.basicConfig(level=logging.DEBUG)

    print_hourly()


if __name__ == "__main__":
    main()


