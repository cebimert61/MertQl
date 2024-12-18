import sqlite3
from datetime import datetime, timedelta
import random

def create_sample_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Tablo yapıları
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category_id INTEGER,
            unit_price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (category_id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY,
            sale_date TEXT NOT NULL,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    ''')
    
    # Örnek veriler
    categories_data = [
        (1, 'Elektronik'),
        (2, 'Giyim'),
        (3, 'Kitap'),
        (4, 'Spor'),
        (5, 'Ev & Yaşam')
    ]
    c.executemany('INSERT OR REPLACE INTO categories VALUES (?,?)', categories_data)
    
    products_data = [
        (1, 'Laptop', 1, 15000, 50),
        (2, 'Akıllı Telefon', 1, 8000, 100),
        (3, 'T-Shirt', 2, 200, 300),
        (4, 'Roman', 3, 50, 1000),
        (5, 'Koşu Ayakkabısı', 4, 800, 100)
    ]
    c.executemany('INSERT OR REPLACE INTO products VALUES (?,?,?,?,?)', products_data)
    
    # Örnek satış verileri
    sales_data = []
    sale_id = 1
    start_date = datetime(2022, 1, 1)
    
    for _ in range(1000):
        sale_date = start_date + timedelta(days=random.randint(0, 730))  # 2 yıllık veri
        product_id = random.randint(1, 5)
        
        c.execute('SELECT unit_price FROM products WHERE product_id = ?', (product_id,))
        unit_price = c.fetchone()[0]
        
        quantity = random.randint(1, 5)
        total_price = unit_price * quantity
        
        sales_data.append((sale_id, sale_date.strftime('%Y-%m-%d'), product_id, quantity, total_price))
        sale_id += 1
    
    c.executemany('INSERT OR REPLACE INTO sales VALUES (?,?,?,?,?)', sales_data)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_sample_db('sample.db')
