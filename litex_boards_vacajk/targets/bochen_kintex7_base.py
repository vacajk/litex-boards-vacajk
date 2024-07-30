#!/usr/bin/env python3

#
# This file is part of LiteX-Boards.

from migen import *

from litex.gen import *

from litex_boards_vacajk.platforms import bochen_kintex7_base

from litex.soc.cores.clock import *
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores.led import LedChaser

from litedram.modules import MT41K256M16
from litedram.phy import s7ddrphy

from liteeth.phy.s7rgmii import LiteEthPHYRGMII

ident_default = "LiteX SoC on Bochen Kintex7 Base"

# CRG ----------------------------------------------------------------------------------------------

class _CRG(LiteXModule):
    def __init__(self, platform, sys_clk_freq,
        with_sdram = False
        ):

        self.rst       = Signal()
        self.cd_sys    = ClockDomain()
        if with_sdram:
            self.cd_sys4x  = ClockDomain()
            self.cd_idelay = ClockDomain()

        # # #

        # Clk/Rst.
        clk50 = platform.request("clk50")

        # PLL.
        self.pll = pll = S7MMCM(speedgrade=-2)
        pll.reset.eq(self.rst)
        pll.register_clkin(clk50, 50e6)
        pll.create_clkout(self.cd_sys,    sys_clk_freq)
        if with_sdram:
            pll.create_clkout(self.cd_sys4x,  4*sys_clk_freq)
            pll.create_clkout(self.cd_idelay, 200e6)
        platform.add_false_path_constraints(self.cd_sys.clk, pll.clkin) # Ignore sys_clk to pll.clkin path created by SoC's rst.

        # IDelayCtrl.
        if with_sdram:
            self.idelayctrl = S7IDELAYCTRL(self.cd_idelay)

# BaseSoC ------------------------------------------------------------------------------------------

class BaseSoC(SoCCore):
    def __init__(self, sys_clk_freq=100e6,
        with_ethernet   = False,
        with_etherbone  = False,
        with_led_chaser = True,
        with_sdram      = False,
        ident           = ident_default,
        **kwargs):
        platform = bochen_kintex7_base.Platform()

        # CRG --------------------------------------------------------------------------------------
        self.crg = _CRG(platform, sys_clk_freq,
                        with_sdram=with_sdram,
                        )

        # SoCCore ----------------------------------------------------------------------------------
        SoCCore.__init__(self, platform, sys_clk_freq, ident=ident, **kwargs)

        # DDR3 SDRAM -------------------------------------------------------------------------------
        if with_sdram and not self.integrated_main_ram_size:
            self.ddrphy = s7ddrphy.K7DDRPHY(platform.request("ddram"),
                memtype      = "DDR3",
                nphases      = 4,
                sys_clk_freq = sys_clk_freq)
            self.add_sdram("sdram",
                phy           = self.ddrphy,
                module        = MT41K256M16(sys_clk_freq, "1:4"),
                l2_cache_size = kwargs.get("l2_size", 8192),
            )

        # Ethernet / Etherbone ---------------------------------------------------------------------
        # if with_ethernet or with_etherbone:
        #     self.ethphy = LiteEthPHYRGMII(
        #         clock_pads = self.platform.request("eth_clocks"),
        #         pads       = self.platform.request("eth"))
        #     if with_ethernet:
        #         self.add_ethernet(phy=self.ethphy)
        #     if with_etherbone:
        #         self.add_etherbone(phy=self.ethphy)

        # Leds -------------------------------------------------------------------------------------
        if with_led_chaser:
            self.leds = LedChaser(
                pads         = platform.request_all("user_led"),
                sys_clk_freq = sys_clk_freq)

# Build --------------------------------------------------------------------------------------------

def main():
    from litex.build.parser import LiteXArgumentParser
    parser = LiteXArgumentParser(platform=bochen_kintex7_base.Platform, description=ident_default)
    parser.add_target_argument("--sys-clk-freq",                            default=100e6,  type=float,     help="System clock frequency.")
    parser.add_target_argument("--with-spi-flash",  action="store_true",                                    help="Enable SPI Flash (MMAPed).")
    parser.add_target_argument("--with-sdram",      action="store_true",    default=True,                   help="Enable optional SDRAM module.")
    # ethopts = parser.target_group.add_mutually_exclusive_group()
    # ethopts.add_argument("--with-ethernet",  action="store_true", help="Enable Ethernet support.")
    # ethopts.add_argument("--with-etherbone", action="store_true", help="Enable Etherbone support.")
    # sdopts = parser.target_group.add_mutually_exclusive_group()
    # sdopts.add_argument("--with-spi-sdcard", action="store_true", help="Enable SPI-mode SDCard support.")
    # sdopts.add_argument("--with-sdcard",     action="store_true", help="Enable SDCard support.")
    args = parser.parse_args()

    soc = BaseSoC(
        sys_clk_freq    = args.sys_clk_freq,
        with_spi_flash  = args.with_spi_flash,
        with_sdram      = args.with_sdram,
        # with_ethernet  = args.with_ethernet,
        # with_etherbone = args.with_etherbone,
        **parser.soc_argdict
    )

    # if args.with_spi_sdcard:
    #     soc.add_spi_sdcard()
    # if args.with_sdcard:
    #     soc.add_sdcard()

    builder = Builder(soc, **parser.builder_argdict)

    if args.build:
        builder.build(**parser.toolchain_argdict)

    if args.load:
        prog = soc.platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"))

if __name__ == "__main__":
    main()
