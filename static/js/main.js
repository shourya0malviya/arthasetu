/* ============================================================
   ArthaSetu — Main JavaScript
   AI Powered Local Skill Intelligence Platform
   ============================================================ */

'use strict';

/* ── 1. Auto-dismiss flash alerts after 4 seconds ────────── */
document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('.alert.fade.show').forEach(function (alertEl) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
            bsAlert.close();
        }, 4000);
    });

    /* ── 2. Animate stat numbers (count-up effect) ───────── */
    animateCounters();

    /* ── 3. Highlight active nav link ────────────────────── */
    highlightActiveNav();

    /* ── 4. Smooth scroll-reveal on cards ────────────────── */
    initScrollReveal();

    /* ── 5. Worker card "Copy Phone" buttons ─────────────── */
    initCopyPhone();
});


/* ── Counter Animation ────────────────────────────────────── */
function animateCounters() {
    document.querySelectorAll('.stat-card-val, .kpi-num').forEach(function (el) {
        var raw = el.textContent.trim();
        // Only animate pure numbers (skip "AI", "4.5", etc.)
        var num = parseInt(raw, 10);
        if (isNaN(num) || raw.includes('.') || raw.length > 4) return;

        var start    = 0;
        var duration = 1200;
        var step     = Math.ceil(num / (duration / 16));
        var current  = start;
        var suffix   = raw.replace(/[0-9]/g, ''); // preserve "+" etc.

        var timer = setInterval(function () {
            current += step;
            if (current >= num) {
                current = num;
                clearInterval(timer);
            }
            el.textContent = current + suffix;
        }, 16);
    });
}


/* ── Active Nav Highlight ─────────────────────────────────── */
function highlightActiveNav() {
    var path = window.location.pathname;
    document.querySelectorAll('.navbar .nav-link').forEach(function (link) {
        var href = link.getAttribute('href');
        if (href && path === href) {
            link.classList.add('active');
            link.style.color = 'var(--orange)';
        }
    });
}


/* ── Scroll Reveal ────────────────────────────────────────── */
function initScrollReveal() {
    if (!('IntersectionObserver' in window)) return;

    var targets = document.querySelectorAll(
        '.step-card, .skill-cat-card, .worker-card, .worker-result-card, .kpi-card, .stat-card'
    );

    targets.forEach(function (el) {
        el.style.opacity  = '0';
        el.style.transform = 'translateY(24px)';
        el.style.transition = 'opacity 0.45s ease, transform 0.45s ease';
    });

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity   = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12 });

    targets.forEach(function (el) { observer.observe(el); });
}


/* ── Copy Phone Number ────────────────────────────────────── */
function initCopyPhone() {
    document.querySelectorAll('[data-copy-phone]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var phone = btn.getAttribute('data-copy-phone');
            if (navigator.clipboard) {
                navigator.clipboard.writeText(phone).then(function () {
                    showToast('Phone number copied!');
                });
            }
        });
    });
}


/* ── Toast Notification ───────────────────────────────────── */
function showToast(message, type) {
    type = type || 'success';
    var toast = document.createElement('div');
    toast.className = 'as-toast as-toast-' + type;
    toast.innerHTML =
        '<i class="bi bi-check-circle-fill me-2"></i>' + message;

    // Inline styles so the toast works without extra CSS
    toast.style.cssText = [
        'position:fixed',
        'bottom:24px',
        'right:24px',
        'background:var(--navy-700)',
        'border:1px solid rgba(245,166,35,0.3)',
        'color:var(--text-primary)',
        'padding:0.65rem 1.1rem',
        'border-radius:10px',
        'font-size:0.88rem',
        'font-family:"DM Sans",sans-serif',
        'z-index:9999',
        'box-shadow:0 8px 32px rgba(0,0,0,0.4)',
        'animation:fadeInUp 0.3s ease',
    ].join(';');

    document.body.appendChild(toast);
    setTimeout(function () {
        toast.style.opacity  = '0';
        toast.style.transition = 'opacity 0.3s ease';
        setTimeout(function () { toast.remove(); }, 300);
    }, 2800);
}


/* ── Confirm Delete / Cancel ──────────────────────────────── */
function confirmAction(message) {
    return window.confirm(message || 'Are you sure?');
}


/* ── Character counter helper (reusable) ──────────────────── */
function attachCharCounter(textareaId, counterId, max) {
    var el    = document.getElementById(textareaId);
    var count = document.getElementById(counterId);
    if (!el || !count) return;
    el.addEventListener('input', function () {
        var len = el.value.length;
        count.textContent = len;
        count.style.color = len > (max * 0.85) ? 'var(--orange)' : 'var(--text-secondary)';
    });
}


/* ── Rating Star Interaction ──────────────────────────────── */
document.querySelectorAll('.star-rating-input').forEach(function (group) {
    var stars = group.querySelectorAll('.star');
    stars.forEach(function (star, idx) {
        star.addEventListener('mouseover', function () {
            stars.forEach(function (s, i) {
                s.style.color = i <= idx ? 'var(--orange)' : 'rgba(255,255,255,0.2)';
            });
        });
        star.addEventListener('click', function () {
            var hiddenInput = group.querySelector('input[type="hidden"]');
            if (hiddenInput) hiddenInput.value = idx + 1;
            stars.forEach(function (s, i) {
                s.dataset.selected = i <= idx ? '1' : '0';
            });
        });
        star.addEventListener('mouseleave', function () {
            stars.forEach(function (s) {
                s.style.color = s.dataset.selected === '1'
                    ? 'var(--orange)' : 'rgba(255,255,255,0.2)';
            });
        });
    });
});

/* ── Availability colour badge live update (profile form) ─── */
var avSelect = document.querySelector('select[name="availability"]');
if (avSelect) {
    avSelect.addEventListener('change', function () {
        var colours = {
            available : '#00d4aa',
            busy      : 'var(--orange)',
            offline   : '#6c757d',
        };
        avSelect.style.borderColor = colours[avSelect.value] || '#ffffff22';
    });
    // Trigger once on load
    avSelect.dispatchEvent(new Event('change'));
}


/* ── Skill filter pills on browse page ────────────────────── */
document.querySelectorAll('.skill-filter-pill').forEach(function (pill) {
    pill.addEventListener('click', function () {
        document.querySelectorAll('.skill-filter-pill').forEach(function (p) {
            p.classList.remove('active');
        });
        pill.classList.add('active');

        var skill = pill.dataset.skill;
        var url   = new URL(window.location.href);
        if (skill) {
            url.searchParams.set('skill', skill);
        } else {
            url.searchParams.delete('skill');
        }
        window.location.href = url.toString();
    });
});


/* ── Back-to-top button ───────────────────────────────────── */
(function () {
    var btn = document.createElement('button');
    btn.id  = 'backToTop';
    btn.innerHTML = '<i class="bi bi-arrow-up"></i>';
    btn.style.cssText = [
        'position:fixed',
        'bottom:72px',
        'right:24px',
        'width:40px',
        'height:40px',
        'background:var(--orange)',
        'color:#fff',
        'border:none',
        'border-radius:50%',
        'cursor:pointer',
        'display:none',
        'align-items:center',
        'justify-content:center',
        'font-size:1rem',
        'z-index:999',
        'box-shadow:0 4px 15px rgba(245,166,35,0.4)',
        'transition:opacity 0.3s',
    ].join(';');

    document.body.appendChild(btn);

    window.addEventListener('scroll', function () {
        btn.style.display = window.scrollY > 400 ? 'flex' : 'none';
    });

    btn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}());
