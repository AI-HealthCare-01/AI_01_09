import pandas as pd

excel_file = r'd:\healthcare_web\API명세서 Cloud9 Care.xlsx'

try:
    # Read all sheets to see what's inside
    xl = pd.ExcelFile(excel_file)
    print(f"Sheets: {xl.sheet_names}")
    
    for sheet in xl.sheet_names:
        print(f"\n--- Sheet: {sheet} ---")
        df = pd.read_excel(excel_file, sheet_name=sheet)
        print(df.to_string())
        # Also print columns for reference
        print(f"Columns: {df.columns.tolist()}")

except Exception as e:
    print(f"Error: {str(e)}")
