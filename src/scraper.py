import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List


class Scraper:

    def __init__(self, max_links: int = 1):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.links = []
        self.max_links = max_links
        self.url_cache = {}

    def query_parallel(self, questions: List[str]):
        result = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            result = executor.map(self.query, questions)
        result_map = {}
        for question, url, text in result:
            result_map[question] = (url, text)
        return result_map


    def query(self, question: str):
        print("test")
        self.search(question)
        text = self._get_link_text()
        urls = self.links
        #self.driver.close() # later close and reopen, setup pool for multiple connections
        return question, urls, text

    def reset(self):
        self.driver.close()
        self.links.clear()

    def search(self, question: str):
        self.driver.get(f"https://www.google.com/search?q={question}")
        results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
        self.links.clear()
        for result in results[:(min(len(results), self.max_links))]:
            link = result.find_element(By.TAG_NAME, "a")
            href = link.get_attribute("href")
            self.links.append(href)


    def _get_link_text(self):
        text = []
        for link in self.links:
            if link in self.url_cache.keys():
                for t in self.url_cache[link]:
                    text.append(t)
                continue

            self.url_cache[link] = []
            self.driver.get(link)
            linkText = re.split(r"(?<!^)\s*[.\n]+\s*(?!$)", "".join(self.driver.find_element(By.TAG_NAME, 'body').text))

            ret = []
            for txt in linkText.copy():
                if len(re.split(", |. |\n| ", txt))>=10: 
                    self.url_cache[link].append(txt)
                    ret.append(txt)
            
            for t in ret: text.append(t)
        return text