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
 * Setup augmented memory to pass into model
 * SQLite database to save extracted text and urls
 * multithreading for more requests

**Next Cycle Todos:**
 * Write tests - DONE
 * Caching, Multiprocessing for requests, recursive search based on unknown keywords - DONE except for multiprocessing, prob not required 

**Dev Cycle 3 Todos:**
 * Testing:
   * Run individual prompt tests
   * Run functionality tests with OpenAI API - almost done 
 * Deployment:
   * Setup CI/CD  
   * Publish as python project
 * New Features (next dev cycle):
   * Redis/sqlite caching option
   * Rate limiting and other limits onto OpenAI models
   * Scraper multithreading
   * Configuration for threshold of requiring searching up a word
 * Results for paper: compare recursive search (next dev cycle)

**Things for the paper:**
 * prompt engineering description
 * Overall architecture explanation
 * Caching embeddings
 * Sending multiple prompts
 * Providing the direct information for question answering
 * Do another example with open source version (e.g. BERT) to directly insert differentiable neural dictionary into the model