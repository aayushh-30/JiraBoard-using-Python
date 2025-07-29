/* ===============================
   DHANIYA JIRA BOARD - CLEAN JS
   =============================== */

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

// Global variables
let darkModeManager = null;
let sidebarManager = null;

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
        
        console.log('🎉 Dhaniya Board initialized successfully!');
        console.log('📊 Status:', {
            darkModeManager: !!darkModeManager,
            sidebarManager: !!sidebarManager
        });
        
    } catch (error) {
        console.error('❌ Initialization failed:', error);
    }
});
