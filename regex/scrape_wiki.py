from bs4 import BeautifulSoup
import requests
from collections import deque
import json
 
def scrape_wiki(start_url, max_links_to_explore):
    response = requests.get(url=start_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    to_return = {}

    # find all of the links
    all_links = soup.find_all("a", href=True)
    link_number = len(all_links)

    to_return[response.content] = link_number
    stack = deque()
    stack.extend(all_links)

    total_links_traversed = 0

    while total_links_traversed < max_links_to_explore:
        link = stack.pop()

        # should really make this more robust
        try:
            response = requests.get(url="https://en.wikipedia.org" + link['href'])
            soup = BeautifulSoup(response.content, 'html.parser')
        except:
            continue

        # Only want other wiki articles (to not run into scraping problems)
        if link['href'].find("/wiki/") == -1: 
            continue

        all_links = soup.find_all("a", href=True)
        link_number = len(all_links)
        to_return[response.content] = link_number
        stack.extendleft(all_links)
        

        total_links_traversed += 1


    return to_return


max_search = 10
result = scrape_wiki("https://en.wikipedia.org/wiki/Web_scraping", max_search)


final = {"train": {"inputs": [],"outputs":[]}, "test": {"inputs":[], "outputs":[]}}

result_keys = list(result.keys())
for i in range(0,len(result_keys)-1,2):
    final["train"]["inputs"].append(str(result_keys[i]))
    final["train"]["outputs"].append(result[result_keys[i]])

    final["test"]["outputs"].append(str(result_keys[i+1]))
    final["test"]["outputs"].append(result[result_keys[i+1]])

with open('WikiData.json', 'w') as outfile:
    # need to fix the bytes -> str -> json conversion
    json.dump(final, outfile)

print("Done")
