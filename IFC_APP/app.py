from flask import Flask, render_template, jsonify
import ifcopenshell
import os
import logging
from logging.handlers import RotatingFileHandler
from .config import config

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    
    # 設定の適用
    app.config.from_object(config[config_name])
    config[config_name].init_app(app) if hasattr(config[config_name], 'init_app') else None
    
    # ログ設定
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/ifc_converter.log',
                                         maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('IFC Converter startup')

    def extract_profile_information(element):
        """
        IFCの要素からプロファイル情報を抽出する
        
        Args:
            element: IFC要素（IFCBEAMまたはIFCCOLUMN）
            
        Returns:
            str: プロファイル名称（Description属性の値）
        """
        try:
            return element.Description
        except Exception as e:
            app.logger.error(f'Error extracting profile information: {str(e)}')
            return None

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/process_ifc/<filename>')
    def process_ifc(filename):
        try:
            file_path = os.path.join(app.config['IFC_UPLOAD_FOLDER'], filename)
            app.logger.info(f'Processing IFC file: {file_path}')
            
            if not os.path.exists(file_path):
                app.logger.error(f'File not found: {file_path}')
                raise FileNotFoundError(f'ファイルが見つかりません: {filename}')
            
            ifc_file = ifcopenshell.open(file_path)
            
            beams = ifc_file.by_type('IfcBeam')
            columns = ifc_file.by_type('IfcColumn')
            
            beam_profiles = []
            column_profiles = []
            
            for beam in beams:
                profile = extract_profile_information(beam)
                if profile:
                    beam_profiles.append(profile)
            
            for column in columns:
                profile = extract_profile_information(column)
                if profile:
                    column_profiles.append(profile)
            
            app.logger.info(f'Successfully processed {filename}')
            return jsonify({
                'status': 'success',
                'beams': beam_profiles,
                'columns': column_profiles
            })
        
        except FileNotFoundError as e:
            app.logger.error(str(e))
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 404
            
        except Exception as e:
            app.logger.error(f'Error processing {filename}: {str(e)}')
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    return app

# アプリケーションインスタンスの作成
app = create_app()

if __name__ == '__main__':
    app.run()