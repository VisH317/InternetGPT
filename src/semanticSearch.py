import openai
from openai.embeddings_utils import distances_from_embeddings
from scraper import Scraper
from recurseEmbeds import RecurseEmbeds
from typing import List
import logging
import tiktoken

"""
SemanticSearch: module for receiving query results from Scraper and evaluating importance based on distances from a desired question prompt (using openai.Embeddings API)

Functions
---------
sort_embeds(val1: tuple[str, embed], val2: tuple[str, embed]) [PRIVATE]
    Helper function used to sort text embedding tuples based on embedding distance

Classes
-------
SemanticSearch: main semantic search class
"""

#logging.basicConfig(filename="test.log", filemode="w", format='%(name)s - %(levelname)s - %(message)s')

def sort_embeds(val1, val2): # custom comparator function for sorting the embedding distances in a tuple to keep the links attached to them
    if val1[1]<val2[1]: return -1;
    if val1[1]>val2[1]: return 1;
    else: return 0

class SemanticSearch:

    """
    Semantic Search to work in tandem with the Chat class in order to sort and evaluate received context based on importance

    Attributes
    ----------
    num_levels: int (2)
        number of levels to recurse while providing context for words (currently inactive)
    first_level: int (1)
        The number of relevant context items to choose for the first recursive iteration
    subseq: int (1)
        The number of relevant context items to choose for subsequent recursive iterations
    
    Methods
    -------
    get_closest_embedding(question: str, context: List[str])
        compares context to distance using openai Embeddings and returns context for each individual relevant context based on the number selected from the most relevant
    get_embeds (question: str, context: List[str])
        creates calls to OpenAI API to receive the embedding values for the question and context
    """

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

