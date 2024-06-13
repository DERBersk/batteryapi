# import external packages
import pandas as pd
import pycountry
import json

def CountryRisk():
    df = pd.read_excel("https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls")

    cols = [col for col in df.columns if col.startswith("GPRC_")]

    data = []
    tail = df.tail(1)
    for col in cols:
        country = pycountry.countries.get(alpha_3=col.split("_")[-1])
        col_data = {
            "countrycode": country.alpha_2,
            "description": country.name,
            "index": tail[col].item()
        }
        data.append(col_data)

    return data