import openai
from openai.embeddings_utils import distances_from_embeddings
from scraper import Scraper

class SemanticSearch:
    def __init__(self, num_levels: int = 2, first_level: int = 10, subseq: int = 2):
        self.num_levels = num_levels
        self.first_level = first_level
        self.subseq = subseq
        self.urls_to_embedding = {}
        self.model = "text-embedding-ada-002"
        self.scraper = Scraper(2)
        

    def get_closest_embedding(self, question: str, context: list(str)):
        embed_question, embeddings = self.get_embeds(question, context)
        distances = distances_from_embeddings(embed_question, embeddings, distance_metric="cosine")
        vals = zip(context, distances)
        vals = sorted(vals, key=self.sort_embeds)
        most_similar = []
        for txt, d in vals[:self.first_level]:
            ctx = self.get_subseq_embeds(txt)
            most_similar.append(ctx)
        return most_similar


    def get_embeds(self, question: str, context: list(str)):
        question_embed = openai.Embedding.create(input=[question], model=self.model)
        context_embed = openai.Embedding.create(input=context, model=self.model)
        return question_embed, context_embed


    def get_subseq_embeds(self, context: str):
        # for now - just search with the context itself. Later: maybe search based on unknown keywords and take the context around it as well
        urls, embeds = self.scraper.query(context)
        ctx, emb = self.get_embeds(context, embeds)
        distances = distances_from_embeddings(ctx, emb, distance_metric="cosine")
        vals = zip(urls, distances)
        vals = sorted(vals, key=self.sort_embeds)
        ret_ctx = context
        for txt,_ in vals[:self.subseq]: ret_ctx += "; " + txt;
        return ret_ctx
    
    
    def sort_embeds(self, val1, val2):
        if val1[1]<val2[1]: return -1;
        if val1[1]>val2[1]: return 1;
        else: return 0

