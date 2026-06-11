import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def scrape_url(url):
    """
    Scrapes content from a news URL.
    Returns a dictionary with 'title', 'text', 'domain', and 'error' (if any).
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        if not domain.startswith('www.'):
            domain_name = domain
        else:
            domain_name = domain[4:]
            
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted script, style, header, footer elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()
            
        # Get title
        title = ""
        if soup.title:
            title = soup.title.get_text().strip()
        elif soup.find('h1'):
            title = soup.find('h1').get_text().strip()
            
        # Get paragraphs
        paragraphs = []
        # Look for article or main tags first
        article_body = soup.find('article') or soup.find('main')
        if article_body:
            p_elements = article_body.find_all('p')
        else:
            p_elements = soup.find_all('p')
            
        for p in p_elements:
            text = p.get_text().strip()
            # Filter out short fragments (likely navigation links or ads)
            if len(text) > 30:
                paragraphs.append(text)
                
        full_text = "\n\n".join(paragraphs)
        
        if not full_text:
            return {
                'title': title,
                'text': '',
                'domain': domain_name,
                'error': 'No readable text content found on this webpage. Please try copy-pasting the text manually.'
            }
            
        return {
            'title': title,
            'text': full_text,
            'domain': domain_name,
            'error': None
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'title': '',
            'text': '',
            'domain': '',
            'error': f'Failed to scrape the webpage: {str(e)}'
        }
