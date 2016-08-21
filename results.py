import gensim
from os import listdir
import xlsxwriter


def arr2str(arr):
    s = ''
    if len(arr) == 0:
        return s
    for i in range(len(arr)-1):
        s += arr[i]
        s += '; '
    s += arr[-1]
    return s

dictionary = gensim.corpora.Dictionary.load('government_docs.dict')
corpus = gensim.corpora.MmCorpus('government_docs.mm')
lda = gensim.models.ldamodel.LdaModel.load('government_docs.model')

names_from_tags = []
created_names = []
with open('named_government_topics.txt', 'r') as f:
    for line in f:
        topic = line.strip().split('\t')
        if len(topic) > 1:
            topic_id, topic_name, source = topic
            if source == 'tag':
                names_from_tags.append((topic_id, topic_name))
            elif source == 'named':
                created_names.append((topic_id, topic_name))
print(names_from_tags)
print(created_names)

topic_names = {}
with open('named_government_topics.txt', 'r') as f:
    for line in f:
        topic = line.strip().split('\t')
        if len(topic) > 1:
            topic_id = topic[0]
            topic_name = topic[1]
            topic_names[topic_id] = topic_name

dir_docs = './parsed_docs/'
files = sorted(listdir(dir_docs))

workbook = xlsxwriter.Workbook('topics_for_government_docs.xlsx')
worksheet = workbook.add_worksheet()
row = 0
for file in files:
    doc_link = 'http://government.ru/docs/' + file + '/'
    with open(dir_docs+file, 'r') as f:
        tokens = f.read().split()
        file_corpus = dictionary.doc2bow(tokens)
        file_topics = lda.get_document_topics(file_corpus)
        sorted_topics = sorted(file_topics, key=lambda tup: -tup[1])
        top_file_topics = [x[0] for x in sorted_topics if x[1] > 0.2]
        named_topics = []
        for topic in top_file_topics:
            named_topics.append(topic_names.get(str(topic)))
            named_topics = [x for x in named_topics if x is not None]
        doc_topics = arr2str(named_topics)
        worksheet.write(row, 0, doc_link)
        worksheet.write(row, 1, doc_topics)
        row += 1
workbook.close()
