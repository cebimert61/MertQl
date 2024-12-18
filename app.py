import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from src.nlp.query_generator import QueryGenerator
from src.visualization.chart_generator import ChartGenerator
from src.db.init_db import create_sample_db

# Çevre değişkenlerini yükle
# load_dotenv()

# SQLite veritabanı yolu
DB_PATH = 'sample.db'

# Eğer veritabanı yoksa örnek veritabanını oluştur
if not os.path.exists(DB_PATH):
    create_sample_db(DB_PATH)

# SQLite engine oluştur
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL)

# Sayfa yapılandırması
st.set_page_config(page_title="SQL ANALİZ", layout="wide")
st.title("SQL ANALİZ")

# Sınıf örneklerini oluştur
query_generator = QueryGenerator()
chart_generator = ChartGenerator()

# Ana içerik ve yan menü için sütunlar oluştur
main_col, settings_col = st.columns([2, 1])

with main_col:
    # Kullanıcı girişi
    user_query = st.text_input(
        "Ne görmek istediğinizi Türkçe olarak yazın:",
        placeholder="Örnek: Yıllara göre satılan ürünlerin çizgi grafiğini çıkart"
    )

    if user_query:
        try:
            # SQL sorgusunu oluştur
            sql_query = query_generator.generate_sql(user_query)
            
            # Veritabanı sorgusu çalıştır
            with engine.connect() as conn:
                df = pd.read_sql(sql_query, conn)
            
            # Sonuçları göster
            st.subheader("Veri Tablosu")
            st.dataframe(df)
            
            # Kullanıcıya sütun seçimi yaptır
            columns = df.columns.tolist()
            x_column = st.selectbox("X Ekseni için sütun seçin:", columns)
            y_column = st.selectbox("Y Ekseni için sütun seçin:", columns)
            
            # Grafik türü seçimi
            chart_types = {
                'Çizgi Grafik': 'line',
                'Sütun Grafik': 'bar',
                'Dağılım Grafiği': 'scatter',
                'Alan Grafiği': 'area',
                'Pasta Grafiği': 'pie'
            }
            selected_chart = st.selectbox("Grafik türünü seçin:", list(chart_types.keys()))
            
            # Grafiği oluştur ve göster
            st.subheader("Grafik")
            try:
                fig = chart_generator.create_chart(
                    df, 
                    x_column=x_column, 
                    y_column=y_column,
                    chart_type=chart_types[selected_chart],
                    title=f"{selected_chart}: {x_column} - {y_column}"
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Grafik oluşturulurken hata oluştu: {str(e)}")
            
        except Exception as e:
            st.error(f"Bir hata oluştu: {str(e)}")

with settings_col:
    st.header("Nasıl Kullanılır?")
    st.markdown("""
    1. Analiz yapmak istediğiniz konuyu Türkçe olarak yazın
    2. Örnek sorgular:
        - "Yıllara göre satışların grafiğini göster"
        - "Aylık satış analizi yap"
        - "Kategorilere göre satışları analiz et"
    3. Grafik ayarları:
        - X ve Y eksenleri için sütun seçin
        - İstediğiniz grafik türünü seçin
    """)
    
    if st.button("Örnek Veritabanını Yeniden Oluştur"):
        create_sample_db(DB_PATH)
        st.success("Örnek veritabanı yeniden oluşturuldu!")