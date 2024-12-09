import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Sayfa yapılandırması
st.set_page_config(page_title="ReportQL", page_icon="📊", layout="wide")

# Başlık
st.title("ReportQL - Mağaza Raporlama Aracı")

with st.sidebar:
    st.header("Mağaza Veritabanı")
    db_file = st.text_input("Veritabanı Dosyası", "store.db")

    if st.button("Örnek Veritabanı Oluştur"):
        conn = sqlite3.connect(db_file)
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
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                customer_name TEXT NOT NULL,
                email TEXT,
                city TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY,
                sale_date TEXT NOT NULL,
                customer_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
                FOREIGN KEY (product_id) REFERENCES products (product_id)
            )
        ''')
        
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
            (3, 'Tablet', 1, 5000, 75),
            (4, 'T-Shirt', 2, 200, 300),
            (5, 'Kot Pantolon', 2, 400, 200),
            (6, 'Roman', 3, 50, 1000),
            (7, 'Bilgisayar Kitabı', 3, 120, 150),
            (8, 'Koşu Ayakkabısı', 4, 800, 100),
            (9, 'Yoga Matı', 4, 150, 200),
            (10, 'Kahve Makinesi', 5, 2000, 50)
        ]
        c.executemany('INSERT OR REPLACE INTO products VALUES (?,?,?,?,?)', products_data)
        
        customers_data = [
            (1, 'Ahmet Yılmaz', 'ahmet@email.com', 'İstanbul'),
            (2, 'Ayşe Demir', 'ayse@email.com', 'Ankara'),
            (3, 'Mehmet Kaya', 'mehmet@email.com', 'İzmir'),
            (4, 'Fatma Şahin', 'fatma@email.com', 'Bursa'),
            (5, 'Ali Öztürk', 'ali@email.com', 'Antalya')
        ]
        c.executemany('INSERT OR REPLACE INTO customers VALUES (?,?,?,?)', customers_data)
        
        import random
        from datetime import datetime, timedelta
        sales_data = []
        sale_id = 1
        start_date = datetime(2023, 1, 1)
        
        for _ in range(1000):
            sale_date = start_date + timedelta(days=random.randint(0, 364))
            customer_id = random.randint(1, 5)
            product_id = random.randint(1, 10)
            
            c.execute('SELECT unit_price FROM products WHERE product_id = ?', (product_id,))
            unit_price = c.fetchone()[0]
            
            quantity = random.randint(1, 5)
            total_price = unit_price * quantity
            sales_data.append((sale_id, sale_date.strftime('%Y-%m-%d'), customer_id, product_id, quantity, total_price))
            sale_id += 1
        
        c.executemany('INSERT OR REPLACE INTO sales VALUES (?,?,?,?,?,?)', sales_data)
        
        conn.commit()
        conn.close()
        st.success("Örnek mağaza veritabanı oluşturuldu!")
        
        st.info("""
        Örnek Sorgular:
        
        1. Kategori bazında toplam satış:
        ```sql
        SELECT c.category_name, SUM(s.total_price) as total_sales
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        JOIN categories c ON p.category_id = c.category_id
        GROUP BY c.category_name
        ORDER BY total_sales DESC;
        ```
        
        2. Aylık satış raporu:
        ```sql
        SELECT 
            strftime('%Y-%m', sale_date) as month,
            COUNT(*) as total_orders,
            SUM(total_price) as total_revenue
        FROM sales
        GROUP BY month
        ORDER BY month;
        ```
        
        3. En çok satın alma yapan müşteriler:
        ```sql
        SELECT 
            c.customer_name,
            c.city,
            COUNT(*) as total_orders,
            SUM(s.total_price) as total_spent
        FROM sales s
        JOIN customers c ON s.customer_id = c.customer_id
        GROUP BY c.customer_id
        ORDER BY total_spent DESC;
        ```
        
        4. En çok satan ürünler:
        ```sql
        SELECT 
            p.product_name,
            cat.category_name,
            SUM(s.quantity) as total_quantity,
            SUM(s.total_price) as total_revenue
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        JOIN categories cat ON p.category_id = cat.category_id
        GROUP BY p.product_id
        ORDER BY total_quantity DESC;
        ```
        """)

# Kullanıcı sorgu girişi
query = st.text_area("SQL Sorgunuzu Buraya Yazın", height=200)

# Sorguyu çalıştırma butonu
if st.button("Sorguyu Çalıştır"):
    try:
        conn = sqlite3.connect(db_file)
        df = pd.read_sql(query, conn)
        conn.close()
        st.session_state['df'] = df  # DataFrame'i session state'e kaydet
        
        st.subheader("Sorgu Sonuçları")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Hata oluştu: {str(e)}")

# Eğer session_state'de df varsa grafik oluşturma seçeneklerini göster
if 'df' in st.session_state and not st.session_state['df'].empty:
    df = st.session_state['df']
    st.subheader("Grafik Oluştur")
    col1, col2 = st.columns(2)

    with col1:
        chart_type = st.selectbox(
            "Grafik Türü",
            ["Çizgi Grafik", "Sütun Grafik", "Pasta Grafik", "Alan Grafik"]
        )

    with col2:
        x_axis = st.selectbox("X Ekseni", df.columns)
        y_axis = st.selectbox("Y Ekseni", df.columns)

    if st.button("Grafik Oluştur"):
        if chart_type == "Çizgi Grafik":
            fig = px.line(df, x=x_axis, y=y_axis)
        elif chart_type == "Sütun Grafik":
            fig = px.bar(df, x=x_axis, y=y_axis)
        elif chart_type == "Pasta Grafik":
            fig = px.pie(df, values=y_axis, names=x_axis)
        else:  # Alan Grafik
            fig = px.area(df, x=x_axis, y=y_axis)

        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("ReportQL 2024")