import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from joblib import dump, load

def preprocess_dataset():
    # Preprocess the dataset and save it as a CSV file
    data = pd.read_csv('raw_messages.csv')
    # ... preprocessing code ...
    data.to_csv('preprocessed_messages.csv', index=False)

def train_model():
    # Load the preprocessed dataset
    data = pd.read_csv('preprocessed_messages.csv')
    X = data['text']
    y = data['sentiment']
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X)

    # Train the model
    model = MultinomialNB()
    model.fit(X, y)

    # Save the trained model as a file
    dump(model, 'sentiment_classifier.joblib')

def classify_message(message_text):
    # Load the preprocessed dataset and trained model
    data = pd.read_csv('preprocessed_messages.csv')
    X = data['text']
    y = data['sentiment']
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X)
    model = load('sentiment_classifier.joblib')

    # Classify the message sentiment
    message_vector = vectorizer.transform([message_text])
    sentiment = model.predict(message_vector)[0]

    return sentiment
