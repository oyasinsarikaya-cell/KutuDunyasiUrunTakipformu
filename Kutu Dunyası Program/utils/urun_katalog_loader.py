import pandas as pd
import logging

logger = logging.getLogger(__name__)

class UrunKatalogYukleyici:
    def __init__(self, dosya_yolu='urun_katalog.xlsx'):
        self.dosya_yolu = dosya_yolu
    
    def yukle(self):
        """Excel dosyasından ürün kataloğunu yükler"""
        try:
            df = pd.read_excel(self.dosya_yolu, sheet_name='Ürün Kataloğu')
            df['Ürün Adı*'] = df['Ürün Adı*'].astype(str).str.strip()
            df['Bıçak Kodu*'] = df['Bıçak Kodu*'].astype(str).str.strip()
            df = df.fillna('')
            logger.info(f"Ürün kataloğu başarıyla yüklendi. Toplam {len(df)} ürün.")
            return df
        except Exception as e:
            logger.error(f"Ürün kataloğu yükleme hatası: {e}")
            return pd.DataFrame(columns=['Ürün Adı*', 'Bıçak Kodu*', 'Bıçak Ebadı En (mm)*', 'Bıçak Ebadı Boy (mm)*'])
    
    def tum_urun_listesi(self):
        """Tüm ürün listesini getirir"""
        try:
            df = self.yukle()
            if df.empty:
                return []
            urun_listesi = df['Ürün Adı*'].dropna().unique().tolist()
            urun_listesi = [urun.strip() for urun in urun_listesi if urun.strip()]
            urun_listesi.sort()
            return urun_listesi
        except Exception as e:
            logger.error(f"Ürün listesi getirme hatası: {e}")
            return []
    
    def urun_bilgisi_getir(self, urun_adi):
        """Ürün adına göre bıçak kodu ve ebatlarını getirir"""
        try:
            df = self.yukle()
            if df.empty:
                return None
                
            urun_adi_aranan = urun_adi.strip()
            bulunan_urun = df[df['Ürün Adı*'] == urun_adi_aranan]
            
            if not bulunan_urun.empty:
                urun_bilgisi = bulunan_urun.iloc[0]
                bicak_kodu = urun_bilgisi['Bıçak Kodu*']
                en = urun_bilgisi['Bıçak Ebadı En (mm)*']
                boy = urun_bilgisi['Bıçak Ebadı Boy (mm)*']
                
                if pd.isna(bicak_kodu) or bicak_kodu == 'nan' or bicak_kodu == '':
                    bicak_kodu = "Bıçak Kodu Bulunamadı"
                
                return {
                    'bicak_kodu': bicak_kodu,
                    'en': en,
                    'boy': boy,
                    'urun_adi': urun_adi_aranan
                }
            return None
        except Exception as e:
            logger.error(f"Ürün bilgisi getirme hatası: {e}")
            return None