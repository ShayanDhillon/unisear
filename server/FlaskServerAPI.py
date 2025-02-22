import requests;

from flask import Flask, jsonify;

def getCanadianPostSecondaryInstitutionsData():

  url = "http://universities.hipolabs.com/search?country=Canada";
  dict = {};
  response = requests.get(url).json();
  instituion_list = [];
  for uni in response:
    uni_name = uni["name"];
    dict[uni_name] = uni["web_pages"];
    instituion_list.append(uni_name);
  return instituion_list, dict;

class FlaskServerAPI:
  def __init__(self):
    self.app = Flask(__name__);
    self.initializeRoutes();
    self.app.run(host='0.0.0.0', port=5000);

    insitution_list, _ = getCanadianPostSecondaryInstitutionsData();
    self.insitution_list = insitution_list;
  
    print("FlaskServerAPI has been initialized");
    
  def initializeRoutes(self):
    @self.app.route('/')
    def test():
      return "hello world";

    @self.app.route('/api/getInstiution')
    def getInsitution():
      return jsonify(self.insitution_list);

