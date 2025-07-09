from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Shop, Product, Review
from forms import ShopForm, ProductForm, ReviewForm
from services.file_service import file_service

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@shop_bp.route('/shop/create', methods=['GET', 'POST'])
@login_required
def create_shop():
    if not current_user.is_seller:
        flash('You must be registered as a seller to create a shop.')
        return redirect(url_for('main.index'))
    
    if current_user.shop:
        flash('You already have a shop.')
        return redirect(url_for('shop.view_shop', shop_id=current_user.shop.id))
    
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
            is_open=False,  # Shop closed by default as specified
            user_id=current_user.id
        )
        
        db.session.add(shop)
        db.session.commit()
        
        flash('Shop created successfully!')
        return redirect(url_for('shop.view_shop', shop_id=shop.id))
    
    return render_template('create_shop.html', form=form)

@shop_bp.route('/shop/<int:shop_id>')
def view_shop(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    products = Product.query.filter_by(shop_id=shop_id, is_available=True).all()
    reviews = Review.query.filter_by(shop_id=shop_id).order_by(Review.created_at.desc()).all()
    
    review_form = ReviewForm() if current_user.is_authenticated else None
    
    return render_template('shop.html', shop=shop, products=products, 
                         reviews=reviews, review_form=review_form)

@shop_bp.route('/shop/<int:shop_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_shop(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    if shop.user_id != current_user.id:
        flash('You can only edit your own shop.')
        return redirect(url_for('shop.view_shop', shop_id=shop_id))
    
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
        return redirect(url_for('shop.view_shop', shop_id=shop_id))
    
    return render_template('edit_shop.html', form=form, shop=shop)

@shop_bp.route('/shop/<int:shop_id>/products/add', methods=['GET', 'POST'])
@login_required
def add_product(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    if shop.user_id != current_user.id:
        flash('You can only add products to your own shop.')
        return redirect(url_for('shop.view_shop', shop_id=shop_id))
    
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
        return redirect(url_for('shop.view_shop', shop_id=shop_id))
    
    return render_template('add_product.html', form=form, shop=shop)

@shop_bp.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.shop.user_id != current_user.id:
        flash('You can only edit your own products.')
        return redirect(url_for('shop.view_shop', shop_id=product.shop_id))
    
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        flash('Product updated successfully!')
        return redirect(url_for('shop.view_shop', shop_id=product.shop_id))
    
    return render_template('edit_product.html', form=form, product=product)

@shop_bp.route('/product/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.shop.user_id != current_user.id:
        flash('You can only delete your own products.')
        return redirect(url_for('shop.view_shop', shop_id=product.shop_id))
    
    shop_id = product.shop_id
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully!')
    return redirect(url_for('shop.view_shop', shop_id=shop_id))

@shop_bp.route('/shop/<int:shop_id>/review', methods=['POST'])
@login_required
def add_review(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    if shop.user_id == current_user.id:
        flash('You cannot review your own shop.')
        return redirect(url_for('shop.view_shop', shop_id=shop_id))
    
    # Check if user already reviewed this shop
    existing_review = Review.query.filter_by(buyer_id=current_user.id, shop_id=shop_id).first()
    if existing_review:
        flash('You have already reviewed this shop.')
        return redirect(url_for('shop.view_shop', shop_id=shop_id))
    
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
    
    return redirect(url_for('shop.view_shop', shop_id=shop_id))