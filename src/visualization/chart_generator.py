import plotly.express as px
import plotly.graph_objects as go

class ChartGenerator:
    @staticmethod
    def create_chart(df, x_column, y_column, chart_type='line', title='Satış Analizi'):
        """
        DataFrame'den seçilen türde grafik oluşturur
        """
        if chart_type == 'line':
            fig = px.line(df, x=x_column, y=y_column,
                         title=title,
                         labels={x_column: x_column.capitalize(), 
                                y_column: y_column.capitalize()})
        
        elif chart_type == 'bar':
            fig = px.bar(df, x=x_column, y=y_column,
                        title=title,
                        labels={x_column: x_column.capitalize(), 
                               y_column: y_column.capitalize()})
        
        elif chart_type == 'scatter':
            fig = px.scatter(df, x=x_column, y=y_column,
                           title=title,
                           labels={x_column: x_column.capitalize(), 
                                  y_column: y_column.capitalize()})
        
        elif chart_type == 'area':
            fig = px.area(df, x=x_column, y=y_column,
                         title=title,
                         labels={x_column: x_column.capitalize(), 
                                y_column: y_column.capitalize()})
        
        elif chart_type == 'pie' and len(df) > 0:
            fig = px.pie(df, values=y_column, names=x_column,
                        title=title)
        
        else:
            raise ValueError(f"Desteklenmeyen grafik türü: {chart_type}")

        # Grafik stilini özelleştir
        fig.update_layout(
            template='plotly_white',
            title_x=0.5,
            title_font_size=20,
            showlegend=True
        )
        
        return fig
