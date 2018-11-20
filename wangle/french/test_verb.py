import unittest

from .structure import Sentence
from .pronoun import add_subject_pronoun
from .verb import add_finite_verb

class Tests(unittest.TestCase):
    def test_verb_inflection(self):
        conjugations = [
            ("je", "je suis"),
            ("tu", "tu es"),
            ("il", "il est"),
            ("nous", "nous sommes"),
            ("vous", "vous êtes"),
            ("ils", "ils sont"),
        ]
        for subject, conjugation in conjugations:
            with self.subTest(subject=subject):
                s = Sentence()
                p = add_subject_pronoun(s, subject)
                v = add_finite_verb(s, 'être', p.id)
                s.inflect()
                self.assertEqual(str(s), conjugation)

    def test_passe_compose(self):
        conjugations = [
            ("je", "j'ai aimé"),
            ("tu", "tu as aimé"),
            ("il", "il a aimé"),
            ("nous", "nous avons aimé"),
            ("vous", "vous avez aimé"),
            ("ils", "ils ont aimé"),
        ]
        for subject, conjugation in conjugations:
            with self.subTest(subject=subject):
                s = Sentence()
                p = add_subject_pronoun(s, subject)
                v = add_finite_verb(s, 'aimer', p.id, tense="passé composé")
                s.inflect()
                s.contract()
                self.assertEqual(str(s), conjugation)

    def test_past_participle_agrees_with_subject_for_transitive_conjugation_with_etre_aux(self):
        declensions = [
            (None, False, "vous êtes allé"),
            (None, True, "vous êtes allés"),
            ("masc", None, "vous êtes allé"),
            ("fem", None, "vous êtes allée"),
            ("masc", False, "vous êtes allé"),
            ("fem", False, "vous êtes allée"),
            ("masc", True, "vous êtes allés"),
            ("fem", True, "vous êtes allées"),
        ]
        for gender, is_plural, result in declensions:
            with self.subTest(gender=gender, is_plural=is_plural):
                s = Sentence()
                p = add_subject_pronoun(s, "vous", gender=gender, is_plural=is_plural)
                v = add_finite_verb(s, "aller", p.id, tense="passé composé")
                s.inflect()
                self.assertEqual(str(s), result)
