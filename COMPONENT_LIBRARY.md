# Local Fare Component Library v2.0

## Overview

The Local Fare Component Library is a comprehensive design system built for scalability, accessibility, and performance. It features modern CSS techniques including container queries, fluid typography, and extensive accessibility support.

## Design System Architecture

### Phase 3 Enhancements
- **Container Queries**: Components adapt based on their container size, not viewport
- **Fluid Typography**: Responsive font sizes that scale smoothly
- **Enhanced Accessibility**: WCAG 2.1 AA compliance with ARIA support
- **Comprehensive Design Tokens**: 200+ design tokens for consistent theming

## Getting Started

### Installation

Include the CSS files in your HTML:

```html
<!-- Core design system -->
<link rel="stylesheet" href="css/design-system.css">

<!-- Component library -->
<link rel="stylesheet" href="css/components-v2.css">

<!-- Accessibility enhancements -->
<link rel="stylesheet" href="css/accessibility.css">
```

### Skip Links (Required for Accessibility)

Always include skip links at the top of your page:

```html
<div class="skip-links">
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <a href="#navigation" class="skip-link">Skip to navigation</a>
</div>
```

## Components

### Button System

Modern, accessible buttons with multiple variants and states.

#### Basic Usage

```html
<!-- Primary button -->
<button class="btn btn--primary btn--md">
  <i class="fas fa-home" aria-hidden="true"></i>
  Primary Action
</button>

<!-- Secondary button -->
<button class="btn btn--secondary btn--md">Secondary Action</button>

<!-- Outline button -->
<button class="btn btn--outline btn--md">Outline Button</button>

<!-- Ghost button -->
<button class="btn btn--ghost btn--md">Ghost Button</button>
```

#### Button Sizes

```html
<button class="btn btn--primary btn--sm">Small</button>
<button class="btn btn--primary btn--md">Medium</button>
<button class="btn btn--primary btn--lg">Large</button>
```

#### Button States

```html
<!-- Loading state -->
<button class="btn btn--primary btn--md btn--loading">Loading...</button>

<!-- Disabled state -->
<button class="btn btn--primary btn--md" disabled>Disabled</button>

<!-- Pressed state (for toggles) -->
<button class="btn btn--primary btn--md" aria-pressed="true">Toggle Active</button>
```

#### Accessibility Features

- Automatic focus management with visible focus indicators
- Support for `aria-pressed`, `aria-expanded`, and `aria-describedby`
- Minimum 44px touch target size
- High contrast mode support

### Card System with Container Queries

Responsive cards that adapt based on container size, not viewport.

#### Basic Card

```html
<div class="card-container">
  <div class="card">
    <div class="card__header">
      <h3 class="card__title">Card Title</h3>
      <p class="card__subtitle">Optional subtitle</p>
    </div>
    <div class="card__body">
      <p class="card__text">Card content goes here...</p>
    </div>
    <div class="card__footer">
      <button class="btn btn--primary btn--sm">Action</button>
    </div>
  </div>
</div>
```

#### Shop Card (Container Query Responsive)

```html
<div class="shop-card-container">
  <div class="card shop-card">
    <div class="shop-card__content">
      <div class="shop-card__image">
        <img src="shop-banner.jpg" alt="Farm Shop Banner">
        <!-- Fallback icon if no image -->
        <i class="fas fa-store" aria-hidden="true"></i>
      </div>
      
      <div class="shop-card__info">
        <h3 class="shop-card__title">Green Valley Farm</h3>
        <p class="shop-card__description">
          Fresh organic vegetables and herbs grown with care...
        </p>
        
        <div class="shop-card__meta">
          <div class="shop-card__status">
            <div class="shop-card__status-indicator" aria-hidden="true"></div>
            <span>Open</span>
          </div>
          
          <div class="shop-card__rating">
            <div class="stars" aria-label="4.5 out of 5 stars">
              <i class="fas fa-star" aria-hidden="true"></i>
              <i class="fas fa-star" aria-hidden="true"></i>
              <i class="fas fa-star" aria-hidden="true"></i>
              <i class="fas fa-star" aria-hidden="true"></i>
              <i class="fas fa-star-half-alt" aria-hidden="true"></i>
            </div>
            <span class="sr-only">4.5 out of 5 stars</span>
            <span>(24 reviews)</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

#### Container Query Behavior

- **< 300px**: Compact vertical layout
- **300px - 500px**: Standard vertical layout  
- **> 500px**: Horizontal layout with image on left

#### Product Card

```html
<div class="product-card-container">
  <div class="card product-card">
    <div class="card__body">
      <i class="fas fa-apple-alt product-card__icon" aria-hidden="true"></i>
      <div class="product-card__content">
        <h4 class="product-card__name">Organic Apples</h4>
        <div class="product-card__price">$4.99</div>
        <div class="product-card__unit">per lb</div>
        <span class="product-card__availability product-card__availability--available">
          Available
        </span>
      </div>
    </div>
  </div>
</div>
```

### Navigation System

Accessible, responsive navigation with keyboard support.

```html
<nav class="navbar" role="navigation" id="navigation">
  <div class="container">
    <a href="/" class="navbar__brand">
      <i class="fas fa-home" aria-hidden="true"></i>
      Local Fare
    </a>
    
    <ul class="navbar__nav">
      <li>
        <a href="/" class="navbar__link navbar__link--active" aria-current="page">
          <i class="fas fa-home" aria-hidden="true"></i>
          Home
        </a>
      </li>
      <li>
        <a href="/map" class="navbar__link">
          <i class="fas fa-map" aria-hidden="true"></i>
          Map
        </a>
      </li>
      <li>
        <a href="/search" class="navbar__link">
          <i class="fas fa-search" aria-hidden="true"></i>
          Search
        </a>
      </li>
    </ul>
  </div>
</nav>
```

### Form Components

Accessible forms with proper validation and error handling.

#### Basic Form Fields

```html
<div class="form-group">
  <label for="shop-name" class="form-label form-label--required">
    Shop Name
  </label>
  <input 
    type="text" 
    id="shop-name" 
    name="shop_name" 
    class="form-control"
    placeholder="Enter your shop name"
    required
    aria-describedby="shop-name-help shop-name-error"
  >
  <div id="shop-name-help" class="form-help">
    Choose a memorable name for your shop
  </div>
  <div id="shop-name-error" class="form-error" role="alert" style="display: none;">
    Shop name is required
  </div>
</div>
```

#### Textarea

```html
<div class="form-group">
  <label for="description" class="form-label">Description</label>
  <textarea 
    id="description" 
    name="description" 
    class="form-control form-textarea"
    placeholder="Describe your shop..."
    rows="4"
  ></textarea>
</div>
```

#### Select Dropdown

```html
<div class="form-group">
  <label for="category" class="form-label">Category</label>
  <select id="category" name="category" class="form-control form-select">
    <option value="">Choose a category</option>
    <option value="vegetables">Vegetables</option>
    <option value="fruits">Fruits</option>
    <option value="herbs">Herbs</option>
  </select>
</div>
```

### Alert System

Accessible alerts with proper ARIA roles.

```html
<!-- Success Alert -->
<div class="alert alert--success" role="alert">
  <i class="fas fa-check-circle alert__icon" aria-hidden="true"></i>
  <div class="alert__content">
    <strong>Success!</strong> Your shop has been created successfully.
  </div>
</div>

<!-- Error Alert -->
<div class="alert alert--error" role="alert">
  <i class="fas fa-exclamation-triangle alert__icon" aria-hidden="true"></i>
  <div class="alert__content">
    <strong>Error:</strong> Please check the required fields.
  </div>
</div>

<!-- Warning Alert -->
<div class="alert alert--warning" role="alert">
  <i class="fas fa-exclamation-triangle alert__icon" aria-hidden="true"></i>
  <div class="alert__content">
    <strong>Warning:</strong> Your shop will be automatically closed at midnight.
  </div>
</div>

<!-- Info Alert -->
<div class="alert alert--info" role="alert">
  <i class="fas fa-info-circle alert__icon" aria-hidden="true"></i>
  <div class="alert__content">
    <strong>Info:</strong> New features have been added to your dashboard.
  </div>
</div>
```

### Modal Dialog

Accessible modal with focus management.

```html
<div class="modal" role="dialog" aria-labelledby="modal-title" aria-describedby="modal-description">
  <div class="modal__backdrop"></div>
  <div class="modal__content">
    <div class="modal__header">
      <h2 id="modal-title" class="modal__title">Confirm Action</h2>
      <button class="modal__close" aria-label="Close dialog">
        <i class="fas fa-times" aria-hidden="true"></i>
      </button>
    </div>
    <div class="modal__body">
      <p id="modal-description">Are you sure you want to delete this item?</p>
    </div>
    <div class="modal__footer">
      <button class="btn btn--outline btn--md">Cancel</button>
      <button class="btn btn--primary btn--md">Delete</button>
    </div>
  </div>
</div>
```

## Design Tokens

### Color System

```css
/* Brand Colors */
--brand-primary: #2E7D32 (Forest Green)
--brand-secondary: #FF9800 (Warm Orange) 
--brand-accent: #81C784 (Light Green)

/* Surface Colors */
--surface-primary: #FAFAFA (Light Gray)
--surface-secondary: #F5F5F5 (Medium Gray)
--surface-elevated: #FFFFFF (White)

/* Text Colors */
--text-primary: #212121 (Dark Gray)
--text-secondary: #424242 (Medium Gray)
--text-tertiary: #757575 (Light Gray)
```

### Typography Scale (Fluid)

```css
/* Responsive typography that scales with viewport */
--text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)    /* 12-14px */
--text-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem)      /* 14-16px */
--text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem)    /* 16-18px */
--text-lg: clamp(1.125rem, 1rem + 0.5vw, 1.375rem)      /* 18-22px */
--text-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.625rem)    /* 20-26px */
```

### Spacing System (8px Base)

```css
--space-1: 0.25rem   /* 4px */
--space-2: 0.5rem    /* 8px */
--space-3: 0.75rem   /* 12px */
--space-4: 1rem      /* 16px */
--space-6: 1.5rem    /* 24px */
--space-8: 2rem      /* 32px */
```

## Accessibility Features

### WCAG 2.1 AA Compliance

- **Color Contrast**: All text meets 4.5:1 contrast ratio
- **Focus Management**: Visible focus indicators on all interactive elements
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader Support**: Proper ARIA labels and roles
- **High Contrast Mode**: Enhanced styles for high contrast preferences
- **Reduced Motion**: Respects `prefers-reduced-motion` settings

### Semantic HTML

Always use proper semantic HTML:

```html
<main role="main" id="main-content">
  <section role="region" aria-labelledby="featured-shops">
    <h2 id="featured-shops">Featured Shops</h2>
    <!-- Shop cards here -->
  </section>
  
  <aside role="complementary" aria-labelledby="sidebar-title">
    <h3 id="sidebar-title">Quick Actions</h3>
    <!-- Sidebar content -->
  </aside>
</main>
```

### Screen Reader Testing

Test with screen readers:
- **NVDA** (Windows, free)
- **JAWS** (Windows, paid)
- **VoiceOver** (macOS/iOS, built-in)
- **TalkBack** (Android, built-in)

## Browser Support

- **Modern Browsers**: Chrome 88+, Firefox 85+, Safari 14+, Edge 88+
- **Container Queries**: Chrome 105+, Firefox 110+, Safari 16+
- **Graceful Degradation**: Fallbacks for older browsers

## Performance

- **Critical CSS**: 4.7KB inlined for above-the-fold content
- **Component CSS**: 15KB gzipped for full component library
- **Container Queries**: Native browser support, no JavaScript required
- **FontAwesome Subset**: 99.6% smaller than full library

## Development Guidelines

### CSS Architecture

1. **Design Tokens First**: Always use design tokens for consistency
2. **Component Isolation**: Each component should be self-contained
3. **Container Queries**: Prefer container queries over media queries for components
4. **Accessibility First**: Consider accessibility from the start, not as an afterthought

### Naming Conventions

- **BEM Methodology**: `.block__element--modifier`
- **Semantic Names**: Use purpose-based names, not appearance-based
- **Consistent Prefixes**: Use consistent prefixes for related components

### Testing Checklist

- [ ] Keyboard navigation works
- [ ] Screen reader announces correctly
- [ ] High contrast mode displays properly
- [ ] Reduced motion preference respected
- [ ] Touch targets are minimum 44px
- [ ] Color contrast meets WCAG standards
- [ ] Components work in all supported browsers

## Migration from v1.0

### Breaking Changes

1. **Class Names**: Updated to BEM methodology
2. **Design Tokens**: New token system requires updates
3. **Container Queries**: Some responsive behavior changed

### Migration Steps

1. Update CSS imports to include new files
2. Replace old class names with new BEM classes
3. Update color variables to new design tokens
4. Test accessibility features
5. Verify container query behavior

### Compatibility Layer

For gradual migration, include compatibility CSS:

```css
/* Legacy support - remove after migration */
.btn-primary { @extend .btn--primary; }
.card-body { @extend .card__body; }
```

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Container Query Polyfill](https://github.com/GoogleChromeLabs/container-query-polyfill)
- [Color Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Screen Reader Testing Guide](https://webaim.org/articles/screenreader_testing/)

## Contributing

When adding new components:

1. Follow the established design token system
2. Include comprehensive accessibility features
3. Add container query support where appropriate
4. Document all ARIA requirements
5. Test with keyboard and screen readers
6. Provide usage examples