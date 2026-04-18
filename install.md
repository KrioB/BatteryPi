# Dependencies

- `python3`
- `python3-systemd` - systemd and journal
- `python3-smbus` - I2C

# Hardware configuration
`sudo raspi-config nonint do_i2c 0` - enable I2C buss

# Directory structure
Create `system-shutdown` directory if not existing

```sh
cd /usr/lib/systemd
ls | grep system-shutdown
sudo mkdir system-shutdown
sudo chown root:root system-shutdown
sudo chmod 644 system-shutdown
```

| file                  | chmod |   chown   | patch                                    |
| :-------------------- | :---: | :-------: | :--------------------------------------- |
| pijuice.py            |  644  | root:root | /usr/local/lib/python3.13/dist-packages/ |
| batterypi-shutdown.py |  755  | root:root | /usr/lib/systemd/system-shutdown/        |
| batterypid.py         |  755  | root:root | /usr/local/bin/                          |
| batterypid.service    |  644  | root:root | /etc/systemd/system/                     |