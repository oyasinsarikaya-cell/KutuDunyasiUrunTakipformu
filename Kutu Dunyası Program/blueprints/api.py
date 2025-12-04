from flask import Blueprint, jsonify, request, send_file
from datetime import datetime
from models.uretim_emri import db, UretimEmri
from utils.urun_katalog_loader import UrunKatalogYukleyici
from utils.pdf_generator import PDFGenerator
import pandas as pd
from io import BytesIO

# Blueprint'i oluştur
api_bp = Blueprint('api', __name__)

# Ürün katalog yükleyici
urun_yukleyici = UrunKatalogYukleyici()

# API Routes

@api_bp.route('/production-data')
def production_data():
    """Üretim verilerini JSON olarak döndür"""
    try:
        kayitlar = UretimEmri.query.order_by(UretimEmri.id.desc()).all()
        
        sonuc = []
        for kayit in kayitlar:
            sonuc.append({
                'id': kayit.id,
                'musteri_adi': kayit.musteri_adi,
                'urun_adi': kayit.urun_adi,
                'usiparis_miktari': kayit.usiparis_miktari,
                'tabaka_adedi': kayit.tabaka_adedi,
                'kagit_cinsi': kayit.kagit_cinsi,
                'gramaj': kayit.gramaj,
                'kagit_olcusu_1': kayit.kagit_olcusu_1,
                'kagit_olcusu_2': kayit.kagit_olcusu_2,
                'bicak_kodu': kayit.bicak_kodu,
                'bicak_olcusu_1': kayit.bicak_olcusu_1,
                'bicak_olcusu_2': kayit.bicak_olcusu_2,
                'renk_sayisi': kayit.renk_sayisi,
                'renk_bilgisi': kayit.renk_bilgisi,
                'verim': kayit.verim,
                'selefon_1': kayit.selefon_1,
                'selefon_2': kayit.selefon_2,
                'varak_yaldiz': kayit.varak_yaldiz,
                'gofre': kayit.gofre,
                'yapistirma': kayit.yapistirma,
                'paketleme': kayit.paketleme,
                'siparis_durumu': kayit.siparis_durumu,
                'notlar': kayit.notlar,
                'baski_adedi': kayit.baski_adedi,
                'selefon_adedi': kayit.selefon_adedi,
                'kesim_adedi': kayit.kesim_adedi,
                'karton_agirligi': kayit.karton_agirligi,
                'tarih': kayit.tarih,
                'olusturma_tarihi': kayit.olusturma_tarihi.strftime("%Y-%m-%d %H:%M:%S") if kayit.olusturma_tarihi else ''
            })
        
        return jsonify(sonuc)
    
    except Exception as e:
        print(f"Production data hatası: {e}")
        return jsonify({'error': 'Veriler yüklenirken hata oluştu'}), 500

@api_bp.route('/production-add', methods=['POST'])
def production_add():
    """Yeni üretim kaydı ekle"""
    try:
        data = request.json
        
        if not data.get('musteri_adi', '').strip():
            return jsonify({'success': False, 'message': 'Müşteri adı zorunludur!'})
        
        # Tarih formatını düzelt
        tarih = data.get('tarih', '')
        if tarih:
            try:
                tarih_obj = datetime.strptime(tarih, "%Y-%m-%d")
                tarih = tarih_obj.strftime("%d.%m.%Y")
            except:
                tarih = datetime.now().strftime("%d.%m.%Y")
        
        yeni_kayit = UretimEmri(
            musteri_adi=data.get('musteri_adi', '').strip(),
            urun_adi=data.get('urun_adi', ''),
            usiparis_miktari=data.get('usiparis_miktari', ''),
            tabaka_adedi=data.get('tabaka_adedi', ''),
            kagit_cinsi=data.get('kagit_cinsi', ''),
            gramaj=data.get('gramaj', ''),
            kagit_olcusu_1=data.get('kagit_olcusu_1', ''),
            kagit_olcusu_2=data.get('kagit_olcusu_2', ''),
            bicak_kodu=data.get('bicak_kodu', ''),
            bicak_olcusu_1=data.get('bicak_olcusu_1', ''),
            bicak_olcusu_2=data.get('bicak_olcusu_2', ''),
            renk_sayisi=data.get('renk_sayisi', ''),
            renk_bilgisi=data.get('renk_bilgisi', ''),
            verim=data.get('verim', ''),
            selefon_1=data.get('selefon_1', ''),
            selefon_2=data.get('selefon_2', ''),
            varak_yaldiz=data.get('varak_yaldiz', 'YOK'),
            gofre=data.get('gofre', 'YOK'),
            yapistirma=data.get('yapistirma', 'YOK'),
            paketleme=data.get('paketleme', ''),
            siparis_durumu=data.get('siparis_durumu', 'YENİ'),
            notlar=data.get('notlar', ''),
            baski_adedi=data.get('baski_adedi', ''),
            selefon_adedi=data.get('selefon_adedi', ''),
            kesim_adedi=data.get('kesim_adedi', ''),
            karton_agirligi=data.get('karton_agirligi', ''),
            tarih=tarih
        )
        
        db.session.add(yeni_kayit)
        db.session.commit()
        
        print(f"Yeni üretim kaydı eklendi: {data.get('musteri_adi')}")
        return jsonify({'success': True, 'message': 'Kayıt başarıyla eklendi!'})
    
    except Exception as e:
        db.session.rollback()
        print(f"Üretim kaydı ekleme hatası: {e}")
        return jsonify({'success': False, 'message': f'Sistem hatası: {str(e)}'})

@api_bp.route('/production-update', methods=['POST'])
def production_update():
    """Üretim kaydını güncelle"""
    try:
        data = request.json
        record_id = data.get('id')
        
        if not record_id:
            return jsonify({'success': False, 'message': 'Kayıt ID gerekli!'})
        
        kayit = UretimEmri.query.get(record_id)
        if not kayit:
            return jsonify({'success': False, 'message': 'Kayıt bulunamadı!'})
        
        # Tarih formatını düzelt
        tarih = data.get('tarih', '')
        if tarih:
            try:
                tarih_obj = datetime.strptime(tarih, "%Y-%m-%d")
                kayit.tarih = tarih_obj.strftime("%d.%m.%Y")
            except:
                pass
        
        # Diğer alanları güncelle
        kayit.musteri_adi = data.get('musteri_adi', kayit.musteri_adi)
        kayit.urun_adi = data.get('urun_adi', kayit.urun_adi)
        kayit.usiparis_miktari = data.get('usiparis_miktari', kayit.usiparis_miktari)
        kayit.siparis_durumu = data.get('siparis_durumu', kayit.siparis_durumu)
        kayit.notlar = data.get('notlar', kayit.notlar)
        
        db.session.commit()
        
        print(f"Üretim kaydı güncellendi: ID {record_id}")
        return jsonify({'success': True, 'message': 'Kayıt başarıyla güncellendi!'})
    
    except Exception as e:
        db.session.rollback()
        print(f"Üretim kaydı güncelleme hatası: {e}")
        return jsonify({'success': False, 'message': f'Sistem hatası: {str(e)}'})

@api_bp.route('/production-update-cell', methods=['POST'])
def production_update_cell():
    """Tek bir hücreyi güncelle"""
    try:
        data = request.json
        record_id = data.get('id')
        field = data.get('field')
        value = data.get('value')
        
        if not record_id or not field:
            return jsonify({'success': False, 'message': 'Eksik parametre!'})
        
        kayit = UretimEmri.query.get(record_id)
        if not kayit:
            return jsonify({'success': False, 'message': 'Kayıt bulunamadı!'})
        
        # Alanı güncelle
        if hasattr(kayit, field):
            setattr(kayit, field, value)
            db.session.commit()
            print(f"Hücre güncellendi: ID {record_id}, {field} = {value}")
            return jsonify({'success': True, 'message': 'Güncellendi!'})
        else:
            return jsonify({'success': False, 'message': 'Geçersiz alan!'})
    
    except Exception as e:
        db.session.rollback()
        print(f"Hücre güncelleme hatası: {e}")
        return jsonify({'success': False, 'message': f'Sistem hatası: {str(e)}'})

@api_bp.route('/production-delete/<int:id>', methods=['DELETE'])
def production_delete(id):
    """Tek bir üretim kaydını sil"""
    try:
        kayit = UretimEmri.query.get_or_404(id)
        musteri_adi = kayit.musteri_adi
        db.session.delete(kayit)
        db.session.commit()
        
        print(f"Üretim kaydı silindi: {musteri_adi} (ID: {id})")
        return jsonify({'success': True, 'message': 'Kayıt silindi!'})
    
    except Exception as e:
        db.session.rollback()
        print(f"Üretim kaydı silme hatası: {e}")
        return jsonify({'success': False, 'message': f'Silme hatası: {str(e)}'})

@api_bp.route('/production-delete-batch', methods=['POST'])
def production_delete_batch():
    """Toplu kayıt silme"""
    try:
        data = request.json
        ids = data.get('ids', [])
        
        if not ids:
            return jsonify({'success': False, 'message': 'Silinecek kayıt seçilmedi!'})
        
        deleted_count = 0
        for record_id in ids:
            kayit = UretimEmri.query.get(record_id)
            if kayit:
                db.session.delete(kayit)
                deleted_count += 1
        
        db.session.commit()
        
        print(f"Toplu silme: {deleted_count} kayıt silindi")
        return jsonify({'success': True, 'message': f'{deleted_count} kayıt silindi!'})
    
    except Exception as e:
        db.session.rollback()
        print(f"Toplu silme hatası: {e}")
        return jsonify({'success': False, 'message': f'Silme hatası: {str(e)}'})

@api_bp.route('/production-export-excel')
def production_export_excel():
    """Üretim verilerini Excel olarak dışa aktar"""
    try:
        kayitlar = UretimEmri.query.order_by(UretimEmri.id.desc()).all()
        
        data = []
        for kayit in kayitlar:
            data.append({
                'ID': kayit.id,
                'Tarih': kayit.tarih,
                'Müşteri Adı': kayit.musteri_adi,
                'Ürün Adı': kayit.urun_adi,
                'Miktar': kayit.usiparis_miktari,
                'Bıçak Kodu': kayit.bicak_kodu,
                'Bıçak Ölçüsü': f"{kayit.bicak_olcusu_1 or ''} x {kayit.bicak_olcusu_2 or ''}",
                'Renk Sayısı': kayit.renk_sayisi,
                'Renk Bilgisi': kayit.renk_bilgisi,
                'Durum': kayit.siparis_durumu,
                'Kağıt Cinsi': kayit.kagit_cinsi,
                'Gramaj': kayit.gramaj,
                'Kağıt Ölçüsü': f"{kayit.kagit_olcusu_1 or ''} x {kayit.kagit_olcusu_2 or ''}",
                'Selefon': f"{kayit.selefon_1 or ''} x {kayit.selefon_2 or ''}",
                'Varak Yaldız': kayit.varak_yaldiz,
                'Gofre': kayit.gofre,
                'Yapıştırma': kayit.yapistirma,
                'Paketleme': kayit.paketleme,
                'Baskı Adedi': kayit.baski_adedi,
                'Selefon Adedi': kayit.selefon_adedi,
                'Kesim Adedi': kayit.kesim_adedi,
                'Karton Ağırlığı': kayit.karton_agirligi,
                'Verim': kayit.verim,
                'Notlar': kayit.notlar,
                'Oluşturma Tarihi': kayit.olusturma_tarihi.strftime("%d.%m.%Y %H:%M") if kayit.olusturma_tarihi else ''
            })
        
        df = pd.DataFrame(data)
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Üretim Planlama')
            
            worksheet = writer.sheets['Üretim Planlama']
            
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'Uretim_Planlama_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx'
        )
    
    except Exception as e:
        print(f"Üretim Excel export hatası: {e}")
        return jsonify({'error': 'Excel export sırasında hata oluştu'}), 500

# Blueprint'i export et
__all__ = ['api_bp']
