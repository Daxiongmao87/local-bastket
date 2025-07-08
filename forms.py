from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, FloatField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional, URL
from flask_wtf.file import FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=200)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    is_seller = BooleanField('I want to sell products')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')


class ShopForm(FlaskForm):
    name = StringField('Shop Name', validators=[DataRequired(), Length(min=2, max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    banner_image = FileField('Banner Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    address = StringField('Address', validators=[DataRequired(), Length(max=300)])
    latitude = FloatField('Latitude', validators=[DataRequired(), NumberRange(min=-90, max=90)])
    longitude = FloatField('Longitude', validators=[DataRequired(), NumberRange(min=-180, max=180)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    email = StringField('Email', validators=[Optional(), Email()])
    website = StringField('Website', validators=[Optional(), URL()])
    
    # Operating Hours
    hours_monday = StringField('Monday Hours', validators=[Optional(), Length(max=50)])
    hours_tuesday = StringField('Tuesday Hours', validators=[Optional(), Length(max=50)])
    hours_wednesday = StringField('Wednesday Hours', validators=[Optional(), Length(max=50)])
    hours_thursday = StringField('Thursday Hours', validators=[Optional(), Length(max=50)])
    hours_friday = StringField('Friday Hours', validators=[Optional(), Length(max=50)])
    hours_saturday = StringField('Saturday Hours', validators=[Optional(), Length(max=50)])
    hours_sunday = StringField('Sunday Hours', validators=[Optional(), Length(max=50)])
    
    # Payment Methods
    payment_cash = BooleanField('Accept Cash')
    payment_venmo = StringField('Venmo Username', validators=[Optional(), Length(max=100)])
    payment_paypal = StringField('PayPal Email/Link', validators=[Optional(), Length(max=100)])
    payment_zelle = StringField('Zelle Email/Phone', validators=[Optional(), Length(max=100)])
    
    is_open = BooleanField('Shop is currently open')


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    unit = StringField('Unit (e.g., lb, each, dozen)', validators=[DataRequired(), Length(max=50)])
    category = SelectField('Category', validators=[DataRequired()], choices=[
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('eggs', 'Eggs'),
        ('meat', 'Meat & Poultry'),
        ('dairy', 'Dairy'),
        ('bread', 'Bread & Baked Goods'),
        ('honey', 'Honey & Syrups'),
        ('herbs', 'Herbs & Spices'),
        ('flowers', 'Flowers'),
        ('preserves', 'Preserves & Jams'),
        ('beverages', 'Beverages'),
        ('firewood', 'Firewood & Fuel'),
        ('other', 'Other')
    ])
    icon_class = SelectField('Icon', validators=[Optional()], choices=[
        ('fas fa-apple-alt', 'Apple'),
        ('fas fa-carrot', 'Carrot'),
        ('fas fa-pepper-hot', 'Pepper'),
        ('fas fa-egg', 'Egg'),
        ('fas fa-drumstick-bite', 'Meat'),
        ('fas fa-cheese', 'Cheese'),
        ('fas fa-bread-slice', 'Bread'),
        ('fas fa-honey-pot', 'Honey'),
        ('fas fa-seedling', 'Herbs'),
        ('fas fa-flower', 'Flower'),
        ('fas fa-jar', 'Preserves'),
        ('fas fa-wine-bottle', 'Beverages'),
        ('fas fa-fire', 'Firewood'),
        ('fas fa-leaf', 'Other')
    ])
    image_url = StringField('Image URL', validators=[Optional(), URL()])
    is_available = BooleanField('Currently Available')
    stock_quantity = IntegerField('Stock Quantity', validators=[Optional(), NumberRange(min=0)])


class ReviewForm(FlaskForm):
    rating = SelectField('Rating', validators=[DataRequired()], choices=[
        ('5', '5 Stars - Excellent'),
        ('4', '4 Stars - Good'),
        ('3', '3 Stars - Average'),
        ('2', '2 Stars - Poor'),
        ('1', '1 Star - Terrible')
    ])
    comment = TextAreaField('Comment', validators=[Optional(), Length(max=500)])


class SearchForm(FlaskForm):
    query = StringField('Search', validators=[Optional(), Length(max=100)])
    category = SelectField('Category', validators=[Optional()], choices=[
        ('', 'All Categories'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('eggs', 'Eggs'),
        ('meat', 'Meat & Poultry'),
        ('dairy', 'Dairy'),
        ('bread', 'Bread & Baked Goods'),
        ('honey', 'Honey & Syrups'),
        ('herbs', 'Herbs & Spices'),
        ('flowers', 'Flowers'),
        ('preserves', 'Preserves & Jams'),
        ('beverages', 'Beverages'),
        ('firewood', 'Firewood & Fuel'),
        ('other', 'Other')
    ])
    max_distance = SelectField('Distance', validators=[Optional()], choices=[
        ('', 'Any Distance'),
        ('5', 'Within 5 miles'),
        ('10', 'Within 10 miles'),
        ('25', 'Within 25 miles'),
        ('50', 'Within 50 miles')
    ])
    min_rating = SelectField('Minimum Rating', validators=[Optional()], choices=[
        ('', 'Any Rating'),
        ('4', '4+ Stars'),
        ('3', '3+ Stars'),
        ('2', '2+ Stars'),
        ('1', '1+ Stars')
    ])


class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=200)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', 
                                   validators=[Optional(), EqualTo('new_password')])