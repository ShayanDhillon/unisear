import requests;

from flask import Flask, jsonify;
from flask_cors import CORS;

def getCanadianPostSecondaryInstitutionsData():
  instituion_list = [];

  # Hand picked universities to speed up the process
  dict = {
    "University of Toronto" : ["http://www.utoronto.ca/"],
    "University of British Columbia" : ["http://www.ubc.ca/"],
    "McGill University" : ["http://www.mcgill.ca/"],
    "University of Alberta" : ["http://www.ualberta.ca/"],
    "University of Ottawa" : ["http://www.uottawa.ca/"],
    "Conestoga College" : ["http://www.conestogac.on.ca/"],
    "University of Waterloo" : ["http://www.uwaterloo.ca/"],
    "Wilfrid Laurier University" : ["http://www.wlu.ca/"],
  }

  """
  url = "http://universities.hipolabs.com/search?country=Canada";
  dict = {};
  response = requests.get(url).json();
  for uni in response:
    uni_name = uni["name"];
    dict[uni_name] = uni["web_pages"];
    instituion_list.append(uni_name);
  """

  for uni in dict:
    instituion_list.append(uni);

  return instituion_list, dict;

class FlaskServerAPI:
  def __init__(self):
    self.app = Flask(__name__);
    CORS(self.app);
    self.initializeRoutes();

    insitution_list, _ = getCanadianPostSecondaryInstitutionsData();
    self.insitution_list = insitution_list;

    print("FlaskServerAPI has been initialized");
    self.app.run(host='0.0.0.0', port=4000);
    
  def initializeRoutes(self):
    @self.app.route('/')
    def test():
      return "hello world";

    @self.app.route('/api/getInstiution')
    def getInsitution():
      return jsonify(self.insitution_list);

