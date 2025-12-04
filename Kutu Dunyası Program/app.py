import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from flask import Flask, render_template, send_from_directory
from config import Config
from models.uretim_emri import db
from blueprints.urun_takip import urun_takip_bp
from blueprints.uretim_planlama import uretim_planlama_bp
from blueprints.api import api_bp

# Logging kurulumu
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler('kutu_dunyasi.log', maxBytes=10000000, backupCount=5),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

# Uygulama oluşturma
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Veritabanını başlat
    db.init_app(app)
    
    # Blueprint'leri kaydet
    app.register_blueprint(urun_takip_bp)
    app.register_blueprint(uretim_planlama_bp)
    app.register_blueprint(api_bp)
    
    # Ana sayfa route'u
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Logo route'u
    @app.route('/logo')
    def logo():
        try:
            return send_from_directory('.', 'logo.jpg')
        except:
            return '', 404
    
    # Veritabanını başlat
    with app.app_context():
        db.create_all()
    
    return app

# Ana fonksiyon
if __name__ == '__main__':
    logger = setup_logging()
    app = create_app()
    
    try:
        logger.info("KUTU DÜNYASI Web Uygulaması başlatılıyor...")
        local_ip = "192.168.1.81"
        
        print("🎯 KUTU DÜNYASI Web Uygulaması")
        print("📍 Yerel erişim: http://localhost:5000")
        print("🌐 Ağ erişimi: http://192.168.1.81:5000")
        print("⏹️  Durdurmak için: Ctrl + C\n")
        
        app.run(
            debug=True,
            host='0.0.0.0', 
            port=5000,
            threaded=True
        )
    except Exception as e:
        logger.critical(f"Uygulama başlatma hatası: {e}")
        print(f"❌ KRİTİK HATA: {e}")
        sys.exit(1)
