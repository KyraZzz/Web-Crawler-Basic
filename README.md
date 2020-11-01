# Web-Crawler-Basic
A simple web crawler using HTML link tags, with Breadth First Search Implemented.

# Step-by-step intro:
``` python
# Reference: https://www.freecodecamp.org/news/how-to-build-a-url-crawler-to-map-a-website-using-python-6a287be1da11/
# Reference: https://pythonprogramming.net/introduction-scraping-parsing-beautiful-soup-tutorial/
# External libraries used: BeautifulSoup, requests, urllib.
```
In this program, the external library we used are:
* BeautifulSoup: parse the HTML file fetched from the url with the help of `lxml` parser
* requests: Check for broken urls using `requests.exceptions` module and fetch response
* urllib: open url and split the url into parts
