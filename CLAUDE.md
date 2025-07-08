# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Local Basket is a Flask-based Progressive Web App (PWA) that connects local homesteaders and farmers with buyers. The app allows sellers to create shop profiles with their location, products, and payment options, while buyers can discover local produce through a map interface.

## Development Setup

### Python Environment
- Always check for and use a virtual environment: `python -m venv venv && source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- If requirements.txt doesn't exist, create it after installing packages: `pip freeze > requirements.txt`

### Common Commands
- Run development server: `python app.py` or `flask run`
- Install Flask and dependencies: `pip install flask flask-sqlalchemy flask-login flask-wtf`
- Create database tables: `flask db init && flask db migrate && flask db upgrade` (if using Flask-Migrate)

### Testing
- Run tests: `python -m pytest` or `python -m unittest discover`
- Create test files in `tests/` directory
- Use `pytest tests/` for specific test directory

## Architecture

### Core Components
- **Flask Application**: Main web server handling routes and business logic
- **User Management**: Authentication system for sellers and buyers
- **Shop Management**: Seller profiles, product listings, and inventory
- **Location Services**: Map integration for finding nearby sellers
- **Payment Integration**: Support for cash, Venmo, PayPal, Zelle
- **PWA Features**: Service worker, manifest, offline capability

### Database Models
- User: Authentication and profile data
- Shop: Seller shop information and settings
- Product: Items for sale with pricing and availability
- Review: Customer reviews and ratings
- Location: Geographic data for shops

### Key Features
- Responsive design with mobile-first approach
- Geolocation integration for buyer discovery
- Real-time shop status (open/closed)
- Image upload for shop banners and product photos
- Email confirmation for user registration
- Review and rating system

## File Structure Conventions
- `app.py`: Main Flask application
- `models.py`: Database models
- `forms.py`: WTForms for user input
- `routes/`: Route handlers organized by feature
- `templates/`: Jinja2 HTML templates
- `static/`: CSS, JavaScript, images
- `static/manifest.json`: PWA manifest
- `static/sw.js`: Service worker for PWA functionality

## Development Guidelines

### Frontend
- Use earthy, organic color tones
- Implement artisan-style fonts
- Ensure mobile-responsive design
- Progressive Web App features required
- Map integration for location services

### Backend
- Use Flask with SQLAlchemy for database
- Implement Flask-Login for authentication
- Use Flask-WTF for form handling
- Email confirmation for registration
- Secure payment method handling (store only payment URLs, not sensitive data)

### Security
- Never store payment credentials
- Use HTTPS in production
- Implement CSRF protection
- Validate all user inputs
- Use secure session management

## Testing Strategy
- Unit tests for business logic
- Integration tests for routes
- Frontend tests for PWA functionality
- Location service mocking for tests
- Payment integration tests (using sandbox/test modes)