# HTTPS Sorunu Çözümü

Google Maps API HTTPS gerektiriyor. HTTP üzerinden çalışması için:

## Çözüm 1: API Key'e HTTP Referrer Ekleme (Önerilen)

1. Google Cloud Console'a gidin: https://console.cloud.google.com/
2. "APIs & Services" > "Credentials" bölümüne gidin
3. API key'inizi bulun ve tıklayın
4. "Application restrictions" bölümünde:
   - "HTTP referrers (web sites)" seçin
   - "Add an item" tıklayın
   - Şu referrer'ları ekleyin:
     - `http://localhost:5000/*`
     - `http://127.0.0.1:5000/*`
     - `http://localhost:*/*`
5. "Save" tıklayın

## Çözüm 2: HTTPS Sunucusu Kullanma

HTTPS için sertifika oluşturmanız gerekiyor. Windows'ta:

1. OpenSSL yükleyin (veya Git Bash ile gelen OpenSSL'i kullanın)
2. Terminal'de şu komutu çalıştırın:
   ```
   openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
   ```
3. `server.py` dosyası otomatik olarak sertifikayı kullanacak
4. `https://localhost:5000` adresini açın
5. Tarayıcıda "Güvenli değil" uyarısı çıkarsa "Gelişmiş" > "Devam et" ile geçin

## Çözüm 3: Basit HTTPS Server (Python)

Alternatif olarak, basit bir HTTPS server için:

```python
python -m http.server 5000 --bind localhost
```

Ama bu da sertifika gerektirir.

## Not

HTTP üzerinden çalışması için API key'in HTTP referrer'lara izin vermesi gerekiyor. Aksi halde Google Maps API çalışmayacaktır.
