import os
import re
import nltk
import pickle
import numpy as np
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# ── Auto-download NLTK data (needed on first run in cloud environments) ──────
for _pkg, _category in [('stopwords', 'corpora'), ('wordnet', 'corpora'),
                         ('punkt', 'tokenizers'), ('punkt_tab', 'tokenizers'),
                         ('omw-1.4', 'corpora')]:
    try:
        nltk.data.find(f'{_category}/{_pkg}')
    except LookupError:
        nltk.download(_pkg, quiet=True)

# ── App setup ────────────────────────────────────────────────────────────────
app = Flask(__name__, template_folder='./templates', static_folder='./static')

# ── Load pre-trained model & vectorizer ─────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
loaded_model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), 'rb'))
vector       = pickle.load(open(os.path.join(BASE_DIR, "vector.pkl"), 'rb'))

lemmatizer = WordNetLemmatizer()
stpwrds    = set(stopwords.words('english'))

# ── Prediction helper ────────────────────────────────────────────────────────
def fake_news_det(news):
    review = re.sub(r'[^a-zA-Z\s]', '', news).lower()
    tokens = nltk.word_tokenize(review)
    corpus = [lemmatizer.lemmatize(w) for w in tokens if w not in stpwrds]
    input_data = [' '.join(corpus)]
    vectorized_input_data = vector.transform(input_data)
    prediction = loaded_model.predict(vectorized_input_data)
    return prediction

# ── Routes ───────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        message = request.form['news']
        pred    = fake_news_det(message)
        if pred[0] == 1:
            result = "Prediction of the News :  Looking Fake News📰"
        else:
            result = "Prediction of the News : Looking Real News📰 "
        return render_template("prediction.html", prediction_text="{}".format(result))
    else:
        return render_template('prediction.html', prediction="Something went wrong")


if __name__ == '__main__':
    app.run(debug=False)