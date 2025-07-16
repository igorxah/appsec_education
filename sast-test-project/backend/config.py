import os

# УЯЗВИМОСТЬ: Hardcoded секреты
class Config:
    SECRET_KEY = "my_very_secret_key_12345"  # Должно быть в .env
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL', 'postgresql://postgres:postgres@localhost:5432/sast_test_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # S3 конфигурация
    S3_ENDPOINT = os.getenv('S3_ENDPOINT', 'http://localhost:9000')
    S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY', 'minioadmin')  # Должно быть в .env
    S3_SECRET_KEY = os.getenv('S3_SECRET_KEY', 'minioadmin')  # Должно быть в .env
    S3_BUCKET = 'sast-test-bucket'

    # УЯЗВИМОСТЬ: Небезопасные CORS настройки
    CORS_ORIGINS = "*"
    
    # Discord интеграция
    DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', 'https://discord.com/api/webhooks/your_webhook')
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', 'your_discord_token')  # Должно быть в .env
    
    # Telegram интеграция
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'your_telegram_token')  # Должно быть в .env
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 'your_chat_id')