## InternetGPT
_Idea:_ a simple python library that pairs web scraping along with chatgpt API calls to create chat clients that can access the internet easily without the restriction of no internet that chatgpt has

**Requirements:**
 * ChatGPT API to call and respond based on the input question
 * Web Scraper to get data:
   * Can be done with selenium, going onto google and extracting the top 5 web results for a question and scraping the pages
   * Take the text points on that page and embed them
   * Take embeddings with least distance to the input question and pass them through the assistant

**Todos:**
 * Setup frontend for demo
 * Publish as a package
 * Brainstorm new features
   * security rate limiters?
 * setup testing framework to run on