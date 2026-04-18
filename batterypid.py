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

# Set up logger
log = logging.getLogger(__name__)
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

# Set up I2C and PiJuice communication
pijuice = PiJuice(1, 0x14)

# Set default daemon state
shutdown_state = False

# Main deamon loop
while True:

  # Pull status from PiJuice
  battery_level =  pijuice.status.GetChargeLevel()['data']
  stat_battery = pijuice.status.GetStatus()['data']['battery']
  stat_power_usb = pijuice.status.GetStatus()['data']['powerInput']
  stat_power_5v = pijuice.status.GetStatus()['data']['powerInput5vIo']

  # Check power supply status
  if stat_power_usb != 'PRESENT' and stat_power_5v != 'PRESENT':
    if not shutdown_state:

      # External power source was unplugged

      log.warning('External power source not present.')
      shutdown_state = True

      # Schedule shutdown
      subprocess.call(['sudo', 'shutdown', '-P', '+5'])

    # Shutdown sheduled, blink RED
    pijuice.status.SetLedBlink('D2', 2, [200, 0, 0], 500, [0, 0, 0], 500)

  else:
    if shutdown_state:

      # External power source was plugged

      log.info('Power source present.')
      shutdown_state = False

      # Cancel shutdown sheduled by this daemon
      subprocess.call(['sudo', 'shutdown', '-c'])

    # Power OK, blink GREEN
    pijuice.status.SetLedBlink('D2', 2, [0, 200, 0], 500, [0, 0, 0], 500)

  # Sleep
  time.sleep(10)
