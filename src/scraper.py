import openai
import urllib.parse as parse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Scraper:

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.links = []
        self.text = []


    def query(self, question: str):
        self.search(question)
        self._get_link_text()
        results = self._get_embeddings(self)
        self.reset()
        return results


    def reset(self):
        self.driver.close()
        self.links.clear()
        self.text.clear()

    def search(self, question: str):
        self.driver.get(f"https://www.google.com/search?q={question}")
        results = self.driver.find_elements_by_css_selector("div.g")
        self.links.clear()
        for result in results:
            link = result.find_element_by_tag_name("a")
            href = link.get_attribute("href")
            self.links.append(parse.parse_qs(parse.urlparse(href).query)['q'][0])


    def _get_link_text(self):
        self.text.clear()
        for link in self.links:
            self.driver.get(link)
            linkText = self.driver.find_element_by_tag_name('body').text.split(".").split("\n")
            for t in linkText: self.text.append(t)
    

    def _get_embeddings(self):
        ret = []
        for text in self.text:
            ret.append(openai.Embeddings.create(input=[text], model="text-embedding-ada-002")["data"[0]["embedding"]])  
        return ret