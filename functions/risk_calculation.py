# import external packages
import pandas as pd
import pycountry
import json

# import models
from models.options import Options
from models.supplier import Supplier
from extensions import db

def CountryRisk():
    # Load data_gpr_export.xls
    df = pd.read_excel("https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls")

    # Extract relevant columns starting with "GPRC_"
    cols = [col for col in df.columns if col.startswith("GPRC_")]

    # Load country codes from countryCode.json
    json_file_name = "lib/json/countryCode.json"
    with open(json_file_name, 'r') as f:
        country_codes = json.load(f)

    # Create a mapping from Alpha-3 codes to the codes from countryCode.json
    alpha3_to_code = {pycountry.countries.get(alpha_2=alpha2).alpha_3: alpha2 for alpha2 in country_codes.keys() if pycountry.countries.get(alpha_2=alpha2)}

    # Find the maximum value from the last row of data_gpr_export.xls
    tail = df.tail(1)
    max_value = max([tail[col].item() for col in cols if not pd.isnull(tail[col].item())])

    # Prepare to read 2024.csv for second set of indices
    second_indices_file = "lib/csv/2024.csv"
    second_df = pd.read_csv(second_indices_file, sep=';', decimal=',')

    # Merge df and second_df on country codes
    data = []

    # Iterate over entries in countryCode.json
    for code, name in country_codes.items():
        country_info = {
            "countrycode": code,
            "description": name,
            "index": -1.0
        }

        # Check if the country is in data_gpr_export.xls columns
        for col in cols:
            country_code_3 = col.split("_")[-1]
            if country_code_3 in alpha3_to_code and alpha3_to_code[country_code_3] == code:
                val = tail[col].item()
                country_info["index"] = val / max_value
                break
        
        # Fetch corresponding index from second_df and normalize if found
        row = second_df[second_df['Country_EN'] == name]
        if not row.empty:
            second_index = row.iloc[0]['Score']  # Adjust column name if necessary
            if pd.notnull(second_index):  # Avoid division by zero and handle NaN
                normalized_second_index = 1-second_index / 100.0
                country_info["index"] = country_info["index"] * 0.5 + normalized_second_index * 0.5
                
        if(country_info["index"] >= 0):      
            data.append(country_info)

    return data

def update_supplier_risk_indices():
    # Fetch options (assuming only one set of options is used)
    options = Options.query.first()

    # Fetch suppliers
    suppliers = Supplier.query.all()

    # Fetch country risk data
    country_risk_data = CountryRisk()
    country_risk_dict = {item['description']: item['index'] for item in country_risk_data}

    for supplier in suppliers:
        if supplier.country in country_risk_dict:
            country_risk_index = country_risk_dict[supplier.country]
        else:
            country_risk_index = 0  # Default to 0 if country risk is not found
            
        if not supplier.reliability:
            supplier.risk_index = country_risk_index
            continue

        print(supplier.reliability)
        
        print(country_risk_index)

        # Calculate risk_index using weights from options and supplier's reliability
        risk_index = (options.risk_index_weight_country_risk * country_risk_index) + \
                     (options.risk_index_weight_reliability * supplier.reliability)
        
        # Update the supplier's risk_index
        supplier.risk_index = risk_index

    # Commit the changes to the database
    db.session.commit()
    
    return [supplier.serialize() for supplier in suppliers]