/**
 * Form validation and enhancement for Local Basket application
 */

class FormValidator {
  constructor() {
    this.forms = new Map();
    this.init();
  }

  /**
   * Initialize form validation
   */
  init() {
    document.addEventListener('DOMContentLoaded', () => {
      this.setupAllForms();
    });
  }

  /**
   * Setup validation for all forms
   */
  setupAllForms() {
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
      this.setupForm(form);
    });
  }

  /**
   * Setup validation for a specific form
   * @param {HTMLFormElement} form - Form element
   */
  setupForm(form) {
    const formId = form.id || `form-${Date.now()}`;
    const config = this.getFormConfig(form);
    
    this.forms.set(formId, {
      element: form,
      config: config,
      fields: new Map()
    });

    // Setup field validation
    this.setupFieldValidation(form, formId);
    
    // Setup form submission
    this.setupFormSubmission(form, formId);
    
    // Setup real-time validation
    this.setupRealTimeValidation(form, formId);
  }

  /**
   * Get form configuration
   * @param {HTMLFormElement} form - Form element
   * @returns {Object} Form configuration
   */
  getFormConfig(form) {
    const dataset = form.dataset;
    return {
      validateOnBlur: dataset.validateOnBlur !== 'false',
      validateOnInput: dataset.validateOnInput === 'true',
      showSuccessIcons: dataset.showSuccessIcons === 'true',
      preventSubmit: dataset.preventSubmit === 'true'
    };
  }

  /**
   * Setup field validation
   * @param {HTMLFormElement} form - Form element
   * @param {string} formId - Form ID
   */
  setupFieldValidation(form, formId) {
    const fields = form.querySelectorAll('[data-validation]');
    const formData = this.forms.get(formId);
    
    fields.forEach(field => {
      const rules = this.parseValidationRules(field.dataset.validation);
      const fieldId = field.id || field.name || `field-${Date.now()}`;
      
      formData.fields.set(fieldId, {
        element: field,
        rules: rules,
        isValid: false,
        errorMessage: null
      });

      this.createErrorElement(field);
    });
  }

  /**
   * Parse validation rules from data attribute
   * @param {string} rulesString - Rules string
   * @returns {Array} Parsed rules
   */
  parseValidationRules(rulesString) {
    const rules = [];
    const ruleStrings = rulesString.split('|');
    
    ruleStrings.forEach(ruleString => {
      const [rule, params] = ruleString.split(':');
      rules.push({
        rule: rule.trim(),
        params: params ? params.split(',').map(p => p.trim()) : []
      });
    });
    
    return rules;
  }

  /**
   * Create error element for field
   * @param {HTMLElement} field - Field element
   */
  createErrorElement(field) {
    const errorElement = document.createElement('div');
    errorElement.className = 'form-error';
    errorElement.id = `${field.id || field.name}-error`;
    errorElement.style.display = 'none';
    
    const formGroup = field.closest('.form-group');
    if (formGroup) {
      formGroup.appendChild(errorElement);
    } else {
      field.parentNode.insertBefore(errorElement, field.nextSibling);
    }
  }

  /**
   * Setup form submission validation
   * @param {HTMLFormElement} form - Form element
   * @param {string} formId - Form ID
   */
  setupFormSubmission(form, formId) {
    form.addEventListener('submit', (e) => {
      const isValid = this.validateForm(formId);
      
      if (!isValid) {
        e.preventDefault();
        this.focusFirstError(formId);
        Utils.showToast('Please correct the errors below', 'error');
      }
    });
  }

  /**
   * Setup real-time validation
   * @param {HTMLFormElement} form - Form element
   * @param {string} formId - Form ID
   */
  setupRealTimeValidation(form, formId) {
    const formData = this.forms.get(formId);
    
    formData.fields.forEach((fieldData, fieldId) => {
      const field = fieldData.element;
      
      if (formData.config.validateOnBlur) {
        field.addEventListener('blur', () => {
          this.validateField(formId, fieldId);
        });
      }
      
      if (formData.config.validateOnInput) {
        field.addEventListener('input', Utils.debounce(() => {
          this.validateField(formId, fieldId);
        }, 300));
      }
    });
  }

  /**
   * Validate entire form
   * @param {string} formId - Form ID
   * @returns {boolean} Is form valid
   */
  validateForm(formId) {
    const formData = this.forms.get(formId);
    if (!formData) return false;
    
    let isValid = true;
    
    formData.fields.forEach((fieldData, fieldId) => {
      const fieldValid = this.validateField(formId, fieldId);
      if (!fieldValid) {
        isValid = false;
      }
    });
    
    return isValid;
  }

  /**
   * Validate single field
   * @param {string} formId - Form ID
   * @param {string} fieldId - Field ID
   * @returns {boolean} Is field valid
   */
  validateField(formId, fieldId) {
    const formData = this.forms.get(formId);
    const fieldData = formData.fields.get(fieldId);
    
    if (!fieldData) return false;
    
    const field = fieldData.element;
    const value = field.value.trim();
    
    // Run validation rules
    for (const rule of fieldData.rules) {
      const result = this.runValidationRule(rule, value, field);
      if (!result.isValid) {
        this.showFieldError(field, result.message);
        fieldData.isValid = false;
        fieldData.errorMessage = result.message;
        return false;
      }
    }
    
    // Field is valid
    this.showFieldSuccess(field);
    fieldData.isValid = true;
    fieldData.errorMessage = null;
    return true;
  }

  /**
   * Run validation rule
   * @param {Object} rule - Validation rule
   * @param {string} value - Field value
   * @param {HTMLElement} field - Field element
   * @returns {Object} Validation result
   */
  runValidationRule(rule, value, field) {
    switch (rule.rule) {
      case 'required':
        return this.validateRequired(value);
      
      case 'email':
        return this.validateEmail(value);
      
      case 'min':
        return this.validateMin(value, parseInt(rule.params[0]));
      
      case 'max':
        return this.validateMax(value, parseInt(rule.params[0]));
      
      case 'minLength':
        return this.validateMinLength(value, parseInt(rule.params[0]));
      
      case 'maxLength':
        return this.validateMaxLength(value, parseInt(rule.params[0]));
      
      case 'pattern':
        return this.validatePattern(value, rule.params[0]);
      
      case 'phone':
        return this.validatePhone(value);
      
      case 'url':
        return this.validateUrl(value);
      
      case 'numeric':
        return this.validateNumeric(value);
      
      case 'decimal':
        return this.validateDecimal(value);
      
      case 'match':
        return this.validateMatch(value, rule.params[0]);
      
      case 'custom':
        return this.validateCustom(value, rule.params[0], field);
      
      default:
        return { isValid: true };
    }
  }

  /**
   * Validation rules
   */
  validateRequired(value) {
    return {
      isValid: value.length > 0,
      message: 'This field is required'
    };
  }

  validateEmail(value) {
    if (!value) return { isValid: true }; // Empty is valid unless required
    
    const isValid = Utils.validateEmail(value);
    return {
      isValid: isValid,
      message: 'Please enter a valid email address'
    };
  }

  validateMin(value, min) {
    if (!value) return { isValid: true };
    
    const num = parseFloat(value);
    return {
      isValid: !isNaN(num) && num >= min,
      message: `Value must be at least ${min}`
    };
  }

  validateMax(value, max) {
    if (!value) return { isValid: true };
    
    const num = parseFloat(value);
    return {
      isValid: !isNaN(num) && num <= max,
      message: `Value must be at most ${max}`
    };
  }

  validateMinLength(value, minLength) {
    if (!value) return { isValid: true };
    
    return {
      isValid: value.length >= minLength,
      message: `Must be at least ${minLength} characters`
    };
  }

  validateMaxLength(value, maxLength) {
    return {
      isValid: value.length <= maxLength,
      message: `Must be no more than ${maxLength} characters`
    };
  }

  validatePattern(value, pattern) {
    if (!value) return { isValid: true };
    
    const regex = new RegExp(pattern);
    return {
      isValid: regex.test(value),
      message: 'Invalid format'
    };
  }

  validatePhone(value) {
    if (!value) return { isValid: true };
    
    const isValid = Utils.validatePhone(value);
    return {
      isValid: isValid,
      message: 'Please enter a valid phone number'
    };
  }

  validateUrl(value) {
    if (!value) return { isValid: true };
    
    try {
      new URL(value);
      return { isValid: true };
    } catch {
      return {
        isValid: false,
        message: 'Please enter a valid URL'
      };
    }
  }

  validateNumeric(value) {
    if (!value) return { isValid: true };
    
    return {
      isValid: !isNaN(value) && !isNaN(parseFloat(value)),
      message: 'Must be a number'
    };
  }

  validateDecimal(value) {
    if (!value) return { isValid: true };
    
    const regex = /^\d+(\.\d{1,2})?$/;
    return {
      isValid: regex.test(value),
      message: 'Must be a valid decimal number'
    };
  }

  validateMatch(value, targetFieldId) {
    const targetField = document.getElementById(targetFieldId);
    if (!targetField) return { isValid: true };
    
    return {
      isValid: value === targetField.value,
      message: 'Fields do not match'
    };
  }

  validateCustom(value, functionName, field) {
    if (typeof window[functionName] === 'function') {
      return window[functionName](value, field);
    }
    return { isValid: true };
  }

  /**
   * Show field error
   * @param {HTMLElement} field - Field element
   * @param {string} message - Error message
   */
  showFieldError(field, message) {
    const errorElement = document.getElementById(`${field.id || field.name}-error`);
    if (errorElement) {
      errorElement.textContent = message;
      errorElement.style.display = 'block';
    }
    
    field.classList.add('is-invalid');
    field.classList.remove('is-valid');
  }

  /**
   * Show field success
   * @param {HTMLElement} field - Field element
   */
  showFieldSuccess(field) {
    const errorElement = document.getElementById(`${field.id || field.name}-error`);
    if (errorElement) {
      errorElement.style.display = 'none';
    }
    
    field.classList.remove('is-invalid');
    field.classList.add('is-valid');
  }

  /**
   * Focus first error field
   * @param {string} formId - Form ID
   */
  focusFirstError(formId) {
    const formData = this.forms.get(formId);
    if (!formData) return;
    
    for (const [fieldId, fieldData] of formData.fields) {
      if (!fieldData.isValid) {
        fieldData.element.focus();
        break;
      }
    }
  }

  /**
   * Clear form validation
   * @param {string} formId - Form ID
   */
  clearValidation(formId) {
    const formData = this.forms.get(formId);
    if (!formData) return;
    
    formData.fields.forEach((fieldData, fieldId) => {
      const field = fieldData.element;
      field.classList.remove('is-invalid', 'is-valid');
      
      const errorElement = document.getElementById(`${field.id || field.name}-error`);
      if (errorElement) {
        errorElement.style.display = 'none';
      }
    });
  }
}

// Initialize form validator
window.FormValidator = new FormValidator();