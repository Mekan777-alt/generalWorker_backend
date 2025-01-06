import firebase_admin
import os
from firebase_admin import credentials, firestore

cred = credentials.Certificate(f"{os.getcwd()}/app-freelance-f3dee-firebase-adminsdk-8d92q-53823e41e1.json")
firebase_admin.initialize_app(cred)

db = firestore.client()