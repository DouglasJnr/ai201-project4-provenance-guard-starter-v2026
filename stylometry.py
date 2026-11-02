"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies. ← TODO

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.
    """
    lengths = [len(words(sentence)) for sentence in sentences(text)]
    lengths = [length for length in lengths if length > 0]
    if len(lengths) < 2:
        return 0.0

    mean = statistics.mean(lengths)
    if mean == 0:
        return 0.0
    return round(statistics.stdev(lengths) / mean, 4)


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words. ← TODO

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    return round(len(set(tokens)) / len(tokens), 4)


def punctuation_density(text: str) -> float:
    """
    How much punctuation, relative to length. ← TODO

    Returns:
        A float. Whether you count all punctuation or only some kinds — commas,
        semicolons, dashes — is a real choice. Semicolons and em dashes are
        more interesting than full stops, because they vary more between
        writers.
    """
    # Full stops and apostrophes are left out: stops just track sentence count,
    # and apostrophes are contractions, not punctuation choices. What's left —
    # commas, semicolons, colons, dashes, brackets, quotes, ! and ? — is where
    # writers differ. Returned as marks per word (roughly 0.0–0.15 in practice).
    tokens = words(text)
    if not tokens:
        return 0.0
    marks = re.findall(r'[,;:—–()!?"“”]|--|\.\.\.|…', text)
    return round(len(marks) / len(tokens), 4)


# ── Two more measures: what kind of words, not how they're arranged ──────────
#
# The three above all measure rhythm and evenness, and so does signal one in
# its own way. Plain human writing is even too, so it scored as AI on every one
# of them. These two look at word choice instead.

ABSTRACT_SUFFIX = re.compile(r"(tion|sion|ment|ity|ness|ance|ence|ism)s?$")

TRANSITION_WORDS = {
    "first", "firstly", "second", "secondly", "third", "thirdly", "finally",
    "lastly", "additionally", "moreover", "furthermore", "overall", "however",
    "therefore", "thus", "ultimately", "consequently", "importantly",
    "similarly", "conversely", "nevertheless", "notably",
}


def abstract_vocabulary(text: str) -> float:
    """
    Share of words that are long or abstract nouns. Higher means more AI-ish.

    A word counts if it's 9+ letters, or 7+ letters ending in an abstract-noun
    suffix (-tion, -ment, -ity, -ness...). Generated explainer prose leans on
    "prioritization" and "environment"; plain human writing on "bus" and
    "shelves". Returns 0.0–1.0; in practice roughly 0.0–0.3.

    Blind spot: formal and academic human writing uses these words too.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    abstract = sum(
        1 for token in tokens
        if len(token) >= 9 or (len(token) > 6 and ABSTRACT_SUFFIX.search(token))
    )
    return round(abstract / len(tokens), 4)


def transition_rate(text: str) -> float:
    """
    Transition and listing words per word. Higher means more AI-ish.

    Catches the "First... Second... Finally... Additionally" scaffolding of
    generated text, which tends to survive light editing. Returns roughly
    0.0–0.08 in practice.

    Blind spot: writers taught the five-paragraph essay do exactly this, and
    deleting the words is trivial.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    return round(sum(token in TRANSITION_WORDS for token in tokens) / len(tokens), 4)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.
    """
    if not words(text):
        return 0.5

    spread = sentence_length_spread(text)
    vocabulary_variety = type_token_ratio(text)
    punctuation = punctuation_density(text)
    abstract = abstract_vocabulary(text)
    transitions = transition_rate(text)

    # Each measure goes onto a 0–1 "AI-ness" scale with a clamped linear map
    # between two anchor values. The first three run "higher = more human", so
    # they're flipped; the last two already point the AI way.
    #
    #   spread       0.2 or less -> 1.0 (sentences march in step)
    #                1.0 or more -> 0.0 (short next to long)
    #   punctuation  0 per word  -> 1.0;  0.10+ per word -> 0.0
    #   vocabulary   TTR 0.65    -> 1.0;  0.95+          -> 0.0
    #   abstract     0           -> 0.0;  0.20+          -> 1.0
    #   transitions  0           -> 0.0;  0.05+ per word -> 1.0
    #
    # Weights: spread 0.3, abstract 0.3, transitions 0.15, punctuation 0.15,
    # TTR 0.1. Rhythm (spread, punctuation) and word choice (abstract,
    # transitions) get 0.45 each, so plain-but-even human writing can't max out
    # the score on rhythm alone. TTR stays small because it drops with text
    # length alone, so on inputs of different sizes it measures length as much
    # as vocabulary.
    spread_component = _clamp((1.0 - spread) / 0.8)
    # One sentence has no spread to measure. That's missing evidence, not
    # evidence of uniformity, so it sits at neutral rather than "very AI".
    if len(sentences(text)) < 2:
        spread_component = 0.5
    punctuation_component = _clamp(1.0 - punctuation / 0.10)
    vocabulary_component = _clamp((0.95 - vocabulary_variety) / 0.30)
    abstract_component = _clamp(abstract / 0.20)
    transition_component = _clamp(transitions / 0.05)

    return round(
        0.3 * spread_component
        + 0.3 * abstract_component
        + 0.15 * transition_component
        + 0.15 * punctuation_component
        + 0.1 * vocabulary_component,
        4,
    )


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"abstract_vocabulary      {abstract_vocabulary(text)}")
    print(f"transition_rate          {transition_rate(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
