#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:40:58 2026

@author: shivprasadkounsalye
"""

from SmartApi import SmartConnect
import pyotp
from logzero import logger
import pandas as pd
# To this:
import datetime
from datetime import timedelta
import time
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

import os
import zipfile
import pandas as pd
from tqdm import tqdm
import requests
import io
import re
# Your credentials
api_key = 'xfiUNWIf'
client_id = 'AACE339837'
pin = '9604'  # Your MPIN or trading password
totp_token = 'MJTI44SBH5VHH4PGSU2RWEOMHI'  # The static token from Angel One
#kaggle_creds = {username : 'shivkounsalye', token : 'KGAT_8ad7de4925fcd1bc2e51159287d1207d'}
# Initialize the connection
smart_api = SmartConnect(api_key)

try:
    # Generate a dynamic TOTP
    totp = pyotp.TOTP(totp_token).now()
except Exception as e:
    logger.error("Invalid TOTP token")
    raise e

# Create a session
data = smart_api.generateSession(client_id, pin, totp)

if data['status'] == False:
    logger.error(f"Login failed: {data}")
else:
    # Extract tokens from the successful login response
    auth_token = data['data']['jwtToken']
    refresh_token = data['data']['refreshToken']
    feed_token = smart_api.getfeedToken()  # Required for live data streams
    logger.info("Login successful. Session established.")
    
    # Test API calls
    print("\n=== Testing API Functions ===")
    
    # 1. Get profile
    profile = smart_api.getProfile(refresh_token)
    print(f"1. Profile Status: {profile['status']}")
    
    # 2. Get holdings
    holdings = smart_api.holding()
    print(f"2. Holdings Count: {len(holdings['data'])}")
    
    # 3. Search for a symbol
    search_result = smart_api.searchScrip("NSE", "RELIANCE")
    print(f"3. Symbol Search: Found {len(search_result)} results")
    
    # Get margin information
    margin = smart_api.rmsLimit()
    print(f"Margin: {margin}")
    
    print("\n✅ All tests passed! Your API is working correctly.")
    
def fetch_historical_data_with_backoff(smart_api, symbol_token, exchange, interval, 
                                        start_date, end_date, max_candles=8000, 
                                        initial_delay=1, backoff_factor=1.5, max_delay=60):
    """
    Fetch historical data with exponential backoff rate limiting
    
    Parameters:
    - smart_api: Your authenticated SmartConnect object
    - symbol_token: Instrument token (e.g., "99926000" for Nifty)
    - exchange: Exchange code (e.g., "NSE")
    - interval: Timeframe (e.g., "ONE_MINUTE")
    - start_date: Start datetime object
    - end_date: End datetime object  
    - max_candles: Max candles per request (default 8000)
    - initial_delay: Initial delay between requests in seconds
    - backoff_factor: Factor to increase delay on errors
    - max_delay: Maximum delay between requests
    """
    
    all_candles = []
    current_delay = initial_delay
    failed_attempts = 0
    max_failed_attempts = 5
    
    # Convert to datetime if strings provided
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)
    
    current_chunk_end = end_date
    
    print(f"Starting historical data fetch from {start_date} to {end_date}")
    print(f"Using delay between requests: {initial_delay} seconds (will increase on errors)")
    
    while current_chunk_end > start_date and failed_attempts < max_failed_attempts:
        # Calculate chunk start (8000 candles ≈ 30 trading days for 1-min)
        current_chunk_start = current_chunk_end - timedelta(days=30)
        
        if current_chunk_start < start_date:
            current_chunk_start = start_date
        
        # Format for API
        from_date_str = current_chunk_start.strftime('%Y-%m-%d %H:%M')
        to_date_str = current_chunk_end.strftime('%Y-%m-%d %H:%M')
        
        print(f"\nRequesting: {from_date_str} to {to_date_str}")
        print(f"Current delay: {current_delay:.1f}s | Failed attempts: {failed_attempts}")
        
        # Prepare API call
        historicParam = {
            "exchange": exchange,
            "symboltoken": symbol_token,
            "interval": interval,
            "fromdate": from_date_str,
            "todate": to_date_str
        }
        
        try:
            # Add delay before request
            time.sleep(current_delay)
            
            # Make API call
            api_response = smart_api.getCandleData(historicParam)
            
            if api_response['status']:
                chunk_data = api_response['data']
                
                if chunk_data:
                    all_candles.extend(chunk_data)
                    print(f"✓ Success: {len(chunk_data)} candles")
                    
                    # Reset delay on success (with minimum)
                    current_delay = max(initial_delay, current_delay / backoff_factor)
                    failed_attempts = 0
                    
                    # Move to next chunk
                    current_chunk_end = current_chunk_start - timedelta(minutes=1)
                else:
                    print("⚠️ No data returned - may have reached earliest available data")
                    current_chunk_end = current_chunk_start - timedelta(minutes=1)
            
            else:
                error_msg = api_response.get('message', 'Unknown API error')
                print(f"✗ API Error: {error_msg}")
                
                # Check if it's a rate limit error
                if "rate limit" in error_msg.lower() or "too many" in error_msg.lower():
                    print(f"Rate limit hit! Increasing delay to {min(current_delay * backoff_factor, max_delay)}s")
                    current_delay = min(current_delay * backoff_factor, max_delay)
                    failed_attempts += 1
                else:
                    print("Stopping due to non-rate-limit error")
                    break
        
        except Exception as e:
            print(f"✗ Exception: {e}")
            failed_attempts += 1
            current_delay = min(current_delay * backoff_factor, max_delay)
            
            if failed_attempts >= max_failed_attempts:
                print("Too many failed attempts. Stopping.")
                break
    
    return all_candles

# ============== CONFIGURATION ==============
# Set your parameters here
SYMBOL_TOKEN = "99926000"  # Nifty 50
EXCHANGE = "NSE"
INTERVAL = "ONE_MINUTE"

# Set your date range
# For maximum historical, try going back 2 years
END_DATE = datetime.datetime.now().replace(hour=15, minute=30, second=0, microsecond=0)
START_DATE = END_DATE - timedelta(days=365*5)

# Rate limiting configuration
INITIAL_DELAY = 2  # Start with 2 seconds between requests
BACKOFF_FACTOR = 2  # Double delay on rate limit errors
MAX_DELAY = 60     # Never wait more than 60 seconds


print("="*60)
print("ANGEL ONE HISTORICAL DATA FETCHER")
print("="*60)
print(f"Symbol: NIFTY 50 ({SYMBOL_TOKEN})")
print(f"Interval: {INTERVAL}")
print(f"Date Range: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
print(f"Rate Limit Protection: {INITIAL_DELAY}s initial delay")
print("="*60)

# ── CACHE CHECK: Load from disk if already fetched, else call API ──
import glob

expected_filename = f"./data/nifty_1min_{START_DATE.strftime('%Y%m%d')}_to_{END_DATE.strftime('%Y%m%d')}.csv"
existing_files    = glob.glob("./data/nifty_1min_*.csv")

if os.path.exists(expected_filename):
    # Exact match — load directly, skip API entirely
    print(f"\n✅ Spot data already exists: {expected_filename}")
    print("Loading from disk — skipping Angel One API call...")
    df = pd.read_csv(expected_filename)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df = df.sort_values('DateTime').reset_index(drop=True)

elif existing_files:
    # Found a file but date range differs — load most recent, warn user
    print(f"\n⚠️  No exact match but existing file(s) found:")
    for f in existing_files:
        print(f"   • {f}  ({os.path.getsize(f)/(1024*1024):.1f} MB)")
    latest_file = max(existing_files, key=os.path.getmtime)
    print(f"\nLoading most recent: {latest_file}")
    print("If you need a different date range, delete this file and re-run.")
    df = pd.read_csv(latest_file)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df = df.sort_values('DateTime').reset_index(drop=True)

else:
    # No file found — fetch from Angel One
    print("\nNo existing spot data found. Fetching from Angel One...")
    print("This is a one-time operation and will take several minutes.\n")

    all_data = fetch_historical_data_with_backoff(
        smart_api=smart_api,
        symbol_token=SYMBOL_TOKEN,
        exchange=EXCHANGE,
        interval=INTERVAL,
        start_date=START_DATE,
        end_date=END_DATE,
        initial_delay=INITIAL_DELAY,
        backoff_factor=BACKOFF_FACTOR,
        max_delay=MAX_DELAY
    )

    if all_data:
        columns = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = pd.DataFrame(all_data, columns=columns)
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df = df.sort_values('DateTime').reset_index(drop=True)
        df = df.drop_duplicates(subset=['DateTime']).reset_index(drop=True)

        # Save with timestamp so cache check finds it next run
        filename = f"nifty_1min_{df['DateTime'].min().strftime('%Y%m%d')}_to_{df['DateTime'].max().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)
        print(f"\nData saved to: {filename}")
    else:
        print("\nNo data was collected. Check your parameters and API connection.")
        df = pd.DataFrame()

# ── df is now always loaded regardless of which path was taken ──
if not df.empty:
    print(f"\n{'='*60}")
    print("SPOT DATA READY")
    print(f"{'='*60}")
    print(f"Total candles : {len(df):,}")
    print(f"Date range    : {df['DateTime'].min().date()} to {df['DateTime'].max().date()}")
    print(f"Days covered  : {(df['DateTime'].max() - df['DateTime'].min()).days}")
    print(f"Avg per day   : {len(df)/((df['DateTime'].max()-df['DateTime'].min()).days or 1):.1f} candles")
    print("\nFirst 5 records:") 
    print(df.head())
    print("\nLast 5 records:")
    print(df.tail())

print(f"\n{'='*60}")
print("Process completed.")

# Lets analyse best time windows.
# ==================== DATA PREPARATION ====================
# Create a copy of your existing df
analysis_df = df.copy()

# Convert DateTime column to datetime and set as index
analysis_df['DateTime'] = pd.to_datetime(analysis_df['DateTime'])
analysis_df.set_index('DateTime', inplace=True)

print(f"Dataset loaded: {len(analysis_df):,} candles from {analysis_df.index.min()} to {analysis_df.index.max()}")

# Filter only trading hours
trading_df = analysis_df.between_time('09:15', '15:30').copy()

# Calculate 5-minute rolling volatility
trading_df['Returns'] = trading_df['Close'].pct_change() * 100
trading_df['5min_Volatility'] = trading_df['Returns'].rolling(5).std()

# Add date and time columns
trading_df['Date'] = trading_df.index.date
trading_df['Time'] = trading_df.index.time

print("="*70)
print("INTRADAY-ONLY VOLATILITY EXPANSION ANALYSIS")
print("="*70)
print(f"Data Range: {trading_df.index.min()} to {trading_df.index.max()}")
print(f"Total Trading Days: {trading_df['Date'].nunique()}")

# ==================== FIND INTRADAY EXPANSION WINDOWS ====================
def find_intraday_expansion_windows(data, expansion_threshold=20):
    """Find volatility expansion windows within same trading day"""
    
    all_windows = []
    
    # Analyze each trading day separately
    for date, day_data in data.groupby('Date'):
        if len(day_data) < 50:  # Skip incomplete days
            continue
            
        # Resample to 15-minute intervals for cleaner analysis
        day_15min = day_data.resample('15T').agg({
            '5min_Volatility': 'mean',
            'Close': 'last'
        }).dropna()
        
        if len(day_15min) < 10:  # Need enough data points
            continue
        
        # Find local minima (convergence) and maxima (peak) within the day
        vol_series = day_15min['5min_Volatility'].values
        
        for i in range(2, len(vol_series) - 2):
            # Look for local minimum (potential entry)
            if (vol_series[i] < vol_series[i-1] and 
                vol_series[i] < vol_series[i-2] and
                vol_series[i] < vol_series[i+1] and
                vol_series[i] < vol_series[i+2]):
                
                # Find next local maximum (potential exit)
                for j in range(i+1, len(vol_series) - 2):
                    if (vol_series[j] > vol_series[j-1] and 
                        vol_series[j] > vol_series[j-2] and
                        vol_series[j] > vol_series[j+1] and
                        vol_series[j] > vol_series[j+2]):
                        
                        # Calculate expansion
                        expansion_pct = ((vol_series[j] - vol_series[i]) / vol_series[i] * 100) if vol_series[i] > 0 else 0
                        
                        # Only consider significant expansions within same day
                        if expansion_pct >= expansion_threshold and (j - i) >= 3:  # At least 45 minutes
                            start_time = day_15min.index[i].time()
                            end_time = day_15min.index[j].time()
                            
                            # Ensure it's within same trading session
                            if start_time < end_time:
                                all_windows.append({
                                    'Date': date,
                                    'Start_Time': start_time,
                                    'End_Time': end_time,
                                    'Start_Vol': round(vol_series[i], 4),
                                    'End_Vol': round(vol_series[j], 4),
                                    'Expansion_Pct': round(expansion_pct, 1),
                                    'Duration_Min': ((day_15min.index[j] - day_15min.index[i]).total_seconds() / 60)
                                })
                        break
    
    return pd.DataFrame(all_windows)

# Find intraday windows
windows_df = find_intraday_expansion_windows(trading_df, expansion_threshold=30)

print(f"\nFound {len(windows_df)} intraday expansion windows (same-day only)")

# ==================== ANALYZE MOST CONSISTENT WINDOWS ====================
print("\n" + "="*70)
print("MOST CONSISTENT INTRADAY WINDOWS (Top 10 by Frequency)")
print("="*70)

if not windows_df.empty:
    # Create time window strings
    windows_df['Window'] = windows_df['Start_Time'].apply(lambda x: x.strftime('%H:%M')) + ' → ' + \
                          windows_df['End_Time'].apply(lambda x: x.strftime('%H:%M'))
    
    # Group by window pattern
    window_stats = windows_df.groupby('Window').agg({
    'Expansion_Pct': ['mean', 'std'],
    'Duration_Min': 'mean',
    'Window': 'size'  # This gives integer count
    }).round(2)
    
    window_stats.columns = ['Avg_Expansion', 'Std_Expansion', 'Frequency', 'Avg_Duration']
    window_stats = window_stats.sort_values('Frequency', ascending=False)
    
    # Show top 10 most frequent windows
    print("\nTop 10 Most Consistent Windows (Occurred Most Often):")
    print("-" * 70)
    for idx, (window, stats) in enumerate(window_stats.head(10).iterrows(), 1):
       print(f"{idx:2d}. {window:15s} | Freq: {int(stats['Frequency']):3d} days | "
              f"Avg Exp: {stats['Avg_Expansion']:6.1f}% | "
              f"Duration: {stats['Avg_Duration']:3.0f} min")
    
    # ==================== BEST TIME WINDOWS BY HOUR ====================
    print("\n" + "="*70)
    print("BEST ENTRY & EXIT TIMES BY HOUR")
    print("="*70)
    
    # Best entry times (start of expansion)
    entry_stats = windows_df.groupby(windows_df['Start_Time'].apply(lambda x: x.hour)).agg({
        'Expansion_Pct': 'mean',
        'Window': 'count'
    }).rename(columns={'Window': 'Count'})
    
    print("\nBest Entry Hours (Volatility Convergence):")
    print("-" * 50)
    for hour, stats in entry_stats.sort_values('Expansion_Pct', ascending=False).head(5).iterrows():
        print(f"  {hour:02d}:00 | Avg Expansion: {stats['Expansion_Pct']:.1f}% | Occurred: {stats['Count']} times")
    
    # Best exit times (peak of expansion)
    exit_stats = windows_df.groupby(windows_df['End_Time'].apply(lambda x: x.hour)).agg({
        'Expansion_Pct': 'mean',
        'Window': 'count'
    }).rename(columns={'Window': 'Count'})
    
    print("\nBest Exit Hours (Volatility Peak):")
    print("-" * 50)
    for hour, stats in exit_stats.sort_values('Expansion_Pct', ascending=False).head(5).iterrows():
        print(f"  {hour:02d}:00 | Avg Expansion: {stats['Expansion_Pct']:.1f}% | Occurred: {stats['Count']} times")
    
    # ==================== OPTIMAL TRADING WINDOWS ====================
    print("\n" + "="*70)
    print("RECOMMENDED TRADING WINDOWS")
    print("="*70)
    
    # Find windows that occurred on at least 20% of trading days
    total_days = trading_df['Date'].nunique()
    min_frequency = total_days * 0.20  # 20% of days
    
    reliable_windows = window_stats[window_stats['Frequency'] >= min_frequency]
    
    if not reliable_windows.empty:
        print(f"\nReliable Windows (Occurred on ≥20% of trading days):")
        print("-" * 70)
        for window, stats in reliable_windows.sort_values('Avg_Expansion', ascending=False).iterrows():
            occurrence_rate = (stats['Frequency'] / total_days) * 100
            print(f"• {window:15s} | Occurrence: {occurrence_rate:.1f}% of days")
            print(f"  Avg Expansion: {stats['Avg_Expansion']:.1f}% | Duration: {stats['Avg_Duration']:.0f} min")
            print()
    else:
        print("No windows met the 20% frequency threshold")
        print(f"Highest frequency window: {window_stats.iloc[0].name} "
              f"({window_stats.iloc[0]['Frequency']}/{total_days} days = "
              f"{(window_stats.iloc[0]['Frequency']/total_days*100):.1f}%)")
    
    # ==================== VISUALIZATION ====================
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('NIFTY 50 - Intraday Volatility Expansion Patterns', 
                 fontsize=16, fontweight='bold')
    
    # 1. Window Frequency Heatmap
    if len(windows_df) > 0:
        # Create a grid for heatmap
        heatmap_data = []
        for hour in range(9, 16):
            for minute in [0, 15, 30, 45]:
                if hour == 9 and minute < 15:
                    continue
                if hour == 15 and minute > 30:
                    continue
                
                time_str = f"{hour:02d}:{minute:02d}"
                # Count how many times this time is a start or end
                start_count = len(windows_df[windows_df['Start_Time'].apply(
                    lambda x: x.strftime('%H:%M')) == time_str])
                end_count = len(windows_df[windows_df['End_Time'].apply(
                    lambda x: x.strftime('%H:%M')) == time_str])
                
                heatmap_data.append({
                    'Hour': hour,
                    'Minute': minute,
                    'Start_Count': start_count,
                    'End_Count': end_count,
                    'Total': start_count + end_count
                })
        
        heatmap_df = pd.DataFrame(heatmap_data)
        pivot_table = heatmap_df.pivot_table(index='Hour', columns='Minute', values='Total')
        
        im = axes[0, 0].imshow(pivot_table.values, aspect='auto', cmap='YlOrRd')
        axes[0, 0].set_title('Optimal Trading Times Heatmap', fontweight='bold')
        axes[0, 0].set_xlabel('Minute')
        axes[0, 0].set_ylabel('Hour')
        axes[0, 0].set_xticks(range(len([0, 15, 30, 45])))
        axes[0, 0].set_xticklabels([0, 15, 30, 45])
        axes[0, 0].set_yticks(range(len(pivot_table.index)))
        axes[0, 0].set_yticklabels([f'{h}:00' for h in pivot_table.index])
        plt.colorbar(im, ax=axes[0, 0], label='Window Count')
    
    # 2. Entry Time Distribution
    if len(windows_df) > 0:
        entry_hours = windows_df['Start_Time'].apply(lambda x: x.hour + x.minute/60)
        axes[0, 1].hist(entry_hours, bins=20, edgecolor='black', color='lightgreen', alpha=0.7)
        axes[0, 1].set_title('Entry Time Distribution', fontweight='bold')
        axes[0, 1].set_xlabel('Time of Day')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_xticks(range(9, 16))
        axes[0, 1].set_xticklabels([f'{h}:00' for h in range(9, 16)])
    
    # 3. Expansion Strength vs Duration
    if len(windows_df) > 0:
        scatter = axes[1, 0].scatter(windows_df['Duration_Min'], windows_df['Expansion_Pct'], 
                                    c=windows_df['Start_Time'].apply(lambda x: x.hour),
                                    cmap='viridis', alpha=0.6, s=50)
        axes[1, 0].set_title('Expansion Strength vs Duration', fontweight='bold')
        axes[1, 0].set_xlabel('Duration (minutes)')
        axes[1, 0].set_ylabel('Expansion (%)')
        plt.colorbar(scatter, ax=axes[1, 0], label='Entry Hour')
    
    # 4. Most Common Windows
    if len(window_stats) > 0:
        top_windows = window_stats.head(8)
        y_pos = range(len(top_windows))
        axes[1, 1].barh(y_pos, top_windows['Frequency'], color='steelblue', alpha=0.7)
        axes[1, 1].set_yticks(y_pos)
        axes[1, 1].set_yticklabels(top_windows.index)
        axes[1, 1].set_title('Most Frequent Trading Windows', fontweight='bold')
        axes[1, 1].set_xlabel('Frequency (days)')
    
    plt.tight_layout()
    plt.show()
    
    # ==================== TRADING STRATEGY ====================
    print("\n" + "="*70)
    print("DAY TRADING STRATEGY RECOMMENDATIONS")
    print("="*70)
    
    # Get the most reliable window
    if len(window_stats) > 0:
        best_window = window_stats.iloc[0]
        best_window_name = window_stats.index[0]
        start_time, end_time = best_window_name.split(' → ')
        
        print(f"\n🎯 PRIMARY STRATEGY: Trade the {best_window_name} window")
        print(f"   • Entry around: {start_time} (volatility convergence)")
        print(f"   • Exit around:  {end_time} (volatility peak)")
        print(f"   • Expected expansion: {best_window['Avg_Expansion']:.1f}%")
        print(f"   • Duration: {best_window['Avg_Duration']:.0f} minutes")
        print(f"   • Reliability: Occurs on {best_window['Frequency']} out of {total_days} days "
              f"({(best_window['Frequency']/total_days*100):.1f}%)")
    
    print("\n📊 ALTERNATIVE STRATEGIES:")
    # Show next best options
    for idx, (window, stats) in enumerate(window_stats.head(4).iterrows(), 1):
        if idx == 1:
            continue  # Skip the first one (already shown)
        start_time, end_time = window.split(' → ')
    print(f"{idx:2d}. {window:15s} | Freq: {int(stats['Frequency']):3d} days | "
          f"Avg Exp: {stats['Avg_Expansion']:6.1f}% | "
          f"Duration: {stats['Avg_Duration']:3.0f} min")
    
    print("\n⚠️  RISK MANAGEMENT:")
    print("   • Never hold positions overnight")
    print("   • Exit all positions by 15:20 (before market close)")
    print("   • Use volatility-based position sizing")
    print("   • Set stop-losses based on entry volatility levels")
    
    # Save results
    windows_df.to_csv('./analysis/intraday_expansion_windows.csv', index=False)
    print(f"\n💾 Results saved to 'intraday_expansion_windows.csv'")
    
else:
    print("No intraday expansion windows found with the current parameters.")
    print("Try adjusting the expansion_threshold parameter.")

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)

# ── Read one specific daily file ───────────────────────────────
BASE_PATH = "./data/nifty_options_raw/nifty_data/nifty_options"

def get_options_file_path(date: pd.Timestamp) -> str:
    """Construct file path from date."""
    day   = date.strftime("%d")
    month = str(date.month)       # folder is 1, 2 ... 12 (no zero padding)
    year  = date.strftime("%Y")
    fname = f"nifty_options_{day}_{month.zfill(2)}_{year}.csv"
    return os.path.join(BASE_PATH, year, month, fname)

def parse_symbol(symbol: str) -> dict:
    """
    Parse NSE symbol string into components.
    Example: NIFTY02JAN2010100PE
      → index=NIFTY, expiry=02JAN20, strike=10100, type=PE
    """
    match = re.match(r"([A-Z]+)(\d{2}[A-Z]{3}\d{2})(\d+)(CE|PE)", symbol)
    if match:
        return {
            "index"      : match.group(1),
            "expiry_str" : match.group(2),
            "strike"     : float(match.group(3)),
            "option_type": match.group(4)
        }
    return {"index": None, "expiry_str": None, "strike": None, "option_type": None}

def load_options_for_date(date: pd.Timestamp, spot: float,
                           strike_range: int = 500,
                           time_from: str = "13:45",
                           time_to:   str = "15:15",
                           verbose: bool = False) -> pd.DataFrame:
    """
    Load options data for one specific date.
    Filters to strikes within ±strike_range of spot.
    Filters to time window only.
    verbose=False suppresses per-file print output (default for backtest)
    """
    path = get_options_file_path(date)

    if not os.path.exists(path):
        if verbose:
            print(f"  ✗ File not found: {path}")
        return pd.DataFrame()


    df = pd.read_csv(path)
    if verbose:
        print(f"  ✓ Loaded {len(df):,} rows from {os.path.basename(path)}")

    # ── Filter time FIRST via string compare (zero regex cost) ───────
    tf = time_from + ":00" if len(time_from) == 5 else time_from
    tt = time_to   + ":00" if len(time_to)   == 5 else time_to
    df = df[(df["time"] >= tf) & (df["time"] <= tt)]
    if df.empty:
        return pd.DataFrame()

    # ── Parse symbol only on the surviving rows ───────────────────────
    parsed = df["symbol"].apply(parse_symbol).apply(pd.Series)
    df     = pd.concat([df, parsed], axis=1)

    # Convert time string → time object
    df["time"] = pd.to_datetime(df["time"], format="%H:%M:%S").dt.time

    # Filter strikes near spot
    df = df[(df["strike"] >= spot - strike_range) &
            (df["strike"] <= spot + strike_range)]

    # Keep only CE and PE
    df = df[df["option_type"].isin(["CE", "PE"])]

    if verbose:
        print(f"  ✓ After filtering: {len(df):,} rows")
    return df.reset_index(drop=True)

def get_nearest_expiry(options_df: pd.DataFrame, trade_date: pd.Timestamp) -> str:
    """
    From available expiries in the day's data, pick the nearest
    one that hasn't expired yet (expiry >= trade_date).
    Prefers weekly expiry over monthly automatically.
    """
    expiry_strings = options_df["expiry_str"].unique()

    expiry_dates = []
    for e in expiry_strings:
        try:
            exp_date = pd.to_datetime(e, format="%d%b%y")   
            if exp_date.date() >= trade_date.date():
                expiry_dates.append((exp_date, e))
        except:
            continue

    if not expiry_dates:
        return None

    expiry_dates.sort(key=lambda x: x[0])
    return expiry_dates[0][1]  # e.g. "07JAN21"


def find_otm_strikes(options_df: pd.DataFrame, spot: float, expiry: str) -> dict:
    """
    Given spot price and expiry, find:
      - 1-step OTM CE = first strike strictly above spot
      - 1-step OTM PE = first strike strictly below spot
    """
    exp_df    = options_df[options_df["expiry_str"] == expiry]
    strikes   = sorted(exp_df["strike"].unique())

    ce_strikes = [s for s in strikes if s > spot]
    pe_strikes = [s for s in strikes if s < spot]

    return {
        "ce_strike": min(ce_strikes) if ce_strikes else None,
        "pe_strike": max(pe_strikes) if pe_strikes else None
    }


def get_entry_ltp(opt_groups: dict, expiry: str, strike: float,
                   opt_type: str, signal_time) -> float:
    """
    Get the actual market LTP (close price) of a specific contract
    at or just after signal_time. Uses pre-grouped dict for O(1) lookup.
    """
    key = (expiry, strike, opt_type)
    grp = opt_groups.get(key)
    if grp is None:
        return None
    match = grp[grp["time"] >= signal_time]
    if match.empty:
        return None
    return match.iloc[0]["close"]

def walk_forward_pnl(opt_groups: dict, expiry: str,
                     ce_strike: float, pe_strike: float,
                     ce_entry_ltp: float, pe_entry_ltp: float,
                     signal_time,
                     spot_df: pd.DataFrame,
                     date,
                     lot_size: int = 65,
                     sl_pct: float = 0.015,
                     tp_pct: float = 0.04,
                     forced_exit_time=None,
                     peak_vol_exit: bool = True,
                     peak_lookback_mins: int = 15,
                     peak_threshold: float = 0.85) -> dict:
    """
    Walk forward minute by minute after BUYING CE + PE (long straddle).

    Buyer P&L = (ce_curr - ce_entry) + (pe_curr - pe_entry) x lot_size

    Exit conditions (first hit wins):
      1. TP        — buyer gain >= tp_pct x capital
      2. SL        — buyer loss >= sl_pct x capital
      3. PEAK_VOL  — spot expanding AND (CE at peak OR PE at peak)
                     locks profit before the winning leg reverses
      4. FORCED    — time >= forced_exit_time

    Parameters:
      spot_df           : full 1m spot DataFrame (same used in detect_consolidation)
      date              : trading date (same format as detect_consolidation)
      peak_vol_exit     : enable/disable exit (default True)
      peak_lookback_mins: rolling window in minutes for peak check (default 15)
      peak_threshold    : fraction of rolling high that triggers exit (default 0.85)
                          0.85 = current price must be within 15% of rolling high
    """

    if forced_exit_time is None:
        forced_exit_time = datetime.time(15, 25)

    total_capital = (ce_entry_ltp + pe_entry_ltp) * lot_size
    tp_trigger    =  total_capital * tp_pct
    sl_trigger    = -total_capital * sl_pct

    ce_key = (expiry, ce_strike, "CE")
    pe_key = (expiry, pe_strike, "PE")
    ce_grp = opt_groups.get(ce_key)
    pe_grp = opt_groups.get(pe_key)

    _no_data = {
        "exit_time"    : None,
        "exit_reason"  : "NO_DATA",
        "ce_exit_ltp"  : None,
        "pe_exit_ltp"  : None,
        "pnl_rs"       : 0.0,
        "pnl_pct"      : 0.0,
        "total_capital": round(total_capital, 2),
        "peak_pnl_rs"  : 0.0,
        "peak_pnl_time": None,
        "pnl_trail"    : []
    }

    if ce_grp is None or pe_grp is None:
        return _no_data

    ce_ticks     = ce_grp[ce_grp["time"] > signal_time].set_index("time")["close"]
    pe_ticks     = pe_grp[pe_grp["time"] > signal_time].set_index("time")["close"]
    common_times = sorted(set(ce_ticks.index) & set(pe_ticks.index))

    if not common_times:
        return _no_data

    peak_pnl_rs     = float('-inf')
    peak_pnl_time   = None
    pnl_trail       = []
    last_peak_check = None      # tracks last time peak vol check ran
    ce_trade_high   = float('-inf')   # highest CE premium seen since entry
    pe_trade_high   = float('-inf')   # highest PE premium seen since entry

    for t in common_times:
        ce_curr = ce_ticks[t]
        pe_curr = pe_ticks[t]
        pnl_rs  = round(((ce_curr - ce_entry_ltp) + (pe_curr - pe_entry_ltp)) * lot_size, 2)
        pnl_pct = round((pnl_rs / total_capital) * 100, 2)

        pnl_trail.append({
            "time"   : t,
            "pnl_rs" : pnl_rs,
            "pnl_pct": pnl_pct,
            "ce_ltp" : ce_curr,
            "pe_ltp" : pe_curr
        })

        if pnl_rs > peak_pnl_rs:
            peak_pnl_rs   = pnl_rs
            peak_pnl_time = t
            
        # Track highest premium seen on each leg since entry
        if ce_curr > ce_trade_high:
            ce_trade_high = ce_curr
        if pe_curr > pe_trade_high:
            pe_trade_high = pe_curr

        def _exit(reason):
            return {
                "exit_time"    : t,
                "exit_reason"  : reason,
                "ce_exit_ltp"  : ce_curr,
                "pe_exit_ltp"  : pe_curr,
                "pnl_rs"       : pnl_rs,
                "pnl_pct"      : pnl_pct,
                "total_capital": round(total_capital, 2),
                "peak_pnl_rs"  : peak_pnl_rs,
                "peak_pnl_time": peak_pnl_time,
                "pnl_trail"    : pnl_trail
            }

        # ── Exit 1: TP ──────────────────────────────────────────────
        if pnl_rs >= tp_trigger:
            return _exit("TP")

        # ── Exit 2: SL ──────────────────────────────────────────────
        if pnl_rs <= sl_trigger:
            return _exit("SL")

        '''
        # ── Exit 3: PEAK_VOL ────────────────────────────────────────
        # Conditions:
        #   - Only runs when trade is currently in profit (no point locking a loss)
        #   - Runs every 5 minutes to avoid per-tick slowdown
        #   - BOTH must be true:
        #       A. Spot expanding over last peak_lookback_mins minutes
        #       B. CE at its rolling peak  OR  PE at its rolling peak
        #          "Either" = directional explosion — one leg surges,
        #          other decays. Exit when winner is at its high.
        if peak_vol_exit and pnl_rs > 0:
            t_dt      = pd.Timestamp(f"2000-01-01 {t}")
            run_check = False

            if last_peak_check is None:
                run_check = True
            else:
                last_dt = pd.Timestamp(f"2000-01-01 {last_peak_check}")
                if (t_dt - last_dt).seconds >= 60:   # every 5 mins
                    run_check = True

            if run_check:
                last_peak_check = t

                # ── B: Is CE or PE pulling back from its trade high? ─────
                # Only exit when leg has ALREADY peaked and is NOW pulling back
                ce_at_peak = (
                    ce_trade_high > ce_entry_ltp and          # leg moved up
                    ce_curr < ce_trade_high and               # leg has pulled back (no longer at high)
                    ce_curr >= peak_threshold * ce_trade_high # but still within threshold of high
                )

                # PE at peak = market moved DOWN, PE surged — now reversing
                pe_at_peak = (
                    pe_trade_high > pe_entry_ltp and
                    pe_curr >= peak_threshold * pe_trade_high
                )

                # Either side exploding = take profit now
                if ce_at_peak or pe_at_peak:
                    return _exit("PEAK_VOL")
        '''
        # ── Exit 4: FORCED ──────────────────────────────────────────
        if t >= forced_exit_time:
            return _exit("FORCED")

    # ── End of data — exit at last available tick ───────────────────
    last_t  = common_times[-1]
    ce_curr = ce_ticks[last_t]
    pe_curr = pe_ticks[last_t]
    pnl_rs  = round(((ce_curr - ce_entry_ltp) + (pe_curr - pe_entry_ltp)) * lot_size, 2)
    return {
        "exit_time"    : last_t,
        "exit_reason"  : "FORCED",
        "ce_exit_ltp"  : ce_curr,
        "pe_exit_ltp"  : pe_curr,
        "pnl_rs"       : pnl_rs,
        "pnl_pct"      : round((pnl_rs / total_capital) * 100, 2),
        "total_capital": round(total_capital, 2),
        "peak_pnl_rs"  : peak_pnl_rs,
        "peak_pnl_time": peak_pnl_time,
        "pnl_trail"    : pnl_trail
    }

# ══════════════════════════════════════════════════════════
# STEP 5 — CONSOLIDATION DETECTOR + SMART EXPIRY SELECTION
# ══════════════════════════════════════════════════════════

def find_25_75_level(price: float) -> float:
    """
    Find the nearest 25/75 level to a given price.
    e.g. 22331 → 22325, 22,368 → 22375, 22,401 → 22375
    These are midpoints between Nifty's 50-point strikes.
    """
    # Round to nearest 25
    rounded = round(price / 25) * 25
    # Keep only X25 and X75 levels — skip X00 and X50
    if rounded % 50 == 0:
        # It's a strike level (X00 or X50) — find nearest X25/X75
        lower = rounded - 25
        upper = rounded + 25
        rounded = lower if abs(price - lower) <= abs(price - upper) else upper
    return rounded


def detect_consolidation(spot_df: pd.DataFrame, date,
                          scan_from: datetime.time = datetime.time(9, 30),
                          scan_to:   datetime.time = datetime.time(15, 0),
                          min_candles: int = 3,
                          max_distance: float = 5.0) -> dict:
    """
    New definition matching visual consolidation on 5m chart:

    1. Resample 1m data to TRUE 5m candles
    2. Slide a window of min_candles (default 3) across the day
    3. A valid consolidation window must satisfy ALL of:
       a. High-Low range of the window <= max_range_pts (tight price action)
       b. ATR of those candles <= atr_threshold (low volatility confirmed)
       c. No single candle body > body_threshold (no strong directional candle)
    4. Returns the FIRST valid window found within scan window
    5. Level = midpoint of the consolidation zone
    6. Strikes = nearest 50pt round numbers above/below midpoint
    """

    # ── Parameters ─────────────────────────────────────────
    max_range_pts  = 40.0   # entire zone must be within 40 Nifty points
    atr_threshold  = 20.0   # ATR of candles in window must be below 20
    body_threshold = 15.0   # no single candle body wider than 15pts

    # ── Filter to date and scan window ─────────────────────
    day_df = spot_df[
        (spot_df["Date"] == date) &
        (spot_df["Time"] >= scan_from) &
        (spot_df["Time"] <= scan_to)
    ].copy()

    if day_df.empty:
        return {"found": False}

    # ── Resample 1m → TRUE 5m candles ──────────────────────
    day_df = day_df.set_index("DateTime")

    # Need OHLC — resample properly
    day_5m = day_df.resample("5min").agg(
        open  = ("Open",  "first"),
        high  = ("High",  "max"),
        low   = ("Low",   "min"),
        close = ("Close", "last")
    ).dropna().reset_index()

    day_5m["Time"] = day_5m["DateTime"].dt.time
    day_5m = day_5m[
        (day_5m["Time"] >= scan_from) &
        (day_5m["Time"] <= scan_to)
    ].reset_index(drop=True)

    if len(day_5m) < min_candles:
        return {"found": False}

    # ── Compute ATR (True Range) for each candle ────────────
    # TR = max(High-Low, |High-PrevClose|, |Low-PrevClose|)
    day_5m["prev_close"] = day_5m["close"].shift(1)
    day_5m["tr"] = day_5m.apply(
        lambda r: max(
            r["high"] - r["low"],
            abs(r["high"] - r["prev_close"]) if not pd.isna(r["prev_close"]) else 0,
            abs(r["low"]  - r["prev_close"]) if not pd.isna(r["prev_close"]) else 0
        ), axis=1
    )
    day_5m["body"] = (day_5m["close"] - day_5m["open"]).abs()

    # ── Slide window across candles ─────────────────────────
    n = len(day_5m)
    for i in range(n - min_candles + 1):
        window = day_5m.iloc[i : i + min_candles]

        # Condition 1 — tight price range across all candles
        zone_high = window["high"].max()
        zone_low  = window["low"].min()
        zone_range = zone_high - zone_low
        if zone_range > max_range_pts:
            continue

        # Condition 2 — ATR below threshold for all candles
        avg_atr = window["tr"].mean()
        if avg_atr > atr_threshold:
            continue

        # Condition 3 — no strong directional candle inside
        max_body = window["body"].max()
        if max_body > body_threshold:
            continue

        # ── Valid consolidation found ───────────────────────
        # Signal fires on the LAST candle of the window
        signal_candle = window.iloc[-1]
        signal_time   = signal_candle["Time"]

        # Level = midpoint of the zone
        level_raw = (zone_high + zone_low) / 2

        # Round to nearest 50 for strike selection
        level = round(level_raw / 50) * 50

        # REPLACE WITH
        return {
            "found"       : True,
            "level"       : level,
            "level_raw"   : round(level_raw, 2),
            "zone_high"   : round(zone_high, 2),
            "zone_low"    : round(zone_low, 2),
            "zone_range"  : round(zone_range, 2),
            "avg_atr"     : round(avg_atr, 2),
            "signal_time" : signal_time,
            "ce_strike"   : level + 50,     # ← OTM call (above spot)
            "pe_strike"   : level - 50,     # ← OTM put (below spot)
            "candles_used": min_candles
        }

    return {"found": False}


def get_smart_expiry(options_df: pd.DataFrame, trade_date: pd.Timestamp) -> str:
    """
    Returns nearest expiry normally.
    On expiry day — skips current expiry, returns next one.
    Uses actual expiry dates from the options data itself.
    """
    expiry_strings = options_df["expiry_str"].unique()

    expiry_dates = []
    for e in expiry_strings:
        try:
            exp_date = pd.to_datetime(e, format="%d%b%y")
            expiry_dates.append((exp_date, e))
        except:
            continue

    expiry_dates.sort(key=lambda x: x[0])

    # Check if today is an expiry day
    today_is_expiry = any(
        exp_date.date() == trade_date.date()
        for exp_date, _ in expiry_dates
    )

    # Filter to unexpired expiries
    future_expiries = [
        (exp_date, e) for exp_date, e in expiry_dates
        if exp_date.date() >= trade_date.date()
    ]

    if not future_expiries:
        return None

    if today_is_expiry:
        # Skip today's expiry, use next one
        if len(future_expiries) >= 2:
            return future_expiries[1][1]
        else:
            return None  # No next expiry available
    else:
        return future_expiries[0][1]

# ──────────────────────────────────────────────────────────────────────
# METHOD 1 — SPOT PEAK VOLATILITY DETECTOR
# Opposite of detect_consolidation.
# Looks for a window where spot is EXPANDING — high range, high ATR,
# strong directional candles — the mirror image of tight consolidation.
# ──────────────────────────────────────────────────────────────────────

def detect_peak_volatility_spot(spot_df: pd.DataFrame, date,
                                  scan_from: datetime.time = datetime.time(9, 15),
                                  scan_to:   datetime.time = datetime.time(15, 0),
                                  min_candles: int = 3) -> dict:
    """
    Detects a peak volatility window on spot (5m candles).

    A valid peak volatility window must satisfy ALL of:
      a. High-Low range of the window >= min_range_pts  (price is spreading)
      b. ATR of those candles >= atr_threshold           (volatility confirmed)
      c. At least one candle body >= body_threshold      (directional move present)

    Returns the FIRST valid window found within scan_from → scan_to.
    Also returns the ATM strike at that moment (nearest 50).
    """

    # ── Parameters (opposite of consolidation thresholds) ──────────
    min_range_pts  = 40.0   # zone must span at least 40 pts
    atr_threshold  = 20.0   # ATR must be >= 20 (active movement)
    body_threshold = 15.0   # at least one strong directional candle

    # ── Filter to date and scan window ─────────────────────────────
    day_df = spot_df[
        (spot_df["Date"] == date) &
        (spot_df["Time"] >= scan_from) &
        (spot_df["Time"] <= scan_to)
    ].copy()

    if day_df.empty:
        return {"found": False}

    # ── Resample 1m → 5m candles ───────────────────────────────────
    day_df = day_df.set_index("DateTime")
    day_5m = day_df.resample("5min").agg(
        open  = ("Open",  "first"),
        high  = ("High",  "max"),
        low   = ("Low",   "min"),
        close = ("Close", "last")
    ).dropna().reset_index()

    day_5m["Time"] = day_5m["DateTime"].dt.time
    day_5m = day_5m[
        (day_5m["Time"] >= scan_from) &
        (day_5m["Time"] <= scan_to)
    ].reset_index(drop=True)

    if len(day_5m) < min_candles:
        return {"found": False}

    # ── Compute ATR and body ────────────────────────────────────────
    day_5m["prev_close"] = day_5m["close"].shift(1)
    day_5m["tr"] = day_5m.apply(
        lambda r: max(
            r["high"] - r["low"],
            abs(r["high"] - r["prev_close"]) if not pd.isna(r["prev_close"]) else 0,
            abs(r["low"]  - r["prev_close"]) if not pd.isna(r["prev_close"]) else 0
        ), axis=1
    )
    day_5m["body"] = (day_5m["close"] - day_5m["open"]).abs()

    # ── Slide window — find FIRST expansion window ──────────────────
    n = len(day_5m)
    for i in range(n - min_candles + 1):
        window = day_5m.iloc[i : i + min_candles]

        zone_high  = window["high"].max()
        zone_low   = window["low"].min()
        zone_range = zone_high - zone_low
        avg_atr    = window["tr"].mean()
        max_body   = window["body"].max()

        # All three must be true — wide range, high ATR, strong body
        if zone_range < min_range_pts:
            continue
        if avg_atr < atr_threshold:
            continue
        if max_body < body_threshold:
            continue

        # ── Valid peak volatility window found ──────────────────────
        signal_candle = window.iloc[-1]
        signal_time   = signal_candle["Time"]
        level_raw     = (zone_high + zone_low) / 2
        level         = round(level_raw / 50) * 50   # nearest 50 = ATM strike

        return {
            "found"       : True,
            "level"       : level,
            "level_raw"   : round(level_raw, 2),
            "zone_high"   : round(zone_high, 2),
            "zone_low"    : round(zone_low, 2),
            "zone_range"  : round(zone_range, 2),
            "avg_atr"     : round(avg_atr, 2),
            "max_body"    : round(max_body, 2),
            "signal_time" : signal_time,
            "ce_strike"   : level,   # ATM — sell at the money
            "pe_strike"   : level,
        }

    return {"found": False}


# ──────────────────────────────────────────────────────────────────────
# METHOD 2 — OPTIONS PREMIUM PEAK DETECTOR
# Checks if CE+PE combined premium is at a LOCAL HIGH in the last
# lookback window — confirming options are expensive at this moment.
# ──────────────────────────────────────────────────────────────────────

def detect_peak_volatility_options(opt_groups: dict, expiry: str,
                                    ce_strike: float, pe_strike: float,
                                    signal_time,
                                    lookback_mins: int = 15,
                                    peak_pct_threshold: float = 0.95) -> bool:
    """
    Returns True if the combined CE+PE premium at signal_time is at or near
    the rolling peak over the last lookback_mins minutes.

    Logic:
      - Fetch CE and PE close prices for last lookback_mins minutes
      - Compute combined premium at each minute
      - If current premium >= peak_pct_threshold * max(window) → options are expensive → True

    peak_pct_threshold = 0.85 means current premium must be within 15% of the
    rolling high. Tune lower (0.80) for more signals, higher (0.90) for fewer.
    """

    ce_grp = opt_groups.get((expiry, ce_strike, "CE"))
    pe_grp = opt_groups.get((expiry, pe_strike, "PE"))

    if ce_grp is None or pe_grp is None:
        return False

    sig_dt  = pd.Timestamp(f"2000-01-01 {signal_time}")
    lb_time = (sig_dt - pd.Timedelta(minutes=lookback_mins)).time()

    ce_win = ce_grp[(ce_grp["time"] >= lb_time) & (ce_grp["time"] <= signal_time)]
    pe_win = pe_grp[(pe_grp["time"] >= lb_time) & (pe_grp["time"] <= signal_time)]

    if len(ce_win) < 3 or len(pe_win) < 3:
        return False

    # Align on common times
    ce_close = ce_win.set_index("time")["close"]
    pe_close = pe_win.set_index("time")["close"]
    common   = sorted(set(ce_close.index) & set(pe_close.index))

    if len(common) < 3:
        return False

    combined = [ce_close[t] + pe_close[t] for t in common]
    current  = combined[-1]
    peak     = max(combined)

    # Current premium must be at or near the rolling peak
    return current >= peak_pct_threshold * peak

# ──────────────────────────────────────────────────────────────────────
# WALK FORWARD P&L — SHORT STRADDLE VERSION
# Mirror of walk_forward_pnl but for selling.
# Seller profits when premiums FALL (market consolidates).
# Seller loses when premiums RISE (market keeps expanding).
# Exit trigger: consolidation detected on spot OR forced exit at 15:25
# ──────────────────────────────────────────────────────────────────────

def walk_forward_pnl_short(opt_groups: dict, expiry: str,
                            ce_strike: float, pe_strike: float,
                            ce_entry_ltp: float, pe_entry_ltp: float,
                            signal_time,
                            spot_df: pd.DataFrame,
                            date,
                            lot_size: int = 65,
                            sl_pct: float = 0.015,
                            tp_pct: float = 0.04,
                            forced_exit_time=None,
                            consolidation_exit: bool = True,
                            no_rules_mode: bool = False) -> dict:
    """
    Walk forward minute by minute after SELLING CE + PE.

    P&L for seller = -(buyer P&L)
      = entry_premium - current_premium (in points)
      × lot_size (in rupees)

    Exit conditions (first hit):
      1. Consolidation detected on spot (detect_consolidation returns found=True)
         → seller wins: market stopped moving, premium decaying
      2. TP: seller gains >= tp_pct of capital (premium fully decayed)
      3. SL: seller loses >= sl_pct of capital (market kept moving hard)
      4. FORCED: 15:25 hard close regardless
    """

    if forced_exit_time is None:
        forced_exit_time = datetime.time(15, 25)

    total_capital = (ce_entry_ltp + pe_entry_ltp) * lot_size
    tp_trigger    =  total_capital * tp_pct    # seller TP — collect this much
    sl_trigger    =  total_capital * sl_pct    # seller SL — lose this much

    ce_key = (expiry, ce_strike, "CE")
    pe_key = (expiry, pe_strike, "PE")
    ce_grp = opt_groups.get(ce_key)
    pe_grp = opt_groups.get(pe_key)

    if ce_grp is None or pe_grp is None:
        return {
            "exit_time"     : None,
            "exit_reason"   : "NO_DATA",
            "ce_exit_ltp"   : None,
            "pe_exit_ltp"   : None,
            "pnl_rs"        : 0.0,
            "pnl_pct"       : 0.0,
            "total_capital" : round(total_capital, 2),
            "peak_pnl_rs"   : 0.0,
            "peak_pnl_time" : None,
            "pnl_trail"     : []
        }

    ce_ticks   = ce_grp[ce_grp["time"] > signal_time].set_index("time")["close"]
    pe_ticks   = pe_grp[pe_grp["time"] > signal_time].set_index("time")["close"]
    common_times = sorted(set(ce_ticks.index) & set(pe_ticks.index))

    if not common_times:
        return {
            "exit_time"     : None,
            "exit_reason"   : "NO_DATA",
            "ce_exit_ltp"   : None,
            "pe_exit_ltp"   : None,
            "pnl_rs"        : 0.0,
            "pnl_pct"       : 0.0,
            "total_capital" : round(total_capital, 2),
            "peak_pnl_rs"   : 0.0,
            "peak_pnl_time" : None,
            "pnl_trail"     : []
        }

    peak_pnl_rs   = float('-inf')
    peak_pnl_time = None
    pnl_trail     = []
    entry_dt      = pd.Timestamp(f"2000-01-01 {signal_time}")
    snap_15m = snap_30m = snap_45m = snap_60m = None

    # Track last consolidation check time to avoid checking every minute
    last_consol_check = None

    for t in common_times:
        ce_curr = ce_ticks[t]
        pe_curr = pe_ticks[t]

        # Seller P&L: entry premium - current premium (seller profits as premium decays)
        seller_pnl_rs  = round(((ce_entry_ltp - ce_curr) + (pe_entry_ltp - pe_curr)) * lot_size, 2)
        seller_pnl_pct = round((seller_pnl_rs / total_capital) * 100, 2)
        mins = (pd.Timestamp(f"2000-01-01 {t}") - entry_dt).total_seconds() / 60

        tick = {
            "time"       : t,
            "min_offset" : int(round(mins)),
            "pnl_rs"     : seller_pnl_rs,
            "pnl_pct"    : seller_pnl_pct,
            "ce_ltp"     : ce_curr,
            "pe_ltp"     : pe_curr
        }
        pnl_trail.append(tick)

        if snap_15m is None and mins >= 15: snap_15m = tick.copy()
        if snap_30m is None and mins >= 30: snap_30m = tick.copy()
        if snap_45m is None and mins >= 45: snap_45m = tick.copy()
        if snap_60m is None and mins >= 60: snap_60m = tick.copy()

        if seller_pnl_rs > peak_pnl_rs:
            peak_pnl_rs   = seller_pnl_rs
            peak_pnl_time = t
        '''
        # ── Exit 1: TP (premium decayed enough, seller wins) ────────
        if seller_pnl_rs >= tp_trigger:
            return {
                "exit_time"     : t,
                "exit_reason"   : "TP",
                "ce_exit_ltp"   : ce_curr,
                "pe_exit_ltp"   : pe_curr,
                "pnl_rs"        : seller_pnl_rs,
                "pnl_pct"       : seller_pnl_pct,
                "total_capital" : round(total_capital, 2),
                "peak_pnl_rs"   : peak_pnl_rs,
                "peak_pnl_time" : peak_pnl_time,
                "pnl_trail"     : pnl_trail
            }
        '''

        if not no_rules_mode:
            # ── Exit 2: SL (market kept moving, seller in pain) ──────
            if seller_pnl_rs <= -sl_trigger:
                return {
                    "exit_time"     : t,
                    "exit_reason"   : "SL",
                    "ce_exit_ltp"   : ce_curr,
                    "pe_exit_ltp"   : pe_curr,
                    "pnl_rs"        : seller_pnl_rs,
                    "pnl_pct"       : seller_pnl_pct,
                    "total_capital" : round(total_capital, 2),
                    "peak_pnl_rs"   : peak_pnl_rs,
                    "peak_pnl_time" : peak_pnl_time,
                    "pnl_trail"     : pnl_trail,
                    "snap_15m"      : snap_15m,
                    "snap_30m"      : snap_30m,
                    "snap_45m"      : snap_45m,
                    "snap_60m"      : snap_60m,
                }

        # ── Exit 3: Forced close at 15:25 ───────────────────────────
        if t >= forced_exit_time:
            return {
                "exit_time"     : t,
                "exit_reason"   : "FORCED",
                "ce_exit_ltp"   : ce_curr,
                "pe_exit_ltp"   : pe_curr,
                "pnl_rs"        : seller_pnl_rs,
                "pnl_pct"       : seller_pnl_pct,
                "total_capital" : round(total_capital, 2),
                "peak_pnl_rs"   : peak_pnl_rs,
                "peak_pnl_time" : peak_pnl_time,
                "pnl_trail"     : pnl_trail,
                "snap_15m"      : snap_15m,
                "snap_30m"      : snap_30m,
                "snap_45m"      : snap_45m,
                "snap_60m"      : snap_60m,
            }
        '''
        # ── Exit 4: Consolidation detected on spot ───────────────────
        # Check every 5 minutes to avoid slow down
        if consolidation_exit:
            t_dt = pd.Timestamp(f"2000-01-01 {t}")
            if last_consol_check is None or (t_dt - pd.Timestamp(f"2000-01-01 {last_consol_check}")).seconds >= 300:
                last_consol_check = t
                t_dt      = pd.Timestamp(f"2000-01-01 {t}")
                look_back = (t_dt - pd.Timedelta(minutes=15)).time()
                
                consol = detect_consolidation(
                    spot_df     = spot_df,
                    date        = date,
                    scan_from   = look_back,
                    scan_to     = t,
                    min_candles = 3
                )
                if consol["found"]:
                    return {
                        "exit_time"     : t,
                        "exit_reason"   : "CONSOLIDATION",
                        "ce_exit_ltp"   : ce_curr,
                        "pe_exit_ltp"   : pe_curr,
                        "pnl_rs"        : seller_pnl_rs,
                        "pnl_pct"       : seller_pnl_pct,
                        "total_capital" : round(total_capital, 2),
                        "peak_pnl_rs"   : peak_pnl_rs,
                        "peak_pnl_time" : peak_pnl_time,
                        "pnl_trail"     : pnl_trail
                    }
    '''
        # ── Exit 4: Premium rebuild detection (skipped in no_rules_mode)
        if not no_rules_mode and consolidation_exit and len(pnl_trail) >= 6:
            t_dt = pd.Timestamp(f"2000-01-01 {t}")
            if last_consol_check is None or (t_dt - pd.Timestamp(f"2000-01-01 {last_consol_check}")).seconds >= 60:
                last_consol_check = t
                recent         = pnl_trail[-6:]
                combined_now   = ce_curr + pe_curr
                combined_5m    = recent[0]['ce_ltp'] + recent[0]['pe_ltp']
                combined_mid   = recent[3]['ce_ltp'] + recent[3]['pe_ltp']
                premium_rebuilding = (
                    combined_now > combined_5m and
                    combined_now > combined_mid
                )
                if premium_rebuilding:
                    return {
                        "exit_time"     : t,
                        "exit_reason"   : "CONSOLIDATION",
                        "ce_exit_ltp"   : ce_curr,
                        "pe_exit_ltp"   : pe_curr,
                        "pnl_rs"        : seller_pnl_rs,
                        "pnl_pct"       : seller_pnl_pct,
                        "total_capital" : round(total_capital, 2),
                        "peak_pnl_rs"   : peak_pnl_rs,
                        "peak_pnl_time" : peak_pnl_time,
                        "pnl_trail"     : pnl_trail,
                        "snap_15m"      : snap_15m,
                        "snap_30m"      : snap_30m,
                        "snap_45m"      : snap_45m,
                        "snap_60m"      : snap_60m,
                    }

    # End of data — forced exit at last available tick
    last_t  = common_times[-1]
    ce_curr = ce_ticks[last_t]
    pe_curr = pe_ticks[last_t]
    seller_pnl_rs = round(((ce_entry_ltp - ce_curr) + (pe_entry_ltp - pe_curr)) * lot_size, 2)
    return {
        "exit_time"     : last_t,
        "exit_reason"   : "FORCED",
        "ce_exit_ltp"   : ce_curr,
        "pe_exit_ltp"   : pe_curr,
        "pnl_rs"        : seller_pnl_rs,
        "pnl_pct"       : round((seller_pnl_rs / total_capital) * 100, 2),
        "total_capital" : round(total_capital, 2),
        "peak_pnl_rs"   : peak_pnl_rs,
        "peak_pnl_time" : peak_pnl_time,
        "pnl_trail"     : pnl_trail,
        "snap_15m"      : snap_15m,
        "snap_30m"      : snap_30m,
        "snap_45m"      : snap_45m,
        "snap_60m"      : snap_60m,
    }

# ══════════════════════════════════════════════════════════════════════
# MT5-FORMAT XLSX CONVERTER
# Converts backtest trades_df → portfolio simulator input format
# IN row (sell) + OUT row (buy) per trade, running balance, MT5 style
# ══════════════════════════════════════════════════════════════════════

def trades_to_mt5_xlsx(trades_df: pd.DataFrame,
                       output_path: str,
                       start_capital: float = 1_000_000.0,
                       symbol: str = "NIFTY") -> pd.DataFrame:
    """
    Converts a backtest trades DataFrame into MT5-style Excel format
    compatible with portfolio-simulator.py.

    Each trade becomes TWO rows:
      Row 1 (IN)  — sell entry  | Profit = 0    | Balance = running balance
      Row 2 (OUT) — buy exit    | Profit = pnl  | Balance = updated balance

    Parameters:
      trades_df    : your backtest output DataFrame (trades_6 / trades_5)
      output_path  : full path to save the .xlsx file
      start_capital: starting balance (default ₹10,00,000)
      symbol       : instrument name shown in Symbol column

    Returns:
      mt5_df : the formatted DataFrame (also saved to output_path)
    """

    import openpyxl

    rows    = []
    deal_id = 2           # MT5 deal IDs start at 2
    order   = 2           # order ID mirrors deal ID
    balance = start_capital

    # Sort by date + signal_time to ensure chronological order
    df = trades_df.copy()
    df["datetime_entry"] = pd.to_datetime(df["date"].astype(str) + " " + df["signal_time"].astype(str))
    df["datetime_exit"]  = pd.to_datetime(df["date"].astype(str) + " " + df["exit_time"].astype(str))
    df = df.sort_values("datetime_entry").reset_index(drop=True)

    for _, t in df.iterrows():
        pnl      = float(t["pnl_rs"])
        prem     = float(t["combined_prem"])
        strike   = int(t["level"])
        expiry   = str(t["expiry"])
        reason   = str(t["exit_reason"])

        # Format expiry comment (e.g. "04JAN24")
        try:
            exp_dt      = pd.to_datetime(expiry, dayfirst=True)
            expiry_str  = exp_dt.strftime("%d%b%y").upper()
        except Exception:
            expiry_str  = expiry[:7].upper()

        # ── IN row (sell entry) ──────────────────────────────────────
        rows.append({
            "Time"       : t["datetime_entry"].strftime("%Y.%m.%d %H:%M:%S"),
            "Deal"       : deal_id,
            "Symbol"     : symbol,
            "Type"       : "sell",
            "Direction"  : "in",
            "Volume"     : round(prem, 2),
            "Price"      : strike,
            "Order"      : order,
            "Commission" : 0,
            "Swap"       : 0,
            "Profit"     : 0,
            "Balance"    : f"{balance:,.2f}".replace(",", " "),
            "Comment"    : f"CE {strike} PE {strike} | {expiry_str}",
        })
        deal_id += 1
        order   += 1

        # ── OUT row (buy exit) ───────────────────────────────────────
        balance += pnl
        rows.append({
            "Time"       : t["datetime_exit"].strftime("%Y.%m.%d %H:%M:%S"),
            "Deal"       : deal_id,
            "Symbol"     : symbol,
            "Type"       : "buy",
            "Direction"  : "out",
            "Volume"     : round(prem, 2),
            "Price"      : strike,
            "Order"      : order,
            "Commission" : 0,
            "Swap"       : 0,
            "Profit"     : round(pnl, 2),
            "Balance"    : f"{balance:,.2f}".replace(",", " "),
            "Comment"    : f"{reason} | pnl {pnl:+.0f}",
        })
        deal_id += 1
        order   += 1

    mt5_df = pd.DataFrame(rows)

    # Save to xlsx
    mt5_df.to_excel(output_path, index=False, sheet_name="Consolidated Trades")
    print(f"✅ MT5 portfolio file saved → {output_path}")
    print(f"   Trades : {len(df)} | Rows : {len(mt5_df)} | Final balance : ₹{balance:,.2f}")

    return mt5_df

# ── TEST: Load one day ──────────────────────────────────────────
test_date = pd.Timestamp("2021-01-04")  # First trading day of 2021
test_spot = 14000                        # Approximate Nifty level Jan 2021

print("="*55)
print(f"TEST: Loading options for {test_date.date()}")
print(f"Spot reference: {test_spot}")
print("="*55)

options_df = load_options_for_date(test_date, test_spot)

if not options_df.empty:
    print(f"\nSample data:")
    print(options_df.head(10).to_string())
    print(f"\nStrikes available : {sorted(options_df['strike'].unique())}")
    print(f"Option types      : {options_df['option_type'].unique().tolist()}")
    print(f"Time range        : {options_df['time'].min()} → {options_df['time'].max()}")
    print("\n✅ File reader working — spot df is preserved, options loaded in options_df")
    
# ── STEP 2 TEST: Entry logic for one signal day ────────────────
test_date_2   = pd.Timestamp("2021-01-04")
test_spot_2   = 14000.0
signal_time_2 = pd.to_datetime("14:00:00").time()

print("\n" + "="*55)
print("STEP 2: ENTRY LOGIC TEST")
print(f"Date        : {test_date_2.date()}")
print(f"Spot        : {test_spot_2}")
print(f"Signal Time : {signal_time_2}")
print("="*55)

# Reuse options_df already loaded above — same date, no re-read needed
if not options_df.empty:
    # 2a: Find nearest expiry
    expiry = get_nearest_expiry(options_df, test_date_2)
    print(f"\nNearest expiry found : {expiry}")

    # 2b: Find 1-step OTM strikes
    strikes   = find_otm_strikes(options_df, test_spot_2, expiry)
    ce_strike = strikes["ce_strike"]
    pe_strike = strikes["pe_strike"]
    print(f"1-step OTM CE strike : {ce_strike}")
    print(f"1-step OTM PE strike : {pe_strike}")

    # 2c: Get entry LTP for both legs
    ce_ltp = get_entry_ltp(options_df, expiry, ce_strike, "CE", signal_time_2)
    pe_ltp = get_entry_ltp(options_df, expiry, pe_strike, "PE", signal_time_2)
    print(f"\nCE entry LTP         : {ce_ltp}")
    print(f"PE entry LTP         : {pe_ltp}")

    if ce_ltp and pe_ltp:
        entry_premium = round(ce_ltp + pe_ltp, 2)
        sl_level      = round(entry_premium * (1 - 0.025), 2)
        tp_level      = round(entry_premium * (1 + 0.050), 2)

        print(f"\nEntry premium (CE+PE) : ₹{entry_premium}")
        print(f"SL level  (-2.5%)     : ₹{sl_level}")
        print(f"TP level  (+5.0%)     : ₹{tp_level}")
        print(f"\n✅ STEP 2 COMPLETE — entry logic working")
    else:
        print("✗ Could not find LTP for one or both legs — check strike/expiry availability")
else:
    print("✗ options_df is empty — re-check Step 1 file reader")
    
# ── STEP 3 TEST: Forward P&L Walk ─────────────────────────────
print("\n" + "="*55)
print("STEP 3: FORWARD P&L WALK TEST (Rupee P&L)")
print("="*55)

LOT_SIZE = 65   # ← change to 75 if testing pre-Nov-2024 data

if ce_ltp and pe_ltp:
    total_capital = (ce_ltp + pe_ltp) * LOT_SIZE
    print(f"\nCE entry LTP   : ₹{ce_ltp}  × {LOT_SIZE} lots = ₹{ce_ltp * LOT_SIZE:,.2f}")
    print(f"PE entry LTP   : ₹{pe_ltp}  × {LOT_SIZE} lots = ₹{pe_ltp * LOT_SIZE:,.2f}")
    print(f"Total capital  : ₹{total_capital:,.2f}")
    print(f"TP trigger     : +₹{total_capital * 0.05:,.2f}  (+5%)")
    print(f"SL trigger     : -₹{total_capital * 0.025:,.2f} (-2.5%)")

    result = walk_forward_pnl(
        options_df   = options_df,
        expiry       = expiry,
        ce_strike    = ce_strike,
        pe_strike    = pe_strike,
        ce_entry_ltp = ce_ltp,
        pe_entry_ltp = pe_ltp,
        signal_time  = signal_time_2,
        lot_size     = LOT_SIZE
    )

    print(f"\nExit time      : {result['exit_time']}")
    print(f"Exit reason    : {result['exit_reason']}")
    print(f"CE exit LTP    : ₹{result['ce_exit_ltp']}")
    print(f"PE exit LTP    : ₹{result['pe_exit_ltp']}")
    print(f"P&L (₹)        : ₹{result['pnl_rs']:,.2f}")
    print(f"P&L (%%)        : {result['pnl_pct']}%")
    print(f"\n✅ STEP 3 COMPLETE — rupee P&L walk working")
else:
    print("✗ Skipping Step 3 — no valid entry from Step 2")
  
'''
# ══════════════════════════════════════════════════════════
# STEP 4 BACKTEST LOOP — Consolidation + Smart Expiry
# ══════════════════════════════════════════════════════════
import datetime

# Replace with

# BACKTEST_START_5 = pd.Timestamp("2021-02-15")
# BACKTEST_END_5   = pd.Timestamp("2024-10-31")
# BACKTEST_START_5 = pd.Timestamp("2024-01-01")
# BACKTEST_END_5   = pd.Timestamp("2024-01-31") 

BACKTEST_START_5 = pd.Timestamp("2021-02-15")
BACKTEST_END_5   = pd.Timestamp("2024-10-31") 
SIGNAL_SCAN_FROM = datetime.time(14, 00)
SIGNAL_SCAN_TO   = datetime.time(15, 15)
LOT_SIZE_5       = 65
NUM_LOTS         = 4
EFFECTIVE_LOTS   = LOT_SIZE_5 * NUM_LOTS   # 260

# Prepare clean spot df
spot_clean_5 = df.copy()
spot_clean_5["DateTime"] = spot_clean_5["DateTime"].dt.tz_localize(None)
spot_clean_5["Date"]     = spot_clean_5["DateTime"].dt.date
spot_clean_5["Time"]     = spot_clean_5["DateTime"].dt.time
spot_clean_5             = spot_clean_5.set_index("DateTime").between_time("09:15", "15:30").reset_index().copy()

# Get all unique trading dates in range
all_dates = sorted(spot_clean_5[
    (spot_clean_5["Date"] >= BACKTEST_START_5.date()) &
    (spot_clean_5["Date"] <= BACKTEST_END_5.date())
]["Date"].unique())

print("="*55)
print("STEP 5: BACKTEST — CONSOLIDATION + SMART EXPIRY")
print("="*55)
print(f"Period         : {BACKTEST_START_5.date()} → {BACKTEST_END_5.date()}")
print(f"Lot size       : {LOT_SIZE_5} × {NUM_LOTS} lots = {EFFECTIVE_LOTS} units")
print(f"Scan window    : {SIGNAL_SCAN_FROM} → {SIGNAL_SCAN_TO}")
print(f"Consolidation  : ±5pts of 25/75 level, min 3 candles")
print(f"Expiry rule    : Next expiry on expiry day")
print(f"SL / TP        : -2.5% / +5% of capital deployed")
print(f"Trading days   : {len(all_dates)}")

# ═══════════════════════════════════════════════════════════════
# REPLACE EVERYTHING FROM "trades_5 = []" DOWN TO
# (BUT NOT INCLUDING) "# ── Results ───..." WITH THIS BLOCK
# ═══════════════════════════════════════════════════════════════

trades_5  = []
skipped_5 = []
trails_5  = []

for date in tqdm(all_dates, desc="Step 5"):
    trade_date   = pd.Timestamp(date)
    scan_from    = SIGNAL_SCAN_FROM
    trades_today = 0

    # ── Get midday spot for options loading ─────────────────
    day_spot = spot_clean_5[spot_clean_5["Date"] == date]
    if day_spot.empty:
        skipped_5.append({"date": date, "reason": "no_spot_data"})
        continue
    spot_ref = day_spot["Close"].iloc[len(day_spot) // 2]

    # ── Load options once per day ────────────────────────────
    opt_df_5 = load_options_for_date(
        date         = trade_date,
        spot         = spot_ref,
        strike_range = 500,
        time_from    = "09:15",
        time_to      = "15:15"
    )

    if opt_df_5.empty:
        skipped_5.append({"date": date, "reason": "no_options_file"})
        continue

    # ── Pre-group once per day — KEY PERFORMANCE FIX ────────
    # Instead of doing full 14k-row boolean scans on every lookup,
    # we group by (expiry, strike, option_type) once and cache it.
    # All subsequent lookups are O(group_size ~200) not O(14,000).
    opt_groups_5 = {
        key: grp.sort_values("time").reset_index(drop=True)
        for key, grp in opt_df_5.groupby(["expiry_str", "strike", "option_type"])
    }

    # ── Smart expiry once per day ────────────────────────────
    expiry_5 = get_smart_expiry(opt_df_5, trade_date)
    if expiry_5 is None:
        skipped_5.append({"date": date, "reason": "no_expiry"})
        continue

    # ── Track levels traded today (local, faster than scanning trades_5) ──
    levels_traded_today = set()

    # ── Multiple entry loop ──────────────────────────────────
    while True:

        signal = detect_consolidation(
            spot_df     = spot_clean_5,
            date        = date,
            scan_from   = scan_from,
            scan_to     = SIGNAL_SCAN_TO,
            min_candles = 3
        )

        if not signal["found"]:
            if trades_today == 0:
                skipped_5.append({"date": date, "reason": "no_consolidation"})
            break

        signal_time = signal["signal_time"]
        level       = signal["level"]
        ce_stk_5    = signal["ce_strike"]
        pe_stk_5    = signal["pe_strike"]

        # 2. Same level re-entry block
        if level in levels_traded_today:
            skipped_5.append({"date": date, "reason": "same_level_reentry"})
            scan_from = (pd.Timestamp(f"2000-01-01 {signal_time}") +
                        pd.Timedelta(minutes=3)).time()
            continue

        # 3. Entry LTP — now uses opt_groups_5 (fast dict lookup)
        ce_ltp_5 = get_entry_ltp(opt_groups_5, expiry_5, ce_stk_5, "CE", signal_time)
        pe_ltp_5 = get_entry_ltp(opt_groups_5, expiry_5, pe_stk_5, "PE", signal_time)

        if ce_ltp_5 is None or pe_ltp_5 is None:
            skipped_5.append({"date": date, "reason": "no_entry_ltp"})
            scan_from = (pd.Timestamp(f"2000-01-01 {signal_time}") +
                        pd.Timedelta(minutes=3)).time()
            continue

        # ── Premium imbalance filter ────────────────────────────
        avg_prem  = (ce_ltp_5 + pe_ltp_5) / 2
        prem_diff = abs(ce_ltp_5 - pe_ltp_5) / avg_prem

        if prem_diff >= 0.30:
            skipped_5.append({"date": date, "reason": "premium_imbalance"})
            scan_from = (pd.Timestamp(f"2000-01-01 {signal_time}") +
                        pd.Timedelta(minutes=3)).time()
            continue

        # ── Options premium consolidation filter ────────────────
        # Uses pre-grouped data — no full DataFrame scan
        sig_dt  = pd.Timestamp(f"2000-01-01 {signal_time}")
        lb_time = (sig_dt - pd.Timedelta(minutes=10)).time()

        ce_grp_data = opt_groups_5.get((expiry_5, ce_stk_5, "CE"))
        pe_grp_data = opt_groups_5.get((expiry_5, pe_stk_5, "PE"))

        if ce_grp_data is None or pe_grp_data is None:
            skipped_5.append({"date": date, "reason": "insufficient_option_data"})
            scan_from = (pd.Timestamp(f"2000-01-01 {signal_time}") +
                        pd.Timedelta(minutes=3)).time()
            continue

        ce_window = ce_grp_data[(ce_grp_data["time"] >= lb_time) & (ce_grp_data["time"] < signal_time)]
        pe_window = pe_grp_data[(pe_grp_data["time"] >= lb_time) & (pe_grp_data["time"] < signal_time)]

        if len(ce_window) < 5 or len(pe_window) < 5:
            skipped_5.append({"date": date, "reason": "insufficient_option_data"})
            scan_from = (pd.Timestamp(f"2000-01-01 {signal_time}") +
                        pd.Timedelta(minutes=3)).time()
            continue

        # Use HIGH and LOW — captures wicks going outside zone
        ce_range = (ce_window["high"].max() - ce_window["low"].min()) / ce_window["close"].mean() * 100
        pe_range = (pe_window["high"].max() - pe_window["low"].min()) / pe_window["close"].mean() * 100

        if ce_range > 10.0 or pe_range > 10.0:
            skipped_5.append({"date": date, "reason": "options_not_consolidating"})
            scan_from = (pd.Timestamp(f"2000-01-01 {signal_time}") +
                        pd.Timedelta(minutes=3)).time()
            continue

        # 6. Enter trade — now uses opt_groups_5 (fast dict lookup)
        result_5 = walk_forward_pnl(
            opt_groups         = opt_groups_5,
            expiry             = expiry_5,
            ce_strike          = ce_stk_5,
            pe_strike          = pe_stk_5,
            ce_entry_ltp       = ce_ltp_5,
            pe_entry_ltp       = pe_ltp_5,
            signal_time        = signal_time,
            spot_df            = spot_clean_5,      # ← NEW
            date               = date,              # ← NEW
            lot_size           = EFFECTIVE_LOTS,
            sl_pct             = 1,
            tp_pct             = 0.30,
            peak_vol_exit      = True,              # ← NEW — set False to compare
            peak_lookback_mins = 15,                # ← NEW
            peak_threshold     = 0.95               # ← NEW
        )

        levels_traded_today.add(level)

        trades_5.append({
            "date"          : date,
            "trade_num"     : trades_today + 1,
            "level"         : level,
            "spot_at_entry" : level,
            "signal_time"   : signal_time,
            "expiry"        : expiry_5,
            "ce_strike"     : ce_stk_5,
            "pe_strike"     : pe_stk_5,
            "ce_entry_ltp"  : ce_ltp_5,
            "pe_entry_ltp"  : pe_ltp_5,
            "ce_range_pct"  : round(ce_range, 2),
            "pe_range_pct"  : round(pe_range, 2),
            "total_capital" : result_5["total_capital"],
            "exit_time"     : result_5["exit_time"],
            "exit_reason"   : result_5["exit_reason"],
            "ce_exit_ltp"   : result_5["ce_exit_ltp"],
            "pe_exit_ltp"   : result_5["pe_exit_ltp"],
            "pnl_rs"        : result_5["pnl_rs"],
            "pnl_pct"       : result_5["pnl_pct"],
            "peak_pnl_rs"   : result_5.get("peak_pnl_rs", 0),
            "peak_pnl_time" : result_5.get("peak_pnl_time", None)
        })

        # 7. Trail collection
        for tick in result_5.get("pnl_trail", []):
            trails_5.append({
                "date"        : date,
                "trade_num"   : trades_today + 1,
                "signal_time" : signal_time,
                "exit_reason" : result_5["exit_reason"],
                "exit_time"   : result_5["exit_time"],
                "peak_pnl_rs" : result_5.get("peak_pnl_rs", 0),
                "time"        : tick["time"],
                "pnl_rs"      : tick["pnl_rs"],
                "pnl_pct"     : tick["pnl_pct"],
                "ce_ltp"      : tick["ce_ltp"],
                "pe_ltp"      : tick["pe_ltp"]
            })

        trades_today += 1

        # 8. Set next scan start after this trade exits
        exit_time = result_5["exit_time"]
        if exit_time is None:
            break

        exit_dt   = pd.Timestamp(f"2000-01-01 {exit_time}")
        scan_end  = pd.Timestamp(f"2000-01-01 {SIGNAL_SCAN_TO}")
        remaining = (scan_end - exit_dt).total_seconds() / 60

        if remaining < 30:
            break

        scan_from = (exit_dt + pd.Timedelta(minutes=1)).time()

# ── Results ─────────────────────────────────────────────────

trades_df_5  = pd.DataFrame(trades_5)
skipped_df_5 = pd.DataFrame(skipped_5)

print(f"\n{'='*55}")
print(f"STEP 5 BACKTEST COMPLETE")
print(f"{'='*55}")
print(f"Total days     : {len(all_dates)}")
print(f"Trades entered : {len(trades_df_5)}")
print(f"Days skipped   : {len(skipped_df_5)}")

if not skipped_df_5.empty:
    print(f"\nSkip reasons:")
    print(skipped_df_5["reason"].value_counts().to_string())

if not trades_df_5.empty:
    wins     = trades_df_5[trades_df_5["pnl_rs"] > 0]
    losses   = trades_df_5[trades_df_5["pnl_rs"] <= 0]
    win_rate = round(len(wins) / len(trades_df_5) * 100, 1)

    print(f"\n--- PERFORMANCE SUMMARY ---")
    print(f"Win rate          : {win_rate}%")
    print(f"Total P&L (₹)     : ₹{trades_df_5['pnl_rs'].sum():,.2f}")
    print(f"Avg P&L / trade   : ₹{trades_df_5['pnl_rs'].mean():,.2f}")
    print(f"Best trade        : ₹{trades_df_5['pnl_rs'].max():,.2f}")
    print(f"Worst trade       : ₹{trades_df_5['pnl_rs'].min():,.2f}")
    print(f"Avg capital / day : ₹{trades_df_5['total_capital'].mean():,.2f}")

    print(f"\nExit reasons:")
    print(trades_df_5["exit_reason"].value_counts().to_string())

    # Monthly P&L breakdown
    trades_df_5["month"] = pd.to_datetime(trades_df_5["date"]).dt.to_period("M")
    monthly = trades_df_5.groupby("month")["pnl_rs"].sum()
    print(f"\nMonthly P&L:")
    print(monthly.to_string())

    # Save
    _s5 = BACKTEST_START_5.strftime("%Y%m%d")
    _e5 = BACKTEST_END_5.strftime("%Y%m%d")

    _trades_file_5   = f"long-straddle-{_s5}-{_e5}-backtest-trades.csv"
    _trail_file_5    = f"long-straddle-{_s5}-{_e5}-pnl-trail.csv"
    _portfolio_file_5 = f"long-straddle-{_s5}-{_e5}-portfolio.xlsx"

    trades_df_5.to_csv(_trades_file_5, index=False)
    print(f"\n✅ Trade log saved to {_trades_file_5}")
  
    trail_df = pd.DataFrame(trails_5)
    trail_df.to_csv(_trail_file_5, index=False)
    print(f"✅ P&L trail saved to {_trail_file_5}")
  
    trades_to_mt5_xlsx(
        trades_df     = trades_df_5,
        output_path   = _portfolio_file_5,
        start_capital = 1_000_000,
        symbol        = "NIFTY"
    )
else:
    print("No trades entered — check consolidation parameters")

'''


# ══════════════════════════════════════════════════════════════════════
# STEP 5 — VOLATILITY SHORT BACKTEST
# Paste this block AFTER your existing Step 5 results section.
# Uses the same spot_clean_5, options loader, and expiry logic.
# ══════════════════════════════════════════════════════════════════════

"""
BACKTEST_START_5 = pd.Timestamp("2021-02-15")
BACKTEST_END_5   = pd.Timestamp("2024-10-31")


BACKTEST_START_5 = pd.Timestamp("2024-01-01")
BACKTEST_END_5   = pd.Timestamp("2024-01-31") 
"""

# ── Config ────────────────────────────────────────────────────────────
BACKTEST_START_6  = pd.Timestamp("2021-02-15")
BACKTEST_END_6    = pd.Timestamp("2024-10-31")

VOL_SCAN_FROM     = datetime.time(9, 15)    # full day scan for analysis
VOL_SCAN_TO       = datetime.time(10, 30)   # last entry allowed at 10:30 AM
VOL_FORCED_EXIT   = datetime.time(15, 28)   # hard close — full day theta capture

LOT_SIZE_6        = 65
NUM_LOTS_6        = 4
EFFECTIVE_LOTS_6  = LOT_SIZE_6 * NUM_LOTS_6   # 260

# ── Peak vol filter parameters ────────────────────────────────────────
VOL_LOOKBACK_MINS = 15    # how far back to look for premium peak
VOL_PEAK_PCT      = 0.85  # premium must be within 15% of rolling high
VOL_SL_PCT        = 0.015 # 1.5% of capital
VOL_TP_PCT        = 0.04  # 4.0% of capital (same as long side)
NO_RULES_MODE_6   = True  # True → collect raw trails; False → live SL/TP/consol exits

# ── Build spot_clean_5 if Step 5 was skipped ─────────────────────────
if "spot_clean_5" not in dir():
    spot_clean_5 = df.copy()
    spot_clean_5["DateTime"] = pd.to_datetime(spot_clean_5["DateTime"]).dt.tz_localize(None)
    spot_clean_5["Date"]     = spot_clean_5["DateTime"].dt.date
    spot_clean_5["Time"]     = spot_clean_5["DateTime"].dt.time
    spot_clean_5             = (spot_clean_5
                                 .set_index("DateTime")
                                 .between_time("09:15", "15:30")
                                 .reset_index()
                                 .copy())

all_dates_6 = sorted(spot_clean_5[
    (spot_clean_5["Date"] >= BACKTEST_START_6.date()) &
    (spot_clean_5["Date"] <= BACKTEST_END_6.date())
]["Date"].unique())

print("\n" + "="*58)
print("STEP 6: VOLATILITY SHORT BACKTEST")
print("="*58)
print(f"Period         : {BACKTEST_START_6.date()} → {BACKTEST_END_6.date()}")
print(f"Lot size       : {LOT_SIZE_6} × {NUM_LOTS_6} lots = {EFFECTIVE_LOTS_6} units")
print(f"Scan window    : {VOL_SCAN_FROM} → {VOL_SCAN_TO}  (full day for analysis)")
print(f"Forced exit    : {VOL_FORCED_EXIT}")
print(f"Strategy       : Sell ATM CE + PE on peak volatility")
print(f"Exit trigger   : Consolidation detected OR TP/SL/Forced")
print(f"SL / TP        : -{VOL_SL_PCT*100:.1f}% / +{VOL_TP_PCT*100:.1f}% of capital")
print(f"Trading days   : {len(all_dates_6)}")

trades_6  = []
skipped_6 = []
trails_6  = []

for date in tqdm(all_dates_6, desc="Step 6 Vol Short"):
    trade_date   = pd.Timestamp(date)
    scan_from    = VOL_SCAN_FROM
    trades_today = 0

    # ── Spot data for this day ────────────────────────────────────
    day_spot = spot_clean_5[spot_clean_5["Date"] == date]
    if day_spot.empty:
        skipped_6.append({"date": date, "reason": "no_spot_data"})
        continue
    spot_ref = day_spot["Close"].iloc[len(day_spot) // 2]

    # ── Load options once per day ─────────────────────────────────
    opt_df_6 = load_options_for_date(
        date         = trade_date,
        spot         = spot_ref,
        strike_range = 500,
        time_from    = "09:15",
        time_to      = "15:25"
    )

    if opt_df_6.empty:
        skipped_6.append({"date": date, "reason": "no_options_file"})
        continue

    # ── Pre-group once per day ────────────────────────────────────
    opt_groups_6 = {
        key: grp.sort_values("time").reset_index(drop=True)
        for key, grp in opt_df_6.groupby(["expiry_str", "strike", "option_type"])
    }

    # ── Smart expiry ──────────────────────────────────────────────
    expiry_6 = get_smart_expiry(opt_df_6, trade_date)
    if expiry_6 is None:
        skipped_6.append({"date": date, "reason": "no_expiry"})
        continue

    levels_traded_today_6 = set()

    # ── Entry scan loop ───────────────────────────────────────────
    while True:

        # ── FILTER 1: Spot peak volatility ───────────────────────
        vol_signal = detect_peak_volatility_spot(
            spot_df     = spot_clean_5,
            date        = date,
            scan_from   = scan_from,
            scan_to     = VOL_SCAN_TO,
            min_candles = 3
        )

        if not vol_signal["found"]:
            if trades_today == 0:
                skipped_6.append({"date": date, "reason": "no_peak_volatility"})
            break

        signal_time = vol_signal["signal_time"]
        level       = vol_signal["level"]
        ce_stk_6    = vol_signal["ce_strike"]   # ATM
        pe_stk_6    = vol_signal["pe_strike"]   # ATM

        # ── Same level block ──────────────────────────────────────
        if level in levels_traded_today_6:
            skipped_6.append({"date": date, "reason": "same_level_reentry"})
            scan_from = (pd.Timestamp(f"2000-01-01 {signal_time}") +
                         pd.Timedelta(minutes=3)).time()
            continue

        # ── Get entry LTP ─────────────────────────────────────────
        ce_ltp_6 = get_entry_ltp(opt_groups_6, expiry_6, ce_stk_6, "CE", signal_time)
        pe_ltp_6 = get_entry_ltp(opt_groups_6, expiry_6, pe_stk_6, "PE", signal_time)

        if ce_ltp_6 is None or pe_ltp_6 is None:
            skipped_6.append({"date": date, "reason": "no_entry_ltp"})
            scan_from = (pd.Timestamp(f"2000-01-01 {signal_time}") +
                         pd.Timedelta(minutes=3)).time()
            continue

        # ── FILTER 2: Options premium at peak ─────────────────────
        options_at_peak = detect_peak_volatility_options(
            opt_groups         = opt_groups_6,
            expiry             = expiry_6,
            ce_strike          = ce_stk_6,
            pe_strike          = pe_stk_6,
            signal_time        = signal_time,
            lookback_mins      = VOL_LOOKBACK_MINS,
            peak_pct_threshold = VOL_PEAK_PCT
        )

        if not options_at_peak:
            skipped_6.append({"date": date, "reason": "options_not_at_peak"})
            scan_from = (pd.Timestamp(f"2000-01-01 {signal_time}") +
                         pd.Timedelta(minutes=3)).time()
            continue

        # ── Premium imbalance filter ──────────────────────────────
        avg_prem  = (ce_ltp_6 + pe_ltp_6) / 2
        prem_diff = abs(ce_ltp_6 - pe_ltp_6) / avg_prem

        if prem_diff >= 0.30:
            skipped_6.append({"date": date, "reason": "premium_imbalance"})
            scan_from = (pd.Timestamp(f"2000-01-01 {signal_time}") +
                         pd.Timedelta(minutes=3)).time()
            continue

        # ── ENTER — Sell ATM straddle ─────────────────────────────
        result_6 = walk_forward_pnl_short(
            opt_groups        = opt_groups_6,
            expiry            = expiry_6,
            ce_strike         = ce_stk_6,
            pe_strike         = pe_stk_6,
            ce_entry_ltp      = ce_ltp_6,
            pe_entry_ltp      = pe_ltp_6,
            signal_time       = signal_time,
            spot_df           = spot_clean_5,
            date              = date,
            lot_size          = EFFECTIVE_LOTS_6,
            sl_pct            = VOL_SL_PCT,
            tp_pct            = VOL_TP_PCT,
            forced_exit_time  = VOL_FORCED_EXIT,
            consolidation_exit= True,
            no_rules_mode     = NO_RULES_MODE_6
        )

        levels_traded_today_6.add(level)

        # ── Log trade ─────────────────────────────────────────────
        trades_6.append({
            "date"          : date,
            "trade_num"     : trades_today + 1,
            "level"         : level,
            "spot_at_entry" : level,
            "signal_time"   : signal_time,
            "signal_hour"   : pd.Timestamp(f"2000-01-01 {signal_time}").hour,
            "expiry"        : expiry_6,
            "ce_strike"     : ce_stk_6,
            "pe_strike"     : pe_stk_6,
            "ce_entry_ltp"  : ce_ltp_6,
            "pe_entry_ltp"  : pe_ltp_6,
            "combined_prem" : round(ce_ltp_6 + pe_ltp_6, 2),
            "zone_range"    : vol_signal["zone_range"],
            "avg_atr"       : vol_signal["avg_atr"],
            "max_body"      : vol_signal["max_body"],
            "total_capital" : result_6["total_capital"],
            "exit_time"     : result_6["exit_time"],
            "exit_reason"   : result_6["exit_reason"],
            "ce_exit_ltp"   : result_6["ce_exit_ltp"],
            "pe_exit_ltp"   : result_6["pe_exit_ltp"],
            "pnl_rs"        : result_6["pnl_rs"],
            "pnl_pct"       : result_6["pnl_pct"],
            "peak_pnl_rs"   : result_6.get("peak_pnl_rs", 0),
            "peak_pnl_time" : result_6.get("peak_pnl_time", None),
            "month"         : pd.Timestamp(str(date)).to_period("M")
        })

        # ── Log trail ─────────────────────────────────────────────
        for tick in result_6.get("pnl_trail", []):
            trails_6.append({
                "date"        : date,
                "trade_num"   : trades_today + 1,
                "signal_time" : signal_time,
                "signal_hour" : pd.Timestamp(f"2000-01-01 {signal_time}").hour,
                "exit_reason" : result_6["exit_reason"],
                "exit_time"   : result_6["exit_time"],
                "peak_pnl_rs" : result_6.get("peak_pnl_rs", 0),
                "time"        : tick["time"],
                "min_offset"  : tick.get("min_offset", None),
                "pnl_rs"      : tick["pnl_rs"],
                "pnl_pct"     : tick["pnl_pct"],
                "ce_ltp"      : tick["ce_ltp"],
                "pe_ltp"      : tick["pe_ltp"]
            })

        trades_today += 1

        # ── Next scan starts after this trade exits ───────────────
        exit_time = result_6["exit_time"]
        if exit_time is None:
            break

        exit_dt   = pd.Timestamp(f"2000-01-01 {exit_time}")
        scan_end  = pd.Timestamp(f"2000-01-01 {VOL_SCAN_TO}")
        remaining = (scan_end - exit_dt).total_seconds() / 60

        if remaining < 15:   # shorter buffer — 15 min left? done for day
            break

        scan_from = (exit_dt + pd.Timedelta(minutes=1)).time()


# ── Results ───────────────────────────────────────────────────────────
trades_df_6  = pd.DataFrame(trades_6)
skipped_df_6 = pd.DataFrame(skipped_6)

print(f"\n{'='*58}")
print(f"STEP 6 VOLATILITY SHORT — BACKTEST COMPLETE")
print(f"{'='*58}")
print(f"Total days     : {len(all_dates_6)}")
print(f"Trades entered : {len(trades_df_6)}")
print(f"Days skipped   : {len(skipped_df_6)}")

if not skipped_df_6.empty:
    print(f"\nSkip reasons:")
    print(skipped_df_6["reason"].value_counts().to_string())

if not trades_df_6.empty:
    wins     = trades_df_6[trades_df_6["pnl_rs"] > 0]
    losses   = trades_df_6[trades_df_6["pnl_rs"] <= 0]
    win_rate = round(len(wins) / len(trades_df_6) * 100, 1)

    print(f"\n--- PERFORMANCE SUMMARY ---")
    print(f"Win rate          : {win_rate}%")
    print(f"Total P&L (₹)     : ₹{trades_df_6['pnl_rs'].sum():,.2f}")
    print(f"Avg P&L / trade   : ₹{trades_df_6['pnl_rs'].mean():,.2f}")
    print(f"Best trade        : ₹{trades_df_6['pnl_rs'].max():,.2f}")
    print(f"Worst trade       : ₹{trades_df_6['pnl_rs'].min():,.2f}")
    print(f"Avg capital/trade : ₹{trades_df_6['total_capital'].mean():,.2f}")
    print(f"Avg combined prem : ₹{trades_df_6['combined_prem'].mean():,.2f}")

    print(f"\nExit reasons:")
    print(trades_df_6["exit_reason"].value_counts().to_string())

    print(f"\nEntry time distribution (hour):")
    print(trades_df_6["signal_hour"].value_counts().sort_index().to_string())

    print(f"\nMonthly P&L (wins / losses / net ₹):")
    monthly_6 = trades_df_6.groupby("month").agg(
        trades  = ("pnl_rs", "count"),
        wins    = ("pnl_rs", lambda x: (x > 0).sum()),
        losses  = ("pnl_rs", lambda x: (x <= 0).sum()),
        net_rs  = ("pnl_rs", "sum"),
        avg_rs  = ("pnl_rs", "mean"),
    )
    monthly_6["win_rate"] = (monthly_6["wins"] / monthly_6["trades"] * 100).round(1)
    print(monthly_6.to_string())

    # ── Save ──────────────────────────────────────────────────────────────
    _s6 = BACKTEST_START_6.strftime("%Y%m%d")
    _e6 = BACKTEST_END_6.strftime("%Y%m%d")

    _trades_file_6    = f"./backtests/vol-short-straddle-{_s6}-{_e6}-trades.csv"
    _trail_file_6     = f"./backtests/vol-short-straddle-{_s6}-{_e6}-trails.csv"
    _portfolio_file_6 = f"./backtests/vol-short-straddle-{_s6}-{_e6}-portfolio.xlsx"

    import os; os.makedirs("./backtests", exist_ok=True)

    trades_df_6.to_csv(_trades_file_6, index=False)
    print(f"\n✅ Trade log saved → {_trades_file_6}")

    trail_df_6 = pd.DataFrame(trails_6)
    trail_df_6.to_csv(_trail_file_6, index=False)
    print(f"✅ P&L trail saved → {_trail_file_6}")

    trades_to_mt5_xlsx(
        trades_df     = trades_df_6,
        output_path   = _portfolio_file_6,
        start_capital = 1_000_000,
        symbol        = "NIFTY"
    )

    # ── Minute-by-minute P&L profile ─────────────────────────────────────
    if not trail_df_6.empty and "min_offset" in trail_df_6.columns:
        print(f"\n--- MINUTE-BY-MINUTE P&L PROFILE (short strangle) ---")
        print(f"{'Min':>4}  {'AvgPct':>8}  {'MedPct':>8}  {'Best%':>7}  {'Worst%':>8}  {'n':>5}")
        _mprofile_6 = (trail_df_6.groupby("min_offset")["pnl_pct"]
                       .agg(["mean","median","max","min","count"])
                       .reset_index())
        for _, row in _mprofile_6.iterrows():
            print(f"  {int(row['min_offset']):3d}  "
                  f"{row['mean']:+8.2f}%  "
                  f"{row['median']:+8.2f}%  "
                  f"{row['max']:+7.2f}%  "
                  f"{row['min']:+8.2f}%  "
                  f"{int(row['count']):5d}")

    # ── Peak P&L distribution ─────────────────────────────────────────────
    if "peak_pnl_rs" in trades_df_6.columns:
        avg_cap = trades_df_6["total_capital"].mean()
        peak_pcts = (trades_df_6["peak_pnl_rs"] / avg_cap * 100)
        print(f"\n--- PEAK P&L DISTRIBUTION ---")
        print(f"  Avg peak    : {peak_pcts.mean():+.2f}%")
        print(f"  Median peak : {peak_pcts.median():+.2f}%")
        print(f"  % with peak > 0%  : {(peak_pcts > 0).mean()*100:.1f}%")
        print(f"  % with peak > 1%  : {(peak_pcts > 1).mean()*100:.1f}%")
        print(f"  % with peak > 2%  : {(peak_pcts > 2).mean()*100:.1f}%")
        print(f"  % with peak > 3%  : {(peak_pcts > 3).mean()*100:.1f}%")
        print(f"  % with peak > 4%  : {(peak_pcts > 4).mean()*100:.1f}%")

    # ── SL/TP simulation on saved trails (NO_RULES_MODE only) ────────────
    if NO_RULES_MODE_6 and not trail_df_6.empty:
        print(f"\n--- SL/TP SIMULATION (post-run on raw trails) ---")
        print(f"{'SL%':>5}  {'TP%':>5}  {'Trades':>7}  {'WinRate':>8}  {'TotalPnl':>10}  {'AvgPnl':>9}  {'AvgPct':>8}")

        def _sim_sltp_6(tdf, sl_pct_cap, tp_pct_cap, cap_mean):
            """Simulate fixed SL/TP on trail data. Returns summary dict."""
            results = []
            for (d, tn), grp in tdf.sort_values("min_offset").groupby(["date","trade_num"]):
                hit = "NONE"
                final_pct = grp.iloc[-1]["pnl_pct"]
                for _, tick in grp.iterrows():
                    if tick["pnl_pct"] <= -sl_pct_cap * 100:
                        final_pct = tick["pnl_pct"]; hit = "SL"; break
                    if tick["pnl_pct"] >= tp_pct_cap * 100:
                        final_pct = tick["pnl_pct"]; hit = "TP"; break
                results.append({"pnl_pct": final_pct, "pnl_rs": final_pct / 100 * cap_mean, "hit": hit})
            rdf = pd.DataFrame(results)
            return {
                "trades"   : len(rdf),
                "win_rate" : round((rdf["pnl_pct"] > 0).mean() * 100, 1),
                "total_pnl": round(rdf["pnl_rs"].sum(), 0),
                "avg_pnl"  : round(rdf["pnl_rs"].mean(), 2),
                "avg_pct"  : round(rdf["pnl_pct"].mean(), 2),
            }

        _cap_mean_6 = trades_df_6["total_capital"].mean()
        for _sl in [0.5, 1.0, 1.5, 2.0, 3.0]:
            for _tp in [1.0, 2.0, 3.0, 4.0, 5.0]:
                if _tp <= _sl:
                    continue
                r = _sim_sltp_6(trail_df_6, _sl/100, _tp/100, _cap_mean_6)
                print(f"  {_sl:4.1f}%  {_tp:4.1f}%  "
                      f"{r['trades']:7d}  {r['win_rate']:7.1f}%  "
                      f"₹{r['total_pnl']:>9,.0f}  ₹{r['avg_pnl']:>8,.2f}  "
                      f"{r['avg_pct']:+7.2f}%")

    # ── Trailing stop simulation ──────────────────────────────────────────
    if NO_RULES_MODE_6 and not trail_df_6.empty:
        print(f"\n--- TRAILING STOP SIMULATION ---")
        print(f"{'Trail%':>7}  {'MinAct%':>8}  {'Trades':>7}  {'WinRate':>8}  {'TotalPnl':>10}  {'AvgPnl':>9}  {'AvgPct':>8}")

        def _sim_trail_6(tdf, trail_pct, min_activation_pct, cap_mean):
            results = []
            for (d, tn), grp in tdf.sort_values("min_offset").groupby(["date","trade_num"]):
                peak_pct = 0.0
                final_pct = grp.iloc[-1]["pnl_pct"]
                activated = False
                for _, tick in grp.iterrows():
                    cur = tick["pnl_pct"]
                    if cur > peak_pct:
                        peak_pct = cur
                    if peak_pct >= min_activation_pct:
                        activated = True
                    if activated and cur <= peak_pct - trail_pct:
                        final_pct = cur; break
                results.append({"pnl_pct": final_pct, "pnl_rs": final_pct / 100 * cap_mean})
            rdf = pd.DataFrame(results)
            return {
                "trades"   : len(rdf),
                "win_rate" : round((rdf["pnl_pct"] > 0).mean() * 100, 1),
                "total_pnl": round(rdf["pnl_rs"].sum(), 0),
                "avg_pnl"  : round(rdf["pnl_rs"].mean(), 2),
                "avg_pct"  : round(rdf["pnl_pct"].mean(), 2),
            }

        _cap_mean_6 = trades_df_6["total_capital"].mean()
        for _trail in [0.5, 1.0, 1.5, 2.0]:
            for _min_act in [0.5, 1.0, 2.0]:
                r = _sim_trail_6(trail_df_6, _trail, _min_act, _cap_mean_6)
                print(f"  {_trail:6.1f}%  {_min_act:7.1f}%  "
                      f"{r['trades']:7d}  {r['win_rate']:7.1f}%  "
                      f"₹{r['total_pnl']:>9,.0f}  ₹{r['avg_pnl']:>8,.2f}  "
                      f"{r['avg_pct']:+7.2f}%")

else:
    print("No trades entered — check peak volatility parameters");
    

'''
# ══════════════════════════════════════════════════════════════════════
# SCENARIO A — 9:20 AM 25/75 LEVEL ENTRY (LONG STRANGLE)
# ══════════════════════════════════════════════════════════════════════
# Logic:
#   1. At 9:20 AM, check if spot close is within ±5 pts of a 25/75 level
#      (spot sits between two consecutive 50-pt Nifty strikes)
#   2. CE = first 50-pt strike strictly above spot
#      PE = largest 50-pt strike at or below spot
#      e.g. spot=21325 → CE=21350, PE=21300
#           spot=21375 → CE=21400, PE=21350
#   3. Use nearest weekly expiry; if today is expiry day → use next expiry
#   4. Capital ₹1,50,000 | Lot size = 65
#      max_lots = floor(150000 / ((CE_ltp + PE_ltp) × 65))
#   5. Walk 60 min — NO SL / TP — pure observation
#   6. P&L recorded every minute; snapshots at +15 / +30 / +45 / +60 min
# ══════════════════════════════════════════════════════════════════════

CAPITAL_920         = 150_000
LOT_SIZE_920        = 65
ENTRY_TIME_920      = datetime.time(9, 30)
FORCED_EXIT_920     = datetime.time(10, 30)
LEVEL_TOLERANCE_920 = 5          # ±5 pts tolerance around a 25/75 level
BACKTEST_START_920  = pd.Timestamp("2021-02-15")
BACKTEST_END_920    = pd.Timestamp("2023-12-31")
#BACKTEST_START_920  = pd.Timestamp("2021-02-15")
#BACKTEST_END_920    = pd.Timestamp("2024-10-31")


def is_25_75_level(price: float, tolerance: float = 5.0) -> bool:
    """True if price sits within ±tolerance of a midpoint 25/75 level."""
    return abs(price % 50 - 25) <= tolerance


def get_bracket_strikes_920(spot: float) -> tuple:
    """
    CE = smallest 50-pt multiple strictly above spot.
    PE = largest  50-pt multiple at or below spot.
    Examples:
      21325 → CE=21350, PE=21300
      21375 → CE=21400, PE=21350
    """
    base = int(spot // 50) * 50
    if spot == float(base):          # spot landed exactly on a strike
        return float(base + 50), float(base - 50)
    return float(base + 50), float(base)


def walk_forward_pnl_920(opt_groups: dict, expiry: str,
                          ce_strike: float, pe_strike: float,
                          ce_entry_ltp: float, pe_entry_ltp: float,
                          entry_time, lots: int) -> dict:
    """
    Walk forward minute-by-minute for up to 60 min after entry_time.
    No SL / TP — pure P&L observation.

    P&L each minute:
      CE_pnl  = (CE_curr - CE_entry) × lots × LOT_SIZE_920
      PE_pnl  = (PE_curr - PE_entry) × lots × LOT_SIZE_920
      net_pnl = CE_pnl + PE_pnl

    Returns:
      pnl_trail : list of per-minute dicts
      snap_15m / snap_30m / snap_45m / snap_60m : first tick at or after
                                                   each milestone
    """
    quantity      = lots * LOT_SIZE_920
    total_capital = round((ce_entry_ltp + pe_entry_ltp) * quantity, 2)

    _no_data = dict(
        exit_time=None, exit_reason="NO_DATA", pnl_rs=0.0,
        total_capital=total_capital, lots=lots, quantity=quantity,
        pnl_trail=[], snap_15m=None, snap_30m=None,
        snap_45m=None, snap_60m=None,
    )

    ce_grp = opt_groups.get((expiry, ce_strike, "CE"))
    pe_grp = opt_groups.get((expiry, pe_strike, "PE"))
    if ce_grp is None or pe_grp is None:
        return _no_data

    entry_dt     = pd.Timestamp(f"2000-01-01 {entry_time}")
    ce_ticks     = ce_grp[ce_grp["time"] > entry_time].set_index("time")["close"]
    pe_ticks     = pe_grp[pe_grp["time"] > entry_time].set_index("time")["close"]
    common_times = sorted(set(ce_ticks.index) & set(pe_ticks.index))

    if not common_times:
        return _no_data

    pnl_trail = []
    snap_930 = snap_15m = snap_30m = snap_45m = snap_60m = None

    for t in common_times:
        if t > FORCED_EXIT_920:
            break

        ce_curr = ce_ticks[t]
        pe_curr = pe_ticks[t]
        ce_pnl  = round((ce_curr - ce_entry_ltp) * quantity, 2)
        pe_pnl  = round((pe_curr - pe_entry_ltp) * quantity, 2)
        net_pnl = round(ce_pnl + pe_pnl, 2)
        net_pct = round((net_pnl / total_capital) * 100, 2) if total_capital > 0 else 0.0

        tick = dict(time=t, ce_ltp=ce_curr, pe_ltp=pe_curr,
                    ce_pnl=ce_pnl, pe_pnl=pe_pnl,
                    net_pnl=net_pnl, net_pct=net_pct)
        pnl_trail.append(tick)

        mins = (pd.Timestamp(f"2000-01-01 {t}") - entry_dt).total_seconds() / 60
        if snap_930 is None and mins >= 10:   # 9:30 AM = entry + 10 min
            snap_930 = tick.copy()
        if snap_15m is None and mins >= 15:
            snap_15m = tick.copy()
        if snap_30m is None and mins >= 30:
            snap_30m = tick.copy()
        if snap_45m is None and mins >= 45:
            snap_45m = tick.copy()
        if snap_60m is None and mins >= 60:
            snap_60m = tick.copy()

    last = pnl_trail[-1] if pnl_trail else None
    return dict(
        exit_time     = last["time"]    if last else None,
        exit_reason   = "FORCED",
        pnl_rs        = last["net_pnl"] if last else 0.0,
        total_capital = total_capital,
        lots          = lots,
        quantity      = quantity,
        pnl_trail     = pnl_trail,
        snap_930      = snap_930,
        snap_15m      = snap_15m,
        snap_30m      = snap_30m,
        snap_45m      = snap_45m,
        snap_60m      = snap_60m,
    )


def _snap_pnl(s): return s["net_pnl"] if s else None
def _snap_pct(s): return s["net_pct"] if s else None


# ── Prepare spot data (independent of Step 5) ───────────────────────
# Build fresh from df so Scenario A runs even if Step 5 was skipped
spot_clean_920 = df.copy()
spot_clean_920["DateTime"] = pd.to_datetime(spot_clean_920["DateTime"]).dt.tz_localize(None)
spot_clean_920["Date"]     = spot_clean_920["DateTime"].dt.date
spot_clean_920["Time"]     = spot_clean_920["DateTime"].dt.time
spot_clean_920             = (spot_clean_920
                               .set_index("DateTime")
                               .between_time("09:15", "15:30")
                               .reset_index()
                               .copy())

# ── Date list ────────────────────────────────────────────────────────
all_dates_920 = sorted(spot_clean_920[
    (spot_clean_920["Date"] >= BACKTEST_START_920.date()) &
    (spot_clean_920["Date"] <= BACKTEST_END_920.date())
]["Date"].unique())

print("\n" + "="*60)
print("SCENARIO A — 9:20 AM 25/75 LEVEL ENTRY (LONG STRANGLE)")
print("="*60)
print(f"Period      : {BACKTEST_START_920.date()} -> {BACKTEST_END_920.date()}")
print(f"Capital     : Rs{CAPITAL_920:,}  |  Lot size : {LOT_SIZE_920}")
print(f"Entry       : 9:20 AM  |  Primary: ±{LEVEL_TOLERANCE_920}pts of 25/75 level  |  Secondary: bracket fallback")
print(f"Walk        : 60 min (forced exit {FORCED_EXIT_920})  |  No SL/TP")
print(f"Trading days: {len(all_dates_920)}")

trades_920  = []
skipped_920 = []
trails_920  = []

for date in tqdm(all_dates_920, desc="Scenario A 9:20"):
    trade_date = pd.Timestamp(date)

    # ── 9:20 AM candle ───────────────────────────────────────────
    day_spot   = spot_clean_920[spot_clean_920["Date"] == date]
    candle_920 = day_spot[day_spot["Time"] == ENTRY_TIME_920]

    if candle_920.empty:
        skipped_920.append({"date": date, "reason": "no_920_candle"})
        continue

    spot_920 = candle_920.iloc[0]["Close"]

    # ── Entry type: primary (25/75 hit) or secondary (bracket) ──
    if is_25_75_level(spot_920, LEVEL_TOLERANCE_920):
        entry_type = "primary"
        r100       = round(spot_920) % 100
        level_type = "25" if abs(r100 - 25) <= LEVEL_TOLERANCE_920 else "75"
    else:
        entry_type = "secondary"
        level_type = "bracket"

    # ── Bracket strikes ──────────────────────────────────────────
    ce_stk_920, pe_stk_920 = get_bracket_strikes_920(spot_920)

    # ── Load morning options only (9:15 → 10:30, faster) ─────────
    opt_df_920 = load_options_for_date(
        date         = trade_date,
        spot         = spot_920,
        strike_range = 500,
        time_from    = "09:15",
        time_to      = "10:30"
    )

    if opt_df_920.empty:
        skipped_920.append({"date": date, "reason": "no_options_file"})
        continue

    # ── Pre-group once per day ────────────────────────────────────
    opt_groups_920 = {
        key: grp.sort_values("time").reset_index(drop=True)
        for key, grp in opt_df_920.groupby(["expiry_str", "strike", "option_type"])
    }

    # ── Smart expiry (skip today if expiry day) ───────────────────
    expiry_920 = get_smart_expiry(opt_df_920, trade_date)
    if expiry_920 is None:
        skipped_920.append({"date": date, "reason": "no_expiry"})
        continue

    # ── Entry LTPs at 9:20 ───────────────────────────────────────
    ce_ltp_920 = get_entry_ltp(opt_groups_920, expiry_920,
                                ce_stk_920, "CE", ENTRY_TIME_920)
    pe_ltp_920 = get_entry_ltp(opt_groups_920, expiry_920,
                                pe_stk_920, "PE", ENTRY_TIME_920)

    if ce_ltp_920 is None or pe_ltp_920 is None:
        skipped_920.append({"date": date, "reason": "no_entry_ltp",
                             "ce_stk": ce_stk_920, "pe_stk": pe_stk_920,
                             "expiry": expiry_920})
        continue

    # ── Max equal lots within Rs1,50,000 ─────────────────────────
    cost_per_lot = (ce_ltp_920 + pe_ltp_920) * LOT_SIZE_920
    if cost_per_lot <= 0:
        skipped_920.append({"date": date, "reason": "zero_premium"})
        continue

    max_lots = int(CAPITAL_920 // cost_per_lot)
    if max_lots < 1:
        skipped_920.append({"date": date, "reason": "insufficient_capital",
                             "cost_per_lot": round(cost_per_lot, 2)})
        continue

    # ── Walk forward 60 minutes ───────────────────────────────────
    res = walk_forward_pnl_920(
        opt_groups   = opt_groups_920,
        expiry       = expiry_920,
        ce_strike    = ce_stk_920,
        pe_strike    = pe_stk_920,
        ce_entry_ltp = ce_ltp_920,
        pe_entry_ltp = pe_ltp_920,
        entry_time   = ENTRY_TIME_920,
        lots         = max_lots,
    )

    trades_920.append({
        "date"         : date,
        "entry_type"   : entry_type,
        "spot_920"     : round(spot_920, 2),
        "level_type"   : level_type,
        "ce_strike"    : ce_stk_920,
        "pe_strike"    : pe_stk_920,
        "expiry"       : expiry_920,
        "ce_entry_ltp" : ce_ltp_920,
        "pe_entry_ltp" : pe_ltp_920,
        "combined_prem": round(ce_ltp_920 + pe_ltp_920, 2),
        "lots"         : max_lots,
        "quantity"     : max_lots * LOT_SIZE_920,
        "total_capital": res["total_capital"],
        "pnl_930"      : _snap_pnl(res["snap_930"]),
        "pct_930"      : _snap_pct(res["snap_930"]),
        "pnl_15m"      : _snap_pnl(res["snap_15m"]),
        "pct_15m"      : _snap_pct(res["snap_15m"]),
        "pnl_30m"      : _snap_pnl(res["snap_30m"]),
        "pct_30m"      : _snap_pct(res["snap_30m"]),
        "pnl_45m"      : _snap_pnl(res["snap_45m"]),
        "pct_45m"      : _snap_pct(res["snap_45m"]),
        "pnl_60m"      : _snap_pnl(res["snap_60m"]),
        "pct_60m"      : _snap_pct(res["snap_60m"]),
        "final_pnl"    : res["pnl_rs"],
        "exit_time"    : res["exit_time"],
    })

    for tick in res["pnl_trail"]:
        trails_920.append({
            "date"     : date,
            "spot_920" : round(spot_920, 2),
            "ce_strike": ce_stk_920,
            "pe_strike": pe_stk_920,
            "expiry"   : expiry_920,
            "time"     : tick["time"],
            "ce_ltp"   : tick["ce_ltp"],
            "pe_ltp"   : tick["pe_ltp"],
            "ce_pnl"   : tick["ce_pnl"],
            "pe_pnl"   : tick["pe_pnl"],
            "net_pnl"  : tick["net_pnl"],
            "net_pct"  : tick["net_pct"],
        })


# ── Results ───────────────────────────────────────────────────────────
trades_df_920  = pd.DataFrame(trades_920)
skipped_df_920 = pd.DataFrame(skipped_920)
trails_df_920  = pd.DataFrame(trails_920)

print(f"\n{'='*60}")
print("SCENARIO A — RESULTS")
print(f"{'='*60}")
print(f"Total days    : {len(all_dates_920)}")
print(f"Trades taken  : {len(trades_df_920)}")
print(f"Days skipped  : {len(skipped_df_920)}")

if not skipped_df_920.empty:
    print(f"\nSkip reasons:")
    print(skipped_df_920["reason"].value_counts().to_string())

if not trades_df_920.empty:
    print(f"\n{'─'*60}")
    print("P&L SNAPSHOT SUMMARY  (long strangle, 1.5L capital, lot=65)")
    print(f"{'─'*60}")

    for label, pnl_col, pct_col in [
        ("+15 min", "pnl_15m", "pct_15m"),
        ("+30 min", "pnl_30m", "pct_30m"),
        ("+45 min", "pnl_45m", "pct_45m"),
        ("+60 min", "pnl_60m", "pct_60m"),
    ]:
        valid = trades_df_920[pnl_col].dropna()
        if valid.empty:
            continue
        wins  = (valid > 0).sum()
        total = len(valid)
        print(f"\n  {label}:")
        print(f"    Win rate : {wins}/{total} = {wins/total*100:.1f}%")
        print(f"    Avg P&L  : Rs{valid.mean():,.2f}")
        print(f"    Median   : Rs{valid.median():,.2f}")
        print(f"    Best     : Rs{valid.max():,.2f}")
        print(f"    Worst    : Rs{valid.min():,.2f}")
        print(f"    Total    : Rs{valid.sum():,.2f}")

    # ── By level type (X25 vs X75) ────────────────────────────────
    print(f"\n{'─'*60}")
    print("BY LEVEL TYPE  (X25 vs X75)")
    print(f"{'─'*60}")
    for lt in ["25", "75"]:
        sub = trades_df_920[trades_df_920["level_type"] == lt]
        if sub.empty:
            continue
        print(f"\n  X{lt} level  ({len(sub)} trades):")
        for label, col in [("+15m", "pnl_15m"), ("+30m", "pnl_30m"),
                            ("+45m", "pnl_45m"), ("+60m", "pnl_60m")]:
            v = sub[col].dropna()
            if v.empty:
                continue
            w = (v > 0).sum()
            print(f"    {label} : win {w}/{len(v)} = {w/len(v)*100:.1f}%  "
                  f"avg Rs{v.mean():,.2f}")

    # ── Primary vs Secondary entry comparison ────────────────────
    print(f"\n{'─'*60}")
    print("PRIMARY vs SECONDARY ENTRY  (+60 min)")
    print(f"{'─'*60}")
    for et, label in [("primary", "Primary  (25/75 hit)"),
                      ("secondary", "Secondary (bracket)  ")]:
        sub = trades_df_920[trades_df_920["entry_type"] == et]
        if sub.empty:
            continue
        v   = sub["pnl_60m"].dropna()
        w   = (v > 0).sum()
        n   = len(v)
        avg_win  = v[v > 0].mean() if w > 0 else 0
        avg_loss = v[v <= 0].mean() if (n - w) > 0 else 0
        print(f"\n  {label}  ({n} trades):")
        print(f"    Win rate  : {w}/{n} = {w/n*100:.1f}%")
        print(f"    Avg P&L   : Rs{v.mean():,.2f}")
        print(f"    Avg win   : Rs{avg_win:,.2f}")
        print(f"    Avg loss  : Rs{avg_loss:,.2f}")
        wl = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
        print(f"    Win/Loss  : {wl:.2f}x")
        print(f"    Total P&L : Rs{v.sum():,.2f}")

    # ── Minute-by-minute P&L profile (SL/TP guidance) ────────────
    if not trails_df_920.empty:
        import datetime as _dt
        base = _dt.datetime.combine(_dt.date.today(), _dt.time(9, 20))
        trails_df_920["min_offset"] = trails_df_920["time"].apply(
            lambda t: int(round(
                (_dt.datetime.combine(_dt.date.today(), t) - base)
                .total_seconds() / 60
            ))
        )
        min_stats = (
            trails_df_920.groupby("min_offset")
            .agg(
                days      = ("net_pct", "count"),
                avg_pct   = ("net_pct", "mean"),
                median_pct= ("net_pct", "median"),
                best_pct  = ("net_pct", "max"),
                worst_pct = ("net_pct", "min"),
            )
            .round(2)
        )
        print(f"\n{'─'*60}")
        print("MINUTE-BY-MINUTE P&L PROFILE  (% of combined capital)")
        print("  Use this to set SL / TP thresholds")
        print(f"{'─'*60}")
        print(f"  {'min':>4}  {'days':>5}  {'avg%':>7}  {'median%':>8}  {'best%':>7}  {'worst%':>8}")
        print(f"  {'────':>4}  {'─────':>5}  {'───────':>7}  {'────────':>8}  {'───────':>7}  {'────────':>8}")
        for offset, row in min_stats.iterrows():
            print(f"  {offset:>4}  {int(row['days']):>5}  "
                  f"{row['avg_pct']:>7.2f}  {row['median_pct']:>8.2f}  "
                  f"{row['best_pct']:>7.2f}  {row['worst_pct']:>8.2f}")

    # ── 9:30 AM exit scenario ─────────────────────────────────────
    sub_930 = trades_df_920[trades_df_920["pnl_930"].notna()].copy()
    if not sub_930.empty:
        wins_930  = (sub_930["pnl_930"] > 0).sum()
        total_930 = len(sub_930)
        avg_win_930  = sub_930.loc[sub_930["pnl_930"] > 0, "pnl_930"].mean() if wins_930 > 0 else 0
        avg_loss_930 = sub_930.loc[sub_930["pnl_930"] <= 0, "pnl_930"].mean() if (total_930 - wins_930) > 0 else 0
        print(f"\n{'─'*60}")
        print("9:30 AM EXIT SCENARIO  (exit exactly at 9:30, +10 min)")
        print(f"{'─'*60}")
        print(f"  Trades      : {total_930}")
        print(f"  Win rate    : {wins_930}/{total_930} = {wins_930/total_930*100:.1f}%")
        print(f"  Avg P&L     : Rs{sub_930['pnl_930'].mean():,.2f}")
        print(f"  Avg P&L %   : {sub_930['pct_930'].mean():.2f}%")
        print(f"  Avg win     : Rs{avg_win_930:,.2f}")
        print(f"  Avg loss    : Rs{avg_loss_930:,.2f}")
        wl_930 = abs(avg_win_930 / avg_loss_930) if avg_loss_930 != 0 else float('inf')
        print(f"  Win/Loss    : {wl_930:.2f}x")
        print(f"  Median P&L  : Rs{sub_930['pnl_930'].median():,.2f}")
        print(f"  Best trade  : Rs{sub_930['pnl_930'].max():,.2f}")
        print(f"  Worst trade : Rs{sub_930['pnl_930'].min():,.2f}")
        print(f"  Total P&L   : Rs{sub_930['pnl_930'].sum():,.2f}")

        # Monthly breakdown for 9:30 exit
        sub_930["month"] = pd.to_datetime(sub_930["date"]).dt.to_period("M")
        monthly_930 = sub_930.groupby("month").agg(
            trades  = ("pnl_930", "count"),
            avg_pnl = ("pnl_930", "mean"),
            total   = ("pnl_930", "sum")
        ).round(2)
        print(f"\n  Monthly (9:30 exit):")
        print(monthly_930.to_string())

        # Save 9:30 exit dataset
        _s_930 = BACKTEST_START_920.strftime("%Y%m%d")
        _e_930 = BACKTEST_END_920.strftime("%Y%m%d")
        _930_file = f"./backtests/920-exit930-{_s_930}-{_e_930}-trades.csv"
        sub_930.to_csv(_930_file, index=False)
        print(f"\n  9:30 exit dataset saved -> {_930_file}")

    # ── CE vs PE contribution ─────────────────────────────────────
    if not trails_df_920.empty:
        last_ticks = (
            trails_df_920.sort_values("time")
            .groupby("date")
            .last()
            .reset_index()
        )
        avg_ce = last_ticks["ce_pnl"].mean()
        avg_pe = last_ticks["pe_pnl"].mean()
        print(f"\n{'─'*60}")
        print("CE vs PE CONTRIBUTION  (avg at final tick per day)")
        print(f"{'─'*60}")
        print(f"  Avg CE P&L : Rs{avg_ce:,.2f}")
        print(f"  Avg PE P&L : Rs{avg_pe:,.2f}")
        print(f"  Net avg    : Rs{avg_ce + avg_pe:,.2f}")

    # ── Monthly breakdown at +60 min ──────────────────────────────
    trades_df_920["month"] = pd.to_datetime(
        trades_df_920["date"]).dt.to_period("M")
    monthly_920 = trades_df_920.groupby("month").agg(
        trades  = ("pnl_60m", "count"),
        avg_pnl = ("pnl_60m", "mean"),
        total   = ("pnl_60m", "sum")
    ).round(2)
    print(f"\n{'─'*60}")
    print("MONTHLY P&L  (+60 min)")
    print(f"{'─'*60}")
    print(monthly_920.to_string())

    # ── Save ──────────────────────────────────────────────────────
    _s_920 = BACKTEST_START_920.strftime("%Y%m%d")
    _e_920 = BACKTEST_END_920.strftime("%Y%m%d")
    _trades_file_920 = f"./backtests/920-level-entry-{_s_920}-{_e_920}-trades.csv"
    _trails_file_920 = f"./backtests/920-level-entry-{_s_920}-{_e_920}-trails.csv"

    trades_df_920.to_csv(_trades_file_920, index=False)
    trails_df_920.to_csv(_trails_file_920, index=False)
    print(f"\nTrades saved -> {_trades_file_920}")
    print(f"Trails saved -> {_trails_file_920}")
    
else:
    print("No trades — check level tolerance or date range")


# ══════════════════════════════════════════════════════════════════════
# SCENARIO B — EOD 25/75 LEVEL ENTRY, OVERNIGHT HOLD, NEXT DAY 9:16 EXIT
# ══════════════════════════════════════════════════════════════════════
# Logic:
#   1. Scan 3:25–3:29 PM — first minute spot is within ±5pts of 25/75 level
#   2. BUY CE (first 50-pt strike above spot) + BUY PE (below) — same bracket
#   3. Fixed 1 lot (65 contracts each side)
#   4. Expiry: if TOMORROW (exit day) is expiry day → use next week's expiry
#              otherwise → nearest expiry
#   5. Exit: next available trading day at 9:16 AM
#   6. P&L = (CE_exit - CE_entry + PE_exit - PE_entry) × 65
# ══════════════════════════════════════════════════════════════════════

SCAN_FROM_B       = datetime.time(15, 25)
SCAN_TO_B         = datetime.time(15, 29)
EXIT_TIME_B       = datetime.time(9, 16)
LOT_SIZE_B        = 65           # fixed 1 lot
LEVEL_TOL_B       = 5            # ±5 pts around 25/75 level
#BACKTEST_START_B  = pd.Timestamp("2021-02-15")
#BACKTEST_END_B    = pd.Timestamp("2024-10-31")
BACKTEST_START_B  = pd.Timestamp("2021-02-15")
BACKTEST_END_B    = pd.Timestamp("2024-10-31")



def scan_eod_level(spot_df, date,
                   scan_from=datetime.time(15, 25),
                   scan_to=datetime.time(15, 29),
                   tolerance=5.0):
    """
    Scan 3:25–3:29 PM for the first minute where spot close
    is within ±tolerance of a 25/75 level.
    Returns (signal_time, spot_close) or (None, None).
    """
    window = spot_df[
        (spot_df["Date"] == date) &
        (spot_df["Time"] >= scan_from) &
        (spot_df["Time"] <= scan_to)
    ].sort_values("Time")

    for _, row in window.iterrows():
        if is_25_75_level(row["Close"], tolerance):
            return row["Time"], row["Close"]
    return None, None


def get_overnight_expiry(opt_df: pd.DataFrame,
                          entry_date: pd.Timestamp,
                          exit_date: pd.Timestamp) -> str:
    """
    Select expiry for overnight trade (entry day D, exit day D+1).

    Rule:
      - If exit_date IS an expiry day → skip that expiry, use next one
        (avoids holding expiry-day options overnight)
      - Otherwise → use nearest expiry >= entry_date
    """
    expiry_strings = opt_df["expiry_str"].unique()

    expiry_dates = []
    for e in expiry_strings:
        try:
            exp_date = pd.to_datetime(e, format="%d%b%y")
            expiry_dates.append((exp_date, e))
        except Exception:
            continue

    expiry_dates.sort(key=lambda x: x[0])

    # Futures from entry date onward
    future = [(d, e) for d, e in expiry_dates if d.date() >= entry_date.date()]
    if not future:
        return None

    # Check if exit day is an expiry day
    exit_is_expiry = any(d.date() == exit_date.date() for d, _ in expiry_dates)

    if exit_is_expiry:
        # Skip exit-day expiry — use the one after
        after_exit = [(d, e) for d, e in future if d.date() > exit_date.date()]
        return after_exit[0][1] if after_exit else None
    else:
        return future[0][1]


# ── Prepare spot data (reuse spot_clean_920 if already built) ────────
if "spot_clean_920" not in dir():
    spot_clean_B = df.copy()
    spot_clean_B["DateTime"] = pd.to_datetime(spot_clean_B["DateTime"]).dt.tz_localize(None)
    spot_clean_B["Date"]     = spot_clean_B["DateTime"].dt.date
    spot_clean_B["Time"]     = spot_clean_B["DateTime"].dt.time
    spot_clean_B             = (spot_clean_B
                                 .set_index("DateTime")
                                 .between_time("09:15", "15:30")
                                 .reset_index()
                                 .copy())
else:
    spot_clean_B = spot_clean_920   # already prepared above

# ── Date list ─────────────────────────────────────────────────────────
all_dates_B = sorted(spot_clean_B[
    (spot_clean_B["Date"] >= BACKTEST_START_B.date()) &
    (spot_clean_B["Date"] <= BACKTEST_END_B.date())
]["Date"].unique())

print("\n" + "="*60)
print("SCENARIO B — EOD 25/75 ENTRY, OVERNIGHT HOLD")
print("="*60)
print(f"Period       : {BACKTEST_START_B.date()} -> {BACKTEST_END_B.date()}")
print(f"Entry window : {SCAN_FROM_B} – {SCAN_TO_B}  (first 25/75 hit)")
print(f"Exit         : Next trading day {EXIT_TIME_B}")
print(f"Size         : 1 lot ({LOT_SIZE_B} contracts each side)")
print(f"Expiry rule  : Skip exit-day expiry -> use next week's")
print(f"Trading days : {len(all_dates_B)}")

trades_B  = []
skipped_B = []

for i, date in enumerate(tqdm(all_dates_B, desc="Scenario B EOD")):
    trade_date = pd.Timestamp(date)

    # ── Find next trading day ─────────────────────────────────────
    if i + 1 >= len(all_dates_B):
        skipped_B.append({"date": date, "reason": "no_next_trading_day"})
        continue
    next_date       = all_dates_B[i + 1]
    next_trade_date = pd.Timestamp(next_date)

    # ── Scan 3:25–3:29 for 25/75 level ───────────────────────────
    signal_time, spot_val = scan_eod_level(
        spot_clean_B, date, SCAN_FROM_B, SCAN_TO_B, LEVEL_TOL_B
    )
    if signal_time is not None:
        # ── Case 1: Symmetric entry (spot hit 25/75 level) ────────
        entry_type = "symmetric"
        ce_stk_B, pe_stk_B = get_bracket_strikes_920(spot_val)
        r100       = round(spot_val) % 100
        level_type = "25" if abs(r100 - 25) <= LEVEL_TOL_B else "75"
    else:
        # ── Case 2: Bracket fallback (use last candle in window) ──
        window_B = spot_clean_B[
            (spot_clean_B["Date"] == date) &
            (spot_clean_B["Time"] >= SCAN_FROM_B) &
            (spot_clean_B["Time"] <= SCAN_TO_B)
        ].sort_values("Time")
        if window_B.empty:
            skipped_B.append({"date": date, "reason": "no_spot_in_window"})
            continue
        last_row    = window_B.iloc[-1]
        signal_time = last_row["Time"]
        spot_val    = last_row["Close"]
        entry_type  = "bracket"
        level_type  = "bracket"
        ce_stk_B, pe_stk_B = get_bracket_strikes_920(spot_val)


    # ── Load entry-day options (3:20 → 3:30) ─────────────────────
    opt_df_entry = load_options_for_date(
        date         = trade_date,
        spot         = spot_val,
        strike_range = 500,
        time_from    = "15:20",
        time_to      = "15:30"
    )
    if opt_df_entry.empty:
        skipped_B.append({"date": date, "reason": "no_entry_options"})
        continue

    # ── Load exit-day options (9:15 → 9:20) ──────────────────────
    opt_df_exit = load_options_for_date(
        date         = next_trade_date,
        spot         = spot_val,
        strike_range = 500,
        time_from    = "09:15",
        time_to      = "09:20"
    )
    if opt_df_exit.empty:
        skipped_B.append({"date": date, "reason": "no_exit_options"})
        continue

    # ── Overnight expiry selection ────────────────────────────────
    expiry_B = get_overnight_expiry(opt_df_entry, trade_date, next_trade_date)
    if expiry_B is None:
        skipped_B.append({"date": date, "reason": "no_expiry"})
        continue

    # ── Pre-group both day's options ──────────────────────────────
    opt_grp_entry = {
        key: grp.sort_values("time").reset_index(drop=True)
        for key, grp in opt_df_entry.groupby(["expiry_str", "strike", "option_type"])
    }
    opt_grp_exit = {
        key: grp.sort_values("time").reset_index(drop=True)
        for key, grp in opt_df_exit.groupby(["expiry_str", "strike", "option_type"])
    }

    # ── Entry LTP (3:25–3:29 signal minute) ──────────────────────
    ce_entry = get_entry_ltp(opt_grp_entry, expiry_B, ce_stk_B, "CE", signal_time)
    pe_entry = get_entry_ltp(opt_grp_entry, expiry_B, pe_stk_B, "PE", signal_time)

    if ce_entry is None or pe_entry is None:
        skipped_B.append({"date": date, "reason": "no_entry_ltp",
                           "ce_stk": ce_stk_B, "pe_stk": pe_stk_B,
                           "expiry": expiry_B})
        continue

    # ── Exit LTP (next day 9:16 AM) ───────────────────────────────
    ce_exit = get_entry_ltp(opt_grp_exit, expiry_B, ce_stk_B, "CE", EXIT_TIME_B)
    pe_exit = get_entry_ltp(opt_grp_exit, expiry_B, pe_stk_B, "PE", EXIT_TIME_B)

    if ce_exit is None or pe_exit is None:
        skipped_B.append({"date": date, "reason": "no_exit_ltp",
                           "ce_stk": ce_stk_B, "pe_stk": pe_stk_B,
                           "expiry": expiry_B})
        continue

    # ── P&L (long buyer: exit - entry) ───────────────────────────
    ce_pnl        = round((ce_exit - ce_entry) * LOT_SIZE_B, 2)
    pe_pnl        = round((pe_exit - pe_entry) * LOT_SIZE_B, 2)
    net_pnl       = round(ce_pnl + pe_pnl, 2)
    total_capital = round((ce_entry + pe_entry) * LOT_SIZE_B, 2)
    net_pct       = round((net_pnl / total_capital) * 100, 2) if total_capital > 0 else 0.0

    trades_B.append({
        "entry_date"   : date,
        "exit_date"    : next_date,
        "spot_entry"   : round(spot_val, 2),
        "level_type"   : level_type,
        "signal_time"  : signal_time,
        "ce_strike"    : ce_stk_B,
        "pe_strike"    : pe_stk_B,
        "expiry"       : expiry_B,
        "ce_entry_ltp" : ce_entry,
        "pe_entry_ltp" : pe_entry,
        "combined_prem": round(ce_entry + pe_entry, 2),
        "total_capital": total_capital,
        "ce_exit_ltp"  : ce_exit,
        "pe_exit_ltp"  : pe_exit,
        "ce_pnl"       : ce_pnl,
        "pe_pnl"       : pe_pnl,
        "net_pnl"      : net_pnl,
        "net_pct"      : net_pct,
    })


# ── Results ───────────────────────────────────────────────────────────
trades_df_B  = pd.DataFrame(trades_B)
skipped_df_B = pd.DataFrame(skipped_B)

print(f"\n{'='*60}")
print("SCENARIO B — RESULTS")
print(f"{'='*60}")
print(f"Total days    : {len(all_dates_B)}")
print(f"Trades taken  : {len(trades_df_B)}")
print(f"Days skipped  : {len(skipped_df_B)}")

if not skipped_df_B.empty:
    print(f"\nSkip reasons:")
    print(skipped_df_B["reason"].value_counts().to_string())

if not trades_df_B.empty:
    wins     = (trades_df_B["net_pnl"] > 0).sum()
    total    = len(trades_df_B)
    win_rate = round(wins / total * 100, 1)

    print(f"\n{'─'*60}")
    print("P&L SUMMARY  (long strangle, 1 lot, overnight hold)")
    print(f"{'─'*60}")
    print(f"  Win rate    : {wins}/{total} = {win_rate}%")
    print(f"  Avg P&L     : Rs{trades_df_B['net_pnl'].mean():,.2f}")
    print(f"  Median P&L  : Rs{trades_df_B['net_pnl'].median():,.2f}")
    print(f"  Best trade  : Rs{trades_df_B['net_pnl'].max():,.2f}")
    print(f"  Worst trade : Rs{trades_df_B['net_pnl'].min():,.2f}")
    print(f"  Total P&L   : Rs{trades_df_B['net_pnl'].sum():,.2f}")
    print(f"  Avg capital : Rs{trades_df_B['total_capital'].mean():,.2f}")

    # ── CE vs PE contribution ─────────────────────────────────────
    print(f"\n{'─'*60}")
    print("CE vs PE CONTRIBUTION")
    print(f"{'─'*60}")
    print(f"  Avg CE P&L  : Rs{trades_df_B['ce_pnl'].mean():,.2f}")
    print(f"  Avg PE P&L  : Rs{trades_df_B['pe_pnl'].mean():,.2f}")

    # ── By level type ─────────────────────────────────────────────
    print(f"\n{'─'*60}")
    print("BY LEVEL TYPE  (X25 vs X75)")
    print(f"{'─'*60}")
    for lt in ["25", "75"]:
        sub = trades_df_B[trades_df_B["level_type"] == lt]
        if sub.empty:
            continue
        w = (sub["net_pnl"] > 0).sum()
        print(f"\n  X{lt} level  ({len(sub)} trades):")
        print(f"    Win rate : {w}/{len(sub)} = {w/len(sub)*100:.1f}%")
        print(f"    Avg P&L  : Rs{sub['net_pnl'].mean():,.2f}")
        print(f"    Total    : Rs{sub['net_pnl'].sum():,.2f}")

    # ── Monthly breakdown ─────────────────────────────────────────
    trades_df_B["month"] = pd.to_datetime(
        trades_df_B["entry_date"]).dt.to_period("M")
    monthly_B = trades_df_B.groupby("month").agg(
        trades  = ("net_pnl", "count"),
        avg_pnl = ("net_pnl", "mean"),
        total   = ("net_pnl", "sum")
    ).round(2)
    print(f"\n{'─'*60}")
    print("MONTHLY P&L")
    print(f"{'─'*60}")
    print(monthly_B.to_string())

    # ── Save ──────────────────────────────────────────────────────
    _sB = BACKTEST_START_B.strftime("%Y%m%d")
    _eB = BACKTEST_END_B.strftime("%Y%m%d")
    _trades_file_B = f"./backtests/eod-overnight-{_sB}-{_eB}-trades.csv"
    trades_df_B.to_csv(_trades_file_B, index=False)
    print(f"\nTrades saved -> {_trades_file_B}")

else:
    print("No trades — check level tolerance or date range")
   
'''

''' 
Backtest for short strangle raw 

==========================================================
STEP 6: VOLATILITY SHORT BACKTEST
==========================================================
Period         : 2021-02-15 → 2024-10-31
Lot size       : 65 × 4 lots = 260 units
Scan window    : 09:15:00 → 10:30:00  (full day for analysis)
Forced exit    : 15:28:00
Strategy       : Sell ATM CE + PE on peak volatility
Exit trigger   : Consolidation detected OR TP/SL/Forced
SL / TP        : -1.5% / +4.0% of capital
Trading days   : 918
Step 6 Vol Short: 100%|██████████| 918/918 [32:07<00:00,  2.10s/it]

==========================================================
STEP 6 VOLATILITY SHORT — BACKTEST COMPLETE
==========================================================
Total days     : 918
Trades entered : 593
Days skipped   : 544

Skip reasons:
reason
premium_imbalance      211
no_expiry              194
no_peak_volatility     131
no_entry_ltp             5
options_not_at_peak      3

--- PERFORMANCE SUMMARY ---
Win rate          : 69.0%
Total P&L (₹)     : ₹769,301.00
Avg P&L / trade   : ₹1,297.30
Best trade        : ₹50,466.00
Worst trade       : ₹-83,915.00
Avg capital/trade : ₹61,060.76
Avg combined prem : ₹234.85

Exit reasons:
exit_reason
FORCED    593

Entry time distribution (hour):
signal_hour
9     564
10     29

Monthly P&L (wins / losses / net ₹):
         trades  wins  losses    net_rs       avg_rs  win_rate
month                                                         
2021-02       8     6       2  -19188.0 -2398.500000      75.0
2021-03      16    12       4  124371.0  7773.187500      75.0
2021-04      14    11       3   56277.0  4019.785714      78.6
2021-05      13     8       5    7267.0   559.000000      61.5
2021-06      10     5       5   11596.0  1159.600000      50.0
2021-07       8     8       0   36075.0  4509.375000     100.0
2021-08      12     8       4    9542.0   795.166667      66.7
2021-09      14    12       2   72449.0  5174.928571      85.7
2021-10      15    12       3   91442.0  6096.133333      80.0
2021-11      14     7       7  -21398.0 -1528.428571      50.0
2021-12      18    12       6   47398.0  2633.222222      66.7
2022-01      16     9       7  -41210.0 -2575.625000      56.2
2022-02      16    13       3   48230.0  3014.375000      81.2
2022-03      16     9       7   42146.0  2634.125000      56.2
2022-04      15    11       4   -1209.0   -80.600000      73.3
2022-05      16    13       3   44837.0  2802.312500      81.2
2022-06      16    12       4   89427.0  5589.187500      75.0
2022-07      13    10       3    5109.0   393.000000      76.9
2022-08      14    10       4  -11518.0  -822.714286      71.4
2022-09      16    12       4    6981.0   436.312500      75.0
2022-10      11     6       5  -15405.0 -1400.454545      54.5
2022-11      11     6       5   13416.0  1219.636364      54.5
2022-12      12     6       6  -17914.0 -1492.833333      50.0
2023-01      15    10       5   32773.0  2184.866667      66.7
2023-02      13     9       4   21840.0  1680.000000      69.2
2023-03      13     9       4   33878.0  2606.000000      69.2
2023-04      10     8       2   27976.0  2797.600000      80.0
2023-05       5     3       2    4615.0   923.000000      60.0
2023-06       7     6       1   17524.0  2503.428571      85.7
2023-07      15    13       2   59085.0  3939.000000      86.7
2023-08      12     8       4   13286.0  1107.166667      66.7
2023-09       7     5       2    9854.0  1407.714286      71.4
2023-10      14     8       6  -27456.0 -1961.142857      57.1
2023-11       5     4       1    9048.0  1809.600000      80.0
2023-12      12     8       4  -69264.0 -5772.000000      66.7
2024-01      17     9       8  -91065.0 -5356.764706      52.9
2024-02      16    11       5  -10881.0  -680.062500      68.8
2024-03      14     9       5  -24219.0 -1729.928571      64.3
2024-04      12     9       3   45877.0  3823.083333      75.0
2024-05      15    12       3   90493.0  6032.866667      80.0
2024-06      14     6       8  -67626.0 -4830.428571      42.9
2024-07      18    15       3   56511.0  3139.500000      83.3
2024-08      15     9       6   11674.0   778.266667      60.0
2024-09      13     9       4  -11271.0  -867.000000      69.2
2024-10      17    11       6   57928.0  3407.529412      64.7

✅ Trade log saved → ./backtests/vol-short-straddle-20210215-20241031-trades.csv
✅ P&L trail saved → ./backtests/vol-short-straddle-20210215-20241031-trails.csv
✅ MT5 portfolio file saved → ./backtests/vol-short-straddle-20210215-20241031-portfolio.xlsx
   Trades : 593 | Rows : 1186 | Final balance : ₹1,769,301.00

--- MINUTE-BY-MINUTE P&L PROFILE (short strangle) ---
 Min    AvgPct    MedPct    Best%    Worst%      n
    1     -0.05%     -0.02%    +3.15%     -4.90%    593
    2     -0.09%     -0.02%    +3.16%    -11.09%    593
    3     -0.08%     +0.04%    +3.96%    -15.43%    592
    4     -0.04%     +0.20%    +4.26%     -7.49%    592
    5     +0.04%     +0.31%    +5.21%    -14.46%    593
    6     +0.10%     +0.43%    +6.30%    -12.54%    593
    7     +0.12%     +0.48%    +6.53%    -12.87%    593
    8     +0.15%     +0.47%    +7.08%    -12.42%    593
    9     +0.09%     +0.44%    +6.42%    -12.59%    593
   10     +0.12%     +0.43%    +6.95%    -19.14%    593
   11     +0.11%     +0.54%    +6.54%    -20.36%    593
   12     +0.17%     +0.68%    +7.32%    -18.97%    593
   13     +0.16%     +0.69%    +7.38%    -14.91%    593
   14     +0.12%     +0.56%    +8.93%    -17.57%    593
   15     +0.19%     +0.82%   +10.70%    -16.22%    593
   16     +0.24%     +0.81%   +11.30%    -21.44%    593
   17     +0.22%     +0.75%    +9.48%    -28.89%    593
   18     +0.28%     +0.82%    +9.69%    -25.33%    593
   19     +0.26%     +0.87%   +10.67%    -25.70%    593
   20     +0.29%     +0.82%   +13.05%    -28.68%    593
   21     +0.24%     +0.88%   +13.47%    -25.77%    593
   22     +0.24%     +0.85%   +10.71%    -22.15%    593
   23     +0.29%     +0.92%    +9.77%    -19.58%    593
   24     +0.30%     +0.94%   +10.26%    -18.86%    593
   25     +0.36%     +1.09%   +11.70%    -17.19%    593
   26     +0.43%     +1.07%   +11.07%    -15.45%    593
   27     +0.42%     +1.02%   +10.76%    -21.11%    593
   28     +0.40%     +1.09%   +10.35%    -20.59%    593
   29     +0.36%     +1.01%   +11.25%    -22.85%    593
   30     +0.42%     +1.07%   +11.45%    -20.21%    593
   31     +0.39%     +1.10%   +12.09%    -22.65%    593
   32     +0.37%     +1.08%   +12.25%    -25.27%    593
   33     +0.37%     +1.05%   +12.81%    -29.05%    593
   34     +0.43%     +1.19%   +11.91%    -25.84%    593
   35     +0.47%     +1.36%   +11.60%    -27.89%    592
   36     +0.44%     +1.29%   +12.28%    -35.19%    592
   37     +0.50%     +1.31%   +11.81%    -35.94%    592
   38     +0.48%     +1.42%   +12.28%    -33.50%    592
   39     +0.42%     +1.27%   +12.18%    -32.21%    592
   40     +0.37%     +1.37%   +11.91%    -37.17%    592
   41     +0.36%     +1.38%   +12.98%    -35.58%    592
   42     +0.34%     +1.40%   +12.52%    -34.52%    592
   43     +0.34%     +1.34%   +12.57%    -41.05%    592
   44     +0.36%     +1.42%   +12.44%    -46.63%    592
   45     +0.37%     +1.42%   +12.58%    -41.01%    592
   46     +0.36%     +1.57%   +12.39%    -41.94%    592
   47     +0.29%     +1.47%   +12.54%    -42.82%    592
   48     +0.30%     +1.54%   +12.98%    -42.34%    592
   49     +0.35%     +1.68%   +13.39%    -35.98%    592
   50     +0.32%     +1.72%   +13.57%    -35.75%    592
   51     +0.32%     +1.71%   +13.62%    -36.82%    592
   52     +0.24%     +1.69%   +13.57%    -39.74%    592
   53     +0.32%     +1.76%   +13.70%    -37.52%    592
   54     +0.32%     +1.83%   +13.98%    -44.84%    592
   55     +0.30%     +1.66%   +14.46%    -37.38%    592
   56     +0.35%     +1.81%   +14.32%    -40.45%    592
   57     +0.36%     +1.81%   +14.30%    -36.25%    592
   58     +0.41%     +1.85%   +14.28%    -37.03%    592
   59     +0.38%     +1.85%   +14.79%    -40.13%    592
   60     +0.35%     +1.81%   +15.04%    -46.86%    592
   61     +0.37%     +1.88%   +15.12%    -42.26%    592
   62     +0.32%     +1.88%   +15.67%    -45.47%    592
   63     +0.31%     +1.84%   +16.17%    -42.11%    592
   64     +0.38%     +1.92%   +15.71%    -47.53%    592
   65     +0.41%     +1.91%   +15.02%    -57.72%    592
   66     +0.36%     +2.00%   +15.56%    -53.11%    592
   67     +0.40%     +1.96%   +14.94%    -48.16%    592
   68     +0.43%     +2.04%   +15.23%    -42.32%    592
   69     +0.44%     +2.10%   +15.20%    -42.05%    592
   70     +0.50%     +2.20%   +15.80%    -55.73%    592
   71     +0.48%     +2.15%   +15.16%    -57.27%    592
   72     +0.44%     +2.19%   +15.64%    -62.84%    592
   73     +0.45%     +2.09%   +15.43%    -65.23%    592
   74     +0.30%     +2.19%   +15.15%    -64.00%    592
   75     +0.23%     +2.19%   +14.77%    -79.07%    592
   76     +0.33%     +2.26%   +15.05%    -58.75%    592
   77     +0.48%     +2.31%   +15.36%    -55.25%    592
   78     +0.49%     +2.33%   +14.94%    -56.01%    592
   79     +0.54%     +2.54%   +15.77%    -59.83%    592
   80     +0.58%     +2.37%   +16.47%    -62.15%    592
   81     +0.55%     +2.44%   +16.55%    -58.09%    592
   82     +0.53%     +2.36%   +16.62%    -54.34%    592
   83     +0.55%     +2.45%   +16.60%    -57.17%    592
   84     +0.64%     +2.41%   +17.11%    -58.09%    592
   85     +0.69%     +2.45%   +17.71%    -58.43%    592
   86     +0.75%     +2.49%   +17.71%    -56.70%    592
   87     +0.81%     +2.71%   +17.30%    -61.80%    592
   88     +0.78%     +2.68%   +17.30%    -63.72%    592
   89     +0.80%     +2.70%   +17.86%    -61.20%    592
   90     +0.77%     +2.80%   +17.92%    -55.29%    592
   91     +0.83%     +2.78%   +17.81%    -50.60%    592
   92     +0.85%     +2.76%   +18.07%    -48.02%    592
   93     +0.91%     +2.90%   +17.68%    -47.17%    592
   94     +0.96%     +2.97%   +17.99%    -50.79%    592
   95     +0.96%     +3.00%   +18.10%    -52.33%    592
   96     +0.98%     +3.05%   +18.20%    -54.41%    592
   97     +0.98%     +3.00%   +18.10%    -50.63%    592
   98     +0.95%     +2.97%   +18.17%    -47.64%    592
   99     +0.95%     +2.92%   +18.63%    -47.54%    592
  100     +0.82%     +3.00%   +18.61%    -52.33%    592
  101     +0.83%     +2.96%   +18.87%    -57.90%    592
  102     +0.87%     +2.96%   +18.46%    -65.19%    592
  103     +0.93%     +3.01%   +18.46%    -69.52%    592
  104     +0.87%     +2.98%   +18.43%    -68.90%    592
  105     +0.86%     +2.96%   +18.54%    -57.85%    592
  106     +0.97%     +2.95%   +18.28%    -51.92%    592
  107     +0.87%     +2.89%   +18.41%    -51.94%    592
  108     +0.90%     +2.95%   +18.49%    -55.48%    592
  109     +0.99%     +3.09%   +18.59%    -53.24%    592
  110     +0.93%     +3.05%   +18.72%    -55.44%    592
  111     +0.98%     +2.97%   +18.41%    -52.27%    592
  112     +0.98%     +2.94%   +18.30%    -56.20%    592
  113     +1.01%     +3.01%   +18.61%    -53.74%    592
  114     +1.00%     +3.02%   +18.43%    -53.23%    592
  115     +1.07%     +3.10%   +18.64%    -53.61%    592
  116     +1.10%     +3.29%   +18.87%    -49.37%    592
  117     +1.07%     +3.34%   +18.82%    -49.06%    592
  118     +1.08%     +3.33%   +18.85%    -50.14%    592
  119     +1.07%     +3.29%   +19.26%    -51.54%    592
  120     +1.09%     +3.40%   +19.08%    -51.81%    592
  121     +1.17%     +3.36%   +18.77%    -50.03%    592
  122     +1.21%     +3.44%   +18.72%    -51.38%    592
  123     +1.22%     +3.58%   +18.64%    -52.45%    592
  124     +1.26%     +3.58%   +18.49%    -49.84%    592
  125     +1.20%     +3.57%   +18.54%    -49.24%    593
  126     +1.16%     +3.44%   +18.33%    -46.04%    593
  127     +1.13%     +3.57%   +18.61%    -44.48%    593
  128     +1.15%     +3.61%   +18.59%    -44.46%    593
  129     +1.16%     +3.51%   +19.00%    -43.61%    593
  130     +1.11%     +3.39%   +18.67%    -41.69%    593
  131     +1.08%     +3.35%   +18.41%    -42.26%    593
  132     +1.09%     +3.40%   +18.49%    -44.84%    593
  133     +1.12%     +3.23%   +18.43%    -44.21%    593
  134     +1.01%     +3.21%   +18.33%    -44.10%    593
  135     +0.96%     +3.29%   +17.53%    -52.07%    592
  136     +1.04%     +3.28%   +17.61%    -57.32%    592
  137     +1.10%     +3.30%   +17.35%    -51.51%    592
  138     +1.12%     +3.25%   +17.66%    -53.69%    592
  139     +1.11%     +3.27%   +18.30%    -52.53%    592
  140     +1.08%     +3.06%   +18.58%    -50.43%    592
  141     +1.07%     +3.22%   +18.47%    -54.71%    592
  142     +1.05%     +3.15%   +17.95%    -57.94%    592
  143     +1.01%     +3.18%   +17.79%    -60.88%    592
  144     +1.06%     +3.23%   +18.32%    -61.04%    592
  145     +1.00%     +3.21%   +18.40%    -58.99%    592
  146     +1.06%     +3.33%   +18.90%    -65.54%    592
  147     +1.04%     +3.24%   +18.24%    -75.04%    592
  148     +1.05%     +3.26%   +18.62%    -66.59%    592
  149     +0.99%     +3.16%   +18.81%    -65.43%    592
  150     +0.99%     +3.23%   +18.47%    -69.39%    592
  151     +0.95%     +3.41%   +18.30%    -69.60%    592
  152     +0.92%     +3.24%   +18.06%    -77.60%    592
  153     +0.96%     +3.17%   +18.69%    -70.09%    592
  154     +0.94%     +3.29%   +18.85%    -65.32%    592
  155     +0.92%     +3.50%   +18.67%    -67.45%    592
  156     +0.96%     +3.33%   +18.83%    -67.74%    592
  157     +1.06%     +3.25%   +18.92%    -67.07%    592
  158     +1.14%     +3.30%   +18.60%    -67.18%    592
  159     +1.13%     +3.54%   +18.89%    -66.16%    592
  160     +1.23%     +3.55%   +18.89%    -66.75%    592
  161     +1.25%     +3.54%   +19.10%    -60.82%    592
  162     +1.17%     +3.48%   +18.63%    -62.14%    592
  163     +1.14%     +3.46%   +18.92%    -63.92%    592
  164     +1.07%     +3.41%   +19.16%    -60.27%    592
  165     +1.05%     +3.46%   +19.49%    -64.86%    592
  166     +1.07%     +3.58%   +19.27%    -69.52%    592
  167     +1.01%     +3.48%   +18.76%    -80.67%    592
  168     +1.02%     +3.40%   +18.32%    -75.28%    592
  169     +1.02%     +3.27%   +19.27%    -86.70%    592
  170     +1.03%     +3.42%   +18.69%    -79.54%    592
  171     +1.07%     +3.48%   +19.28%    -78.84%    592
  172     +1.03%     +3.58%   +19.77%    -81.74%    592
  173     +1.00%     +3.50%   +19.45%    -83.09%    592
  174     +0.93%     +3.67%   +20.66%    -96.04%    592
  175     +0.90%     +3.53%   +20.93%    -91.68%    592
  176     +0.95%     +3.66%   +20.71%    -95.88%    592
  177     +0.89%     +3.70%   +19.98%   -100.22%    592
  178     +0.90%     +3.69%   +19.99%    -98.82%    592
  179     +0.90%     +3.72%   +19.64%   -102.18%    592
  180     +0.96%     +3.72%   +19.23%   -108.48%    592
  181     +1.02%     +3.88%   +19.39%    -95.53%    592
  182     +1.00%     +3.75%   +25.54%    -93.65%    592
  183     +0.99%     +3.86%   +21.63%    -82.88%    592
  184     +0.99%     +3.67%   +22.94%    -86.59%    592
  185     +1.04%     +3.78%   +21.63%    -86.54%    592
  186     +0.98%     +3.78%   +21.54%    -96.12%    591
  187     +1.03%     +3.73%   +21.96%    -91.71%    591
  188     +1.03%     +3.87%   +20.85%    -81.64%    591
  189     +1.05%     +3.85%   +21.17%    -81.18%    591
  190     +1.04%     +3.89%   +21.32%    -85.00%    591
  191     +1.05%     +3.78%   +21.09%    -82.77%    591
  192     +1.05%     +3.71%   +21.24%    -81.50%    591
  193     +1.08%     +3.89%   +21.65%    -81.93%    591
  194     +1.13%     +3.76%   +21.56%    -77.44%    591
  195     +1.05%     +3.97%   +21.35%    -79.21%    591
  196     +1.01%     +3.78%   +21.39%    -79.08%    591
  197     +1.02%     +3.92%   +20.70%    -80.43%    591
  198     +1.04%     +3.88%   +20.78%    -81.18%    591
  199     +0.99%     +3.86%   +22.02%    -85.89%    591
  200     +1.03%     +3.94%   +21.28%    -87.61%    591
  201     +1.06%     +3.99%   +21.41%    -84.87%    591
  202     +1.06%     +3.92%   +21.58%    -83.52%    591
  203     +1.05%     +3.96%   +21.95%    -80.64%    591
  204     +1.00%     +3.81%   +21.20%    -76.28%    591
  205     +0.98%     +3.81%   +21.45%    -80.24%    591
  206     +1.06%     +3.91%   +21.72%    -82.61%    591
  207     +0.99%     +3.83%   +21.92%    -85.03%    591
  208     +0.98%     +3.94%   +22.54%    -85.33%    591
  209     +0.93%     +3.88%   +22.37%    -83.33%    591
  210     +0.92%     +3.95%   +22.36%    -77.73%    591
  211     +1.00%     +4.02%   +24.49%    -82.63%    591
  212     +1.04%     +4.12%   +23.56%    -78.73%    591
  213     +1.03%     +4.16%   +24.40%    -75.23%    591
  214     +0.97%     +3.92%   +24.98%    -72.94%    591
  215     +0.92%     +3.95%   +25.14%    -74.23%    591
  216     +0.98%     +4.07%   +25.67%    -76.68%    591
  217     +1.03%     +4.08%   +26.10%    -76.44%    591
  218     +1.07%     +4.16%   +26.45%    -77.84%    591
  219     +1.10%     +4.29%   +26.88%    -77.06%    591
  220     +1.16%     +4.36%   +26.49%    -74.66%    591
  221     +1.16%     +4.39%   +26.54%    -76.52%    591
  222     +1.12%     +4.39%   +27.27%    -74.15%    591
  223     +1.17%     +4.36%   +27.96%    -76.47%    591
  224     +1.11%     +4.44%   +28.05%    -76.25%    591
  225     +1.09%     +4.31%   +28.10%    -77.09%    591
  226     +1.14%     +4.38%   +28.05%    -79.99%    591
  227     +1.15%     +4.24%   +28.01%    -78.89%    591
  228     +1.14%     +4.24%   +27.46%    -84.65%    591
  229     +1.13%     +4.27%   +27.96%    -82.39%    591
  230     +1.21%     +4.34%   +27.04%    -84.98%    591
  231     +1.21%     +4.57%   +27.50%    -85.22%    591
  232     +1.18%     +4.44%   +27.73%    -88.18%    591
  233     +1.23%     +4.38%   +28.54%    -86.54%    591
  234     +1.24%     +4.47%   +30.02%    -88.64%    591
  235     +1.17%     +4.47%   +31.94%    -90.50%    591
  236     +1.21%     +4.51%   +35.08%    -99.84%    591
  237     +1.24%     +4.43%   +35.77%   -101.18%    591
  238     +1.28%     +4.45%   +36.56%    -98.41%    591
  239     +1.22%     +4.55%   +37.63%    -95.37%    591
  240     +1.20%     +4.54%   +37.34%   -101.16%    591
  241     +1.28%     +4.68%   +37.38%   -108.77%    591
  242     +1.29%     +4.72%   +37.27%   -107.55%    591
  243     +1.35%     +4.82%   +36.35%   -106.42%    591
  244     +1.40%     +4.73%   +36.82%   -107.21%    591
  245     +1.49%     +4.54%   +37.65%   -102.06%    591
  246     +1.55%     +4.85%   +37.18%    -94.34%    591
  247     +1.53%     +4.73%   +37.45%    -96.89%    591
  248     +1.49%     +4.81%   +36.91%    -99.76%    591
  249     +1.56%     +4.93%   +37.52%   -101.60%    591
  250     +1.54%     +5.03%   +37.29%   -103.24%    591
  251     +1.48%     +5.06%   +37.14%   -102.71%    591
  252     +1.50%     +4.90%   +36.87%   -102.33%    591
  253     +1.51%     +4.80%   +35.51%   -107.35%    591
  254     +1.47%     +4.84%   +37.18%   -109.57%    591
  255     +1.42%     +4.77%   +35.08%   -106.46%    591
  256     +1.47%     +4.90%   +33.53%   -104.88%    591
  257     +1.42%     +4.84%   +36.18%   -117.15%    591
  258     +1.48%     +4.75%   +36.22%   -119.40%    591
  259     +1.43%     +4.75%   +34.85%   -119.44%    591
  260     +1.34%     +4.64%   +36.00%   -130.23%    591
  261     +1.43%     +4.88%   +33.74%   -129.04%    591
  262     +1.51%     +5.03%   +39.73%   -126.46%    591
  263     +1.51%     +4.78%   +38.70%   -127.69%    591
  264     +1.45%     +4.86%   +40.18%   -125.35%    591
  265     +1.39%     +4.86%   +37.05%   -123.22%    591
  266     +1.37%     +5.28%   +34.79%   -126.66%    591
  267     +1.41%     +5.31%   +33.36%   -116.61%    591
  268     +1.47%     +5.30%   +35.62%   -117.26%    591
  269     +1.45%     +5.31%   +35.42%   -117.96%    591
  270     +1.54%     +5.44%   +33.65%   -114.92%    591
  271     +1.45%     +5.34%   +32.12%   -110.37%    591
  272     +1.55%     +5.28%   +34.04%   -112.92%    591
  273     +1.53%     +5.32%   +33.95%   -116.40%    591
  274     +1.54%     +5.60%   +35.61%   -112.41%    591
  275     +1.48%     +5.22%   +34.97%   -115.94%    591
  276     +1.46%     +5.19%   +36.30%   -118.49%    591
  277     +1.51%     +5.27%   +37.00%   -127.15%    591
  278     +1.43%     +5.26%   +38.15%   -132.21%    591
  279     +1.43%     +5.27%   +35.39%   -131.43%    591
  280     +1.43%     +5.40%   +35.93%   -127.26%    591
  281     +1.53%     +5.30%   +37.76%   -129.86%    591
  282     +1.58%     +5.38%   +37.98%   -120.11%    591
  283     +1.60%     +5.53%   +37.60%   -114.86%    591
  284     +1.57%     +5.66%   +38.71%   -117.15%    591
  285     +1.51%     +5.70%   +38.87%   -118.77%    591
  286     +1.46%     +5.79%   +39.14%   -122.67%    591
  287     +1.39%     +5.75%   +37.72%   -128.27%    591
  288     +1.41%     +5.57%   +38.21%   -131.45%    591
  289     +1.31%     +5.67%   +37.69%   -130.80%    591
  290     +1.23%     +5.64%   +37.90%   -138.13%    591
  291     +1.36%     +5.77%   +37.14%   -136.78%    590
  292     +1.25%     +5.80%   +36.16%   -137.94%    590
  293     +1.33%     +5.80%   +36.71%   -151.83%    590
  294     +1.38%     +5.69%   +38.20%   -144.53%    590
  295     +1.38%     +5.84%   +36.99%   -146.90%    590
  296     +1.43%     +5.94%   +37.31%   -150.03%    590
  297     +1.45%     +5.88%   +39.51%   -147.39%    590
  298     +1.44%     +5.83%   +39.81%   -149.97%    590
  299     +1.38%     +6.11%   +39.25%   -149.17%    590
  300     +1.37%     +6.08%   +38.62%   -137.45%    590
  301     +1.55%     +6.01%   +37.62%   -133.55%    589
  302     +1.57%     +6.10%   +37.25%   -139.31%    589
  303     +1.61%     +6.07%   +38.94%   -141.90%    589
  304     +1.58%     +5.99%   +39.51%   -145.21%    589
  305     +1.64%     +5.98%   +39.06%   -144.29%    589
  306     +1.64%     +6.05%   +40.62%   -141.41%    585
  307     +1.59%     +6.09%   +41.99%   -153.96%    585
  308     +1.60%     +6.04%   +43.19%   -151.97%    584
  309     +1.63%     +5.88%   +43.29%   -154.95%    584
  310     +1.66%     +5.96%   +42.45%   -153.15%    585
  311     +1.71%     +6.13%   +42.73%   -155.76%    578
  312     +1.64%     +6.17%   +42.97%   -163.70%    578
  313     +1.62%     +6.08%   +42.44%   -159.05%    578
  314     +1.57%     +6.11%   +42.54%   -159.59%    578
  315     +1.56%     +6.01%   +44.01%   -167.26%    578
  316     +1.71%     +6.22%   +43.80%   -171.46%    573
  317     +1.71%     +6.05%   +45.10%   -168.20%    573
  318     +1.76%     +6.26%   +44.23%   -164.89%    573
  319     +1.71%     +6.12%   +43.85%   -159.91%    573
  320     +1.56%     +5.85%   +43.70%   -163.27%    573
  321     +1.75%     +6.08%   +44.06%   -161.47%    566
  322     +1.93%     +6.16%   +44.44%   -149.44%    566
  323     +1.86%     +6.04%   +44.67%   -163.98%    566
  324     +1.84%     +6.09%   +45.17%   -162.60%    566
  325     +1.81%     +6.23%   +44.21%   -160.26%    566
  326     +1.70%     +6.25%   +44.22%   -147.25%    561
  327     +1.80%     +6.26%   +44.06%   -146.02%    561
  328     +1.81%     +6.23%   +44.30%   -144.86%    561
  329     +1.90%     +6.12%   +43.80%   -146.85%    560
  330     +1.75%     +6.20%   +43.65%   -156.03%    561
  331     +1.83%     +6.03%   +44.06%   -150.92%    553
  332     +1.87%     +6.35%   +44.45%   -154.04%    553
  333     +1.89%     +6.37%   +44.12%   -151.91%    554
  334     +1.82%     +6.40%   +43.69%   -147.90%    554
  335     +1.80%     +6.32%   +42.95%   -154.98%    554
  336     +1.86%     +6.45%   +43.36%   -178.36%    547
  337     +1.91%     +6.43%   +44.17%   -185.61%    547
  338     +1.92%     +6.57%   +45.10%   -191.60%    547
  339     +1.98%     +6.68%   +45.43%   -196.02%    547
  340     +1.83%     +6.35%   +44.58%   -197.47%    547
  341     +1.91%     +6.31%   +43.86%   -195.13%    540
  342     +2.13%     +6.38%   +43.91%   -197.29%    540
  343     +2.15%     +6.42%   +43.85%   -200.26%    540
  344     +2.18%     +6.69%   +44.74%   -201.04%    540
  345     +1.82%     +6.18%   +43.99%   -193.49%    540
  346     +2.06%     +6.30%   +44.30%   -201.71%    478
  347     +2.21%     +6.22%   +44.67%   -205.39%    478
  348     +2.27%     +6.20%   +44.09%   -214.31%    478
  349     +2.28%     +6.46%   +42.77%   -214.91%    478
  350     +2.17%     +6.29%   +44.21%   -213.49%    478
  351     +2.28%     +6.50%   +45.31%   -217.70%    464
  352     +2.24%     +6.62%   +44.97%   -210.26%    464
  353     +2.13%     +6.63%   +44.47%   -211.64%    464
  354     +2.19%     +6.49%   +43.40%   -212.79%    464
  355     +2.19%     +6.55%   +43.25%   -217.40%    464
  356     +2.12%     +6.25%   +42.85%   -215.54%    442
  357     +2.65%     +6.96%   +43.05%   -223.05%    442
  358     +2.44%     +6.62%   +43.13%   -223.01%    442
  359     +2.35%     +6.70%   +43.29%   -230.78%    442
  360     +2.60%     +6.84%   +44.93%   -239.96%    442

--- PEAK P&L DISTRIBUTION ---
  Avg peak    : +11.25%
  Median peak : +9.81%
  % with peak > 0%  : 98.3%
  % with peak > 1%  : 96.0%
  % with peak > 2%  : 92.1%
  % with peak > 3%  : 89.0%
  % with peak > 4%  : 85.3%

--- SL/TP SIMULATION (post-run on raw trails) ---
  SL%    TP%   Trades   WinRate    TotalPnl     AvgPnl    AvgPct
   0.5%   1.0%      593     46.4%  ₹   34,719  ₹   58.55    +0.10%
   0.5%   2.0%      593     34.1%  ₹   26,049  ₹   43.93    +0.07%
   0.5%   3.0%      593     28.5%  ₹   46,870  ₹   79.04    +0.13%
   0.5%   4.0%      593     23.6%  ₹   58,490  ₹   98.63    +0.16%
   0.5%   5.0%      593     20.1%  ₹   60,114  ₹  101.37    +0.17%
   1.0%   2.0%      593     45.5%  ₹   60,646  ₹  102.27    +0.17%
   1.0%   3.0%      593     38.6%  ₹   92,312  ₹  155.67    +0.25%
   1.0%   4.0%      593     32.2%  ₹   96,714  ₹  163.09    +0.27%
   1.0%   5.0%      593     28.2%  ₹  106,514  ₹  179.62    +0.29%
   1.5%   2.0%      593     54.0%  ₹   93,576  ₹  157.80    +0.26%
   1.5%   3.0%      593     46.9%  ₹  132,386  ₹  223.25    +0.37%
   1.5%   4.0%      593     41.0%  ₹  166,537  ₹  280.84    +0.46%
   1.5%   5.0%      593     36.6%  ₹  191,352  ₹  322.69    +0.53%
   2.0%   3.0%      593     52.1%  ₹  142,504  ₹  240.31    +0.39%
   2.0%   4.0%      593     46.9%  ₹  198,374  ₹  334.53    +0.55%
   2.0%   5.0%      593     41.5%  ₹  199,357  ₹  336.18    +0.55%
   3.0%   4.0%      593     54.5%  ₹  209,115  ₹  352.64    +0.58%
   3.0%   5.0%      593     50.1%  ₹  242,997  ₹  409.78    +0.67%

--- TRAILING STOP SIMULATION ---
 Trail%   MinAct%   Trades   WinRate    TotalPnl     AvgPnl    AvgPct
     0.5%      0.5%      593     75.9%  ₹   20,999  ₹   35.41    +0.06%
     0.5%      1.0%      593     88.0%  ₹  -23,612  ₹  -39.82    -0.07%
     0.5%      2.0%      593     90.7%  ₹   36,166  ₹   60.99    +0.10%
     1.0%      0.5%      593     64.2%  ₹   62,593  ₹  105.55    +0.17%
     1.0%      1.0%      593     77.4%  ₹   27,343  ₹   46.11    +0.08%
     1.0%      2.0%      593     89.5%  ₹   84,484  ₹  142.47    +0.23%
     1.5%      0.5%      593     58.7%  ₹   97,465  ₹  164.36    +0.27%
     1.5%      1.0%      593     66.3%  ₹   45,087  ₹   76.03    +0.12%
     1.5%      2.0%      593     86.7%  ₹  134,834  ₹  227.38    +0.37%
     2.0%      0.5%      593     53.3%  ₹  156,114  ₹  263.26    +0.43%
     2.0%      1.0%      593     58.9%  ₹  101,404  ₹  171.00    +0.28%
     2.0%      2.0%      593     79.4%  ₹  206,611  ₹  348.42    +0.57%
     
'''