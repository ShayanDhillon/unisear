import requests;
import re;
import os;

import pandas as pd;

from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup;

YEAR_PATTERN = re.compile(r"\b(20\d{2})\b");

class WebScraperAPI():

  def __init__(self, school_name : str, starting_url : list):
    self.name = school_name;
    self.starting_url = starting_url;
    self.parsed_url = None;

    try:
      self.parsed_url = urlparse(starting_url);
      self.absolute_url = f"{self.parsed_url.scheme}://{self.parsed_url.netloc}/";
    except Exception as e:
      print(f"Failed to parse url {starting_url}: {e}");
      return None;

    # Dataframe to store the scraped data
    self.df = pd.DataFrame();

  def scrape(self):
    # Irelevant pages
    IGNORE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", 
                     ".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv", ".webm")

    # Create a dictionary to store scraped links so we don't scrape the same thing again
    scraped_links = [];
    # Copy the initial web_pages to web_links so we can start web crawling
    weblinks_queue = [self.starting_url];
    index = 0;
    # While web_links exist, (web_links acts as a priority queue)
    while len(weblinks_queue) > index:
      print(f"LINKS QUEUED: {len(weblinks_queue)} | INDEX: {index}");

      # First get the link first in queue and remove it as we process it
      link = weblinks_queue[index];
      print(f"PROCESSING LINK: {link}");

      # If the link has not been scraped already then...
      # Start web crawling
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
        
        # Scrape header body content
        new_data = [];
        for h1 in soup.find_all("h1"):
          header = h1.get_text(strip=True);

          # Find content under the header
          content = "";
          next_element = h1.find_next_sibling();

          # Collect all content
          while next_element and next_element.name != "h1":
            if next_element.name is None:
              content += next_element.strip();
            elif next_element.name in ["p", "div", "span"]:
              content += next_element.get_text(strip=True);
            next_element = next_element.find_next_sibling();

          if content != "" or header == "Search Results":
            # Append the data only if the content is not empty
            new_data.append({"Header" : header, "Content": content});

        # After iterating append to data frame;
        new_df = pd.DataFrame(new_data);
        self.df = pd.concat([self.df, new_df], ignore_index=True);
      
        # Extract links:
        links = soup.find_all('a', href=True);
        for link in links:
          
          # We do not want to scrape pages that are old so any links with old years become invalid.
          match = YEAR_PATTERN.search(link['href']);
          if match:
            year = int(match.group(1));
            if year <= 2023:
              continue;

          # Avoid URL join on bad URLS
          absolute_url = None;
          parsed_link = None;
          try:
            absolute_url = urljoin(self.absolute_url, link['href']);
            parsed_link = urlparse(absolute_url);
          except Exception as e:
            print(f"Failed to get absolute URL, skipping: {e}");
            continue;

          is_search_link = parsed_link.path == "/search.php";
          is_image_or_video = absolute_url.lower().endswith(IGNORE_EXTENSIONS);
          # If the domain is the same and we have not scraped the site yet add it to the list
          if (self.parsed_url.netloc == parsed_link.netloc) and (absolute_url not in weblinks_queue) and (not is_image_or_video) and (not is_search_link) and (len(weblinks_queue) < 15000):
            # Append to weblinks queue to be processed later
            weblinks_queue.append(absolute_url);
      
      index += 1;
    print(f"Finished Scraping | {self.name}");

  def saveScrapedData(self):
    # Get directory path
    dir_path = f"./scrapped_data/{self.name}";
    os.makedirs(dir_path, exist_ok=True);

    # Write data to local system (scraping takes a lot of time)
    self.df.to_csv(f"{dir_path}/scraped_data.csv");
    print(f"Scraped data has been saved | {self.name}");
