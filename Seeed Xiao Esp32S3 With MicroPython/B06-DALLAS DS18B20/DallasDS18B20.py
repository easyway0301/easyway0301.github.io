from machine import Pin
import onewire, ds18x20 # MicroPython 內建的驅動模組（driver）
import time

dat = Pin(9, Pin.IN, Pin.PULL_UP)  # 建議腳位
ow = onewire.OneWire(dat)
ds = ds18x20.DS18X20(ow)

roms = ds.scan()
print("找到 DS18B20:", roms)

if not roms:
    print("❌ 沒有偵測到 DS18B20，請檢查接線與 4.7kΩ 上拉電阻")
else:
    ds.convert_temp()
    time.sleep_ms(750)

    for rom in roms:
        temp = ds.read_temp(rom)
        print("🌡 溫度:", temp, "°C")

