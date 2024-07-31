
                                  __   _ __      _  __    ___                   __
                                 / /  (_) /____ | |/_/___/ _ )___  ___ ________/ /__
                                / /__/ / __/ -_)>  </___/ _  / _ \/ _ `/ __/ _  (_-<
                               /____/_/\__/\__/_/|_|   /____/\___/\_,_/_/  \_,_/___/

                                              LiteX boards files

                                     Copyright 2012-2023 / LiteX-Hub community

[![](https://github.com/litex-hub/litex-boards/workflows/ci/badge.svg)](https://github.com/litex-hub/litex-boards/actions) ![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)

[> Intro
--------
<figure>
<p align="center">
<img src="https://user-images.githubusercontent.com/1450143/88511626-73792100-cfe5-11ea-8d3e-dbeea6314e15.JPG">
</p>
<figcaption>
<p align="center">
From the very tiny Fomu to large PCIe accelerator boards....
</p>
</figcaption>
</figure>

This repository contains the platforms/targets currently supported by LiteX:

- The platform provides the definition of the board: IOs, constraints, clocks, components + methods to load and flash the bitstream to it.
- The target provides a LiteX base design for the board that allows you to create a SoC (with or without a CPU) and integrate easily all the base components of your board: Ethernet, DRAM, PCIe, SPIFlash, SDCard, Leds, GPIOs, etc...

The targets can be used as a base to build more complex or custom SoCs. They are are for example directly reused by the [Linux-on-LiteX-VexRiscv](https://github.com/litex-hub/linux-on-litex-vexriscv) project that is just using a specific configuration (Linux-capable CPU, additional peripherals). Basing your design on provided targets allows to to reduce code duplication between very various projects.

First make sure to install LiteX correctly by following the [installation guide](https://github.com/enjoy-digital/litex/wiki/Installation) and have a look at the [LiteX's wiki](https://github.com/enjoy-digital/litex/wiki) for [tutorials](https://github.com/enjoy-digital/litex/wiki/Tutorials-Resources),  [examples of projects](https://github.com/enjoy-digital/litex/wiki/Projects) and more information to use/build FPGA designs with it.

Each target provides a default configuration with a CPU, ROM, SRAM, UART, DRAM (if available), Ethernet (if available), etc... that can be simply built and loaded to the FPGA with:

    $ python3 -m litex_boards.targets.<board> --build --load

You can then open a terminal on the main UART of the board and interact with the LiteX BIOS:

<p align="center"><img src="https://raw.githubusercontent.com/enjoy-digital/litex/master/doc/bios_screenshot.png"></p>

**Build/Compilation behavior:**
- python3 -m litex_boards.targets.board : Test LiteX/Migen syntax but does not generate anything.
- Add `--build` to generate the SoC/Software headers and run the Software/Gateware compilation.
- Add `--no-compile` to disable the Softwate/Gateware compilation.
- Add `--no-compile-software` to disable the Software compilation.
- Add `--no-compile-gateware` to disable the Gateware compilation.

But this is just the starting point to create your own hardware! You can then:

- Change the CPU: add `--cpu-type=lm32, microwatt, serv, rocket, etc... `
- Change the Bus standard: add `--bus-standard=wishbone, axi-lite`
- Enable components: add `--with-ethernet --with-etherbone --with-sdcard etc...`
- [Load application code to the CPU](https://github.com/enjoy-digital/litex/wiki/Load-Application-Code-To-CPU) over UART/Ethernet/SDCard, etc...
- Create a bridge with your computer to easily [access the main bus of your SoC](https://github.com/enjoy-digital/litex/wiki/Use-Host-Bridge-to-control-debug-a-SoC).
- Add a Logic Analyzer to your SoC to easily [observe/debug your design](https://github.com/enjoy-digital/litex/wiki/Use-LiteScope-To-Debug-A-SoC).
- Simulate your SoC and interact with it at decent speed with [LiteX Sim](https://github.com/enjoy-digital/litex/blob/master/litex/tools/litex_sim.py)/Verilator.
- Integrate external cores/CPU to create your own design.
- etc...

Please use `python3 -m litex_boards.targets.<board> --help` to see the pre-built various possibilities.

Hoping you will find this useful and enjoy it, please contribute back if you make improvements that could be useful to others or find issues!

**A question or want to get in touch? Our IRC channel is [#litex at irc.libera.chat](https://web.libera.chat/#litex)**


[> Supported boards
-------------------

LiteX-Boards currently supports > 150 boards from very various FPGA Vendors (Xilinx, Intel, Lattice, Efinix, Gowin, etc...)!
Some of these boards are fully open-hardware boards (Fomu, NeTV2, OrangeCrab, Butterstick, etc...) with FPGAs often supported by the open-source toolchains, some of them are repurposed off-the-shelf hardware (Colorlight 5A/I5/I9, SQRL Acorn CLE 215+, FK33, Siglent SDS1104X-E, Decklink Mini 4k, etc...) and we also of course support popular/regular FPGA dev boards :)


Most of the peripherals present are generally supported: DRAM, UART, Ethernet, SPI-Flash, SDCard, PCIe, SATA, etc... making LiteX-Boards' targets hopefully a good base infrastructure to create your own custom SoCs!

> **Note:** All boards with >= 32MB of memory and enough logic can be considered as Linux Capable, have a look at [LiteX-on-LiteX-Vexriscv](https://github.com/litex-hub/linux-on-litex-vexriscv) project to try Linux on your FPGA board!


<figure>
<p align="center">
<img src="https://user-images.githubusercontent.com/1450143/156173620-355c6f1d-87dc-4dda-be45-910bf379ae9a.jpg">
</p>
<figcaption>
<p align="center">
Some of the suported boards, see yours? Give LiteX-Boards a try!
</p>
</figcaption>
</figure>

[> Boards list
---------------
    └── bochen_kintex7_base
