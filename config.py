from os import environ
from dotenv import load_dotenv

load_dotenv()
NASA_API_KEY = environ.get('NASA_API_KEY')
NASA_API_URL = 'https://api.nasa.gov/'
