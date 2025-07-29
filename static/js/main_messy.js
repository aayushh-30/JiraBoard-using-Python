// Modern JIRA Board Frontend - Advanced Implementation

// Toast Notification System for User Feedback
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
            container.className = 'toast-container position-fixed top-0 end-0 p-3';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }
        return container;
    }

    show(message, type = 'info', duration = 4000) {
        const id = Date.now() + Math.random();
        const toast = this.createToast(id, message, type);
        
        this.container.appendChild(toast);
        this.toasts.set(id, toast);
        
        // Trigger animation
        requestAnimationFrame(() => {
            toast.classList.add('show');
        });
        
        // Auto dismiss
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
                    style="flex-shrink: 0; background: none; border: none; color: #9CA3AF; cursor: pointer; padding: 4px; border-radius: 4px; transition: color 0.2s;"
                    onmouseover="this.style.color='#6B7280'" 
                    onmouseout="this.style.color='#9CA3AF'"
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
            'error': 'fa-exclamation-triangle',
            'warning': 'fa-exclamation-circle',
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

// Dark Mode with Smooth 300ms Transitions
class DarkModeManager {
    constructor() {
        this.darkThemeLink = document.getElementById('dark-theme-css');
        this.icon = document.getElementById('dark-mode-icon');
        
        if (!this.darkThemeLink) {
            console.error('Dark theme CSS link not found!');
            return;
        }
        
        if (!this.icon) {
            console.error('Dark mode icon not found!');
        }
        
        console.log('DarkModeManager initialized', {
            darkThemeLink: !!this.darkThemeLink,
            icon: !!this.icon
        });
        
        this.init();
    }

    init() {
        this.addTransitionStyles();
        const savedTheme = localStorage.getItem('dhaniya-theme');
        console.log('Saved theme:', savedTheme);
        
        if (savedTheme === 'dark') {
            this.enableDarkMode();
        } else {
            this.enableLightMode();
        }
    }

    addTransitionStyles() {
        const style = document.createElement('style');
        style.textContent = `
            * {
                transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease !important;
            }
            .sidebar, .content-wrapper {
                transition: all 0.3s ease !important;
            }
        `;
        document.head.appendChild(style);
    }

    toggle() {
        console.log('Dark mode toggle clicked!');
        
        if (!this.darkThemeLink) {
            console.error('Cannot toggle - dark theme link not found');
            return;
        }
        
        const isDarkMode = !this.darkThemeLink.disabled;
        console.log('Current state:', { isDarkMode, disabled: this.darkThemeLink.disabled });
        
        if (isDarkMode) {
            this.enableLightMode();
            toastManager.show('Light mode enabled', 'info', 2000);
        } else {
            this.enableDarkMode();
            toastManager.show('Dark mode enabled', 'info', 2000);
        }
    }

    enableDarkMode() {
        console.log('Enabling dark mode...');
        if (this.darkThemeLink) {
            this.darkThemeLink.disabled = false;
            console.log('Dark theme CSS enabled');
        }
        if (this.icon) this.icon.className = 'fas fa-sun';
        localStorage.setItem('dhaniya-theme', 'dark');
        document.body.classList.add('dark-mode');
        console.log('Dark mode enabled successfully');
    }

    enableLightMode() {
        console.log('Enabling light mode...');
        if (this.darkThemeLink) {
            this.darkThemeLink.disabled = true;
            console.log('Dark theme CSS disabled');
        }
        if (this.icon) this.icon.className = 'fas fa-moon';
        localStorage.setItem('dhaniya-theme', 'light');
        document.body.classList.remove('dark-mode');
        console.log('Light mode enabled successfully');
    }
}

// Enhanced Sidebar Collapse/Expand with Dynamic Content Adjustment
class SidebarManager {
    constructor() {
        this.sidebar = document.getElementById('sidebar-wrapper');
        this.toggleBtn = document.getElementById('sidebar-toggle');
        this.contentWrapper = document.getElementById('content-wrapper');
        this.isCollapsed = false;
        this.init();
    }

    init() {
        if (this.toggleBtn) {
            this.toggleBtn.addEventListener('click', () => this.toggle());
        }
        
        // Adjust content wrapper for user management cards
        this.adjustContentWrapper();
        
        // Listen for window resize
        window.addEventListener('resize', () => this.adjustContentWrapper());
    }

    toggle() {
        if (!this.sidebar) return;
        
        this.isCollapsed = !this.isCollapsed;
        
        if (this.isCollapsed) {
            this.collapse();
        } else {
            this.expand();
        }
        
        // Adjust content wrapper after toggle
        setTimeout(() => this.adjustContentWrapper(), 300);
    }

    collapse() {
        if (this.sidebar) {
            this.sidebar.classList.add('collapsed');
        }
        if (this.contentWrapper) {
            this.contentWrapper.classList.add('sidebar-collapsed');
        }
        toastManager.show('Sidebar collapsed', 'info', 1500);
    }

    expand() {
        if (this.sidebar) {
            this.sidebar.classList.remove('collapsed');
        }
        if (this.contentWrapper) {
            this.contentWrapper.classList.remove('sidebar-collapsed');
        }
        toastManager.show('Sidebar expanded', 'info', 1500);
    }

    adjustContentWrapper() {
        // Dynamically adjust content wrapper based on sidebar state
        const cards = document.querySelectorAll('.card');
        const tables = document.querySelectorAll('.table-responsive');
        
        cards.forEach(card => {
            if (this.isCollapsed) {
                card.style.maxWidth = 'calc(100vw - 64px - 40px)';
            } else {
                card.style.maxWidth = 'calc(100vw - 300px - 40px)';
            }
        });
        
        tables.forEach(table => {
            if (this.isCollapsed) {
                table.style.maxWidth = 'calc(100vw - 64px - 40px)';
            } else {
                table.style.maxWidth = 'calc(100vw - 300px - 40px)';
            }
        });
    }
}

// Event Delegation for Dropdowns with Proper Z-Index
class DropdownManager {
    constructor() {
        this.init();
    }

    init() {
        // Event delegation for all dropdowns
        document.addEventListener('click', this.handleDocumentClick.bind(this));
        this.initializeRoleDropdowns();
    }

    handleDocumentClick(e) {
        if (!e.target.closest('.dropdown')) {
            this.closeAllDropdowns();
        }
    }

    initializeRoleDropdowns() {
        // Role switching dropdown with proper z-index layering
        const roleSubmenus = document.querySelectorAll('.dropdown-submenu');
        
        roleSubmenus.forEach((submenu, index) => {
            const toggle = submenu.querySelector('.dropdown-toggle');
            const submenuDropdown = submenu.querySelector('.dropdown-menu');
            
            if (toggle && submenuDropdown) {
                // Set proper z-index for layering to prevent overlap
                submenuDropdown.style.zIndex = 1055 + index;
                
                submenu.addEventListener('mouseenter', () => {
                    this.showSubmenu(submenuDropdown);
                });
                
                submenu.addEventListener('mouseleave', () => {
                    this.hideSubmenu(submenuDropdown);
                });
                
                toggle.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this.toggleSubmenu(submenuDropdown);
                });
            }
        });
    }

    showSubmenu(submenu) {
        submenu.classList.add('show');
        submenu.style.display = 'block';
        submenu.style.transform = 'translateY(0)';
        submenu.style.opacity = '1';
    }

    hideSubmenu(submenu) {
        submenu.style.transform = 'translateY(-10px)';
        submenu.style.opacity = '0';
        setTimeout(() => {
            submenu.classList.remove('show');
            submenu.style.display = 'none';
        }, 150);
    }

    toggleSubmenu(submenu) {
        if (submenu.classList.contains('show')) {
            this.hideSubmenu(submenu);
        } else {
            this.showSubmenu(submenu);
        }
    }

    closeAllDropdowns() {
        document.querySelectorAll('.dropdown-submenu .dropdown-menu').forEach(submenu => {
            this.hideSubmenu(submenu);
        });
    }
}

// Role Switching Manager for Admin Users
class RoleSwitchManager {
    constructor() {
        this.currentRole = 'admin'; // Default role
        this.availableRoles = ['admin', 'manager', 'developer', 'client', 'viewer'];
        this.init();
    }

    init() {
        this.createRoleSwitchDropdown();
        this.bindEvents();
    }

    createRoleSwitchDropdown() {
        const switchButton = document.getElementById('role-switch-btn');
        if (switchButton) {
            switchButton.addEventListener('click', (e) => {
                e.preventDefault();
                this.showRoleDropdown();
            });
        }
    }

    showRoleDropdown() {
        // Create dropdown if it doesn't exist
        let dropdown = document.getElementById('role-switch-dropdown');
        if (!dropdown) {
            dropdown = this.buildRoleDropdown();
            document.body.appendChild(dropdown);
        }

        // Position dropdown below the button
        const switchButton = document.getElementById('role-switch-btn');
        if (switchButton) {
            const rect = switchButton.getBoundingClientRect();
            dropdown.style.position = 'fixed';
            dropdown.style.top = `${rect.bottom + 5}px`;
            dropdown.style.left = `${rect.left}px`;
            dropdown.style.zIndex = '1200';
            dropdown.style.display = 'block';
            dropdown.classList.add('show');
        }

        // Close dropdown when clicking outside
        document.addEventListener('click', this.handleOutsideClick.bind(this));
    }

    buildRoleDropdown() {
        const dropdown = document.createElement('div');
        dropdown.id = 'role-switch-dropdown';
        dropdown.className = 'dropdown-menu role-switch-dropdown';
        dropdown.innerHTML = `
            <h6 class="dropdown-header">Switch Role View</h6>
            ${this.availableRoles.map(role => `
                <a class="dropdown-item" href="#" data-role="${role}">
                    <i class="fas fa-user-${this.getRoleIcon(role)} me-2"></i>
                    ${role.charAt(0).toUpperCase() + role.slice(1)}
                    ${role === this.currentRole ? '<i class="fas fa-check float-end"></i>' : ''}
                </a>
            `).join('')}
        `;

        // Bind click events for role items
        dropdown.addEventListener('click', this.handleRoleSelect.bind(this));
        
        return dropdown;
    }

    getRoleIcon(role) {
        const icons = {
            'admin': 'crown',
            'manager': 'cog',
            'developer': 'code',
            'client': 'handshake',
            'viewer': 'eye'
        };
        return icons[role] || 'user';
    }

    handleRoleSelect(e) {
        e.preventDefault();
        const roleItem = e.target.closest('.dropdown-item');
        if (roleItem) {
            const selectedRole = roleItem.dataset.role;
            this.switchRole(selectedRole);
        }
    }

    switchRole(newRole) {
        if (newRole === this.currentRole) return;

        this.currentRole = newRole;
        
        // Update UI to reflect role change
        this.updateRoleDisplay();
        
        // Show toast notification
        toastManager.show(`Switched to ${newRole.charAt(0).toUpperCase() + newRole.slice(1)} view`, 'success', 3000);
        
        // Hide dropdown
        this.hideRoleDropdown();
        
        // Optionally refresh page content or make AJAX call to update view
        // For now, we'll just update the UI elements
        this.updateContentForRole(newRole);
    }

    updateRoleDisplay() {
        const switchButton = document.getElementById('role-switch-btn');
        if (switchButton) {
            switchButton.innerHTML = `
                <i class="fas fa-user-${this.getRoleIcon(this.currentRole)} me-1"></i>
                ${this.currentRole.charAt(0).toUpperCase() + this.currentRole.slice(1)} View
                <i class="fas fa-chevron-down ms-1"></i>
            `;
        }
    }

    updateContentForRole(role) {
        // Update dashboard content based on selected role
        const dashboardCards = document.querySelectorAll('.dashboard-card-row .col-md-3');
        
        // Hide/show different sections based on role
        if (role === 'admin') {
            // Show all admin content
            document.querySelectorAll('.admin-only').forEach(el => el.style.display = 'block');
        } else {
            // Hide admin-only content for other roles
            document.querySelectorAll('.admin-only').forEach(el => el.style.display = 'none');
        }
        
        // Update sidebar items visibility
        this.updateSidebarForRole(role);
    }

    updateSidebarForRole(role) {
        const sidebarItems = document.querySelectorAll('#sidebar-wrapper .list-group-item');
        
        sidebarItems.forEach(item => {
            const href = item.getAttribute('href');
            
            // Hide admin-only links for non-admin roles
            if (role !== 'admin') {
                if (href && (href.includes('/admin/') || href.includes('/users/'))) {
                    item.style.display = 'none';
                }
            } else {
                item.style.display = 'flex';
            }
        });
    }

    hideRoleDropdown() {
        const dropdown = document.getElementById('role-switch-dropdown');
        if (dropdown) {
            dropdown.classList.remove('show');
            dropdown.style.display = 'none';
        }
        document.removeEventListener('click', this.handleOutsideClick.bind(this));
    }

    handleOutsideClick(e) {
        const dropdown = document.getElementById('role-switch-dropdown');
        const switchButton = document.getElementById('role-switch-btn');
        
        if (dropdown && !dropdown.contains(e.target) && !switchButton.contains(e.target)) {
            this.hideRoleDropdown();
        }
    }
}

// Multi-Role Management System
class RoleSwitchManager {
    constructor() {
        this.currentRoles = [];
        this.activeRole = null;
        this.canSwitch = false;
        this.init();
    }

    init() {
        this.loadUserRoles();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Load roles when dropdown is opened
        const dropdown = document.getElementById('roleSwitchDropdown');
        if (dropdown) {
            dropdown.addEventListener('show.bs.dropdown', () => {
                this.loadUserRoles();
            });
        }
    }

    async loadUserRoles() {
        try {
            const response = await fetch('/profile/get-user-roles');
            if (!response.ok) throw new Error('Failed to load roles');
            
            const data = await response.json();
            this.currentRoles = data.roles || [];
            this.activeRole = data.active_role;
            this.canSwitch = data.can_switch || false;
            
            this.updateRoleDropdown();
            this.updateRoleDisplay();
        } catch (error) {
            console.error('Error loading user roles:', error);
            toastManager.show('Failed to load user roles', 'error');
        }
    }

    updateRoleDropdown() {
        const dropdownMenu = document.querySelector('#role-switch-dropdown .dropdown-menu');
        if (!dropdownMenu) return;

        // Clear existing items except header
        const header = dropdownMenu.querySelector('.dropdown-header');
        const divider = dropdownMenu.querySelector('.dropdown-divider');
        dropdownMenu.innerHTML = '';
        
        if (header) dropdownMenu.appendChild(header);
        if (divider) dropdownMenu.appendChild(divider);

        if (this.currentRoles.length === 0) {
            const noRolesItem = document.createElement('li');
            noRolesItem.innerHTML = '<span class="dropdown-item-text text-muted">No roles assigned</span>';
            dropdownMenu.appendChild(noRolesItem);
            return;
        }

        if (this.currentRoles.length === 1) {
            const singleRoleItem = document.createElement('li');
            singleRoleItem.innerHTML = `<span class="dropdown-item-text text-muted">Single role: ${this.currentRoles[0].role_name.charAt(0).toUpperCase() + this.currentRoles[0].role_name.slice(1)}</span>`;
            dropdownMenu.appendChild(singleRoleItem);
            return;
        }

        // Add role switch options
        this.currentRoles.forEach(role => {
            const li = document.createElement('li');
            const isActive = role.role_name === this.activeRole;
            const isPrimary = role.is_primary;
            
            const roleIcon = this.getRoleIcon(role.role_name);
            const statusIcon = isPrimary ? '<i class="fas fa-star text-warning me-1" title="Primary Role"></i>' : '';
            const activeIcon = isActive ? '<i class="fas fa-check text-success ms-2"></i>' : '';
            
            li.innerHTML = `
                <a class="dropdown-item ${isActive ? 'active' : ''}" 
                   href="/profile/switch-role/${role.role_name}"
                   onclick="return roleSwitchManager.switchRole('${role.role_name}', event)">
                    ${roleIcon} ${statusIcon}${role.role_name.charAt(0).toUpperCase() + role.role_name.slice(1)}
                    ${activeIcon}
                </a>
            `;
            dropdownMenu.appendChild(li);
        });

        // Hide the dropdown if user can't switch (only one role)
        const dropdown = document.getElementById('role-switch-dropdown');
        if (dropdown) {
            dropdown.style.display = this.canSwitch ? 'block' : 'none';
        }
    }

    updateRoleDisplay() {
        const currentRoleDisplay = document.getElementById('current-role-display');
        const profileRoleDisplay = document.getElementById('profile-role-display');
        
        if (currentRoleDisplay && this.activeRole) {
            currentRoleDisplay.textContent = this.activeRole.charAt(0).toUpperCase() + this.activeRole.slice(1);
        }
        
        if (profileRoleDisplay && this.activeRole) {
            profileRoleDisplay.textContent = this.activeRole.charAt(0).toUpperCase() + this.activeRole.slice(1);
        }
    }

    getRoleIcon(roleName) {
        const icons = {
            'admin': '<i class="fas fa-crown text-danger me-2"></i>',
            'manager': '<i class="fas fa-users-cog text-warning me-2"></i>',
            'developer': '<i class="fas fa-code text-primary me-2"></i>',
            'client': '<i class="fas fa-handshake text-info me-2"></i>',
            'viewer': '<i class="fas fa-eye text-secondary me-2"></i>',
            'pending': '<i class="fas fa-clock text-muted me-2"></i>'
        };
        return icons[roleName] || '<i class="fas fa-user me-2"></i>';
    }

    async switchRole(roleName, event) {
        if (event) event.preventDefault();
        
        if (roleName === this.activeRole) {
            toastManager.show('Already using this role', 'info');
            return false;
        }

        try {
            // Show loading state
            toastManager.show('Switching role...', 'info', 1000);
            
            // For admin users, use admin-switch-role for testing purposes
            // For regular users, this would use proper role switching logic
            window.location.href = `/profile/admin-switch-role/${roleName}`;
            
        } catch (error) {
            console.error('Error switching role:', error);
            toastManager.show('Failed to switch role', 'error');
        }
        
        return false;
    }
}

// Global instances
const toastManager = new ToastManager();
let darkModeManager, sidebarManager, dropdownManager, roleSwitchManager;

// Legacy function for backward compatibility
function toggleDarkMode() {
    console.log('toggleDarkMode called!');
    console.log('darkModeManager:', darkModeManager);
    if (darkModeManager) {
        console.log('DarkModeManager exists, calling toggle');
        darkModeManager.toggle();
    } else {
        console.error('DarkModeManager not initialized!');
        // Try to initialize it now
        try {
            darkModeManager = new DarkModeManager();
            darkModeManager.toggle();
        } catch (e) {
            console.error('Failed to create DarkModeManager:', e);
        }
    }
}

// Modern smooth interactions initialization
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM Content Loaded - Starting initialization");
    
    // Check if elements exist
    const darkThemeElement = document.getElementById('dark-theme-css');
    const darkModeIcon = document.getElementById('dark-mode-icon');
    
    console.log('Found elements:', {
        darkThemeElement: !!darkThemeElement,
        darkModeIcon: !!darkModeIcon
    });
    
    // Initialize all managers for smooth modern interactions
    try {
        darkModeManager = new DarkModeManager();
        sidebarManager = new SidebarManager();
        dropdownManager = new DropdownManager();
        roleSwitchManager = new RoleSwitchManager();
        
        console.log("🚀 Modern JIRA Board Frontend with smooth animations and role switching initialized");
        console.log('darkModeManager created:', !!darkModeManager);
    } catch (error) {
        console.error('Error during initialization:', error);
    }
});
