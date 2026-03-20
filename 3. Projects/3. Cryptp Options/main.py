# de_api_key = 'TsjwX0WMQ4CtoNKECm3nNjk8aytodw'
# de_api_skey = 'RmFWLC9XHAoBx89xseayjkAPGx2ECokbPYNH3Q5gq6QGAY5yVSql0ZhJ3mv6'


import requests
import time
import hmac
import hashlib
import json
from delta_rest_client import DeltaRestClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm




API_KEY = "TsjwX0WMQ4CtoNKECm3nNjk8aytodw"
API_SECRET = "RmFWLC9XHAoBx89xseayjkAPGx2ECokbPYNH3Q5gq6QGAY5yVSql0ZhJ3mv6"
API_KEY_BACKTEST = 'IFDcDcJuM9ho9tPdfmonCbDec9Df34'
API_SECRET_BACKTEST = 'KWQ58v6GV3qloVCTehKVsU06wIPiwjYVr6CV2RlS89OLF8xGU3nbE0E1eCoN'
MAIN_NET_BASE_URL = "https://api.india.delta.exchange"
TEST_NET_BASE_URL = 'https://cdn-ind.testnet.deltaex.org'


client = DeltaRestClient(
    base_url=MAIN_NET_BASE_URL,
    api_key=API_KEY_BACKTEST,
    api_secret=API_SECRET_BACKTEST
)

# Test private endpoint
assets = client.get_assets()
print(assets)

def fetch_delta_5y_data(symbol, resolution, base_url=BASE_URL):
    """
    Fetch historical candle data from Delta Exchange
    
    Args:
        symbol: Trading pair symbol (e.g., "BTCUSDT")
        resolution: Candle resolution (e.g., "1m", "5m", "1h")
        base_url: API base URL
    """
    # Clean symbol format - Delta might expect format like "BTCUSDT"
    if not symbol.endswith('USDT') and not symbol.endswith('USD'):
        symbol = f"{symbol}USDT"
    
    filename = f"{symbol}_{resolution}_5y.xlsx"

    # ---------------------------------------------------
    # STEP 1: Load if file exists
    # ---------------------------------------------------
    if os.path.exists(filename):
        print("Excel file found. Loading from disk...")
        df = pd.read_excel(filename)
        print(f"Loaded {len(df)} rows.")
        return df

    print("No local file found. Downloading from API...")

    # ---------------------------------------------------
    # STEP 2: Prepare time range
    # ---------------------------------------------------
    end_time = int(datetime.now().timestamp())
    start_time = int((datetime.now() - timedelta(days=5*365)).timestamp())
    
    all_data = []
    page = 1
    
    print(f"Fetching data from {datetime.fromtimestamp(start_time)} to {datetime.fromtimestamp(end_time)}")

    with tqdm(desc="Downloading candles", unit=" candles") as pbar:
        while True:
            params = {
                "symbol": symbol,
                "resolution": resolution,
                "start": start_time,
                "end": end_time,
                # "page": page  # Add pagination
            }

            try:
                response = requests.get(
                    f"{base_url}/v2/history/candles",
                    params=params,
                    timeout=30
                )
                
                print(f"Request URL: {response.url}")  # Debug: print the full URL
                print(f"Response Status: {response.status_code}")  # Debug: print status code

                if response.status_code != 200:
                    print(f"Error response: {response.text}")
                    break

                data = response.json()
                
                # Check different possible response structures
                if isinstance(data, dict):
                    if "result" in data:
                        candles = data["result"]
                    elif "candles" in data:
                        candles = data["candles"]
                    else:
                        candles = data.get("data", [])
                elif isinstance(data, list):
                    candles = data
                else:
                    candles = []

                if not candles:
                    print(f"No more candles found. Total fetched: {len(all_data)}")
                    break

                all_data.extend(candles)
                pbar.update(len(candles))
                
                # Check if we've reached the end of data
                if len(candles) < 500:  # Assuming 500 is the page size
                    break
                    
                page += 1
                time.sleep(0.3)  # Rate limiting

            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                break
    
    if not all_data:
        print("No data was fetched. Please check:")
        print(f"1. Symbol '{symbol}' is correct")
        print(f"2. Resolution '{resolution}' is valid")
        print("3. API endpoint is accessible")
        return pd.DataFrame()

    print(f"Sample raw response (first 2 candles): {all_data[:2]}")

    # ---------------------------------------------------
    # STEP 3: Convert to DataFrame
    # ---------------------------------------------------
    df = pd.DataFrame(all_data)
    
    # Handle different data formats
    if len(df) > 0:
        # Check if data is in list format
        if isinstance(all_data[0], list):
            df.columns = ["timestamp", "open", "high", "low", "close", "volume"]
        
        # Check if data is in dict format
        elif isinstance(all_data[0], dict):
            # Try different possible column names
            if "time" in df.columns:
                df.rename(columns={"time": "timestamp"}, inplace=True)
            elif "timestamp" not in df.columns and "start_time" in df.columns:
                df.rename(columns={"start_time": "timestamp"}, inplace=True)
            
            # Ensure numeric columns
            for col in ["open", "high", "low", "close", "volume"]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert timestamp to datetime
        if "timestamp" in df.columns:
            df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
            df.sort_values("datetime", inplace=True)
            
            # Select and order columns
            cols = ["datetime", "open", "high", "low", "close", "volume"]
            available_cols = [col for col in cols if col in df.columns]
            df = df[available_cols]

    # ---------------------------------------------------
    # STEP 4: Save to Excel
    # ---------------------------------------------------
    if not df.empty:
        df.to_excel(filename, index=False)
        print(f"Saved {len(df)} candles to {filename}")
    else:
        print("DataFrame is empty, nothing to save")

    return df

# Test with different symbol formats
SYMBOL = "BTCUSDT"  # Try both "BTCUSD" and "BTCUSDT"
RESOLUTION = "1h"  # Start with 1h to get less data for testing

# Run
print("Starting data fetch...")
df = fetch_delta_5y_data(SYMBOL, RESOLUTION)
print(df.head())

def load_options_data(signal_date, symbol="BTC", options_dir="options_data"):
    """
    Load options data for a specific date and track until position closes
    
    Args:
        signal_date: datetime or string, when signal was generated
        symbol: str, symbol prefix (default: "BTC")
        options_dir: str, directory containing options files
    
    Returns:
        DataFrame with options data from signal_date onwards
    """
    # Convert signal_date to datetime if string
    if isinstance(signal_date, str):
        signal_date = pd.to_datetime(signal_date)
    
    # Find the relevant file based on signal_date
    signal_year_month = signal_date.strftime("%Y-%m")
    filename = f"{symbol}_{signal_year_month}.csv"
    filepath = os.path.join(options_dir, filename)
    
    # Load the data
    if not os.path.exists(filepath):
        # If exact month file doesn't exist, find the closest previous month
        all_files = sorted([f for f in os.listdir(options_dir) if f.startswith(symbol)])
        if not all_files:
            raise FileNotFoundError(f"No options files found in {options_dir}")
        
        # Find file with date <= signal_date
        for f in reversed(all_files):
            file_date = f.replace(f"{symbol}_", "").replace(".csv", "")
            if pd.to_datetime(file_date + "-01") <= signal_date:
                filepath = os.path.join(options_dir, f)
                print(f"Exact month file not found, using {f}")
                break
    
    print(f"Loading options data from: {filepath}")
    options_df = pd.read_csv(filepath)
    
    # Ensure datetime column exists and convert
    if 'timestamp' in df.columns:
        options_df['datetime'] = pd.to_datetime(options_df['timestamp'])
    elif 'date' in df.columns:
        options_df['datetime'] = pd.to_datetime(options_df['date'])
    elif 'time' in df.columns:
        options_df['datetime'] = pd.to_datetime(options_df['time'])
    
    # Filter data from signal_date onwards
    options_df = options_df[df['datetime'] >= signal_date].copy()
    options_df.sort_values('datetime', inplace=True)
    
    return df

def track_option_position(option_data, entry_time, exit_time=None):
    """
    Track PnL for an option position
    
    Args:
        option_data: DataFrame with option prices
        entry_time: datetime when position was opened
        exit_time: datetime when position was closed (None if still open)
    
    Returns:
        dict with position tracking info
    """
    # Filter data for the position duration
    position_data = option_data[option_data['datetime'] >= entry_time].copy()
    
    if exit_time:
        position_data = position_data[position_data['datetime'] <= exit_time]
    
    if position_data.empty:
        return {"error": "No data for specified time range"}
    
    # Calculate metrics
    tracking = {
        "entry_time": entry_time,
        "exit_time": exit_time if exit_time else position_data['datetime'].iloc[-1],
        "entry_price": position_data.iloc[0].get('price', position_data.iloc[0].get('close', 0)),
        "current_price": position_data.iloc[-1].get('price', position_data.iloc[-1].get('close', 0)),
        "max_price": position_data.get('high', position_data['price']).max() if 'high' in position_data else position_data['price'].max(),
        "min_price": position_data.get('low', position_data['price']).min() if 'low' in position_data else position_data['price'].min(),
        "price_history": position_data[['datetime', 'price']].to_dict('records') if 'price' in position_data else None
    }
    
    # Calculate PnL
    tracking['pnl'] = tracking['current_price'] - tracking['entry_price']
    tracking['pnl_pct'] = (tracking['pnl'] / tracking['entry_price']) * 100
    
    return tracking

# Example usage:
if __name__ == "__main__":
    # When signal is generated on Jan 15, 2025
    signal_date = "2025-01-15"
    
    # Load options data from that point forward
    options_df = load_options_data(signal_date)
    
    print(f"Loaded {len(options_df)} rows from {options_df['datetime'].min()} to {options_df['datetime'].max()}")
    
    # Track a position entered at signal_date and exited 7 days later
    entry = pd.to_datetime(signal_date)
    exit_time = entry + pd.Timedelta(days=7)
    
    position = track_option_position(options_df, entry, exit_time)
    print(f"\nPosition PnL: ${position['pnl']:.2f} ({position['pnl_pct']:.2f}%)")
