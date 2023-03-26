import openai
from scraper import Scraper
from openai.embeddings_utils import distances_from_embeddings
from nltk.corpus import stopwords


class RecurseEmbeds:
    def __init__(self, subseq_cmp: int = 2):
        self.subseq = subseq_cmp

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
    
    
    def get_word_counts(self, doc: list(str)):
        """Gets the word counts or TF_IDF for the full document returned from the webpage, idea is that rare words based on these counts can be searched recursively in the most similar contexts"""


