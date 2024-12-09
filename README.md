# ReportQL

SQL Server veritabanınıza bağlanarak sorgular çalıştırmanızı ve sonuçları grafiksel olarak görüntülemenizi sağlayan bir raporlama aracı.

## Özellikler

- SQL Server veritabanına bağlanma
- Özel SQL sorguları çalıştırma
- Sorgu sonuçlarını tablo halinde görüntüleme
- Çeşitli grafik tipleriyle veri görselleştirme:
  - Çizgi Grafik
  - Sütun Grafik
  - Pasta Grafik
  - Alan Grafik

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. SQL Server ODBC sürücüsünü yükleyin:
- Windows: Microsoft ODBC Driver for SQL Server'ı indirin ve yükleyin
- macOS/Linux: unixODBC ve Microsoft ODBC Driver for SQL Server'ı yükleyin

## Kullanım

1. Uygulamayı başlatın:
```bash
streamlit run app.py
```

2. Web tarayıcınızda açılan arayüzden:
   - Veritabanı bağlantı bilgilerini girin
   - SQL sorgunuzu yazın
   - Sorguyu çalıştırın
   - Sonuçları görüntüleyin ve grafikler oluşturun

## Gereksinimler

- Python 3.7+
- SQL Server
- SQL Server ODBC Driver
# MertQl
