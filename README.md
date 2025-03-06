# TSBot İftar ve Sahur Takip Botu

Bu Python scripti, TeamSpeak 3 sunucunuzda belirli şehirler için iftar ve sahur saatlerini takip eden ve bu bilgileri kanallarda dinamik olarak güncelleyen bir bottur.

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

    Proje dizininde `.env` adında bir dosya oluşturun ve TeamSpeak 3 yatqa bilgilerinizi aşağıdaki formatta ekleyin:
    Size önerim ayrı bir serverquery login açmanız ve onu girmeniz.

    ```
    TS3_USERNAME=yatqa_kullanici_adi
    TS3_PASSWORD=yatqa_şifresi
    TS3_ADDRESS=sunucu_adresi
    ```

    Örnek .env dosyası:
    ```
    TS3_USERNAME=serveradmin
    TS3_PASSWORD=sifregir
    TS3_ADDRESS=192.168.1.1
    ```

    `sunucu_adresi` kısmında, sunucunuzun adresini doğru şekilde belirttiğinizden emin olun.

3.  **Şehirleri Ayarlayın:**

    Scriptin içindeki `cities` listesini, iftar ve sahur saatlerini takip etmek istediğiniz şehirlerle güncelleyin. Örneğin:

    ```python
    cities = ["Istanbul", "Ankara", "Izmir", "Bursa"]
    ```

4.  **Betiği Çalıştırın:**

    ```bash
    python dosya_adi.py
    ```

    `dosya_adi.py` kısmını, scriptin dosya adıyla değiştirin.

## İşleyiş

1.  **Bağlantı:**

    Bot, TeamSpeak 3 sunucusuna belirtilen kimlik bilgileriyle bağlanır.

2.  **Kanal Oluşturma:**

    Bot, belirtilen şehirler için iftar ve sahur saatlerini gösterecek kanallar oluşturur. Kanalların düzeni şöyledir:

    ![Görsel](https://i.hizliresim.com/t5x4eku.png)

3.  **Saat Güncelleme:**

    Bot, her dakika iftar ve sahur saatlerini kontrol eder ve kanallardaki süreleri günceller.

4.  **Şehir ID'si Bulma:**

    Bot, `vakit.vercel.app` API'sini kullanarak şehirlerin ID'lerini bulur. Bu ID'ler, iftar ve sahur saatlerini almak için kullanılır.

5.  **İftar ve Sahur Saati Hesaplama:**

    Bot, `vakit.vercel.app` API'sini kullanarak her şehir için iftar ve sahur saatlerini alır ve kalan süreleri hesaplar.

## Özelleştirme

* **Şehirleri Değiştirme:** `cities` listesini düzenleyerek takip edilecek şehirleri değiştirebilirsiniz.

## Sorun Giderme

* **Bağlantı Sorunları:** `.env` dosyasındaki kimlik bilgilerinin doğru olduğundan emin olun. Sunucu adresinin ve portunun doğru olduğunu kontrol edin.
* **API Sorunları:** `vakit.vercel.app` API'sinin çalıştığından emin olun. API'den veri alamıyorsanız, API belgelerini kontrol edin.

## Notlar

* Bu script, `vakit.vercel.app` API'sini kullanır. API'nin kullanım koşullarını ve sınırlamalarını kontrol edin.
* Scripti çalıştırırken herhangi bir sorunla karşılaşırsanız, hata mesajlarını kontrol edin ve gerekli düzenlemeleri yapın.