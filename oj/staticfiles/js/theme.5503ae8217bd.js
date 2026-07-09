/**
 * theme.js — CodeForge Global Theme Engine
 *
 * Responsibilities:
 *   1. On page load: read the saved preference from localStorage
 *      and apply it to <body data-theme="..."> before any paint.
 *   2. Expose a global toggleTheme() function called by the navbar button.
 *
 * Scope: This script is loaded once in base.html and runs on every page.
 * It never touches page-specific DOM — only `data-theme` and `#theme-icon`.
 */

(function () {
    'use strict';

    const STORAGE_KEY = 'cf-theme';
    const DARK  = 'dark';
    const LIGHT = 'light';

    const ICONS = {
        [DARK]:  '🌙',
        [LIGHT]: '☀️',
    };

    /** Apply a theme to <body> and update the toggle icon. */
    function applyTheme(theme) {
        document.body.setAttribute('data-theme', theme);
        const icon = document.getElementById('theme-icon');
        if (icon) icon.textContent = ICONS[theme];
    }

    /** Persist the current theme and flip to the opposite one. */
    window.toggleTheme = function () {
        const current = document.body.getAttribute('data-theme') || DARK;
        const next    = current === DARK ? LIGHT : DARK;
        localStorage.setItem(STORAGE_KEY, next);
        applyTheme(next);
    };

    /** Run immediately on script evaluation (before DOMContentLoaded)
     *  so there is no flash-of-wrong-theme. */
    const saved = localStorage.getItem(STORAGE_KEY) || DARK;
    applyTheme(saved);

})();
