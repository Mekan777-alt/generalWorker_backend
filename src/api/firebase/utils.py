import firebase_admin
import os
from firebase_admin import credentials, firestore

cred = credentials.Certificate(f"{os.getcwd()}/generaworker-firebase-adminsdk-49tht-8d334ad9df.json")
firebase_admin.initialize_app(cred)

db = firestore.client()