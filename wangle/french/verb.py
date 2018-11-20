def add_finite_verb(sentence, lemma, subject_id, mood="indicatif", tense="présent", informal=False, position=None):
    verb = sentence.register_word(lemma)

    verb.set_tag("verb")
    verb.set_tag("main_verb")
    verb.set_tag("mood", value=mood)
    verb.set_tag("tense", value=mood)

    if informal:
        verb.set_tag("informal")

    if mood == "indicatif":
        if tense in ["présent", "imparfait", "passé simple", "futur"]:
            verb.set_tag("finite_verb")
            verb.set_tag("conj_mood", value=mood)
            verb.set_tag("conj_tense", value=tense)

    if position is not None:
        sentence.tokens.insert(position, verb)
    else:
        sentence.tokens.append(verb)

    subj = sentence.words[subject_id]
    subj.set_tag("subject_for", verb.id)

    return verb

def conjugate(sentence, verb):
    if verb.has_tag("finite_verb"):
        # TODO: if this is an auxiliary we will have to find the subject from the parent
        subjects = sentence.find_words_by_tag("subject_for", value=verb.id)
        if any(subjects):
            subject = subjects[0]
            conj_group = None
            if subject.lemma == "je":
                conj_group = "S1"
            elif subject.lemma == "tu":
                conj_group = "S2"
            elif subject.lemma == "nous":
                conj_group = "P1"
            elif subject.lemma == "vous":
                conj_group = "P2"
            elif subject.has_tag("is_plural"):
                if subject.get_tag_value("is_plural"):
                    conj_group = "P3"
                else:
                    conj_group = "S3"

            if conj_group is not None:
                verb.set_tag("conj_group", value=conj_group)
                conj_mood = verb.get_tag_value("conj_mood")
                conj_tense = verb.get_tag_value("conj_tense")
                if conj_mood == "indicatif" and conj_tense == "présent":
                    verb.inflection = sentence.conjugator.calculate_present(verb.lemma, conj_group)
