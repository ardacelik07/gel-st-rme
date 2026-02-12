# Netlify ile Deploy

## 1. GitHub'a push (ilk kez)

Proje klasöründe terminal açın:

```bash
cd "c:\Users\celik\Desktop\sevgililer gümü"

git init
git add .
git commit -m "Sevgililer günü rotası - Netlify deploy"
```

GitHub'da yeni bir repo oluşturun (https://github.com/new), sonra:

```bash
git remote add origin https://github.com/KULLANICI_ADINIZ/REPO_ADI.git
git branch -M main
git push -u origin main
```

(KULLANICI_ADINIZ ve REPO_ADI yerine kendi GitHub kullanıcı adınızı ve repo adınızı yazın.)

## 2. Netlify'a bağlama

1. https://app.netlify.com adresine gidin, giriş yapın (GitHub ile giriş yapabilirsiniz).
2. **Add new site** → **Import an existing project**.
3. **GitHub** seçin, repo'nuzu seçin.
4. Ayarlar:
   - **Build command:** boş bırakın
   - **Publish directory:** `.` (nokta)
5. **Site settings** → **Environment variables** bölümüne gidin.
6. **Add a variable** → **Add single variable**:
   - Key: `GOOGLE_MAPS_API_KEY`
   - Value: `AIzaSyAKS4a9rCu2hRTebc2lHA9o24BthtqyLjc`
   - (İsterseniz kendi API key'inizi kullanın.)
7. **Deploy site** tıklayın.

Birkaç dakika sonra siteniz canlı olacak (örn. `https://rastgele-isim.netlify.app`).

## 3. Sonraki güncellemeler

Kodda değişiklik yaptıktan sonra:

```bash
git add .
git commit -m "Açıklama"
git push
```

Netlify otomatik olarak yeni deploy alacaktır.

## Not

- **HTTPS:** Netlify varsayılan olarak HTTPS kullanır, Google Maps API sorunsuz çalışır.
- **API key:** Netlify'da environment variable olarak eklediğinizde function bu key'i kullanır; kodu değiştirmenize gerek yok.
