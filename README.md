# Dinamik Fiyatlandırma Sistemi

Bu proje, talep bazlı dinamik fiyatlandırma sisteminin prototip uygulamasıdır. Sistem, ürünlerin fiyatlarını talebe göre otomatik olarak ayarlar.

## Özellikler

- 4 farklı ürün için gerçek zamanlı fiyat takibi
- Talep bazlı otomatik fiyat ayarlama
- Görsel fiyat geçmişi grafikleri
- Responsive tasarım
- Anlık fiyat güncellemeleri

## Kurulum

1. Python 3.8 veya üzeri sürümün yüklü olduğundan emin olun
2. Proje dizinine gidin:
   ```bash
   cd demand_market_app
   ```
3. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
4. Uygulamayı başlatın:
   ```bash
   python app.py
   ```
5. Tarayıcınızda `http://localhost:5000` adresini açın

## Nasıl Çalışır?

- Her ürünün bir taban fiyatı vardır
- Bir ürün satın alındığında:
  - O ürünün fiyatı %5 artar
  - Diğer ürünlerin fiyatları %3 düşer (taban fiyatın altına düşmez)
- Fiyat değişimleri gerçek zamanlı olarak grafiklerde gösterilir
- Piyasa genel görünümü grafiği tüm ürünlerin fiyat hareketlerini karşılaştırmalı olarak gösterir

## Teknolojiler

- Backend: Python Flask
- Frontend: HTML, CSS, JavaScript
- Grafikler: Plotly.js
- HTTP İstekleri: Axios 