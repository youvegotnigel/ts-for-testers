#!/usr/bin/env python3
"""
Inline figures and interactive blocks for the cheat sheet.

The Markdown source drops a token on its own line, for example:

    [widget:promise-receipt]

and build.py swaps it for the HTML below. Keeping them here means the
Markdown stays readable and downloadable while the diagrams stay in one
place. Every colour comes from a CSS custom property, so the figures
follow the dark and light themes without a second copy.

Arrow heads: each SVG defines its own marker so the ids stay unique
across the page.
"""


def _defs(mid):
    return (
        '<defs><marker id="%s" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto">'
        '<path d="M0 0L10 5L0 10z" fill="currentColor" style="color:var(--text-3)"/>'
        "</marker></defs>" % mid
    )


def _figure(caption, svg):
    # The inner div scrolls on narrow screens so the labels stay legible,
    # the same trick .table-scroll uses for wide tables.
    return (
        '<figure class="fig"><div class="fig-scroll">%s</div>'
        "<figcaption>%s</figcaption></figure>" % (svg, caption)
    )


# ----------------------------------------------------------------------
# 1. A promise is a receipt
# ----------------------------------------------------------------------

def promise_receipt(_render_code):
    svg = """<svg class="diagram" viewBox="0 0 660 150" role="img" aria-label="Ordering coffee returns a buzzer immediately, the coffee or an error arrives later">
%s
<text class="d-label" x="8" y="24" style="fill:var(--text-3)">TIME →</text>
<line x1="8" y1="34" x2="652" y2="34" stroke="var(--line)" stroke-width="1"/>

<rect class="d-box" x="8" y="52" width="128" height="66" rx="9"/>
<text class="d-title" x="72" y="80" text-anchor="middle">You order</text>
<text class="d-sub" x="72" y="98" text-anchor="middle">orderCoffee()</text>

<path class="d-arrow" d="M140 85 L188 85" marker-end="url(#ah-receipt)"/>
<text class="d-sub" x="164" y="76" text-anchor="middle">0 ms</text>

<rect class="d-box" x="192" y="42" width="140" height="86" rx="9" style="stroke:var(--amber)"/>
<text class="d-title" x="262" y="70" text-anchor="middle" style="fill:var(--amber)">Buzzer</text>
<text class="d-sub" x="262" y="88" text-anchor="middle">Promise&lt;Coffee&gt;</text>
<text class="d-sub" x="262" y="105" text-anchor="middle">state: pending</text>
<text class="d-sub" x="262" y="119" text-anchor="middle">you have this NOW</text>

<path class="d-arrow" d="M336 85 L392 85" marker-end="url(#ah-receipt)"/>
<text class="d-sub" x="364" y="76" text-anchor="middle">180 s</text>
<text class="d-sub" x="364" y="102" text-anchor="middle">await</text>

<rect class="d-box" x="396" y="52" width="128" height="66" rx="9" style="stroke:var(--green)"/>
<text class="d-title" x="460" y="80" text-anchor="middle" style="fill:var(--green)">Coffee</text>
<text class="d-sub" x="460" y="98" text-anchor="middle">fulfilled</text>

<path class="d-arrow" d="M336 100 Q 430 168 556 124" style="stroke:var(--red)" marker-end="url(#ah-receipt)"/>
<rect class="d-box" x="540" y="52" width="112" height="66" rx="9" style="stroke:var(--red)"/>
<text class="d-title" x="596" y="76" text-anchor="middle" style="fill:var(--red)">Sorry, the</text>
<text class="d-title" x="596" y="92" text-anchor="middle" style="fill:var(--red)">machine broke</text>
<text class="d-sub" x="596" y="109" text-anchor="middle">rejected</text>
</svg>""" % _defs("ah-receipt")
    return _figure("The order returns instantly. The result arrives later, or fails.", svg)


# ----------------------------------------------------------------------
# 2. The three states
# ----------------------------------------------------------------------

def promise_states(_render_code):
    svg = """<svg class="diagram" viewBox="0 0 660 190" role="img" aria-label="Promise state machine: pending moves to fulfilled or rejected, then it is settled and cannot change">
%s
<rect class="d-box" x="16" y="66" width="150" height="60" rx="9" style="stroke:var(--amber)"/>
<text class="d-title" x="91" y="92" text-anchor="middle" style="fill:var(--amber)">pending</text>
<text class="d-sub" x="91" y="110" text-anchor="middle">still brewing</text>

<path class="d-arrow" d="M170 84 L246 44" style="stroke:var(--green)" marker-end="url(#ah-states)"/>
<text class="d-sub" x="205" y="50" text-anchor="middle" style="fill:var(--green)">resolve</text>

<path class="d-arrow" d="M170 108 L246 148" style="stroke:var(--red)" marker-end="url(#ah-states)"/>
<text class="d-sub" x="205" y="152" text-anchor="middle" style="fill:var(--red)">reject</text>

<rect class="d-box" x="250" y="12" width="170" height="60" rx="9" style="stroke:var(--green)"/>
<text class="d-title" x="335" y="38" text-anchor="middle" style="fill:var(--green)">fulfilled</text>
<text class="d-sub" x="335" y="56" text-anchor="middle">await gives you the value</text>

<rect class="d-box" x="250" y="120" width="170" height="60" rx="9" style="stroke:var(--red)"/>
<text class="d-title" x="335" y="146" text-anchor="middle" style="fill:var(--red)">rejected</text>
<text class="d-sub" x="335" y="164" text-anchor="middle">await throws</text>

<path class="d-arrow" d="M424 42 L500 74" marker-end="url(#ah-states)"/>
<path class="d-arrow" d="M424 150 L500 118" marker-end="url(#ah-states)"/>
<rect class="d-box" x="504" y="66" width="146" height="60" rx="9"/>
<text class="d-title" x="577" y="90" text-anchor="middle">settled</text>
<text class="d-sub" x="577" y="108" text-anchor="middle">frozen forever</text>
</svg>""" % _defs("ah-states")
    return _figure(
        "A promise settles once. After that it never changes, and re-awaiting "
        "returns the same result instantly.", svg)


# ----------------------------------------------------------------------
# 3. What await actually unwraps
# ----------------------------------------------------------------------

def await_unwraps(_render_code):
    svg = """<svg class="diagram" viewBox="0 0 660 200" role="img" aria-label="Without await the variable holds a promise wrapper, with await it holds the value">
<text class="d-label" x="10" y="18" style="fill:var(--red)">WITHOUT await</text>
<rect class="d-box" x="10" y="28" width="290" height="62" rx="9" style="stroke:var(--red)"/>
<text class="d-sub" x="24" y="54">const title =</text>
<rect x="120" y="38" width="168" height="42" rx="7" fill="var(--amber-dim)" stroke="var(--amber)"/>
<text class="d-title" x="204" y="56" text-anchor="middle" style="fill:var(--amber);font-size:11px">Promise wrapper</text>
<text class="d-sub" x="204" y="72" text-anchor="middle">{ state: pending }</text>
<text class="d-sub" x="24" y="112" style="fill:var(--red)">typeof title === 'object'</text>
<text class="d-sub" x="24" y="128" style="fill:var(--red)">Boolean(title) === true  (always)</text>

<text class="d-label" x="360" y="18" style="fill:var(--green)">WITH await</text>
<rect class="d-box" x="360" y="28" width="290" height="62" rx="9" style="stroke:var(--green)"/>
<text class="d-sub" x="374" y="54">const title =</text>
<rect x="470" y="38" width="168" height="42" rx="7" fill="var(--green-dim)" stroke="var(--green)"/>
<text class="d-title" x="554" y="64" text-anchor="middle" style="fill:var(--green);font-size:12px">'Dashboard'</text>
<text class="d-sub" x="374" y="112" style="fill:var(--green)">typeof title === 'string'</text>
<text class="d-sub" x="374" y="128" style="fill:var(--green)">comparisons behave normally</text>

<line x1="10" y1="152" x2="650" y2="152" stroke="var(--line)"/>
<text class="d-title" x="330" y="178" text-anchor="middle" style="fill:var(--amber)">await unwraps the box. Nothing else does.</text>
</svg>"""
    return _figure(
        "The unawaited variable is not empty and not undefined. "
        "It is a full, valid, useless object.", svg)


# ----------------------------------------------------------------------
# 4. Awaited vs floating
# ----------------------------------------------------------------------

def floating_promise(_render_code):
    svg = """<svg class="diagram" viewBox="0 0 660 230" role="img" aria-label="An awaited call finishes before the assertion starts, a floating call overlaps it">
<text class="d-label" x="10" y="16" style="fill:var(--green)">AWAITED</text>
<rect x="10" y="26" width="640" height="72" rx="9" class="d-box"/>
<rect x="24" y="42" width="180" height="18" rx="5" fill="var(--blue)"/>
<text class="d-sub" x="114" y="55" text-anchor="middle" style="fill:#fff">await click()</text>
<rect x="212" y="42" width="150" height="18" rx="5" fill="var(--green)"/>
<text class="d-sub" x="287" y="55" text-anchor="middle" style="fill:#fff">expect(toast)</text>
<text class="d-sub" x="24" y="84">click finishes, THEN the assertion starts. Order guaranteed.</text>
<text class="d-title" x="620" y="60" text-anchor="middle" style="fill:var(--green);font-size:16px">✓</text>

<text class="d-label" x="10" y="126" style="fill:var(--red)">FLOATING (no await)</text>
<rect x="10" y="136" width="640" height="84" rx="9" class="d-box" style="stroke:var(--red)"/>
<rect x="24" y="152" width="180" height="18" rx="5" fill="var(--blue)" opacity=".32"/>
<text class="d-sub" x="114" y="165" text-anchor="middle" style="fill:var(--text-2)">click() still running…</text>
<rect x="24" y="176" width="150" height="18" rx="5" fill="var(--red)"/>
<text class="d-sub" x="99" y="189" text-anchor="middle" style="fill:#fff">expect(toast)</text>
<text class="d-sub" x="184" y="190" style="fill:var(--red)">starts immediately, overlaps the click</text>
<text class="d-sub" x="24" y="214">Both run at once. Whether it passes depends on which wins the race.</text>
<text class="d-title" x="620" y="182" text-anchor="middle" style="fill:var(--red);font-size:16px">?</text>
</svg>"""
    return _figure(
        "The floating promise does not skip the work. "
        "It removes the ordering guarantee.", svg)


# ----------------------------------------------------------------------
# 5. The constructor race
# ----------------------------------------------------------------------

def constructor_race(_render_code):
    svg = """<svg class="diagram" viewBox="0 0 660 210" role="img" aria-label="The constructor returns before its async work completes, so the assertion reads an undefined field">
<text class="d-sub" x="14" y="18" style="fill:var(--text-3)">the assertion lands inside the gap</text>
<line x1="14" y1="176" x2="646" y2="176" stroke="var(--line)" stroke-width="1.5"/>
<text class="d-sub" x="14" y="196">t = 0</text>
<text class="d-sub" x="600" y="196">time →</text>

<rect x="20" y="30" width="120" height="26" rx="6" fill="var(--blue-dim)" stroke="var(--blue)"/>
<text class="d-sub" x="80" y="47" text-anchor="middle" style="fill:var(--blue)">new Dashboard()</text>
<line x1="80" y1="56" x2="80" y2="176" stroke="var(--blue)" stroke-dasharray="3 3"/>

<rect x="150" y="70" width="330" height="26" rx="6" fill="var(--amber-dim)" stroke="var(--amber)"/>
<text class="d-sub" x="315" y="87" text-anchor="middle" style="fill:var(--amber)">this.load() still running… awaiting count()</text>
<line x1="150" y1="96" x2="150" y2="176" stroke="var(--amber)" stroke-dasharray="3 3"/>
<line x1="480" y1="96" x2="480" y2="176" stroke="var(--amber)" stroke-dasharray="3 3"/>
<text class="d-sub" x="480" y="112" text-anchor="middle" style="fill:var(--amber)">field finally set</text>

<rect x="150" y="122" width="150" height="26" rx="6" fill="var(--red-dim)" stroke="var(--red)"/>
<text class="d-sub" x="225" y="139" text-anchor="middle" style="fill:var(--red)">expect(patientCount)</text>
<line x1="225" y1="148" x2="225" y2="176" stroke="var(--red)" stroke-dasharray="3 3"/>
<text class="d-sub" x="225" y="166" text-anchor="middle" style="fill:var(--red)">reads undefined</text>
</svg>"""
    return _figure(
        "The constructor hands back an object that is still filling itself in.", svg)


# ----------------------------------------------------------------------
# 6. Diagnosis flow
# ----------------------------------------------------------------------

def diagnosis_flow(_render_code):
    svg = """<svg class="diagram" viewBox="0 0 660 400" role="img" aria-label="Flowchart for diagnosing whether a flaky test is caused by a promise bug">
%s
<rect x="220" y="6" width="220" height="40" rx="8" class="d-box" style="stroke:var(--amber)"/>
<text class="d-title" x="330" y="31" text-anchor="middle" style="fill:var(--amber)">A test fails intermittently</text>
<path class="d-arrow" d="M330 46 L330 68" marker-end="url(#ah-flow)"/>

<rect x="180" y="70" width="300" height="42" rx="8" class="d-box"/>
<text class="d-label" x="330" y="88" text-anchor="middle">Does it pass locally and fail in CI,</text>
<text class="d-label" x="330" y="103" text-anchor="middle">or fail more with more workers?</text>

<path class="d-arrow" d="M180 91 L92 91 L92 128" marker-end="url(#ah-flow)"/>
<text class="d-sub" x="120" y="85" style="fill:var(--red)">no</text>
<rect x="12" y="130" width="160" height="44" rx="8" class="d-box"/>
<text class="d-label" x="92" y="149" text-anchor="middle">Probably environment,</text>
<text class="d-label" x="92" y="164" text-anchor="middle">data, or a real bug</text>

<path class="d-arrow" d="M330 112 L330 136" marker-end="url(#ah-flow)"/>
<text class="d-sub" x="340" y="130" style="fill:var(--green)">yes</text>

<rect x="180" y="138" width="300" height="42" rx="8" class="d-box"/>
<text class="d-label" x="330" y="156" text-anchor="middle">Is the failing line the one that</text>
<text class="d-label" x="330" y="171" text-anchor="middle">actually does the broken thing?</text>

<path class="d-arrow" d="M330 180 L330 204" marker-end="url(#ah-flow)"/>
<text class="d-sub" x="340" y="197" style="fill:var(--red)">no, it is downstream</text>

<rect x="150" y="206" width="360" height="44" rx="8" class="d-box" style="stroke:var(--red)"/>
<text class="d-title" x="330" y="225" text-anchor="middle" style="fill:var(--red)">Strong signal: floating promise upstream</text>
<text class="d-sub" x="330" y="241" text-anchor="middle">read every line above the failure for a missing await</text>

<path class="d-arrow" d="M330 250 L330 272" marker-end="url(#ah-flow)"/>

<rect x="140" y="274" width="380" height="42" rx="8" class="d-box"/>
<text class="d-label" x="330" y="292" text-anchor="middle">Run the linter: no-floating-promises,</text>
<text class="d-label" x="330" y="307" text-anchor="middle">no-misused-promises, await-thenable</text>

<path class="d-arrow" d="M330 316 L330 332 L220 332 L220 344" marker-end="url(#ah-flow)"/>
<path class="d-arrow" d="M330 316 L330 332 L454 332 L454 344" marker-end="url(#ah-flow)"/>

<rect x="104" y="346" width="232" height="44" rx="8" class="d-box" style="stroke:var(--green)"/>
<text class="d-title" x="220" y="366" text-anchor="middle" style="fill:var(--green)">Rule fires</text>
<text class="d-sub" x="220" y="382" text-anchor="middle">that is your bug. Fix and move on.</text>

<rect x="344" y="346" width="220" height="44" rx="8" class="d-box"/>
<text class="d-title" x="454" y="366" text-anchor="middle">Nothing fires</text>
<text class="d-sub" x="454" y="382" text-anchor="middle">open the trace, compare timings</text>
</svg>""" % _defs("ah-flow")
    return _figure(
        "Run the linter before you read the trace. It costs thirty seconds and "
        "resolves most of these outright.", svg)


# ----------------------------------------------------------------------
# Tabbed comparisons
# ----------------------------------------------------------------------

def _tabs(group, label, panes, render_code):
    """panes: list of (tab label, language, code, trailing note HTML or '')."""
    tabs, bodies = [], []
    for i, (name, lang, code, note) in enumerate(panes):
        first = i == 0
        tabs.append(
            '<button class="flip-tab" type="button" role="tab" id="tab-%s-%d" '
            'aria-controls="pane-%s-%d" aria-selected="%s" tabindex="%s">%s</button>'
            % (group, i, group, i, "true" if first else "false",
               "0" if first else "-1", name)
        )
        bodies.append(
            '<div class="flip-pane" role="tabpanel" id="pane-%s-%d" '
            'aria-labelledby="tab-%s-%d"%s>%s%s</div>'
            % (group, i, group, i, "" if first else " hidden",
               render_code(code, lang), note)
        )
    return (
        '<div class="flip">'
        '<div class="flip-tabs" role="tablist" aria-label="%s">%s</div>%s</div>'
        % (label, "".join(tabs), "".join(bodies))
    )


LOOP_FOREACH = """patients.forEach(async (p) => {
  await api.create(p);            // forEach throws this promise away
});
await expect(list).toHaveCount(3);  // runs before any create finishes
"""

LOOP_FOR_OF = """for (const p of patients) {
  await api.create(p);            // each one completes before the next starts
}
await expect(list).toHaveCount(3);  // safe
"""

LOOP_ALL = """await Promise.all(patients.map((p) => api.create(p)));
await expect(list).toHaveCount(3);
// Only when the items genuinely do not depend on each other.
"""


def loop_tabs(render_code):
    return _tabs("loops", "Ways to loop over async work", [
        ("forEach (broken)", "ts", LOOP_FOREACH, ""),
        ("for...of (correct)", "ts", LOOP_FOR_OF, ""),
        ("Promise.all (parallel)", "ts", LOOP_ALL, ""),
    ], render_code)


CLASS_FACTORY = """class DashboardPage {
  private constructor(
    private readonly page: Page,
    readonly patientCount: number,
  ) {}

  static async open(page: Page): Promise<DashboardPage> {
    await page.goto('/dashboard');
    const count = await page.locator('.row').count();
    return new DashboardPage(page, count);
  }
}

const dash = await DashboardPage.open(page);   // fully built, or not at all
"""

CLASS_LAZY = """class DashboardPage {
  constructor(private readonly page: Page) {}   // stays synchronous

  async patientCount(): Promise<number> {
    return this.page.locator('.row').count();   // read fresh, every call
  }
}

expect(await dash.patientCount()).toBe(12);
"""

CLASS_FIXTURE = """export const test = base.extend<{ dashboard: DashboardPage }>({
  dashboard: async ({ page }, use) => {
    const dash = await DashboardPage.open(page);
    await use(dash);
  },
});

test('shows every patient', async ({ dashboard }) => {
  // arrives fully constructed, with no await for anyone to forget
});
"""


def class_fix_tabs(render_code):
    return _tabs("classfix", "Three ways to keep async work out of a constructor", [
        ("Static factory", "ts", CLASS_FACTORY,
         "<p>The private constructor makes the unsafe path impossible. Nobody can "
         "call <code>new</code> by accident, so the compiler enforces the rule "
         "instead of a review comment.</p>"),
        ("Lazy getters", "ts", CLASS_LAZY,
         "<p>This is the right default for page objects. State read on demand "
         "cannot go stale, which is the same reason you store a "
         "<code>Locator</code> and never an <code>ElementHandle</code>.</p>"),
        ("Fixture (best)", "ts", CLASS_FIXTURE,
         "<p>A fixture puts the setup somewhere a test author cannot skip it. "
         "That is the framework level fix: remove the opportunity for the "
         "mistake rather than documenting it.</p>"),
    ], render_code)


# ----------------------------------------------------------------------
# The race simulator
# ----------------------------------------------------------------------

def _lane(idx, name, marker):
    return (
        '<div class="lane">'
        '<div class="lane-top"><span class="lane-name">%s</span>'
        '<span class="verdict pass" data-verdict="%d">passed</span></div>'
        '<div class="track">'
        '<div class="bar action" data-bar="%da"></div>'
        '<div class="bar assert pass" data-bar="%db"></div>%s</div></div>'
        % (name, idx, idx, idx, marker)
    )


def race_simulator(_render_code):
    presets = [("120", "Your laptop"), ("380", "CI, idle"),
               ("620", "CI, 8 workers"), ("860", "CI, box under load")]
    buttons = "".join(
        '<button class="sim-preset%s" type="button" data-ms="%s">%s</button>'
        % (" on" if ms == "120" else "", ms, label) for ms, label in presets)

    marker = ('<div class="sim-marker" data-marker>'
              '<span>retry budget ends</span></div>')

    return (
        '<div class="sim" data-sim>'
        '<div class="sim-head"><h4>Drag the machine speed</h4>'
        '<span class="sim-hint">same test, same code, both lanes</span></div>'
        '<div class="sim-row">'
        '<input type="range" class="sim-range" min="50" max="900" step="10" '
        'value="120" aria-label="How long the click takes, in milliseconds">'
        '<span class="sim-val" data-val>120 ms</span></div>'
        '<div class="sim-presets">%s</div>'
        '%s%s'
        '<div class="sim-legend">'
        '<span><i style="background:var(--blue)"></i>click running</span>'
        '<span><i style="background:var(--green)"></i>assertion, satisfied</span>'
        '<span><i style="background:var(--red)"></i>assertion, timed out</span>'
        "</div>"
        '<p class="sim-verdict ok" data-sim-verdict aria-live="polite"></p>'
        "</div>"
        % (buttons,
           _lane(1, "await page.click()  →  await expect(toast)", ""),
           _lane(2, "page.click()  →  await expect(toast)   [no await]", marker))
    )


# ----------------------------------------------------------------------

WIDGETS = {
    "promise-receipt": promise_receipt,
    "promise-states": promise_states,
    "await-unwraps": await_unwraps,
    "floating-promise": floating_promise,
    "constructor-race": constructor_race,
    "diagnosis-flow": diagnosis_flow,
    "loop-tabs": loop_tabs,
    "class-fix-tabs": class_fix_tabs,
    "race-simulator": race_simulator,
}


def render(name, render_code):
    """HTML for [widget:name]. Unknown names fail the build rather than
    silently leaving a token in the page."""
    if name not in WIDGETS:
        raise SystemExit(
            "Unknown widget '%s'. Known widgets: %s"
            % (name, ", ".join(sorted(WIDGETS)))
        )
    return WIDGETS[name](render_code)
