import urllib.request
import os

url = "https://raw.githubusercontent.com/selva86/datasets/master/supermarket_sales.csv"
target = os.path.join("data", "supermarket_sales.csv")

try:
    urllib.request.urlretrieve(url, target)
    size = os.path.getsize(target)
    print(f"Downloaded from: {url}")
    print(f"Saved to: {target}")
    print(f"File size: {size} bytes")
    
    # Quick verification
    import pandas as pd
    df = pd.read_csv(target)
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print(f"Columns: {list(df.columns)}")
except Exception as e:
    print(f"Download failed: {e}")
