import structure

from . import conjugator
from . import decliner 

class Sentence(structure.Sentence):
    conjugator = conjugator
    decliner = decliner


    def add_subject_pronoun(self, lemma, gender=None, is_plural=None, position=None):
        word = self.register_word(lemma)
        self.set_property(word.id, "pronoun")
        if lemma in ["il", "ils"]:
            self.set_property(word.id, "gender", "masc")
        elif lemma in ["elle", "elles"]:
            self.set_property(word.id, "gender", "fem")
        elif gender is not None:
            self.set_property(word.id, "gender", complement=gender)
        if lemma in ["je", "tu", "il", "elle", "on", "ça", "cela", "ceci"]:
            self.set_property(word.id, "is_plural", False)
        elif lemma in ["nous", "ils", "elles"]:
            self.set_property(word.id, "is_plural", True)
        elif is_plural is not None:
            self.set_property(word.id, "is_plural", complement=is_plural)
        self.add_word(word.id, lemma, position=position)
        return word

    def add_finite_verb(self, lemma, subject_id, mood="indicatif", tense="présent", informal=False, position=None):
        verb = self.register_word(lemma)
        subj = self.words[subject_id]
        self.set_property(verb.id, "verb")
        self.set_property(verb.id, "main_verb")
        self.set_property(verb.id, "mood", complement=mood)
        self.set_property(verb.id, "tense", complement=mood)
        if informal:
            self.set_property(verb.id, "informal")
        self.set_property(subj.id, "subject_for", verb.id)
        if mood == "indicatif":
            if tense in ["présent", "imparfait", "passé simple", "futur"]:
                self.set_property(verb.id, "finite_verb")
                self.set_property(verb.id, "conj_mood", complement=mood)
                self.set_property(verb.id, "conj_tense", complement=tense)

        self.add_word(verb.id, lemma, position=position)
        return verb
    
    def add_adjective(self, lemma, nominal_word_id, position=None):
        word = self.register_word(lemma)
        self.set_property(word.id, "adjective")
        self.set_property(word.id, "modifies", nominal_word_id)
        self.add_word(word.id, lemma, position=position)
        return word

    def determine_declension_parameters(self):
        # for adjectives, derive gender and plurality from the word that it modifies
        for part in self.parts:
            if part.word_id is not None:
                word = self.words[part.word_id]
                if self.has_property(word.id, "adjective") and self.has_property(word.id, "modifies"):
                    modifies_word_id = self.get_property_complement(word.id, "modifies")
                    if not self.has_property(word.id, "gender") and self.has_property(modifies_word_id, "gender"):
                        gender = self.get_property_complement(modifies_word_id, "gender")
                        self.set_property(word.id, "gender", complement=gender)
                    if not self.has_property(word.id, "is_plural") and self.has_property(modifies_word_id, "is_plural"):
                        is_plural = self.get_property_complement(modifies_word_id, "is_plural")
                        self.set_property(word.id, "is_plural", complement=is_plural)

    def determine_conjugation_parameters(self):
        for part in self.parts:
            if part.word_id is not None:
                word = self.words[part.word_id]
                if self.has_property(word.id, "finite_verb"):
                    # TODO: if this is an auxiliary we will have to find the subject from the parent
                    subjects = self.find_words_by_property(name="subject_for", complement=word.id)
                    if any(subjects):
                        subject = subjects[0]
                        if subject.lemma == "je":
                            self.set_property(word.id, "conj_group", complement="S1")
                        elif subject.lemma == "tu":
                            self.set_property(word.id, "conj_group", complement="S2")
                        elif subject.lemma == "nous":
                            self.set_property(word.id, "conj_group", complement="P1")
                        elif subject.lemma == "vous":
                            self.set_property(word.id, "conj_group", complement="P2")
                        elif self.has_property(subject.id, "is_plural") and not self.get_property_complement(subject.id, "is_plural"):
                            self.set_property(word.id, "conj_group", complement="S3")
                        elif self.has_property(subject.id, "is_plural") and self.get_property_complement(subject.id, "is_plural"):
                            self.set_property(word.id, "conj_group", complement="P3")

    def inflect(self):
        self.determine_declension_parameters()
        for part in self.parts:
            if part.word_id is not None:
                word = self.words[part.word_id]
                if self.has_property(word.id, "adjective"):
                    gender = "masc"
                    if self.has_property(word.id, "gender"):
                        gender = self.get_property_complement(word.id, "gender")
                    is_plural = False
                    if self.has_property(word.id, "is_plural"):
                        is_plural = self.get_property_complement(word.id, "is_plural")
                    part.text = self.decliner.decline(word.lemma, gender == "masc", is_plural)

        self.determine_conjugation_parameters()
        for part in self.parts:
            if part.word_id is not None:
                word = self.words[part.word_id]
                if self.has_property(word.id, "finite_verb") and self.has_property(word.id, "conj_group"):
                    conj_mood = self.get_property_complement(word.id, "conj_mood")
                    conj_tense = self.get_property_complement(word.id, "conj_tense")
                    conj_group = self.get_property_complement(word.id, "conj_group")
                    if conj_mood == "indicatif" and conj_tense == "présent":
                        part.text = self.conjugator.calculate_present(word.lemma, conj_group)

    def contract(self):
        i = 0
        while i < len(self.parts) - 1:
            part = self.parts[i]
            next_part = self.parts[i + 1]
            if part.text in ["je", "me", "te", "se", "le", "la"] and next_part.text[0] in "aâeéèêhiîïoôuy":
                part.text = part.text[0]
                self.parts.insert(i + 1, structure.Part("'"))
            i += 1
