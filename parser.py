from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import RussianStemmer
from stop_words import get_stop_words
import os

docs_directory = './government_docs/'
dir_parsed_docs = './parsed_docs/'
doc_set = os.listdir(docs_directory)

tokens = []
tokenizer = RegexpTokenizer(r'[а-я]+')
stemmer = RussianStemmer()
stop_words = get_stop_words('ru')

for doc in doc_set:
    with open(docs_directory + doc, 'r') as f:
        for line in f:
            line = line.strip().lower()
            raw_tokens = tokenizer.tokenize(line)
            stopped_tokens = [i for i in raw_tokens if (not i in stop_words) and (len(i) > 2)]
            stemmed_tokens = [stemmer.stem(i) for i in stopped_tokens]
            tokens += stemmed_tokens
    with open(dir_parsed_docs + doc[:-8], 'w') as f:
        print(' '.join(str(i) for i in tokens), file=f)
    tokens = []
