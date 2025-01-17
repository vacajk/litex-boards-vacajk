#!/usr/bin/env python3

#
# This file is part of LiteX-Boards.

from migen import *

from litex.gen import *

from litex_boards_vacajk.platforms import bochen_kintex7_base

from litex.soc.cores.clock import *
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores.video import VideoS7HDMIPHY
from litex.soc.cores.led import LedChaser

from litedram.modules import MT41K256M16
from litedram.phy import s7ddrphy

from liteeth.phy.s7rgmii import LiteEthPHYRGMII

ident_default = "LiteX SoC on Bochen Kintex7 Base"

# CRG ----------------------------------------------------------------------------------------------

class _CRG(LiteXModule):
    def __init__(self, platform, sys_clk_freq,
        with_sdram      = False,
        with_ethernet   = False,
        with_hdmi       = False,
        ):

        clk_with_idelay = with_sdram or with_ethernet

        self.rst       = Signal()
        self.cd_sys    = ClockDomain()

        # # #

        # Clk/Rst.
        clk50 = platform.request("clk50")
        rst_n = platform.request("cpu_reset_n")

        # PLL.
        self.pll = pll = S7MMCM(speedgrade=-2)
        self.comb += pll.reset.eq(~rst_n | self.rst)
        pll.register_clkin(clk50, 50e6)
        pll.create_clkout(self.cd_sys,    sys_clk_freq)

        # IDelayCtrl.
        if clk_with_idelay:
            self.cd_idelay = ClockDomain()
            pll.create_clkout(self.cd_idelay, 200e6)
            self.idelayctrl = S7IDELAYCTRL(self.cd_idelay)

        if with_sdram:
            self.cd_sys4x  = ClockDomain()
            pll.create_clkout(self.cd_sys4x,  4*sys_clk_freq)

        if with_hdmi:
            self.cd_hdmi   = ClockDomain()
            self.cd_hdmi5x = ClockDomain()
            self.video_pll = video_pll = S7MMCM(speedgrade=-2)
            video_pll.register_clkin(clk50, 50e6)
            video_pll.create_clkout(self.cd_hdmi,   25e6,  margin=0)
            video_pll.create_clkout(self.cd_hdmi5x, 125e6, margin=0)

        platform.add_false_path_constraints(self.cd_sys.clk, pll.clkin) # Ignore sys_clk to pll.clkin path created by SoC's rst.

# BaseSoC ------------------------------------------------------------------------------------------

class BaseSoC(SoCCore):
    def __init__(self,
        sys_clk_freq        = 100e6,
        with_led_chaser     = True,

        with_sdram          = False,
        with_spi_flash      = False,
        with_spi_sdcard     = False,
        with_sdcard         = False,

        with_ethernet       = False,
        with_etherbone      = False,
        eth_phy             = 0,
        eth_ip              = "192.168.1.50",
        eth_remote_ip       = None,
        eth_software_debug  = False,
        eth_dynamic_ip      = False,

        with_video_terminal     = False,
        with_video_framebuffer  = False,
        with_video_colorbars    = False,

        ident           = ident_default,
        **kwargs):
        platform = bochen_kintex7_base.Platform()

        # CRG --------------------------------------------------------------------------------------
        self.crg = _CRG(platform, sys_clk_freq,
                        with_sdram      = with_sdram,
                        with_ethernet   = with_ethernet or with_etherbone,
                        with_hdmi       = with_video_terminal or with_video_framebuffer or with_video_colorbars
                        )

        # SoCCore ----------------------------------------------------------------------------------
        SoCCore.__init__(self, platform, sys_clk_freq, ident=ident, **kwargs)

        # Leds -------------------------------------------------------------------------------------
        if with_led_chaser:
            self.leds = LedChaser(
                pads         = platform.request_all("user_led"),
                sys_clk_freq = sys_clk_freq)

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

        # SPI Flash --------------------------------------------------------------------------------
        if with_spi_flash:
            from litespi.modules import MX25L25645G
            from litespi.opcodes import SpiNorFlashOpCodes as Codes
            self.add_spi_flash(mode="4x", module=MX25L25645G(Codes.READ_1_1_1), with_master=True)

        # SD Card --------------------------------------------------------------------------------
        if with_spi_sdcard:
            self.add_spi_sdcard()
        if with_sdcard:
            self.add_sdcard()

        # HDMI Options -----------------------------------------------------------------------------
        if with_video_colorbars or with_video_framebuffer or with_video_terminal:
            self.videophy = VideoS7HDMIPHY(platform.request("hdmi_out"), clock_domain="hdmi")
            if with_video_colorbars:
                self.add_video_colorbars(phy=self.videophy, timings="640x480@60Hz", clock_domain="hdmi")
            if with_video_terminal:
                self.add_video_terminal(phy=self.videophy, timings="640x480@60Hz", clock_domain="hdmi")
            if with_video_framebuffer:
                self.add_video_framebuffer(phy=self.videophy, timings="640x480@60Hz", clock_domain="hdmi")

        # Ethernet / Etherbone ---------------------------------------------------------------------
        if with_ethernet or with_etherbone:
            self.ethphy = LiteEthPHYRGMII(
                clock_pads  = self.platform.request("eth_clocks", eth_phy),
                pads        = self.platform.request("eth", eth_phy),
                tx_delay    = 1e-9,
                rx_delay    = 1e-9,
            )
            if with_etherbone:
                self.add_etherbone(phy=self.ethphy, ip_address=eth_ip, with_ethmac=with_ethernet)
            elif with_ethernet:
                self.add_ethernet(phy=self.ethphy, dynamic_ip=eth_dynamic_ip, local_ip=eth_ip, remote_ip=eth_remote_ip, software_debug=eth_software_debug)

# Build --------------------------------------------------------------------------------------------

def main():
    from litex.build.parser import LiteXArgumentParser
    parser = LiteXArgumentParser(platform=bochen_kintex7_base.Platform, description=ident_default)
    parser.add_target_argument("--flash",               action="store_true",                                help="Flash bitstream.")

    parser.add_target_argument("--sys-clk-freq",        default=100e6,              type=float,             help="System clock frequency.")
    parser.add_target_argument("--with-sdram",          action="store_true",                                help="Enable optional SDRAM module.")
    parser.add_target_argument("--with-spi-flash",      action="store_true",                                help="Enable SPI Flash (MMAPed).")

    parser.add_target_argument("--with-ethernet",       action="store_true",                                help="Enable Ethernet support.")
    parser.add_target_argument("--with-etherbone",      action="store_true",                                help="Enable Etherbone support.")
    parser.add_target_argument("--eth-phy",             default=0,                                          help="Ethernet/Etherbone PHY index.")
    parser.add_target_argument("--eth-ip",              default="192.168.1.50",                             help="Ethernet/Etherbone IP address.")
    parser.add_target_argument("--eth-remote-ip",       default="192.168.1.106",                            help="Remote IP address of TFTP server.")
    parser.add_target_argument("--eth-dynamic-ip",      action="store_true",                                help="Enable dynamic Ethernet IP addresses setting.")
    parser.add_target_argument("--eth-software-debug",  action="store_true",                                help="Enable UDP debug.")

    sdopts = parser.target_group.add_mutually_exclusive_group()
    sdopts.add_argument("--with-spi-sdcard",            action="store_true",                                help="Enable SPI-mode SDCard support.")
    sdopts.add_argument("--with-sdcard",                action="store_true",                                help="Enable SDCard support.")

    viopts = parser.target_group.add_mutually_exclusive_group()
    viopts.add_argument("--with-video-terminal",        action="store_true",                                help="Enable Video Terminal (VGA).")
    viopts.add_argument("--with-video-framebuffer",     action="store_true",                                help="Enable Video Framebuffer (VGA).")
    viopts.add_argument("--with-video-colorbars",       action="store_true",                                help="Enable Video Colorbars (VGA).")

    parser.set_defaults(
        soc_csv                 = "csr.csv",
        with_sdram              = False,
        with_spi_flash          = False,
        with_sdcard             = False,

        with_ethernet           = False,
        with_etherbone          = False,

        with_video_terminal     = False,
        with_video_framebuffer  = False,
        with_video_colorbars    = False,
    )

    args = parser.parse_args()

    assert not (args.with_etherbone and args.eth_dynamic_ip)

    soc = BaseSoC(
        sys_clk_freq            = args.sys_clk_freq,
        with_sdram              = args.with_sdram,
        with_spi_flash          = args.with_spi_flash,
        with_spi_sdcard         = args.with_spi_sdcard,
        with_sdcard             = args.with_sdcard,

        with_ethernet           = args.with_ethernet,
        with_etherbone          = args.with_etherbone,
        eth_phy                 = args.eth_phy,
        eth_ip                  = args.eth_ip,
        eth_remote_ip           = args.eth_remote_ip,
        eth_dynamic_ip          = args.eth_dynamic_ip,
        eth_software_debug      = args.eth_software_debug,

        with_video_terminal     = args.with_video_terminal,
        with_video_framebuffer  = args.with_video_framebuffer,
        with_video_colorbars    = args.with_video_colorbars,

        **parser.soc_argdict
    )

    builder = Builder(soc, **parser.builder_argdict)

    if args.build:
        builder.build(**parser.toolchain_argdict)

    if args.load:
        prog = soc.platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"))

    if args.flash:
        prog = soc.platform.create_programmer_vivado()
        prog.flash(0, builder.get_bitstream_filename(mode="flash"))
        # prog = soc.platform.create_programmer()
        # print(os.path.join(builder.gateware_dir))
        # prog.flash(0, os.path.join(builder.gateware_dir))

if __name__ == "__main__":
    main()
