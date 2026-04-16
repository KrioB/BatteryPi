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

try:
  pijuice = PiJuice(1, 0x14)
except Exception as err:
  sys.exit(1)

try:
  pijuice.status.SetLedState('D2', [0 ,0, 0])
except Exception as err:
  pass

if len(sys.argv) > 1 and sys.argv[1] == "poweroff":
  try:
    pijuice.status.SetLedBlink('D2', 10, [255, 0, 0], 100, [0, 0, 0], 400)
    pijuice.power.SetPowerOff(30)
  except Exception as err:
    pass
