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

# Result of this example:
```python
Processing url 1: https://news.ycombinator.com/
Processing url 2: https://news.ycombinator.com/jobs
Processing url 3: https://news.ycombinator.com/user?id=schedutron
Processing url 4: https://news.ycombinator.com/bookmarklet.html
Processing url 5: https://news.ycombinator.com/from?site=onlywei.github.io
Processing url 6: https://news.ycombinator.com/from?site=x86.lol
Processing url 7: https://news.ycombinator.com/hide?id=24959519&goto=news
Processing url 8: https://news.ycombinator.com/hide?id=24950018&goto=news
Processing url 9: https://news.ycombinator.com
Processing url 10: https://news.ycombinator.com/vote?id=24960948&how=up&goto=news
Processing url 11: https://news.ycombinator.com/item?id=24958504
Processing url 12: https://github.com/HackerNews/API
Processing url 13: https://news.ycombinator.com/user?id=nanomonkey
Processing url 14: https://news.ycombinator.com/user?id=jwmhjwmh
Processing url 15: https://news.ycombinator.com/item?id=24959947
Processing url 16: https://news.ycombinator.com/vote?id=24961342&how=up&goto=news
Processing url 17: https://news.ycombinator.com/from?site=streetwriters.co
Processing url 18: https://news.ycombinator.com/item?id=24959588
Processing url 19: https://news.ycombinator.com/newcomments
Processing url 20: https://www.nngroup.com/articles/ux-gains-shrinking/
Processing url 21: https://gist.github.com/erincandescent/8a10eeeea1918ee4f9d9982f7618ef68
Processing url 22: https://news.ycombinator.com/item?id=24957783
Processing url 23: https://science.sciencemag.org/content/370/6516/530
Processing url 24: https://news.ycombinator.com/user?id=cwaffles
Processing url 25: https://news.ycombinator.com/user?id=krizhanovsky
Processing url 26: https://news.ycombinator.com/item?id=24957727
Processing url 27: https://news.ycombinator.com/security.html
Processing url 28: https://news.ycombinator.com/user?id=quyleanh
Processing url 29: https://news.ycombinator.com/hide?id=24950777&goto=news
Processing url 30: https://news.ycombinator.com/item?id=24950777
Processing url 31: https://news.ycombinator.com/item?id=24960108
Processing url 32: https://news.ycombinator.com/vote?id=24958725&how=up&goto=news
Processing url 33: https://news.ycombinator.com/hide?id=24960994&goto=news
Processing url 34: https://news.ycombinator.com/from?site=the-scientist.com
Processing url 35: https://github.com/mitmproxy/mitmproxy/releases/tag/v5.3.0
Processing url 36: https://news.ycombinator.com/from?site=eclecticlight.co
Processing url 37: https://news.ycombinator.com/vote?id=24958558&how=up&goto=news
Processing url 38: https://news.ycombinator.com/vote?id=24949335&how=up&goto=news
Processing url 39: https://news.ycombinator.com/hide?id=24949542&goto=news
Processing url 40: https://news.ycombinator.com/user?id=ingve
Processing url 41: https://news.ycombinator.com/hide?id=24959897&goto=news
Processing url 42: https://news.ycombinator.com/user?id=eitland
Processing url 43: https://blog.streetwriters.co/overcoming-writers-block/
Processing url 44: https://news.ycombinator.com/hide?id=24957280&goto=news
Processing url 45: https://news.ycombinator.com/user?id=panda17
Processing url 46: https://news.ycombinator.com/vote?id=24949736&how=up&goto=news
Processing url 47: https://news.ycombinator.com/user?id=reddotX
Processing url 48: https://news.ycombinator.com/from?site=probablydance.com
Processing url 49: https://news.ycombinator.com/user?id=benkoller
Processing url 50: https://news.ycombinator.com/from?site=orwellfoundation.com
Processing url 51: https://news.ycombinator.com/vote?id=24958392&how=up&goto=news
Processing url 52: https://news.ycombinator.com/user?id=XzetaU8
Processing url 53: https://news.ycombinator.com/vote?id=24957727&how=up&goto=news
Processing url 54: https://news.ycombinator.com/from?site=electrospaces.net
Processing url 55: https://netflixtechblog.com/netflix-android-and-ios-studio-apps-kotlin-multiplatform-d6d4d8d25d23
Processing url 56: https://news.ycombinator.com/newsfaq.html
Processing url 57: https://news.ycombinator.com/login?goto=news
Processing url 58: https://news.ycombinator.com/from?site=maiot.io
Processing url 59: https://news.ycombinator.com/hide?id=24959238&goto=news
Processing url 60: https://news.ycombinator.com/hide?id=24949335&goto=news
Processing url 61: https://news.ycombinator.com/submit
Processing url 62: https://news.ycombinator.com/from?site=netflixtechblog.com
Processing url 63: https://news.ycombinator.com/from?site=wisc.edu
Processing url 64: https://news.ycombinator.com/item?id=24959408
Processing url 65: https://news.ycombinator.com/hide?id=24961253&goto=news
Processing url 66: https://news.ycombinator.com/vote?id=24957280&how=up&goto=news
Processing url 67: https://news.ycombinator.com/from?site=nngroup.com
Processing url 68: https://www.atlasobscura.com/articles/peoples-linguistic-survey-of-india-ganesh-devy
Processing url 69: https://news.ycombinator.com/hide?id=24958504&goto=news
Processing url 70: https://x86.lol/generic/2020/10/30/complexity-in-operating-systems.html
Processing url 71: https://news.ycombinator.com/from?site=wired.com
Processing url 72: https://news.ycombinator.com/hide?id=24961028&goto=news
Processing url 73: https://news.ycombinator.com/from?site=pine64.com
Processing url 74: https://news.ycombinator.com/hide?id=24957783&goto=news
Processing url 75: https://news.ycombinator.com/item?id=24958725
Processing url 76: https://blog.maiot.io/12-factors-of-ml-in-production/
Processing url 77: https://news.ycombinator.com/item?id=24960772
Processing url 78: https://news.ycombinator.com/item?id=24949736
Processing url 79: https://news.ycombinator.com/item?id=24949983
Processing url 80: https://api.peervadoo.com/test
Processing url 81: https://news.ycombinator.com/lists
Processing url 82: https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/looking-back-on-the-spanish-war/
Processing url 83: https://news.ycombinator.com/vote?id=24959090&how=up&goto=news
Processing url 84: https://eclecticlight.co/2020/09/16/boot-volume-layout/
Processing url 85: https://news.ycombinator.com/hide?id=24959408&goto=news
Processing url 86: https://news.ycombinator.com/vote?id=24960108&how=up&goto=news
Processing url 87: https://news.ycombinator.com/hide?id=24958725&goto=news
Processing url 88: https://news.ycombinator.com/user?id=dsego
Processing url 89: https://news.ycombinator.com/vote?id=24961253&how=up&goto=news
Processing url 90: https://news.ycombinator.com/vote?id=24958423&how=up&goto=news
Processing url 91: https://news.ycombinator.com/from?site=gist.github.com
Processing url 92: https://news.ycombinator.com/vote?id=24950777&how=up&goto=news
Processing url 93: https://news.ycombinator.com/user?id=thecodrr
Processing url 94: https://www.workatastartup.com/companies/21800
Processing url 95: https://news.ycombinator.com/hide?id=24958423&goto=news
Processing url 96: https://news.ycombinator.com/user?id=vulpesx2
Processing url 97: https://github.com/sepfy/piipcam
Processing url 98: https://news.ycombinator.com/from?site=peervadoo.com
Processing url 99: http://www.ycombinator.com/legal/
Processing url 100: https://news.ycombinator.com/user?id=ducktective
Visited 100 urls, Simple Web Crawler Job done!
```
