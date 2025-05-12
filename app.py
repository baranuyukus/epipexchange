from flask import Flask, render_template, request, redirect, jsonify
import json
from datetime import datetime
import pandas as pd
import math

app = Flask(__name__)

INITIAL_STOCK = 1000  # Her ürün için başlangıç stok miktarı
VOLATILITY_FACTOR = 0.02  # Fiyat değişim faktörü

# Ürünler başlangıç verisi
products = [
    {
        "id": 0, 
        "name": "Ürün A", 
        "code": "DEP000",
        "base_price": 100, 
        "current_price": 100, 
        "initial_stock": INITIAL_STOCK,
        "remaining_stock": INITIAL_STOCK,
        "demand": 0, 
        "price_history": [],
        "volatility": 1.0  # Ürünün volatilite katsayısı
    },
    {
        "id": 1, 
        "name": "Ürün B", 
        "code": "DEP001",
        "base_price": 120, 
        "current_price": 120, 
        "initial_stock": INITIAL_STOCK,
        "remaining_stock": INITIAL_STOCK,
        "demand": 0, 
        "price_history": [],
        "volatility": 1.2  # Daha yüksek volatilite
    },
    {
        "id": 2, 
        "name": "Ürün C", 
        "code": "DEP002",
        "base_price": 90, 
        "current_price": 90, 
        "initial_stock": INITIAL_STOCK,
        "remaining_stock": INITIAL_STOCK,
        "demand": 0, 
        "price_history": [],
        "volatility": 0.8  # Daha düşük volatilite
    },
    {
        "id": 3, 
        "name": "Ürün D", 
        "code": "DEP003",
        "base_price": 110, 
        "current_price": 110, 
        "initial_stock": INITIAL_STOCK,
        "remaining_stock": INITIAL_STOCK,
        "demand": 0, 
        "price_history": [],
        "volatility": 1.5  # En yüksek volatilite
    }
]

def calculate_price_change(product):
    """
    Stok durumuna ve talebe göre fiyat değişimini hesaplar
    """
    stock_ratio = product["remaining_stock"] / product["initial_stock"]
    demand_pressure = product["demand"] / product["initial_stock"]
    
    # Stok azaldıkça fiyat arttır
    stock_factor = math.exp(2 * (1 - stock_ratio)) - 1
    
    # Talep baskısı faktörü
    demand_factor = math.log1p(demand_pressure) * VOLATILITY_FACTOR * 2
    
    # Volatilite etkisi
    volatility_impact = product["volatility"] * (1 + abs(stock_factor))
    
    # Toplam fiyat değişim 
    total_factor = (stock_factor + demand_factor) * volatility_impact
    
    # Değişim faktörünü sınırla
    return min(max(total_factor, -0.1), 0.15)  # Maksimum %15 artış, %10 düşüş

def calculate_min_price(product):
    """
    Stok durumuna göre minimum fiyat hesaplar
    """
    stock_ratio = product["remaining_stock"] / product["initial_stock"]
    base_price = product["base_price"]
    
    # Stok azaldıkça minimum fiyat artar
    min_price_factor = math.exp(1.5 * (1 - stock_ratio)) 
    return base_price * min_price_factor

def update_price_history(product, price):
    """
    Ürünün fiyat geçmişini günceller
    """
    product["price_history"].append({
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "price": round(price, 2)
    })
    # Son 50 veriyi tut
    if len(product["price_history"]) > 50:
        product["price_history"].pop(0)

@app.route("/")
def index():
    return render_template("index.html", products=products)

@app.route("/buy/<int:product_id>", methods=["POST"])
def buy(product_id):
    target_product = None
    price_change = 0
    success = False
    
    for product in products:
        if product["id"] == product_id:
            # Stok kontrolü
            if product["remaining_stock"] <= 0:
                return jsonify({
                    "error": "Stok yetersiz",
                    "products": products
                }), 400
            
            # İşlemi gerçekleştir
            product["demand"] += 1
            product["remaining_stock"] -= 1
            
            # Fiyat değişimi hesapla
            price_change = calculate_price_change(product)
            new_price = product["current_price"] * (1 + price_change)
            
            # Minimum fiyat kontrolü
            min_price = calculate_min_price(product)
            new_price = max(min_price, new_price)
            product["current_price"] = round(new_price, 2)
            update_price_history(product, new_price)
            target_product = product
            success = True
            break
    
    if success and target_product:
        # Diğer ürünlerin fiyatlarını güncelle
        for product in products:
            if product["id"] != product_id:
                # Diğer ürünlerin fiyatları hedef ürünün değişimine ters orantılı etkilenir
                # Ancak stok durumuna göre sınırlandırılır
                stock_ratio = product["remaining_stock"] / product["initial_stock"]
                max_decrease = -0.1 * stock_ratio  # Stok azaldıkça düşüş sınırlanır
                
                inverse_change = -price_change * 0.3 * (product["volatility"] / target_product["volatility"])
                inverse_change = max(inverse_change, max_decrease)
                
                new_price = product["current_price"] * (1 + inverse_change)
                min_price = calculate_min_price(product)
                new_price = max(min_price, new_price)
                product["current_price"] = round(new_price, 2)
                update_price_history(product, new_price)
        
        return jsonify({
            "success": True,
            "products": products
        })
    else:
        return jsonify({
            "error": "Ürün bulunamadı",
            "products": products
        }), 404

@app.route("/api/products")
def api_products():
    return jsonify(products)

@app.route("/api/price_history/<int:product_id>")
def price_history(product_id):
    product = products[product_id]
    return jsonify(product["price_history"])

if __name__ == "__main__":
    # Başlangıç fiyat geçmişi
    for p in products:
        update_price_history(p, p["current_price"])
    app.run(debug=True, port=5002) 