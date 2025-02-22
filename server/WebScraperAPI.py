import scrapy;
import requests;
import re;
import time;
import asyncio;

from pyppeteer import launch;
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup;


class WebScraperAPI():

  def __init__(self, name : str, web_pages : list):
    self.name = name;
    self.web_pages = web_pages;
    self.sentences = [];

    self.base_domain = None;
    if len(self.web_pages) != 0:
      parsed_url = urlparse(self.web_pages[0]);
      self.base_domain = parsed_url.netloc; 
      self.absolute_url = f"{parsed_url.scheme}://{parsed_url.netloc}";
    pass;
  
  def cleanSentence(self, sentence):
    # First remove leading and trailing whitespaces
    sentence = sentence.strip();
    # Replace multiple spaces with a single space
    sentence = re.sub(r'\s+', ' ', sentence);
    # Remove puncutation
    sentence = re.sub(r'[^\w\s]', '', sentence);

    sentence = sentence.lower();
    return sentence;

  def collectScrapedText(self, text):
    # Append all sentences to the list
    scraped_sentences = re.split(r'(?<=\w[.?]) +', text);
    for sentence in scraped_sentences:
      cleaned_sentence = self.cleanSentence(sentence);
      if cleaned_sentence and cleaned_sentence not in self.sentences:
        self.sentences.append(cleaned_sentence);
  
  def scrape(self):
    # Irelevant pages
    ignore_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", 
                     ".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv", ".webm")

    # Create a dictionary to store scraped links so we don't scrape the same thing again
    scraped_links = [];
    # Copy the initial web_pages to web_links so we can start web crawling
    weblinks_queue = [webpage for webpage in self.web_pages];
    index = 0;
    # While web_links exist, (web_links acts as a priority queue)
    while len(weblinks_queue) > index:
      print(f"LINKS QUEUED: {len(weblinks_queue)} | INDEX: {index}")
      # First get the link first in queue and remove it as we process it
      link = weblinks_queue[index];
      #print(f"PROCESSING: {link}");

      # If the link has not been scraped already then...
      if link not in scraped_links:
        # Attempt to get the webpage html, ignore invalid links
        if not link.startswith(("http://", "https://")):
          index += 1; # Skip this iteration 
          continue;
        
        # Scraping static data
        response = None;
        soup = None;
        try:
          response = requests.get(link);
          soup = BeautifulSoup(response.text, 'html.parser');
        except Exception as e:
          print(f"An exception has occured: {e}");
          index += 1;
          continue;

        text = soup.get_text();

        # Append all sentences to the list
        self.collectScrapedText(text);
      
        # Extract links:
        links = soup.find_all('a', href=True);
        for link in links:
          # Avoid URL join on bad URLS
          absolute_url = None;
          try:
            absolute_url = urljoin(self.absolute_url, link['href']);
          except Exception as e:
            print(f"Failed to get absolute URL, skipping.");
            continue;
          parsed_link = urlparse(absolute_url);
          #print(f"Link: {absolute_url} | Schema {parsed_link.scheme} | Netloc: {parsed_link.netloc}");

          is_image_or_video = absolute_url.lower().endswith(ignore_extensions);
          # If the domain is the same and we have not scraped the site yet add it to the list
          if (self.base_domain == parsed_link.netloc) and (absolute_url not in weblinks_queue) and (not is_image_or_video): #and (len(weblinks_queue) < 10):
            #print(f"PASSED: {absolute_url}");
            weblinks_queue.append(absolute_url);
      
        """
        # Dynamic Scrapping for more data
        browser = await launch(headless=True, executablePath=r"C:\Program Files\Google\Chrome\Application\chrome.exe");
        page = await browser.newPage();
      
        # Go to the page
        await page.goto(absolute_url);

        # Wait for page to load
        await page.waitForSelector('body');
      
        # Scrapes text
        page_text = await page.evaluate('document.body.innerText');
        # Append all sentences to the list
        self.collectScrapedText(page_text);

        # Scrapes links
        links = await page.evaluate('''() => {
        const links = Array.from(document.querySelectorAll('a'));
        return links.map(link => link.href);
        }''');
      
        for link in links:
          parsed_link = urlparse(link);
          # If the domain is the same and we have not scraped the site yet add it to the list
          if (self.base_domain == parsed_link.netloc) and (absolute_url not in weblinks_queue):
            weblinks_queue.append(absolute_url);
        

        # Close the browser
        await browser.close();
        """
      index += 1;
    print(f"Finished Scrapping | {self.name}");



