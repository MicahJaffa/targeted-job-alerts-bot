"""
score.py — Fit scoring for Two Bits Creative.

Six divisions (mapped by index, matching DIVISION_QUERIES order in job_search.py):
  0. Multimedia
  1. Graphic Design
  2. Account Management
  3. Social Media
  4. Client Acquisition & Sponsorships
  5. AI & Analytics

score(p, div_on) is called by job_search.py with:
  - p      : raw JSearch job dict
  - div_on : integer index of the division (0-5)

Returns a plain integer score (0-100).
Scores are only comparable within the same division.
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

# ==================================================================================
# DIVISION INDEX — must match DIVISION_QUERIES order in job_search.py
# ==================================================================================

DIVISION_INDEX = {
    1: "Multimedia",
    2: "Graphic Design",
    3: "Account Management",
    4: "Social Media",
    5: "Client Acquisition & Sponsorships",
    6: "AI & Analytics",
}

# ==================================================================================
# DIVISION DEFINITIONS
# Each division has its own:
#   title_pat  — strong signal, full base score
#   desc_pat   — medium signal, needs 2+ hits for half base
#   weak_pat   — weak signal, needs 1+ hit for quarter base
#   kw_bonus   — contextual bonus keywords (sports/athletic context)
#   kw_penalty — off-target penalty keywords
#   weights    — all point values for this division specifically
# ==================================================================================

DIVISIONS = {
    "Multimedia": {
        "title_pat": re.compile(
            r"videograph|video (production|editor|coordinator)|broadcast|highlight editor|"
            r"media coordinator|content creator|multimedia|cinematograph|live.?stream|"
            r"camera operator|production assistant|media production|video intern",
            re.I,
        ),
        "desc_pat": re.compile(
            r"premiere pro|after effects|final cut|davinci resolve|"
            r"video (editing|production|content|shoot)|broadcast|highlight reel|"
            r"live.?stream|multimedia|cinematograph|footage|b.?roll",
            re.I,
        ),
        "weak_pat": re.compile(
            r"video|film|camera|recording|editing|production|media|content|visual",
            re.I,
        ),
        "kw_bonus": re.compile(
            r"sports|athletic|athlete|ncaa|espn|nfl|nba|mlb|nhl|mls|"
            r"arena|stadium|varsity|collegiate|gameday",
            re.I,
        ),
        "kw_penalty": re.compile(
            r"software engineer|developer|accounti|legal|warehouse|recruiter",
            re.I,
        ),
        "weights": {
            "title_match":  62,
            "desc_match":   31,
            "weak_match":   15,
            "no_match":      4,
            "kw_bonus":      6,
            "kw_bonus_cap": 18,
            "kw_penalty":  -15,
            "geo": {1: 30, 2: 12, 3: 4, 4: -100},
            "gainesville":  20,
            "not_intern":  -55,
            "grad_only":   -45,
            "wrong_term":  -25,
            "clearance":    -8,
            "target":       10,
        },
    },

    "Graphic Design": {
        "title_pat": re.compile(
            r"graphic design|visual brand|creative services|motion graphics|"
            r"illustrat|art director|brand design|design intern|visual content|"
            r"digital design|creative design|graphic intern",
            re.I,
        ),
        "desc_pat": re.compile(
            r"adobe (illustrator|photoshop|indesign|creative suite|xd)|"
            r"figma|motion graphics|visual identity|brand(ing)?|"
            r"typography|color palette|logo|print design|vector",
            re.I,
        ),
        "weak_pat": re.compile(
            r"canva|design|visual|creative|branding|photoshop|artwork|layout",
            re.I,
        ),
        "kw_bonus": re.compile(
            r"sports|athletic|athlete|ncaa|espn|nfl|nba|mlb|nhl|mls|"
            r"arena|stadium|varsity|collegiate|gameday",
            re.I,
        ),
        "kw_penalty": re.compile(
            r"software engineer|developer|accounti|legal|warehouse|recruiter",
            re.I,
        ),
        "weights": {
            "title_match":  62,
            "desc_match":   31,
            "weak_match":   15,
            "no_match":      4,
            "kw_bonus":      6,
            "kw_bonus_cap": 18,
            "kw_penalty":  -15,
            "geo": {1: 30, 2: 12, 3: 4, 4: -100},
            "gainesville":  20,
            "not_intern":  -55,
            "grad_only":   -45,
            "wrong_term":  -25,
            "clearance":    -8,
            "target":       10,
        },
    },

    "Account Management": {
        "title_pat": re.compile(
            r"account (coordinator|manager|executive|director|associate)|"
            r"nil coordinator|talent manager|athlete relations|"
            r"client (success|services|coordinator|associate)|"
            r"agency coordinator|brand manager|relationship manager",
            re.I,
        ),
        "desc_pat": re.compile(
            r"client relationship|account management|nil|name,? image,? likeness|"
            r"talent management|athlete relations|client deliverable|"
            r"client.facing|account coordinator|manage (client|account)|"
            r"day.to.day (client|account)|agency",
            re.I,
        ),
        "weak_pat": re.compile(
            r"client|account|coordinator|liaison|relationship|brand|partner|talent",
            re.I,
        ),
        "kw_bonus": re.compile(
            r"sports|athletic|athlete|ncaa|nil|agency|brand partner|collegiate|varsity",
            re.I,
        ),
        "kw_penalty": re.compile(
            r"software engineer|developer|warehouse|recruiter|clinical|"
            r"cold call|door to door|commission only|insurance sales",
            re.I,
        ),
        "weights": {
            "title_match":  62,
            "desc_match":   31,
            "weak_match":   15,
            "no_match":      4,
            "kw_bonus":      6,
            "kw_bonus_cap": 18,
            "kw_penalty":  -18,
            "geo": {1: 30, 2: 12, 3: 4, 4: -100},
            "gainesville":  20,
            "not_intern":  -55,
            "grad_only":   -45,
            "wrong_term":  -25,
            "clearance":    -8,
            "target":       10,
        },
    },

    "Social Media": {
        "title_pat": re.compile(
            r"social media (coordinator|manager|assistant|specialist|intern|strategist)|"
            r"digital media (coordinator|assistant|intern)|"
            r"digital content (creator|coordinator)|community manager|"
            r"content (creator|strategist|coordinator)|social content",
            re.I,
        ),
        "desc_pat": re.compile(
            r"social media (strategy|management|content|platform|calendar|post)|"
            r"instagram|tiktok|twitter|x\.com|youtube|"
            r"content calendar|community management|digital content|"
            r"follower growth|engagement rate|hashtag|reel|short.form video",
            re.I,
        ),
        "weak_pat": re.compile(
            r"social|content|digital|post|platform|online|facebook|community|audience",
            re.I,
        ),
        "kw_bonus": re.compile(
            r"sports|athletic|athlete|ncaa|espn|nfl|nba|mlb|nhl|mls|"
            r"fan engagement|gameday|arena|stadium|collegiate|varsity",
            re.I,
        ),
        "kw_penalty": re.compile(
            r"software engineer|developer|warehouse|recruiter|clinical|legal",
            re.I,
        ),
        "weights": {
            "title_match":  62,
            "desc_match":   31,
            "weak_match":   15,
            "no_match":      4,
            "kw_bonus":      6,
            "kw_bonus_cap": 18,
            "kw_penalty":  -15,
            "geo": {1: 30, 2: 12, 3: 4, 4: -100},
            "gainesville":  20,
            "not_intern":  -55,
            "grad_only":   -45,
            "wrong_term":  -25,
            "clearance":    -8,
            "target":       10,
        },
    },

    "Client Acquisition & Sponsorships": {
        "title_pat": re.compile(
            r"sponsorship (coordinator|manager|activation|sales|associate)|"
            r"partnership (coordinator|manager|associate|development)|"
            r"corporate partner|brand deal|business development|"
            r"revenue (coordinator|development|associate)|"
            r"sales coordinator|partnership activation",
            re.I,
        ),
        "desc_pat": re.compile(
            r"sponsorship|partnership activation|brand deal|nil deal|"
            r"corporate partner|business development|revenue generation|"
            r"sponsor (relationship|outreach|proposal)|prospecting|"
            r"pitch deck|client acquisition|sell(ing)? sponsor",
            re.I,
        ),
        "weak_pat": re.compile(
            r"sponsor|partner|sales|revenue|acquisition|deal|activation|pitch",
            re.I,
        ),
        "kw_bonus": re.compile(
            r"sports|athletic|athlete|ncaa|nil|agency|team|league|"
            r"brand activation|naming rights|collegiate|varsity",
            re.I,
        ),
        "kw_penalty": re.compile(
            r"software engineer|developer|warehouse|recruiter|clinical|legal|"
            r"door to door|commission only|insurance|retail sales",
            re.I,
        ),
        "weights": {
            "title_match":  62,
            "desc_match":   31,
            "weak_match":   15,
            "no_match":      4,
            "kw_bonus":      6,
            "kw_bonus_cap": 18,
            "kw_penalty":  -18,
            "geo": {1: 30, 2: 12, 3: 4, 4: -100},
            "gainesville":  20,
            "not_intern":  -55,
            "grad_only":   -45,
            "wrong_term":  -25,
            "clearance":    -8,
            "target":       10,
        },
    },

    "AI & Analytics": {
        "title_pat": re.compile(
            r"data analy(st|tics)|business intelligence|\bbi analyst\b|"
            r"analytics (intern|coordinator|analyst)|performance analy(st|tics)|"
            r"sports analy(st|tics)|research analyst|data scientist|"
            r"ai analyst|operations analy(st|tics)|insights analyst",
            re.I,
        ),
        "desc_pat": re.compile(
            r"\bsql\b|tableau|power\s?bi|python|\br\b|"
            r"data (visualization|pipeline|model|warehouse|dashboard)|"
            r"business intelligence|kpi|reporting|"
            r"performance data|machine learning|predictive model",
            re.I,
        ),
        "weak_pat": re.compile(
            r"data|analytics|metrics|insights|reporting|excel|spreadsheet|"
            r"statistic|dashboard|analysis",
            re.I,
        ),
        "kw_bonus": re.compile(
            r"sports|athletic|athlete|ncaa|espn|nfl|nba|mlb|nhl|mls|"
            r"player tracking|fan analytics|ticketing|collegiate|varsity",
            re.I,
        ),
        "kw_penalty": re.compile(
            r"software engineer|developer|devops|embedded|firmware|"
            r"warehouse|recruiter|clinical|legal",
            re.I,
        ),
        "weights": {
            "title_match":  62,
            "desc_match":   31,
            "weak_match":   15,
            "no_match":      4,
            "kw_bonus":      6,
            "kw_bonus_cap": 18,
            "kw_penalty":  -15,
            "geo": {1: 30, 2: 12, 3: 4, 4: -100},
            "gainesville":  20,
            "not_intern":  -55,
            "grad_only":   -45,
            "wrong_term":  -25,
            "clearance":    -8,
            "target":       10,
        },
    },
}

# ==================================================================================
# SHARED PATTERNS
# ==================================================================================

NOT_INTERN = re.compile(
    r"\bintern(ship|s)?\b|\bco-?op\b|summer analyst|summer associate|"
    r"student|early career|campus|apprentice|rotational",
    re.I,
)
MBA_PHD = re.compile(
    r"\bmba\b|\bphd\b|ph\.d|doctoral|postdoc|\bjd\b|law student|nursing|pharmacy|\bmd\b",
    re.I,
)
CLEARANCE = re.compile(
    r"clearance|secret|ts/sci|\bsci\b|public trust|us citizen|u\.s\. citizen|"
    r"dod|department of defense",
    re.I,
)
YEAR         = re.compile(r"\b(20(2[5-9]))\b|'(2[5-9])\b")
OTHER_SEASON = re.compile(r"\b(spring|fall|autumn|winter)\b", re.I)
SUMMER       = re.compile(r"summer", re.I)
GAINESVILLE  = re.compile(r"gainesville", re.I)

FORCE_EXCLUDE = re.compile(
    r"software engineer|full[- ]?stack|back[- ]?end|front[- ]?end|devops|"
    r"embedded|firmware|\bswe\b|\bsde\b|actuar|pharmac|\bnurs\b|clinical|"
    r"\blegal\b|paralegal|human resources|\bhr\b|recruit|\btax\b|"
    r"underwrit|\bclaims\b|naval|architect|construction|real estate|"
    r"procurement|treasury|investment banking|\btrading\b|equity research|"
    r"warehouse|cashier|freight|loss prevention",
    re.I,
)

# ==================================================================================
# GEOGRAPHY
# ==================================================================================

TIER1_STATES = {"FL"}

TIER1_CITIES = re.compile(
    r"gainesville|tampa|orlando|miami|jacksonville|fort lauderdale|boca|"
    r"st\.? pete|tallahassee|palm beach|sarasota|clearwater|daytona|"
    r"pensacola|naples|cape coral|ocala|lakeland",
    re.I,
)
EAST_STATES = {
    "ME", "NH", "VT", "MA", "RI", "CT", "DE", "MD", "DC", "VA", "NC", "SC",
    "GA", "WV", "OH",
    # former tier-1 states now bumped to tier 2
    "NJ", "NY", "PA", "CA", "TX", "IL", "TN",
}
EAST_CITIES = re.compile(
    r"new york|nyc|manhattan|brooklyn|jersey|newark|princeton|hoboken|"
    r"philadelphia|pittsburgh|los angeles|atlanta|chicago|dallas|houston|"
    r"nashville|charlotte|boston|denver|phoenix|las vegas|seattle|austin|"
    r"san francisco|baltimore|washington|arlington|mclean|reston|richmond|"
    r"raleigh|durham|columbus|cleveland|cincinnati|wilmington|bethesda|"
    r"tysons|herndon|alexandria|norfolk|hartford|stamford|providence",
    re.I,
)
INTL = re.compile(
    r"canada|united kingdom|\buk\b|london|ireland|india|australia|germany|"
    r"france|europe|emea|apac|latam|singapore|mexico|brazil|japan|china|hong kong",
    re.I,
)
STATE_RE  = re.compile(r"\b([A-Z]{2})\b")
US_STATES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA",
    "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT",
    "VA","WA","WV","WI","WY","DC",
}


def _load_targets():
    path = os.path.join(ROOT, "boards.json")
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        return {b["company"].lower() for b in json.load(f)}

TARGET_COMPANIES = _load_targets()

TARGET_EMPLOYERS = {
    "teamworks", "athlete", "nil", "nfl", "nba", "mlb", "nhl", "mls", "pga",
    "nascar", "ufc", "espn", "fox sports", "nbc sports", "cbs sports",
    "turner sports", "bleacher report", "the athletic", "sports illustrated",
    "nike", "adidas", "under armour", "new balance", "puma", "gatorade",
    "powerade", "wilson", "callaway", "red bull", "fanatics", "ticketmaster",
    "live nation", "sportradar", "stats perform", "wme sports", "caa sports",
    "wasserman", "endeavor", "img", "octagon", "university of florida",
    "florida gators", "opendorse",
}


def geo_tier(locations, remote=False):
    loc    = locations or ""
    states = {s for s in STATE_RE.findall(loc) if s in US_STATES}
    if INTL.search(loc) and not states:
        return 4
    if states:
        if states & TIER1_STATES:
            return 1
        if states & EAST_STATES or remote or re.search(r"remote", loc, re.I):
            return 2
        return 3
    if TIER1_CITIES.search(loc):
        return 1
    if EAST_CITIES.search(loc) or remote or re.search(r"remote", loc, re.I):
        return 2
    if not loc.strip() or re.search(r"united states|\busa?\b|multiple|various|nationwide", loc, re.I):
        return 2
    return 3


def wrong_term(title):
    years = {int(a or ("20" + b)) for a, _, b in YEAR.findall(title)}
    if years and not (years & {2025, 2026, 2027, 2028, 2029}):
        return True
    return bool(OTHER_SEASON.search(title)) and not SUMMER.search(title)


# ==================================================================================
# CORE DIVISION SCORER
# ==================================================================================

def _score_within_division(title: str, desc: str, text: str, div: dict) -> tuple:
    """
    Score purely against this division's own criteria.
    Returns (raw_score, match_source).
    """
    w = div["weights"]

    # 1. Title match — strongest signal
    if div["title_pat"].search(title):
        return w["title_match"], "title"

    # 2. Description match — medium signal, needs 2+ hits
    if len(div["desc_pat"].findall(desc[:4000])) >= 2:
        return w["desc_match"], "desc"

    # 3. Weak match — 1 soft keyword anywhere in title+desc
    if div["weak_pat"].search(text):
        return w["weak_match"], "weak"

    # 4. No match
    return w["no_match"], "none"


# ==================================================================================
# PUBLIC API — called by job_search.py as score(job, div_on)
# ==================================================================================

def score(p: dict, div_on: int) -> int:
    """
    Parameters
    ----------
    p      : raw JSearch job dict
    div_on : integer index (0-5) matching DIVISION_QUERIES order in job_search.py
             0=Multimedia, 1=Graphic Design, 2=Account Management,
             3=Social Media, 4=Client Acquisition & Sponsorships, 5=AI & Analytics

    Returns
    -------
    int : score 0-100, comparable only within the same division
    """

    # --- resolve division name from index ---
    # div_on increments each division loop in job_search.py starting at 0
    # clamp to valid range in case it drifts
    division = DIVISION_INDEX.get(div_on % len(DIVISION_INDEX), "Multimedia")
    div      = DIVISIONS[division]
    w        = div["weights"]

    # --- extract JSearch fields ---
    title   = p.get("job_title", "")         or ""
    desc    = p.get("job_description", "")   or ""
    company = p.get("employer_name", "")     or ""
    remote  = bool(p.get("job_is_remote", False))

    loc_parts = [
        p.get("job_city", "")    or "",
        p.get("job_state", "")   or "",
        p.get("job_country", "") or "",
    ]
    locations = " ".join(x for x in loc_parts if x).strip()
    text      = f"{title} {desc}"

    # --- hard exclude ---
    if FORCE_EXCLUDE.search(title):
        return 0

    # --- division-local base score ---
    s, _ = _score_within_division(title, desc, text, div)

    # --- keyword bonus (sports/athletic context, capped per division) ---
    bonus_hits = len(div["kw_bonus"].findall(text))
    s += min(bonus_hits * w["kw_bonus"], w["kw_bonus_cap"])

    # --- keyword penalty ---
    if div["kw_penalty"].search(text):
        s += w["kw_penalty"]

    # --- geography ---
    geo = geo_tier(locations, remote)
    s  += w["geo"].get(geo, -100)

    # --- Gainesville bonus (stacks on top of geo) ---
    if GAINESVILLE.search(locations):
        s += w["gainesville"]

    # --- shared modifiers ---
    if not NOT_INTERN.search(title):
        s += w["not_intern"]

    if MBA_PHD.search(title):
        s += w["grad_only"]

    if CLEARANCE.search(text):
        s += w["clearance"]

    if wrong_term(title):
        s += w["wrong_term"]

    # --- target employer ---
    c_lower = company.lower()
    if c_lower in TARGET_COMPANIES or any(t in c_lower for t in TARGET_EMPLOYERS):
        s += w["target"]

    return max(0, min(100, s))