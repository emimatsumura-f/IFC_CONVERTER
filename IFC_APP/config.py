import os

# プロジェクトのルートディレクトリパスを取得
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# インスタンス固有のデータを保存するディレクトリパス
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
# アップロードされたファイルの保存ディレクトリ
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
# SQLiteデータベースファイルのパス
DATABASE_PATH = os.path.join(INSTANCE_DIR, 'ifc_converter.db')

# 必要なディレクトリを自動作成（存在しない場合のみ）
os.makedirs(INSTANCE_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class Config:
    # 基本設定
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    
    # IFCファイルの設定
    IFC_UPLOAD_FOLDER = os.environ.get('IFC_UPLOAD_FOLDER') or os.path.join(BASE_DIR, '')
    
    # ログ設定
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'

    # データベース設定
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{DATABASE_PATH}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    # アップロード設定
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    UPLOAD_FOLDER = UPLOAD_FOLDER

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
    
    @classmethod
    def init_app(cls, app):
        # 本番環境では必ずSECRET_KEYを環境変数で設定すること
        if not os.environ.get('SECRET_KEY'):
            raise ValueError('Production environment requires SECRET_KEY to be set')
        
        # 本番環境では必要なディレクトリが存在することを確認
        required_dirs = [INSTANCE_DIR, UPLOAD_FOLDER]
        for directory in required_dirs:
            if not os.path.exists(directory):
                os.makedirs(directory)

# 環境変数に基づいて設定を選択
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}