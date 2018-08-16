DCFurs Badge Firmware
=====================

This directory contains the firmware sources used by the 2018 DCFurs badge.
The bluetooth firmware and BLE beacons are built from the
[Zephyr Project](https://github.com/zephyrproject-rtos) and the STM32F4
is running [Micropython](https://micropython.org/).

Both of these projects required some modifications to their codebase, the
modified versions have been included as git submodules. Use the command
`git submodule update --init` to checkout the correct versions, or clone them
yourself from:
  * https://github.com/oskirby/zephyr.git
  * https://github.com/oskirby/micropython-dcfurs.git

Building Micropython
--------------------
Prior to building the Micropython firmware, we must first generate a tarball
containing the initial filesystem. Use the script at `tools/dcfurs-mktar.sh`
to generate this file.

After cloning the Micropython firmware, change directory into `ports/stm32`
and run the command `make BOARD=DCFURS_F411 FLASH_TARBALL_FILE=<path to dc26-fur-scripts.tar.gz>`

Preparing Zephyr
----------------
Please read through the Zephyr [Getting Started Guide](http://docs.zephyrproject.org/getting_started/getting_started.html)
in order to properly check out and set up the build environment. Since the board support for the
Taiyo Yuden EYSGCNZWY module and nRF58122 Beacon are not available in the SDK, we will be following
the instructions on building without the Zephyr SDK. This may also require the installation of the
[GNU ARM Embedded](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm) toolchain.

Building the Bluetooth Firwmare
-------------------------------
Change directory into the `firmware/bluetooth` directory, and run the following commands
to build the firmware:

```
    source <path to zephyr>/zephyr-env.sh
    export ZEPHYR_TOOLCHAIN_VARIANT=gccarmemb
    mkdir build && cd build
    cmake -GNinja -DBOARD=nrf51_eysgcnzwy ..
    ninja
```

Building the BLE Beacon Firmware
--------------------------------
Change directory into the `firmware/beacon` directory, and run the following commands
to build the firmware:

```
    source <path to zephyr>/zephyr-env.sh
    export ZEPHYR_TOOLCHAIN_VARIANT=gccarmemb
    mkdir build && cd build
    cmake -GNinja -DBOARD=nrf51_beacon ..
    ninja
```
