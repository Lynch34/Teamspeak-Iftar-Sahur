# TSBot İftar ve Sahur Takip Botu

Bu Python betiği, TeamSpeak 3 sunucunuzda belirli şehirler için iftar ve sahur saatlerini takip eden ve bu bilgileri kanallarda dinamik olarak güncelleyen bir bottur.

## Gereksinimler

* Python 3.6 veya üzeri
* `tsbot` kütüphanesi
* `unidecode` kütüphanesi
* `python-dotenv` kütüphanesi
* `requests` kütüphanesi

## Kurulum

1.  **Gerekli Kütüphaneleri Yükleyin:**

    ```bash
    pip install tsbot unidecode python-dotenv requests
    ```

2.  **.env Dosyası Oluşturun:**

    Proje dizininde `.env` adında bir dosya oluşturun ve TeamSpeak 3 sunucu bilgilerinizi aşağıdaki formatta ekleyin:

    ```
    TS3_USERNAME=sunucu_kullanici_adi
    TS3_PASSWORD=sunucu_sifresi
    TS3_ADDRESS=sunucu_adresi
    ```

    `sunucu_adresi` kısmında, sunucunuzun adresini doğru şekilde belirttiğinizden emin olun.

3.  **Şehirleri Ayarlayın:**

    Betiğin içindeki `cities` listesini, iftar ve sahur saatlerini takip etmek istediğiniz şehirlerle güncelleyin. Örneğin:

    ```python
    cities = ["Istanbul", "Ankara", "Izmir", "Bursa"]
    ```

4.  **Betiği Çalıştırın:**

    ```bash
    python dosya_adi.py
    ```

    `dosya_adi.py` kısmını, betiğin dosya adıyla değiştirin.

## İşleyiş

1.  **Bağlantı:**

    Bot, TeamSpeak 3 sunucusuna belirtilen kimlik bilgileriyle bağlanır.

2.  **Kanal Oluşturma:**

    Bot, belirtilen şehirler için iftar ve sahur saatlerini gösterecek kanallar oluşturur. Kanalların düzeni şöyledir:

    ```
    ╚═══════════════════╝
    Sahur Saatleri
    ╔═══════════════════╗
    [şehir] | [kalan_sure_sahur]
    ╚═══════════════════╝
    Iftar Saatleri
    ╔═══════════════════╗
    [şehir] | [kalan_sure_iftar]
    ```

    Örneğin:

    ```
    ╚═══════════════════╝
    Sahur Saatleri
    ╔═══════════════════╗
    Istanbul | 2 saat 30 dakika
    Ankara | 2 saat 45 dakika
    ╚═══════════════════╝
    Iftar Saatleri
    ╔═══════════════════╗
    Istanbul | 16 saat 15 dakika
    Ankara | 16 saat 30 dakika
    ```

3.  **Saat Güncelleme:**

    Bot, her dakika iftar ve sahur saatlerini kontrol eder ve kanallardaki süreleri günceller.

4.  **Şehir ID'si Bulma:**

    Bot, `vakit.vercel.app` API'sini kullanarak şehirlerin ID'lerini bulur. Bu ID'ler, iftar ve sahur saatlerini almak için kullanılır.

5.  **İftar ve Sahur Saati Hesaplama:**

    Bot, `vakit.vercel.app` API'sini kullanarak her şehir için iftar ve sahur saatlerini alır ve kalan süreleri hesaplar.

6.  **Hata Yönetimi:**

    Bot, şehir bulunamadığında veya API'den veri alınamadığında hata mesajları yazdırır.

## Özelleştirme

* **Şehirleri Değiştirme:** `cities` listesini düzenleyerek takip edilecek şehirleri değiştirebilirsiniz.
* **Kanal Düzeni:** `create_channel` fonksiyonunu düzenleyerek kanal düzenini değiştirebilirsiniz.
* **Güncelleme Sıklığı:** `asyncio.sleep(60)` satırını düzenleyerek güncelleme sıklığını değiştirebilirsiniz (saniye cinsinden).
* **API Değiştirme:** `vakit.vercel.app` API'sini değiştirmek isterseniz, `check_city_id` ve `check_iftar_and_sahur` fonksiyonlarını uygun şekilde düzenlemeniz gerekir.

## Sorun Giderme

* **Bağlantı Sorunları:** `.env` dosyasındaki kimlik bilgilerinin doğru olduğundan emin olun. Sunucu adresinin ve portunun doğru olduğunu kontrol edin.
* **API Sorunları:** `vakit.vercel.app` API'sinin çalıştığından emin olun. API'den veri alamıyorsanız, API belgelerini kontrol edin.
* **Kanal Oluşturma Sorunları:** TeamSpeak 3 sunucusunda botun kanal oluşturma yetkisine sahip olduğundan emin olun.

## Notlar

* Bu betik, `vakit.vercel.app` API'sini kullanır. API'nin kullanım koşullarını ve sınırlamalarını kontrol edin.
* TeamSpeak 3 sunucunuzda botun gerekli yetkilere sahip olduğundan emin olun.
* Betiği çalıştırırken herhangi bir sorunla karşılaşırsanız, hata mesajlarını kontrol edin ve gerekli düzenlemeleri yapın.