# This file for enriching the dataset with semantic tags and embeddings
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer
import spacy

# Download NLTK resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('punkt_tab')

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
ENGLISH_STOP_WORDS = set(stopwords.words('english'))

# Preprocess text
def preprocess_text(text):
    text = text.lower()                             # Convert to lowercase
    text = re.sub(r'[^a-z\s]', '', text)            # Remove special characters and numbers
    text = re.sub(r'\s+', ' ', text).strip()        # Remove extra spaces

    # Remove stopwords
    words = text.split()
    words = [word for word in words if word not in ENGLISH_STOP_WORDS]

    return " ".join(words)

# Tokenize and lemmatize text
def tokenize_and_lemmatize(text):
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return " ".join(lemmatized_tokens)

# Load models
nlp = spacy.load("en_core_web_sm")
# load BERT model for semantic embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Extract semantic tags
def extract_semantic_tags(text):
    doc = nlp(text)
    return ", ".join([ent.label_ for ent in doc.ents])

# Generate embeddings
def generate_embeddings(text):
    return model.encode(text)

# Enrich dataset
def enrich_dataset(df):
    df['cleaned_descriptions'] = df['descriptions'].astype(str).apply(preprocess_text)
    df['lemmatized_descriptions'] = df['cleaned_descriptions'].apply(tokenize_and_lemmatize)
    df['semantic_tags'] = df['lemmatized_descriptions'].apply(extract_semantic_tags)
    df['embeddings'] = df['lemmatized_descriptions'].apply(generate_embeddings)
    return df