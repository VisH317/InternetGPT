import openai

import openai
from openai.embeddings_utils import distances_from_embeddings
from scraper import Scraper
from multiprocessing import Process
from semanticSearch import SemanticSearch

class Chat:
    def __init__(self, openai_key, additional_prompt: str, num_levels: int = 2, first_level: int = 10, subseq: int = 2):
        self.scraper = Scraper
        openai.api_key = openai_key
        self.add_prompt = additional_prompt
        self.current_requests = 0
        self.ss = SemanticSearch(num_levels, first_level, subseq)


    def query(self, question: str):
        urls, context = self.scraper.query(question)
        context = "\n\n###\n\n".join(self.ss.get_closest_embedding(question, context))
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are an assistant who will complete the following task based on a provided context and input. If the solution to the task based on the input is not within the context, answer using your own knowledge. The context includes ten sequences of words separated by ###. Task: {self.add_prompt}"},
                {"role": "user", "content": f"Input: {question}.\nContext: {context}"}
            ],
            temperature=0.35,
            max_tokens=25
        )
        return response

    
    def change_prompt(self, prompt: str):
        self.add_prompt = prompt

