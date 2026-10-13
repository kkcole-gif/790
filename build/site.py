"""Static site builder for crd709cole.org.

Run from the repository root:  python3 build/site.py
Week content lives in build/weeks.py. Shared chrome lives here.
"""
import datetime as dt
import re
import html
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from weeks import COURSE, MOVEMENTS, WEEKS, MILESTONES  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ("https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,600"
         "&family=Public+Sans:ital,wght@0,400;0,700;1,400&display=swap")


def week_date(n):
    """Thursday of week n, skipping spring break."""
    first = dt.date.fromisoformat(COURSE["first_thursday"])
    if n == COURSE["meeting_week"]:
        return first + dt.timedelta(weeks=n - 2)
    return first + dt.timedelta(weeks=n - 1)


def week_when(n, short=True):
    if n == COURSE["meeting_week"]:
        return COURSE["meeting_window_short" if short else "meeting_window"]
    return fmt_date(week_date(n), short=short)


def fmt_date(d, short=False):
    return d.strftime("%b %-d" if short else "%A, %B %-d")


def week_href(n, from_weeks_dir=False):
    prefix = "" if from_weeks_dir else "weeks/"
    return f"{prefix}week-{n:02d}.html"


def page(title, body, depth=0, description=""):
    up = "../" * depth
    nav = [("Schedule", f"{up}index.html#schedule"),
           ("Milestones", f"{up}index.html#milestones"),
           ("Marginalia guide", f"{up}guides/marginalia.html"),
           ("Canvas", COURSE["canvas"]),
           ("Office hours", COURSE["office_hours"])]
    nav_html = "".join(f'<li><a href="{h}">{html.escape(t)}</a></li>' for t, h in nav)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{up}assets/site.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="site-name" href="{up}index.html">CRDM 790 &middot; Spring 2027</a>
    <nav class="site-nav" aria-label="Site"><ul>{nav_html}</ul></nav>
  </div>
</header>
<main id="main" class="wrap">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>CRDM 790, Issues in Communication, Rhetoric, and Digital Media. Listed by the registrar as CRD 790-001, Professional Paths in CRDM (class number 1605). NC State University, Spring 2027.</p>
    <p>Kirsti K. Cole, Tompkins Hall 226, <a href="mailto:{COURSE['email']}">{COURSE['email']}</a>.</p>
    <p>If any format on this site creates a barrier, email me and I will send an alternative before the next session.</p>
  </div>
</footer>
<script>
  window.addEventListener("beforeprint", function () {{
    document.querySelectorAll("details").forEach(function (d) {{ d.setAttribute("open", ""); }});
  }});
</script>
</body>
</html>
"""


def li(items):
    return "".join(f"<li>{i}</li>" for i in items)


def build_index():
    rows = []
    for m in MOVEMENTS:
        items = []
        for w in [w for w in WEEKS if w["movement"] == m["id"]]:
            d = week_date(w["n"])
            meta = []
            if w.get("due"):
                meta.append(f'<span class="chip due">Due: {html.escape(w["due"])}</span>')
            if w.get("guest"):
                meta.append('<span class="chip m{0}">Guest</span>'.format(m["id"]))
            meta.append(html.escape(w["summary"]))
            when = f'<span class="week-when"><b>Week {w["n"]}</b>{week_when(w["n"])}</span>'
            inner = (f'{when}<span class="week-title">{html.escape(w["title"])}</span>'
                     f'<span class="week-meta">{" ".join(meta)}</span>')
            if w.get("built"):
                items.append(f'<li><a href="{week_href(w["n"])}">{inner}</a></li>')
            else:
                items.append(f'<li><div class="pending">{inner}</div></li>')
            if w["n"] == COURSE["break_after_week"]:
                items.append('<li class="break-row">Spring break, March 15 to 19. No session.</li>')
        rows.append(f"""
<section class="movement m{m['id']}" aria-labelledby="mv{m['id']}">
  <p class="eyebrow">Movement {m['numeral']} &middot; Weeks {m['weeks']}</p>
  <h3 id="mv{m['id']}">{html.escape(m['title'])}</h3>
  <p>{m['blurb']}</p>
  <ul class="weeks">{''.join(items)}</ul>
</section>""")

    ms = []
    for m in MILESTONES:
        if m.get("due_text"):
            due = m["due_text"](week_date, fmt_date)
        else:
            due = f"Week {m['due_week']} ({fmt_date(week_date(m['due_week']), short=True)}), {m['due_note']}"
        ms.append(f"<li><strong><a href=\"{m['href']}\">{html.escape(m['title'])}</a></strong>, due {due}. "
                  f"{m['weight']} of the final grade. {m['gist']}</li>")

    body = f"""
<p class="eyebrow">NC State University &middot; Spring 2027 &middot; CRD 790-001, Professional Paths in CRDM</p>
<h1>Issues in Communication, Rhetoric, and Digital Media</h1>
<p class="lede">CRDM 790 sits between coursework and candidacy. Over fifteen weeks, each of you builds a committee, drafts an exam list, and writes a prospectus, while the cohort reads a shared body of theory together.</p>

<dl class="facts">
  <dt>Meets</dt><dd>Thursdays, 10:15 am to 1:00 pm, in person, January 14 to April 22</dd>
  <dt>Final</dt><dd>Prospectus due by 11:00 am, April 29, our scheduled exam slot</dd>
  <dt>Room</dt><dd>{COURSE['room']}</dd>
  <dt>Instructor</dt><dd>Kirsti K. Cole (she/her), <a href="mailto:{COURSE['email']}">{COURSE['email']}</a></dd>
  <dt>Office</dt><dd>Tompkins Hall 226</dd>
  <dt>Office hours</dt><dd>By appointment, <a href="{COURSE['office_hours']}">book a time</a></dd>
</dl>

<h2 id="where">Where things live</h2>
<div class="panel">
  <p><strong>This site</strong> holds each week's session page, the activity handouts, and the milestone guides. Every page opens without a login and prints cleanly.</p>
  <p><strong><a href="{COURSE['canvas']}">Canvas</a></strong> holds announcements, the readings, the reading lead notes, milestone submissions, and grades.</p>
</div>

<h2 id="schedule">Schedule</h2>
<p>Each week page lists what to read and bring, how the session runs, and what follows. Current students, alumni, and program faculty join us across the term.</p>
{''.join(rows)}

<h2 id="milestones">Milestones</h2>
<p>The course uses threshold grading. Each milestone is assessed as complete and substantive (full points), nearly there (80 percent), or not yet complete (no points). A nearly-there milestone revised to the complete threshold earns its full points. Submit through Canvas, by email, or in hard copy.</p>
<ul>{''.join(ms)}</ul>

<h2 id="access">Access and comfort</h2>
<p>Every session page and handout comes in more than one format. If a format creates a barrier for you, email me, and you will have an alternative before the next session. If you hold an accommodation letter, share it with me in the first two weeks.</p>
<p>Sessions run close to three hours. Bring food. Leave the room whenever you need to, without asking. You are welcome here as a whole person.</p>
"""
    out = page("CRDM 790 · Spring 2027", body, 0,
               "Session pages, handouts, and milestone guides for CRDM 790, Spring 2027, NC State University.")
    (ROOT / "index.html").write_text(out)


ICONS = {
    "book": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
    "pen": '<path d="M15 4l5 5L9 20H4v-5z"/><path d="M13 6l5 5"/>',
    "flag": '<path d="M5 22V3"/><path d="M5 4h12l-2.5 4L17 12H5"/>',
    "people": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><circle cx="17.5" cy="9" r="2.5"/><path d="M16 14.2a5 5 0 0 1 6 4.8"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "question": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6V14"/><circle cx="12" cy="17.5" r=".6"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "shelf": '<path d="M5 3v18M10 3v18M15 5l4 15"/>',
    "spark": '<path d="M12 3v6M12 15v6M3 12h6M15 12h6"/>',
}
FACT_ICON = {"Read": "book", "Bring": "pen", "Prepare": "pen", "Due": "flag", "Guest": "people",
             "Guests": "people", "When": "calendar"}


def icon(name):
    return (f'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" '
            f'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def fold(title, inner, ic, open_=False, hid=""):
    return (f'<details class="fold"{" open" if open_ else ""}><summary><h3{hid}>{icon(ic)}{title}</h3></summary>'
            f'<div class="fold-body">{inner}</div></details>')


def build_week(w):
    m = next(m for m in MOVEMENTS if m["id"] == w["movement"])
    c = w["content"]
    tiles = "".join(
        f'<div class="tile"><dt>{icon(FACT_ICON.get(k, "spark"))}{k}</dt><dd>{v}</dd></div>' for k, v in c["facts"])
    welcome = (f'<div class="welcome"><p>{c["welcome"]}</p><p class="sig">Kirsti</p></div>'
               if c.get("welcome") else "")
    out = [f"""
<header class="week-hero m{m['id']}">
  <p class="eyebrow">Movement {m['numeral']} &middot; Week {w['n']} &middot; {week_when(w['n'], short=False)}</p>
  <h1>{html.escape(w['title'])}</h1>
  {welcome}
</header>
<section aria-label="This week at a glance" class="glance"><dl>{tiles}</dl></section>
<p class="lede">{c['lede']}</p>"""]

    out.append(f"<h2 id=\"before\">{c.get('before_heading', 'Before we meet')}</h2>")
    if c.get("milestone"):
        mhref = next((m2["href"] for m2 in MILESTONES if m2["title"] in c["milestone"][0]
                      or (c["milestone"][0].startswith("Prospectus") and m2["title"] == "Dissertation Prospectus")), None)
        link = f'<p><a href="../{mhref}">Full guide to the {html.escape(c["milestone"][0])} milestone</a></p>' if mhref else ""
        out.append(f'<div class="panel milestone"><h3>{icon("flag")}Milestone due: {c["milestone"][0]}</h3><p>{c["milestone"][1]}</p>{link}</div>')
    if c.get("read"):
        out.append(f"<h3>{icon('book')}Read</h3><ul>{li(c['read'])}</ul>"
                   '<p class="aside">Read with a pen. The <a href="../guides/marginalia.html">marginalia guide</a> describes the practice.</p>')
    if c.get("bring"):
        out.append(f"<h3>{icon('pen')}{c.get('bring_heading', 'Write and bring')}</h3><ul>{li(c['bring'])}</ul>")
    if c.get("questions"):
        out.append(fold(c.get('questions_heading', 'Questions to carry into the reading'),
                        f"<ul>{li(c['questions'])}</ul>", "question"))

    out.append(f"<h2 id=\"in-class\">{c.get('in_class_heading', 'When we meet')}</h2>{c.get('in_class_intro', '')}")
    if c.get("schedule"):
        sched = "".join(f'<tr><th scope="row">{t}</th><td>{a}</td></tr>' for t, a in c["schedule"])
        out.append(fold("Session plan",
                        f'<table class="schedule"><thead><tr><th scope="col">Time</th><th scope="col">Activity</th></tr></thead><tbody>{sched}</tbody></table>',
                        "clock", open_=True))
    for act in c.get("activities", []):
        handout = f'<p><a href="../{act["handout"]}">Open the full handout</a></p>' if act.get("handout") else ""
        out.append(fold(html.escape(act["title"]),
                        f"<p>{act['intro']}</p><ol class=\"steps\">{li(act['steps'])}</ol>{handout}", "spark"))
    if c.get("after"):
        out.append(f"<h2 id=\"after\">{c.get('after_heading', 'After we meet')}</h2><ul class=\"after\">{li(c['after'])}</ul>")
    if c.get("further"):
        out.append(fold("Further reading, if this week opened something up", f"<ul>{li(c['further'])}</ul>", "shelf"))
    parts = ["\n".join(out)]
    prev_w = next((x for x in WEEKS if x["n"] == w["n"] - 1), None)
    next_w = next((x for x in WEEKS if x["n"] == w["n"] + 1), None)
    pager = []
    if prev_w:
        label = f'Previous: Week {prev_w["n"]}, {html.escape(prev_w["title"])}'
        pager.append(f'<a href="{week_href(prev_w["n"], True)}" rel="prev">{label}</a>' if prev_w.get("built") else f"<span>{label}</span>")
    else:
        pager.append("<span></span>")
    if next_w:
        label = f'Next: Week {next_w["n"]}, {html.escape(next_w["title"])}'
        pager.append(f'<a href="{week_href(next_w["n"], True)}" rel="next">{label}</a>' if next_w.get("built") else f"<span>{label}</span>")
    parts.append(f'<nav class="pager" aria-label="Weeks">{"".join(pager)}</nav>')
    out = page(f"Week {w['n']}: {w['title']} · CRDM 790", "".join(parts), 1, c["lede"])
    (ROOT / "weeks" / f"week-{w['n']:02d}.html").write_text(out)


def build_pages():
    """Wrap each fragment in build/pages. First line of a fragment is <!-- title | description -->."""
    src = ROOT / "build" / "pages"
    n = 0
    for frag in sorted(src.rglob("*.html")):
        rel = frag.relative_to(src)
        text = frag.read_text()
        head, body = text.split("\n", 1)
        title, desc = [x.strip() for x in head.strip()[4:-3].split("|", 1)]
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(f"{title} · CRDM 790", body, len(rel.parts) - 1, desc))
        n += 1
    return n


def build_redirects():
    """Old slide and support files redirect to their replacements."""
    targets = {"CRDM790_Perusall.html": "guides/marginalia.html",
               "guides/perusall.html": "marginalia.html",
               "CRDM790_Submissions.html": "index.html#milestones",
               "milestones/m2-draft-exam-list.html": "m3-draft-exam-list.html",
               "milestones/m3-committee-confirmation.html": "m2-committee-confirmation.html"}
    for f in ROOT.glob("CRDM790_Week*.html"):
        n = int(re.search(r"Week(\d+)", f.name).group(1))
        targets[f.name] = f"weeks/week-{n:02d}.html"
    for name, dest in targets.items():
        (ROOT / name).write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Moved · CRDM 790</title>
<meta http-equiv="refresh" content="0; url={dest}"><link rel="canonical" href="{dest}"></head>
<body><p>This page has moved to <a href="{dest}">its new address</a>.</p></body></html>
""")
    return len(targets)


if __name__ == "__main__":
    print("redirected", build_redirects(), "old pages")
    print("built", build_pages(), "support pages")
    (ROOT / "weeks").mkdir(exist_ok=True)
    build_index()
    for w in WEEKS:
        if w.get("built"):
            build_week(w)
    print("built", 1 + sum(1 for w in WEEKS if w.get("built")), "pages")
