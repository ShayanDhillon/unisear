import requests;
import scrapy;
import pandas as pd;
import numpy as np;
import asyncio;
import os;
import time;

from transformers import pipeline;
from FlaskServerAPI import FlaskServerAPI;
from WebScraperAPI import WebScraperAPI;
from MachineLearningAPI import MachineLearningAPI;
from SentenceGrabberAPI import SentenceGrabberAPI;
from nltk.tokenize import sent_tokenize;

def main():
  print("Starting Application...");

  flask_app = FlaskServerAPI();
  # Retrieves institution data
  # instiutions_list, instiutions_data = getCanadianPostSecondaryInstitutionsData();


  # Single line scrapping
  #scrapper = WebScraperAPI("Wilfrid Laurier University", "https://academic-calendar.wlu.ca/index_old.php?cal=1&y=90");
  #scrapper.scrape();
  #scrapper.saveScrapedData();
  
  # ml_api = MachineLearningAPI("scraped_data/Wilfrid Laurier University");
  # Summarizer testing
  #results = ml_api.summarize("Tell me about coop");
  #print(results["summary_text"]);

  # Q and A testing
  #answer = ml_api.query("What computer science courses are available?");
  #print(answer["answer"]);
main();