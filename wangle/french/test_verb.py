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
