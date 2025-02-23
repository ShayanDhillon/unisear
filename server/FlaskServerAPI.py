import requests;

from flask import Flask, jsonify, request;
from flask_cors import CORS;
from WebScraperAPI import WebScraperAPI;
from MlFlowAPI import MLFlowAPI;

def getCanadianPostSecondaryInstitutionsData():
  instituion_list = [];

  # Hand picked universities to speed up the process
  #print("DEATH TO ASHLEY")

  
  url = "http://universities.hipolabs.com/search?country=Canada";
  dict = {};
  response = requests.get(url).json();
  for uni in response:
    uni_name = uni["name"];
    dict[uni_name] = uni["web_pages"];
    instituion_list.append(uni_name);
  


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
    @self.app.route('/api/queryAI', methods=["GET"])
    def queryAI():
      institution = request.args.get("insitution", "Wilfrid Laurier University");
      prompt = request.args.get("prompt", "Hello!");
      
      if institution in self.insitution_list:

        web_scraper = WebScraperAPI(name=institution, web_pages=self.instituion_data[institution]);
        ml_model = MLFlowAPI(rf"scrapped_data/{institution}", web_scraper);

        return jsonify(ml_model.summarizeQuery(prompt));
      else:
        # Invalid institution?
        print(f"Invalid institution {institution} was passed.");
        return "";
      

    @self.app.route('/api/getInstiutionList')
    def getInsitutionList():

      return jsonify(self.insitution_list);

