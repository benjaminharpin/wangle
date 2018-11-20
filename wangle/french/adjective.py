def add_adjective(sentence, lemma, nominal_word_id, position=None):
    word = sentence.register_word(lemma)

    word.set_tag("adjective")
    word.set_tag("modifies", nominal_word_id)

    if position is not None:
        sentence.tokens.insert(position, word)
    else:
        sentence.tokens.append(word)

    return word

def decline(sentence, adjective):
    gender, is_plural = "masc", False
    if adjective.has_tag("modifies"):
        modifies = sentence.words[adjective.get_tag_value("modifies")]

        if not adjective.has_tag("gender") and modifies.has_tag("gender"):
            gender = modifies.get_tag_value("gender")
            adjective.set_tag("gender", value=gender)

        if not adjective.has_tag("is_plural") and modifies.has_tag("is_plural"):
            is_plural = modifies.get_tag_value("is_plural")
            adjective.set_tag("is_plural", value=is_plural)

    adjective.inflection = sentence.decliner.decline(adjective.lemma, gender == "masc", is_plural)
