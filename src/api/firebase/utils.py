import firebase_admin
import os
from firebase_admin import credentials, firestore

cred = credentials.Certificate(f"{os.getcwd()}/freelance-f82f0-firebase-adminsdk-fbsvc-fa13706488.json")
firebase_admin.initialize_app(cred)

db = firestore.client()