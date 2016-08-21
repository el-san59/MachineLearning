from os import listdir
from gensim import corpora, models


num_topics = 100
num_words = 20
dir_docs = './parsed_docs/'
files = sorted(listdir(dir_docs))
texts = []

for file in files:
    with open(dir_docs+file, 'r') as f:
        texts.append(f.read().split())


# dictionary creation
dictionary = corpora.Dictionary(texts)
print(dictionary)
dictionary.filter_extremes(no_below=5, no_above=0.3)
dictionary.compactify()
print(dictionary)
dictionary.save('government_docs.dict')

# corpus creation
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('government_docs.mm', corpus)

# LDA_model creation
ldamodel = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary)
ldamodel.save('government_docs.model')

# generated topics
topics = ldamodel.print_topics(num_topics=num_topics, num_words=num_words)
print(topics)



