import streamlit as st
import os
import json
import random
import ssl
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Bypass SSL certificate verification for nltk downloads
ssl._create_default_https_context = ssl._create_unverified_context

# Download necessary nltk data
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

# Load intents JSON file
with open("intents.json", "r") as f:
    intents = json.load(f)["intents"]

# Prepare training data
training_sentences = []
training_labels = []
for intent in intents:
    for example in intent['examples']:
        training_sentences.append(example)
        training_labels.append(intent['intent'])

# Train the model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(training_sentences)
clf = LogisticRegression()
clf.fit(X, training_labels)

# Define the chatbot function
def chatbot(input_text):
    # Transform input and predict intent
    input_vector = vectorizer.transform([input_text])
    predicted_intent = clf.predict(input_vector)[0]

    # Search for the matching intent and return a random response
    for intent in intents:
        if intent['intent'] == predicted_intent:
            return random.choice(intent['responses'])

    # Fallback response if no intent is matched
    return "I'm sorry, I don't understand your question."

# Streamlit UI
st.title("Resume Builder Chatbot")
st.write("Ask me anything about building a great resume! 💼")

# User input
user_input = st.text_input("You:", "")

if user_input:
    # Generate chatbot response
    response = chatbot(user_input)
    st.text_area("Bot:", response, height=200)
