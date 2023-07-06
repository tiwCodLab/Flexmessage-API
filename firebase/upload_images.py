import pyrebase


config = {
    "apiKey": "AIzaSyDx8mCmy_slvdo9gM4y16Veb0b6WP4aGoI",
    "authDomain": "flexmessage-image.firebaseapp.com",
    "projectId": "flexmessage-image",
    "storageBucket": "flexmessage-image.appspot.com",
    "messagingSenderId": "145273278045",
    "appId": "1:145273278045:web:e2e3042693206f79a847b4",
    "measurementId": "G-YVDLS56ZMY",
    "serviceAccount": "serviceAccount.json",
    "databaseURL": "https://flexmessage-image-default-rtdb.asia-southeast1.firebasedatabase.app/"

}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

# first write the filename you want to be displayed on database,
storage.child("photoss.jpg").put("photo.jpg")

file_url = storage.child("photoss.jpg").get_url(None)
print(file_url)
