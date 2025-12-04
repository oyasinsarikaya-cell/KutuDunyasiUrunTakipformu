// Ana JavaScript fonksiyonları
document.addEventListener('DOMContentLoaded', function() {
    // Klavye kısayolları
    document.addEventListener('keydown', function(event) {
        if (event.key === '1' || event.key === 'Enter') {
            window.location.href = '/urun-takip';
        }
        if (event.key === '2') {
            window.location.href = '/uretim-planlama';
        }
    });
    
    // Hover efektleri
    document.querySelectorAll('.btn-module').forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 16px rgba(0,0,0,0.2)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
        });
    });
});