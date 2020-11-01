# Web-Crawler-Basic
A simple web crawler using HTML link tags, with Breadth First Search Implemented.

# Idea:
Each website has various other websites linked to it and each one also links to some local or external websites. Visually speaking, it looks like a graph of **nodes** and **arcs**, where nodes represent the distinguish websites and arcs represent the link or relationship between two websites.

We can use a `Breadth First Search(BFS)` to search through the graph. BFS means for each node, we will go through all its child nodes before reaching to the next level. Commonly, BFS is implemented by a queue and I have used a `deque` data structure in Python for implementation.


# Step-by-step intro:
``` python
# Reference: https://www.freecodecamp.org/news/how-to-build-a-url-crawler-to-map-a-website-using-python-6a287be1da11/
# Reference: https://pythonprogramming.net/introduction-scraping-parsing-beautiful-soup-tutorial/
# External libraries used: BeautifulSoup, requests, urllib.
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlsplit
```
In this program, the external library we used are:
* BeautifulSoup: parse the HTML file fetched from the url with the help of `lxml` parser
* requests: Check for broken urls using `requests.exceptions` module and fetch response
* urllib: open url and split the url into parts

``` python
from collections import deque

ini_url = "https://news.ycombinator.com/"

# A queue of the unvisited urls
url_q = deque([ini_url])
``` 

I used a `deque` data structure to implement a queue which will store the urls that are waited to be visited. We first enqueue the initial url.

``` python
# Sets of visited, unvisited and broken urls
vis_url = set()
child_url = set()
broken_url = set()
```

Set up three sets to store urls in different status, we use set because we do not want to visit the same url twice:
* `vis_url`: the visited url set, once we have visited 100 urls, we will halt the program.
* `child_url`: a temperary set stores the children of a particular url 
* `broken_url`: the url which are broken and have been catched by the `request.exceptions` module.

``` python
# Start BFS the queue
while len(url_q) and len(vis_url) < 100:
    url = url_q.popleft()
    vis_url.add(url)
    child_url = set()
    print("Processing url {}: {}".format(len(vis_url), url))
    ...
```
We start doing the BFS operations on the queue by pop the front item of queue and add it into the visited set `vis_url`, this item is the url we are going to work on. In order to improve the efficiency of the codes, we will empty the `child_url` set evertime when we are operating on a new url.

``` python
    ...
    # An try-except code block to catch all the broken urls
    try:
        response = requests.get(url)
    except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
        broken_url.add(url)
        print("Warning: A broken url")
        continue
    ...
```
This is a `try-except` block to catch the broken urls, in this way, when we are processing the urls, `BeautifulSoup` will be notified and will stop processing the broken urls.

``` python
    ...
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
    ...
```
This block of code splits the url into various parts, the part we are interested in is the domain of the url. We also set up the `strip_domain` and `base_url` for later use when formatting the child urls.

``` python
    ...
    # Initialise BeautifulSoup to process the HTML document
    # if the response is an error message, BS will not attempt to open it
    soup = BeautifulSoup(response.text, "lxml")
    ...
```

`BeautifulSoup` is initialised to process the HTML document, we utilise the response message from the `try-catch` block to make sure the broken urls are not been processed.

``` python
    ...
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
            child_url.add(new_url)
        elif strip_domain in anchor:
            # if the anchor contains the url, then it is a local url
            child_url.add(anchor)
        elif not anchor.startswith('http'):
            # not a foreign link
            new_url = path + anchor
            child_url.add(new_url)
        else:
            # a foreign link
            child_url.add(anchor)
    ...
```
We iterate through all the children of the current url and form a fully qualified url based on their conditions.

``` python
    ...
    for link in child_url:
        # if we have not visited and added the link to the queue, then add the link to the queue
        if (link not in url_q) and (link not in vis_url):
            url_q.append(link)
    ...
```
For each link in the `child_url`, make sure none of them have been visited before and none of them are currently in the queue. This helps us to avoid having infinite loops in the program.

``` python
print("Visited {} urls, Simple Web Crawler Job done!".format(len(vis_url)))
```
Print the statement to inform the users that the job is done.
