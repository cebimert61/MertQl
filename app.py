import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from src.nlp.query_generator import QueryGenerator
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go

# Sayfa yapılandırması
st.set_page_config(
    page_title="MertQL - Doğal Dil ile Veri Analizi",
    page_icon="📊",
    layout="wide"
)

# CSS stil tanımlamaları
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stApp {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #0066cc;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0052a3;
    }
    .loading {
        text-align: center;
        padding: 1rem;
        background-color: #e9ecef;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# SQL Server bağlantı bilgileri
SERVER = 'DESKTOP-R23C9G7\\MSSQLSERVER01'
DATABASE = 'Northwind'
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect=DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;TrustServerCertificate=yes"
engine = create_engine(DATABASE_URL)

# Ana başlık
st.title("📊 MertQL - Türkçe Veri Analizi")
st.markdown("---")

# Layout oluşturma
col1, col2 = st.columns([2, 1])

# Session state başlatma
if 'current_df' not in st.session_state:
    st.session_state.current_df = None
if 'x_col' not in st.session_state:
    st.session_state.x_col = None
if 'y_col' not in st.session_state:
    st.session_state.y_col = None
if 'chart_type' not in st.session_state:
    st.session_state.chart_type = "Çizgi Grafiği"

with col1:
    # Sorgu girişi
    st.subheader("🔍 Veri Analizi Sorgusu")
    user_input = st.text_area(
        "Sorgunuzu doğal dilde yazın (örn: 'En çok satış yapılan 5 ürünü göster')",
        height=100
    )
    
    # Sorgu çalıştırma
    if st.button("🚀 Analiz Et", use_container_width=True):
        if user_input:
            try:
                with st.spinner('🔄 Sorgu çalıştırılıyor...'):
                    # QueryGenerator ile SQL sorgusunu oluştur
                    query_gen = QueryGenerator()
                    sql_query = query_gen.generate_sql(user_input)
                    
                    # Sorguyu çalıştır
                    df = pd.read_sql(sql_query, engine)
                    st.session_state.current_df = df
                    
                    # İlk sütunları seç
                    if len(df.columns) >= 2:
                        st.session_state.x_col = df.columns[0]
                        st.session_state.y_col = df.columns[1]
                    
                    st.success("✅ Sorgu başarıyla çalıştırıldı!")
                
            except Exception as e:
                st.error(f"❌ Bir hata oluştu: {str(e)}")
        else:
            st.warning("⚠️ Lütfen bir sorgu girin.")
    
    # Eğer veri varsa göster
    if st.session_state.current_df is not None:
        df = st.session_state.current_df
        
        # Veri tablosu
        st.subheader("📋 Veri Tablosu")
        st.dataframe(df, use_container_width=True)
        
        # Grafik seçenekleri
        st.subheader("📈 Grafik Görünümü")
        
        if len(df.columns) >= 2:
            # Grafik türü seçimi
            st.session_state.chart_type = st.selectbox(
                "Grafik türünü seçin:",
                ["Çizgi Grafiği", "Sütun Grafiği", "Pasta Grafiği", "Alan Grafiği"],
                index=["Çizgi Grafiği", "Sütun Grafiği", "Pasta Grafiği", "Alan Grafiği"].index(st.session_state.chart_type)
            )
            
            # X ve Y ekseni seçimi (Pasta grafiği hariç)
            if st.session_state.chart_type != "Pasta Grafiği":
                st.session_state.x_col = st.selectbox(
                    "X ekseni için sütun seçin:", 
                    df.columns,
                    index=list(df.columns).index(st.session_state.x_col) if st.session_state.x_col in df.columns else 0
                )
                
                y_options = [col for col in df.columns if col != st.session_state.x_col]
                if st.session_state.y_col not in y_options and y_options:
                    st.session_state.y_col = y_options[0]
                
                st.session_state.y_col = st.selectbox(
                    "Y ekseni için sütun seçin:", 
                    y_options,
                    index=y_options.index(st.session_state.y_col) if st.session_state.y_col in y_options else 0
                )
            else:
                # Pasta grafiği için otomatik olarak ilk sayısal sütunu seç
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
                if len(numeric_cols) > 0:
                    st.session_state.y_col = numeric_cols[0]
                    st.session_state.x_col = df.columns[0] if df.columns[0] != st.session_state.y_col else df.columns[1]
            
            # Grafik yükleniyor mesajı
            with st.spinner('📊 Grafik hazırlanıyor...'):
                # Seçilen grafik türüne göre görselleştirme
                if st.session_state.chart_type == "Çizgi Grafiği":
                    fig = px.line(df, x=st.session_state.x_col, y=st.session_state.y_col, 
                                title=f"{st.session_state.y_col} - {st.session_state.x_col} İlişkisi")
                elif st.session_state.chart_type == "Sütun Grafiği":
                    fig = px.bar(df, x=st.session_state.x_col, y=st.session_state.y_col, 
                               title=f"{st.session_state.y_col} - {st.session_state.x_col} Dağılımı")
                elif st.session_state.chart_type == "Pasta Grafiği":
                    fig = px.pie(df, values=st.session_state.y_col, names=st.session_state.x_col, 
                               title=f"{st.session_state.y_col} Dağılımı")
                else:  # Alan Grafiği
                    fig = px.area(df, x=st.session_state.x_col, y=st.session_state.y_col, 
                                title=f"{st.session_state.y_col} - {st.session_state.x_col} Trendi")
                
                # Grafik stilini özelleştir
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(size=12)
                )
                
                # Grafiği göster
                st.plotly_chart(fig, use_container_width=True)
            
            # İndirme seçenekleri
            st.subheader("⬇️ Veriyi İndir")
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "CSV olarak indir",
                csv,
                "veri_analizi.csv",
                "text/csv",
                key='download-csv'
            )

with col2:
    st.subheader("📚 Nasıl Kullanılır?")
    st.markdown("""
    1. **Sorgu Yazma**
        - Doğal dilde sorgunuzu yazın
        - Türkçe karakterler kullanabilirsiniz
        - Detaylı sorgular için örnekleri inceleyin
        
    2. **Örnek Sorgular**
        - "En çok satış yapılan 5 ürünü göster"
        - "Aylık satış toplamlarını göster"
        - "Hangi kategoride kaç ürün var?"
        - "En yüksek cirolu müşteriler kimler?"
        
    3. **Grafik Özelleştirme**
        - İstediğiniz grafik türünü seçin
        - X ve Y eksenlerini belirleyin
        - Grafiği tam ekran yapabilirsiniz
        
    4. **Veri İndirme**
        - Analiz sonuçlarını CSV olarak indirin
        - Raporlarınızda kullanın
    """)
    
    # Bilgi kutusu
    st.info("""
    💡 **İpucu**: Daha iyi sonuçlar için:
    - Açık ve net sorular sorun
    - Tarih aralığı belirtin
    - Gruplamak istediğiniz alanları belirtin
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center'>
            <p>Developed by MertQL Team 🚀</p>
        </div>
    """, unsafe_allow_html=True)