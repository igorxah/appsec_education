from flask import Blueprint, request, jsonify
import requests
from config import Config
import pickle
import json

discord_bp = Blueprint('discord', __name__)

# УЯЗВИМОСТЬ: Небезопасная десериализация
@discord_bp.route('/webhook', methods=['POST'])
def discord_webhook():
    data = request.data
    
    # УЯЗВИМОСТЬ: pickle небезопасен для десериализации
    try:
        payload = pickle.loads(data)
    except:
        payload = json.loads(data)
    
    # УЯЗВИМОСТЬ: SSRF потенциально возможен
    if 'callback_url' in payload:
        requests.get(payload['callback_url'])
    
    # Отправка в Discord
    headers = {
        "Authorization": f"Bot {Config.DISCORD_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        Config.DISCORD_WEBHOOK_URL,
        json={"content": str(payload)},
        headers=headers
    )
    
    return jsonify({"status": "success"})

# УЯЗВИМОСТЬ: Информация о сервере раскрывается
@discord_bp.route('/server_info', methods=['GET'])
def discord_server_info():
    headers = {
        "Authorization": f"Bot {Config.DISCORD_TOKEN}"
    }
    
    response = requests.get(
        "https://discord.com/api/v9/guilds/your_server_id",
        headers=headers
    )
    
    return jsonify(response.json())