import requests;
import scrapy;
import pandas as pd;
import numpy as np;
import asyncio;
import os;
import time;

from FlaskServerAPI import FlaskServerAPI, getCanadianPostSecondaryInstitutionsData;
from WebScraperAPI import WebScraperAPI;
from MlFlowAPI import MLFlowAPI;

def scrapeInstituionData(instituion, instituion_web_pages):
  web_scraper = WebScraperAPI(instituion, instituion_web_pages);
  # First scrape the data;
  web_scraper.scrape();
  # Next save the data;
  web_scraper.saveScrapedData();

  ml_flow_ai = MLFlowAPI(rf"scrapped_data/{instituion}", web_scraper);
  ml_flow_ai;
  return web_scraper;

def scrapeAllInstitutionsData(institutions_list, institutions_data):
  
  count = 0;
  for institution in institutions_data:

    count += 1;
    print(f"Scraping Progress: {count/len(institutions_data)*100:.2f}%");

    scrapeInstituionData(institution, institutions_data[institution]);
  
def main():
  print("Starting Application...");


  """
  WE ASSUME:
  [1]: Data has been scrapped at least ONCE.
  [2]: meta_data has been created
  """
  _, dict = getCanadianPostSecondaryInstitutionsData();
  INSTITUTION_NAME = "Wilfrid Laurier University"
  #ai = MLFlowAPI(f"scrapped_data/{INSTITUTION_NAME}", WebScraperAPI(f"{INSTITUTION_NAME}", dict[INSTITUTION_NAME]));
  #ai.storeDataFrameAsVectorDB();

  #scrapeInstituionData("Wilfrid Laurier University", ["https://www.wlu.ca/"])
  flask_app = FlaskServerAPI();
  # Retrieves institution data
  instiutions_list, instiutions_data = getCanadianPostSecondaryInstitutionsData();

  # Single line testing

  # scrapper = scrapeInstituionData("Wilfrid Laurier University", ["https://www.wlu.ca/"]);
  
  # Full data scraping
  # scrapeAllInstitutionsData(instiutions_list, instiutions_data);


main();