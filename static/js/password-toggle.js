/**
 * Password visibility toggle functionality
 * As specified in web-app-idea.md: "provide ability to view password which is common now a days"
 */

class PasswordToggle {
  constructor() {
    this.init();
  }

  init() {
    document.addEventListener('DOMContentLoaded', () => {
      this.setupPasswordToggles();
    });
  }

  setupPasswordToggles() {
    const passwordFields = document.querySelectorAll('input[type="password"]');
    
    passwordFields.forEach(field => {
      this.addToggleButton(field);
    });
  }

  addToggleButton(passwordField) {
    // Create wrapper if it doesn't exist
    let wrapper = passwordField.parentElement;
    if (!wrapper.classList.contains('password-field-wrapper')) {
      wrapper = document.createElement('div');
      wrapper.className = 'password-field-wrapper';
      passwordField.parentNode.insertBefore(wrapper, passwordField);
      wrapper.appendChild(passwordField);
    }

    // Create toggle button
    const toggleButton = document.createElement('button');
    toggleButton.type = 'button';
    toggleButton.className = 'password-toggle-btn';
    toggleButton.innerHTML = '<i class="fas fa-eye"></i>';
    toggleButton.setAttribute('aria-label', 'Toggle password visibility');
    
    // Add click event
    toggleButton.addEventListener('click', () => {
      this.togglePasswordVisibility(passwordField, toggleButton);
    });

    wrapper.appendChild(toggleButton);
  }

  togglePasswordVisibility(passwordField, toggleButton) {
    const icon = toggleButton.querySelector('i');
    
    if (passwordField.type === 'password') {
      passwordField.type = 'text';
      icon.classList.remove('fa-eye');
      icon.classList.add('fa-eye-slash');
      toggleButton.setAttribute('aria-label', 'Hide password');
    } else {
      passwordField.type = 'password';
      icon.classList.remove('fa-eye-slash');
      icon.classList.add('fa-eye');
      toggleButton.setAttribute('aria-label', 'Show password');
    }
  }
}

// Initialize password toggle functionality
new PasswordToggle();