(function () {
  'use strict';

  var specs = Array.prototype.slice.call(document.querySelectorAll('.spec'));
  var items = Array.prototype.slice.call(document.querySelectorAll('.speclist li'));
  var total = specs.length;
  var passed = 0;
  var startedAt = Date.now();

  /* ---------- run summary ---------- */

  function fmtDuration(ms) {
    var s = Math.floor(ms / 1000);
    var m = Math.floor(s / 60);
    s = s % 60;
    return m > 0 ? m + 'm ' + (s < 10 ? '0' : '') + s + 's' : s + 's';
  }

  function updateSummary() {
    document.getElementById('passCount').textContent = passed;
    document.getElementById('pendCount').textContent = total - passed;
    document.getElementById('railFill').style.width = (passed / total * 100) + '%';

    var foot = document.getElementById('runnerFoot');
    var label = document.getElementById('footLabel');
    if (passed === total) {
      foot.classList.add('complete');
      label.textContent = '\u2713 ' + total + ' passed (' + fmtDuration(Date.now() - startedAt) + ')';
    } else {
      foot.classList.remove('complete');
      label.textContent = passed + '/' + total + ' specs passed';
    }
  }

  function setPassed(spec, value) {
    var idx = specs.indexOf(spec);
    var item = items[idx];
    var btn = spec.querySelector('.markdone');

    spec.classList.toggle('done', value);
    if (item) item.classList.toggle('done', value);

    spec.querySelector('.pill').textContent = value ? 'passed' : 'pending';
    if (item) item.querySelector('.glyph').textContent = value ? '\u2713' : '\u25CB';
    btn.querySelector('.tick').textContent = value ? '\u2713' : '\u25CB';
    btn.querySelector('.markdone-label').textContent = value ? 'Passed' : 'Mark as passed';
    btn.setAttribute('aria-pressed', String(value));

    passed = specs.filter(function (s) { return s.classList.contains('done'); }).length;
    updateSummary();
  }

  specs.forEach(function (spec) {
    var btn = spec.querySelector('.markdone');
    btn.addEventListener('click', function () {
      setPassed(spec, !spec.classList.contains('done'));
    });
  });

  document.getElementById('resetBtn').addEventListener('click', function () {
    specs.forEach(function (s) { setPassed(s, false); });
    startedAt = Date.now();
  });

  updateSummary();

  /* ---------- copy buttons ---------- */

  var COPY_ICON = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="5.5" y="5.5" width="8" height="9" rx="1.5"/><path d="M10.5 3.5v-1a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h1"/></svg>';
  var OK_ICON = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 8.5l3.2 3.2L13 5"/></svg>';

  document.querySelectorAll('.copy').forEach(function (btn) {
    btn.innerHTML = COPY_ICON + '<span>Copy</span>';
    btn.addEventListener('click', function () {
      var code = btn.closest('.codeblock').querySelector('pre').innerText;
      var done = function () {
        btn.classList.add('ok');
        btn.innerHTML = OK_ICON + '<span>Copied</span>';
        setTimeout(function () {
          btn.classList.remove('ok');
          btn.innerHTML = COPY_ICON + '<span>Copy</span>';
        }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(code).then(done, fallback);
      } else {
        fallback();
      }
      function fallback() {
        var ta = document.createElement('textarea');
        ta.value = code;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); done(); } catch (e) { /* clipboard unavailable */ }
        document.body.removeChild(ta);
      }
    });
  });

  /* ---------- search ---------- */

  var search = document.getElementById('search');
  var noResults = document.getElementById('noResults');
  var index = specs.map(function (s) { return s.innerText.toLowerCase(); });

  function runSearch() {
    var q = search.value.trim().toLowerCase();
    var hits = 0;

    specs.forEach(function (spec, i) {
      var match = !q || index[i].indexOf(q) !== -1;
      spec.classList.toggle('hidden', !match);
      if (items[i]) items[i].classList.toggle('hidden', !match);
      if (match) hits++;
    });

    document.querySelector('.runner-head').textContent =
      q ? hits + ' of ' + total + ' specs match' : 'Running ' + total + ' specs';
    noResults.classList.toggle('show', hits === 0);
    document.getElementById('queryEcho').textContent = q;
    document.querySelector('.hero').style.display = q ? 'none' : '';
  }

  search.addEventListener('input', runSearch);
  search.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { search.value = ''; runSearch(); search.blur(); }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== search) {
      e.preventDefault();
      search.focus();
      search.select();
    }
  });

  /* ---------- active section tracking ---------- */

  function markActive() {
    var offset = 140;
    var current = 0;
    for (var i = 0; i < specs.length; i++) {
      if (specs[i].classList.contains('hidden')) continue;
      if (specs[i].getBoundingClientRect().top <= offset) current = i;
    }
    items.forEach(function (li, i) { li.classList.toggle('active', i === current); });

    var active = items[current];
    if (active && !active.classList.contains('hidden')) {
      var list = document.querySelector('.speclist');
      var top = active.offsetTop;
      if (top < list.scrollTop || top > list.scrollTop + list.clientHeight - 60) {
        list.scrollTo({ top: top - list.clientHeight / 2, behavior: 'smooth' });
      }
    }

    document.getElementById('toTop').classList.toggle('show', window.scrollY > 700);
  }

  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () { markActive(); ticking = false; });
  }, { passive: true });
  markActive();

  document.getElementById('toTop').addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  /* ---------- theme ---------- */

  var SUN = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="8" cy="8" r="3.1"/><path d="M8 1v1.6M8 13.4V15M15 8h-1.6M2.6 8H1M12.9 3.1l-1.1 1.1M4.2 11.8l-1.1 1.1M12.9 12.9l-1.1-1.1M4.2 4.2L3.1 3.1"/></svg>';
  var MOON = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M13.5 9.6A5.9 5.9 0 0 1 6.4 2.5 5.9 5.9 0 1 0 13.5 9.6z"/></svg>';

  var themeBtn = document.getElementById('themeBtn');
  function applyTheme(mode) {
    document.documentElement.setAttribute('data-theme', mode);
    themeBtn.innerHTML = mode === 'light' ? MOON : SUN;
    themeBtn.setAttribute('aria-label', mode === 'light' ? 'Switch to dark theme' : 'Switch to light theme');
  }
  applyTheme('dark');
  themeBtn.addEventListener('click', function () {
    applyTheme(document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light');
  });

  /* ---------- mobile drawer ---------- */

  var sidebar = document.querySelector('.sidebar');
  var scrim = document.querySelector('.scrim');

  function toggleNav(open) {
    sidebar.classList.toggle('open', open);
    scrim.classList.toggle('open', open);
  }
  document.getElementById('menuBtn').addEventListener('click', function () {
    toggleNav(!sidebar.classList.contains('open'));
  });
  scrim.addEventListener('click', function () { toggleNav(false); });
  document.querySelectorAll('.speclist a').forEach(function (a) {
    a.addEventListener('click', function () {
      if (window.innerWidth <= 860) toggleNav(false);
    });
  });
})();
