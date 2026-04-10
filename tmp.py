from pijuice import PiJuice
pijuice = PiJuice(1, 0x14)

#  self.interface = PiJuiceInterface(bus, address)
#  self.status = PiJuiceStatus(self.interface)
#  self.config = PiJuiceConfig(self.interface)
#  self.power = PiJuicePower(self.interface)
#  self.rtcAlarm = PiJuiceRtcAlarm(self.interface)

pijuice.status.GetStatus()
{'data': {'isFault': True, 'isButton': False, 'battery': 'NORMAL', 'powerInput': 'NOT_PRESENT', 'powerInput5vIo': 'PRESENT'}, 'error': 'NO_ERROR'}

pijuice.status.GetChargeLevel()
{'data': 97, 'error': 'NO_ERROR'}

pijuice.status.GetFaultStatus()
{'data': {'forced_power_off': True, 'forced_sys_power_off': True}, 'error': 'NO_ERROR'}

pijuice.status.ResetFaultFlags(flags)
#

pijuice.status.GetButtonEvents()
{'data': {'SW1': 'NO_EVENT', 'SW2': 'NO_EVENT', 'SW3': 'NO_EVENT'}, 'error': 'NO_ERROR'}

pijuice.status.AcceptButtonEvent(button)
#

pijuice.status.GetBatteryTemperature()
{'data': 24, 'error': 'NO_ERROR'}

pijuice.status.GetBatteryVoltage()
{'data': 4135, 'error': 'NO_ERROR'}

pijuice.status.GetBatteryCurrent()
{'data': 14, 'error': 'NO_ERROR'}

pijuice.status.GetIoVoltage()
{'data': 5126, 'error': 'NO_ERROR'}

pijuice.status.GetIoCurrent()
{'data': -466, 'error': 'NO_ERROR'}

pijuice.status.SetLedState('D2', [0 ,0, 100])
{'error': 'NO_ERROR'}

pijuice.status.GetLedState('D2')
{'data': [0, 0, 100], 'error': 'NO_ERROR'}

pijuice.status.SetLedBlink('D2', 2, [255, 0, 0], 500, [0, 0, 100], 2000)
{'error': 'NO_ERROR'}

pijuice.status.GetLedBlink('D2')
{'data': {'count': 0, 'rgb1': [0, 0, 0], 'period1': 0, 'rgb2': [0, 0, 0], 'period2': 0}, 'error': 'NO_ERROR'}

pijuice.power.GetWakeUpOnCharge()
{'data': 'DISABLED', 'non_volatile': False, 'error': 'NO_ERROR'}

pijuice.power.GetPowerOff()
{'data': [255], 'error': 'NO_ERROR'}

pijuice.power.SetPowerOff(120)
{'error': 'NO_ERROR'}



#!/usr/bin/python3

import subprocess
import time
from pijuice import PiJuice

pijuice = PiJuice(1, 0x14)

pijuice.status.SetLedState('D2', [0 ,150, 0])
time.sleep(1)
pijuice.status.SetLedBlink('D2', 0, [0, 0, 0], 0, [0, 0, 0], 0)


while True:

  battery_level =  pijuice.status.GetChargeLevel()['data']
  stat_battery = pijuice.status.GetStatus()['data']['battery']
  stat_power_usb = pijuice.status.GetStatus()['data']['powerInput']
  stat_power_5v = pijuice.status.GetStatus()['data']['powerInput5vIo']

  print(stat_battery, '\t', battery_level, '%')

  if stat_power_usb != 'PRESENT' and stat_power_5v != 'PRESENT':
    print('no power supply')
    pijuice.status.SetLedState('D2', [0 ,0, 0])
    time.sleep(1)
    pijuice.status.SetLedBlink('D2', 255, [255, 0, 0], 500, [0, 0, 0], 1000)
    pijuice.power.SetPowerOff(240)
    subprocess.call(["sudo", "shutdown", "-P", "+1"])
    break

  time.sleep(10)
