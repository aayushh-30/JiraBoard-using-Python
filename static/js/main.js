/* ===============================
   DHANIYA JIRA BOARD - CLEAN JS
   =============================== */

// Toast Notification System
class ToastManager {
    constructor() {
        this.container = this.createContainer();
        this.toasts = new Map();
    }

    createContainer() {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container position-fixed end-0 p-3';
            container.style.cssText = `
                top: 70px;
                z-index: 9999;
                max-width: 400px;
            `;
            document.body.appendChild(container);
        }
        return container;
    }

    show(message, type = 'info', duration = 4000) {
        const id = Date.now() + Math.random();
        const toast = this.createToast(id, message, type);
        
        this.container.appendChild(toast);
        this.toasts.set(id, toast);
        
        requestAnimationFrame(() => {
            toast.classList.add('show');
        });
        
        if (duration > 0) {
            setTimeout(() => this.dismiss(id), duration);
        }
        
        return id;
    }

    createToast(id, message, type) {
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        toast.style.cssText = `
            position: relative;
            min-width: 300px;
            padding: 16px 20px;
            margin-bottom: 12px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            border-left: 4px solid ${this.getBorderColor(type)};
            display: flex;
            align-items: center;
            transform: translateX(100%);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        `;
        
        const iconColor = this.getIconColor(type);
        toast.innerHTML = `
            <div style="display: flex; align-items: center; gap: 12px; flex: 1;">
                <div style="flex-shrink: 0; width: 20px; height: 20px; color: ${iconColor};">
                    <i class="fas ${this.getIcon(type)}" style="font-size: 16px;"></i>
                </div>
                <div style="flex: 1; color: #374151; font-size: 14px; font-weight: 500; line-height: 1.4;">
                    ${message}
                </div>
                <button 
                    onclick="toastManager.dismiss(${id})" 
                    style="flex-shrink: 0; background: none; border: none; color: #FFFFFF; cursor: pointer; padding: 4px; border-radius: 4px; transition: color 0.2s;"
                    onmouseover="this.style.color='#E5E7EB'" 
                    onmouseout="this.style.color='#FFFFFF'"
                >
                    <i class="fas fa-times" style="font-size: 14px;"></i>
                </button>
            </div>
        `;
        return toast;
    }

    getBorderColor(type) {
        const colors = {
            'success': '#10B981',
            'error': '#EF4444', 
            'warning': '#F59E0B',
            'info': '#3B82F6'
        };
        return colors[type] || '#3B82F6';
    }

    getIconColor(type) {
        const colors = {
            'success': '#10B981',
            'error': '#EF4444',
            'warning': '#F59E0B',
            'info': '#3B82F6'
        };
        return colors[type] || '#3B82F6';
    }

    getIcon(type) {
        const icons = {
            'success': 'fa-check-circle',
            'error': 'fa-exclamation-circle',
            'warning': 'fa-exclamation-triangle',
            'info': 'fa-info-circle'
        };
        return icons[type] || 'fa-info-circle';
    }

    dismiss(id) {
        const toast = this.toasts.get(id);
        if (toast) {
            toast.style.transform = 'translateX(100%)';
            toast.style.opacity = '0';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
                this.toasts.delete(id);
            }, 300);
        }
    }
}

// Simple Dark Mode Manager
class DarkModeManager {
    constructor() {
        console.log('🌙 DarkModeManager initializing...');
        
        // Get DOM elements
        this.darkThemeLink = document.getElementById('dark-theme-css');
        this.toggleIcon = document.getElementById('dark-mode-icon');
        
        // Validate elements exist
        if (!this.darkThemeLink) {
            console.error('❌ Dark theme CSS link (#dark-theme-css) not found!');
            return;
        }
        
        if (!this.toggleIcon) {
            console.error('❌ Dark mode icon (#dark-mode-icon) not found!');
        }
        
        console.log('✅ Dark mode elements found:', {
            darkThemeLink: !!this.darkThemeLink,
            toggleIcon: !!this.toggleIcon
        });
        
        // Initialize theme
        this.init();
    }

    init() {
        // Load saved theme preference
        const savedTheme = localStorage.getItem('dhaniya-theme');
        console.log('💾 Saved theme preference:', savedTheme);
        
        if (savedTheme === 'dark') {
            this.enableDarkMode();
        } else {
            this.enableLightMode();
        }
        
        console.log('✅ DarkModeManager initialized successfully');
    }

    toggle() {
        console.log('🔄 Toggling dark mode...');
        
        const isDarkMode = !this.darkThemeLink.disabled;
        console.log('Current state - isDark:', isDarkMode);
        
        if (isDarkMode) {
            this.enableLightMode();
        } else {
            this.enableDarkMode();
        }
    }

    enableDarkMode() {
        console.log('🌙 Enabling dark mode...');
        
        // Enable dark theme CSS
        if (this.darkThemeLink) {
            this.darkThemeLink.disabled = false;
        }
        
        // Update toggle icon
        if (this.toggleIcon) {
            this.toggleIcon.className = 'fas fa-sun';
        }
        
        // Save preference
        localStorage.setItem('dhaniya-theme', 'dark');
        
        console.log('✅ Dark mode enabled');
    }

    enableLightMode() {
        console.log('☀️ Enabling light mode...');
        
        // Disable dark theme CSS
        if (this.darkThemeLink) {
            this.darkThemeLink.disabled = true;
        }
        
        // Update toggle icon
        if (this.toggleIcon) {
            this.toggleIcon.className = 'fas fa-moon';
        }
        
        // Save preference
        localStorage.setItem('dhaniya-theme', 'light');
        
        console.log('✅ Light mode enabled');
    }
}

// Sidebar Manager
class SidebarManager {
    constructor() {
        this.sidebar = document.getElementById('sidebar-wrapper');
        this.contentWrapper = document.querySelector('.content-wrapper');
        this.toggleButton = document.getElementById('sidebar-toggle');
        
        if (this.toggleButton) {
            this.toggleButton.addEventListener('click', () => this.toggle());
        }
    }

    toggle() {
        if (this.sidebar) {
            this.sidebar.classList.toggle('collapsed');
        }
        
        if (this.contentWrapper) {
            this.contentWrapper.classList.toggle('sidebar-collapsed');
        }
    }
}

// Dropdown Manager for Bootstrap dropdowns
class DropdownManager {
    constructor() {
        this.initializeDropdowns();
    }

    initializeDropdowns() {
        document.addEventListener('click', (e) => {
            // Close dropdowns when clicking outside
            if (!e.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                    menu.classList.remove('show');
                });
            }
        });
    }
}

// Role Switch Manager for multi-role users
class RoleSwitchManager {
    constructor() {
        this.currentRole = null;
        this.availableRoles = [];
        this.init();
    }

    init() {
        // Initialize role switching functionality
        const roleSwitchDropdown = document.getElementById('roleSwitchDropdown');
        if (roleSwitchDropdown) {
            this.loadUserRoles();
        }
    }

    loadUserRoles() {
        // This would typically fetch from an API
        // For now, we'll use placeholder data
        console.log('🔄 Loading user roles...');
    }

    switchRole(roleId, roleName) {
        console.log(`🔄 Switching to role: ${roleName} (${roleId})`);
        
        // Make API call to switch role
        fetch('/admin/switch-role', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify({ role_id: roleId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                toastManager.show(`Switched to ${roleName}`, 'success');
                // Update UI
                this.updateRoleDisplay(roleName);
                // Optionally reload page to reflect new permissions
                setTimeout(() => window.location.reload(), 1000);
            } else {
                toastManager.show(data.message || 'Failed to switch role', 'error');
            }
        })
        .catch(error => {
            console.error('Role switch error:', error);
            toastManager.show('Network error occurred', 'error');
        });
    }

    updateRoleDisplay(roleName) {
        const roleDisplay = document.getElementById('current-role-display');
        if (roleDisplay) {
            roleDisplay.textContent = roleName;
        }
    }

    getCSRFToken() {
        const token = document.querySelector('meta[name="csrf-token"]');
        return token ? token.getAttribute('content') : '';
    }
}

// Global instances
const toastManager = new ToastManager();
let darkModeManager = null;
let sidebarManager = null;
let dropdownManager = null;
let roleSwitchManager = null;

// Legacy function for dark mode toggle (backward compatibility)
function toggleDarkMode() {
    console.log('🔄 toggleDarkMode() called');
    
    if (darkModeManager) {
        darkModeManager.toggle();
    } else {
        console.error('❌ DarkModeManager not initialized!');
        console.log('🔄 Attempting emergency initialization...');
        
        try {
            darkModeManager = new DarkModeManager();
            if (darkModeManager.darkThemeLink) {
                darkModeManager.toggle();
            }
        } catch (error) {
            console.error('❌ Emergency initialization failed:', error);
        }
    }
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 DOM Content Loaded - Initializing Dhaniya Board...');
    
    try {
        // Initialize managers
        darkModeManager = new DarkModeManager();
        sidebarManager = new SidebarManager();
        dropdownManager = new DropdownManager();
        roleSwitchManager = new RoleSwitchManager();
        
        console.log('🎉 Dhaniya Board initialized successfully!');
        console.log('📊 Status:', {
            darkModeManager: !!darkModeManager,
            sidebarManager: !!sidebarManager,
            dropdownManager: !!dropdownManager,
            roleSwitchManager: !!roleSwitchManager,
            toastManager: !!toastManager
        });
        
    } catch (error) {
        console.error('❌ Initialization failed:', error);
    }
});
