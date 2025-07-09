from flask import Blueprint, render_template, request, session, redirect, url_for
from models import Shop, Product
from forms import SearchForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    search_form = SearchForm()
    shops = Shop.query.filter_by(is_active=True).all()
    return render_template('index.html', shops=shops, search_form=search_form)

@main_bp.route('/search')
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