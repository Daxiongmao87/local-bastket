# Development Guide

This document provides development guidelines and best practices for the Local Basket project.

## Development Environment Setup

### Python Environment
Always use a virtual environment to isolate project dependencies:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### Required Dependencies
```bash
pip install flask flask-sqlalchemy flask-login flask-wtf flask-migrate
pip install email-validator
pip freeze > requirements.txt
```

## Project Structure

```
local-basket/
├── app.py              # Main Flask application
├── models.py           # Database models
├── forms.py            # WTForms for user input
├── routes/             # Route handlers by feature
├── templates/          # Jinja2 HTML templates
├── static/            
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript files
│   ├── images/        # Static images
│   ├── manifest.json  # PWA manifest
│   └── sw.js          # Service worker
├── tests/             # Test files
└── migrations/        # Database migrations
```

## Database Management

### Initial Setup
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Making Changes
```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

## Testing Strategy

### Running Tests
```bash
python -m pytest
python -m pytest tests/test_specific.py
python -m pytest tests/test_specific.py::test_function
```

### Test Structure
- `tests/test_models.py` - Database model tests
- `tests/test_routes.py` - Route handler tests  
- `tests/test_forms.py` - Form validation tests
- `tests/test_auth.py` - Authentication tests

## Frontend Development

### Design Guidelines
- Use earthy, organic color tones (#8B4513, #228B22, #DAA520)
- Implement artisan-style fonts (serif or handwritten styles)
- Mobile-first responsive design
- Ensure accessibility standards

### FontAwesome Integration
The project includes FontAwesome Pro 5.15.4 for icons:

1. **Setup**: Extract `fontawesome-pro-5.15.4-web.zip` to `static/fontawesome/`
   ```bash
   unzip fontawesome-pro-5.15.4-web.zip -d static/fontawesome/
   ```

2. **Include in templates**: Add to your base template:
   ```html
   <link rel="stylesheet" href="{{ url_for('static', filename='fontawesome/css/all.min.css') }}">
   ```

3. **Usage examples**:
   - Shopping cart: `<i class="fas fa-shopping-cart"></i>`
   - Location pin: `<i class="fas fa-map-marker-alt"></i>`
   - User profile: `<i class="fas fa-user"></i>`
   - Phone: `<i class="fas fa-phone"></i>`
   - Email: `<i class="fas fa-envelope"></i>`
   - Star rating: `<i class="fas fa-star"></i>`

4. **Product category icons** (for representing different farm/homestead products):
   - Eggs: `<i class="fas fa-egg"></i>`
   - Vegetables: `<i class="fas fa-carrot"></i>` `<i class="fas fa-pepper-hot"></i>`
   - Fruits: `<i class="fas fa-apple-alt"></i>` `<i class="fas fa-lemon"></i>`
   - Meat/Poultry: `<i class="fas fa-drumstick-bite"></i>`
   - Dairy: `<i class="fas fa-cheese"></i>`
   - Bread/Baked goods: `<i class="fas fa-bread-slice"></i>`
   - Honey: `<i class="fas fa-honey-pot"></i>`
   - Firewood: `<i class="fas fa-fire"></i>` `<i class="fas fa-tree"></i>`
   - Herbs/Spices: `<i class="fas fa-seedling"></i>` `<i class="fas fa-leaf"></i>`
   - Flowers: `<i class="fas fa-flower"></i>` `<i class="fas fa-rose"></i>`
   - Preserves/Jams: `<i class="fas fa-jar"></i>`
   - Wine/Beverages: `<i class="fas fa-wine-bottle"></i>` `<i class="fas fa-coffee"></i>`
   - Fish: `<i class="fas fa-fish"></i>`
   - Tools/Equipment: `<i class="fas fa-hammer"></i>` `<i class="fas fa-tools"></i>`

   **Implementation tip**: Consider adding an `icon_class` field to your Product model to store the FontAwesome class name, making it easy to display consistent icons across the app:
   ```python
   # In models.py
   class Product(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(100), nullable=False)
       icon_class = db.Column(db.String(50), default='fas fa-apple-alt')
       # other fields...
   ```

5. **File structure after extraction**:
   ```
   static/fontawesome/
   ├── css/
   │   ├── all.min.css
   │   └── fontawesome.min.css
   ├── js/
   └── webfonts/
   ```

### PWA Implementation
- Manifest file for app installation
- Service worker for offline functionality
- Responsive design for all screen sizes
- Location services integration

## Code Quality

### Pre-commit Hooks
Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python -m pytest
python -m flake8 --max-line-length=88
python -m black --check .
```

### File Size Limits
- Keep source files under 1000 lines
- Refactor large files into smaller modules
- Use clear, descriptive function and variable names

## Security Considerations

### Authentication
- Email confirmation required for registration
- Secure session management with Flask-Login
- CSRF protection with Flask-WTF

### Payment Integration
- Store only payment URLs/QR codes, never credentials
- Use HTTPS in production
- Validate all payment method URLs

### Data Protection
- Sanitize all user inputs
- Use parameterized database queries
- Implement proper error handling without exposing system details

## Development Workflow

### Feature Development
1. Create feature branch from main
2. Write tests for new functionality
3. Implement feature following existing patterns
4. Ensure all tests pass
5. Update documentation if needed
6. Submit pull request

### Database Changes
1. Create migration with descriptive message
2. Test migration on development database
3. Update model tests if needed
4. Document any manual steps required

## Performance Considerations

### Database Optimization
- Use database indexes for frequently queried fields
- Implement pagination for large result sets
- Consider caching for location queries

### Frontend Performance
- Optimize images before upload
- Implement lazy loading for product images
- Use efficient map rendering techniques
- Minimize JavaScript bundle size

## Deployment

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export DATABASE_URL=your-database-url
export MAIL_SERVER=your-mail-server
export MAIL_USERNAME=your-mail-username
export MAIL_PASSWORD=your-mail-password
```

### Production Checklist
- [ ] Debug mode disabled
- [ ] Secret key set from environment
- [ ] Database migrations applied
- [ ] HTTPS configured
- [ ] Static files served efficiently
- [ ] Error logging configured
- [ ] Backup strategy implemented