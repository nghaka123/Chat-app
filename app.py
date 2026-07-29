import firebase_admin
from firebase_admin import credentials, firestore
import json, os

key_dict = json.loads(os.environ.get('FIREBASE_KEY'))
cred = credentials.Certificate(key_dict)
firebase_admin.initialize_app(cred)
db = firestore.client()
