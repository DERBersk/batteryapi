# import external packages
import pandas as pd
import pycountry
import json

# import models
from models.options import Options
from models.supplier import Supplier
from extensions import db

def CountryRisk():
    df = pd.read_excel("https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls")

    cols = [col for col in df.columns if col.startswith("GPRC_")]

    cols = [col for col in df.columns if col.startswith("GPRC_")]

    json_file_name = "lib/json/countryCode.json"

    with open(json_file_name, 'r') as f:
        country_codes = json.load(f)

    # Erstellen eines Mappings von Alpha-3 Codes zu den Codes aus der countryCode.json Datei
    alpha3_to_code = {pycountry.countries.get(alpha_2=alpha2).alpha_3: alpha2 for alpha2 in country_codes.keys() if pycountry.countries.get(alpha_2=alpha2)}

    data = []
    tail = df.tail(1)
    
    max_value = max([tail[col].item() for col in cols if not tail[col].isnull().item()])

    # Schleife durch die countryCode.json Datei
    for code, name in country_codes.items():
        country_info = {
            "countrycode": code,
            "description": name,
            "index": -1.0
        }

        # Überprüfen, ob das Land in den Spalten der Excel-Datei vorhanden ist
        for col in cols:
            country_code_3 = col.split("_")[-1]
            if country_code_3 in alpha3_to_code and alpha3_to_code[country_code_3] == code:
                val = tail[col].item()
                country_info["index"] = val / max_value
                break
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