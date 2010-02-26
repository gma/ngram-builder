from distutils.core import setup

import ngb


setup(name="ngram-NgramBuilder",
      py_modules=["ngb"],
      version=ngb.__version__,
      description="Build ngrams from chunks of text",
      author="Graham Ashton",
      author_email="graham@effectif.com",
      url="http://github.com/gma/ngram-NgramBuilder",
      )
