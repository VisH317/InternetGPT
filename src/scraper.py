import urllib.parse as parse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def search(self, question: str):
        self.driver.get(f"https://www.google.com/search?q={question}")
        results = self.driver.find_elements_by_css_selector("div.g")
        self.links = []
        for result in results:
            link = result.find_element_by_tag_name("a")
            href = link.get_attribute("href")
            self.links.append(parse.parse_qs(parse.urlparse(href).query)['q'][0])