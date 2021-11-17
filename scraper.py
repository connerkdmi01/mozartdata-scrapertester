import requests
from bs4 import BeautifulSoup
import pandas as pd

# PERSONAL TIP: use py not python (this is 3.9)
# 3 parts: extract, transform, load

def get_proxies():
    res = requests.get('https://free-proxy-list.net/', headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'})
    soup = BeautifulSoup(res.text,"lxml")

    for items in soup.select("#proxylisttable tbody tr"):
        proxy_list = ':'.join([item.text for item in items.select("td")[:2]])
    return proxy_list

def extract(search, location, page):
    # set headers (user agent)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    # Indeed url iterates by page, can modify in url as shown below
    # Pages are 0, 10, 20...
    url = "https://www.indeed.com/jobs?q={s}&l={l}&start={p}".format(s = search, p = page*10, l = location)
    # use requests to get url
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

# currently transforms to find job and company
def transform(soup):
    # tried ('div', class_ = 'jobsearch-SerpJobCard') but seems outdated
    # tried ('table', class_ = 'jobCard_mainContent') but not close enough to the job titles
    company_raw = soup.find_all('td', class_ = 'resultContent')
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
                'location': location
            }
            jobs.append(job)

jobs = []
def main():
    print(get_proxies())
    searches = ['python+developer']
    locations = ['San+Francisco+Bay+Area%2C+CA', 'New+York%2C+NY', 'Austin%2C+TX']
    pages = 1
    for loc in locations:
        for search in searches:
            for i in range(1):
                print('DEBUG: searching page {p} of {s} jobs in {l}'.format(p = i, s = search, l = loc))
                c = transform(extract(search, loc, i))
    print(jobs)
    df = pd.DataFrame(joblist)
    print(df.head())
    df.to_csv('jobs.csv')

if __name__ == "__main__":
    main()