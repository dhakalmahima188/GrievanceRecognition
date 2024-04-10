import pickle
import os
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from django.conf import settings
import numpy as np
from gensim.models import Word2Vec
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer,TrainingArguments,Trainer

nepali_stopwords = set(stopwords.words("nepali"))
english_stopwords = set(stopwords.words("english"))

print("Loading model")

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

# model_id = "nadika/nepali_gov_complaints_classification2"  # replace with your model's repository name
model_id = "nadika/nepali_complaints_classification_muril3" 
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)

def preprocess_and_tokenize(text):
    # Assuming the `preprocess_text` is your text cleaning and preprocessing function
    # Make sure to include the preprocess_text function or adjust this part accordingly
    processed_text = preprocess_text(text)  # Use your preprocessing here
    encoded_input = tokenizer(processed_text, padding=True, truncation=True, max_length=512, return_tensors="pt")
    return encoded_input

def make_prediction(text):
    # Preprocess and tokenize the text
    encoded_input = preprocess_and_tokenize(text)

    # Generate predictions
    with torch.no_grad():
        output = model(**encoded_input)

    # The output is logits; apply softmax to get probabilities
    probabilities = torch.nn.functional.softmax(output.logits, dim=-1)

    # Convert probabilities to numpy for easier handling
    probabilities = probabilities.detach().cpu().numpy()

    # Get the most likely class index
    predicted_class_idx = probabilities.argmax()

    # Decode the predicted class index to the class name using the model's config
    predicted_class = model.config.id2label[predicted_class_idx]
    return predicted_class, probabilities[0][predicted_class_idx]

# # Example text for prediction
# new_text = "मेरो घर मा पानि आएन "
# predicted_class, probability = make_prediction(new_text)
# print(f"Predicted Class: {predicted_class}, Probability: {probability}")
