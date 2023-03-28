import pytest
import time
from src.scraper import Scraper

def test_query():
    s = Scraper()
    res = s.query("What is jalapenos?")
    assert len(res)>0

def test_scraper_split():
    s = Scraper()
    res = s.query("What is a test?")
    ret = True
    for r in res:
        if "." in r or "\n" in r: ret = False
    assert ret

def test_in_memory_scraper_cache():
    s = Scraper()
    res = s.query("What is cache?")
    start = time.time()
    res2 = s.query("What is cache?")
    end = time.time()
    elapsed = end - start
    assert elapsed<1000

def test_scraper_multithreading():
    # will be implemented once multithreading for scraper is complete
    pass