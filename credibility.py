from app.models import db, SourceCredibility
from urllib.parse import urlparse

# Default credibility lists if database is not seeded
DEFAULT_CREDIBLE = {
    'reuters.com': (98, True, 'Reuters - International news agency'),
    'apnews.com': (97, True, 'Associated Press - Non-profit global news agency'),
    'bbc.co.uk': (95, True, 'BBC News - British public service broadcaster'),
    'bbc.com': (95, True, 'BBC News - British public service broadcaster'),
    'nytimes.com': (93, True, 'The New York Times - High reputation daily newspaper'),
    'bloomberg.com': (94, True, 'Bloomberg News - Business and financial news'),
    'wsj.com': (94, True, 'The Wall Street Journal - Business-focused daily newspaper'),
    'npr.org': (92, True, 'National Public Radio - American public radio network'),
    'politifact.com': (99, True, 'PolitiFact - Fact-checking project'),
    'snopes.com': (99, True, 'Snopes - Fact-checking website'),
    'factcheck.org': (99, True, 'FactCheck.org - Non-partisan fact-checking group'),
    'pressinstitute.in': (90, True, 'Press Institute of India'),
    'thehindu.com': (92, True, 'The Hindu - Reputable Indian daily newspaper'),
    'timesofindia.indiatimes.com': (85, True, 'Times of India - English-language daily newspaper'),
}

DEFAULT_SUSPICIOUS = {
    'theonion.com': (15, False, 'The Onion - Satirical news site'),
    'clickhole.com': (15, False, 'ClickHole - Satirical news website'),
    'naturalnews.com': (20, False, 'Natural News - Conspiracy and pseudo-science site'),
    'infowars.com': (10, False, 'InfoWars - Far-right conspiracy theory website'),
    'worldnewsdailyreport.com': (5, False, 'World News Daily Report - Fake news website'),
}

def get_source_credibility(url_or_domain):
    """
    Extracts domain from URL and looks up its credibility score and verification status.
    Returns: (trust_score, is_verified, description)
    """
    if not url_or_domain:
        return 50, False, 'Unknown domain (no URL provided)'
        
    domain = url_or_domain.strip().lower()
    
    # Extract domain if a full URL was provided
    if '/' in domain:
        try:
            parsed = urlparse(domain)
            domain = parsed.netloc.lower()
        except Exception:
            pass
            
    if domain.startswith('www.'):
        domain = domain[4:]
        
    # 1. Check database first
    try:
        record = SourceCredibility.query.filter_by(domain=domain).first()
        if record:
            return record.trust_score, record.is_verified, record.source_description or 'No description available'
    except Exception:
        # Fallback to defaults if DB is not ready/connected
        pass
        
    # 2. Check default list
    if domain in DEFAULT_CREDIBLE:
        score, verified, desc = DEFAULT_CREDIBLE[domain]
    elif domain in DEFAULT_SUSPICIOUS:
        score, verified, desc = DEFAULT_SUSPICIOUS[domain]
    else:
        # Neutral score for unknown domain
        score, verified, desc = 50, False, 'Unverified domain. Proceed with caution.'
        
    # 3. Add to database dynamically if possible
    try:
        new_record = SourceCredibility(
            domain=domain,
            trust_score=score,
            is_verified=verified,
            source_description=desc
        )
        db.session.add(new_record)
        db.session.commit()
    except Exception:
        # Silently fail if db is not initialized/locked
        if db.session:
            db.session.rollback()
            
    return score, verified, desc
