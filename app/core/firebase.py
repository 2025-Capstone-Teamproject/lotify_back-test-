# # app/core/firebase.py
# import firebase_admin
# from firebase_admin import credentials, auth
# import os
# from app.core.config import settings

# cred_path = settings.FIREBASE_CREDENTIALS_PATH


# # Firebase 앱 초기화 (한 번만)
# if not firebase_admin._apps:
#     cred_path = os.path.join(os.getcwd(), "firebase_admin_key.json")
#     cred = credentials.Certificate(cred_path)
#     firebase_admin.initialize_app(cred)

# def verify_token(id_token: str):
#     try:
#         decoded_token = auth.verify_id_token(id_token)
#         return decoded_token
#     except Exception as e:
#         print(f"Token verification failed: {e}")
#         return None
