# -*- coding: utf-8 -*-
"""
The human-evaluation rubric: ten questions, in the order the form shows them.

Edit the wording here; keep the ``key`` of a question stable once annotation has
started, because the stored answers and the agreement report are keyed by it.
Bump RUBRIC_VERSION when the meaning of a question changes; every annotation
records the version it was made under.
"""
from __future__ import annotations

from dataclasses import dataclass, field

RUBRIC_VERSION = "1"

LIKERT = (1, 2, 3, 4, 5)
BINARY = (0, 1)


@dataclass(frozen=True)
class Question:
    key: str
    number: int
    text: str
    text_te: str
    kind: str                         # 'likert' (1-5, ordinal) | 'binary' (0/1, nominal)
    low: str = ""                     # anchor of the lowest value
    high: str = ""                    # anchor of the highest value
    applies: str = "always"           # 'always' | 'bhavam' (needs a bhavam) | 'prasa' (meter has prāsa)
    na_reason: str = ""               # shown instead of the choices when the question does not apply
    guide: str = ""                   # one-paragraph guidance in the rubric guide
    anchors: dict = field(default_factory=dict)

    @property
    def choices(self) -> tuple[int, ...]:
        return LIKERT if self.kind == "likert" else BINARY

    @property
    def level(self) -> str:
        """Level of measurement used for Krippendorff's alpha."""
        return "ordinal" if self.kind == "likert" else "nominal"

    def label(self, value: int) -> str:
        if self.kind == "binary":
            return "అవును · Yes" if value == 1 else "కాదు · No"
        return self.anchors.get(value, "")


def _scale(low: str, high: str) -> dict:
    return {1: low, 5: high}


QUESTIONS: tuple[Question, ...] = (
    Question("readability", 1, "How easy is it to read?", "చదవడం ఎంత సులభం?", "likert",
             low="Very difficult", high="Very easy", anchors=_scale("Very difficult", "Very easy"),
             guide="Fluency of reading the poem aloud or silently: does it flow, or do you stumble over it?"),
    Question("comprehension", 2, "How easy is it to understand immediately after reading?",
             "చదివిన వెంటనే అర్థం చేసుకోవడం ఎంత సులభం?", "likert",
             low="Not understood", high="Understood at once", anchors=_scale("Not understood", "Understood at once"),
             guide="Your first-pass understanding, before opening the bhavam. Answer 1–3 before revealing it."),
    Question("lexical", 3, "How easy is it to recognize and understand the words in the poem?",
             "పద్యంలోని పదాలను గుర్తించి అర్థం చేసుకోవడం ఎంత సులభం?", "likert",
             low="Most words unclear", high="Every word clear", anchors=_scale("Most words unclear", "Every word clear"),
             guide="Word level only: can you split the sandhi and recognise each word, and are the words real Telugu or Sanskrit words?"),
    Question("bhavam", 4, "How close is the poem with the bhavam?", "పద్యం భావానికి ఎంత దగ్గరగా ఉంది?", "likert",
             low="Unrelated", high="Conveys it fully", anchors=_scale("Unrelated", "Conveys it fully"),
             applies="bhavam", na_reason="ఈ పద్యానికి భావం అందుబాటులో లేదు · No bhavam is available for this poem.",
             guide="Open the bhavam only after answering 1–3. Judge how faithfully the poem expresses that meaning."),
    Question("chandassu", 5, "Is chandassu correct?", "ఛందస్సు సరిగ్గా ఉందా?", "binary",
             guide="Gaṇas, guru/laghu and the number of pādas of the named meter. The gaṇa division shown is the engine's reading; check it."),
    Question("prasa", 6, "Is prasa correct?", "ప్రాస సరిగ్గా ఉందా?", "binary",
             applies="prasa", na_reason="ఈ ఛందస్సులో ప్రాస నియమం లేదు · This meter has no prāsa rule.",
             guide="The second akshara of every pāda (double underline) must rhyme by the prāsa rules."),
    Question("yati", 7, "Is yathi correct?", "యతి సరిగ్గా ఉందా?", "binary",
             guide="The first akshara of each pāda and its yati-sthāna akshara (single underline) must be yati-maitri."),
    Question("shabdalankara", 8, "Were you able to identify any shabda alankaras?",
             "శబ్దాలంకారాలు ఏవైనా గుర్తించగలిగారా?", "binary",
             guide="Sound figures: anuprāsa, vṛttyanuprāsa, chēkānuprāsa, yamaka, lāṭānuprāsa, antyānuprāsa …"),
    Question("arthalankara", 9, "Were you able to identify any artha alankaras?",
             "అర్థాలంకారాలు ఏవైనా గుర్తించగలిగారా?", "binary",
             guide="Figures of meaning: upamā, rūpaka, utprēkṣā, atiśayōkti, ślēṣa, arthāntaranyāsa …"),
    Question("poetic", 10, "How poetic is it?", "పద్యం ఎంత కవితాత్మకంగా ఉంది?", "likert",
             low="Prose in metre", high="Highly poetic", anchors=_scale("Prose in metre", "Highly poetic"),
             guide="Overall poetic quality: imagery, diction, rasa and craft, beyond metrical correctness."),
)

BY_KEY = {q.key: q for q in QUESTIONS}
COMMENTS_MAX = 5000


def applicable(question: Question, poem) -> bool:
    """Whether ``question`` is asked for ``poem`` (a store.Poem)."""
    if question.applies == "bhavam":
        return poem.has_bhavam
    if question.applies == "prasa":
        return poem.prasa_applicable
    return True


def parse_answers(form, poem) -> tuple[dict, dict]:
    """Validate a submitted form. Returns (answers, errors), both keyed by question key.

    A question that does not apply to the poem is stored as None whatever was sent.
    """
    answers, errors = {}, {}
    for q in QUESTIONS:
        if not applicable(q, poem):
            answers[q.key] = None
            continue
        raw = (form.get(q.key) or "").strip()
        try:
            value = int(raw)
        except ValueError:
            value = None
        if value not in q.choices:
            errors[q.key] = "Please choose an answer."
            answers[q.key] = None
        else:
            answers[q.key] = value
    return answers, errors
