import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List


class Scraper:
    def __init__(self, max_links: int = 1, min_text_size: int = 10):
        
        self.max_links = max_links # the max amount of links to be chosen for a specific query
        self.url_cache = {} # url cache in memory dictionary to prevent extracting text from the same webpage multiple times
        self.min_text_size = min_text_size


    def create_chrome_driver(self):
        chrome_options = Options() # create a chrome options object, these options increase speed
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) # return the webdriver installed through the chromedrivermanager and the provided options


    def query_parallel(self, questions: List[str]):
        result = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            result = executor.map(self.query, questions) # runs a query for each question in the provided list
        result_map = {} 
        for question, url, text in result:
            result_map[question] = (url, text)
        return result_map # returns map of question -> (urls and corresponding text)


    def query(self, question: str):
        driver = self.create_chrome_driver() # create a driver for the specific thread
        links = self.search(question, driver) # get links from the search function
        text = self._get_link_text(links) # extract text from each link
        driver.quit() # end the selenium session
        return question, links, text  # return questions, links, and text for

    def search(self, question: str, driver):
        driver.get(f"https://www.google.com/search?q={question}") # create a google search with the corresponding question
        results = driver.find_elements(By.CSS_SELECTOR, "div.g") # get all of the search result containers (div.g selector)
        links = []
        for result in results[:(min(len(results), self.max_links))]:
            link = result.find_element(By.TAG_NAME, "a") # extract the link from each container and add the href pointer to the array
            href = link.get_attribute("href")
            links.append(href)
        return links # return the list of hrefs


    def _get_link_text(self, links: List[str]):
        text = []
        with ThreadPoolExecutor(max_workers=4) as executor: # multiple threads to run each text extraction process in parallel
            text = executor.map(self._get_text, links)
        ret = []
        for i in text: ret = [*ret, *text[i]] # takes all the nested lists and converts to one list
        return ret

    
    def _get_text(self, link):
        text = []
        if link in self.url_cache.keys(): # checks if the URL is in the cache and adds if it is
            for t in self.url_cache[link]:
                text.append(t)
            return text

        self.url_cache[link] = [] # creates a url cache entry 
        driver = self.create_chrome_driver() # creates a new driver for the task
        driver.get(link) # fetch the link provided by the function argument
        linkText = re.split(r"(?<!^)\s*[.\n]+\s*(?!$)", "".join(driver.find_element(By.TAG_NAME, 'body').text)) # extract all the text on the page and split by common end of sentence or new line separators

        ret = []
        for txt in linkText.copy():
            if len(re.split(", |. |\n| ", txt))>=self.min_text_size: # only appends to returned list if the actual piece of information is greater than 10 entities/words
                self.url_cache[link].append(txt)
                ret.append(txt)
        
        for t in ret: text.append(t)
        driver.quit()
        return text # returns all the extracted and separated text