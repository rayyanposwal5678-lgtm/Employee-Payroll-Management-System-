/**
 * EPMS — Premium Interaction Layer v2.0
 * Ultra-premium micro-interactions, animated counters,
 * scroll reveals, quick-action arrow animations,
 * smooth page transitions, and interactive search.
 */

document.addEventListener('DOMContentLoaded', function () {

    // ============================================
    // 0. SIDEBAR SCROLL PERSISTENCE
    // Remembers scroll position across page loads
    // ============================================
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        // Restore saved scroll position
        const savedScroll = sessionStorage.getItem('sidebarScroll');
        if (savedScroll) {
            sidebar.scrollTop = parseInt(savedScroll, 10);
        }
        // Save scroll position before navigating away
        window.addEventListener('beforeunload', function () {
            sessionStorage.setItem('sidebarScroll', sidebar.scrollTop);
        });
    }

    // ============================================
    // 1. ANIMATED NUMBER COUNTERS
    // Animates stat numbers from 0 → target with easing
    // ============================================
    function animateCounters() {
        const statNumbers = document.querySelectorAll('.card-box h2.fw-bold');
        statNumbers.forEach(el => {
            const rawText = el.textContent.trim();
            // Skip elements with non-numeric content (e.g. "$35.2K", "N/A")
            if (!/^\d+$/.test(rawText.replace(/,/g, ''))) return;
            
            const target = parseInt(rawText.replace(/,/g, ''), 10);
            if (isNaN(target) || target === 0) return;

            el.textContent = '0';
            el.classList.add('counter-value');

            const duration = 1400;
            const startTime = performance.now();

            function updateCounter(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                // Ease-out cubic for smooth deceleration
                const eased = 1 - Math.pow(1 - progress, 3);
                const current = Math.round(target * eased);
                el.textContent = current.toLocaleString();
                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                }
            }
            requestAnimationFrame(updateCounter);
        });
    }
    animateCounters();

    // ============================================
    // 2. SCROLL REVEAL
    // Fade-in elements when scrolled into the viewport
    // ============================================
    function initScrollReveal() {
        const revealElements = document.querySelectorAll('.reveal');
        if (!revealElements.length) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

        revealElements.forEach(el => observer.observe(el));
    }
    initScrollReveal();

    // ============================================
    // 3. GLOBAL SEARCH FILTER
    // Live-search sidebar navigation + Ctrl+K shortcut
    // ============================================
    const searchInput = document.getElementById('globalSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const query = this.value.toLowerCase().trim();
            const sidebarLinks = document.querySelectorAll('.sidebar a');
            const sidebarLabels = document.querySelectorAll('.sidebar-section-label');

            if (!query) {
                sidebarLinks.forEach(link => {
                    link.style.display = '';
                    link.style.opacity = '';
                });
                sidebarLabels.forEach(label => label.style.display = '');
                return;
            }

            sidebarLinks.forEach(link => {
                const text = link.textContent.toLowerCase();
                if (text.includes(query)) {
                    link.style.display = '';
                    link.style.opacity = '1';
                } else {
                    link.style.display = 'none';
                    link.style.opacity = '0';
                }
            });

            sidebarLabels.forEach(label => {
                label.style.display = query ? 'none' : '';
            });
        });

        // Keyboard shortcut: Ctrl+K to focus search
        document.addEventListener('keydown', function (e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                searchInput.focus();
            }
            // Escape to blur
            if (e.key === 'Escape' && document.activeElement === searchInput) {
                searchInput.blur();
                searchInput.value = '';
                searchInput.dispatchEvent(new Event('input'));
            }
        });
    }

    // ============================================
    // 4. SMOOTH PAGE TRANSITIONS
    // Fade out content before navigation
    // ============================================
    function initPageTransitions() {
        const pageContent = document.querySelector('.page-content');
        if (!pageContent) return;

        const internalLinks = document.querySelectorAll('.sidebar a[href], .btn[href], a.btn[href]');
        internalLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && href.startsWith('/') && !href.includes('logout')) {
                link.addEventListener('click', function (e) {
                    e.preventDefault();
                    pageContent.style.opacity = '0';
                    pageContent.style.transform = 'translateY(8px)';
                    pageContent.style.transition = 'all 0.18s ease';
                    setTimeout(() => {
                        window.location.href = href;
                    }, 160);
                });
            }
        });
    }
    initPageTransitions();

    // ============================================
    // 5. TABLE ROW INTERACTIONS
    // Press-down micro-feedback on table rows
    // ============================================
    function initTableInteractions() {
        const tableRows = document.querySelectorAll('.table-hover tbody tr');
        tableRows.forEach(row => {
            row.addEventListener('mousedown', function () {
                this.style.transform = 'scale(0.998)';
                this.style.transition = 'transform 0.08s ease';
            });
            row.addEventListener('mouseup', function () {
                this.style.transform = '';
            });
            row.addEventListener('mouseleave', function () {
                this.style.transform = '';
            });
        });
    }
    initTableInteractions();

    // ============================================
    // 6. QUICK ACTION ARROW ANIMATION
    // Animate arrow icons on hover
    // ============================================
    function initQuickActionArrows() {
        const actionBtns = document.querySelectorAll('.d-grid .btn');
        actionBtns.forEach(btn => {
            const arrow = btn.querySelector('.fa-arrow-right');
            if (!arrow) return;

            btn.addEventListener('mouseenter', function () {
                arrow.style.transition = 'all 0.2s ease';
                arrow.style.transform = 'translateX(4px)';
                arrow.style.opacity = '1';
            });
            btn.addEventListener('mouseleave', function () {
                arrow.style.transform = 'translateX(0)';
                arrow.style.opacity = btn.classList.contains('btn-primary') ? '0.6' : '0.3';
            });
        });
    }
    initQuickActionArrows();

    // ============================================
    // 7. TOOLTIP INITIALIZATION
    // ============================================
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));

    // ============================================
    // 8. AUTO-DISMISS ALERTS
    // Fade out success/info alerts after 5s
    // ============================================
    function initAlertAutoDismiss() {
        const alerts = document.querySelectorAll('.alert-success, .alert-info');
        alerts.forEach(alert => {
            setTimeout(() => {
                alert.style.transition = 'all 0.35s ease';
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-8px)';
                setTimeout(() => alert.remove(), 350);
            }, 5000);
        });
    }
    initAlertAutoDismiss();

    // ============================================
    // 9. CARD TILT MICRO-INTERACTION
    // Subtle 3D tilt on stat card hover
    // ============================================
    function initCardTilt() {
        const statCards = document.querySelectorAll('.row.g-4 .card-box');
        statCards.forEach(card => {
            card.addEventListener('mousemove', function (e) {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = ((y - centerY) / centerY) * -2;
                const rotateY = ((x - centerX) / centerX) * 2;

                card.style.transform = `translateY(-4px) perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            });

            card.addEventListener('mouseleave', function () {
                card.style.transform = '';
                card.style.transition = 'all 0.35s ease';
            });

            card.addEventListener('mouseenter', function () {
                card.style.transition = 'all 0.08s ease';
            });
        });
    }
    initCardTilt();

});
