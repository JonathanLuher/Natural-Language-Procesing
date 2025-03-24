import requests
from bs4 import BeautifulSoup
import csv
import os
import re

def format_date(date_str):
    month_dict = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
        "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
        "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    }
    
    # Expresión regular para extraer año, mes y día
    date_pattern = re.compile(r"(\d{4})\s+([A-Za-z]{3})\s+(\d{1,2})")
    match = date_pattern.search(date_str)
    
    if match:
        year = match.group(1)
        month = month_dict.get(match.group(2), "00")
        day = match.group(3).zfill(2)
    else:
        year, month, day = "0000", "00", "00"
    
    return f"{day}/{month}/{year}"

def get_article_details(article_id):
    url = f"https://pubmed.ncbi.nlm.nih.gov/{article_id}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('h1', class_='heading-title').get_text(strip=True) if soup.find('h1', class_='heading-title') else 'No title'
    
    authors = soup.find('div', class_='authors-list')
    if authors:
        authors = ', '.join([author.get_text(strip=True) for author in authors.find_all('a', class_='full-name')])
    else:
        authors = 'No authors'
    
    abstract = soup.find('div', class_='abstract-content')
    if abstract:
        abstract = abstract.get_text(strip=True)
    else:
        abstract = 'No abstract'
    
    journal = soup.find('button', class_='journal-actions-trigger')
    if journal:
        journal = journal.get_text(strip=True)
    else:
        journal = 'No journal'
    
    date = soup.find('span', class_='cit')
    if date:
        date = format_date(date.get_text(strip=True))
    else:
        date = "00/00/0000"
    
    doi = soup.find('span', class_='identifier doi')
    if doi:
        doi = doi.get_text(strip=True).replace("DOI:", "").strip()  # Eliminar "DOI:" y espacios adicionales
    else:
        doi = 'No DOI'
    
    return [doi, title, authors, abstract, journal, date]

def save_to_csv(articles_data, folder="pubmed_articles", filename="pubmed_articles.csv"):
    # Crear la carpeta si no existe
    if not os.path.exists(folder):
        os.makedirs(folder)    
    filepath = os.path.join(folder, filename)
    
    # Guardar los datos en el archivo CSV
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["DOI", "Title", "Authors", "Abstract", "Journal", "Date"])
        writer.writerows(articles_data)

#Funcion para leer aticulos de la pagina
def get_pubmed_articles():
    base_url = "https://pubmed.ncbi.nlm.nih.gov/trending/"
    articles_data = []
    page = 1 
    max_articles = 300 

    while len(articles_data) < max_articles:
        url = f"{base_url}?page={page}" if page > 1 else base_url  # Construir la URL de la página
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = soup.find_all('div', class_='docsum-content')
        if not articles:
            break
        
        #Bucle de articulos en cada pagina
        for article in articles:
            if len(articles_data) >= max_articles:
                break
            article_id = article.find('a', class_='docsum-title')['href'].split('/')[-2]
            article_details = get_article_details(article_id)
            articles_data.append(article_details)
        page += 1

    save_to_csv(articles_data)
    
    return articles_data