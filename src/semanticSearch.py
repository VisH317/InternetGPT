import openai
from openai.embeddings_utils import distances_from_embeddings
from scraper import Scraper
from recurseEmbeds import RecurseEmbeds
from typing import List
import logging
import tiktoken

logging.basicConfig(filename="test.log", filemode="w", format='%(name)s - %(levelname)s - %(message)s')

def sort_embeds(val1, val2):
    if val1[1]<val2[1]: return -1;
    if val1[1]>val2[1]: return 1;
    else: return 0

class SemanticSearch:
    def __init__(self, num_levels: int = 2, first_level: int = 1, subseq: int = 1):
        self.num_levels = num_levels
        self.first_level = first_level
        self.subseq = subseq
        self.urls_to_embedding = {}
        self.model = "text-embedding-ada-002"
        self.scraper = Scraper(2)
        self.recurse = RecurseEmbeds(subseq)
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        

    def get_closest_embedding(self, question: str, context: List[str]):
        embed_question, embeddings = self.get_embeds(question, context)
        distances = distances_from_embeddings(embed_question, embeddings, distance_metric="cosine")
        vals = zip(context, distances)
        vals = sorted(vals, key=lambda val: val[1])
        most_similar = []
        for txt, d in vals[:self.first_level]:
            ctx = self.recurse.get_subseq_embeds(txt, context)
            most_similar.append(ctx)
        return most_similar


    def get_embeds(self, question: str, context: List[str]):
        newcontext = []
        for c in context: newcontext.append(self.tokenizer.encode(c))
        question_embed = openai.Embedding.create(input=[self.tokenizer.encode(question)], engine=self.model)["data"]
        context_embed = openai.Embedding.create(input=newcontext, engine=self.model)["data"]
        ctx = []
        for c in context_embed: ctx.append(c['embedding'])
        logging.info(context_embed)
        logging.info(question_embed)
        # print("CONTEXT: ",context_embed)
        # print("QUESTION: ", question_embed)
        return question_embed[0]["embedding"], ctx

