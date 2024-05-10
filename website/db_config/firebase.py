from firebase_admin import credentials, firestore, initialize_app, storage

cred = credentials.Certificate('./Crypto community/website/db_config/serviceAccountKey.json')
default_app = initialize_app(cred)
db = firestore.client()
ArrayUnion = firestore.ArrayUnion
bucket = storage.bucket(default_app.project_id)