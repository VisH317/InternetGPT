import pytest
from src.scraper import Scraper

def test_query():
    s = Scraper()
    res = s.query("What is jalapenos?")
    return res