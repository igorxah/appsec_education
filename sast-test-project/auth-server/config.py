import os

# УЯЗВИМОСТЬ: Hardcoded секреты
class Config:
    SECRET_KEY = "oauth_secret_key_12345"  # Должно быть в .env
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL', 'postgresql://postgres:postgres@localhost:5432/sast_test_db')
    
    # OAuth2 конфигурация
    OAUTH2_REFRESH_TOKEN_GENERATOR = True
    OAUTH2_TOKEN_EXPIRES_IN = {
        'authorization_code': 864000,
        'implicit': 3600,
        'password': 864000,
        'client_credentials': 864000
    }
    
    # УЯЗВИМОСТЬ: Небезопасные клиенты
    OAUTH2_CLIENTS = {
        "test_client": {
            "client_id": "test_client",
            "client_secret": "test_secret",  # Должно быть в .env
            "redirect_uris": ["http://localhost:3000/callback"],
            "scope": "profile email",
            "grant_types": ["authorization_code", "password", "refresh_token"],
            "response_types": ["code"]
        }
    }