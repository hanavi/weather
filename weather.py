#!/usr/bin/env python
# coding: utf-8

import requests
import json
import datetime
import re
import configparser
from colorama import Fore, Back, Style
import click
from time import sleep
import os
import pathlib

import logging
import structlog
from structlog.stdlib import LoggerFactory
structlog.configure(logger_factory=LoggerFactory())

# Easier/Pretty logging
log = structlog.get_logger()
debug = log.debug
info = log.info
error = log.error


def load_data():
    """Load data from file or from the web."""

    # Get the config from file
    config_filename = "weather.conf"
    config = configparser.ConfigParser()
    config.read(config_filename)
    config = config['default']

    if 'local' in config:
        local = config['local']
    else:
        local = "no"

    if local == "yes":

        debug("Running locally")
        with open("tmp.json") as fd:
            data = fd.read()
        data = json.loads(data)

    else:

        debug("Running over http")

        if 'cachefile' in config:

            debug('checking cachefile')
            cachefile = pathlib.Path(config['cachefile'])

            if not cachefile.exists():
                mtime = 0
            else:
                mtime = cachefile.stat().st_mtime

            now = datetime.datetime.now().timestamp()
            last_update = now - mtime
            debug(f"Cache file last updated {last_update:0.0f} s ago")

            # Update the cache file every 10 min
            if last_update > 60*10:
                debug("Cache file is out of date or does not exist... Updating!")

                # TODO: error checking
                latitude = config['latitude']
                longitude = config['longitude']
                api_key = config['api_key']

                url = f'https://api.darksky.net/forecast/{api_key}/{latitude},{longitude}'

                req = requests.get(url)
                data = json.loads(req.content.decode())

                with open(cachefile,'w') as fd:
                    fd.write(json.dumps(data))

            else:
                debug("Using cache file")
                with open(cachefile) as fd:
                    data = fd.read()
                    data = json.loads(data)

    return data

def print_hourly(data=None):
    """Print out the hourly forecast for the next 24 hours."""

    header_color = Fore.WHITE

    if data is None:
        data = load_data()

    header = ("  Time               |"
              " Summary                   |"
              " Temp    |"
              " Winds                    |"
              " Precip ")

    header_border = "="* len(header)
    border = "-"* len(header)
    footer_border = "-"* len(header)

    print(header_color, end='')
    print(header)
    print(header_border)

    # This is so we can find the start of a new day and print a divider
    newday = re.compile("00:00:00")

    i = 0
    for hour in data['hourly']['data']:

        # Only print 24-hours-ish
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

        # Set the colors for the output
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

    print(header_color, end='')
    print(footer_border, end='')
    print(Style.RESET_ALL)


def run_loop():
    """Run every 60 seconds."""

    while True:
        os.system("clear")
        print_hourly()
        sleep(60)


@click.command()
@click.option("-d", "--debug", is_flag=True, default=False,
              help="Show debugging info")
@click.option("-l", "--loop", is_flag=True, default=False,
              help="Run every 60 seconds")
def main(debug, loop):
    """Show weather information."""

    if debug is True:
        logging.basicConfig(level=logging.DEBUG)

    if loop is True:
        run_loop()
    else:
        print_hourly()


if __name__ == "__main__":
    main()


