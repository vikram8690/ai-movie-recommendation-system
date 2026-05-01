/* ===================================================================
   AI Movie Recommendation System — Main JavaScript
   =================================================================== */

document.addEventListener('DOMContentLoaded', function () {

  // ----------------------------------------------------------------
  // 1. Sidebar toggle (mobile)
  // ----------------------------------------------------------------
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar       = document.getElementById('sidebar');

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.toggle('show');
    });

    // Close sidebar when clicking outside
    document.addEventListener('click', function (e) {
      if (
        sidebar.classList.contains('show') &&
        !sidebar.contains(e.target) &&
        !sidebarToggle.contains(e.target)
      ) {
        sidebar.classList.remove('show');
      }
    });
  }

  // ----------------------------------------------------------------
  // 2. Auto-dismiss alert messages after 5 seconds
  // ----------------------------------------------------------------
  const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // ----------------------------------------------------------------
  // 3. Star rating UI for review form
  //    Highlights stars on hover / click using CSS + hidden radio inputs
  // ----------------------------------------------------------------
  function initStarRating() {
    const container = document.getElementById('starRatingContainer');
    if (!container) return;

    const ratingInput = document.getElementById('id_rating');  // hidden or number input

    const stars = container.querySelectorAll('.star-btn');
    stars.forEach(function (star, index) {
      star.addEventListener('click', function () {
        const value = parseInt(star.dataset.value);
        if (ratingInput) ratingInput.value = value;
        updateStars(value);
      });

      star.addEventListener('mouseenter', function () {
        const value = parseInt(star.dataset.value);
        highlightStars(value);
      });

      star.addEventListener('mouseleave', function () {
        const current = ratingInput ? parseInt(ratingInput.value) : 0;
        updateStars(current);
      });
    });

    function highlightStars(count) {
      stars.forEach(function (s, i) {
        s.classList.toggle('active', i < count);
      });
    }

    function updateStars(count) {
      stars.forEach(function (s, i) {
        s.classList.toggle('active', i < count);
      });
    }

    // Set initial state from existing rating
    if (ratingInput && ratingInput.value) {
      updateStars(parseInt(ratingInput.value));
    }
  }

  initStarRating();

  // ----------------------------------------------------------------
  // 4. Confirm delete actions
  // ----------------------------------------------------------------
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      const msg = el.dataset.confirm || 'Are you sure?';
      if (!window.confirm(msg)) {
        e.preventDefault();
      }
    });
  });

  // ----------------------------------------------------------------
  // 5. Search form — clear filter button
  // ----------------------------------------------------------------
  const clearBtn = document.getElementById('clearFilters');
  if (clearBtn) {
    clearBtn.addEventListener('click', function () {
      window.location.href = clearBtn.dataset.url || window.location.pathname;
    });
  }

  // ----------------------------------------------------------------
  // 6. Animate stat cards on scroll (Intersection Observer)
  // ----------------------------------------------------------------
  const statValues = document.querySelectorAll('.stat-value');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    statValues.forEach(function (el) { observer.observe(el); });
  }

  function animateCounter(el) {
    const target   = parseInt(el.textContent.replace(/\D/g, '')) || 0;
    const duration = 800;
    const step     = Math.ceil(target / (duration / 16));
    let   current  = 0;

    const timer = setInterval(function () {
      current = Math.min(current + step, target);
      el.textContent = current;
      if (current >= target) clearInterval(timer);
    }, 16);
  }

  // ----------------------------------------------------------------
  // 7. Watchlist button AJAX-style feedback
  // ----------------------------------------------------------------
  document.querySelectorAll('.watchlist-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
      setTimeout(function () { btn.closest('form').submit(); }, 300);
    });
  });

  // ----------------------------------------------------------------
  // 8. Poster image lazy loading fallback
  // ----------------------------------------------------------------
  document.querySelectorAll('img[data-src]').forEach(function (img) {
    img.src = img.dataset.src;
    img.onerror = function () {
      img.src = 'https://placehold.co/300x450/1a1a2e/f5c518?text=No+Poster';
    };
  });

  // ----------------------------------------------------------------
  // 9. Tooltip init
  // ----------------------------------------------------------------
  const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltips.forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

  // ----------------------------------------------------------------
  // 10. Genre badge color map
  // ----------------------------------------------------------------
  const genreColors = {
    action:      '#e74c3c', adventure:  '#e67e22', animation: '#9b59b6',
    biography:   '#3498db', comedy:     '#f39c12', crime:     '#c0392b',
    documentary: '#16a085', drama:      '#2980b9', fantasy:   '#8e44ad',
    horror:      '#e74c3c', mystery:    '#2c3e50', romance:   '#e91e63',
    'sci-fi':    '#00bcd4', thriller:   '#ff5722', musical:   '#4caf50',
  };

  document.querySelectorAll('.badge-genre').forEach(function (badge) {
    const genre = badge.textContent.trim().toLowerCase();
    if (genreColors[genre]) {
      badge.style.borderColor = genreColors[genre];
      badge.style.color       = genreColors[genre];
      badge.style.background  = genreColors[genre] + '22';
    }
  });

});
