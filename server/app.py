import requests;
import scrapy;
import pandas as pd;
import numpy as np;
import asyncio;
import os;
import time;


from FlaskServerAPI import FlaskServerAPI, getCanadianPostSecondaryInstitutionsData;
from WebScraperAPI import WebScraperAPI;

def scrapeInstituionData(instituion, instituion_web_pages):
  test_scraper = WebScraperAPI(instituion, instituion_web_pages);
  test_scraper.scrape();

  dir_path = f"scrapped_data/{test_scraper.name}";
  os.makedirs(dir_path, exist_ok=True);

  # Write data to local system (scraping takes a lot of time)
  with open(f"{dir_path}/scrapped_data.txt", "w", encoding='utf-8') as file:
    file.writelines(f"{int(time.time())}\n")
    file.writelines(f"{sentence}\n" for sentence in test_scraper.sentences);

def scrapeAllInstitutionsData(institutions_list, institutions_data):
  
  count = 0;
  for institution in institutions_data:

    count += 1;
    print(f"Scraping Progress: {count/len(institutions_data)*100:.2f}%");

    scrapeInstituionData(institution, institutions_data[institution]);
  


def main():
  print("Starting Application...");

  #flask_app = FlaskServerAPI();
  # Retrieves institution data
  # instiutions_list, instiutions_data = getCanadianPostSecondaryInstitutionsData();

  # Single line testing
  scrapeInstituionData("Wilfrid Laurier University", ["https://www.wlu.ca/"]);

  # Full data scraping
  # scrapeAllInstitutionsData(instiutions_list, instiutions_data);

main();