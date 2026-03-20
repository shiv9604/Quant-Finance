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
existing_files    = glob.glob("nifty_1min_*.csv")

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

    # Load
    df = pd.read_csv(path)
    if verbose:
        print(f"  ✓ Loaded {len(df):,} rows from {os.path.basename(path)}")
        print(f"  Columns: {df.columns.tolist()}")

    # Parse symbol into components
    parsed = df["symbol"].apply(parse_symbol).apply(pd.Series)
    df     = pd.concat([df, parsed], axis=1)

    # Filter time window
    df["time"] = pd.to_datetime(df["time"], format="%H:%M:%S").dt.time
    time_from_t = pd.to_datetime(time_from).time()
    time_to_t   = pd.to_datetime(time_to).time()
    df = df[(df["time"] >= time_from_t) & (df["time"] <= time_to_t)]

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
                            consolidation_exit: bool = True) -> dict:
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

    # Track last consolidation check time to avoid checking every minute
    last_consol_check = None

    for t in common_times:
        ce_curr = ce_ticks[t]
        pe_curr = pe_ticks[t]

        # Seller P&L: entry premium - current premium (seller profits as premium decays)
        seller_pnl_rs  = round(((ce_entry_ltp - ce_curr) + (pe_entry_ltp - pe_curr)) * lot_size, 2)
        seller_pnl_pct = round((seller_pnl_rs / total_capital) * 100, 2)

        pnl_trail.append({
            "time"    : t,
            "pnl_rs"  : seller_pnl_rs,
            "pnl_pct" : seller_pnl_pct,
            "ce_ltp"  : ce_curr,
            "pe_ltp"  : pe_curr
        })

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

        # ── Exit 2: SL (market kept moving, seller in pain) ─────────
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
                "pnl_trail"     : pnl_trail
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
                "pnl_trail"     : pnl_trail
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
        # ── Exit 4: Premium rebuild detection ───────────────────────
        # Check every minute (60 seconds)
        # Exit when combined premium stops decaying and starts rebuilding
        # This directly measures whether seller's edge is reversing
        if consolidation_exit and len(pnl_trail) >= 6:
            t_dt = pd.Timestamp(f"2000-01-01 {t}")
            if last_consol_check is None or (t_dt - pd.Timestamp(f"2000-01-01 {last_consol_check}")).seconds >= 60:
                last_consol_check = t

                # Combined premium over last 5 minutes
                recent         = pnl_trail[-6:]        # last 6 rows = ~5 mins
                combined_now   = ce_curr + pe_curr
                combined_5m    = recent[0]['ce_ltp'] + recent[0]['pe_ltp']
                combined_mid   = recent[3]['ce_ltp'] + recent[3]['pe_ltp']

                # Premium is rebuilding if:
                # A. Combined premium NOW is higher than 5 mins ago
                # B. AND higher than midpoint (confirming upward direction)
                premium_rebuilding = (
                    combined_now > combined_5m and      # higher than 5m ago
                    combined_now > combined_mid         # higher than midpoint too
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
                        "pnl_trail"     : pnl_trail
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
        "pnl_trail"     : pnl_trail
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
  

# ══════════════════════════════════════════════════════════
# STEP 4 BACKTEST LOOP — Consolidation + Smart Expiry
# ══════════════════════════════════════════════════════════
import datetime

# Replace with
'''
BACKTEST_START_5 = pd.Timestamp("2021-02-15")
BACKTEST_END_5   = pd.Timestamp("2024-10-31")


BACKTEST_START_5 = pd.Timestamp("2024-01-01")
BACKTEST_END_5   = pd.Timestamp("2024-01-31") 
'''
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
VOL_SCAN_TO       = datetime.time(10,  0)   # stop looking for entries at 15:00
VOL_FORCED_EXIT   = datetime.time(15, 25)   # hard close all positions

LOT_SIZE_6        = 65
NUM_LOTS_6        = 4
EFFECTIVE_LOTS_6  = LOT_SIZE_6 * NUM_LOTS_6   # 260

# ── Peak vol filter parameters ────────────────────────────────────────
VOL_LOOKBACK_MINS = 15    # how far back to look for premium peak
VOL_PEAK_PCT      = 0.85  # premium must be within 15% of rolling high
VOL_SL_PCT        = 0.015 # 1.5% of capital
VOL_TP_PCT        = 0.04  # 4.0% of capital (same as long side)

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
            consolidation_exit= True
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

    print(f"\nMonthly P&L:")
    monthly_6 = trades_df_6.groupby("month")["pnl_rs"].sum()
    print(monthly_6.to_string())

    # Save
    _s6 = BACKTEST_START_6.strftime("%Y%m%d")
    _e6 = BACKTEST_END_6.strftime("%Y%m%d")

    _trades_file_6    = f"short-straddle-{_s6}-{_e6}-backtest-trades.csv"
    _trail_file_6     = f"short-straddle-{_s6}-{_e6}-pnl-trail.csv"
    _portfolio_file_6 = f"short-straddle-{_s6}-{_e6}-portfolio.xlsx"

    trades_df_6.to_csv(_trades_file_6, index=False)
    print(f"\n✅ Trade log saved to {_trades_file_6}")

    trail_df_6 = pd.DataFrame(trails_6)
    trail_df_6.to_csv(_trail_file_6, index=False)
    print(f"✅ P&L trail saved to {_trail_file_6}")

    trades_to_mt5_xlsx(
        trades_df     = trades_df_6,
        output_path   = _portfolio_file_6,
        start_capital = 1_000_000,
        symbol        = "NIFTY"
    )

else:
    print("No trades entered — check peak volatility parameters")
    
    '''