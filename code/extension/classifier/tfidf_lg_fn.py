import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import re
from stop_words import STOP_WORDS
import joblib

def preprocess_text(text):

    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    words = text.split()
    filtered_words = [word for word in words if word not in STOP_WORDS]
    filtered_text = ' '.join(filtered_words)
    return filtered_text


def classifier():
    # Training and testing dataset
    train_df = pd.read_csv("data/combined.csv")
    test_df = pd.read_csv("data/validation_clean.csv")

    # Preprocessing
    train_df['text'] = train_df['text'].apply(preprocess_text)
    test_df['text'] = test_df['text'].apply(preprocess_text)

    # Get text and label
    train_text = train_df['text'].tolist()
    train_label = train_df['label'].tolist()

    test_text = test_df['text'].tolist()
    test_label = test_df['label'].tolist()

    # Vectorize the text
    vectorizer = TfidfVectorizer()
    train_text_tfidf = vectorizer.fit_transform(train_text)
    test_text_tfidf = vectorizer.transform(test_text)

    # Load the trained model
    model = joblib.load('trained_model_updated.pkl')
    
    df = pd.read_csv('shopee_comments.csv')
    df_copy = df.copy()

    predictions = []
    preprocessed_reviews = []

    for review in df['text']:
        preprocessed_review = preprocess_text(review)
        preprocessed_reviews.append(preprocessed_review)
        # Convert the review to TF-IDF representation
        review_tfidf = vectorizer.transform([preprocessed_review])
        # Predict sentiment
        prediction = model.predict(review_tfidf)
        predictions.append(prediction[0])

    df_copy['text'] = preprocessed_reviews
    df_copy['label'] = predictions
    df_copy.to_csv('shopee_comments_with_labels.csv', index=False)

    print("Predictions written to shopee_comments_with_labels.csv")

