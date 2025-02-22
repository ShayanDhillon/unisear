import scrapy;
import requests;
import re;

from bs4 import BeautifulSoup;

class MySpider():

  def __init__(self, name : str, web_pages : list):
    self.name = name;
    self.web_pages = web_pages;
    self.sentences = [];
    pass;

  def scrape(self):
    # Create a dictionary to store scraped links so we don't scrape the same thing again
    scraped_links = {};
    # Copy the initial web_pages to web_links so we can start web crawling
    web_links = [webpage for webpage in self.web_pages];

    # While web_links exist, (web_links acts as a priority queue)
    while len(web_links) > 0:

      # First get the link first in queue
      link = web_links[0];

      # If the link has been scraped already then remove it
      if scraped_links[link]:


      # Attempt to get the webpage html
      response = requests.get(link);
      json_data = response.json();

      soup = BeautifulSoup(response.text, 'html.parser');
      text = soup.get_text();

      scraped_sentences = re.split(r'(?<=\w[.?]) +', text);
      for sentence in scraped_sentences:
        self.sentences.append(sentence);

      # After scraping the page remove the first item as processed and store the link to ensure we don't get to this link again
      web_links.pop(0);
      scraped_links[link] = True;




