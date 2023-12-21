import pickle
import os
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from django.conf import settings
import numpy as np
from gensim.models import Word2Vec

nepali_stopwords = set(stopwords.words("nepali"))
english_stopwords = set(stopwords.words("english"))



def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove specified characters
    text = re.sub("[#\\/।(),०-९<<?!,—–’‘:\u200d]+", "", text)
    # Strip double quotes
    text = text.strip('"')

    # Tokenize the text
    words = word_tokenize(text)
    # Remove stop words for both Nepali and English
    filtered_words = [
        word
        for word in words
        if word.lower() not in nepali_stopwords
        and word.lower() not in english_stopwords
    ]
    # Join the filtered words to form the processed text
    processed_text = " ".join(filtered_words)
    return processed_text


# Load the trained model
model_path = os.path.join(settings.BASE_DIR, "backend/finalweb2vec.pkl")
with open(model_path, "rb") as model_file:
    clf = pickle.load(model_file)


word2vec_model_path = os.path.join(settings.BASE_DIR, "backend/nepaliW2V_5Million.model")
word2vec_model = Word2Vec.load(word2vec_model_path)

def text_to_vector(text):
    vector = np.zeros(200)
    count = 0
    for word in word_tokenize(text):
        if word in word2vec_model.wv:
            vector += word2vec_model.wv[word]
            count += 1
    if count != 0:
        vector /= count
    return vector

# mapping dictionary
mapping_category = {
    0: "लागु पदार्थ सम्बन्धी ",
    1: "प्राकृतिक श्रोत/साधन सम्बन्धी",
    2: "अर्थिक अनियमितता तथा भ्रष्टाचार सम्बन्धी ",
    3: "कर्मचारी सम्वन्धी ",
    4: "अर्थ सबन्धी ",
    5: "सोधपुछ, सुझाव, प्रशंसा सम्बन्धी",
    6: "सूचना तथा  संचार सम्बन्धी ",
    7: "सूचना तथा  संचार सम्बन्धी",
    8: "स्वास्थ्यसँग सम्बन्धी",
    9: "वेबसाइट तथा अभिलेख व्यवस्थापन सम्बन्धी ",
    10: "शान्ति सुरक्षा सम्बन्धी ",
    11: "खानेपानी सम्बन्धी ",
}

encoder_path = os.path.join(settings.BASE_DIR, "backend/labelencoder.pkl")   
# Load the Label Encoder
with open(encoder_path, 'rb') as encoder_file:
    label_encoder = pickle.load(encoder_file)


def make_prediction(text):
    # Preprocess the text if needed
    preprocessed_text = preprocess_text(text)
    test_text_vector=text_to_vector(preprocessed_text)

    # Make predictions
    prediction = clf.predict([test_text_vector])
    decoded_predictions = label_encoder.inverse_transform(prediction)

    print(prediction,decoded_predictions)
    return decoded_predictions
