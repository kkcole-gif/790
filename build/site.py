"""Static site builder for crd709cole.org.

Run from the repository root:  python3 build/site.py
Week content lives in build/weeks.py. Shared chrome lives here.
"""
import datetime as dt
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
    <p>CRDM 790, Issues in Communication, Rhetoric, and Digital Media. NC State University, Spring 2027.</p>
    <p>Kirsti K. Cole, Tompkins Hall 226, <a href="mailto:{COURSE['email']}">{COURSE['email']}</a>.</p>
    <p>If any format on this site creates a barrier, email me and I will send an alternative before the next session.</p>
  </div>
</footer>
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
        ms.append(f"<li><strong>{html.escape(m['title'])}</strong>, due {due}. "
                  f"{m['weight']} of the final grade. {m['gist']}</li>")

    body = f"""
<p class="eyebrow">NC State University &middot; Spring 2027</p>
<h1>Issues in Communication, Rhetoric, and Digital Media</h1>
<p class="lede">CRDM 790 sits between coursework and candidacy. Over fifteen weeks, each of you builds a committee, drafts an exam list, and writes a prospectus, while the cohort reads a shared body of theory together.</p>

<dl class="facts">
  <dt>Meets</dt><dd>Thursdays, 10:15 am to 1:00 pm, in person</dd>
  <dt>Room</dt><dd>{COURSE['room']}</dd>
  <dt>Instructor</dt><dd>Kirsti K. Cole (she/her), <a href="mailto:{COURSE['email']}">{COURSE['email']}</a></dd>
  <dt>Office</dt><dd>Tompkins Hall 226</dd>
  <dt>Office hours</dt><dd>By appointment, <a href="{COURSE['office_hours']}">book a time</a></dd>
</dl>

<h2 id="where">Where things live</h2>
<div class="panel">
  <p><strong>This site</strong> holds each week's session page, the activity handouts, and the milestone guides. Every page opens without a login and prints cleanly.</p>
  <p><strong><a href="{COURSE['canvas']}">Canvas</a></strong> holds announcements, the Perusall readings, milestone submissions, and grades.</p>
</div>

<h2 id="schedule">Schedule</h2>
<p>Each week page lists what to read and bring, how the session runs, and what follows. Pages appear here as the semester approaches. Current students, alumni, and program faculty join us across the term.</p>
{''.join(rows)}

<h2 id="milestones">Milestones</h2>
<p>The course uses threshold grading. Each milestone is assessed as complete and substantive, nearly there, or not yet complete. Submit through Canvas, by email, or in hard copy.</p>
<ul>{''.join(ms)}</ul>

<h2 id="access">Access and comfort</h2>
<p>Every session page and handout comes in more than one format. If a format creates a barrier for you, email me, and you will have an alternative before the next session. If you hold an accommodation letter, share it with me in the first two weeks.</p>
<p>Sessions run close to three hours. Bring food. Leave the room whenever you need to, without asking. You are welcome here as a whole person.</p>
"""
    out = page("CRDM 790 · Spring 2027", body, 0,
               "Session pages, handouts, and milestone guides for CRDM 790, Spring 2027, NC State University.")
    (ROOT / "index.html").write_text(out)


def build_week(w):
    m = next(m for m in MOVEMENTS if m["id"] == w["movement"])
    c = w["content"]
    out = [f"""
<div class="week-head m{m['id']}">
  <p class="eyebrow">Movement {m['numeral']} &middot; Week {w['n']} &middot; {week_when(w['n'], short=False)}</p>
  <h1>{html.escape(w['title'])}</h1>
</div>
<p class="lede">{c['lede']}</p>
<dl class="facts">{''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in c['facts'])}</dl>
<h2 id="before">{c.get('before_heading', 'Before class')}</h2>"""]
    if c.get("milestone"):
        out.append(f'<div class="panel milestone"><h3>Milestone due: {c["milestone"][0]}</h3><p>{c["milestone"][1]}</p></div>')
    if c.get("read"):
        out.append(f"<h3>Read</h3><ul>{li(c['read'])}</ul>")
    if c.get("bring"):
        out.append(f"<h3>{c.get('bring_heading', 'Write and bring')}</h3><ul>{li(c['bring'])}</ul>")
    if c.get("questions"):
        out.append(f"<h3>{c.get('questions_heading', 'Questions to carry into the reading')}</h3><ul>{li(c['questions'])}</ul>")
    out.append(f"<h2 id=\"in-class\">{c.get('in_class_heading', 'In class')}</h2>{c.get('in_class_intro', '')}")
    if c.get("schedule"):
        sched = "".join(f'<tr><th scope="row">{t}</th><td>{a}</td></tr>' for t, a in c["schedule"])
        out.append('<table class="schedule"><caption class="eyebrow" style="text-align:left;margin:0 0 .3rem">Session plan</caption>'
                   f'<thead><tr><th scope="col">Time</th><th scope="col">Activity</th></tr></thead><tbody>{sched}</tbody></table>')
    for act in c.get("activities", []):
        out.append(f"""<div class="panel">
<h3>{html.escape(act['title'])}</h3>
<p>{act['intro']}</p>
<ol class="steps">{li(act['steps'])}</ol>
</div>""")
    if c.get("after"):
        out.append(f"<h2 id=\"after\">{c.get('after_heading', 'After class')}</h2><ul>{li(c['after'])}</ul>")
    if c.get("further"):
        out.append(f"<h2 id=\"further\">Further reading</h2><ul>{li(c['further'])}</ul>")
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


if __name__ == "__main__":
    (ROOT / "weeks").mkdir(exist_ok=True)
    build_index()
    for w in WEEKS:
        if w.get("built"):
            build_week(w)
    print("built", 1 + sum(1 for w in WEEKS if w.get("built")), "pages")
