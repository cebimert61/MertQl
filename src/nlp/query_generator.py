from transformers import pipeline

class QueryGenerator:
    def __init__(self):
        self.nlp = pipeline("text2text-generation", model="facebook/bart-large-cnn")

    def generate_sql(self, text_query):
        """
        Türkçe metni SQL sorgusuna çevirir
        """
        # Temel sorgu şablonları
        templates = {
            "yıllara göre": """
                SELECT strftime('%Y', sale_date) as yil, 
                       SUM(total_price) as toplam_satis
                FROM sales
                GROUP BY strftime('%Y', sale_date)
                ORDER BY yil
            """,
            "aylara göre": """
                SELECT strftime('%Y', sale_date) as yil,
                       strftime('%m', sale_date) as ay,
                       SUM(total_price) as toplam_satis
                FROM sales
                GROUP BY strftime('%Y', sale_date), strftime('%m', sale_date)
                ORDER BY yil, ay
            """,
            "kategorilere göre": """
                SELECT c.category_name,
                       SUM(s.total_price) as toplam_satis
                FROM sales s
                JOIN products p ON s.product_id = p.product_id
                JOIN categories c ON p.category_id = c.category_id
                GROUP BY c.category_name
                ORDER BY toplam_satis DESC
            """
        }

        # Basit bir kural tabanlı eşleştirme
        text_query = text_query.lower()
        
        if "yıl" in text_query:
            return templates["yıllara göre"]
        elif "ay" in text_query:
            return templates["aylara göre"]
        elif "kategori" in text_query:
            return templates["kategorilere göre"]
        
        # Varsayılan olarak yıllara göre analiz
        return templates["yıllara göre"]
