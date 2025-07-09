from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    is_seller = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    shop = db.relationship('Shop', backref='owner', uselist=False)
    reviews_written = db.relationship('Review', foreign_keys='Review.buyer_id', backref='buyer')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Shop(db.Model):
    __tablename__ = 'shops'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    banner_image = db.Column(db.String(200))
    address = db.Column(db.String(300), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    website = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    is_open = db.Column(db.Boolean, default=False)  # Closed by default as specified
    hours_monday = db.Column(db.String(50))
    hours_tuesday = db.Column(db.String(50))
    hours_wednesday = db.Column(db.String(50))
    hours_thursday = db.Column(db.String(50))
    hours_friday = db.Column(db.String(50))
    hours_saturday = db.Column(db.String(50))
    hours_sunday = db.Column(db.String(50))
    payment_cash = db.Column(db.Boolean, default=True)
    payment_venmo = db.Column(db.String(100))
    payment_paypal = db.Column(db.String(100))
    payment_zelle = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    products = db.relationship('Product', backref='shop', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='shop', lazy=True)
    
    @property
    def average_rating(self):
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews)
    
    @property
    def total_reviews(self):
        return len(self.reviews)
    
    def __repr__(self):
        return f'<Shop {self.name}>'


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    icon_class = db.Column(db.String(50), default='fas fa-apple-alt')
    image_url = db.Column(db.String(200))
    is_available = db.Column(db.Boolean, default=True)
    stock_quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    
    @classmethod
    def get_category_icons(cls):
        """Get predefined category icons as specified in DEVELOPMENT.md"""
        return {
            'eggs': 'fas fa-egg',
            'vegetables': 'fas fa-carrot',
            'peppers': 'fas fa-pepper-hot', 
            'fruits': 'fas fa-apple-alt',
            'citrus': 'fas fa-lemon',
            'meat': 'fas fa-drumstick-bite',
            'dairy': 'fas fa-cheese',
            'bread': 'fas fa-bread-slice',
            'honey': 'fas fa-honey-pot',
            'firewood': 'fas fa-fire',
            'lumber': 'fas fa-tree',
            'herbs': 'fas fa-seedling',
            'leafy_greens': 'fas fa-leaf',
            'flowers': 'fas fa-flower',
            'roses': 'fas fa-rose',
            'preserves': 'fas fa-jar',
            'wine': 'fas fa-wine-bottle',
            'beverages': 'fas fa-coffee',
            'fish': 'fas fa-fish',
            'tools': 'fas fa-hammer',
            'equipment': 'fas fa-tools',
        }
    
    def __repr__(self):
        return f'<Product {self.name}>'


class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    
    def __repr__(self):
        return f'<Review {self.rating} stars for {self.shop.name}>'


class Location(db.Model):
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(300), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), default='United States')
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<Location {self.city}, {self.state}>'