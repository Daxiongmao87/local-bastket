from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from models import db, User
from forms import RegistrationForm, LoginForm
from services.email_service import email_service

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken.')
            return redirect(url_for('auth.register'))
        
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
            flash('Registration successful! Please log in.')
        
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            
            # User intent memory - return to intended page after login
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            # Check if user was trying to set up shop
            if session.get('intended_action') == 'setup_shop':
                session.pop('intended_action', None)
                if user.is_seller and not user.shop:
                    return redirect(url_for('shop.create_shop'))
            
            return redirect(url_for('main.index'))
        flash('Invalid email or password.')
    
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    email = email_service.confirm_token(token)
    if not email:
        flash('The confirmation link is invalid or has expired.')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User not found.')
        return redirect(url_for('auth.login'))
    
    if user.is_verified:
        flash('Account already confirmed.')
    else:
        user.is_verified = True
        db.session.commit()
        flash('Your account has been confirmed. Thank you!')
    
    return redirect(url_for('auth.login'))