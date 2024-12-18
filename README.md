# Python Project Template

Modern ve ölçeklenebilir bir Python projesi.

## Proje Yapısı

```
Try/
├── src/              # Kaynak kodlar
│   ├── api/          # API ve route tanımlamaları
│   ├── models/       # Veritabanı modelleri
│   ├── services/     # İş mantığı servisleri
│   └── utils/        # Yardımcı fonksiyonlar
├── tests/            # Test dosyaları
├── config/           # Konfigürasyon dosyaları
└── app.py           # Ana uygulama dosyası
```

## Kurulum

1. Sanal ortam oluşturun:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

2. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

3. Uygulamayı çalıştırın:
```bash
python app.py
```

## Geliştirme

- Kod formatı için `black` kullanılmaktadır
- Kod kalitesi için `flake8` kullanılmaktadır
- Testler için `pytest` kullanılmaktadır

## Test

```bash
pytest tests/
