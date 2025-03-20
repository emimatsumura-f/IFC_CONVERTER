#!/bin/bash

# 本番環境の環境変数を設定
export FLASK_APP=app.py
export FLASK_ENV=production
export FLASK_DEBUG=0
export SECRET_KEY="your-secure-secret-key-here"  # 本番環境では必ず変更してください
export IFC_UPLOAD_FOLDER="/path/to/production/ifc/files"  # 本番環境のパスに変更してください
export LOG_LEVEL="INFO"

# Flaskアプリケーションを起動
flask run --host=0.0.0.0 --port=5000