from firebase_admin import credentials, firestore, initialize_app, storage

cred = credentials.Certificate('./website/db_config/serviceAccountKey.json')
default_app = initialize_app(cred, {
    'storageBucket': 'crypto-community-cb11a.appspot.com'
})
db = firestore.client()
ArrayUnion = firestore.ArrayUnion
bucket = storage.bucket()