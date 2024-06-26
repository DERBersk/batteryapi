# import external packages
import pandas as pd
import pycountry
import json

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
                country_info["index"] = val / 2 
                break
        if(country_info["index"] >= 0):      
            data.append(country_info)
        
    return data

    