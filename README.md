## InternetGPT
> A simple python library that pairs web scraping along with chatgpt API calls to create chat clients that can access the internet easily without the restriction of no internet that chatgpt has

Uses OpenAI embeddings and chat completion to research through the internet, search up rare phrases, organize data, and create a smart prompt with context

**Installation**
`pip install --index-url https://test.pypi.org/simple/InternetGPT`

**Usage**
1. import Chat class
2. Add OpenAI Keys and other configurations (embedding and internet collection sizes)
3. Add or change a prompt to execute

**Todos:**
 * Testing:
   * Run individual prompt tests
   * Run functionality tests with OpenAI API - almost done 
 * Deployment:
   * Setup CI/CD  
   * Publish as python project
 * New Features (next dev cycle):
   * Redis/sqlite caching option
   * Rate limiting and other limits onto OpenAI models
   * Scraper multithreading - very important, COMPLETED
   * Multi-level recursive embedding search
   * Embedder multithreading if possible as well
   * Configuration for threshold of requiring searching up a word
   * System prompt embedding and search
 * Results for paper: compare recursive search (next dev cycle)

**Things for the paper:**
 * prompt engineering description
 * Overall architecture explanation
 * Caching embeddings
 * Sending multiple prompts
 * Providing the direct information for question answering
 * Do another example with open source version (e.g. BERT) to directly insert differentiable neural dictionary into the model