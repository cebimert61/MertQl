class QueryGenerator:
    def __init__(self):
        pass

    def extract_limit(self, text_query):
        """
        Metinden LIMIT değerini çıkarır
        """
        text_query = text_query.lower()
        limit = None
        
        # Sayı ve anahtar kelime kombinasyonlarını kontrol et
        import re
        number_words = {
            'bir': 1, 'iki': 2, 'üç': 3, 'dört': 4, 'beş': 5,
            'altı': 6, 'yedi': 7, 'sekiz': 8, 'dokuz': 9, 'on': 10,
            'onbeş': 15, 'yirmi': 20, 'otuz': 30, 'kırk': 40, 'elli': 50
        }
        
        # Önce sayısal değerleri kontrol et
        numbers = re.findall(r'ilk (\d+)', text_query)
        if numbers:
            limit = int(numbers[0])
        else:
            # Yazı ile yazılmış sayıları kontrol et
            for word, num in number_words.items():
                if f'ilk {word}' in text_query:
                    limit = num
                    break
        
        return limit

    def generate_sql(self, text_query):
        """
        Türkçe metni SQL sorgusuna çevirir
        """
        # LIMIT değerini çıkar
        limit = self.extract_limit(text_query)
        top_clause = f"TOP {limit}" if limit else ""
        
        # Temel sorgu şablonları
        templates = {
            "yıllara göre": """
                SELECT {top}
                    YEAR(OrderDate) as yil, 
                    SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as toplam_satis
                FROM dbo.[Order Details] od
                JOIN dbo.Orders o ON od.OrderID = o.OrderID
                GROUP BY YEAR(OrderDate)
                ORDER BY yil
            """,
            "aylara göre": """
                SELECT {top}
                    CONVERT(varchar(7), OrderDate, 120) as ay,
                    SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as toplam_satis
                FROM dbo.[Order Details] od
                JOIN dbo.Orders o ON od.OrderID = o.OrderID
                GROUP BY CONVERT(varchar(7), OrderDate, 120)
                ORDER BY ay
            """,
            "kategorilere göre": """
                SELECT {top}
                    c.CategoryName as kategori, 
                    SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as toplam_satis,
                    COUNT(DISTINCT o.OrderID) as siparis_sayisi
                FROM dbo.[Order Details] od
                JOIN dbo.Orders o ON od.OrderID = o.OrderID
                JOIN dbo.Products p ON od.ProductID = p.ProductID
                JOIN dbo.Categories c ON p.CategoryID = c.CategoryID
                GROUP BY c.CategoryName
                ORDER BY toplam_satis DESC
            """,
            "ülkelere göre": """
                SELECT {top}
                    o.ShipCountry as ulke,
                    SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as toplam_satis,
                    COUNT(DISTINCT o.OrderID) as siparis_sayisi,
                    COUNT(DISTINCT c.CustomerID) as musteri_sayisi
                FROM dbo.[Order Details] od
                JOIN dbo.Orders o ON od.OrderID = o.OrderID
                JOIN dbo.Customers c ON o.CustomerID = c.CustomerID
                GROUP BY o.ShipCountry
                ORDER BY toplam_satis DESC
            """,
            "çalışanlara göre": """
                SELECT {top}
                    e.FirstName + ' ' + e.LastName as calisan,
                    e.Title as unvan,
                    COUNT(DISTINCT o.OrderID) as siparis_sayisi,
                    COUNT(DISTINCT c.CustomerID) as musteri_sayisi,
                    SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as toplam_satis
                FROM dbo.[Order Details] od
                JOIN dbo.Orders o ON od.OrderID = o.OrderID
                JOIN dbo.Employees e ON o.EmployeeID = e.EmployeeID
                JOIN dbo.Customers c ON o.CustomerID = c.CustomerID
                GROUP BY e.FirstName, e.LastName, e.Title
                ORDER BY toplam_satis DESC
            """,
            "ürünlere göre": """
                SELECT {top}
                    p.ProductName as urun,
                    c.CategoryName as kategori,
                    SUM(od.Quantity) as satilan_adet,
                    SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as toplam_satis
                FROM dbo.[Order Details] od
                JOIN dbo.Products p ON od.ProductID = p.ProductID
                JOIN dbo.Categories c ON p.CategoryID = c.CategoryID
                GROUP BY p.ProductName, c.CategoryName
                ORDER BY toplam_satis DESC
            """
        }
        
        # Basit anahtar kelime eşleştirmesi
        text_query = text_query.lower()
        for key in templates:
            if key in text_query:
                return templates[key].format(top=top_clause)
                
        # Özel durumlar
        if "çalışan" in text_query or "personel" in text_query:
            return templates["çalışanlara göre"].format(top=top_clause)
        elif "ülke" in text_query:
            return templates["ülkelere göre"].format(top=top_clause)
        elif "ürün" in text_query or "mamül" in text_query:
            return templates["ürünlere göre"].format(top=top_clause)
                
        # Varsayılan sorgu
        return templates["yıllara göre"].format(top=top_clause)
