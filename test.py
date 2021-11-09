import Algorithmia
import numpy as np
import itertools

# Fill in with search terms
search_terms = [
    "python programmer", 
    "data analyst"] 
# Fill in with locations
locations = np.array([
    "New York, NY", 
    "San Francisco, CA"]) 
# Tuples of every permutation of search term and location (in that order) 
search_arr = list(itertools.product(search_terms, locations))
# Num pages to go through for every location and search term
pages = 5

for i in range(len(search_arr)):
    curr_search = search_terms[i] # should be a tuple
    for j in range(pages):
        input = {
            "search_terms": curr_search[0],
            "location": curr_search[1],
            "page": str(j) # all terms must be be strings
        }
        client = Algorithmia.client('simWhdQfGBL0kvg7doa4TNhwrz91')
        algo = client.algo('specrom/Extract_From_Indeed_Job_Scraper/0.2.0')
        algo.set_options(timeout=300) # optional timeout
        print(algo.pipe(input).result)

