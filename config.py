class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:ShrK.postgres@localhost/dhaniya_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key'  # Replace with a secure key
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size