import pandas as pd
import json

excel_file = r'd:\healthcare_web\API명세서 Cloud9 Care.xlsx'

def clean(val):
    if pd.isna(val): return None
    return str(val).strip()

try:
    df = pd.read_excel(excel_file, sheet_name='origin')
    
    apis = []
    # Data seems to start from row 1 (0-indexed) if row 0 is headers
    for index, row in df.iterrows():
        url = clean(row.iloc[1])
        if url and url.startswith('/'):
            api = {
                "domain": clean(row.iloc[0]),
                "url": url,
                "method": clean(row.iloc[2]),
                "description": clean(row.iloc[3]),
                "req_body_schema": clean(row.iloc[10]),
                "res_success_schema": clean(row.iloc[12]),
                "res_error_schema": clean(row.iloc[14]),
            }
            apis.append(api)
    
    with open('api_spec_extracted.json', 'w', encoding='utf-8') as f:
        json.dump(apis, f, ensure_ascii=False, indent=2)
        
    print(f"Extracted {len(apis)} API endpoints.")

except Exception as e:
    print(f"Error: {str(e)}")
