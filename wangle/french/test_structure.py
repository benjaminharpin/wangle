import unittest

from .structure import *

class Tests(unittest.TestCase):

    def test_subject_pronoun_gender(self):
        pronoun_genders = [
            ('je', None),
            ('tu', None),
            ('il', "masc"),
            ('elle', "fem"),
            ('on', None),
            ('ce', None),
            ('ça', None),
            ('cela', None),
            ('ceci', None),
            ('qui', None),
            ('nous', None),
            ('vous', None),
            ('ils', "masc"),
            ('elles', "fem"),
        ]
        for pronoun, gender in pronoun_genders:
            with self.subTest(pronoun=pronoun):
                s = Sentence()
                p = s.add_subject_pronoun(pronoun)
                if gender is None:
                    self.assertFalse(s.has_property(p.id, "gender"))
                else:
                    self.assertEqual(s.get_property_complement(p.id, "gender"), gender)

    def test_subject_pronoun_plurality(self):
        pronoun_pluralities = [
            ('je', False),
            ('tu', False),
            ('il', False),
            ('elle', False),
            ('on', False),
            ('ce', None),
            ('ça', False),
            ('cela', False),
            ('ceci', False),
            ('nous', True),
            ('vous', None),
            ('ils', True),
            ('elles', True),
        ]
        for pronoun, is_plural in pronoun_pluralities:
            with self.subTest(pronoun=pronoun):
                s = Sentence()
                p = s.add_subject_pronoun(pronoun)
                if is_plural is None:
                    self.assertFalse(s.has_property(p.id, "is_plural"))
                else:
                    self.assertEqual(s.get_property_complement(p.id, "is_plural"), is_plural)

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
                p = s.add_subject_pronoun(subject)
                v = s.add_finite_verb('être', p.id)
                s.inflect()
                self.assertEqual(s.render(), conjugation)

    def test_adjective_derives_declension(self):
        for gender in [None, "masc", "fem"]:
            for is_plural in [None, True, False]:
                with self.subTest(gender=gender, is_plural=is_plural):
                    s = Sentence()
                    p = s.add_subject_pronoun("vous", gender=gender, is_plural=is_plural)
                    if gender is None:
                        self.assertFalse(s.has_property(p.id, "gender"))
                    else:
                        self.assertEqual(s.get_property_complement(p.id, "gender"), gender)
                    if is_plural is None:
                        self.assertFalse(s.has_property(p.id, "is_plural"))
                    else:
                        self.assertEqual(s.get_property_complement(p.id, "is_plural"), is_plural)
                    v = s.add_finite_verb("être", p.id)
                    adj = s.add_adjective("content", p.id)

                    s.determine_declension_parameters()
                    if gender is None:
                        self.assertFalse(s.has_property(adj.id, "gender"))
                    else:
                        self.assertEqual(s.get_property_complement(adj.id, "gender"), gender)
                    if is_plural is None:
                        self.assertFalse(s.has_property(adj.id, "is_plural"))
                    else:
                        self.assertEqual(s.get_property_complement(adj.id, "is_plural"), is_plural)

    def test_adjective_declension(self):
        declensions = [
            (None, False, "vous êtes content"),
            (None, True, "vous êtes contents"),
            ("masc", None, "vous êtes content"),
            ("fem", None, "vous êtes contente"),
            ("masc", False, "vous êtes content"),
            ("fem", False, "vous êtes contente"),
            ("masc", True, "vous êtes contents"),
            ("fem", True, "vous êtes contentes"),
        ]
        for gender, is_plural, declension in declensions:
            with self.subTest(gender=gender, is_plural=is_plural):
                s = Sentence()
                p = s.add_subject_pronoun("vous", gender=gender, is_plural=is_plural)
                v = s.add_finite_verb("être", p.id)
                adj = s.add_adjective("content", p.id)
                s.inflect()
                self.assertEqual(s.render(), declension)

    def test_simple_contraction(self):
        s = Sentence()
        p = s.add_subject_pronoun('je')
        v = s.add_finite_verb('aimer', p.id)
        s.inflect()
        s.contract()
        self.assertEqual(s.render(), "j'aime")
