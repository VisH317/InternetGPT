import pytest
from chat import Chat
import logging

logging.basicConfig(filename="test.log", filemode="w", format='%(name)s - %(levelname)s - %(message)s')

def test_e2e():
    print("creating chat class")
    c = Chat("Answer the questions in the following prompts using the provided context")
    print("querying chat")
    res = c.query("What is the difference between a meme and a traditional joke")
    print(res)
    logging.info(res)
    return res

if __name__=="__main__":
    test_e2e()