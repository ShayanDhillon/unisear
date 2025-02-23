import re;
from nltk.tokenize import sent_tokenize;
from sklearn.feature_extraction.text import TfidfVectorizer;
from sklearn.metrics.pairwise import cosine_similarity;

class SentenceGrabberAPI():
  def __init__(self):
    pass

  def grabRelevantSentences(self, sentences : list, query : str, top_n : int):
    keyword_sentences = self.filterByKeywords(sentences, query);
    ranked_sentences = self.rankBySimilarity(keyword_sentences, query);

    return ranked_sentences[:top_n];

  def filterByKeywords(self, sentences : list, query : str) -> list:
    keywords = set(query.lower().split());

    relevant_sentences = [];
    for sentence in sentences:
      sentence_lower = sentence.lower();
      if any(keyword in sentence_lower for keyword in keywords):
        relevant_sentences.append(sentence);
    return relevant_sentences;

  def rankBySimilarity(self, sentences: list, query : str) -> list:
    all_texts = [query] + sentences;
    vectorizer = TfidfVectorizer();
    tfidf_matrix = vectorizer.fit_transform(all_texts);

    query_vector = tfidf_matrix[0:1];
    sentence_vectors = tfidf_matrix[1:];
    similarities = cosine_similarity(query_vector, sentence_vectors).flatten();
    ranked_sentences = [sentence for _, sentence in sorted(zip(similarities, sentences), reverse=True)];
    return ranked_sentences;

