#
# This file is part of LiteX-Boards.

from litex.build.generic_platform import *
from litex.build.xilinx import Xilinx7SeriesPlatform, VivadoProgrammer
from litex.build.openocd import OpenOCD

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk50", 0, Pins("G22"), IOStandard("LVCMOS33")),
#    ("clk200", 0,
#         Subsignal("p", Pins("AD12"), IOStandard("LVDS")),
#         Subsignal("n", Pins("AD11"), IOStandard("LVDS"))
#     ),
    ("cpu_reset_n", 0, Pins("H26"), IOStandard("LVCMOS33")),

    # Leds
    ("user_led", 0, Pins("A23"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("A24"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("D23"), IOStandard("LVCMOS33")),
    ("user_led", 3, Pins("C24"), IOStandard("LVCMOS33")),
    ("user_led", 4, Pins("C26"), IOStandard("LVCMOS33")),
    ("user_led", 5, Pins("D24"), IOStandard("LVCMOS33")),
    ("user_led", 6, Pins("D25"), IOStandard("LVCMOS33")),
    ("user_led", 7, Pins("E25"), IOStandard("LVCMOS33")),

    # Buttons
    ("user_btn", 0, Pins("D26"), IOStandard("LVCMOS33")),
    ("user_btn", 1, Pins("J26"), IOStandard("LVCMOS33")),
    ("user_btn", 2, Pins("E26"), IOStandard("LVCMOS33")),
    ("user_btn", 3, Pins("G26"), IOStandard("LVCMOS33")),

    # SPIFlash
    ("spiflash4x", 0,
        Subsignal("cs_n", Pins("C23")),
        # Subsignal("clk",  Pins("C8")), # Accessed through STARTUPE2
        Subsignal("dq",   Pins("B24 A25 B22 A22")),
        IOStandard("LVCMOS33")
    ),

#     # Switches
#     ("user_sw", 0, Pins("G19"), IOStandard("LVCMOS12")),
#     ("user_sw", 1, Pins("G25"), IOStandard("LVCMOS12")),
#     ("user_sw", 2, Pins("H24"), IOStandard("LVCMOS12")),
#     ("user_sw", 3, Pins("K19"), IOStandard("LVCMOS12")),
#     ("user_sw", 4, Pins("N19"), IOStandard("LVCMOS12")),
#     ("user_sw", 5, Pins("P19"), IOStandard("LVCMOS12")),
#     ("user_sw", 6, Pins("P26"), IOStandard("LVCMOS33")),
#     ("user_sw", 7, Pins("P27"), IOStandard("LVCMOS33")),

    # Serial
    ("serial", 0,
        Subsignal("tx", Pins("C22")),
        Subsignal("rx", Pins("B20")),
        IOStandard("LVCMOS33")
    ),

#     # USB FIFO
#     ("usb_fifo", 0, # Can be used when FT2232H's Channel A configured to ASYNC FIFO 245 mode
#         Subsignal("data",  Pins("AD27 W27 W28 W29 Y29 Y28 AA28 AA26")),
#         Subsignal("rxf_n", Pins("AB29")),
#         Subsignal("txe_n", Pins("AA25")),
#         Subsignal("rd_n",  Pins("AB25")),
#         Subsignal("wr_n",  Pins("AC27")),
#         Subsignal("siwua", Pins("AB28")),
#         Subsignal("oe_n",  Pins("AC30")),
#         Misc("SLEW=FAST"),
#         Drive(8),
#         IOStandard("LVCMOS33"),
#     ),

    # SDCard
    ("spisdcard", 0,
        Subsignal("clk",  Pins("G24")),
        Subsignal("cs_n", Pins("F24"), Misc("PULLUP True")),
        Subsignal("mosi", Pins("G25"), Misc("PULLUP True")),
        Subsignal("miso", Pins("F23"), Misc("PULLUP True")),
        Misc("SLEW=FAST"),
        IOStandard("LVCMOS33")
    ),
    ("sdcard", 0,
        Subsignal("clk",  Pins("G24")),
        Subsignal("cmd",  Pins("G25"),             Misc("PULLUP True")),
        Subsignal("data", Pins("F23 E23 F25 F24"), Misc("PULLUP True")),
        Misc("SLEW=FAST"),
        IOStandard("LVCMOS33")
    ),

    # DDR3 SDRAM
    ("ddram", 0,
        Subsignal("a", Pins(
            "AF8 AB10 V9  Y7   AC9 W8 Y11 V8",
            "AA8 AC11 AD9 AA10 AF9 V7 Y8"),
            IOStandard("SSTL15")),
        Subsignal("ba",    Pins("AA7 AB11 AF7"), IOStandard("SSTL15")),
        Subsignal("ras_n", Pins("AD8"), IOStandard("SSTL15")),
        Subsignal("cas_n", Pins("W10"), IOStandard("SSTL15")),
        Subsignal("we_n",  Pins("W9"),  IOStandard("SSTL15")),
        Subsignal("cs_n",  Pins("AB7"), IOStandard("SSTL15")),
        Subsignal("dm", Pins("AF15 AA15 AB19 V14"),
            IOStandard("SSTL15")),
        Subsignal("dq", Pins(
            "AF14 AF17 AE15 AE17 AD16 AF20 AD15 AF19",
            "AB15 AC14 AA18 AA14 AB16 AB14 AA17 AD14",
            "AD19 AC19 AD18 AA19 AC17 AA20 AC18 AB17",
            "Y17  V16  V17  W14  V18  W15  V19  W16"),
            IOStandard("SSTL15_T_DCI")),
        Subsignal("dqs_p", Pins("AE18 Y15 AD20 W18"),
            IOStandard("DIFF_SSTL15")),
        Subsignal("dqs_n", Pins("AF18 Y16 AE20 W19"),
            IOStandard("DIFF_SSTL15")),
        Subsignal("clk_p", Pins("AA9"),  IOStandard("DIFF_SSTL15")),
        Subsignal("clk_n", Pins("AB9"),  IOStandard("DIFF_SSTL15")),
        Subsignal("cke",   Pins("AF10"), IOStandard("SSTL15")),
        Subsignal("odt",   Pins("AC8"),  IOStandard("SSTL15")),
        Subsignal("reset_n", Pins("Y10"), IOStandard("LVCMOS15")),
        Misc("SLEW=FAST"),
        Misc("VCCAUX_IO=HIGH")
    ),

    # RGMII Ethernet (RTL8211FD)
    ("eth_clocks", 0,
        Subsignal("tx", Pins("AC2")),
        Subsignal("rx", Pins("AB2")),
        IOStandard("LVCMOS18")
    ),
    ("eth", 0,
        Subsignal("rst_n",   Pins("Y2")),
        Subsignal("mdio",    Pins("AF5")),
        Subsignal("mdc",     Pins("W1")),
        Subsignal("rx_ctl",  Pins("AF4")),
        Subsignal("rx_data", Pins("AF3 AC3 AE2 AE1")),
        Subsignal("tx_ctl",  Pins("Y1")),
        Subsignal("tx_data", Pins("AC1 AB1 AB4 Y3")),
        IOStandard("LVCMOS18"),
    ),

    # HDMI In
    ("hdmi_in", 0,
        Subsignal("clk_p",   Pins("F17"), IOStandard("TMDS_33")),
        Subsignal("clk_n",   Pins("E17"), IOStandard("TMDS_33")),
        Subsignal("data0_p", Pins("J15"), IOStandard("TMDS_33")),
        Subsignal("data0_n", Pins("J16"), IOStandard("TMDS_33")),
        Subsignal("data1_p", Pins("E15"), IOStandard("TMDS_33")),
        Subsignal("data1_n", Pins("E16"), IOStandard("TMDS_33")),
        Subsignal("data2_p", Pins("G17"), IOStandard("TMDS_33")),
        Subsignal("data2_n", Pins("F18"), IOStandard("TMDS_33")),
        Subsignal("scl",     Pins("H19"), IOStandard("LVCMOS33")),
        Subsignal("sda",     Pins("F19"), IOStandard("LVCMOS33")),
    ),

    # HDMI Out
    ("hdmi_out", 0,
        Subsignal("clk_p",   Pins("E18"), IOStandard("TMDS_33")),
        Subsignal("clk_n",   Pins("D18"), IOStandard("TMDS_33")),
        Subsignal("data0_p", Pins("D19"), IOStandard("TMDS_33")),
        Subsignal("data0_n", Pins("D20"), IOStandard("TMDS_33")),
        Subsignal("data1_p", Pins("H17"), IOStandard("TMDS_33")),
        Subsignal("data1_n", Pins("H18"), IOStandard("TMDS_33")),
        Subsignal("data2_p", Pins("G19"), IOStandard("TMDS_33")),
        Subsignal("data2_n", Pins("F20"), IOStandard("TMDS_33")),
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
]

# Platform -----------------------------------------------------------------------------------------

class Platform(Xilinx7SeriesPlatform):
    default_clk_name   = "clk50"
    default_clk_period = 1e9/50e6

    def __init__(self, toolchain="vivado"):
        Xilinx7SeriesPlatform.__init__(self, "xc7k325t-ffg676-2", _io, _connectors, toolchain=toolchain)
        self.toolchain.bitstream_commands = [
            "set_property BITSTREAM.GENERAL.COMPRESS True [current_design]",
            "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]",
            "set_property BITSTREAM.CONFIG.CONFIGRATE 50 [current_design]",
        ]
        self.toolchain.additional_commands = [
            "write_cfgmem -force -format bin -interface spix4 -size 16 -loadbit \"up 0x0 \
            {build_name}.bit\" -file {build_name}.bin"
        ]

    def create_programmer(self):
        return OpenOCD("openocd_xc7_ft232.cfg", "bscan_spi_xc7a325t.bit")

    def create_programmer_vivado(self):
        return VivadoProgrammer(flash_part="mx25l25645g-spi-x1_x2_x4")

    def do_finalize(self, fragment):
        Xilinx7SeriesPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk50", loose=True), 1e9/50e6)
        self.add_platform_command("set_property DCI_CASCADE {{32}} [get_iobanks 33]")
