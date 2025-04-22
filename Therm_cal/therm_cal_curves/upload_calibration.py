#!/usr/bin/env python3
# Brian Koopman

# Downloaded from Github by Zach Huber on 5/3/2023

import argparse
import time
import datetime

# LS240
from socs.Lakeshore.Lakeshore240 import Channel
from socs.Lakeshore.Lakeshore240 import Module as LS240

# LS372
from socs.Lakeshore.Lakeshore372 import Curve
from socs.Lakeshore.Lakeshore372 import LS372

PARSER = argparse.ArgumentParser(description='Upload a .340 format calibration curve ' \
                                             'to a Lakeshore 240 or 372.')
PARSER.add_argument('model', type=int, choices=[240, 372],
                    help='Model number of Lakeshore device (either 240 or 372)')
PARSER.add_argument('address', type=str, help='Address or TTY for the Lakeshore, ' \
                                              'i.e. 10.10.10.4, /dev/LSA24R5')
PARSER.add_argument('channel', type=int, help='The channel (or curve slot) to upload the curve to')
PARSER.add_argument('file', type=str, help='The calibration file to upload')

ARGS = PARSER.parse_args()

assert ARGS.model in [240, 372], "{} is not a supported Lakeshore model".format(ARGS.model)

if ARGS.model == 240:
    LAKESHORE = LS240(port=ARGS.address)
    CHANNEL = Channel(LAKESHORE, ARGS.channel)
    print('Start:', datetime.datetime.utcfromtimestamp(time.time()))
    CHANNEL.load_curve(ARGS.file)
    print('End:', datetime.datetime.utcfromtimestamp(time.time()))

elif ARGS.model == 372:
    LAKESHORE = LS372(ip=ARGS.address)
    CURVE = Curve(LAKESHORE, ARGS.channel)
    print('Start:', datetime.datetime.utcfromtimestamp(time.time()))
    print(CURVE.set_curve(ARGS.file))
    print('End:', datetime.datetime.utcfromtimestamp(time.time()))

else:
    raise RuntimeError("I don't know how we got here...")
