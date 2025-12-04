from flask import Blueprint, render_template, jsonify, request, send_file
from datetime import datetime
from models.uretim_emri import db, UretimEmri
from utils.urun_katalog_loader import UrunKatalogYukleyici
from utils.pdf_generator import PDFGenerator
import pandas as pd
from io import BytesIO

urun_takip_bp = Blueprint('urun_takip', __name__, url_prefix='/urun-takip')
urun_yukleyici = UrunKatalogYukleyici()
pdf_generator = PDFGenerator()

@urun_takip_bp.route('/')
def index():
    """Ürün Takip Formu sayfası"""
    bugun = datetime.now().strftime("%d.%m.%Y")
    return render_template('urun_takip.html', bugun=bugun)

@urun_takip_bp.route('/urun-ara')
def urun_ara():
    """Ürün adında arama yapar"""
    query = request.args.get('q', '').strip().lower()
    if not query or len(query) < 2:
        return jsonify([])
    
    tum_urunler = urun_yukleyici.tum_urun_listesi()
    sonuclar = [urun for urun in tum_urunler if query in urun.lower()]
    return jsonify(sonuclar[:10])

@urun_takip_bp.route('/urun-listesi')
def urun_listesi():
    """Tüm ürün listesini getirir"""
    tum_urunler = urun_yukleyici.tum_urun_listesi()
    return jsonify(tum_urunler)

@urun_takip_bp.route('/urun-bilgi')
def urun_bilgi():
    """Ürün adına göre bıçak kodu ve ebatlarını getirir"""
    urun_adi = request.args.get('urun_adi', '').strip()
    if not urun_adi:
        return jsonify({'success': False, 'message': 'Ürün adı gerekli'})
    
    bilgiler = urun_yukleyici.urun_bilgisi_getir(urun_adi)
    if bilgiler:
        return jsonify({
            'success': True,
            'bicak_kodu': bilgiler['bicak_kodu'],
            'en': bilgiler['en'],
            'boy': bilgiler['boy'],
            'urun_adi': bilgiler.get('urun_adi', urun_adi)
        })
    return jsonify({'success': False, 'message': 'Ürün katalogda bulunamadı'})

@urun_takip_bp.route('/save', methods=['POST'])
def save_record():
    """Kayıt kaydet"""
    data = request.json
    # ... kayıt işlemleri ...