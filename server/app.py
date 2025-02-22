import requests;
import scrapy;

import pandas as pd;
import numpy as np;

def getCanadianPostSecondaryInstitutions():

  url = "http://universities.hipolabs.com/search?country=Canada";
  dict = {};
  response = requests.get(url).json();
  for uni in response:
    uni_name = uni["name"];
    dict[uni_name] = uni["web_pages"];
  return dict;

def main():
  instituions = getCanadianPostSecondaryInstitutions();
  print(instituions);

  pass;

main();