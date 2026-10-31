"""Headword lookup against padarchana.db (43 Telugu dictionaries, 94,702 entries, 110,801
spelling variants, 3,441 token redirects).

The dictionaries write చ/జ as ౘ/ౙ in native words (ౘదువు, ౙముఁడు) and keep the arasunna
(కనఁబడు), so every lookup normalises both sides: ౘ→చ, ౙ→జ, ఁ removed, ఱ→ర.

    lex = Lexicon()
    lex.status("కందువ")      -> "headword"
    lex.status("కనబడు")      -> "variant"       (listed as కనఁబడు)
    lex.status("నలుగడలు")    -> "inflected"     (నలుగడ + plural)
    lex.status("కావుళము")    -> None

`status` tries the surface form, then the dictionary's own redirects, then a small set of
Telugu inflections stripped from the end (plural -లు, oblique -ల, case endings, -ంబు/-ము,
-ఁడు/-డు/-ండు, drutam) so that an inflected part such as సంపదలు or రాజునకు resolves to its
headword. It never splits a word into two words: that is the model's job.
"""
import re
import json
import os
import sqlite3
import threading
from functools import lru_cache
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "padarchana.db"
_TRANS = str.maketrans({"ౘ": "చ", "ౙ": "జ", "ఁ": "", "ఱ": "ర"})
_SIGNS = set("ాిీుూృెేైొోౌ")
_VERB_ENDINGS = {"ుతున్నాను", "ుతున్నావు", "ుతున్నాడు", "ుతున్నది", "ుతున్నారు", "ుచున్", "ుచు", "ుచును", "ించి",
                 "ించె", "ించెను", "ించిన", "ిల్లి", "ిల్లె", "ిల్లుచు", "ెను", "ెద", "ెదన్", "ిన", "ిరి", "ెడు", "ెడి",
                 "ుట", "ుటకు", "ుటన్", "ంగ", "ంగా", "ంగన్", "ఁగ", "గ", "గా", "గన్", "క", "కన్", "ుము", "ుమా", "ండి",
                 "ుదురు", "ుదును", "ుతురు", "ుతును", "ుతాను", "ుతారు", "ాను", "ావు", "ాడు", "ారు", "ాము", "ింది",
                 "ితి", "ితిని", "ితే", "ాలి", "లేదు", "కుండ", "కుండా", "ె", "ి"}

# (ending, replacements) tried in order; "" means drop the ending
_INFLECTIONS = [
    ("లను", ["లు", "ము", ""]), ("లకు", ["లు", "ము", ""]), ("లకున్", ["లు", "ము"]), ("లలో", ["లు", "ము"]),
    ("లన్", ["లు", "ము", ""]), ("ల", ["లు", "ము", ""]), ("లు", ["ము", "", "ఉ"]), ("ల్", ["", "లు", "ము"]),
    ("ముల్", ["ము", "ం"]), ("ముల", ["ము", "ం"]), ("ములు", ["ము", "ం"]), ("ముల్", ["ము"]),
    ("ంబులు", ["ము"]), ("ంబుల", ["ము"]), ("ంబున", ["ము"]), ("ంబు", ["ము"]), ("ంబున్", ["ము"]), ("ంబుల్", ["ము"]),
    ("మ్ము", ["ము"]), ("మ్మును", ["ము"]), ("మ్మున", ["ము"]), ("మ్మునకు", ["ము"]),
    ("మున", ["ము"]), ("మును", ["ము"]), ("మునకు", ["ము"]), ("మునకున్", ["ము"]), ("మునన్", ["ము"]), ("మున్", ["ము"]),
    ("ములు", ["ము"]), ("ముల", ["ము"]), ("ముతో", ["ము"]), ("ంబుతో", ["ము"]),
    ("ని", ["డు", "ము", ""]), ("నిన్", ["డు", ""]), ("నికి", ["డు", ""]), ("నకు", ["డు", "ము", ""]), ("నకున్", ["", "డు", "ము"]),
    ("నందు", ["ము", ""]), ("యందు", [""]), ("లోన", [""]), ("లోనన్", [""]), ("చే", [""]), ("చేత", [""]), ("వలన", [""]),
    ("ులు", ["ుడు", "ు"]), ("ుల", ["ుడు", "ు"]), ("ులన్", ["ుడు", "ు"]), ("ులకు", ["ుడు", "ు"]), ("ులను", ["ుడు", "ు"]),
    ("ుండు", ["ుడు"]), ("ుండ", ["ుడు"]), ("ుండును", ["ుడు"]), ("ుడును", ["ుడు"]), ("ుఁడు", ["ుడు"]),
    ("ుతున్నాను", ["ు"]), ("ుతున్నావు", ["ు"]), ("ుతున్నాడు", ["ు"]), ("ుతున్నది", ["ు"]), ("ుతున్నారు", ["ు"]),
    ("ుచున్", ["ు"]), ("ుచు", ["ు"]), ("ుచును", ["ు"]), ("ించి", ["ించు"]), ("ించె", ["ించు"]), ("ించెను", ["ించు"]),
    ("ించిన", ["ించు"]), ("ిల్లి", ["ిల్లు"]), ("ిల్లె", ["ిల్లు"]), ("ిల్లుచు", ["ిల్లు"]), ("ెను", ["ు"]), ("ెద", ["ు"]), ("ెదన్", ["ు"]),
    ("ిన", ["ు"]), ("ిరి", ["ు"]), ("ెడు", ["ు"]), ("ెడి", ["ు"]), ("ుట", ["ు"]), ("ుటకు", ["ు"]), ("ుటన్", ["ు"]),
    ("ంగ", ["ు"]), ("ంగా", ["ు"]), ("ంగన్", ["ు"]), ("ఁగ", ["ు"]), ("గ", ["ు"]), ("గా", ["ు"]), ("గన్", ["ు"]),
    ("క", ["ు"]), ("కన్", ["ు"]), ("ుము", ["ు"]), ("ుమా", ["ు"]), ("ుడు", ["ు"]), ("ుఁడు", ["ు"]), ("ండి", ["ు"]),
    ("ుదురు", ["ు"]), ("ుదును", ["ు"]), ("ుతురు", ["ు"]), ("ుతును", ["ు"]), ("ుతాను", ["ు"]), ("ుతారు", ["ు"]),
    ("ాను", ["ు"]), ("ావు", ["ు"]), ("ాడు", ["ు"]), ("ారు", ["ు"]), ("ాము", ["ు"]), ("ింది", ["ు"]), ("ితి", ["ు"]), ("ితిని", ["ు"]),
    ("ితే", ["ు"]), ("ాలి", ["ు"]), ("వలె", [""]), ("వలెను", [""]), ("లేదు", ["ు"]), ("కుండ", ["ు"]), ("కుండా", ["ు"]),
    ("ండు", ["డు"]), ("ండ", ["డు"]), ("డు", ["డు"]), ("ండి", ["డు"]),
    ("కు", [""]), ("కున్", [""]), ("కిన్", [""]), ("కి", [""]), ("ను", [""]), ("న్", ["", "ము"]), ("న", ["", "ము"]),
    ("లో", [""]), ("తో", [""]), ("యు", [""]), ("ను", ["ము"]),
    ("ా", ["", "ు"]), ("ీ", ["ి"]), ("ీ", ["ు"]), ("ిని", ["ి"]), ("ున్", ["ు"]), ("ుని", ["ుడు"]),
    ("ు", ["ము"]), ("ి", ["ు"]), ("ె", ["ు"]), ("ై", ["ు"]),
]


def normalize(s):
    return s.translate(_TRANS)


def _reorder(infl):
    """The -ులు family (nouns in -ి, -ు, -ుడు) must be tried before the generic -లు, which would
    strip to a bare stem that happens to exist (గుడులు → గుడ); and it needs the -ి completion."""
    ul = [(e, r + (["ి"] if "ి" not in r else [])) for e, r in infl if e.startswith("ుల")]
    rest = [(e, r) for e, r in infl if not e.startswith("ుల")]
    return ul + rest


_INFLECTIONS = _reorder(_INFLECTIONS)
_VERB_ALTERNATION_ENDINGS = ("ిన", "ిరి", "ితి", "ితిని", "ితివి", "ితిమి", "ితిరి", "ిచి", "ి",
                             "ాను", "ావు", "ాడు", "ారు", "ాము", "ింది", "ాయి", "ియె", "ియెను", "ియున్")  # విఱిగిన, కలిగి, చదివాను: stem ఇ ↔ root ఉ
_PARTICLES = [("యు", "sign"), ("తో", "any"), ("ను", "sign"), ("ని", "cons:అని"), ("ే", "elide:ఏ"), ("ై", "elide:ఐ"), ("ో", "elide:ఓ")]

_DEVOICE = {"గ": "క", "జ": "చ", "డ": "ట", "ద": "త", "బ": "ప", "వ": "ప"}
_SIGN_TO_VOWEL = {"ా": "ఆ", "ి": "ఇ", "ీ": "ఈ", "ు": "ఉ", "ూ": "ఊ", "ె": "ఎ", "ే": "ఏ", "ై": "ఐ", "ొ": "ఒ", "ో": "ఓ", "ౌ": "ఔ"}


def initial_variants(w):
    """Spellings the word may have had before sandhi with the preceding word."""
    out = []
    if w and w[0] in _DEVOICE:
        out.append(_DEVOICE[w[0]] + w[1:])
    if w.startswith("య"):
        if len(w) > 1 and w[1] in _SIGN_TO_VOWEL:
            out.append(_SIGN_TO_VOWEL[w[1]] + w[2:])
        elif len(w) > 1 and w[1] != "్":
            out.append("అ" + w[1:])
    if w.startswith("న") and len(w) > 2 and w[1] in _SIGN_TO_VOWEL:  # ద్రుతం of the previous word: నొప్పున్ = న్ + ఒప్పున్
        out.append(_SIGN_TO_VOWEL[w[1]] + w[2:])
    return out


def _lexeme(h):
    """Compare headwords at lexeme level: a final -ము / -ు / -ుడు spelling difference is not a different word."""
    h = normalize(h or "")
    for e in ("ుడు", "ము", "ం", "ు"):
        if h.endswith(e) and len(h) > len(e) + 1:
            return h[: -len(e)]
    return h


def aksharas(s):
    """Number of syllables: letters that are not vowel signs, virama or anusvara."""
    return sum(1 for c in s if c not in _SIGNS and c not in "ంః")


_LEXICAL_LU = {"కోడలు", "నిచ్చలు", "చెల్లెలు", "దిగులు", "పగలు", "తిప్పలు", "మరులు", "వెడలు", "కడలు", "నడలు", "మొదలు", "ఇల్లు", "కల్లు"}
_PLURAL_CASES = ("లను", "లకు", "లలో", "లతో", "లన్", "లకున్", "లచే", "లపై")
_PRONOUN_STEMS = {"మన", "మీ", "వీర", "వార", "తమ", "నా", "నీ", "మా", "వీరి", "వారి"}
_TRIKA = {"అ": "ఆ", "ఇ": "ఈ", "ఎ": "ఏ"}  # త్రిక సంధి: the demonstrative whose vowel shortened before the doubled consonant
_FINAL_UNASSIMILATED = {"ద": "త", "జ": "త", "చ": "త", "డ": "ట", "గ": "క", "బ": "ప"}  # సద్ = సత్, షడ్ = షట్, దిగ్ = దిక్
_VISARGA_PREFIXES = {"దుః": "దుర్", "దుస్": "దుర్", "దుష్": "దుర్", "నిః": "నిర్", "నిస్": "నిర్", "నిష్": "నిర్", "అంతః": "అంతర్",
                     "పునః": "పునర్", "ప్రాతః": "ప్రాతర్", "బహిః": "బహిర్", "ఆవిః": "ఆవిర్"}
_PRONOMINAL_STEMS = {"తత్", "మత్", "భవత్", "అస్మత్", "యుష్మత్", "తద్", "మద్", "అస్మద్", "యుష్మద్", "ఏతత్", "యత్", "త్వత్"}
_VARIANT_RULES = (("చ్చి", "చ్యు"), ("చ్చు", "చ్యు"), ("ంత", "ింత"), ("ద్దర", "ద్ర"))


class Lexicon:
    def __init__(self, db=DB, annamayya=False, padyarchana=False):
        # one connection shared by all threads (the annotation server answers requests in threads),
        # serialised by a lock for the queries made after loading
        self.con = sqlite3.connect(f"file:{db}?mode=ro", uri=True, check_same_thread=False, timeout=120)  # wait out another process's write
        self.con.execute("PRAGMA query_only=1")
        self._db_lock = threading.Lock()
        # sandhi preference (LEXICON_SANDHI_PREFERENCE=1): a voiced-initial or న-initial token that is itself
        # an entry (బట్టి, గని, గాక, జేయు, నను) is read as the devoiced / drutam-less word when that reading is a
        # verb root and the entry is not, or when its corpus frequency is far higher (గని → కను, జేయు → చేయు),
        # never when the entry is the frequent one (నీవు, నీకు, గద). Frequencies: results/resolution/headword_freq.json
        import os
        self.sandhi_preference = os.environ.get("LEXICON_SANDHI_PREFERENCE", "0") == "1"
        self.headword_freq = {}
        fq = Path(db).parent / "bilstm" / "results" / "resolution" / "headword_freq.json"
        if fq.exists():  # corpus token counts per headword (v22 output); the sandhi preference, trika and yadagama guards use it
            self.headword_freq = json.load(open(fq, encoding="utf-8"))
        # the అన్నమయ్య పదనిఘంటువు (onboard_annamayya.py): usage forms with modern glosses, used as attestation
        # and gloss evidence, never as headwords; opt-in so that a running pipeline keeps its behaviour
        self.annamayya = {}
        if annamayya:
            try:
                for form_norm, gloss in self.con.execute("select form_norm, gloss from annamayya_forms where is_phrase = 0"):
                    self.annamayya.setdefault(form_norm, []).append(gloss)
            except sqlite3.OperationalError:
                pass
        # the Padyarchana prathipadartham (onboard_padyarchana.py, dictionary 50): the poems' editorial word glosses,
        # same two uses, same opt-in; they share the glossary dict (self.annamayya) that attested() and gloss_of() read
        if padyarchana:
            try:
                for form_norm, gloss in self.con.execute(
                        "select form_norm, gloss from padyarchana_forms where layer = 'editorial' and is_phrase = 0"):
                    self.annamayya.setdefault(form_norm, []).append(gloss)
            except sqlite3.OperationalError:
                pass
        self.glossary = self.annamayya
        rows = self.con.execute("select word from entries").fetchall()
        self.headwords = {normalize(w) for (w,) in rows}
        # dictionaries kept out of the lexicon unless asked for (LEXICON_EXCLUDE_DICTS, default 47,48,49): DSAL Brown and
        # Telugu Wiktionary added 22,534 headwords (v21) that raised coverage 0.904 → 0.922 but lowered the precision on
        # the fair judged words 0.574 → 0.543: they resolved fragments and syncopated spellings in the dictionary pass
        # (డైన → టైము, నపుడు, గల్గు → కల్గు over కలుగు) that the later stages had resolved correctly. పదబంధ పారిజాతము
        # (49, onboard_parijatamu.py, 2026-10-25: 14,861 new entries, 4,320 of them single words) is excluded until it is
        # evaluated the same way; set LEXICON_EXCLUDE_DICTS="47,48" to let it in. 50 (పద్యార్చన ప్రతిపదార్థము, onboard_padyarchana.py)
        # likewise: its curated new headwords stay out until measured
        excl = [int(x) for x in os.environ.get("LEXICON_EXCLUDE_DICTS", "47,48,49,50").split(",") if x.strip()]
        self._excluded = self._introduced_by(excl) if excl else set()
        self.headwords -= self._excluded
        # headwords only the added dictionaries list (46 judge-backfilled, 47 DSAL Brown, 48 Wiktionary, 49 పదబంధ పారిజాతము,
        # 50 పద్యార్చన ప్రతిపదార్థము): they resolve a
        # word only when the established dictionaries cannot (resolve() retries with them hidden), so an addition never
        # captures a word the established lexicon reads (v20: సల్పుచు → సల్పు over సలుపు, బిగియించి → బిగియించు)
        try:
            self.added_only = self._introduced_by((46, 47, 48, 49, 50))  # (the verb roots read from the మణిదీపిక table are established, not added)
        except Exception:
            self.added_only = set()
        self._hide_added = False
        rows = self.con.execute("select variant from variants").fetchall()
        self.variants = {normalize(w) for (w,) in rows} - self.headwords
        rows = self.con.execute("select token, base_token from token_redirects").fetchall()
        self.redirects = {normalize(t): normalize(b) for t, b in rows}
        # the other token kinds: synonyms (words from the thesaurus lists) and fulltext (any word
        # occurring in a meaning or citation: an attested form, not a headword). After rebuild_search_index.py the
        # table token_dicts says which dictionaries' texts carry each fulltext token; a token found only in the texts
        # of the excluded dictionaries does not count as attested, so the index can cover them without changing the lexicon
        self.synonyms, self.fulltext = set(), set()
        only_excluded = set()
        if excl and self.con.execute("select count(*) from sqlite_master where name = 'token_dicts'").fetchone()[0]:
            q = ",".join("?" * len(excl))
            only_excluded = {t for (t,) in self.con.execute(
                f"select t.token from tokens t where (t.kinds & 8) and not exists "
                f"(select 1 from token_dicts td where td.token_id = t.token_id and td.dict_id not in ({q}))", excl)}
        for t, k in self.con.execute("select token, kinds from tokens"):
            n = normalize(t)
            if k & 4 and n not in self.headwords:
                self.synonyms.add(n)
            if k & 8 and t not in only_excluded:
                self.fulltext.add(n)
        # verb roots of క్రియాస్వరూప మణిదీపిక (data/kriya_swarupa/verb_roots.tsv), if prepared
        self.verb_roots = set()
        vr = Path(db).parent / "data" / "kriya_swarupa" / "verb_roots.tsv"
        if vr.exists():
            import csv
            with open(vr, encoding="utf-8") as f:
                self.verb_roots = {normalize(r["root"]) for r in csv.DictReader(f, delimiter="\t")}
            self.headwords |= self.verb_roots

    def _introduced_by(self, dict_ids):
        """Normalised words of the entries that only the given (added) dictionaries introduced: every definition is
        theirs and no original source (sources rows of the main/tn/vijaya imports) lists the entry. A spelling that an
        established entry shares after normalisation (dictionary 49 తఱుచంటి beside తరుచంటి) is not introduced: an
        added dictionary attached to an existing entry, or spelled like one, must not hide the established headword."""
        q = ",".join("?" * len(dict_ids))
        words = [w for (w,) in self.con.execute(
            f"select e.word from entries e where exists (select 1 from definitions d where d.entry_id = e.id and d.dict_id in ({q})) "
            f"and not exists (select 1 from definitions d where d.entry_id = e.id and d.dict_id not in ({q})) "
            f"and not exists (select 1 from sources s join dictionaries dd on dd.source_type = s.source_type "
            f"where s.entry_id = e.id and dd.dict_id not in ({q}))", tuple(dict_ids) * 3)]
        raw = set(words)
        others = {normalize(w) for (w,) in self.con.execute("select word from entries") if w not in raw}
        return {normalize(w) for w in words} - others

    # the paradigm index; LEXICON_FORMS_DB points a run at another build (v24: an index that includes dictionaries 49-50)
    FORMS_DB = Path(os.environ.get("LEXICON_FORMS_DB") or (Path(__file__).parent / "results" / "resolution" / "paradigm_forms.db"))

    def _q(self, con, sql, params=()):
        """A query on a shared connection, one thread at a time."""
        with self._db_lock:
            return con.execute(sql, params).fetchall()

    def generated(self, word):
        g = self._generated(word)
        if g and self._excluded:
            g = tuple(h for h in g if h not in self._excluded)
        if self._hide_added and g:
            return tuple(h for h in g if h not in self.added_only)
        return g

    @lru_cache(maxsize=500000)
    def _generated(self, word):
        """Headwords whose paradigm (paradigm_generator.py) produces this form, as a tuple; empty
        if the index is absent or the form is not generated."""
        if not hasattr(self, "_forms_con"):
            self._forms_con = sqlite3.connect(f"file:{self.FORMS_DB}?mode=ro", uri=True, check_same_thread=False) if self.FORMS_DB.exists() else None
        if self._forms_con is None:
            return ()
        rows = self._q(self._forms_con, "select headword from forms where form = ?", (normalize(word),))
        return tuple(sorted({r[0] for r in rows}))

    def _direct(self, w, min_aksharas=2):
        """Exact dictionary match. Bases reached by stripping or completing an ending must have
        two syllables (వి, దు, కా, ము are never evidence for a split); a whole word may be one."""
        if aksharas(w) < min_aksharas:
            return None
        if w in self.headwords and not (self._hide_added and w in self.added_only):
            return "headword"
        if w in self.variants:
            return "variant"
        if w in self.redirects:
            return "redirect"
        if w in self.synonyms:
            return "synonym"
        return None

    def attested(self, word):
        """True if the word occurs anywhere in the dictionaries' text (meanings, citations) or as a
        form in the Annamayya glossary or the Padyarchana prathipadartham when loaded: weaker evidence
        than a headword, but evidence that the form exists."""
        n = normalize(word)
        return n in self.fulltext or n in self.annamayya

    def gloss_of(self, word):
        """The glossaries' glosses for a form (empty unless Lexicon(annamayya=True) and/or Lexicon(padyarchana=True))."""
        return self.annamayya.get(normalize(word), [])

    def _base(self, w):
        """The headword w stands for: itself, its ు-less root, its -ము/-ం spelling, or its
        samāsa-stem completion."""
        if self._direct(w):
            return self.redirects.get(w, w)
        if w.endswith("ం") and self._direct(w[:-1] + "ము"):  # కార్యం = కార్యము
            return w[:-1] + "ము"
        if w.endswith("ము") and self._direct(w[:-2] + "ం"):
            return w[:-2] + "ం"
        if w.endswith("ు") and len(w) > 2 and self._direct(w[:-1]):
            return self.redirects.get(w[:-1], w[:-1])
        if w and w[-1] not in _SIGNS and w[-1] != "్":
            for r in ("ము", "ుడు", "ు", "ి", "ం", "ా"):
                if self._direct(w + r):
                    return w + r
        return None

    @lru_cache(maxsize=2000000)
    def resolve(self, word):
        r = self._resolve_full(word)
        if self.added_only and r[1] and normalize(r[1]) in self.added_only and not self._hide_added:
            self._hide_added = True
            try:
                r2 = self._resolve_full(word)
            finally:
                self._hide_added = False
            if r2[0] is not None:
                return r2
        return r

    def _resolve_full(self, word):
        """Also undoes a sandhi change at the START of the word caused by the previous word:
        గసడదవాదేశ voicing (జూచి -> చూచి, గాక -> కాక) and యడాగమ (యని -> అని, యీ -> ఈ)."""
        r = self._resolve(word)
        w = normalize(word)
        if self.sandhi_preference and r[0] in ("headword", "variant", "synonym", "redirect") and w and (w[0] in _DEVOICE or w[0] == "న"):
            alt = self._sandhi_alternative(w, r)
            if alt:
                return alt
        if r[0] in ("headword", "variant", "synonym", "redirect", "inflected", None):
            # v18: an a-stem plural case form (పాటలను → పాట, సురలకు → సుర, తొడలపై → తొడ), whatever the stripper read
            # (పాటల, పెద్దలు); not the pronouns (మనలను stays మనము), not -ు stems (రాజులకు: రాజు/రాజి is the
            # paradigm's call), not a verb in -లు (వెడలన్ is వెడలు): +2 / -0 on the 2026-10-13 gold pairs
            for cs in _PLURAL_CASES:
                if w.endswith(cs) and aksharas(w[: -len(cs)]) >= 2:
                    st = w[: -len(cs)]
                    if (self._direct(st) and normalize(r[1] or "") != st and st not in _PRONOUN_STEMS and not st.endswith(("ు", "్"))
                            and st not in ("మర",) and self.is_verb(st + "లు") is not True):  # మరలన్ is the adverb మరల
                        return ("inflected", self.redirects.get(st, st), "plural-case")
                    break
        if r[0] in ("headword", "variant", "synonym", "redirect"):
            # v17 (2026-10-13 gold): a plural the dictionaries list as an entry of its own, usually for a special sense
            # (పూజలు, నెలలు), resolves to its singular when the singular is an a-final headword (మాటలు → మాట,
            # పిల్లలు → పిల్ల): +9 / -0 on the gold pairs; words whose -లు is part of the word are kept
            if w.endswith("లు") and len(w) > 3 and w not in _LEXICAL_LU and self.is_verb(w) is not True:
                st = w[:-2]
                if st and (st[-1] not in _SIGN_TO_VOWEL or st[-1] == "ా") and st[-1] != "్" and aksharas(st) >= 2 and self._direct(st):
                    return ("inflected", self.redirects.get(st, st), "plural-entry")
        if r[0] in ("headword", "variant", "synonym", "redirect") and self.FORMS_DB.exists():
            # a verb form the dictionaries list as an entry of its own (ఉన్నది, ఉన్న, పాసి, పడె, కా) resolves
            # to the verb whose paradigm produces it: +66 / -2 on the 2,217 gold pairs of 2026-10-12
            verbs = [h for h in self.generated(w) if _lexeme(h) != _lexeme(r[1]) and self.is_verb(h) is True]
            if len(verbs) == 1 and self.is_verb(normalize(r[1])) is not True and r[2] not in ("o-stem", "visarga", "final-consonant"):
                return ("inflected", verbs[0], "generated-verb-over-entry")
        if r[0] in ("inflected", "stem") and w.startswith("న") and len(w) > 2 and w[1] in _SIGN_TO_VOWEL:
            # weak reading of a న-initial word: the drutam reading wins if it is a headword or a verb root
            # with a verb ending (నొప్పక → ఒప్పు, not నొప్ప; నడచి → నడచు stays, as both are verb roots)
            r2 = self._resolve(_SIGN_TO_VOWEL[w[1]] + w[2:])
            if r2[0] is not None and (r2[0] == "headword" or (normalize(r2[1]) in self.verb_roots and normalize(r[1]) not in self.verb_roots)):
                return (r2[0], r2[1], "initial-sandhi")
        if (r[0] == "inflected" and w.startswith("య") and len(w) >= 2 and (w[1] in "ెేొో" or (w[1] not in _SIGN_TO_VOWEL and w[1] != "్"))
                and not any(_lexeme(h) == _lexeme(r[1]) for h in (self.generated(w) if self.FORMS_DB.exists() else []))):
            # weak reading of a య-initial word (the stripper alone, the paradigm silent): the యడాగమ reading (యతని = అతని,
            # యెత్తి = ఎత్తి, యే = ఏ, యవి = అవి) wins when it is a listed word or a form the paradigm confirms; native words
            # rarely begin with యె/యొ, so యా/యు/యూ/యి (యూధము, యుక్తి) are left alone. Sandhi-engine evaluation, 2026-10-25
            alt = (_SIGN_TO_VOWEL[w[1]] + w[2:]) if w[1] in _SIGN_TO_VOWEL else ("అ" + w[1:])
            r2 = self._resolve(alt)
            if r2[0] is not None and r2[1]:
                # the inherent-అ case (యతని = అతని, యవి = అవి; but యము is యముడు and యక్షుం is యక్షుడు) only when the yadagama
                # headword is a documented word and more frequent in the corpus than the stripper's (అతడు 6.3k vs యతి 3.3k,
                # the latter inflated by these very misreadings); యె/యొ/యే/యో need no guard
                fa, fs = self.headword_freq.get(normalize(r2[1]), 0), self.headword_freq.get(normalize(r[1]), 0)
                guard_ok = w[1] in "ెేొో" or (fa > 0 and fa >= 1.5 * fs and bool(self.pos(r2[1])))
                if guard_ok and r2[0] in ("headword", "variant", "synonym", "redirect"):
                    return (r2[0], r2[1], "initial-sandhi")
                if guard_ok and r2[0] in ("inflected", "stem") and self.FORMS_DB.exists() and any(_lexeme(h) == _lexeme(r2[1]) for h in self.generated(alt)):
                    return ("inflected", r2[1], "initial-sandhi+generated")
        if r[0] is not None:
            if r[0] in ("inflected", "stem") and self.FORMS_DB.exists():
                g = self.generated(w)
                if g:
                    lex_r = _lexeme(r[1])
                    if any(_lexeme(h) == lex_r for h in g):
                        return (r[0], r[1], r[2] + "+generated")  # stripper and paradigm agree
                    if len(g) == 1:
                        return ("inflected", g[0], "generated-over-stripper")  # the paradigm reaches a listed form, the stripper guessed
            return r
        for alt in initial_variants(w):
            r = self._resolve(alt)
            if r[0] is not None:
                return (r[0], r[1], "initial-sandhi")
        # the drutam (న్) or its -ను spelling after a form that resolves on its own (అనువునన్, ఇచ్చెన్, చంపెదను):
        # +54 / +6 on the gold pairs of 2026-10-12; the rest must be an inflected or listed form of at least three aksharas
        for suf, min_ak in (("న్", 3), ("ను", 3), ("ం", 2)):  # ం: the drutam written as a full anusvara (నీకుం = నీకున్)
            if w.endswith(suf) and aksharas(w[: -len(suf)]) >= min_ak:
                r = self._resolve_full(w[: -len(suf)]) if self._hide_added else self.resolve(w[: -len(suf)])
                if r[0] in ("headword", "variant", "redirect", "synonym", "inflected"):
                    return ("inflected", r[1], (r[2] or "") + "+drutam")
        if self.FORMS_DB.exists():
            for form in [w] + initial_variants(w):
                g = self.generated(form)
                if len(g) == 1:
                    return ("inflected", g[0], "generated")
                if len(g) > 1:
                    best = max(g, key=lambda h: (self.pos(h) is not None, -len(h)))  # prefer a documented, shorter headword
                    return ("inflected", best, "generated-ambiguous")
        # last resort: the few spelling variants that were right every time on the 2026-10-12 gold (అచ్చితుడు → అచ్యుతుడు,
        # అక్షంతలు → అక్షింతలు, నిద్దరించు → నిద్రించు); vowel-length and ళ/ల, ఱ/ర swaps were wrong as often as right and are left out
        # a Sanskrit stem's final consonant as assimilated to the next word (సద్గుణ, షడ్భుజ, దిగ్గజ: సద్ = సత్, షడ్ = షట్,
        # దిగ్ = దిక్) is the stem the dictionaries list; the drutam న్ and the plural ల్ are left alone (every gold loss of
        # the broader rule was one of those). Sandhi-engine evaluation, 2026-10-25
        if len(w) >= 3 and w.endswith("్") and w[-2] in _FINAL_UNASSIMILATED and aksharas(w) >= 2:
            q = w[:-2] + _FINAL_UNASSIMILATED[w[-2]] + "్"
            if self._direct(q):
                return ("variant", self.redirects.get(q, q), "final-consonant")
        # last resorts read off the poems' word-by-word splits (2026-10-14):
        # a syncopated verb (పల్కు, కల్గు, నిల్పి, మాన్పి: a ు dropped inside a cluster) is its full verb (పలుకు, కలుగు,
        # నిలుపు, మానుపు): 11k tokens, 2 right / 1 debatable on the gold; geminates (మెల్ల, మ్మని) and short lemmas excluded
        if not getattr(self, "_in_variant", False):
            for i in range(1, len(w) - 1):
                if (w[i] == "్" and w[i - 1] not in "ంః" and w[i + 1] not in _SIGN_TO_VOWEL and w[i + 1] not in "ృ్"
                        and w[i + 1] != w[i - 1] and w[i - 1] + w[i + 1] not in ("ళల", "లళ")):
                    v = w[:i] + "ు" + w[i + 1:]
                    self._in_variant = True
                    try:
                        for f in [v] + initial_variants(v):
                            r = self.resolve.__wrapped__(self, f)
                            h = normalize(r[1] or "")
                            if r[0] in ("headword", "variant", "redirect", "synonym", "inflected") and h.endswith("ు") and aksharas(h) >= 3 and self.is_verb(h) is True:
                                return ("inflected", r[1], (r[2] or "") + "+syncope")
                    finally:
                        self._in_variant = False
            # a Sanskrit consonant stem (జగత్, తపస్, మనః) is its Telugu noun (జగత్తు, తపస్సు, మనస్సు); not the pronominal stems
            cands = []
            if w.endswith("్") and len(w) >= 3 and w[-2] in "తదసకషశ" and w not in _PRONOMINAL_STEMS:
                cands.append(w + w[-2] + "ు")
            if w.endswith("ః") and len(w) >= 3:
                cands.append(w[:-1] + "స్సు")
            for c in cands:
                if self._direct(c):
                    return ("variant", self.redirects.get(c, c), "consonant-stem")
        # త్రిక సంధి (ఆ ఈ ఏ + a word: the vowel shortens, the word's first consonant doubles): ఇవ్విధంబున = ఈ + విధంబున,
        # అత్తెఱంగున = ఆ + తెఱంగున, అయ్యవసరంబున = ఆ + (య)అవసరంబున. Only for a word nothing else reads, and only when the
        # remainder's headword has three or more aksharas (ఎవ్వరికి, అప్పటి, అచ్చెరువు are words of their own): 1.8k
        # tokens. The sandhi engine's R11, adapted 2026-10-25; resolve_corpus.py writes it as a split
        if (not getattr(self, "_in_variant", False) and len(w) >= 5 and w[0] in _TRIKA and w[2] == "్" and w[1] == w[3]
                and "\u0c15" <= w[1] <= "\u0c39" and aksharas(w) >= 3):
            rest = w[3:]
            self._in_variant = True
            try:
                r = self.resolve.__wrapped__(self, rest)
            finally:
                self._in_variant = False
            fr = self.headword_freq.get(normalize(r[1] or ""), 0)
            # the doubled consonant is the remainder's own initial, so a reading that devoices it is out (అద్దపు is not
            # ఆ + దపు → తపము); the yadagama glide may still be undone (అయ్యవసరంబున = ఆ + యవసరంబున → అవసరము)
            if "initial-sandhi" in (r[2] or "") and not rest.startswith("య"):
                r = (None, None, None)
            if (r[1] and aksharas(normalize(r[1])) >= 3 and aksharas(rest) >= 2 and not rest.endswith("ా")
                    and ((r[0] == "inflected" and fr >= 250) or (r[0] in ("headword", "variant", "redirect", "synonym") and fr >= 1000))):
                # an inflected remainder of a frequent word (విధంబున, యవసరంబున, మహాత్ముండు), or a bare one of a very frequent
                # word (అవ్విధము, ఎన్నెన్ని); not అట్టికము (టికము), ఎగ్గళమా (గళము), ఇచ్చలాడవలె
                return ("inflected", r[1], f"trika:{_TRIKA[w[0]]}:{rest}")
        if not getattr(self, "_in_variant", False):
            for a, b in _VARIANT_RULES:
                if a in w:
                    self._in_variant = True  # one substitution, never nested (ింత contains ంత)
                    try:
                        r = self.resolve.__wrapped__(self, w.replace(a, b, 1))  # uncached: computed without the fallback
                    finally:
                        self._in_variant = False
                    if r[0] in ("headword", "variant", "redirect", "synonym", "inflected"):
                        return ("inflected", r[1], (r[2] or "") + "+variant")
        return (None, None, None)

    def _sandhi_alternative(self, w, r, ratio=5.0):
        """The devoiced / drutam-less reading of a voiced- or న-initial entry, when it should win."""
        for alt in initial_variants(w):
            r2 = self._resolve(alt)
            if r2[0] not in ("headword", "variant", "synonym", "redirect", "inflected"):
                continue
            h1, h2 = normalize(r[1] or w), normalize(r2[1] or alt)
            if _lexeme(h1) == _lexeme(h2):
                continue
            v1, v2 = self.is_verb(h1) is True, self.is_verb(h2) is True
            f1, f2 = self.headword_freq.get(h1, 0), self.headword_freq.get(h2, 0)
            if (v2 and not v1 and f2 >= f1) or (f2 >= ratio * max(f1, 1) and f2 >= 50):
                return (r2[0], r2[1], "sandhi-preferred")
        return None

    def _resolve(self, word):
        """(status, matched headword, kind) with status in
        'headword' | 'variant' | 'redirect' | 'inflected' | 'stem' | None and kind in
        'direct' | 'nominal' | 'verbal' | 'stem' (which kind of ending was stripped)."""
        w = normalize(word)
        if not w:
            return (None, None, None)
        if (d := self._direct(w, min_aksharas=1)):
            return (d, self.redirects.get(w, w), "direct")
        # the -ం spelling of a -ము noun the dictionaries list only as a synonym or variant (కార్యం = కార్యము)
        if w.endswith("ం") and len(w) > 2 and self._direct(w[:-1] + "ము"):
            h = w[:-1] + "ము"
            return ("variant", self.redirects.get(h, h), "direct")
        # verb roots the dictionaries list without the final ు (వచ్ౘ for వచ్చు, వెలయ for వెలయు)
        if w.endswith("ు") and len(w) > 2 and self._direct(w[:-1]):
            return ("variant", self.redirects.get(w[:-1], w[:-1]), "direct")
        # a Sanskrit -అస్ stem as it stands before a voiced sound (మనో-, తపో-, యశో-: the -ఓ of మనః, తపః, యశః) is the Telugu
        # noun (మనస్సు, తపస్సు), and a visarga prefix (దుః, నిః, అంతః) the listed prefix (దుర్, నిర్, అంతర్); before the
        # particle rule, which read మనో as మన + ఓ. 3.6k tokens, no gold loss (sandhi-engine evaluation, 2026-10-25)
        if w in _VISARGA_PREFIXES and self._direct(_VISARGA_PREFIXES[w]):
            return ("variant", self.redirects.get(_VISARGA_PREFIXES[w], _VISARGA_PREFIXES[w]), "visarga")
        if w == "మహో":  # మహా + ఉ (మహోదయ, మహోత్సవ), not మహస్
            return ("variant", "మహా", "o-stem")
        if w.endswith("ో") and aksharas(w) >= 2 and (self._direct(w[:-1] + "ః") or self._direct(w[:-1] + "స్సు")):
            h = w[:-1] + ("ః" if self._direct(w[:-1] + "ః") else "స్సు")  # the dictionaries' own form first (నమః over నమస్సు)
            return ("variant", self.redirects.get(h, h), "o-stem")
        # particles the project splits off (-యు -తో -ను -అని -ఏ -ఐ -ఓ): the rest must be a headword itself
        if (p := self.particle(w)):
            base, part = p
            return ("inflected", self.redirects.get(base, base), f"particle:{part}")
        # plural / oblique -ులు of nouns in -ు, -ుడు, -ి: only directly listed forms, the shortest first
        # (పశువులు → పశువు, భక్తులు → భక్తుడు, గుడులు → గుడి, అప్పులు → అప్పు; never a bare stem such as గుడ)
        for ending in ("ులను", "ులకున్", "ులకు", "ులన్", "ులలో", "ులతో", "ులు", "ుల"):
            if w.endswith(ending) and len(w) > len(ending) + 1:
                stem = w[: -len(ending)]
                for r in ("ు", "ుడు", "ి"):
                    if self._direct(stem + r):
                        return ("inflected", self.redirects.get(stem + r, stem + r), "nominal")
        # a long stem whose -ము form is a headword is that noun, not an inflection (అనుమాన → అనుమానము, not అనుమా+న)
        if aksharas(w) >= 3 and w[-1] not in _SIGNS and w[-1] != "్" and self._direct(w + "ము") \
                and not w.endswith(("ిన", "ిరి", "ెడ", "ింప", "ంగ", "ఁగ", "చున", "యున")):
            return ("stem", w + "ము", "stem")
        # past/converb forms with the stem vowel ఇ of a root in ఉ (విఱిగిన → విఱుగు, కలిగి → కలుగు, పిలిచి → పిలుచు)
        for ending in _VERB_ALTERNATION_ENDINGS:
            if w.endswith(ending) and len(w) > len(ending) + 2:
                stem = w[: -len(ending)]
                i = stem.rfind("ి")
                if i > 0 and i >= len(stem) - 3:  # the ి sits on the stem's last or second-last consonant (కలిగ-, చదివ-)
                    root = stem[:i] + "ు" + stem[i + 1:] + ("ు" if stem[-1] not in _SIGNS else "")
                    if self._direct(root) and self.is_verb(root) is not False:
                        return ("inflected", self.redirects.get(root, root), "verbal")
        # infinitive / conditional -న్ and the negative participle -ని on a verb root (పెట్టన్ → పెట్టు,
        # చేరని → చేరు, తెలియని → తెలియు) before the nominal readings (పెట్ట, చేరడు)
        for ending in ("న్", "న", "ని"):
            if w.endswith(ending) and len(w) > len(ending) + 1:
                stem = w[: -len(ending)]
                if stem[-1] not in _SIGNS and stem[-1] != "్" and self._direct(stem + "ు") and self.is_verb(stem + "ు"):
                    return ("inflected", self.redirects.get(stem + "ు", stem + "ు"), "verbal")
        for ending, repls in _INFLECTIONS:
            if w.endswith(ending) and len(w) > len(ending) + 1:
                stem = w[: -len(ending)]
                for r in repls:
                    if (base := self._base(stem + r)):
                        kind = "verbal" if ending in _VERB_ENDINGS else "nominal"
                        return ("inflected", base, kind)
        # a bare Sanskrit/Telugu stem as used inside a samāsa (ధర్మ, రాజ, యుద్ధ, పుత్త్ర)
        if w[-1] not in _SIGNS and w[-1] != "్":
            for r in ("ము", "ుడు", "ు", "ి", "ం", "ా"):
                if self._direct(w + r):
                    return ("stem", w + r, "stem")
        if w.endswith("ా") and self._direct(w[:-1]):
            return ("stem", w[:-1], "stem")
        # converbs / past forms of -యు and -చు verbs (చేసి -> చేయు, నిల్చె -> నిలుచు)
        for ending, stems in (("సి", ["యు", "చు"]), ("చి", ["చు"]), ("చె", ["చు"]), ("సె", ["యు", "చు"]),
                              ("ల్చి", ["లుచు"]), ("ల్చె", ["లుచు"]), ("ర్చి", ["రుచు"]), ("ట్టి", ["ట్టు"])):
            if w.endswith(ending) and len(w) > len(ending) + 1:
                for st in stems:
                    if self._direct(w[: -len(ending)] + st):
                        return ("inflected", w[: -len(ending)] + st, "verbal")
        return (None, None, None)

    def particle(self, w):
        """(base headword, particle) when the word is a headword plus one of the particles the project
        splits off: కోటయు → (కోట, యు), భక్తితో → (భక్తి, తో), దిక్కని → (దిక్కు, అని), నీవే → (నీవు, ఏ),
        గురువై → (గురువు, ఐ), ఎంతో → (ఎంత, ఓ). None unless the base is a headword in its own right."""
        for ending, how in _PARTICLES:
            if not w.endswith(ending) or len(w) <= len(ending) + 1:
                continue
            rest = w[: -len(ending)]
            if how == "sign" and rest[-1] not in _SIGNS:
                continue  # -యు / -ను only after a vowel sign (కోటయు, సీతను), not inside a stem
            if how.startswith("cons"):  # -అని after a consonant: the base's final ు was elided
                if rest[-1] in _SIGNS or rest[-1] == "్":
                    continue
                rest, ending = rest + "ు", how.split(":")[1]
            elif how.startswith("elide"):  # -ఏ / -ఐ / -ఓ replaced the base's final vowel sign
                ending = how.split(":")[1]
                if rest[-1] in _SIGNS or rest[-1] == "్":
                    continue
                rest = rest + "ు" if ending != "ఓ" else rest
            if ending == "ఓ" and rest.endswith("ల"):
                continue  # -లో is the locative, not plural + ఓ
            if aksharas(rest) >= 2 and self._direct(rest) and (ending in ("ఏ", "ఐ", "ఓ", "తో") or self.is_verb(rest) is not True):
                return rest, ending
            if ending == "ఓ" and aksharas(rest) >= 2 and self._direct(rest + "ు") and self.is_verb(rest + "ు") is not True:
                return rest + "ు", ending
        return None

    def status(self, word):
        return self.resolve(word)[0]

    @lru_cache(maxsize=200000)
    def grammar(self, headword):
        """The dictionaries' grammar metadata for a headword: a set of (pos, gender, ending, origin)
        tuples over all its definitions (88,114 entries carry one; pos such as విశేష్యము, విశేషణము,
        సకర్మక/అకర్మక క్రియ, అవ్యయము; gender పుంలింగము/స్త్రీలింగము/నపుంసకలింగము; ending అకారాంతము ...)."""
        if not hasattr(self, "_spellings"):  # normalized headword -> the dictionary's own spellings (ౘదువు, చదువు)
            self._spellings = {}
            for (w,) in self._q(self.con, "select word from entries"):
                self._spellings.setdefault(normalize(w), set()).add(w)
        spellings = self._spellings.get(normalize(headword), {headword})
        rows = []
        for sp in spellings:
            rows += self._q(self.con,
                "select g.pos, g.gender, g.ending, g.origin from entries e join definitions d on d.entry_id = e.id "
                "join grammar g on g.g_id = d.g_id where e.word = ?", (sp,))
        out = set()
        for pos, gender, ending, origin in rows:
            try:
                tags = tuple(json.loads(pos)) if pos else ()
            except Exception:
                tags = (pos,)
            out.add((tags, gender or "", ending or "", origin or ""))
        return out

    @lru_cache(maxsize=100000)
    def is_verb(self, headword):
        """True if మణిదీపిక lists it as a verb root or any dictionary gives it a verb part of
        speech; None if nothing is known."""
        if normalize(headword) in self.verb_roots:
            return True
        pos = self.pos(headword)
        if not pos:
            return None
        return any("క్రియ" in p for p in pos)

    @lru_cache(maxsize=100000)
    def is_nominal(self, headword):
        pos = self.pos(headword)
        if not pos:
            return None
        return any(k in p for p in pos for k in ("విశేష్యము", "నామవాచకము", "సర్వనామము", "విశేషణము", "అవ్యయము"))

    SHORT_OK = {"ఆ", "ఈ", "ఏ", "ఐ", "ఓ", "న", "ము", "కు", "ను", "తో", "యు", "ర",
                "నా", "నీ", "మీ", "తా", "ఈ", "ఊ", "ఆ"}  # one-syllable words that are real parts

    def known(self, word):
        return self.status(word) is not None

    def known_part(self, part):
        """A part counts as resolved if it is a closed-class particle / fragment, or a word of
        at least two syllables the dictionary knows: one-syllable entries (దు, కా, ఎన్) never
        count, otherwise any split would look supported."""
        if part in self.SHORT_OK:
            return True
        return aksharas(part) >= 2 and self.status(part) is not None

    def analysis_known(self, analysis, sep="+"):
        """True if every part of a split analysis is in the dictionary."""
        return all(self.known(p) for p in analysis.split(sep))

    @lru_cache(maxsize=50000)
    def pos(self, word):
        """Parts of speech recorded for the headword (JSON strings), or [] if none."""
        w = normalize(word)
        rows = self._q(self.con,
            "select g.pos from entries e join definitions d on d.entry_id=e.id join grammar g on g.g_id=d.g_id "
            "where e.word in (?, ?) and g.pos != '[]'", (word, w))
        return sorted({r[0] for r in rows})


if __name__ == "__main__":
    import sys
    lex = Lexicon()
    print(f"{len(lex.headwords):,} headwords, {len(lex.variants):,} extra variants, {len(lex.redirects):,} redirects")
    for w in sys.argv[1:] or ["కందువ", "కనబడు", "నలుగడలు", "కావుళము", "సంపదలు", "రాజునకు", "చదువు", "చదువుతున్నాను"]:
        print(f"{w:<16} {lex.status(w)}")
