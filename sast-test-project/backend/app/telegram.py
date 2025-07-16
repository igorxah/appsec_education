from flask import Blueprint, request, jsonify
import requests
from config import Config

telegram_bp = Blueprint('telegram', __name__)

# УЯЗВИМОСТЬ: Нет ограничения частоты запросов
@telegram_bp.route('/send_message', methods=['POST'])
def send_telegram_message():
    message = request.json.get('message', '')
    chat_id = request.json.get('chat_id', Config.TELEGRAM_CHAT_ID)
    
    # УЯЗВИМОСТЬ: XSS в сообщении
    url = f"https://api.telegram.org/bot{Config.TELEGRAM_TOKEN}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"  # УЯЗВИМОСТЬ: Позволяет HTML/JS инъекции
    }
    
    response = requests.post(url, json=params)
    return jsonify(response.json())

# УЯЗВИМОСТЬ: Раскрытие информации о боте
@telegram_bp.route('/bot_info', methods=['GET'])
def get_bot_info():
    url = f"https://api.telegram.org/bot{Config.TELEGRAM_TOKEN}/getMe"
    response = requests.get(url)
    return jsonify(response.json())