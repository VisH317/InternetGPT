import openai
import math
from scraper import Scraper
from openai.embeddings_utils import distances_from_embeddings
from nltk.corpus import stopwords
from typing import NamedTuple

class WordEntry(NamedTuple):
    word: str
    tfidf: float

class ScraperOutput(NamedTuple):
    urls: list(str)
    text: list(str)

def compare_word_entry(we1: WordEntry, we2: WordEntry):
    if we1.tfidf<we2.tfidf: return 1
    elif we1.tfidf>we2.tfidf: return -1
    else: return 0

class RecurseEmbeds:
    def __init__(self, subseq_cmp: int = 2, tf_idf_thresh: float = 2.0):
        self.subseq = subseq_cmp
        self.tf_idf_thresh = tf_idf_thresh
        self.scraper = Scraper(2)

    def get_subseq_embeds(self, context: str, doc: list(str)):
        sub = self.get_word_counts(doc, context).sort(key=compare_word_entry)[:self.subseq]
        urls_list = []
        words_map = []
        text_list = []
        for s in sub:
            urls, text = self.scraper.query(context)
            for u in urls: urls_list.append(u)
            for t in text: 
                text_list.append(t)
                words_map.append(s.word)
        ctx, emb = self.get_embeds(context, text_list)
        distances = distances_from_embeddings(ctx, emb, distance_metric="cosine")
        vals = zip(urls, distances)
        vals = sorted(vals, key=self.sort_embeds)
        ret_ctx = context
        for txt,_ in vals[:self.subseq]: ret_ctx += "; " + txt;
        return ret_ctx
    

    def get_embeds(self, question: str, context: list(str)):
        question_embed = openai.Embedding.create(input=[question], model=self.model)
        context_embed = openai.Embedding.create(input=context, model=self.model)
        return question_embed, context_embed
    
    
    def get_word_counts(self, doc: list(str), selected_doc: str) -> list(WordEntry):
        """Gets the word counts or TF_IDF for the full document returned from the webpage, idea is that rare words based on these counts can be searched recursively in the most similar contexts"""
        # first remove stopwords and tokenize words with nltk
        # then create the TF rank - research how to represent for all documents (maybe average TF across all documents)
        # calculate IDF matrix
        # multiply and sort for highest score and search based on that as well as surrounding context words
        # instead: calculate overall idf frequency, then go through term frequency in each and determine if below a desired threshold to require searching up
        filtered_doc = [w for w in d.split(" ") if w.replace(",", "").replace(";", "").replace(":", "") not in stopwords.words("english")]

        # calculate counts for IDF
        idf_cnt = {}
        for d in doc:
            found = []
            for w in [w.replace(",", "").replace(";", "").replace(":", "") for w in d.split(" ")]:
                if w not in found: 
                    if w not in idf_cnt.keys(): idf_cnt[w] = 1
                    else: idf_cnt[w]+=1
        # calculate IDF
        for key, value in idf_cnt.items():
            idf_cnt[key] = math.log(len(doc)/value)

        doc_ctx = []
        ret = []
        for w in filtered_doc:
            # later take surrounding context maybe
            tfidf = (filtered_doc.count(w)/len(filtered_doc))*idf_cnt[w]
            if w not in ret and tfidf>=self.tf_idf_thresh: doc_ctx.append(WordEntry(w, tfidf))
        
        return doc_ctx
