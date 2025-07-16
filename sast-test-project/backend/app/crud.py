from flask import Blueprint, request, jsonify
from . import db
from .models import User, Document
import boto3
from config import Config
import os

crud_bp = Blueprint('crud', __name__)

s3 = boto3.client(
    's3',
    endpoint_url=Config.S3_ENDPOINT,
    aws_access_key_id=Config.S3_ACCESS_KEY,
    aws_secret_access_key=Config.S3_SECRET_KEY
)

# УЯЗВИМОСТЬ: SQL-инъекция
@crud_bp.route('/user/<username>', methods=['GET'])
def get_user(username):
    query = f"SELECT * FROM user WHERE username = '{username}'"
    result = db.engine.execute(query)
    user = result.fetchone()
    
    if user:
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })
    else:
        return jsonify({"error": "User not found"}), 404

# УЯЗВИМОСТЬ: Небезопасная загрузка файлов
@crud_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # УЯЗВИМОСТЬ: Не проверяется тип файла
    s3_path = f"uploads/{file.filename}"
    s3.upload_fileobj(file, Config.S3_BUCKET, s3_path)
    
    # УЯЗВИМОСТЬ: Нет проверки авторизации
    new_doc = Document(name=file.filename, s3_path=s3_path, owner_id=1)
    db.session.add(new_doc)
    db.session.commit()
    
    return jsonify({"status": "success", "path": s3_path})

# УЯЗВИМОСТЬ: IDOR (Insecure Direct Object Reference)
@crud_bp.route('/document/<int:doc_id>', methods=['GET'])
def get_document(doc_id):
    doc = Document.query.get(doc_id)
    if doc:
        # УЯЗВИМОСТЬ: Нет проверки прав доступа
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': Config.S3_BUCKET, 'Key': doc.s3_path},
            ExpiresIn=3600
        )
        return jsonify({"url": url})
    else:
        return jsonify({"error": "Document not found"}), 404
    
# False Positive: Выглядит как SQL-инъекция, но на самом деле безопасно
@crud_bp.route('/safe_query', methods=['GET'])
def safe_query():
    table_name = request.args.get('table')
    
    # Это безопасно, хотя выглядит подозрительно
    if table_name not in ['users', 'documents']:  # Белый список таблиц
        return jsonify({"error": "Invalid table"}), 400
        
    # False Positive: SAST может ошибочно детектировать SQL-инъекцию
    query = f"SELECT * FROM {table_name} LIMIT 10"  # На самом деле безопасно
    result = db.engine.execute(query)
    return jsonify({"data": [dict(row) for row in result]})

# False Positive: Выглядит как path traversal
@crud_bp.route('/safe_file', methods=['GET'])
def safe_file():
    filename = request.args.get('file')
    
    # Это безопасно, так как путь жестко задан
    if filename != "allowed.txt":
        return jsonify({"error": "Invalid file"}), 400
        
    # False Positive: SAST может ошибочно детектировать traversal
    with open(f"/safe_dir/{filename}") as f:  # На самом деле безопасно
        return f.read(), 200, {'Content-Type': 'text/plain'}