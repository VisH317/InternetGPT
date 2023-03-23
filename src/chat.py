import openai

import openai
from openai.embeddings_utils import distances_from_embeddings
from scraper import Scraper

class Chat:
    def __init__(self):
        self.scraper = Scraper


    def query(self, question: str):
        embeddings = self.scraper.query(question)
        embed_question = openai.Embedding.create(input=question, model="text-embedding-ada-002")
        similar = self.get_closest_embedding(embeddings, embed_question)
        context = "\n###\n".join(similar)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            prompt=f"You are a question answering agent that will answer a question based on the following context provided. If the answer to the question is not within the context, answer using your own knowledge. The context includes ten sequences of words separated by ###. Context: {context}, Question: {question}",
            temperature=0.35,
            max_tokens=25
        )
        return response


    def get_closest_embedding(self, embeddings, embed_question):
        distances = distances_from_embeddings(embed_question, embeddings, distance_metric="cosine")
        distances.sort()
        most_similar = []
        for idx, d, in enumerate(distances):
            most_similar.append(embeddings[idx])
        return most_similar
