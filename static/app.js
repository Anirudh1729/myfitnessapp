// My Fitness App - JavaScript

// Service Worker Registration for PWA
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/sw.js')
            .then(reg => console.log('Service Worker registered'))
            .catch(err => console.log('Service Worker registration failed:', err));
    });
}

// Add fade-in animation to elements as they load
document.addEventListener('DOMContentLoaded', function() {
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.05}s`;
    });
});

// Utility functions
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 100px;
        left: 50%;
        transform: translateX(-50%);
        background: var(--card);
        color: var(--text);
        padding: 12px 24px;
        border-radius: 12px;
        z-index: 2000;
        animation: fadeIn 0.3s ease-out;
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 2000);
}

// Handle iOS standalone mode
if (window.navigator.standalone === true) {
    document.body.classList.add('ios-standalone');
}

// Prevent pull-to-refresh on iOS
document.body.addEventListener('touchmove', function(e) {
    if (e.target.closest('.modal-content')) {
        return; // Allow scrolling in modals
    }
}, { passive: false });
