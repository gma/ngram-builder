# Ngram Builder

You'll find this library handy if you're interested in extracting
[n-grams](http://en.wikipedia.org/wiki/N-gram) from chunks of text.

## Installation

    $ sudo python setup.py install

## Usage

These code snippets should give you an idea of what you can do with it:

    >>> counter = ngb.Counter()
    >>> builder = ngb.NgramBuilder()
    >>> text = "One response to this kind of shortcoming is to abandon the simple or strict n-gram model and introduce features from traditional linguistic theory, such as hand-crafted state variables that represent, for instance, the position in a sentence, the general topic of discourse or a grammatical state variable. Some of the best parsers of English currently in existence are roughly of this form."
    >>>
    >>> for i in range(1, 4):
    ...     counter.add(builder.find_ngrams(text, i))
    ... 

At this point we have a dictionary containing n-grams of one, two or three words in length mapped to the number of times that each n-gram occurred. 

Because the corpus of text was so small it's quite likely that most n-grams will only occur once, but let's see what else we've got:

    >>> for ngram, count in counter.iteritems():
    ...     if count > 1:
    ...         print ngram, count
    ... 
    to 2
    the 4
    state 2
    of 5
    or 2
    this 2
    in 2

If you're using this library seriously you should experiment with
`ngb.Counter.remove_subphrases` -- it can come in very handy. It removes
n-grams that are part of a longer n-gram if the shorter n-gram appears just as
frequently as the longer n-gram (which means that it can only be present
within the longer n-gram).

In this example, it removes the majority of our n-grams.

    >>> len(counter)
    165
    >>> counter.remove_subphrases()
    >>> len(counter)
    65

Finally, if you're not interested in stop words, we can really reduce the set further by passing a set of words that are to be ignored to the builder:

    >>> builder = ngb.NgramBuilder(ngb.stopwords)
    >>> counter = ngb.Counter()
    >>> for i in range(1, 4):
    ...     counter.add(builder.find_ngrams(text, i))
    ... 
    >>> counter.remove_subphrases()
    >>> len(counter)
    29
    >>> ngrams = counter.keys()
    >>> ngrams.sort()
    >>> for ngram in ngrams:
    ...     print ngram
    ... 
    abandon the simple
    best parsers
    currently in existence
    discourse or grammatical
    english currently
    existence are roughly
    features from traditional
    form
    general topic
    grammatical state variable
    hand-crafted state variables
    instance the position
    introduce features
    kind of shortcoming
    linguistic theory such
    model and introduce
    one response
    parsers of english
    position in sentence
    represent for instance
    sentence the general
    simple or strict
    state
    state variable some
    strict n-gram model
    such as hand-crafted
    topic of discourse
    traditional linguistic theory
    variables that represent
