import numpy
from gensim import corpora, models, similarities


def get_similarity_scores_all_pairs(texts):
    """Takes a list of strings as input and returns a matrix of cosine similarity values where element [m][n] represents the similarity between text m and text n.
    >>> get_similarity_scores_all_pairs(['apple banana', 'banana cherry'])
    array([[ 1.,  0.],
           [ 0.,  1.]])
    """
    n = len(texts)
    all_similarities = numpy.empty(shape=(n, n))
    corpora_dictionary = __get_corpora_dictionary__(texts)
    similarity_matrix, tfidf = __get_tfidf_similarity_matrix__(corpora_dictionary, texts)
    for i, text in enumerate(texts):
        all_similarities[i] = __get_similarity_scores__(corpora_dictionary, similarity_matrix, text, tfidf)
    return all_similarities


def __get_similarity_scores__(corpora_dictionary, similarity_matrix, text, tfidf):
    """Takes a similarity matrix and string as input and returns a list, where element i represents the cosine similarity of text and vector i in the similarity matrix."""
    vec = tfidf[corpora_dictionary.doc2bow(__tokenize_text__(text))]
    return list(similarity_matrix[vec])


def __get_tfidf_similarity_matrix__(corpora_dictionary, texts):
    """Takes a gensim.corpora.Dictionary object and list of strings as input. Returns a gensim.similarities.SparseMatrixSimilarity object for calculating cosine similarities."""
    texts_tokenized = [__tokenize_text__(text) for text in texts]

    # gensim has us convert tokens to numeric IDs using corpora.Dictionary
    corpus = [corpora_dictionary.doc2bow(text_tokenized) for text_tokenized in texts_tokenized]
    tfidf = models.TfidfModel(corpus, normalize=True)
    corpus_tfidf = tfidf[corpus]  # Feed corpus back into its own model to get the TF-IDF values for the texts

    # If texts are all identical, the call to similarities.MatrixSimilarity(...) produces an exception.
    return similarities.MatrixSimilarity(corpus_tfidf), tfidf


def __get_corpora_dictionary__(texts):
    """Takes a list of strings as input. Returns a gensim.corpora.Dictionary object."""
    return corpora.Dictionary([__tokenize_text__(text) for text in texts])


def __tokenize_text__(text):
    """Convert text to lowercase, replace periods and commas, and split it into a list.
    >>> __tokenize_text__('hi. I am, a, sentence.')
    ['hi', 'i', 'am', 'a', 'sentence']
    """
    return text.lower().replace(',', '').replace('.', '').split()

# def add_tfidf_to(texts):
#     freq_dists = get_frequency_distributions(texts)
#     freq_dist_all = reduce(lambda x, y: x + y, freq_dists)

#     tf_idfs = []
#     for i, text in enumerate(texts):
#         idf = log(len(texts) / float())


#     tokens = {}
#     for id, doc in enumerate(documents):
#         get_frequency_distributions()

#         tf = {}
#         doc["tfidf"] = {}
#         doc_tokens = doc.get("tokens", [])
#         for token in doc_tokens:
#             tf[token] = tf.get(token, 0) + 1
#         num_tokens = len(doc_tokens)
#         if num_tokens > 0:
#             for token, freq in tf.iteritems():
#                 tokens.setdefault(token, []).append((id, float(freq) / num_tokens))

#     doc_count = float(len(documents))
#     for token, docs in tokens.iteritems():
#         idf = log(doc_count / len(docs))
#         for id, tf in docs:
#             tfidf = tf * idf
#             if tfidf > 0:
#                 documents[id]["tfidf"][token] = tfidf

#     for doc in documents:
#         doc["tfidf"] = normalize(doc["tfidf"])
#         print "**"

#     writer = csv.writer(open('similarities.csv','wb'),delimiter=';')
#     for i, document in enumerate(documents):
#         for document2 in documents[i+1:]:
#             print document['id'], document2['id'], cosine_distance(document, document2)
#             writer.writerow([document['id'], document2['id'], cosine_distance(document, document2)])


# def get_frequency_distributions(texts):
#     term_frequencies = [FreqDist(text.lower().split()) for text in texts]


# def normalize(features):
#     norm = 1.0 / sqrt(sum(i**2 for i in features.itervalues()))
#     for k, v in features.iteritems():
#         features[k] = v * norm
#     return features


# def cosine_distance(a, b):
#     cos = 0.0
#     a_tfidf = a["tfidf"]
#     for token, tfidf in b["tfidf"].iteritems():
#         if token in a_tfidf:
#             cos += tfidf * a_tfidf[token]
#     return cos
