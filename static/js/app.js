/**
 * Main application JavaScript for Local Basket
 */

class LocalBasketApp {
  constructor() {
    this.init();
  }

  /**
   * Initialize application
   */
  init() {
    document.addEventListener('DOMContentLoaded', () => {
      this.setupEventListeners();
      this.initializeComponents();
      this.setupFlashMessages();
    });
  }

  /**
   * Setup global event listeners
   */
  setupEventListeners() {
    // Mobile menu toggle
    this.setupMobileMenu();
    
    // Search functionality
    this.setupSearch();
    
    // Shop filters
    this.setupShopFilters();
    
    // Product interactions
    this.setupProductInteractions();
    
    // Review system
    this.setupReviewSystem();
  }

  /**
   * Initialize components
   */
  initializeComponents() {
    // Initialize map if on map page
    if (document.getElementById('map-container')) {
      this.initializeMap();
    }
    
    // Initialize location services
    this.initializeLocationServices();
    
    // Initialize image uploads
    this.initializeImageUploads();
  }

  /**
   * Setup mobile menu
   */
  setupMobileMenu() {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileToggle && mobileMenu) {
      mobileToggle.addEventListener('click', () => {
        mobileMenu.classList.toggle('active');
      });
      
      // Close menu when clicking outside
      document.addEventListener('click', (e) => {
        if (!mobileMenu.contains(e.target) && !mobileToggle.contains(e.target)) {
          mobileMenu.classList.remove('active');
        }
      });
    }
  }

  /**
   * Setup search functionality
   */
  setupSearch() {
    const searchInput = document.getElementById('search-input');
    const searchFilters = document.querySelector('.search-filters');
    
    if (searchInput) {
      searchInput.addEventListener('input', Utils.debounce((e) => {
        this.performSearch(e.target.value);
      }, 300));
    }
    
    if (searchFilters) {
      searchFilters.addEventListener('change', (e) => {
        this.updateFilters();
      });
    }
  }

  /**
   * Setup shop filters
   */
  setupShopFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const sortSelect = document.getElementById('sort-select');
    
    filterButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        e.preventDefault();
        this.toggleFilter(button);
      });
    });
    
    if (sortSelect) {
      sortSelect.addEventListener('change', (e) => {
        this.sortShops(e.target.value);
      });
    }
  }

  /**
   * Setup product interactions
   */
  setupProductInteractions() {
    // Product availability toggle
    const availabilityToggles = document.querySelectorAll('.availability-toggle');
    availabilityToggles.forEach(toggle => {
      toggle.addEventListener('change', (e) => {
        this.toggleProductAvailability(e.target);
      });
    });
    
    // Product quick actions
    const quickActionButtons = document.querySelectorAll('.quick-action');
    quickActionButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        this.handleQuickAction(e.target);
      });
    });
  }

  /**
   * Setup review system
   */
  setupReviewSystem() {
    // Star rating input
    const starRatings = document.querySelectorAll('.star-rating');
    starRatings.forEach(rating => {
      this.setupStarRating(rating);
    });
    
    // Review form
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
      reviewForm.addEventListener('submit', (e) => {
        this.submitReview(e);
      });
    }
  }

  /**
   * Initialize map
   */
  async initializeMap() {
    try {
      await MapService.init('map-container', {
        zoom: 12,
        center: { lat: 40.7128, lng: -74.0060 }
      });
      
      MapService.initControls();
      
    } catch (error) {
      console.error('Failed to initialize map:', error);
    }
  }

  /**
   * Initialize location services
   */
  initializeLocationServices() {
    const locationButtons = document.querySelectorAll('.location-btn');
    
    locationButtons.forEach(button => {
      button.addEventListener('click', async (e) => {
        e.preventDefault();
        await this.requestLocation(button);
      });
    });
  }

  /**
   * Initialize image uploads
   */
  initializeImageUploads() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(input => {
      input.addEventListener('change', (e) => {
        this.handleImageUpload(e.target);
      });
    });
  }

  /**
   * Setup flash messages
   */
  setupFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
      // Auto-dismiss after 5 seconds
      setTimeout(() => {
        message.style.opacity = '0';
        setTimeout(() => {
          message.remove();
        }, 300);
      }, 5000);
      
      // Manual dismiss
      const closeBtn = message.querySelector('.alert-close');
      if (closeBtn) {
        closeBtn.addEventListener('click', () => {
          message.remove();
        });
      }
    });
  }

  /**
   * Perform search
   * @param {string} query - Search query
   */
  async performSearch(query) {
    try {
      const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
      const results = await response.json();
      
      this.displaySearchResults(results);
      
    } catch (error) {
      console.error('Search failed:', error);
      Utils.showToast('Search failed. Please try again.', 'error');
    }
  }

  /**
   * Display search results
   * @param {Array} results - Search results
   */
  displaySearchResults(results) {
    const resultsContainer = document.getElementById('search-results');
    if (!resultsContainer) return;
    
    if (results.length === 0) {
      resultsContainer.innerHTML = '<p class="text-muted">No results found.</p>';
      return;
    }
    
    const html = results.map(result => {
      if (result.type === 'shop') {
        return this.renderShopCard(result);
      } else if (result.type === 'product') {
        return this.renderProductCard(result);
      }
    }).join('');
    
    resultsContainer.innerHTML = html;
  }

  /**
   * Render shop card
   * @param {Object} shop - Shop data
   * @returns {string} HTML string
   */
  renderShopCard(shop) {
    const status = shop.is_open ? 'Open' : 'Closed';
    const statusClass = shop.is_open ? 'text-success' : 'text-error';
    const stars = Utils.generateStars(shop.rating || 0);
    
    return `
      <div class="col-md-6 col-lg-4 mb-4">
        <div class="card shop-card">
          <div class="card-header shop-card-header">
            ${Utils.sanitizeHTML(shop.name)}
          </div>
          <div class="card-body">
            <p class="shop-card-text">${Utils.sanitizeHTML(shop.description || '')}</p>
            <div class="shop-rating mb-2">
              ${stars} (${(shop.rating || 0).toFixed(1)})
            </div>
            <p class="text-muted">
              <i class="fas fa-map-marker-alt"></i> ${Utils.sanitizeHTML(shop.address)}
            </p>
          </div>
          <div class="card-footer">
            <div class="d-flex justify-content-between align-items-center">
              <span class="shop-status ${statusClass}">
                <i class="fas fa-circle"></i> ${status}
              </span>
              <a href="/shop/${shop.id}" class="btn btn-primary btn-sm">
                View Shop
              </a>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  /**
   * Render product card
   * @param {Object} product - Product data
   * @returns {string} HTML string
   */
  renderProductCard(product) {
    const price = Utils.formatPrice(product.price);
    const availability = product.is_available ? 'Available' : 'Out of Stock';
    const availabilityClass = product.is_available ? 'available' : 'unavailable';
    
    return `
      <div class="col-md-6 col-lg-3 mb-4">
        <div class="card product-card">
          <div class="card-body text-center">
            <div class="product-icon">
              <i class="${product.icon_class || 'fas fa-apple-alt'}"></i>
            </div>
            <h5 class="product-name">${Utils.sanitizeHTML(product.name)}</h5>
            <p class="product-price">${price}</p>
            <p class="product-unit text-muted">per ${Utils.sanitizeHTML(product.unit)}</p>
            <p class="product-availability ${availabilityClass}">
              ${availability}
            </p>
            <a href="/shop/${product.shop_id}" class="btn btn-outline-primary btn-sm">
              View Shop
            </a>
          </div>
        </div>
      </div>
    `;
  }

  /**
   * Toggle filter
   * @param {HTMLElement} button - Filter button
   */
  toggleFilter(button) {
    button.classList.toggle('active');
    this.updateFilters();
  }

  /**
   * Update filters
   */
  updateFilters() {
    const activeFilters = document.querySelectorAll('.filter-btn.active');
    const filters = Array.from(activeFilters).map(btn => btn.dataset.filter);
    
    // Apply filters to current view
    this.applyFilters(filters);
  }

  /**
   * Apply filters
   * @param {Array} filters - Active filters
   */
  applyFilters(filters) {
    const items = document.querySelectorAll('.filterable-item');
    
    items.forEach(item => {
      const itemFilters = item.dataset.filters ? item.dataset.filters.split(',') : [];
      const shouldShow = filters.length === 0 || filters.some(filter => itemFilters.includes(filter));
      
      item.style.display = shouldShow ? '' : 'none';
    });
  }

  /**
   * Sort shops
   * @param {string} sortBy - Sort criteria
   */
  sortShops(sortBy) {
    const container = document.querySelector('.shop-grid');
    if (!container) return;
    
    const shops = Array.from(container.children);
    
    shops.sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.querySelector('.shop-card-title').textContent.localeCompare(
            b.querySelector('.shop-card-title').textContent
          );
        case 'rating':
          const ratingA = parseFloat(a.dataset.rating || '0');
          const ratingB = parseFloat(b.dataset.rating || '0');
          return ratingB - ratingA;
        case 'distance':
          const distanceA = parseFloat(a.dataset.distance || '999');
          const distanceB = parseFloat(b.dataset.distance || '999');
          return distanceA - distanceB;
        default:
          return 0;
      }
    });
    
    // Re-append sorted elements
    shops.forEach(shop => container.appendChild(shop));
  }

  /**
   * Toggle product availability
   * @param {HTMLElement} toggle - Toggle element
   */
  async toggleProductAvailability(toggle) {
    const productId = toggle.dataset.productId;
    const isAvailable = toggle.checked;
    
    try {
      const response = await fetch(`/api/products/${productId}/availability`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ is_available: isAvailable })
      });
      
      if (response.ok) {
        Utils.showToast('Product availability updated', 'success');
      } else {
        throw new Error('Failed to update availability');
      }
      
    } catch (error) {
      console.error('Failed to update product availability:', error);
      toggle.checked = !isAvailable; // Revert toggle
      Utils.showToast('Failed to update availability', 'error');
    }
  }

  /**
   * Handle quick action
   * @param {HTMLElement} button - Action button
   */
  handleQuickAction(button) {
    const action = button.dataset.action;
    const targetId = button.dataset.targetId;
    
    switch (action) {
      case 'copy-payment':
        this.copyPaymentInfo(targetId);
        break;
      case 'share-shop':
        this.shareShop(targetId);
        break;
      case 'report-shop':
        this.reportShop(targetId);
        break;
      default:
        console.warn('Unknown quick action:', action);
    }
  }

  /**
   * Copy payment info
   * @param {string} paymentInfo - Payment information
   */
  async copyPaymentInfo(paymentInfo) {
    try {
      await Utils.copyToClipboard(paymentInfo);
      Utils.showToast('Payment info copied to clipboard', 'success');
    } catch (error) {
      Utils.showToast('Failed to copy payment info', 'error');
    }
  }

  /**
   * Share shop
   * @param {string} shopId - Shop ID
   */
  async shareShop(shopId) {
    const url = `${window.location.origin}/shop/${shopId}`;
    
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Check out this local shop!',
          url: url
        });
      } catch (error) {
        if (error.name !== 'AbortError') {
          console.error('Share failed:', error);
        }
      }
    } else {
      // Fallback to clipboard
      await Utils.copyToClipboard(url);
      Utils.showToast('Shop link copied to clipboard', 'success');
    }
  }

  /**
   * Report shop
   * @param {string} shopId - Shop ID
   */
  reportShop(shopId) {
    // This would open a modal or navigate to a report form
    Utils.showToast('Report feature coming soon', 'info');
  }

  /**
   * Setup star rating
   * @param {HTMLElement} ratingElement - Rating element
   */
  setupStarRating(ratingElement) {
    const stars = ratingElement.querySelectorAll('.star');
    const input = ratingElement.querySelector('input[type="hidden"]');
    
    stars.forEach((star, index) => {
      star.addEventListener('click', () => {
        const rating = index + 1;
        input.value = rating;
        
        // Update visual state
        stars.forEach((s, i) => {
          s.classList.toggle('active', i < rating);
        });
      });
      
      star.addEventListener('mouseenter', () => {
        stars.forEach((s, i) => {
          s.classList.toggle('hover', i <= index);
        });
      });
    });
    
    ratingElement.addEventListener('mouseleave', () => {
      stars.forEach(s => s.classList.remove('hover'));
    });
  }

  /**
   * Submit review
   * @param {Event} e - Submit event
   */
  async submitReview(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    
    try {
      const response = await fetch(form.action, {
        method: 'POST',
        body: formData
      });
      
      if (response.ok) {
        Utils.showToast('Review submitted successfully', 'success');
        form.reset();
        
        // Reload reviews section
        setTimeout(() => {
          window.location.reload();
        }, 1000);
      } else {
        throw new Error('Failed to submit review');
      }
      
    } catch (error) {
      console.error('Review submission failed:', error);
      Utils.showToast('Failed to submit review', 'error');
    }
  }

  /**
   * Request location
   * @param {HTMLElement} button - Location button
   */
  async requestLocation(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Getting location...';
    button.disabled = true;
    
    try {
      const position = await GeolocationService.getCurrentPosition();
      const { latitude, longitude } = position.coords;
      
      // Update hidden form fields if they exist
      const latInput = document.getElementById('latitude');
      const lonInput = document.getElementById('longitude');
      
      if (latInput) latInput.value = latitude;
      if (lonInput) lonInput.value = longitude;
      
      Utils.showToast('Location found successfully', 'success');
      
    } catch (error) {
      console.error('Location request failed:', error);
      Utils.showToast(`Location error: ${error.message}`, 'error');
    } finally {
      button.innerHTML = originalText;
      button.disabled = false;
    }
  }

  /**
   * Handle image upload
   * @param {HTMLInputElement} input - File input
   */
  handleImageUpload(input) {
    const file = input.files[0];
    if (!file) return;
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
      Utils.showToast('Please select an image file', 'error');
      input.value = '';
      return;
    }
    
    // Validate file size (5MB max)
    if (file.size > 5 * 1024 * 1024) {
      Utils.showToast('Image must be smaller than 5MB', 'error');
      input.value = '';
      return;
    }
    
    // Show preview if preview element exists
    const preview = document.getElementById(input.dataset.preview);
    if (preview) {
      const reader = new FileReader();
      reader.onload = (e) => {
        preview.src = e.target.result;
        preview.style.display = 'block';
      };
      reader.readAsDataURL(file);
    }
  }
}

// Initialize application
window.LocalBasketApp = new LocalBasketApp();