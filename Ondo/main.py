"""
GASに送信して、ワークシートに温湿度センサーの値を追加していく
2025-01-07 penkich
温湿度センサー：AHT21B
表示器　　　　：ssd1306(I2C)
マイコン　　　：xiao esp32c3
"""
from machine import Pin, I2C
import ssd1306
import time
import ntptime
from ahtx0 import AHT10  # AHT10ライブラリはAHT21Bとも互換性があります

# I2Cの設定
i2c = I2C(0, scl=Pin(5), sda=Pin(4))  # SCL=GPIO5, SDA=GPIO4

# AHT21Bの初期化
sensor = AHT10(i2c)

# SSD1306 OLEDの初期化
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('ESSID', 'PASS') # 使用するESSIDとPASSを入れます。
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect() # WiFiに接続

UTC_OFFSET = 9 * 60 * 60 # JST補正用
ntptime.settime() # ネットワークタイム

import requests

# デプロイIDをここにコピペ
deployid = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


# メインループ
while True:
    try:
        # AHT21Bから温湿度データを取得
        temperature = sensor.temperature
        humidity = sensor.relative_humidity
        (year, month, date, hour, minute, sec, week, yearday) = time.localtime(time.time() + UTC_OFFSET)
        yyyymmdd = f'{year}/{month:02d}/{date:02d}'
        jikoku = f'{hour:02d}:{minute:02d}:{sec:02d}'

        # ディスプレイにデータを表示
        oled.fill(0)  # 画面をクリア
        # oled.text("AHT21B Sensor", 0, 0)
        oled.text("Temp: {:.2f} C".format(temperature), 0, 0)
        oled.text("Hum : {:.2f} %".format(humidity), 0, 16)
        oled.text(f'Date: {yyyymmdd}', 0, 32)
        oled.text(f'Time: {jikoku}', 0, 48)
        oled.show()
        
        # GASに送信
        requests.get(f'https://script.google.com/macros/s/{deployid}/exec?yyyymmdd={yyyymmdd}&jikoku={jikoku}&temp={temperature}&humid={humidity}')

        # 600秒待機
        time.sleep(600) # 送信間隔（秒）を設定します。
        

    except Exception as e:
        # エラー処理
        oled.fill(0)
        oled.text("Error:", 0, 0)
        oled.text(str(e), 0, 16)
        oled.show()
        time.sleep(2)
