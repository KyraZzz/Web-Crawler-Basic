# Reference: https://www.freecodecamp.org/news/how-to-build-a-url-crawler-to-map-a-website-using-python-6a287be1da11/
# Reference: https://pythonprogramming.net/introduction-scraping-parsing-beautiful-soup-tutorial/
# External libraries used: BeautifulSoup, requests, urllib.

# Idea: Breadth first search implementing using queue data structure

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlsplit
from collections import deque

ini_url = "https://news.ycombinator.com/"

# A queue of the unvisited urls
url_q = deque([ini_url])

# A set of visited urls
vis_url = set()
unvis_url = set()
broken_url = set()

# Start BFS the queue
while len(url_q) and len(vis_url) < 100:
    url = url_q.popleft()
    vis_url.add(url)
    print("Processing url {}: {}".format(len(vis_url), url))

    # An try-except code block to catch all the broken urls
    try:
        response = requests.get(url)
    except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
        broken_url.add(url)
        print("Warning: A broken url")
        continue

    # A url has parts: scheme(protocols) + domain_name + file_path
    # SplitResult(scheme='https', netloc='news.ycombinator.com', path='/', query='', fragment='')
    parts = urlsplit(url)

    # Get the domain name
    domain = parts.netloc
    # Make sure the subdomain is stripped off
    strip_domain = domain.replace("www.", "")
    # base_url: https://news.ycombinator.com
    base_url = "{}://{}".format(parts.scheme, parts.netloc)

    # path: https://news.ycombinator.com/
    if '/' in parts.path:
        path = url[:url.rfind('/')+1]
    else:
        path = url

    # Initialise BeautifulSoup to process the HTML document
    # if the response is an error message, BS will not attempt to open it
    soup = BeautifulSoup(response.text, "lxml")

    # Iterate through each anchor found in the HTML document
    # link example: <a href="">text</a>
    for link in soup.find_all('a'):
        # set anchor as the href attribute in the tag
        if "href" in link.attrs:
            anchor = link.attrs["href"]
        else:
            anchor = ""
        # form a url using anchor and the following conditions
        if anchor.startswith('/'):
            # a url points to a file within the website
            new_url = base_url + anchor
            unvis_url.add(new_url)
        elif strip_domain in anchor:
            # if the anchor contains the url, then it is a local url
            unvis_url.add(anchor)
        elif not anchor.startswith('http'):
            # not a foreign link
            new_url = path + anchor
            unvis_url.add(new_url)
        else:
            # a foreign link
            unvis_url.add(anchor)
    for link in unvis_url:
        # if we have not visited and added the link to the queue, then add the link to the queue
        if (link not in url_q) and (link not in vis_url):
            url_q.append(link)
print("Visited {} urls, Simple Web Crawler Job done!".format(len(vis_url)))
