import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from models import db, User, Shop, Product, Review, Location
from forms import (RegistrationForm, LoginForm, ShopForm, ProductForm, 
                   ReviewForm, SearchForm, ProfileForm)
from services.email_service import email_service
from services.file_service import file_service
from services.location_service import location_service
from config import config
import secrets


def create_app(config_name=None):
    app = Flask(__name__)
    
    # Configuration
    config_name = config_name or os.environ.get('FLASK_CONFIG', 'default')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    email_service.init_app(app)
    
    # Login manager setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create upload directory if it doesn't exist
    upload_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    os.makedirs(upload_path, exist_ok=True)
    
    # Routes
    @app.route('/')
    def index():
        search_form = SearchForm()
        shops = Shop.query.filter_by(is_active=True).all()
        return render_template('index.html', shops=shops, search_form=search_form)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            # Check if user already exists
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered.')
                return redirect(url_for('register'))
            
            if User.query.filter_by(username=form.username.data).first():
                flash('Username already taken.')
                return redirect(url_for('register'))
            
            # Create new user
            user = User(
                username=form.username.data,
                email=form.email.data,
                full_name=form.full_name.data,
                phone=form.phone.data,
                is_seller=form.is_seller.data
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            # Send confirmation email
            try:
                email_service.send_confirmation_email(user)
                flash('Registration successful! Please check your email to confirm your account.')
            except Exception as e:
                current_app.logger.error(f'Email sending failed: {str(e)}')
                flash('Registration successful! Please log in.')
            
            return redirect(url_for('login'))
        
        return render_template('register.html', form=form)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('index'))
            flash('Invalid email or password.')
        
        return render_template('login.html', form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('index'))
    
    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html', user=current_user)
    
    @app.route('/shop/create', methods=['GET', 'POST'])
    @login_required
    def create_shop():
        if not current_user.is_seller:
            flash('You must be registered as a seller to create a shop.')
            return redirect(url_for('index'))
        
        if current_user.shop:
            flash('You already have a shop.')
            return redirect(url_for('view_shop', shop_id=current_user.shop.id))
        
        form = ShopForm()
        if form.validate_on_submit():
            shop = Shop(
                name=form.name.data,
                description=form.description.data,
                address=form.address.data,
                latitude=form.latitude.data,
                longitude=form.longitude.data,
                phone=form.phone.data,
                email=form.email.data,
                website=form.website.data,
                hours_monday=form.hours_monday.data,
                hours_tuesday=form.hours_tuesday.data,
                hours_wednesday=form.hours_wednesday.data,
                hours_thursday=form.hours_thursday.data,
                hours_friday=form.hours_friday.data,
                hours_saturday=form.hours_saturday.data,
                hours_sunday=form.hours_sunday.data,
                payment_cash=form.payment_cash.data,
                payment_venmo=form.payment_venmo.data,
                payment_paypal=form.payment_paypal.data,
                payment_zelle=form.payment_zelle.data,
                is_open=form.is_open.data,
                user_id=current_user.id
            )
            
            db.session.add(shop)
            db.session.commit()
            
            flash('Shop created successfully!')
            return redirect(url_for('view_shop', shop_id=shop.id))
        
        return render_template('create_shop.html', form=form)
    
    @app.route('/shop/<int:shop_id>')
    def view_shop(shop_id):
        shop = Shop.query.get_or_404(shop_id)
        products = Product.query.filter_by(shop_id=shop_id, is_available=True).all()
        reviews = Review.query.filter_by(shop_id=shop_id).order_by(Review.created_at.desc()).all()
        
        review_form = ReviewForm() if current_user.is_authenticated else None
        
        return render_template('shop.html', shop=shop, products=products, 
                             reviews=reviews, review_form=review_form)
    
    @app.route('/shop/<int:shop_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_shop(shop_id):
        shop = Shop.query.get_or_404(shop_id)
        if shop.user_id != current_user.id:
            flash('You can only edit your own shop.')
            return redirect(url_for('view_shop', shop_id=shop_id))
        
        form = ShopForm(obj=shop)
        if form.validate_on_submit():
            # Handle banner image upload
            if 'banner_image' in request.files:
                banner_file = request.files['banner_image']
                if banner_file and banner_file.filename:
                    try:
                        # Delete old banner if exists
                        if shop.banner_image:
                            file_service.delete_file(shop.banner_image)
                        
                        shop.banner_image = file_service.save_shop_banner(banner_file)
                    except ValueError as e:
                        flash(f'Banner upload failed: {str(e)}')
                        return render_template('edit_shop.html', form=form, shop=shop)
            
            form.populate_obj(shop)
            db.session.commit()
            flash('Shop updated successfully!')
            return redirect(url_for('view_shop', shop_id=shop_id))
        
        return render_template('edit_shop.html', form=form, shop=shop)
    
    @app.route('/shop/<int:shop_id>/products/add', methods=['GET', 'POST'])
    @login_required
    def add_product(shop_id):
        shop = Shop.query.get_or_404(shop_id)
        if shop.user_id != current_user.id:
            flash('You can only add products to your own shop.')
            return redirect(url_for('view_shop', shop_id=shop_id))
        
        form = ProductForm()
        if form.validate_on_submit():
            # Handle image upload
            image_url = None
            if 'product_image' in request.files:
                image_file = request.files['product_image']
                if image_file and image_file.filename:
                    try:
                        image_url = file_service.save_product_image(image_file)
                    except ValueError as e:
                        flash(f'Image upload failed: {str(e)}')
                        return render_template('add_product.html', form=form, shop=shop)
            
            product = Product(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                unit=form.unit.data,
                category=form.category.data,
                icon_class=form.icon_class.data,
                image_url=image_url or form.image_url.data,
                is_available=form.is_available.data,
                stock_quantity=form.stock_quantity.data,
                shop_id=shop_id
            )
            
            db.session.add(product)
            db.session.commit()
            
            flash('Product added successfully!')
            return redirect(url_for('view_shop', shop_id=shop_id))
        
        return render_template('add_product.html', form=form, shop=shop)
    
    @app.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_product(product_id):
        product = Product.query.get_or_404(product_id)
        if product.shop.user_id != current_user.id:
            flash('You can only edit your own products.')
            return redirect(url_for('view_shop', shop_id=product.shop_id))
        
        form = ProductForm(obj=product)
        if form.validate_on_submit():
            form.populate_obj(product)
            db.session.commit()
            flash('Product updated successfully!')
            return redirect(url_for('view_shop', shop_id=product.shop_id))
        
        return render_template('edit_product.html', form=form, product=product)
    
    @app.route('/product/<int:product_id>/delete', methods=['POST'])
    @login_required
    def delete_product(product_id):
        product = Product.query.get_or_404(product_id)
        if product.shop.user_id != current_user.id:
            flash('You can only delete your own products.')
            return redirect(url_for('view_shop', shop_id=product.shop_id))
        
        shop_id = product.shop_id
        db.session.delete(product)
        db.session.commit()
        
        flash('Product deleted successfully!')
        return redirect(url_for('view_shop', shop_id=shop_id))
    
    @app.route('/shop/<int:shop_id>/review', methods=['POST'])
    @login_required
    def add_review(shop_id):
        shop = Shop.query.get_or_404(shop_id)
        if shop.user_id == current_user.id:
            flash('You cannot review your own shop.')
            return redirect(url_for('view_shop', shop_id=shop_id))
        
        # Check if user already reviewed this shop
        existing_review = Review.query.filter_by(buyer_id=current_user.id, shop_id=shop_id).first()
        if existing_review:
            flash('You have already reviewed this shop.')
            return redirect(url_for('view_shop', shop_id=shop_id))
        
        form = ReviewForm()
        if form.validate_on_submit():
            review = Review(
                rating=int(form.rating.data),
                comment=form.comment.data,
                buyer_id=current_user.id,
                shop_id=shop_id
            )
            
            db.session.add(review)
            db.session.commit()
            
            flash('Review added successfully!')
        
        return redirect(url_for('view_shop', shop_id=shop_id))
    
    @app.route('/search')
    def search():
        form = SearchForm()
        shops = []
        
        if form.validate():
            query = Shop.query.filter_by(is_active=True)
            
            if form.query.data:
                query = query.filter(Shop.name.contains(form.query.data))
            
            if form.category.data:
                query = query.join(Product).filter(Product.category == form.category.data)
            
            shops = query.all()
        
        return render_template('search.html', form=form, shops=shops)
    
    @app.route('/api/shops')
    def api_shops():
        shops = Shop.query.filter_by(is_active=True).all()
        return jsonify([{
            'id': shop.id,
            'name': shop.name,
            'latitude': shop.latitude,
            'longitude': shop.longitude,
            'address': shop.address,
            'rating': shop.average_rating,
            'is_open': shop.is_open
        } for shop in shops])
    
    @app.route('/map')
    def map_view():
        return render_template('map.html')
    
    @app.route('/confirm/<token>')
    def confirm_email(token):
        email = email_service.confirm_token(token)
        if not email:
            flash('The confirmation link is invalid or has expired.')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User not found.')
            return redirect(url_for('login'))
        
        if user.is_verified:
            flash('Account already confirmed.')
        else:
            user.is_verified = True
            db.session.commit()
            flash('Your account has been confirmed. Thank you!')
        
        return redirect(url_for('login'))
    
    @app.route('/api/geocode')
    def api_geocode():
        address = request.args.get('address')
        if not address:
            return jsonify({'error': 'Address parameter required'}), 400
        
        try:
            coordinates = location_service.geocode_address(address)
            if coordinates:
                return jsonify({
                    'latitude': coordinates[0],
                    'longitude': coordinates[1]
                })
            else:
                return jsonify({'error': 'Address not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/reverse-geocode')
    def api_reverse_geocode():
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        
        if not lat or not lng:
            return jsonify({'error': 'Latitude and longitude parameters required'}), 400
        
        try:
            address = location_service.reverse_geocode(float(lat), float(lng))
            if address:
                return jsonify({'address': address})
            else:
                return jsonify({'error': 'Address not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/offline')
    def offline():
        return render_template('offline.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000)