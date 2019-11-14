# Changelog
All notable changes to this core library will be documented in this file.


## 2019-02-8: ChibiOS upgrade to 19.1.0
Please refer to `chibios/release_note_19.1.0.txt` for details, basically no changes is required for running code, but some more features of the stm32f4 chip is supported.
Your `halconf.h` should now define `_CHIBIOS_HAL_CONF_VER_7_0_` and `chconf.h` should define `_CHIBIOS_RT_CONF_VER_6_0_` instead of their previous versions.
