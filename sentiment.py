from textblob import TextBlob

# Basic sentiment keyword maps for Hindi and Marathi to help when TextBlob is used on transliterated/local texts
HINDI_POSITIVE = ['अच्छा', 'सुंदर', 'बेहतर', 'खुश', 'सफल', 'जीत', 'महान', 'शानदार', 'सच्चा', 'ईमानदार']
HINDI_NEGATIVE = ['बुरा', 'खराब', 'दुखी', 'असफल', 'हार', 'गलत', 'झूठ', 'धोखा', 'भ्रष्ट', 'खतरनाक']

MARATHI_POSITIVE = ['चांगला', 'सुंदर', 'उत्तम', 'आनंदी', 'यशस्वी', 'विजय', 'महान', 'खरे', 'प्रामाणिक']
MARATHI_NEGATIVE = ['वाईट', 'खराब', 'दुःखी', 'अपयशी', 'पराभव', 'चुकीचे', 'खोटे', 'फसवणूक', 'धोकादायक']

def analyze_sentiment(text, lang='en'):
    """
    Analyzes sentiment of text.
    Returns: 'Positive', 'Negative', or 'Neutral'
    """
    if not text or len(text.strip()) == 0:
        return 'Neutral'
        
    try:
        # Check specific language local keywords first
        if lang == 'hi':
            pos_count = sum(1 for w in HINDI_POSITIVE if w in text)
            neg_count = sum(1 for w in HINDI_NEGATIVE if w in text)
            if pos_count > neg_count:
                return 'Positive'
            elif neg_count > pos_count:
                return 'Negative'
                
        elif lang == 'mr':
            pos_count = sum(1 for w in MARATHI_POSITIVE if w in text)
            neg_count = sum(1 for w in MARATHI_NEGATIVE if w in text)
            if pos_count > neg_count:
                return 'Positive'
            elif neg_count > pos_count:
                return 'Negative'
                
        # Fallback to TextBlob polarity score
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            return 'Positive'
        elif polarity < -0.1:
            return 'Negative'
        else:
            return 'Neutral'
            
    except Exception:
        return 'Neutral'
