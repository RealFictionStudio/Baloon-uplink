# ICM20602

![PyPI](https://img.shields.io/pypi/v/icm20602.svg)
![License](https://img.shields.io/github/license/kagankongar/ICM20602.svg)
![PyPi Downloads](https://img.shields.io/pypi/dw/icm20602)


#### Python library for the icm-20602 and mpu-6500 IMU comm via spi, suitable for Raspberry Pi

Capable of reading acceleration and gyroscope values, 
threaded use, calibration, DLPF, smoothing and inclination 
calculation.

Since ICM-20602 is the successor of MPU-6500, they are register 
address compatible. This library can be used for both. Be sure to 
connect the wires correct.

Both IMUs were tested on RaspBerry Pi 5, 2GB, Linux RPLite 6.6.62+rpt-rpi-2712 


### Installation
pip install icm20602


### Dependencies
spidev


### Usage

Please check examples/ directory for usage


### ToDo

- Better documentation
- FIFO Support


### License

Copyright (c) 2025 kagankongar  (kagan.kongar@gmail.com). 
Available under the **MIT License**. For more information, 
see [LICENSE](LICENSE).
