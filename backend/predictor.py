import pickle
import os
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from django.conf import settings

nepali_stopwords = set(stopwords.words('nepali'))
english_stopwords = set(stopwords.words('english'))

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove specified characters
    text = re.sub('[#\\/।(),०-९<<?!,—–’‘:\u200d]', '', text)
    # Strip double quotes
    text = text.strip('"')

    # Tokenize the text
    words=word_tokenize(text)
    # Remove stop words for both Nepali and English
    filtered_words = [word for word in words if word.lower() not in nepali_stopwords and word.lower() not in english_stopwords]
    # Join the filtered words to form the processed text
    processed_text = ' '.join(filtered_words)
    return processed_text


# Load the trained model
model_path = os.path.join(settings.BASE_DIR, 'backend/random_forest.pkl')
with open(model_path, 'rb') as model_file:
    clf = pickle.load(model_file)


def make_prediction(text):
    # Preprocess the text if needed
    preprocessed_text = preprocess_text(text)

    # Make predictions
    prediction = clf.predict([preprocessed_text])

    return prediction[0]
