#!/usr/bin/python3

# -------------------------------------------
# batterypid.py
# Copyright (c) 2026 KrioB
#
# Part of Battery Pi https://github.com/KrioB/BatteryPi
# ver 1.0
#
# Main service script monitrs power supply and battery level
# -------------------------------------------

import logging
from systemd.journal import JournalHandler
import sys
import time
import subprocess
from pijuice import PiJuice

# Configure logger
log = logging.getLogger(__name__)
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

pijuice = PiJuice(1, 0x14)

shutdown_state = False

while True:


  battery_level =  pijuice.status.GetChargeLevel()['data']
  stat_battery = pijuice.status.GetStatus()['data']['battery']
  stat_power_usb = pijuice.status.GetStatus()['data']['powerInput']
  stat_power_5v = pijuice.status.GetStatus()['data']['powerInput5vIo']

  if stat_power_usb != 'PRESENT' and stat_power_5v != 'PRESENT':
    if not shutdown_state:
      shutdown_state = True
      subprocess.call(['sudo', 'shutdown', '-P', '+5'])
      log.warning('Power source not present.')

    pijuice.status.SetLedBlink('D2', 2, [200, 0, 0], 500, [0, 0, 0], 500)

  else:
    if shutdown_state:
      shutdown_state = False
      subprocess.call(['sudo', 'shutdown', '-c'])
      log.info('Power source present.')

    pijuice.status.SetLedBlink('D2', 2, [0, 200, 0], 500, [0, 0, 0], 500)

  time.sleep(10)
