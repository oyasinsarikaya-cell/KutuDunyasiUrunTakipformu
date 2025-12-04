import os

class Config:
    SECRET_KEY = 'kutu_dunyasi_secret_key_2024'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///kutu_dunyasi_web.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'uploads'
    
    @staticmethod
    def init_app(app):
        # Klasörleri oluştur
        for folder in ['uploads', 'uretim_planlari']:
            os.makedirs(folder, exist_ok=True)