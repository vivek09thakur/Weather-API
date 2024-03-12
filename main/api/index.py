from flask import Flask,jsonify,request
from flask_cors import CORS
from scarper.scraper import Scraper

app = Flask(__name__)
CORS(app)

scraper = Scraper()

@app.route('/')
def home():
    return 'Open Source Weather API - By Vivek Thakur'

@app.route('/get_weather_data',method=['POST'])
def fetch_weather_data():
    data = request.get_json()
    query = data['query']
    
    if type(query) is not str:
         return jsonify({'error': {
             'message': 'Internal Server Error: query Type must be a string.'}})
    
    scraped_data = scraper.scrape_data(query)
    if scraped_data is None:
        return jsonify({'error': 
            {'message': 'An internal server error occurred while fetching the API.'}})
    
    return jsonify({'response':scraped_data})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,PATCH,POST,DELETE,OPTIONS')
    return response