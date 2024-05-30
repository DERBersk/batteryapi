import random
import json

# Function to generate a random number between 0 and 1
def calculate_risk_index():
    return round(random.uniform(0, 1), 3)

# Function to transform the JSON data
def transform_country_data(country_data):
    transformed_data = []
    for country_code, description in country_data.items():
        transformed_entry = {
            "countrycode": country_code,
            "description": description,
            "no.": calculate_risk_index()
        }
        transformed_data.append(transformed_entry)
    return transformed_data

# Load the countryCode.json data
def load_country_data():
    with open('lib/json/countryCode.json') as file:
        country_data = json.load(file)
    return country_data