import firebase_admin
from firebase_admin import credentials
import os
from firebase_admin.auth import verify_id_token

# firebaseConfig = {
#   'apiKey': "AIzaSyABhn7jQeke67WJrF9UmR--DI73EQ0CUX4",
#   'authDomain': "pricee-b2112.firebaseapp.com",
#   'projectId': "pricee-b2112",
#   'storageBucket': "pricee-b2112.appspot.com",
#   'messagingSenderId': "89726629063",
#   'appId': "1:89726629063:web:be82d77279b73d9b6d3ae2",
#   'measurementId': "G-3P4ST2LYZH"
# }

file = os.path.join(os.path.dirname(__file__), 'pricee-b2112-firebase-adminsdk-8tz94-b8e03ac9bc.json')
cred = credentials.Certificate(file)
firebase_admin.initialize_app(cred)


def decode_token(id_token):
  decoded_token = verify_id_token(id_token)
  return decoded_token

