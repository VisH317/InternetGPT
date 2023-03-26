import openai
import math
from scraper import Scraper
from openai.embeddings_utils import distances_from_embeddings
from nltk.corpus import stopwords


class RecurseEmbeds:
    def __init__(self, subseq_cmp: int = 2, tf_idf_thresh: float = 0.5):
        self.subseq = subseq_cmp
        self.tf_idf_thresh = tf_idf_thresh

    def get_subseq_embeds(self, context: str):
        urls, text = self.scraper.query(context)
        ctx, emb = self.get_embeds(context, text)
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
    
    
    def get_word_counts(self, doc: list(str), selected_docs: list(str)):
        """Gets the word counts or TF_IDF for the full document returned from the webpage, idea is that rare words based on these counts can be searched recursively in the most similar contexts"""
        # first remove stopwords and tokenize words with nltk
        # then create the TF rank - research how to represent for all documents (maybe average TF across all documents)
        # calculate IDF matrix
        # multiply and sort for highest score and search based on that as well as surrounding context words
        # instead: calculate overall idf frequency, then go through term frequency in each and determine if below a desired threshold to require searching up
        filtered_doc = []
        for d in selected_docs:
            filtered_doc.append(" ".join([w for w in d.split(" ") if w.replace(",", "").replace(";", "").replace(":", "") not in stopwords.words("english")]))

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
        for d in selected_docs:
            l = [w.replace(",", "").replace(";", "").replace(":", "") for w in d.split(" ")]
            ret = []
            for w in l:
                # later take surrounding context maybe
                if w not in ret and (l.count(w)/len(l))*idf_cnt[w]<=self.tf_idf_thresh: ret.append(w)
            doc_ctx.append(ret)
        
        return doc_ctx
