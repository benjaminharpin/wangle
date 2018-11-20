class Word:    
    def __init__(self, id, lemma):
        self.id = id
        self.lemma = lemma

class Property:
    def __init__(self, name, complement=None):
        self.name = name
        self.complement = complement

    def clone(self):
        return Property(self.name, complement=self.complement)

class Part:
    def __init__(self, text, word_id=None):
        self.text = text 
        self.word_id = word_id

    def clone(self):
        return Part(self.text, self.word_id)

class Sentence:
    def __init__(self):
        self._word_id_seed = 1
        self.words = {}
        self.parts = []
        self.properties = {}

    def register_word(self, lemma):
        word = Word(self._word_id_seed, lemma)
        self.words[word.id] = word
        self._word_id_seed += 1
        return word

    def add_word(self, word_id, text, position=None):
        part = Part(text, word_id)
        if position is None:
            position = len(self.parts)
        self.parts.insert(position, part)

    def set_property(self, word_id, name, complement=None):
        if word_id not in self.properties:
            self.properties[word_id] = {}
        self.properties[word_id][name] = Property(name, complement=complement)

    def has_property(self, word_id, name):
        return word_id in self.properties and name in self.properties[word_id]

    def find_words_by_property(self, name, complement=None):
        result = []
        for word_id in self.properties:
            for name in self.properties[word_id]:
                if complement is None or complement == self.properties[word_id][name].complement:
                    result.append(self.words[word_id])
                    break
        return result

    def get_property(self, word_id, name):
        if word_id in self.properties and name in self.properties[word_id]:
            return self.properties[word_id][name]

    def get_property_complement(self, word_id, name):
        if word_id in self.properties and name in self.properties[word_id]:
            return self.properties[word_id][name].complement

    def render(self):
        result = ""
        for i, part in enumerate(self.parts):
            # add space between two words
            if i > 0:
                prev = self.parts[i - 1]
                if prev.word_id is not None and part.word_id is not None:
                    result += " "
            result += part.text

        return result
