from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import mm
from io import BytesIO
from datetime import datetime
import os

class PDFGenerator:
    @staticmethod
    def turkce_duzelt(metin):
        """Türkçe karakterleri düzelt"""
        if not metin:
            return ""
        cevirme_tablosu = {
            'ı': 'i', 'İ': 'I', 'ğ': 'g', 'Ğ': 'G',
            'ü': 'u', 'Ü': 'U', 'ş': 's', 'Ş': 'S',
            'ö': 'o', 'Ö': 'O', 'ç': 'c', 'Ç': 'C'
        }
        for tr, en in cevirme_tablosu.items():
            metin = str(metin).replace(tr, en)
        return metin
    
    def generate(self, data, download=True):
        """PDF oluştur"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=5*mm,
            leftMargin=5*mm,
            topMargin=1*mm,
            bottomMargin=2*mm
        )
        story = self._create_story(data)
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _create_story(self, data):
        """PDF içeriğini oluştur"""
        story = []
        styles = getSampleStyleSheet()
        
        # Logo ekle
        self._add_logo(story)
        
        # Başlık ekle
        self._add_header(story, styles, data)
        
        # Tablo ekle
        self._add_table(story, styles, data)
        
        # Alt bilgi ekle
        self._add_footer(story, styles)
        
        return story
    
    def _add_logo(self, story):
        """Logo ekle"""
        try:
            if os.path.exists('logo.jpg'):
                logo = Image('logo.jpg', width=40*mm, height=15*mm)
                logo.hAlign = 'CENTER'
                story.append(logo)
                story.append(Spacer(1, 0.5*mm))
        except:
            pass
    
    def _add_header(self, story, styles, data):
        """Başlık ve tarih ekle"""
        baslik_stili = ParagraphStyle(
            'AnaBaslik',
            parent=styles['Heading1'],
            fontSize=14,
            spaceAfter=0.5*mm,
            alignment=1,
            textColor=colors.HexColor('#2C3E50'),
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph("URETIM FORMU", baslik_stili))
        
        tarih_stili = ParagraphStyle(
            'Tarih',
            parent=styles['Normal'],
            fontSize=11,
            alignment=2,
            spaceAfter=0.5*mm,
            textColor=colors.HexColor('#7F8C8D'),
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph(f"<b>Tarih:</b> {data.get('tarih', '')}", tarih_stili))
        story.append(Spacer(1, 0.5*mm))
    
    def _add_table(self, story, styles, data):
        """Ana tabloyu ekle"""
        tum_veriler = self._prepare_table_data(styles, data)
        tablo = Table(tum_veriler, colWidths=[60*mm, 140*mm], 
                     rowHeights=self._get_row_heights())
        tablo.setStyle(self._get_table_style())
        story.append(tablo)
    
    def _add_footer(self, story, styles):
        """Alt bilgi ekle"""
        story.append(Spacer(1, 0.5*mm))
        alt_bilgi_stili = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=6,
            alignment=1,
            textColor=colors.HexColor('#7F8C8D'),
            fontName='Helvetica-Bold'
        )
        alt_bilgi = Paragraph(
            f"Olusturulma: {datetime.now().strftime('%d.%m.%Y %H:%M')} - KUTU DUNYASI",
            alt_bilgi_stili
        )
        story.append(alt_bilgi)
    
    def _prepare_table_data(self, styles, data):
        """Tablo verilerini hazırla"""
        # Bu fonksiyon uzun olduğu için kısaltılmış halde gösteriliyor
        # Tam versiyon orijinal koddan alınabilir
        tum_veriler = []
        # ... tablo verilerini hazırlama kodları ...
        return tum_veriler
    
    def _get_row_heights(self):
        """Satır yüksekliklerini belirle"""
        return [30, 22, 22, 22, 22, 22, 30, 22, 22, 22, 22, 22, 22,
                30, 22, 22, 22, 22, 30, 22, 22, 22, 22, 30, 35,
                30, 30, 30, 30]
    
    def _get_table_style(self):
        """Tablo stilini belirle"""
        return TableStyle([
            # ... stil tanımlamaları ...
        ])
    