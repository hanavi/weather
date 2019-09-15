#!/usr/bin/env python

"""Script Description

Filename: taf.py
Author: James Casey
Date Created: 2019-09-06
Last Updated: 2019-09-06
"""

import click
import logging
import structlog
from structlog.stdlib import LoggerFactory
import requests

structlog.configure(logger_factory=LoggerFactory())
log = structlog.get_logger()

debug = log.debug
info = log.info
warning = log.warning
error = log.error

def get_taf(airport):

    base_url="https://tgftp.nws.noaa.gov/data/forecasts/taf/stations/"

    airport_url = base_url + airport.upper() + ".TXT"

    data = requests.get(airport_url).content.decode()

    print()
    print(data)
    print()


@click.command()
@click.option("-v", "--verbose", is_flag=True, default=False,
              help="Show debuggging information")
@click.argument("airport")
def main(verbose, airport):

    if verbose is True:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    get_taf(airport)

if __name__ == "__main__":
    main()


