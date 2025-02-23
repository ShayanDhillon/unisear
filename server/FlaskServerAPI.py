import requests;

from flask import Flask, jsonify;
from flask_cors import CORS;

def getCanadianPostSecondaryInstitutionsData():
  instituion_list = [];

  # Hand picked universities to speed up the process
  dict = {
    "Acadia University": "https://www2.acadiau.ca/",
    "Algoma University": "https://algomau.ca/",
    "Athabasca University": "https://www.athabascau.ca/",
    "Bishop's University": "https://www.ubishops.ca/",
    "Brandon University": "https://www.brandonu.ca/",
    "Brock University": "https://brocku.ca/",
    "Cape Breton University": "https://www.cbu.ca/",
    "Carleton University": "https://carleton.ca/",
    "Concordia University": "https://www.concordia.ca/",
    "Dalhousie University": "https://www.dal.ca/",
    "Emily Carr University of Art + Design": "https://www.ecuad.ca/",
    "Lakehead University": "https://www.lakeheadu.ca/",
    "Laurentian University": "https://laurentian.ca/",
    "MacEwan University": "https://www.macewan.ca/",
    "McGill University": "https://www.mcgill.ca/",
    "McMaster University": "https://www.mcmaster.ca/",
    "Memorial University of Newfoundland": "https://www.mun.ca/",
    "Mount Allison University": "https://www.mta.ca/",
    "Mount Royal University": "https://www.mtroyal.ca/",
    "Mount Saint Vincent University": "https://www.msvu.ca/",
    "Nipissing University": "https://www.nipissingu.ca/",
    "OCAD University": "https://www.ocadu.ca/",
    "Ontario Tech University": "https://ontariotechu.ca/",
    "Queen's University": "https://www.queensu.ca/",
    "Royal Roads University": "https://www.royalroads.ca/",
    "Ryerson University": "https://www.ryerson.ca/",
    "Saint Mary's University": "https://www.smu.ca/",
    "Simon Fraser University": "https://www.sfu.ca/",
    "St. Francis Xavier University": "https://www.stfx.ca/",
    "Thompson Rivers University": "https://www.tru.ca/",
    "Trent University": "https://www.trentu.ca/",
    "Université de Moncton": "https://www.umoncton.ca/",
    "Université de Montréal": "https://www.umontreal.ca/",
    "Université de Sherbrooke": "https://www.usherbrooke.ca/",
    "Université du Québec": "https://www.uquebec.ca/",
    "Université Laval": "https://www.ulaval.ca/",
    "University of Alberta": "https://www.ualberta.ca/",
    "University of British Columbia": "https://www.ubc.ca/",
    "University of Calgary": "https://www.ucalgary.ca/",
    "University of Guelph": "https://www.uoguelph.ca/",
    "University of King's College": "https://ukings.ca/",
    "University of Lethbridge": "https://www.uleth.ca/",
    "University of Manitoba": "https://umanitoba.ca/",
    "University of New Brunswick": "https://www.unb.ca/",
    "University of Northern British Columbia": "https://www.unbc.ca/",
    "University of Ontario Institute of Technology": "https://ontariotechu.ca/",
    "University of Ottawa": "https://www.uottawa.ca/",
    "University of Prince Edward Island": "https://www.upei.ca/",
    "University of Regina": "https://www.uregina.ca/",
    "University of Saskatchewan": "https://www.usask.ca/",
    "University of the Fraser Valley": "https://www.ufv.ca/",
    "University of Toronto": "https://www.utoronto.ca/",
    "University of Victoria": "https://www.uvic.ca/",
    "University of Waterloo": "https://uwaterloo.ca/",
    "University of Windsor": "https://www.uwindsor.ca/",
    "University of Winnipeg": "https://www.uwinnipeg.ca/",
    "Vancouver Island University": "https://www.viu.ca/",
    "Western University": "https://www.uwo.ca/",
    "Wilfrid Laurier University": "https://www.wlu.ca/",
    "York University": "https://www.yorku.ca/"
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

