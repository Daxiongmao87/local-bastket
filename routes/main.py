from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from models import Shop, Product
from forms import SearchForm
from services.location_service import location_service

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    search_form = SearchForm()
    shops = Shop.query.filter_by(is_active=True).all()
    return render_template('index.html', shops=shops, search_form=search_form)

@main_bp.route('/search')
def search():
    form = SearchForm(request.args)
    shops = []
    
    if form.validate():
        query = Shop.query.filter_by(is_active=True)
        
        if form.query.data:
            search_term = f"%{form.query.data}%"
            query = query.filter(Shop.name.ilike(search_term))
        
        if form.category.data:
            query = query.join(Product).filter(Product.category == form.category.data)
            
        if form.min_rating.data:
            query = query.filter(Shop.average_rating >= form.min_rating.data)

        all_shops = query.all()
        
        # Filter by distance in Python after getting results
        if form.max_distance.data and form.user_lat.data and form.user_lon.data:
            user_lat = float(form.user_lat.data)
            user_lon = float(form.user_lon.data)
            max_dist = float(form.max_distance.data)
            
            nearby_shops_data = location_service.get_nearby_shops(
                user_lat, user_lon, all_shops, max_dist, unit='miles'
            )
            shops = [d['shop'] for d in nearby_shops_data]
        else:
            shops = all_shops
    
    return render_template('search.html', form=form, shops=shops)

@main_bp.route('/map')
def map_view():
    return render_template('map.html')

@main_bp.route('/offline')
def offline():
    return render_template('offline.html')

@main_bp.route('/setup-shop-intent')
def setup_shop_intent():
    """Handle user intent to set up shop - redirect to login if needed"""
    session['intended_action'] = 'setup_shop'
    return redirect(url_for('auth.login'))