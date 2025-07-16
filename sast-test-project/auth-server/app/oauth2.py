from flask import Blueprint, request, jsonify, redirect, session
from authlib.integrations.flask_client import OAuthError
from . import db, oauth
from .models import User
from config import Config
import hashlib
import jwt

oauth2_bp = Blueprint('oauth2', __name__)

# УЯЗВИМОСТЬ: Небезопасная реализация OAuth2
@oauth2_bp.route('/authorize', methods=['GET'])
def authorize():
    client_id = request.args.get('client_id')
    redirect_uri = request.args.get('redirect_uri')
    
    # УЯЗВИМОСТЬ: Нет proper validation client_id и redirect_uri
    if client_id not in Config.OAUTH2_CLIENTS:
        return jsonify({"error": "invalid_client"}), 400
    
    # УЯЗВИМОСТЬ: Состояние не проверяется
    session['oauth_client_id'] = client_id
    session['oauth_redirect_uri'] = redirect_uri
    
    return redirect('/login')

@oauth2_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # УЯЗВИМОСТЬ: Слабый хеш
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        user = User.query.filter_by(
            username=username,
            password_hash=password_hash
        ).first()
        
        if user:
            session['user_id'] = user.id
            return redirect('/approve')
        else:
            return "Invalid credentials", 401
    
    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Username">
            <input type="password" name="password" placeholder="Password">
            <button type="submit">Login</button>
        </form>
    '''

@oauth2_bp.route('/approve', methods=['GET', 'POST'])
def approve():
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        # УЯЗВИМОСТЬ: Нет реальной проверки scope
        client_id = session['oauth_client_id']
        redirect_uri = session['oauth_redirect_uri']
        
        # УЯЗВИМОСТЬ: Небезопасная генерация кода
        auth_code = hashlib.md5(f"{client_id}{session['user_id']}".encode()).hexdigest()
        
        return redirect(f"{redirect_uri}?code={auth_code}")
    
    return '''
        <form method="post">
            <p>Approve access?</p>
            <button type="submit">Approve</button>
        </form>
    '''

@oauth2_bp.route('/token', methods=['POST'])
def issue_token():
    grant_type = request.form.get('grant_type')
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    code = request.form.get('code')
    
    # УЯЗВИМОСТЬ: Слабая проверка клиента
    if client_id not in Config.OAUTH2_CLIENTS:
        return jsonify({"error": "invalid_client"}), 400
    
    if Config.OAUTH2_CLIENTS[client_id]['client_secret'] != client_secret:
        return jsonify({"error": "invalid_client"}), 400
    
    # УЯЗВИМОСТЬ: Небезопасная проверка кода
    if grant_type == 'authorization_code' and code:
        # УЯЗВИМОСТЬ: Токен содержит user_id
        access_token = f"access_{client_id}_{code}"
        refresh_token = f"refresh_{client_id}_{code}"
        
        return jsonify({
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": refresh_token
        })
    
    return jsonify({"error": "unsupported_grant_type"}), 400

@oauth2_bp.route('/userinfo', methods=['GET'])
def userinfo():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "invalid_token"}), 401
    
    # УЯЗВИМОСТЬ: Слабая проверка токена
    token = auth_header[7:]
    if not token.startswith('access_'):
        return jsonify({"error": "invalid_token"}), 401
    
    # УЯЗВИМОСТЬ: Раскрытие всей информации о пользователе
    _, client_id, code = token.split('_', 2)
    user_id = int(code[:10])  # УЯЗВИМОСТЬ: Небезопасное предположение
    
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "sub": user.id,
            "name": user.username,
            "email": user.email,
            "email_verified": True  # УЯЗВИМОСТЬ: Ложное утверждение
        })
    
    return jsonify({"error": "invalid_token"}), 401

# False Positive: Выглядит как небезопасная JWT-валидация
def validate_test_token(token):
    try:
        # Это тестовый токен с публичным ключом
        decoded = jwt.decode(
            token,
            key=Config.TEST_ONLY_PUBLIC_KEY,  # Публичный ключ из конфига
            algorithms=["RS256"]
        )
        return decoded
    except Exception as e:
        print(f"Token validation error: {e}")
        return None