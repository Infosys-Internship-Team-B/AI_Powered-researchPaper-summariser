import firebase_admin
from firebase_admin import credentials, firestore
import os

# Check if Firebase is already initialized
if not firebase_admin._apps:
    # Path to your service account key
    cred = credentials.Certificate("firebase_key.json")
    
    # Initialize Firebase Admin SDK
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()