# MicroPython SSD1306 OLED driver, I2C and SPI interfaces

from micropython import const
import framebuf

# 將波特律動 16x16 字模匯入
from font16 import FONT16


SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)

class SSD1306:
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        self.fb = framebuf.FrameBuffer(
            self.buffer, self.width, self.height, framebuf.MONO_VLSB
        )
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00,
            SET_MEM_ADDR, 0x00,
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01,
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR | 0x08,
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x02 if self.height == 32 else 0x12,
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0x22 if self.external_vcc else 0xF1,
            SET_VCOM_DESEL, 0x30,
            SET_CONTRAST, 0xFF,
            SET_ENTIRE_ON,
            SET_NORM_INV,
            SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01,
        ):
            self.write_cmd(cmd)

    def fill(self, col):
        self.fb.fill(col)

    def pixel(self, x, y, col):
        self.fb.pixel(x, y, col)

    def text(self, string, x, y, col=1):
        self.fb.text(string, x, y, col)

    def show(self):
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.width - 1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)

class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.i2c.writeto(self.addr, b"\x40" + buf)
        
    def _font16_row_to_vlsb(self, font):
        """
        將波特律動 16x16 字模轉 SSD1306 MONO_VLSB 可用格式
        保持字型方向正確（水平排列），不鏡像、不旋轉
        """
        out = bytearray(32)  # 16x16 -> 32 bytes
        img = font[4:]       # 跳過前 4 bytes 頭部

        for i in range(16):  # 波特律動原本 Column
            byte_top = img[i*2]
            byte_bottom = img[i*2+1]

            # 上半部 8 pixel
            for bit in range(8):
                if byte_top & (1 << bit):
                    page = i // 8
                    out[page*16 + bit] |= 1 << (i % 8)

            # 下半部 8 pixel
            for bit in range(8):
                if byte_bottom & (1 << bit):
                    page = i // 8
                    out[page*16 + bit + 8] |= 1 << (i % 8)

        return out

    def text16(self, text, x, y, spacing=0):
        """
        直接在 OLED 上顯示多個 FONT16 中文字
        用法：oled.text16("你好嗎", 0, 32)
        """
        cx = x
        for ch in text:
            raw = FONT16.get(ch)
            if raw:
                data = self._font16_row_to_vlsb(raw)
                fb = framebuf.FrameBuffer(bytearray(data), 16, 16, framebuf.MONO_VLSB)
                self.fb.blit(fb, cx, y)
            cx += 16 + spacing