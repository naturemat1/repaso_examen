import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
from datetime import datetime
import os
import logging as log

def save_csv(lista, output_path):
    """
    Guarda los datos extraídos en un archivo CSV.

    Parámetros:
    - lista (list): Lista de diccionarios con los datos a guardar (ej: [{'quote': '...', 'author': '...'}]).
    - output_path (str): Ruta del archivo CSV donde guardar los datos.
    """
    now = datetime.now().strftime("%Y-%m-%d")
    hour = datetime.now().strftime("%H:%M:%S")

    # Convertimos a DataFrame correctamente
    df = pd.DataFrame(lista)

    # Añadimos las columnas de fecha y hora
    df.insert(0, "fecha", now)
    df.insert(1, "hora", hour)

    # Guardamos como columnas verdaderas
    if os.path.exists(output_path):
        df.to_csv(output_path, mode="a", header=False, index=False)
    else:
        df.to_csv(output_path, index=False)

    log.info(f"Datos guardados en {output_path}")

class QuotesSpider(scrapy.Spider):
    # Nombre del spider
    name = "quotes"
    
    # URLs a scrapear
    start_urls = ["https://quotes.toscrape.com/"]
    
    def parse(self, response):
        """
        Método que procesa la respuesta HTML.
        Extrae títulos (quotes) de la página.
        """
        
        # Extraer al menos 5 elementos: los quotes/citas
        quotes = response.css("span.text::text").getall()
        
        # Extraer autores (elemento adicional del mismo tipo)
        authors = response.css("small.author::text").getall()
        
        # Mostrar datos por consola
        print("\n" + "="*60)
        print("CITAS EXTRAÍDAS:")
        print("="*60)
        
        for i, (quote, author) in enumerate(zip(quotes, authors), 1):
            print(f"\n{i}. {quote}")
            print(f"   {author}")
        
        print("\n" + "="*60)
        print(f"Total de citas extraídas: {len(quotes)}")
        print("="*60 + "\n")

        # Preparar datos para guardar en CSV
        trends = [{'quote': quote, 'author': author} for quote, author in zip(quotes, authors)]
        # Guardar en CSV
        save_csv(trends, 'quotes.csv')


# Configuración del scraper
process = CrawlerProcess({
    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})

# Ejecutar el spider
process.crawl(QuotesSpider)
process.start()