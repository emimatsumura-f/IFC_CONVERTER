#!/bin/bash

# 開発環境の環境変数を設定
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1
export SECRET_KEY="dev-secret-key"
export IFC_UPLOAD_FOLDER="../"
export LOG_LEVEL="DEBUG"

# Flaskアプリケーションを起動
flask run