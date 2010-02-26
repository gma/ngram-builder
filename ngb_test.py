import unittest

import ngb


class CounterTest(unittest.TestCase):
    
    def test_when_adding_two_ngrams_then_counts_added(self):
        counter = ngb.Counter({ "apple": 1 })
        counter.add(ngb.Counter({ "apple": 2 }))
        self.assertEqual(counter["apple"], 3)

    def test_when_cannot_remove_subphrases_then_none_removed(self):
        counter = ngb.Counter({
            "apple": 4,
            "apple core": 3,
            "apple core removal": 2,
            "apple core removal tool": 1,
        })
        counter.remove_subphrases()
        self.assertEqual(len(counter.keys()), 4)

    def test_when_can_remove_all_subphrases_then_all_removed(self):
        counter = ngb.Counter({
            "apple": 1,
            "apple core": 1,
            "core removal": 1,
            "apple core removal": 1,
            "apple core removal tool": 1,
        })
        counter.remove_subphrases()
        self.assertEqual(counter, { "apple core removal tool": 1 })

    def test_when_can_remove_some_subphrases_then_some_removed(self):
        counter = ngb.Counter({
            "apple": 2,
            "apple core": 1,
            "core removal": 1,
            "apple core removal tool": 1,
        })
        counter.remove_subphrases()
        self.assertEqual(counter, { "apple": 2, "apple core removal tool": 1 })
    
    def test_when_subphrase_appears_within_ngram_then_can_be_removed(self):
        counter = ngb.Counter({ "core": 1, "apple core removal": 1 })
        counter.remove_subphrases()
        self.failIf("core" in counter)


class NgramBuilderTest(unittest.TestCase):
    
    def setUp(self):
        self.text = "apple banana apple potato"
        self.NgramBuilder = ngb.NgramBuilder(stopwords=ngb.stopwords)
    
    def test_when_counting_unigrams_then_single_words_found(self):
        ngrams = { "apple": 2, "banana": 1, "potato": 1 }
        self.assertEqual(self.NgramBuilder.find_ngrams(self.text, 1), ngrams)
    
    def test_when_counting_bigrams_then_double_words_found(self):
        ngrams = { "apple banana": 1, "banana apple": 1, "apple potato": 1 }
        self.assertEqual(self.NgramBuilder.find_ngrams(self.text, 2), ngrams)
    
    def test_when_counting_ngrams_same_length_as_input_then_1_found(self):
        length = len(self.text.split(" "))
        self.assertEqual(
                self.NgramBuilder.find_ngrams(self.text, length), { self.text: 1 })
    
    def test_when_counting_ngrams_longer_than_input_then_nothing_found(self):
        self.assertEqual(self.NgramBuilder.find_ngrams(self.text, 100), {})
    
    def test_when_text_contains_punctuation_then_punctuation_ignored(self):
        text = "apple, banana"
        expected =  { "apple": 1, "banana": 1 }
        self.assertEqual(self.NgramBuilder.find_ngrams(text, 1), expected)
    
    def test_when_text_contains_numbers_then_not_returned_as_unigrams(self):
        text = "1 potato, 2 potato"
        self.assertEqual(self.NgramBuilder.find_ngrams(text, 1), { "potato": 2 })
    
    def test_when_unigram_is_single_character_then_excluded(self):
        self.assertEqual(self.NgramBuilder.find_ngrams("a bc", 1), { "bc": 1 })
    
    def test_when_unigram_doesnt_contain_letter_then_ignored(self):
        self.assertEqual(self.NgramBuilder.find_ngrams("23:45", 1), {})

    def test_when_ngram_starts_with_stopword_then_ignored(self):
        self.assertEqual(self.NgramBuilder.find_ngrams("the apple", 2), {})
        self.assertEqual(self.NgramBuilder.find_ngrams("of the bear", 2), {})

    def test_when_ngram_ends_with_stopword_then_ignored(self):
        self.assertEqual(self.NgramBuilder.find_ngrams("apple the", 2), {})
        self.assertEqual(self.NgramBuilder.find_ngrams("bear of the", 2), {})


class TokenizerTest(unittest.TestCase):
    
    def tokenize(self, text):
        return ngb.NgramBuilder().split_into_unigrams(text)[1]
    
    def test_when_word_contains_apostrophe_then_included_in_unigram(self):
        self.assertTrue("don't" in self.tokenize("don't you know"))
    
    def test_when_word_ends_with_punctuation_then_removed(self):
        unigrams = self.tokenize("yes, thanks! - much.")
        self.assertEqual(["yes", "thanks", "much"], unigrams)
    
    def test_when_word_is_punctuation_then_removed(self):
        self.assertEqual([], self.tokenize("{ } [ ] ( ) /"))
    
    def test_when_content_is_whitespace_then_not_considered_an_ngram(self):
        self.assertEqual(["fruit"], self.tokenize("  \tfruit!\n \t\t "))
    
    def test_when_content_contains_newlines_then_split_on_newlines(self):
        self.assertEqual(["foo", "bar"], self.tokenize("foo\n\nbar"))


if __name__ == '__main__':
    unittest.main()

