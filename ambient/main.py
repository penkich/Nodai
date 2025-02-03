def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('ESSID', 'xxxxxxxxxxxxx')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
do_connect()

import ambient
am = ambient.Ambient(チャネルID, "ライトキー", "リードキー")

from machine import Pin, I2C,WDT
import ssd1306
import time
from ahtx0 import AHT10  # AHT10ライブラリはAHT21Bとも互換性があります

# I2Cの設定
i2c = I2C(0, scl=Pin(5), sda=Pin(4))  # SCL=GPIO5, SDA=GPIO4

# AHT21Bの初期化
sensor = AHT10(i2c)

# SSD1306 OLEDの初期化
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)




# ウオッチドッグタイマー
# （サンプリングインターバルより長いこと！）
wdt = WDT(timeout=30 * 60000) # 30分

# メインループ
count = 0  # カウンターを初期化
while True:
    try:
        # AHT21Bから温湿度データを取得
        temperature = sensor.temperature
        humidity = sensor.relative_humidity

        # ディスプレイにデータを表示
        oled.fill(0)  # 画面をクリア
        oled.text("AHT21B Sensor", 0, 0)
        oled.text("Temp: {:.2f} C".format(temperature), 0, 16)
        oled.text("Hum: {:.2f} %".format(humidity), 0, 32)
        oled.show()

        # 1秒待機
        time.sleep(1)
        if count > 600: # 600秒を超えたら
            r = am.send({'d1': temperature, 'd2': humidity}) # 送信
            count = 0 # 送信したらカウンターを初期化
        count = count + 1 # 600秒を超えてなければカウントアップ

    except Exception as e:
        # エラー処理
        oled.fill(0)
        oled.text("Error:", 0, 0)
        oled.text(str(e), 0, 16)
        oled.show()
        time.sleep(2)
    wdt.feed() # ここまで時間内に来れたらリブート（再起動）させない。

