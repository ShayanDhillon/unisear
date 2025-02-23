import requests;

from flask import Flask, jsonify, request;
from flask_cors import CORS;
from gemini_module import gemini_txt_wrapper;
from MachineLearningAPI import MachineLearningAPI;


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

  for uni in dict:
    instituion_list.append(uni);

  return instituion_list, dict;

class FlaskServerAPI:
  def __init__(self):
    self.app = Flask(__name__);

    CORS(self.app);
    self.initializeRoutes();

    insitution_list, instituion_data = getCanadianPostSecondaryInstitutionsData();
    self.insitution_list = insitution_list;
    self.instituion_data = instituion_data;

    print("FlaskServerAPI has been initialized");
    self.app.run(host='0.0.0.0', port=4000);
    
  def initializeRoutes(self):
    @self.app.route('/api/queryAI', methods=["POST"])
    def queryAI():
      data = request.json;
      institution = data.get("insitution", "Wilfrid Laurier University");
      prompt = data.get("prompt", "Hello!");
      
      if institution in self.insitution_list:
        
        ai_model = MachineLearningAPI(f"scraped_data/{institution}");
        improved_result = gemini_txt_wrapper(ai_model.query(prompt)["answer"]);
        return improved_result;
      else:
        # Invalid institution?
        print(f"Invalid institution {institution} was passed.");
        return "";
      

    @self.app.route('/api/getInstiutionList')
    def getInsitutionList():
      return jsonify(self.insitution_list);

