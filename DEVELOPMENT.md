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

## Phase 4: Advanced CSS Development Tools

### CSS Architecture Overview

The project now includes a comprehensive CSS development toolchain with:

```
static/css/
├── variables.css           # Core design tokens
├── design-system.css       # Extended design tokens (200+ variables)
├── base.css               # Base styles and typography
├── main.css               # Main application styles
├── components-v2.css      # Modern component library with container queries
├── accessibility.css      # WCAG 2.1 AA compliance features
└── build/                 # Production builds (auto-generated)
```

### Development Tools

#### CSS Linting and Formatting
```bash
# Install Node.js dependencies
npm install

# Lint CSS files with Stylelint
npm run lint:css

# Format CSS files with Prettier
npm run format:css

# Combined test (linting + build)
npm run test:css
```

#### CSS Build System
```bash
# Build production CSS bundle
npm run build:css
python build_css.py

# Watch CSS files for changes
npm run dev:css

# Development server with hot reload
python dev_server.py
```

#### CSS Analysis
```bash
# Comprehensive CSS analysis
npm run analyze:css
python analyze_css.py

# Output includes:
# - File size analysis and compression ratios
# - CSS rule and selector statistics
# - Custom property usage
# - Accessibility feature detection
# - Optimization recommendations
```

### Design System Usage

#### Design Tokens
Use CSS custom properties for consistent styling:

```css
/* Color System (semantic colors) */
.my-component {
  background: var(--color-surface);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

/* Typography Scale (fluid typography) */
.title { font-size: var(--text-2xl); }
.body { font-size: var(--text-base); }
.caption { font-size: var(--text-sm); }

/* Spacing Scale */
.component {
  padding: var(--space-base);
  margin-bottom: var(--space-lg);
}
```

#### Container Queries
Components respond to their container size:

```css
.shop-card {
  container-type: inline-size;
  container-name: shop-card;
}

@container shop-card (min-width: 500px) {
  .shop-card__content {
    flex-direction: row;
    align-items: stretch;
  }
}
```

#### BEM Methodology
Follow Block Element Modifier naming:

```css
/* Block */
.shop-card { }

/* Elements */
.shop-card__image { }
.shop-card__title { }
.shop-card__description { }

/* Modifiers */
.shop-card--featured { }
.shop-card--compact { }
```

### Accessibility Standards

All CSS must meet WCAG 2.1 AA compliance:

```css
/* Focus Management */
.interactive-element:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* High Contrast Support */
@media (prefers-contrast: high) {
  .component {
    border: 2px solid;
  }
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  .component {
    animation: none;
    transition: none;
  }
}
```

### Performance Optimization

#### Bundle Size Monitoring
- **Target Bundle Size**: < 60KB uncompressed
- **Critical CSS**: < 5KB for above-the-fold content
- **FontAwesome Subset**: Custom subset (99.6% size reduction)
- **Gzip Compression**: Achieve > 80% compression ratio

#### Development Workflow
1. **Edit CSS files** in `static/css/`
2. **Watch builds automatically** with `python dev_server.py`
3. **Analyze performance** with `npm run analyze:css`
4. **Test accessibility** with automated tools
5. **Lint before commit** with pre-commit hooks

### Pre-commit Hooks

The project includes automated quality checks:

```bash
# Install pre-commit hooks
pip install pre-commit  
pre-commit install

# Manual run
pre-commit run --all-files
```

Hooks include:
- CSS linting with Stylelint
- Python formatting with Black
- CSS build verification
- File size checks

### Production Build

Generate optimized production assets:

```bash
# Full production build
npm run build:css

# Generates:
# - static/build/bundle.min.css (complete bundle)
# - static/build/fontawesome-subset.min.css (icon subset)
# - static/build/critical.min.css (above-the-fold styles)
# - templates/base_production.html (optimized template)
```

### Component Development

#### Creating New Components

1. **Define component in `components-v2.css`**:
```css
.new-component {
  padding: var(--space-base);
  background: var(--color-surface);
  border-radius: var(--radius-base);
  container-type: inline-size;
  container-name: new-component;
}

@container new-component (min-width: 400px) {
  .new-component {
    padding: var(--space-lg);
  }
}
```

2. **Add accessibility features**:
```css
.new-component:focus-visible {
  outline: 2px solid var(--color-focus);
}

@media (prefers-reduced-motion: reduce) {
  .new-component {
    transition: none;
  }
}
```

3. **Document in COMPONENT_LIBRARY.md**

4. **Test with analysis tools**:
```bash
npm run analyze:css
```

### Troubleshooting

#### Common Issues

**Build Failures**:
```bash
# Clear build cache
rm -rf static/build/*
python build_css.py
```

**Linting Errors**:
```bash
# Auto-fix most issues
npm run lint:css --fix
```

**Hot Reload Not Working**:
```bash
# Restart development server
python dev_server.py --no-browser
```

**Performance Issues**:
```bash
# Analyze bundle size and usage
npm run analyze:css
```

For detailed component documentation, see [COMPONENT_LIBRARY.md](COMPONENT_LIBRARY.md)