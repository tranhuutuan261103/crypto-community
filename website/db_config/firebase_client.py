import pyrebase

# For Firebase JS SDK v7.20.0 and later, measurementId is optional
firebaseConfig = {
    'apiKey': "AIzaSyBLAMYhh06J4CRQ-IDpdn7EualpYMFuXwE",
    'databaseURL': 'https://crypto-community-cb11a-default-rtdb.firebaseio.com',
    'authDomain': "crypto-community-cb11a.firebaseapp.com",
    'projectId': "crypto-community-cb11a",
    'storageBucket': "crypto-community-cb11a.appspot.com",
    'messagingSenderId': "130645757916",
    'appId': "1:130645757916:web:c5194fb8d5544e48958919",
    'measurementId': "G-DS52DPENQS"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()