import pandas as pd

excel_file = r"d:\healthcare_web\API명세서 Cloud9 Care.xlsx"

try:
    xl = pd.ExcelFile(excel_file)
    print(f"Sheets: {xl.sheet_names}")
except Exception as e:
    print(f"Error: {str(e)}")
