import time
import ujson
import network
from machine import Pin
import storage
from mqtt_client import ResilientMQTTClient

# Donanım ve Konfigürasyon
config = storage.load_config()
WIFI_SSID = config.get("wifi_ssid")
WIFI_PASS = config.get("wifi_pass")
BROKER = config.get("mqtt_broker", "broker.hivemq.com")
STUDENT_ID = config.get("student_id", "onurcan")
DEVICE_ID = config.get("device_id", "pico-w-pump-01")

# Donanım Tanımlaması (Pico-Relay-B Röle 1)
PUMP_RELAY_PIN = 21
pump_relay = Pin(PUMP_RELAY_PIN, Pin.OUT, value=0)  # KURAL: Cihaz reseti sonrası röle HER ZAMAN kapalı başlar!

# Topic Ağacı
TOPIC_BASE = f"internship/{STUDENT_ID}/{DEVICE_ID}"
TOPIC_COMMAND = f"{TOPIC_BASE}/command"
TOPIC_STATE = f"{TOPIC_BASE}/state"
TOPIC_AVAILABILITY = f"{TOPIC_BASE}/availability"

# Pompa Durum Değişkenleri
pump_state = "stopped"
pump_start_time = 0
pump_duration = 0

def connect_wifi_non_blocking():
    """Arka planda Wi-Fi bağlantısını kontrol eder, ana döngüyü kilitlemez."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    return wlan.isconnected()

print("=== PICO W OFFLINE-FIRST ARCHITECTURE & REBOOT TESTS ===")

# MQTT İstemcisini Başlat
mqtt = ResilientMQTTClient(client_id=f"{DEVICE_ID}-offline-test", broker=BROKER)

# Manuel Pompa Başlatma (Offline Test İçin 20 Saniye)
pump_relay.value(1)
pump_state = "running"
pump_start_time = time.ticks_ms()
pump_duration = 20
print("[OFLLINE TEST] Pompa 20 saniye için başlatıldı. Wi-Fi/MQTT kesilse de durmayacak.")

last_conn_check = 0
CHECK_INTERVAL = 5000  # 5 saniyede bir bağlantı denemesi

while True:
    current_time = time.ticks_ms()

    # -------------------------------------------------------------
    # CRITICAL TASK: Pompa Süresi Kontrolü (Ağ durumundan TAMAMEN BAĞIMSIZ)
    # -------------------------------------------------------------
    if pump_state == "running":
        elapsed_sec = time.ticks_diff(current_time, pump_start_time) // 1000
        if elapsed_sec >= pump_duration:
            pump_relay.value(0)
            pump_state = "stopped"
            print("[OFLLINE TEST OK] Ağ olmasa dahi çalışma süresi doldu ve pompa güvenle durduruldu.")

    # -------------------------------------------------------------
    # NETWORK TASK: Bağlantı Varsa MQTT Kontrol Et, Yoksa Periyodik Dene
    # -------------------------------------------------------------
    if time.ticks_diff(current_time, last_conn_check) >= CHECK_INTERVAL:
        last_conn_check = current_time
        
        if connect_wifi_non_blocking():
            if not mqtt.is_connected:
                print("[NETWORK] İnternet mevcut. Broker'a bağlanılıyor...")
                if mqtt.connect(lwt_topic=TOPIC_AVAILABILITY, lwt_msg="offline"):
                    mqtt.publish(TOPIC_AVAILABILITY, "online", retain=True)
                    mqtt.subscribe(TOPIC_COMMAND)
            else:
                mqtt.check_msg()
        else:
            print("[OFFLINE MODE] Wi-Fi bağlantısı yok. Yerel zamanlayıcı çalışmaya devam ediyor...")

    time.sleep_ms(50)