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