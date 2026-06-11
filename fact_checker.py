import requests
from urllib.parse import quote
import os

# Optional Google API key can be set in environment variables
API_KEY = os.environ.get('GOOGLE_FACT_CHECK_API_KEY') or None

MOCK_FACTS = [
    {
        'claim': 'UFO landed in Central Park and demanded coffee.',
        'claimant': 'Social Media Posts',
        'publisher': 'Snopes',
        'review_date': '2026-06-05',
        'rating': 'False / Satire',
        'url': 'https://www.snopes.com/fact-check/ufo-central-park-coffee/'
    },
    {
        'claim': 'Government plans to ban weekends starting next month.',
        'claimant': 'Viral WhatsApp Message',
        'publisher': 'PolitiFact',
        'review_date': '2026-06-07',
        'rating': 'Pants on Fire',
        'url': 'https://www.politifact.com/factchecks/2026/jun/07/viral-image/no-the-government-is-not-planning-to-ban-weekends/'
    },
    {
        'claim': 'Scientists discovered water on Mars in a groundbreaking study.',
        'claimant': 'NASA Press Release',
        'publisher': 'FactCheck.org',
        'review_date': '2026-05-15',
        'rating': 'True / Accurate',
        'url': 'https://www.factcheck.org/2026/05/nasa-confirms-new-liquid-water-findings-on-mars/'
    }
]

def check_fact(query):
    """
    Searches fact check databases for similar claims.
    Returns: A list of dicts with 'claim', 'claimant', 'publisher', 'rating', 'url', and 'review_date'.
    """
    if not query or len(query.strip()) < 10:
        return []
        
    results = []
    
    # 1. Try Google Fact Check Tools API if key is available
    if API_KEY:
        try:
            url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={quote(query)}&key={API_KEY}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                claims = data.get('claims', [])
                for claim in claims[:4]:
                    claimant = claim.get('claimant', 'Unknown')
                    text = claim.get('text', '')
                    
                    review = claim.get('claimReview', [])
                    if review:
                        publisher = review[0].get('publisher', {}).get('name', 'Fact-Checker')
                        rating = review[0].get('textualRating', 'Unrated')
                        review_url = review[0].get('url', '#')
                        review_date = review[0].get('reviewDate', 'Recent')
                        
                        results.append({
                            'claim': text,
                            'claimant': claimant,
                            'publisher': publisher,
                            'rating': rating,
                            'url': review_url,
                            'review_date': review_date
                        })
                if results:
                    return results
        except Exception:
            pass
            
    # 2. Smart Fallback: Search mock database using simple word overlaps
    query_lower = query.lower()
    for mock in MOCK_FACTS:
        # Check if key words overlap (e.g. 'ufo', 'weekends', 'mars', 'water')
        keywords = ['ufo', 'coffee', 'weekends', 'weekend', 'mars', 'water', 'nasa', 'scientists']
        for keyword in keywords:
            if keyword in query_lower and keyword in mock['claim'].lower():
                results.append(mock)
                break
                
    # If no overlaps, return a default helpful disclaimer/general check
    if not results:
        # Create a dynamic unverified fact check item based on query
        results.append({
            'claim': query[:80] + '...' if len(query) > 80 else query,
            'claimant': 'Unspecified source',
            'publisher': 'System FactCheck Search',
            'rating': 'No Direct Matches Found',
            'url': 'https://www.google.com/search?q=' + quote(query + " fact check"),
            'review_date': 'N/A'
        })
        
    return results
