from bs4 import BeautifulSoup
import requests

r = requests.get('https://arxiv.org/list/cs.CL/recent')

soup = BeautifulSoup(r.content, 'html.parser')

html_links = [
    'https://arxiv.org' + a_tag['href'] 
    for a_tag in soup.find_all('a', {'title': 'Abstract'})
]    

if html_links:
    print("Found HTML links:")
    for idx, link in enumerate(html_links, 1):
        print(f"{idx}. {link}")
        r_article = requests.get(link)
        soup_article = BeautifulSoup(r_article.content, 'html.parser')
        title = soup_article.find('h1', {'class': 'title mathjax'}).text.strip().replace('Title:', '').strip() if soup_article.find('h1', {'class': 'title mathjax'}) else None
        authors = soup_article.find('div', {'class': 'authors'}).text.strip().replace('Authors:', '').strip() if soup_article.find('div', {'class': 'authors'}) else None
        abstract = soup_article.find('blockquote', {'class': 'abstract mathjax'}).text.strip().replace('Abstract:', '').strip() if soup_article.find('blockquote', {'class': 'abstract mathjax'}) else None
        date = soup_article.find('div', {'class': 'dateline'}).text.strip() if soup_article.find('div', {'class': 'dateline'}) else None
        doi = soup_article.find('div', {'class': 'doi'}).text.strip() if soup_article.find('div', {'class': 'doi'}) else None
        section = 'cs.CL'
        html_title = title

        print("Extracted Title:", title)
        print("Extracted Authors:", authors)
        print("Extracted Abstract:", abstract)
        print("Extracted Date:", date)
        print("Extracted DOI:", doi)
        print("Extracted Section:", section)
        print("Extracted HTML_Title:", html_title)
        print("-" * 80)

else:
    print("No HTML links found")