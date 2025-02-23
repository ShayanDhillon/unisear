import requests;
import re;
import os;
import time;
import json;
import nltk;

from pyppeteer import launch;
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup;
from nltk.corpus import words;

nltk.download('words')

class WebScraperAPI():

  def __init__(self, name : str, web_pages : list):
    self.name = name;
    self.web_pages = web_pages;
    self.scraping = False;
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

    university_whitelist = self.name.split()
    UNIVERSITY_NAMES = [word.lower() for word in university_whitelist]  # make all of the list into lower
    VALID_WORDS = set(words.words())
    TWO_LETTER_WORDS = ["of", "to", "in", "it", "is", "be", "as", "at", "so", "we", "he", "by", "or", "on", "do", "if", "me", "my", "up", "an", "go", "no", "us", "am", "up"]
    CANADIAN_CITIES = [
        "Banff", "Brooks", "Calgary", "Edmonton", "Fort McMurray", "Grande Prairie", "Jasper", "Lake Louise",
        "Lethbridge", "Medicine Hat", "Red Deer", "Saint Albert", "Abbotsford", "Burnaby", "Campbell River", 
        "Castlegar", "Chilliwack", "Coquitlam", "Courtenay", "Cranbrook", "Dawson Creek", "Delta", "Duncan", 
        "Fort St. John", "Kamloops", "Kelowna", "Langley", "Maple Ridge", "Merritt", "Nanaimo", "Nelson", 
        "New Westminster", "North Vancouver", "Parksville", "Penticton", "Port Alberni", "Port Coquitlam", 
        "Port Moody", "Prince George", "Quesnel", "Richmond", "Salmon Arm", "Surrey", "Terrace", "Vancouver", 
        "Vernon", "Victoria", "West Kelowna", "West Vancouver", "White Rock", "Brandon", "Dauphin", "Flin Flon", 
        "Morden", "Portage la Prairie", "Thompson", "Winnipeg", "Bathurst", "Campbellton", "Edmundston", 
        "Fredericton", "Miramichi", "Moncton", "Saint John", "Corner Brook", "Mount Pearl", "St. John's", 
        "Halifax", "Sydney", "Ajax", "Barrie", "Belleville", "Brampton", "Brantford", "Brockville", "Burlington", 
        "Cambridge", "Cornwall", "Dryden", "Greater Sudbury", "Guelph", "Hamilton", "Kawartha Lakes", "Kingston", 
        "Kitchener", "London", "Markham", "Milton", "Mississauga", "Niagara Falls", "North Bay", "Oakville", 
        "Oshawa", "Ottawa", "Owen Sound", "Peterborough", "Pickering", "Richmond Hill", "Sarnia", "Sault Ste. Marie", 
        "St. Catharines", "Thunder Bay", "Toronto", "Vaughan", "Waterloo", "Windsor", "Charlottetown", "Summerside", 
        "Alma", "Amos", "Baie-Comeau", "Beloeil", "Blainville", "Brossard", "Chambly", "Charlesbourg", "Châteauguay", 
        "Chicoutimi", "Drummondville", "Granby", "Joliette", "Laval", "Lévis", "Longueuil", "Magog", "Mascouche", 
        "Mont-Laurier", "Mont-Saint-Hilaire", "Montreal", "Repentigny", "Rimouski", "Rouyn-Noranda", "Saguenay", 
        "Saint-Hyacinthe", "Saint-Jean-sur-Richelieu", "Saint-Jérôme", "Saint-Lambert", "Saint-Sauveur", "Shawinigan", 
        "Sherbrooke", "Sorel-Tracy", "Terrebonne", "Trois-Rivières", "Val-d'Or", "Varennes", "Victoriaville", "Estevan", 
        "Humboldt", "Kindersley", "Lloydminster", "Martensville", "Meadow Lake", "Melfort", "Moose Jaw", 
        "North Battleford", "Prince Albert", "Regina", "Saskatoon", "Swift Current", "Weyburn", "Yorkton", "Yellowknife", 
        "Iqaluit", "Whitehorse"
    ]

    lines = sentence.splitlines()

    filtered_lines = []
    for line in lines:
        words_list = re.split(r'[ .,\t\r]+', line)  # split the words into an array by spaces
    
        filtered_words = [word for word in words_list
            if (
                (word.lower() in VALID_WORDS or word.lower() in CANADIAN_CITIES or word.lower() in UNIVERSITY_NAMES)  # either a valid word OR its a university name OR a city name
                and (len(word) != 2 or word.lower() in TWO_LETTER_WORDS)  # if two letter that isn't in the 2 letter words array, remove
                and len(word) != 1  # if char, remove
            )]
        filtered_lines.append(" ".join(filtered_words))
    output_string = "\n".join([line for line in filtered_lines if line.strip()])
    return output_string;


  def collectScrapedText(self, text):
    # Append all sentences to the list
    scraped_sentences = re.split(r'(?<=\w[.?]) +', text);
    for sentence in scraped_sentences:
      cleaned_sentence = self.cleanSentence(sentence);
      if cleaned_sentence and cleaned_sentence not in self.sentences:
        self.sentences.append(cleaned_sentence);
  
  def scrape(self):
    self.scraping = True;
    
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
          if (self.base_domain == parsed_link.netloc) and (absolute_url not in weblinks_queue) and (not is_image_or_video) and (len(weblinks_queue) < 100):
            #print(f"PASSED: {absolute_url}");
            weblinks_queue.append(absolute_url);
      
      index += 1;
    self.scraping = True;
    print(f"Finished Scraping | {self.name}");

  def saveScrapedData(self):
    # Get directory path
    dir_path = f"scrapped_data/{self.name}";
    os.makedirs(dir_path, exist_ok=True);

    # Save meta data of the current time
    meta_data = {"scrape_time" : int(time.time()),};
    with open(rf"{dir_path}/meta_data.json", "w") as json_file:
      json.dump(meta_data, json_file, indent=2);
    
    # Write data to local system (scraping takes a lot of time)
    with open(f"{dir_path}/scrapped_data.txt", "w", encoding='utf-8') as file:
      file.writelines(f"{sentence}\n" for sentence in self.sentences);
    print(f"Scraped data has been saved | {self.name}");

  def scrapeAndSave(self):
    self.scrape();
    self.saveScrapedData();
