from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate('./Crypto community/website/db_config/serviceAccountKey.json')
default_app = initialize_app(cred)
db = firestore.client()