from bs4 import BeautifulSoup
import requests
import csv
import os
from datetime import datetime

def format_date(date_str):
    try:
        # Extraer la parte la fecha de los corchetes
        date_str = date_str.strip()
        if date_str.startswith("[") and date_str.endswith("]"):
            date_str = date_str[1:-1]  # Eliminar los corchetes
        if "Submitted on" in date_str:
            date_str = date_str.replace("Submitted on", "").strip()
        
        # Convertir la fecha al formato dd/mm/yyyy
        date_obj = datetime.strptime(date_str, "%d %b %Y")
        return date_obj.strftime("%d/%m/%Y")
    except ValueError:
        # Si solo hay un año o no hay datos, devolver "00/00/00"
        if len(date_str) == 4 and date_str.isdigit():
            return f"00/00/{date_str}"
        return "00/00/0000"

def get_arxiv_articles():
    sections = ['cs.CL', 'cs.CV']
    all_results = {"cs.CL": [], "cs.CV": []}
    
    for section in sections:
        url = f'https://arxiv.org/list/{section}/recent?skip=0&show=2000'
        
        # Realizar la solicitud GET
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Extraer enlaces a los artículos
        html_links = [
            'https://arxiv.org' + a_tag['href'] 
            for a_tag in soup.find_all('a', {'title': 'Abstract'})
        ][:150]  # Limitar a 150 artículos
        
        # Recorrer los enlaces y extraer la información
        for link in html_links:
            r_article = requests.get(link)
            soup_article = BeautifulSoup(r_article.content, 'html.parser')
            
            # Extraer los datos
            title = soup_article.find('h1', {'class': 'title mathjax'}).text.strip().replace('Title:', '').strip() if soup_article.find('h1', {'class': 'title mathjax'}) else "No title"        
            authors = soup_article.find('div', {'class': 'authors'}).text.strip().replace('Authors:', '').strip() if soup_article.find('div', {'class': 'authors'}) else "No authors"
            abstract = soup_article.find('blockquote', {'class': 'abstract mathjax'}).text.strip().replace('Abstract:', '').strip() if soup_article.find('blockquote', {'class': 'abstract mathjax'}) else "No abstract"
            date = soup_article.find('div', {'class': 'dateline'}).text.strip() if soup_article.find('div', {'class': 'dateline'}) else "No date"
            arxiv_id = link.split('/')[-1]  # Extraer el arXiv ID
            
            formatted_date = format_date(date)
            all_results[section].append([arxiv_id, title, authors, abstract, section, formatted_date])
        
        save_to_csv(all_results[section], f"arxiv_articles/{section}_articles.csv")
    return all_results

#Guardar datos en un csv
def save_to_csv(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["DOI", "Title", "Authors", "Abstract", "Section", "Date"])
        writer.writerows(data)