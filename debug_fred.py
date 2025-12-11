import os
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('FRED_API_KEY')
print(f"Using API Key: {api_key[:5]}...")

fred = Fred(api_key=api_key)

series_to_check = ['DFF', 'SOFR', 'EXHOSLUSM495S', 'TRFSTSI']

print("Checking FRED Series...")
for s in series_to_check:
    try:
        data = fred.get_series(s, limit=5)
        print(f"[OK] {s}: Found {len(data)} points.")
    except Exception as e:
        print(f"[FAIL] {s}: {e}")
