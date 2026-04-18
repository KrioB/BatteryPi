#!/usr/bin/python3

# -------------------------------------------
# batterypi-shutdown.py
# Copyright (c) 2026 KrioB
#
# Part of Battery Pi https://github.com/KrioB/BatteryPi
# ver 1.0
#
# Script runs before the actual power-off, halt, reboot, or kexec action.
# If receive as argument <poweroff>, it will set delayd power cut-off to battery MCU.
# -------------------------------------------

import sys
from pijuice import PiJuice

# Set up I2C and PiJuice communication
try:
  pijuice = PiJuice(1, 0x14)
except Exception as err:
  sys.exit(1)

# Clear LED
try:
  pijuice.status.SetLedState('D2', [0 ,0, 0])
except Exception as err:
  pass

# Check if <shutdown -P> was performed
if len(sys.argv) > 1 and sys.argv[1] == "poweroff":
  try:
    # Blink RED
    pijuice.status.SetLedBlink('D2', 10, [255, 0, 0], 100, [0, 0, 0], 400)

    # Schedule power cut off
    # Shutdown process will wait up to 90s before continue
    pijuice.power.SetPowerOff(100)

  except Exception as err:
    pass
