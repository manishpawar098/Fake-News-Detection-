import re

KEYWORDS = {
    'Politics': [
        'government', 'president', 'election', 'congress', 'parliament', 'minister', 'senate', 
        'political', 'vote', 'party', 'democrat', 'republican', 'law', 'policy', 'pm', 'modi', 
        'bjp', 'congress', 'चुनाव', 'राजनीति', 'सरकार', 'मंत्री', 'खासदार', 'पक्ष', 'मतदार'
    ],
    'Sports': [
        'football', 'basketball', 'cricket', 'soccer', 'tennis', 'athlete', 'league', 
        'championship', 'game', 'match', 'coach', 'cup', 'olympics', 'score', 'runs', 'wickets', 
        'ipl', 'क्रिकेट', 'खेळ', 'सामना', 'धावा', 'खेळाडू', 'मैदान', 'स्पर्धा', 'खेल'
    ],
    'Technology': [
        'computer', 'software', 'apple', 'google', 'microsoft', 'technology', 'internet', 
        'ai', 'intelligence', 'device', 'database', 'cyber', 'data', 'tech', 'application', 
        'phone', 'mobile', 'संगणक', 'तंत्रज्ञान', 'इंटरनेट', 'मोबाईल', 'सॉफ्टवेअर', 'डेटा'
    ],
    'Health': [
        'doctor', 'patient', 'health', 'medical', 'cancer', 'disease', 'virus', 'hospital', 
        'drug', 'treatment', 'vaccine', 'medicine', 'clinical', 'fitness', 'covid', 
        'डॉक्टर', 'रुग्ण', 'आरोग्य', 'औषध', 'रुग्णालय', 'कर्करोग', 'लस', 'हॉस्पिटल'
    ],
    'Entertainment': [
        'movie', 'film', 'music', 'actor', 'singer', 'actress', 'hollywood', 'show', 'concert', 
        'award', 'theater', 'star', 'celebrity', 'bollywood', 'boxoffice', 
        'चित्रपट', 'चित्रपटगृह', 'गाणे', 'गायक', 'अभिनेता', 'अभिनेत्री', 'बॉलीवूड', 'शो'
    ],
    'Business': [
        'market', 'company', 'economy', 'stock', 'stocks', 'business', 'finance', 'revenue', 
        'profit', 'investment', 'bank', 'trade', 'price', 'sale', 'sales', 'billion', 'million', 
        'गुंतवणूक', 'व्यवसाय', 'बाजार', 'कंपनी', 'बँक', 'आर्थिक', 'शेअर', 'नफा'
    ]
}

def detect_category(text):
    """
    Categorizes the article text based on keyword counts.
    Returns: A string representing the category.
    """
    if not text:
        return 'General'
        
    text_lower = text.lower()
    scores = {cat: 0 for cat in KEYWORDS.keys()}
    
    for category, words in KEYWORDS.items():
        for word in words:
            # Match word with boundaries to avoid false positives (like 'cup' in 'occupy')
            # Using simple word boundaries for english, and direct inclusion for unicode
            if re.search(r'\b' + re.escape(word) + r'\b', text_lower) or (not word.isalnum() and word in text_lower):
                scores[category] += text_lower.count(word)
                
    max_score = 0
    best_category = 'General'
    
    for category, score in scores.items():
        if score > max_score:
            max_score = score
            best_category = category
            
    return best_category
