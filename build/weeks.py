"""Course data for crd709cole.org. Edit here, then run build/site.py."""

COURSE = {
    # Confirm against the registrar's calendar. Week dates derive from this value.
    "first_thursday": "2027-01-14",
    "break_after_week": 10,
    # Week 10 has no group session. Individual meetings run across this window.
    "meeting_week": 10,
    "meeting_window": "Individual meetings, March 11 to 24",
    "meeting_window_short": "Mar 11\u201324",
    "room": "Winston Hall 20",
    "email": "kkcole2@ncsu.edu",
    "canvas": "https://ncsu.instructure.com/courses/798",
    "office_hours": "https://calendar.app.google/pgZeqTD9Kd9ZxBPX7",
}

MOVEMENTS = [
    {"id": 1, "numeral": "I", "weeks": "1 to 5", "title": "Who Are We and What Do We Think?",
     "blurb": "A shared critical vocabulary, and a first account of who each of you is as a scholar. Readings from Giroux, Benjamin, Mbembe, and Brown."},
    {"id": 2, "numeral": "II", "weeks": "6 to 10", "title": "What Do I Know and Who Helps Me Know It?",
     "blurb": "Committees, exam lists, and the labor behind both. Readings from Federici, Coverley, and Haraway."},
    {"id": 3, "numeral": "III", "weeks": "11 to 15", "title": "What Will I Make and Where Am I Going?",
     "blurb": "The prospectus, and the question of what the work is for. Readings from Marcuse and Ghosh."},
]

MILESTONES = [
    {"title": "Scholarly Identity Statement", "href": "milestones/m1-scholarly-identity.html", "due_week": 5, "due_note": "before class", "weight": "20%",
     "gist": "About 500 words on who you are as a scholar and what your research is for."},
    {"title": "Draft Exam List", "href": "milestones/m2-draft-exam-list.html", "due_week": 8, "due_note": "before class", "weight": "25%",
     "gist": "A working list with a rationale naming the fields it answers to and your position in each."},
    {"title": "Committee Confirmation", "href": "milestones/m3-committee-confirmation.html", "weight": "15%",
     "due_text": lambda wd, fd: "by March 24, the close of the Week 10 meeting window",
     "gist": "Your chair's confirmation, or a plan naming faculty and a timeline."},
    {"title": "Dissertation Prospectus", "href": "milestones/m4-prospectus.html", "weight": "40%",
     "due_text": lambda wd, fd: f"in two stages: a workshop draft before Week 14 ({fd(wd(14), True)}), and the final version by 11:00 am on {fd(wd(15) + __import__('datetime').timedelta(weeks=1), True)}, the close of our scheduled exam slot",
     "gist": "A problem, its place in the scholarship, a method, and stakes beyond the field. Nonacademic equivalents are welcome."},
]

WEEKS = [
    {"n": 1, "movement": 1, "title": "Arrivals",
     "summary": "Introductions, intellectual autobiographies, constellation mapping."},
    {"n": 2, "movement": 1, "title": "Critical Pedagogy and the Scholar-Critic",
     "summary": "Giroux, On Critical Pedagogy. Institutional autopsy."},
    {"n": 3, "movement": 1, "title": "The Past Is Not Past", "guest": True,
     "summary": "Benjamin, Illuminations. Wreckage and promise gallery. A current doctoral student joins us."},
    {"n": 4, "movement": 1, "title": "Who Gets to Live",
     "summary": "Mbembe, Necropolitics. Concept translation workshop."},
    {"n": 5, "movement": 1, "title": "The University Under Neoliberalism", "due": "Identity Statement",
     "summary": "Brown, Undoing the Demos. Identity statement exchange."},
    {"n": 6, "movement": 2, "title": "The Labor of Knowledge and the Labor of Committees", "guest": True, "built": True,
     "summary": "Federici, Caliban and the Witch. A recently advanced student joins us. Committee email workshop.",
     "content": {
        "welcome": "The practical work of candidacy begins this week. We read Federici on whose labor builds a field, then turn her question on ourselves with a recently advanced student and a workshop for your first committee email. Bring a draft, rough or not.",
        "lede": "Federici asks whose labor built the fields you inherit. The second half of the session turns her question toward your own degree: whose labor will it require, and on what terms do you ask for it?",
        "facts": [
            ("Read", "Federici, <cite>Caliban and the Witch</cite>, Introduction and Chapter 2 (about 71 pages)"),
            ("Bring", "A committee map and a draft email to your first committee contact"),
            ("Guest", "A recently advanced CRDM student"),
            ("Due", "No milestone this week"),
        ],
        "read": [
            "Silvia Federici, <cite>Caliban and the Witch: Women, the Body, and Primitive Accumulation</cite> (Autonomedia, 2004). Introduction, pages 7 to 20, and Chapter 2, “The Accumulation of Labor and the Degradation of Women,” pages 75 to 131. In the week’s Canvas Files folder.",
            "Read slowly. The argument is dense, and pages 91 to 109, on the enclosure of women’s bodies and reproductive labor, reward a second pass.",
        ],
        "bring": [
            "Your marked copy, with a note beside one passage in Federici bearing on your own field, connecting her argument to a dynamic you recognize.",
            "A committee map. Name each position (chair, readers, outside member), write two or three sentences on why each person, and note whom you have already spoken with.",
            "A draft of the email you will send your first committee contact. We workshop it in class.",
        ],
        "questions": [
            "Federici reads the witch hunts as a political campaign to discipline women’s bodies at the dawn of capitalism. What does her argument require you to revise about early modernity?",
            "Primitive accumulation usually refers to land and labor. Federici extends the concept to bodies and knowledge. Where does the extension appear in the fields you inherit?",
            "Whose labor built your field? Whose names appear in its canon, and whose do not?",
            "What has your field enclosed or suppressed? Which knowledges has it made to look like non-knowledge?",
            "How does Federici’s materialism sit with the discursive frameworks of Mbembe and Brown?",
            "Committee service is labor, much of it uncounted. What do you owe the faculty you ask to serve, and what do you expect from them in return?",
        ],
        "schedule": [
            ("10:15–10:30", "Opening question: what does primitive accumulation mean in Marx, and what does Federici do to the concept?"),
            ("10:30–11:15", "Discussion of Federici: the witch hunts as politics, the body as a site of accumulation, the labor behind a field."),
            ("11:15–11:30", "From Federici to the committee: whose labor will your degree require?"),
            ("11:30–11:45", "Break"),
            ("11:45–12:30", "Conversation with a recently advanced student on choosing a chair and readers, and on writing the first email."),
            ("12:30–1:00", "Committee email workshop."),
        ],
        "activities": [
            {"title": "Committee email workshop",
             "intro": "The workshop turns your committee map into a first message. A strong first ask runs about three sentences: what the project is, why this person, and what you are asking for.",
             "steps": [
                 "Trade draft emails with a partner.",
                 "Respond to your partner’s email in writing for ten minutes. Is the ask clear? Does the email convey the project’s stakes? Is it warm without being overfamiliar?",
                 "Discuss your responses, five minutes per email.",
                 "As a group, name the common problems: an ask too vague to answer, too much detail for a first contact, a request for commitment before interest.",
                 "Revise. Then name the person you will write to first and the day you will send the email.",
             ]},
        ],
        "after": [
            "Send at least one committee email within 48 hours of class.",
            "Keep any replies. They inform your exam list in Weeks 8 and 9.",
            "If you are unsure whom to ask, or how, email me before Week 8.",
        ],
        "further": [
            "Saidiya Hartman, “Venus in Two Acts,” on the archive, its silences, and humanistic imagination. It pairs with next week.",
            "María Lugones, “Heterosexualism and the Colonial/Modern Gender System,” a decolonial feminist extension of Federici.",
            "Karen Kelsky, <cite>The Professor Is In</cite>, the chapters on choosing advisors and committee dynamics. Library Reserve.",
        ],
     }},
    {"n": 7, "movement": 2, "title": "Hauntology: What Haunts Your Field?",
     "summary": "Coverley, Hauntology. Rapid presentations. First-pass exam list, tagged by field."},
    {"n": 8, "movement": 2, "title": "Exam List Workshop", "due": "Draft Exam List",
     "summary": "Structured peer review of draft lists."},
    {"n": 9, "movement": 2, "title": "Situated Knowledges: Revising the List", "guest": True,
     "summary": "Haraway, “Situated Knowledges.” A program faculty member joins us. Canon audit of the draft lists."},
    {"n": 10, "movement": 2, "title": "Individual Meetings", "due": "Committee Confirmation",
     "summary": "No group session. Individual meetings and prospectus seed writing."},
    {"n": 11, "movement": 3, "title": "One-Dimensional Thinking and the Dissertation Imagination",
     "summary": "Marcuse, One-Dimensional Man. Method, methodology, epistemology."},
    {"n": 12, "movement": 3, "title": "What Can Humanistic Imagination Actually Do?", "guest": True,
     "summary": "Ghosh, The Great Derangement. The “so what” gauntlet. A CRDM graduate joins us."},
    {"n": 13, "movement": 3, "title": "Paths Forward: Alt-Ac and Otherwise", "guest": True,
     "summary": "Graduates working beyond the academy join us. Three versions of one project."},
    {"n": 14, "movement": 3, "title": "Prospectus Workshop", "due": "Prospectus draft",
     "summary": "Small-group workshop on full drafts."},
    {"n": 15, "movement": 3, "title": "What We Made and What We’re Seeing",
     "summary": "Prospectus presentations. The Week 1 cards return."},
]


# Full week content lives in build/content/week_NN.py as CONTENT = {...}.
import importlib as _il
for _w in WEEKS:
    try:
        _mod = _il.import_module(f"content.week_{_w['n']:02d}")
    except ModuleNotFoundError:
        continue
    _w["content"] = _mod.CONTENT
    _w["built"] = True
