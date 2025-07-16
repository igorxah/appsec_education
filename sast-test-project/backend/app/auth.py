from flask import Blueprint, request, session, jsonify
from . import db
from .models import User
import hashlib

auth_bp = Blueprint('auth', __name__)

# УЯЗВИМОСТЬ: Небезопасная аутентификация
@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # УЯЗВИМОСТЬ: Слабый хеш (MD5)
    password_hash = hashlib.md5(password.encode()).hexdigest()
    
    # УЯЗВИМОСТЬ: SQL-инъекция возможна
    query = f"SELECT * FROM user WHERE username = '{username}' AND password_hash = '{password_hash}'"
    result = db.engine.execute(query)
    user = result.fetchone()
    
    if user:
        session['user_id'] = user.id
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "failure"}), 401

# УЯЗВИМОСТЬ: CSRF - нет защиты
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"status": "success"})

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    # УЯЗВИМОСТЬ: Нет валидации ввода
    # УЯЗВИМОСТЬ: Слабый хеш
    password_hash = hashlib.md5(password.encode()).hexdigest()
    
    new_user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"status": "success"})