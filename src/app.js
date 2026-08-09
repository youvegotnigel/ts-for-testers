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
  /* textContent, not innerText, so collapsed tab panes stay searchable */
  var index = specs.map(function (s) { return s.textContent.toLowerCase(); });

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

  function highlight(current) {
    items.forEach(function (li, i) { li.classList.toggle('active', i === current); });

    var active = items[current];
    if (active && !active.classList.contains('hidden')) {
      var list = document.querySelector('.speclist');
      var top = active.offsetTop;
      if (top < list.scrollTop || top > list.scrollTop + list.clientHeight - 60) {
        list.scrollTo({ top: top - list.clientHeight / 2, behavior: 'smooth' });
      }
    }
  }

  function markActive() {
    var offset = 140;
    var current = 0;
    for (var i = 0; i < specs.length; i++) {
      if (specs[i].classList.contains('hidden')) continue;
      if (specs[i].getBoundingClientRect().top <= offset) current = i;
    }
    highlight(current);
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
  document.querySelectorAll('.speclist a').forEach(function (a, i) {
    a.addEventListener('click', function () {
      /* mark it straight away: clicking the last spec, or one already in
         view, scrolls too little to fire a scroll event */
      highlight(i);
      if (window.innerWidth <= 860) toggleNav(false);
    });
  });

  /* ---------- tabbed comparisons ---------- */

  document.querySelectorAll('.flip-tabs').forEach(function (tablist) {
    var tabs = Array.prototype.slice.call(tablist.querySelectorAll('.flip-tab'));
    var panes = tabs.map(function (tab) {
      return document.getElementById(tab.getAttribute('aria-controls'));
    });

    function select(i, moveFocus) {
      tabs.forEach(function (tab, j) {
        var on = i === j;
        tab.setAttribute('aria-selected', String(on));
        tab.tabIndex = on ? 0 : -1;
        if (panes[j]) panes[j].hidden = !on;
      });
      if (moveFocus) tabs[i].focus();
    }

    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { select(i, false); });
      tab.addEventListener('keydown', function (e) {
        if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
        var next = i + (e.key === 'ArrowRight' ? 1 : -1);
        if (next < 0 || next >= tabs.length) return;
        e.preventDefault();
        select(next, true);
      });
    });
  });

  /* ---------- the race simulator ----------
     Two lanes run the same test. The awaited lane is ordered by the
     language; the floating lane is ordered by luck. Slide the machine
     speed and watch only one of them break. */

  var RETRY_BUDGET = 500;   /* scaled stand-in for Playwright's 5s expect timeout */
  var HEAD_START = 40;      /* how far the unawaited test runs ahead */

  document.querySelectorAll('[data-sim]').forEach(function (sim) {
    var range = sim.querySelector('.sim-range');
    var readout = sim.querySelector('[data-val]');
    var summary = sim.querySelector('[data-sim-verdict]');
    var marker = sim.querySelector('[data-marker]');
    var presets = Array.prototype.slice.call(sim.querySelectorAll('.sim-preset'));

    var bars = {};
    sim.querySelectorAll('[data-bar]').forEach(function (b) { bars[b.dataset.bar] = b; });
    var verdicts = {};
    sim.querySelectorAll('[data-verdict]').forEach(function (v) { verdicts[v.dataset.verdict] = v; });

    function place(el, left, width) {
      el.style.left = left + '%';
      el.style.width = Math.max(width, 1.5) + '%';
    }

    function render() {
      var ms = +range.value;
      var deadline = HEAD_START + RETRY_BUDGET;
      var span = Math.max(ms + RETRY_BUDGET, 700);
      function pct(v) { return v / span * 100; }

      readout.textContent = ms + ' ms';

      /* awaited: the click finishes, then the assertion starts */
      place(bars['1a'], 0, pct(ms));
      place(bars['1b'], pct(ms), pct(60));

      /* floating: the assertion starts early and polls until it gives up */
      var passes = ms <= deadline;
      place(bars['2a'], 0, pct(ms));
      place(bars['2b'], pct(HEAD_START), pct(Math.max((passes ? ms : deadline) - HEAD_START, 20)));
      bars['2b'].className = 'bar assert ' + (passes ? 'pass' : 'fail');
      verdicts['2'].className = 'verdict ' + (passes ? 'pass' : 'fail');
      verdicts['2'].textContent = passes ? 'passed' : 'failed';
      marker.style.left = pct(deadline) + '%';
      marker.classList.toggle('flip', pct(deadline) > 55);

      summary.className = 'sim-verdict ' + (passes ? 'ok' : 'bad');
      summary.textContent = passes
        ? 'Passing by luck. The click finishes at ' + ms + ' ms, inside the '
          + deadline + ' ms retry budget, so the assertion catches it. '
          + 'Nothing in the code guarantees that.'
        : 'Failed. The click finishes at ' + ms + ' ms, past the ' + deadline
          + ' ms retry budget. Identical code, slower box. '
          + 'This is the CI only failure.';

      presets.forEach(function (p) { p.classList.toggle('on', +p.dataset.ms === ms); });
    }

    range.addEventListener('input', render);
    presets.forEach(function (p) {
      p.addEventListener('click', function () { range.value = p.dataset.ms; render(); });
    });
    render();
  });
})();
