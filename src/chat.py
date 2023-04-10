import openai

import os
import openai
from openai.embeddings_utils import distances_from_embeddings
from scraper import Scraper
from multiprocessing import Process
from semanticSearch import SemanticSearch
from dotenv import load_dotenv

load_dotenv("../.env")

"""
ChatGPT prompts with context found through a smart recursive search that ranks words based on rarity/importance and evaluates all information gained using the OpenAI embeddings API

Classes:
    Chat
"""


class Chat:

    """
    Executor for ChatGPT prompts with augmented internet search and evaluation for defining rare words and comparing collected information

    Initialization Params
    ---------------------
    prompt: str
        The initial system prompt of the ChatGPT instance, defines the objective of the ChatGPT instance
    key: str
        OpenAI API key (REQUIRED)
    num_levels: int (2)
        The number of levels to recurse when searching for information in prompts (currently only supports 2 and has no effect, multi-level recursive searching will be implemented in the future)
    first_level: int (10)
        The number of context prompts to select from a search
    subseq: int (2)
        The number of context entries to add to the overall context in the prompt for each subsequent search after the main one (first_level)
    temperature: float (0.35)
        Corresponds to OpenAI API ChatCompletion temperature
    max_tokens: int (25)
        Corresponds to OpenAI API ChatCompletion max tokens

    Attributes
    ----------
    scraper: Scraper
        scraper instance to do the initial search for the provided question/user prompt
    prompt: str
        current system prompt that the ChatGPT instance will answer based on
    ss: SemanticSearch
        semantic search module to embed and evalute text entries
    temperature: float
        corresponds to instance variable
    max_tokens: int
        corresponds to instance variable

    Methods
    -------
    query(question: str)
        uses ChatCompletion + internet search and evaluation to answer a user prompt based on the provided system prompt during initialization
    get_context(question: str)
        same as query method but does not answer the question and returns the scraped and sorted entries relating to the user prompt
    change_prompt(prompt: str)
        change the current system prompt
    """

    def __init__(self, prompt: str, key: str, num_levels: int = 2, first_level: int = 10, subseq: int = 2, temperature=0.35, max_tokens=25):
        self.scraper = Scraper()
        print("scraper initialized")
        openai.api_key = key
        self.prompt = prompt
        self.ss = SemanticSearch(num_levels, first_level, subseq)

        self.temperature = temperature
        self.max_tokens = max_tokens


    def query(self, question: str):
        q, urls, context = self.scraper.query(question)
        context = self.ss.get_closest_embedding(question, context)
        for i in context: context[i] = "\n\n".join([context[i][0], *context[i][1]])
        context = "\n\n###\n\n".join(context)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are an assistant who will complete the following task based on a provided context and input. If the solution to the task based on the input is not within the context, answer using your own knowledge. The context includes ten sequences of words separated by ###. Task: {self.prompt}"},
                {"role": "user", "content": f"Input: {question}.\nContext: {context}"}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response
    
    def get_context(self, question: str):
        q, urls, context = self.scraper.query(question)
        return self.ss.get_closest_embedding(question, context)

    
    def change_prompt(self, prompt: str):
        self.prompt = prompt

