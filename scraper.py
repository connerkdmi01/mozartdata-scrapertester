import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# PERSONAL TIP: use py not python (this is 3.9)
# 3 parts: extract, transform, load

# global jobs list, contains dictionaries of jobs
jobs = []
# proxies that will automatically rotate with each access
proxy_list = {
    "http": "http://ykvgvroz-rotate:9rhpmcjoqup7@p.webshare.io:80/",
    "https": "http://ykvgvroz-rotate:9rhpmcjoqup7@p.webshare.io:80/"
}

def extract(search, location, limit, radius, age, page):
    # set headers (user agent)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    # Indeed url iterates by page, can modify in url as shown below
    # Pages are dependent on how many results per page
    url = "https://www.indeed.com/jobs?q={s}&l={l}&limit={li}&radius={r}&fromage={a}&start={p}".format(s=search, l=location, li=limit, r=radius, a=age, p=page*limit)
    # use requests to get url
    r = requests.get(url, headers, proxies=proxy_list)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup, search_job, search_location):
    # tried ('div', class_ = 'jobsearch-SerpJobCard') but seems outdated
    # tried ('table', class_ = 'jobCard_mainContent') but not close enough to the job titles
    company_raw = soup.find_all('td', class_ = 'resultContent')
    print('{e} entries found on this page'.format(e=len(company_raw)))
    company_arr = []
    for item in company_raw:
        title = item.find('div', class_ = 'heading4 color-text-primary singleLineTitle tapItem-gutter').find('h2', class_ = 'jobTitle').find('span').text.strip()
        # for some reason Indeed web designers like to reuse 
        # jobTitle headers to indicate if a job is new, this filters that out
        if title != 'new':
            company = item.find('div', class_ = 'heading6 company_location tapItem-gutter').find('span').text.strip()
            location = item.find('div', class_ = 'heading6 company_location tapItem-gutter').find('div', class_ = 'companyLocation').text.strip()
            job = {
                'title': title,
                'company': company,
                'location': location,
                'search_job': search_job,
                'search_location': search_location
            }
            print('found {t} at {c} at {l}'.format(t=title, c=company, l=location))
            jobs.append(job)

def load():
    searches = ['Data+Engineer',
                'Data+Analyst',
                'Infrastructure',
                'CIO',
                'AI',
                'Machine+Learning']
    locations = ['San+Francisco+Bay+Area%2C+CA', 
                 'San+Diego%2C+CA',
                 'Los+Angeles%2C+CA',
                 'New+York%2C+NY', 
                 'Austin%2C+TX',
                 'Seattle%2C+WA',
                 'Denver%2C+CO',
                 'Boston%2C+MA',
                 ]
    # searches = ['Data+Engineer']
    # locations = ['San+Francisco+Bay+Area%2C+CA', 
    #              'San+Diego%2C+CA']
    limit = 50 # no. results per page (50 is max)
    radius = 50 # no. miles around location
    age = 15 # no. days since job was posted
    pages = 1 # no. pages to search for each search/loc pair
    sleep = 30 # seconds between each request
    total = len(locations) * len(searches) * pages # number of searches to do
    count = 0 # number of searches done
    remaining = len(locations) * len(searches) * pages 
    search_avg = 0
    for loc in locations:
        for search in searches:
            for i in range(pages):
                print('searching page {p} of {s} jobs in {l}'.format(p = i + 1, s = search, l = loc))
                
                tic = time.perf_counter()
                c = transform(extract(search, loc, limit, radius, age, i), search, loc)
                toc = time.perf_counter()
                search_avg = (search_avg * count + toc - tic) / (count + 1)
                
                count += 1
                print('approximately {t} left'.format(t=str(datetime.timedelta(seconds = (total - count) * (sleep + search_avg)))))
                print('searchtime average is: {t} seconds'.format(t=search_avg))
                for j in reversed(range(sleep)):
                    if count != total: # doesn't sleep on the last search, saves a sleep cycle
                        if (j + 1) % 5 == 0:
                            print("sleeping {s}".format(s = j + 1))
                        time.sleep(1)
                
    print(jobs)
    df = pd.DataFrame(jobs)
    print(df.head())
    df.to_csv('jobs.csv')
    
def main():
    load()
    

if __name__ == "__main__":
    main()