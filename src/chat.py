import openai

import openai
from openai.embeddings_utils import distances_from_embeddings
from scraper import Scraper
from multiprocessing import Process

class Chat:
    def __init__(self, openai_key, additional_prompt: str):
        self.scraper = Scraper
        openai.api_key = openai_key
        self.add_prompt = additional_prompt
        self.urls = {}
        self.current_requests = 0


    def query(self, question: str, max_similar: int):
        urls, embeddings = self.scraper.query(question)
        for url, embed in zip(urls, embeddings): self.urls[url] = embed
        embed_question = openai.Embedding.create(input=question, model="text-embedding-ada-002")
        similar = self._get_closest_embedding(embeddings, embed_question, max_similar)
        context = "\n\n###\n\n".join(similar)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant who will complete the following task based on{ a provided context and input. If the solution to the task based on the input is not within the context, answer using your own knowledge. The context includes ten sequences of words separated by ###."},
                {"role": "user", "content": f"Input: {question}.\nContext: {context}"}
            ],
            temperature=0.35,
            max_tokens=25
        )
        return response


    def _get_closest_embedding(self, embeddings, embed_question, max_similar):
        distances = distances_from_embeddings(embed_question, self.urls.values(), distance_metric="cosine")
        distances.sort()
        most_similar = []
        for idx, d, in enumerate(distances[:max_similar]):
            most_similar.append(embeddings[idx])
        return most_similar
    
    def change_prompt(self, prompt: str):
        self.add_prompt = prompt

    def get_url_embeddings(self):
        return self.urls