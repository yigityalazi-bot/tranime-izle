"""
=============================================================================
TRAnime - Kişisel Anime İzleme Platformu Backend Mimarisi
Geliştirici: Senior Python/Flask Developer
Teknoloji Yığını: Python 3, Flask, Flask-SQLAlchemy, SQLite
=============================================================================
"""

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# ---------------------------------------------------------------------------
# 1. UYGULAMA VE DİZİN YAPILANDIRMASI
# ---------------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Şablon ve statik klasör yollarını mutlak (absolute) yol ile tanımlıyoruz
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

# SQLite Veritabanı Yapılandırması: 'site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'site.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tr-anime-secret-key-production-ready-2026'

# SQLAlchemy ORM Örneği
db = SQLAlchemy(app)


# ---------------------------------------------------------------------------
# 2. VERİTABANI ŞEMASI (MODELS)
# ---------------------------------------------------------------------------

class Anime(db.Model):
    """
    Anime Modeli:
    Bir animeyi ve bu animeye ait temel meta bilgileri temsil eder.
    Bir anime, birden çok bölüme (Bolum) sahip olabilir (1 - N İlişkisi).
    """
    __tablename__ = 'anime'

    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(150), nullable=False, index=True)
    kapak_resmi = db.Column(db.String(500), nullable=True)
    tur = db.Column(db.String(100), nullable=True, index=True)
    aciklama = db.Column(db.Text, nullable=True)

    # 1 - N İlişkisi (One-to-Many Relationship)
    bolumler = db.relationship(
        'Bolum',
        backref='anime',
        lazy=True,
        cascade='all, delete-orphan',
        order_by='Bolum.bolum_no'
    )

    def son_bolum_no(self):
        """Animeye ait son eklenen bölüm numarasını döndürür."""
        if self.bolumler:
            return self.bolumler[-1].bolum_no
        return 1

    def __repr__(self):
        return f'<Anime id={self.id} baslik="{self.baslik}">'


class Bolum(db.Model):
    """
    Bölüm Modeli:
    Her bir anime bölümünü, bölüm numarasını ve oynatılacak video kaynağını temsil eder.
    Foreign Key ile Anime modeline bağlanır.
    """
    __tablename__ = 'bolum'

    id = db.Column(db.Integer, primary_key=True)
    bolum_no = db.Column(db.Integer, nullable=False)
    video_url = db.Column(db.String(500), nullable=False)

    # Foreign Key Bağlantısı -> anime tablosunun id sütunu
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id'), nullable=False, index=True)

    def __repr__(self):
        return f'<Bolum id={self.id} anime_id={self.anime_id} bolum_no={self.bolum_no}>'


# ---------------------------------------------------------------------------
# 3. VERİTABANI BAŞLANGIÇ & DUMMY VERİ FONKSİYONU
# ---------------------------------------------------------------------------

def ornek_verileri_yukle():
    """
    Veritabanı boş ise test yapabilmek amacıyla 5 adet örnek anime
    ve bu animelere ait ilişkili bölümleri otomatik ekler.
    """
    if Anime.query.count() == 0:
        ornekler = [
            {
                "baslik": "Jujutsu Kaisen: Shibuya Olayı",
                "kapak_resmi": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=600&auto=format&fit=crop&q=80",
                "tur": "Aksiyon, Doğaüstü",
                "aciklama": "Cadılar Bayramı gecesi Shibuya'da özel mühürler kırılır ve lanet kullanıcıları ile büyücüler arasındaki savaş başlar.",
                "bolumler": [1, 2, 3, 24]
            },
            {
                "baslik": "Demon Slayer: Hashira Eğitimi",
                "kapak_resmi": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=600&auto=format&fit=crop&q=80",
                "tur": "Shounen, Fantezi",
                "aciklama": "Tanjiro ve İblis Avcısı Birliği, yaklaşan nihai savaş öncesinde Hashiralar ile eğitime girer.",
                "bolumler": [1, 2, 8]
            },
            {
                "baslik": "Chainsaw Man",
                "kapak_resmi": "https://images.unsplash.com/photo-1563089145-599997674d42?w=600&auto=format&fit=crop&q=80",
                "tur": "Aksiyon, Korku",
                "aciklama": "Denji, testere iblisi köpeği Pochita ile yaşarken ölümcül bir komploya kurban gider ve Chainsaw Man olarak dirilir.",
                "bolumler": [1, 2, 12]
            },
            {
                "baslik": "Attack on Titan: The Final Season",
                "kapak_resmi": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&auto=format&fit=crop&q=80",
                "tur": "Dram, Askeri",
                "aciklama": "Duvarların ötesindeki dünyanın gerçeği ortaya çıktığında, özgürlük arayışı tüm dünyayı sarsacak bir felakete dönüşür.",
                "bolumler": [1, 2, 87]
            },
            {
                "baslik": "Sousou no Frieren",
                "kapak_resmi": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&auto=format&fit=crop&q=80",
                "tur": "Fantezi, Macera",
                "aciklama": "İblis Kral'ı yenen kahraman grubunun büyücüsü olan elf Frieren, insanların faniliğini anlamak için yeni bir yolculuğa çıkar.",
                "bolumler": [1, 2, 28]
            }
        ]

        for item in ornekler:
            anime = Anime(
                baslik=item["baslik"],
                kapak_resmi=item["kapak_resmi"],
                tur=item["tur"],
                aciklama=item["aciklama"]
            )
            db.session.add(anime)
            db.session.flush()

            for b_no in item["bolumler"]:
                bolum = Bolum(
                    bolum_no=b_no,
                    video_url=f"https://www.youtube.com/embed/placeholder_{anime.id}_{b_no}",
                    anime_id=anime.id
                )
                db.session.add(bolum)

        db.session.commit()
        print(">> [BAŞARILI] 'site.db' veritabanına 5 adet örnek anime ve ilişkili bölümleri eklendi.")


# ---------------------------------------------------------------------------
# 4. VIEW CONTROLLERS / ROUTES
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    """Ana Sayfa: Tüm animeleri listeler."""
    animeler = Anime.query.all()
    return render_template('index.html', animeler=animeler, aktif_tur='Tümü')


@app.route('/kategori/<tur>')
def kategori(tur):
    """Kategori Filtreleme: Belirli bir türe ait animeleri listeler."""
    animeler = Anime.query.filter(Anime.tur.ilike(f"%{tur}%")).all()
    return render_template('index.html', animeler=animeler, aktif_tur=tur)


# ---------------------------------------------------------------------------
# 5. UYGULAMA VE VERİTABANI BAŞLATICI
# ---------------------------------------------------------------------------

# Canlı sunucu (gunicorn) ve yerel çalıştırma için tabloları başlatıyoruz
with app.app_context():
    db.create_all()
    ornek_verileri_yukle()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "=" * 60)
    print(" [TRAnime] Uygulama Başarıyla Çalıştırıldı!")
    print(" Veritabanı: site.db")
    print(f" Yerel Adres: http://127.0.0.1:{port}")
    print("=" * 60 + "\n")

    app.run(host='0.0.0.0', port=port, debug=True)

