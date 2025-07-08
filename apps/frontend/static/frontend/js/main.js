/**
 * Frontend Main JavaScript
 * Interactive features for Credentials Manager Frontend
 */

// DOM ready utility
function ready(fn) {
    if (document.readyState !== 'loading') {
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}

// CSRF token utility - improved for better production compatibility
function getCSRFToken() {
    // Try multiple methods to get CSRF token
    
    // Method 1: Try meta tag (most reliable for AJAX)
    const metaTag = document.querySelector('meta[name=csrf-token]');
    if (metaTag) {
        return metaTag.getAttribute('content');
    }
    
    // Method 2: Try cookie (Django's default for AJAX)
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='));
    if (cookieValue) {
        return cookieValue.split('=')[1];
    }
    
    // Method 3: Try form input (fallback)
    const formToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (formToken) {
        return formToken.value;
    }
    
    // Method 4: Try hidden input in any form
    const anyForm = document.querySelector('form input[name=csrfmiddlewaretoken]');
    if (anyForm) {
        return anyForm.value;
    }
    
    console.error('CSRF token not found! This will cause 403 errors on API calls.');
    return null;
}

// API utilities
const API = {
    async request(url, options = {}) {
        const defaults = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            credentials: 'same-origin'
        };
        
        const config = { ...defaults, ...options };
        if (config.headers) {
            config.headers = { ...defaults.headers, ...options.headers };
        }
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            
            return await response.text();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    },
    
    async get(url) {
        return this.request(url, { method: 'GET' });
    },
    
    async post(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
};

// Notification system
const Notifications = {
    show(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        // Add styles if not already present
        if (!document.querySelector('#notification-styles')) {
            const styles = document.createElement('style');
            styles.id = 'notification-styles';
            styles.textContent = `
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    min-width: 300px;
                    padding: 1rem;
                    border-radius: 0.375rem;
                    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
                    z-index: 1050;
                    animation: slideIn 0.3s ease-out;
                }
                .notification-info { background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }
                .notification-success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
                .notification-warning { background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; }
                .notification-error { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
                .notification-content { display: flex; justify-content: space-between; align-items: center; }
                .notification-close { background: none; border: none; cursor: pointer; padding: 0; }
                @keyframes slideIn { from { transform: translateX(100%); } to { transform: translateX(0); } }
            `;
            document.head.appendChild(styles);
        }
        
        document.body.appendChild(notification);
        
        if (duration > 0) {
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, duration);
        }
    },
    
    success(message, duration) { this.show(message, 'success', duration); },
    error(message, duration) { this.show(message, 'error', duration); },
    warning(message, duration) { this.show(message, 'warning', duration); },
    info(message, duration) { this.show(message, 'info', duration); }
};

// Toggle favorite functionality
async function toggleFavorite(type, id, iconElement) {
    const originalClass = iconElement.className;
    const originalColor = iconElement.style.color;
    
    // Debug information
    console.log('Toggle favorite called:', { type, id, iconElement });
    const csrfToken = getCSRFToken();
    console.log('CSRF token available:', csrfToken ? 'Yes' : 'No', csrfToken ? csrfToken.substring(0, 10) + '...' : 'null');
    
    try {
        // Show loading state
        iconElement.className = 'fas fa-spinner fa-spin';
        iconElement.style.color = '#6c757d';
        
        const response = await API.post('/api/toggle-favorite/', {
            type: type,
            id: parseInt(id)
        });
        
        if (response.success) {
            // Update icon based on new favorite status
            if (response.is_favorite) {
                iconElement.className = 'fas fa-star';
                iconElement.style.color = '#ffc107';
            } else {
                iconElement.className = 'far fa-star';
                iconElement.style.color = '#6c757d';
            }
            
            Notifications.success(response.message || 'Favorite status updated');
        } else {
            throw new Error(response.error || 'Failed to toggle favorite');
        }
    } catch (error) {
        console.error('Toggle favorite failed:', error);
        console.error('Error details:', {
            message: error.message,
            stack: error.stack,
            type: typeof error,
            response: error.response || 'No response data'
        });
        
        // Restore original state
        iconElement.className = originalClass;
        iconElement.style.color = originalColor;
        
        // Better error messages based on error type
        if (error.message.includes('403')) {
            Notifications.error('Security error: Please refresh the page and try again');
            console.error('CSRF token issue detected. Current token:', getCSRFToken());
        } else if (error.message.includes('404')) {
            Notifications.error('API endpoint not found');
        } else if (error.message.includes('500')) {
            Notifications.error('Server error: Please try again later');
        } else {
            Notifications.error('Failed to update favorite status: ' + error.message);
        }
    }
}

// Search functionality
class SearchManager {
    constructor() {
        this.searchInput = null;
        this.searchForm = null;
        this.debounceTimer = null;
        this.init();
    }
    
    init() {
        ready(() => {
            this.searchInput = document.querySelector('#search-input, input[name="query"]');
            this.searchForm = document.querySelector('#search-form, form[method="get"]');
            
            if (this.searchInput) {
                this.setupEventListeners();
            }
        });
    }
    
    setupEventListeners() {
        // Real-time search with debouncing
        this.searchInput.addEventListener('input', (e) => {
            clearTimeout(this.debounceTimer);
            this.debounceTimer = setTimeout(() => {
                this.performSearch(e.target.value);
            }, 300);
        });
        
        // Clear search
        const clearButton = document.querySelector('#clear-search');
        if (clearButton) {
            clearButton.addEventListener('click', () => {
                this.clearSearch();
            });
        }
    }
    
    async performSearch(query) {
        if (query.length < 2) return;
        
        try {
            const response = await API.post('/api/search/', {
                query: query,
                limit: 10
            });
            
            this.displaySearchResults(response);
        } catch (error) {
            console.error('Search failed:', error);
        }
    }
    
    displaySearchResults(results) {
        // This would be implemented based on the specific search UI
        console.log('Search results:', results);
    }
    
    clearSearch() {
        if (this.searchInput) {
            this.searchInput.value = '';
            this.searchInput.focus();
        }
    }
}

// Form utilities
const FormUtils = {
    // Auto-save form data to localStorage
    autoSave(formSelector, key) {
        const form = document.querySelector(formSelector);
        if (!form) return;
        
        // Load saved data
        const saved = localStorage.getItem(key);
        if (saved) {
            try {
                const data = JSON.parse(saved);
                Object.keys(data).forEach(fieldName => {
                    const field = form.querySelector(`[name="${fieldName}"]`);
                    if (field && field.type !== 'password') {
                        field.value = data[fieldName];
                    }
                });
            } catch (error) {
                console.error('Failed to load saved form data:', error);
            }
        }
        
        // Save on input
        form.addEventListener('input', () => {
            const formData = new FormData(form);
            const data = {};
            
            for (let [key, value] of formData.entries()) {
                const field = form.querySelector(`[name="${key}"]`);
                if (field && field.type !== 'password') {
                    data[key] = value;
                }
            }
            
            localStorage.setItem(key, JSON.stringify(data));
        });
        
        // Clear on submit
        form.addEventListener('submit', () => {
            localStorage.removeItem(key);
        });
    },
    
    // Form validation
    validate(form) {
        const errors = [];
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                errors.push(`${field.name} is required`);
                field.classList.add('is-invalid');
            } else {
                field.classList.remove('is-invalid');
            }
        });
        
        return errors;
    },
    
    // Password strength indicator
    setupPasswordStrength(passwordFieldSelector) {
        const passwordField = document.querySelector(passwordFieldSelector);
        if (!passwordField) return;
        
        const strengthIndicator = document.createElement('div');
        strengthIndicator.className = 'password-strength';
        strengthIndicator.innerHTML = `
            <div class="strength-bar">
                <div class="strength-fill"></div>
            </div>
            <div class="strength-text">Password strength: <span class="strength-level">Weak</span></div>
        `;
        
        // Add styles
        if (!document.querySelector('#password-strength-styles')) {
            const styles = document.createElement('style');
            styles.id = 'password-strength-styles';
            styles.textContent = `
                .password-strength { margin-top: 0.5rem; }
                .strength-bar { width: 100%; height: 4px; background: #e9ecef; border-radius: 2px; overflow: hidden; }
                .strength-fill { height: 100%; transition: all 0.3s ease; }
                .strength-text { font-size: 0.875rem; margin-top: 0.25rem; }
                .strength-weak .strength-fill { width: 25%; background: #dc3545; }
                .strength-fair .strength-fill { width: 50%; background: #ffc107; }
                .strength-good .strength-fill { width: 75%; background: #17a2b8; }
                .strength-strong .strength-fill { width: 100%; background: #28a745; }
            `;
            document.head.appendChild(styles);
        }
        
        passwordField.parentNode.appendChild(strengthIndicator);
        
        passwordField.addEventListener('input', (e) => {
            const strength = this.calculatePasswordStrength(e.target.value);
            this.updatePasswordStrength(strengthIndicator, strength);
        });
    },
    
    calculatePasswordStrength(password) {
        let score = 0;
        if (password.length >= 8) score++;
        if (password.length >= 12) score++;
        if (/[a-z]/.test(password)) score++;
        if (/[A-Z]/.test(password)) score++;
        if (/[0-9]/.test(password)) score++;
        if (/[^A-Za-z0-9]/.test(password)) score++;
        
        if (score < 3) return { level: 'weak', score };
        if (score < 4) return { level: 'fair', score };
        if (score < 6) return { level: 'good', score };
        return { level: 'strong', score };
    },
    
    updatePasswordStrength(indicator, strength) {
        const levels = ['weak', 'fair', 'good', 'strong'];
        levels.forEach(level => indicator.classList.remove(`strength-${level}`));
        indicator.classList.add(`strength-${strength.level}`);
        indicator.querySelector('.strength-level').textContent = strength.level.charAt(0).toUpperCase() + strength.level.slice(1);
    }
};

// Copy to clipboard utility
async function copyToClipboard(text, successMessage = 'Copied to clipboard') {
    try {
        await navigator.clipboard.writeText(text);
        Notifications.success(successMessage);
    } catch (error) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
            Notifications.success(successMessage);
        } catch (fallbackError) {
            Notifications.error('Failed to copy to clipboard');
        }
        
        document.body.removeChild(textArea);
    }
}

// Password visibility toggle functions
function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    
    if (!field) {
        console.error('Password field not found:', fieldId);
        return;
    }
    
    console.log('Toggling password for field:', fieldId, 'Current type:', field.type);
    
    // Find the toggle button - it's the first button in the input-group-append div
    const inputGroup = field.parentElement;
    const inputGroupAppend = inputGroup.querySelector('.input-group-append');
    const toggleButton = inputGroupAppend ? inputGroupAppend.querySelector('button:first-child') : null;
    const icon = toggleButton ? toggleButton.querySelector('i') : null;
    
    if (!toggleButton || !icon) {
        console.error('Toggle button or icon not found for field:', fieldId);
        console.log('InputGroup:', inputGroup);
        console.log('InputGroupAppend:', inputGroupAppend);
        console.log('ToggleButton:', toggleButton);
        console.log('Icon:', icon);
        return;
    }
    
    if (field.type === 'password') {
        field.type = 'text';
        icon.className = 'fas fa-eye-slash';
        toggleButton.setAttribute('title', 'Hide password');
        console.log('Password shown');
    } else {
        field.type = 'password';
        icon.className = 'fas fa-eye';
        toggleButton.setAttribute('title', 'Show password');
        console.log('Password hidden');
    }
}

function togglePasswordVisibility(fieldId) {
    const field = document.getElementById(fieldId);
    
    if (!field) {
        console.error('Password field not found:', fieldId);
        return;
    }
    
    // Try to find toggle button - could be nextElementSibling or in input-group-append
    let toggle = field.nextElementSibling;
    let icon = null;
    
    if (toggle && toggle.classList.contains('password-toggle')) {
        // Direct sibling case (credential form)
        icon = toggle.querySelector('i, .icon');
    } else {
        // Bootstrap input-group case (credential detail)
        const inputGroup = field.parentElement;
        const inputGroupAppend = inputGroup.querySelector('.input-group-append');
        toggle = inputGroupAppend ? inputGroupAppend.querySelector('button[onclick*="togglePasswordVisibility"]') : null;
        icon = toggle ? toggle.querySelector('i') : null;
    }
    
    if (!toggle || !icon) {
        console.error('Toggle button or icon not found for field:', fieldId);
        return;
    }
    
    if (field.type === 'password') {
        field.type = 'text';
        if (icon.className.includes('fa-')) {
            icon.className = 'fas fa-eye-slash';
        } else {
            icon.className = 'icon-eye-off';
        }
        toggle.setAttribute('title', 'Hide password');
    } else {
        field.type = 'password';
        if (icon.className.includes('fa-')) {
            icon.className = 'fas fa-eye';
        } else {
            icon.className = 'icon-eye';
        }
        toggle.setAttribute('title', 'Show password');
    }
}

// Show/hide password with proper icon switching
function showPassword(fieldId) {
    const field = document.getElementById(fieldId);
    if (field) {
        field.type = 'text';
        const button = field.parentElement.querySelector('button i');
        if (button) button.className = 'fas fa-eye-slash';
    }
}

function hidePassword(fieldId) {
    const field = document.getElementById(fieldId);
    if (field) {
        field.type = 'password';
        const button = field.parentElement.querySelector('button i');
        if (button) button.className = 'fas fa-eye';
    }
}

// Loading states
const Loading = {
    show(element, text = 'Loading...') {
        const originalContent = element.innerHTML;
        element.dataset.originalContent = originalContent;
        element.innerHTML = `
            <span class="loading-spinner"></span>
            <span class="loading-text">${text}</span>
        `;
        element.disabled = true;
    },
    
    hide(element) {
        if (element.dataset.originalContent) {
            element.innerHTML = element.dataset.originalContent;
            delete element.dataset.originalContent;
        }
        element.disabled = false;
    }
};

// Theme utilities
const Theme = {
    init() {
        ready(() => {
            const savedTheme = localStorage.getItem('theme') || 'light';
            this.setTheme(savedTheme);
            
            // Theme toggle button
            const themeToggle = document.querySelector('#theme-toggle');
            if (themeToggle) {
                themeToggle.addEventListener('click', () => {
                    this.toggleTheme();
                });
            }
        });
    },
    
    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        const themeIcon = document.querySelector('#theme-toggle i');
        if (themeIcon) {
            themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    },
    
    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }
};

// Modal utilities
const Modal = {
    show(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'flex';
            modal.classList.add('show');
            document.body.style.overflow = 'hidden'; // Prevent body scroll
        }
    },
    
    hide(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
            modal.classList.remove('show');
            document.body.style.overflow = ''; // Restore body scroll
        }
    },
    
    init() {
        // Handle modal triggers
        document.querySelectorAll('[data-toggle="modal"]').forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                const target = trigger.getAttribute('data-target');
                if (target) {
                    const modalId = target.replace('#', '');
                    this.show(modalId);
                }
            });
        });
        
        // Handle modal close buttons
        document.querySelectorAll('[data-dismiss="modal"], .modal-close').forEach(closeBtn => {
            closeBtn.addEventListener('click', (e) => {
                e.preventDefault();
                const modal = closeBtn.closest('.modal');
                if (modal) {
                    this.hide(modal.id);
                }
            });
        });
        
        // Handle modal overlay clicks (close modal when clicking outside)
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.hide(modal.id);
                }
            });
        });
        
        // Handle escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                const openModal = document.querySelector('.modal.show');
                if (openModal) {
                    this.hide(openModal.id);
                }
            }
        });
    }
};

// Initialize components
ready(() => {
    // Initialize search manager
    new SearchManager();
    
    // Initialize theme
    Theme.init();
    
    // Initialize modal functionality
    Modal.init();
    
    // Setup auto-save for forms
    const credentialForm = document.querySelector('#credential-form');
    if (credentialForm) {
        FormUtils.autoSave('#credential-form', 'credential-form-draft');
        FormUtils.setupPasswordStrength('#id_password, input[name="password"]');
    }
    
    const noteForm = document.querySelector('#note-form');
    if (noteForm) {
        FormUtils.autoSave('#note-form', 'note-form-draft');
    }
    
    // Add click handlers for copy buttons
    document.querySelectorAll('[data-copy]').forEach(button => {
        button.addEventListener('click', () => {
            const text = button.dataset.copy;
            copyToClipboard(text);
        });
    });
    
    // Add confirmation dialogs for delete buttons
    document.querySelectorAll('[data-confirm]').forEach(button => {
        button.addEventListener('click', (e) => {
            if (!confirm(button.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });
});

// Global error handler
window.addEventListener('error', (e) => {
    console.error('Global error:', e.error);
    // Don't show notifications for script errors in production
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        Notifications.error(`Error: ${e.error.message}`);
    }
});

// Debug function to test password toggle functionality
function testPasswordToggle() {
    console.log('Testing password toggle functionality...');
    
    // Test togglePassword function
    const passwordField = document.getElementById('password-field');
    if (passwordField) {
        console.log('Found password field:', passwordField);
        togglePassword('password-field');
        console.log('Password field type after toggle:', passwordField.type);
    } else {
        console.log('Password field not found');
    }
    
    // Test togglePassword for secret field
    const secretField = document.getElementById('secret-field');
    if (secretField) {
        console.log('Found secret field:', secretField);
        togglePassword('secret-field');
        console.log('Secret field type after toggle:', secretField.type);
    } else {
        console.log('Secret field not found');
    }
}

// Debug function to test CSRF token functionality
function testCSRFToken() {
    console.log('=== CSRF Token Debug ===');
    
    // Test CSRF token retrieval
    const token = getCSRFToken();
    console.log('CSRF token:', token ? token.substring(0, 10) + '...' : 'Not found');
    
    // Check all possible token sources
    console.log('Meta tag:', document.querySelector('meta[name=csrf-token]')?.getAttribute('content')?.substring(0, 10) + '...' || 'Not found');
    console.log('Cookie:', document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1]?.substring(0, 10) + '...' || 'Not found');
    console.log('Form input:', document.querySelector('[name=csrfmiddlewaretoken]')?.value?.substring(0, 10) + '...' || 'Not found');
    
    // Test API call
    if (token) {
        console.log('Testing API call with token...');
        fetch('/api/stats/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': token,
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin'
        })
        .then(response => {
            console.log('API test response status:', response.status);
            if (response.status === 403) {
                console.error('403 error - CSRF token is invalid or missing');
            } else if (response.ok) {
                console.log('API call successful - CSRF token is working');
            }
            return response.text();
        })
        .then(data => {
            console.log('API response data type:', typeof data);
        })
        .catch(error => {
            console.error('API test failed:', error);
        });
    } else {
        console.error('No CSRF token found - cannot test API call');
    }
    
    console.log('=== End CSRF Debug ===');
}

// Export utilities for use in templates
window.CredentialsManager = {
    API,
    Notifications,
    toggleFavorite,
    copyToClipboard,
    togglePassword,
    togglePasswordVisibility,
    showPassword,
    hidePassword,
    Loading,
    Theme,
    FormUtils,
    Modal,
    testPasswordToggle,
    testCSRFToken,
    getCSRFToken
}; 