from flask import Blueprint, render_template, jsonify, request, send_file
from datetime import datetime
from models.uretim_emri import db, UretimEmri
import pandas as pd
from io import BytesIO
import json
import os
import re

# BURAYA DİKKAT: Değişken ismi 'uretim_planlama_bp' olmalı
uretim_planlama_bp = Blueprint('uretim_planlama', __name__)

@uretim_planlama_bp.route('/')
def uretim_planlama_index():
    """Üretim Planlama sayfası"""
    try:
        return render_template('uretim_planlama.html')
    except Exception as e:
        print(f"Üretim planlama sayfası hatası: {e}")
        return "Sistem geçici olarak hizmet veremiyor", 500

@uretim_planlama_bp.route('/api/simple-production-data')
def simple_production_data():
    """Basit üretim verilerini JSON olarak döndür"""
    try:
        kayitlar = UretimEmri.query.order_by(UretimEmri.id.desc()).limit(100).all()
        
        sonuc = []
        for kayit in kayitlar:
            sonuc.append({
                'id': kayit.id,
                'musteri_adi': kayit.musteri_adi,
                'urun_adi': kayit.urun_adi,
                'tabaka_adedi': kayit.tabaka_adedi,
                'renk_sayisi': kayit.renk_sayisi,
                'renk_bilgisi': kayit.renk_bilgisi,
                'notlar': kayit.notlar
            })
        
        return jsonify(sonuc)
    
    except Exception as e:
        print(f"Simple production data hatası: {e}")
        return jsonify({'error': 'Veriler yüklenirken hata oluştu'}), 500

@uretim_planlama_bp.route('/api/get-selected-records', methods=['POST'])
def get_selected_records():
    """Seçilen kayıtları getir"""
    try:
        data = request.json
        ids = data.get('ids', [])
        
        if not ids:
            return jsonify([])
        
        ids = [int(id) for id in ids if str(id).isdigit()]
        
        kayitlar = UretimEmri.query.filter(UretimEmri.id.in_(ids)).all()
        
        sonuc = []
        for kayit in kayitlar:
            sonuc.append({
                'id': kayit.id,
                'musteri_adi': kayit.musteri_adi,
                'urun_adi': kayit.urun_adi,
                'tabaka_adedi': kayit.tabaka_adedi,
                'renk_sayisi': kayit.renk_sayisi,
                'renk_bilgisi': kayit.renk_bilgisi,
                'notlar': kayit.notlar
            })
        
        return jsonify(sonuc)
    
    except Exception as e:
        print(f"Get selected records hatası: {e}")
        return jsonify({'error': 'Kayıtlar getirilirken hata oluştu'}), 500

@uretim_planlama_bp.route('/api/save-production-plan', methods=['POST'])
def save_production_plan():
    """Üretim planını kaydet"""
    try:
        data = request.json
        plan_adi = data.get('plan_adi', '')
        veriler = data.get('veriler', [])
        
        if not plan_adi or not veriler:
            return jsonify({'success': False, 'message': 'Eksik veri!'})
        
        plan_data = {
            'plan_adi': plan_adi,
            'tarih': datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            'veriler': veriler
        }
        
        plan_folder = 'uretim_planlari'
        
        if not os.path.exists(plan_folder):
            os.makedirs(plan_folder)
            print(f"Klasör oluşturuldu: {plan_folder}")
        
        safe_plan_name = re.sub(r'[^\w\s-]', '', plan_adi)
        safe_plan_name = re.sub(r'[-\s]+', '_', safe_plan_name)
        
        filename = f"{plan_folder}/{safe_plan_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(plan_data, f, ensure_ascii=False, indent=2)
        
        print(f"Üretim planı kaydedildi: {plan_adi}")
        return jsonify({
            'success': True, 
            'message': 'Plan kaydedildi!', 
            'filename': filename
        })
    
    except Exception as e:
        print(f"Save production plan hatası: {e}")
        return jsonify({'success': False, 'message': f'Sistem hatası: {str(e)}'})

# Bu satır dosyanın sonunda olmalı
__all__ = ['uretim_planlama_bp']