# 🔌 Pico W - Offline-First Mimari ve Yeniden Başlatma Testleri

Raspberry Pi Pico W için tasarlanmış, ağ bağlantısı (Wi-Fi/MQTT) kopsa dahi temel donanım görevlerini kesintisiz sürdüren ve cihaz reseti sonrası güvenli başlangıç ilkelerini uygulayan MicroPython altyapısı.

## 🚀 Özellikler

- **Offline-First Çalışma Prensibi:** Pompa süresi ve güvenlik zamanlayıcıları Wi-Fi veya MQTT sunucusundan tamamen bağımsız çalışır; bağlantı kopsa dahi zamanı gelen pompa güvenle kapatılır.
- **Güvenli Yeniden Başlatma (Fail-Safe Boot):** Cihaz elektriği kesilip tekrar açıldığında veya yeniden başlatıldığında Röle 1 kapalı (`LOW`) başlar.
- **Kilitlemeyen Ağ Yönetimi:** İnternet bağlantısı koptuğunda ana kontrol döngüsü kilitlenmez, arka planda periyodik olarak bağlantı kurulmaya çalışılır.

## 📋 Offline Çalışma Test Matrisi

| Senaryo | Beklenen Davranış | Test Sonucu |
| :--- | :--- | :--- |
| **Pompa çalışırken Wi-Fi kopması** | Pompa belirlenen süre sonunda otomatik kapanır. | Başarılı |
| **Cihaz yeniden başlatıldığında** | Röle kesinlikle kapalı başlar. | Başarılı |
| **Broker erişilemez olduğunda** | Yerel sulama mantığı çalışmaya devam eder. | Başarılı |

## 🛠️ Gereksinimler

- Donanım: Raspberry Pi Pico W, Waveshare Pico-Relay-B
- Yazılım: MicroPython (v1.20.0+)