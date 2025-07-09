/**
 * Utility functions for Local Basket application
 */

class Utils {
  /**
   * Debounce function to limit function calls
   * @param {Function} func - Function to debounce
   * @param {number} wait - Wait time in milliseconds
   * @param {boolean} immediate - Execute immediately
   * @returns {Function} Debounced function
   */
  static debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        timeout = null;
        if (!immediate) func(...args);
      };
      const callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) func(...args);
    };
  }

  /**
   * Throttle function to limit function calls
   * @param {Function} func - Function to throttle
   * @param {number} limit - Time limit in milliseconds
   * @returns {Function} Throttled function
   */
  static throttle(func, limit) {
    let inThrottle;
    return function(...args) {
      if (!inThrottle) {
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }

  /**
   * Format distance for display
   * @param {number} distance - Distance in kilometers
   * @param {string} unit - Unit (km or mi)
   * @returns {string} Formatted distance
   */
  static formatDistance(distance, unit = 'km') {
    if (unit === 'km') {
      return distance < 1 ? `${Math.round(distance * 1000)}m` : `${distance.toFixed(1)}km`;
    } else {
      return distance < 1 ? `${Math.round(distance * 5280)}ft` : `${distance.toFixed(1)}mi`;
    }
  }

  /**
   * Format price for display
   * @param {number} price - Price value
   * @param {string} currency - Currency symbol
   * @returns {string} Formatted price
   */
  static formatPrice(price, currency = '$') {
    return `${currency}${price.toFixed(2)}`;
  }

  /**
   * Generate star rating HTML
   * @param {number} rating - Rating value (0-5)
   * @param {number} maxStars - Maximum number of stars
   * @returns {string} HTML string for stars
   */
  static generateStars(rating, maxStars = 5) {
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 >= 0.5;
    const emptyStars = maxStars - fullStars - (halfStar ? 1 : 0);
    
    let starsHtml = '';
    
    // Full stars
    for (let i = 0; i < fullStars; i++) {
      starsHtml += '<i class="fas fa-star"></i>';
    }
    
    // Half star
    if (halfStar) {
      starsHtml += '<i class="fas fa-star-half-alt"></i>';
    }
    
    // Empty stars
    for (let i = 0; i < emptyStars; i++) {
      starsHtml += '<i class="far fa-star"></i>';
    }
    
    return starsHtml;
  }

  /**
   * Validate email format
   * @param {string} email - Email to validate
   * @returns {boolean} Is valid email
   */
  static validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  /**
   * Validate phone number format
   * @param {string} phone - Phone number to validate
   * @returns {boolean} Is valid phone number
   */
  static validatePhone(phone) {
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
  }

  /**
   * Sanitize HTML to prevent XSS
   * @param {string} html - HTML string to sanitize
   * @returns {string} Sanitized HTML
   */
  static sanitizeHTML(html) {
    const temp = document.createElement('div');
    temp.textContent = html;
    return temp.innerHTML;
  }

  /**
   * Get URL parameters
   * @param {string} param - Parameter name
   * @returns {string|null} Parameter value
   */
  static getUrlParameter(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
  }

  /**
   * Set URL parameter without page reload
   * @param {string} param - Parameter name
   * @param {string} value - Parameter value
   */
  static setUrlParameter(param, value) {
    const url = new URL(window.location);
    url.searchParams.set(param, value);
    window.history.replaceState({}, '', url);
  }

  /**
   * Format date for display
   * @param {Date|string} date - Date to format
   * @param {Object} options - Formatting options
   * @returns {string} Formatted date
   */
  static formatDate(date, options = {}) {
    const defaultOptions = {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    };
    
    const formatOptions = { ...defaultOptions, ...options };
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    
    return dateObj.toLocaleDateString('en-US', formatOptions);
  }

  /**
   * Calculate time ago
   * @param {Date|string} date - Date to calculate from
   * @returns {string} Time ago string
   */
  static timeAgo(date) {
    const now = new Date();
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    const seconds = Math.floor((now - dateObj) / 1000);
    
    const intervals = {
      year: 31536000,
      month: 2592000,
      week: 604800,
      day: 86400,
      hour: 3600,
      minute: 60
    };
    
    for (const [unit, secondsInUnit] of Object.entries(intervals)) {
      const interval = Math.floor(seconds / secondsInUnit);
      if (interval >= 1) {
        return `${interval} ${unit}${interval > 1 ? 's' : ''} ago`;
      }
    }
    
    return 'Just now';
  }

  /**
   * Copy text to clipboard
   * @param {string} text - Text to copy
   * @returns {Promise<boolean>} Success status
   */
  static async copyToClipboard(text) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (err) {
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.style.position = 'fixed';
      textArea.style.opacity = '0';
      document.body.appendChild(textArea);
      textArea.select();
      
      try {
        document.execCommand('copy');
        return true;
      } catch (fallbackErr) {
        return false;
      } finally {
        document.body.removeChild(textArea);
      }
    }
  }

  /**
   * Show toast notification
   * @param {string} message - Message to display
   * @param {string} type - Type of toast (success, error, warning, info)
   * @param {number} duration - Duration in milliseconds
   */
  static showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} flash-message`;
    toast.innerHTML = `
      ${Utils.sanitizeHTML(message)}
      <button type="button" class="alert-close" onclick="this.parentElement.remove()">
        <i class="fas fa-times"></i>
      </button>
    `;
    
    let container = document.querySelector('.flash-messages');
    if (!container) {
      container = document.createElement('div');
      container.className = 'flash-messages';
      document.body.appendChild(container);
    }
    
    container.appendChild(toast);
    
    // Auto-remove after duration
    setTimeout(() => {
      if (toast.parentElement) {
        toast.remove();
      }
    }, duration);
  }

  /**
   * Load script dynamically
   * @param {string} src - Script source URL
   * @returns {Promise<void>} Promise that resolves when script is loaded
   */
  static loadScript(src) {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = src;
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  /**
   * Check if element is in viewport
   * @param {HTMLElement} element - Element to check
   * @returns {boolean} Is element in viewport
   */
  static isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  }

  /**
   * Smooth scroll to element
   * @param {HTMLElement|string} target - Element or selector
   * @param {number} offset - Offset from top
   */
  static scrollToElement(target, offset = 0) {
    const element = typeof target === 'string' ? document.querySelector(target) : target;
    if (element) {
      const targetPosition = element.offsetTop - offset;
      window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      });
    }
  }
}

// Export for use in other modules
window.Utils = Utils;