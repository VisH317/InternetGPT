import openai
from openai.embeddings_utils import distances_from_embeddings
from scraper import Scraper
from recurseEmbeds import RecurseEmbeds
from typing import List
import logging
import tiktoken

#logging.basicConfig(filename="test.log", filemode="w", format='%(name)s - %(levelname)s - %(message)s')

def sort_embeds(val1, val2): # custom comparator function for sorting the embedding distances in a tuple to keep the links attached to them
    if val1[1]<val2[1]: return -1;
    if val1[1]>val2[1]: return 1;
    else: return 0

class SemanticSearch:
    def __init__(self, num_levels: int = 2, first_level: int = 1, subseq: int = 1):
        self.num_levels = num_levels # number of levels to recurse while providing context for words
        self.first_level = first_level # number of context items to choose from the list of the most relevant in the first level
        self.subseq = subseq # number of context items to choose in subsequent searches
        self.urls_to_embedding = {}
        self.model = "text-embedding-ada-002" # sets the embedding model used for openai
        self.scraper = Scraper(2) # creates a scraper object
        self.recurse = RecurseEmbeds(subseq) # recurse embed object to get deeper context
        self.tokenizer = tiktoken.get_encoding("cl100k_base") # text tokenizer (required for input to embedding)
        

    def get_closest_embedding(self, question: str, context: List[str]):
        embed_question, embeddings = self.get_embeds(question, context) # receive the question and context embeddings
        distances = distances_from_embeddings(embed_question, embeddings, distance_metric="cosine") # compute distances from the context to the desired question embedding
        vals = zip(context, distances) 
        vals = sorted(vals, key=lambda val: val[1]) 
        most_similar = []
        for txt, d in vals[:self.first_level]:
            ctx = self.recurse.get_subseq_embeds(txt, context) # for the most relevant context: search subsequent embeddings and append to most_similar
        most_similar.append((txt, ctx)) # append the relevant contexts for each
        return most_similar


    def get_embeds(self, question: str, context: List[str]):
        newcontext = []
        for c in context: newcontext.append(self.tokenizer.encode(c)) # tokenize all the context words and put into a new list
        question_embed = openai.Embedding.create(input=[self.tokenizer.encode(question)], engine=self.model)["data"] # receive the embedding for the question
        context_embed = openai.Embedding.create(input=newcontext, engine=self.model)["data"] # receive the embedding for all the context
        ctx = []
        for c in context_embed: ctx.append(c['embedding'])
        
        return question_embed[0]["embedding"], ctx # return the embeddings

