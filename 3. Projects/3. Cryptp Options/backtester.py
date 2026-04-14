    """
    BTCUSD – Intraday Volatility Expansion Window Analysis
    Adapted from the NIFTY analysis. BTC trades 24/7, so there is no
    market-hours filter; the full UTC day is analysed.

    Data source: data/BTCUSD/spot/BTCUSDT-1m-*.csv  (Binance klines format)
    """

    import os
    import glob
    import pandas as pd
    import matplotlib.pyplot as plt
    import warnings
    warnings.filterwarnings("ignore")
    from tqdm import tqdm

    # ==================== DATA PREPARATION ====================

    SPOT_DIR = "data/BTCUSD/spot"
    EXCEL_CACHE = os.path.join("data/BTCUSD/spot", "BTCUSDT_1m_combined.xlsx")
    BINANCE_COLS = [
        "open_time", "Open", "High", "Low", "Close", "Volume",
        "close_time", "quote_vol", "trades", "taker_base", "taker_quote", "ignore"
    ]

    if os.path.exists(EXCEL_CACHE):
        print(f"Loading combined data from cache: {EXCEL_CACHE}")
        raw = pd.read_excel(EXCEL_CACHE)
        raw["DateTime"] = pd.to_datetime(raw["DateTime"], utc=True)
    else:
        files = sorted(glob.glob(os.path.join(SPOT_DIR, "BTCUSDT-1m-*.csv")))
        if not files:
            raise FileNotFoundError(f"No 1-minute CSV files found in {SPOT_DIR}")

        print(f"Found {len(files)} CSV files. Processing...")
        chunks = []
        for f in files:
            tmp = pd.read_csv(f, header=None, names=BINANCE_COLS)
            # Detect ms vs µs per file — ms: ~1.7e12, µs: ~1.7e15
            sample = tmp["open_time"].dropna().iloc[0]
            unit = "us" if sample > 1e14 else "ms"
            tmp["DateTime"] = pd.to_datetime(tmp["open_time"], unit=unit, utc=True, errors="coerce")
            chunks.append(tmp)

        raw = pd.concat(chunks, ignore_index=True)
        raw.dropna(subset=["DateTime"], inplace=True)
        raw.sort_values("DateTime", inplace=True)
        raw.drop_duplicates(subset="DateTime", inplace=True)

        export_df = raw[["DateTime", "Open", "High", "Low", "Close", "Volume"]].copy()
        export_df["DateTime"] = export_df["DateTime"].dt.tz_localize(None)
        print(f"Saving {len(export_df):,} rows to {EXCEL_CACHE} ...")
        export_df.to_excel(EXCEL_CACHE, index=False)
        print("Saved.")

    analysis_df = raw[["DateTime", "Open", "High", "Low", "Close", "Volume"]].copy()
    analysis_df.set_index("DateTime", inplace=True)
    analysis_df.index = analysis_df.index.tz_convert("Asia/Kolkata")   # all times → IST
    analysis_df = analysis_df.apply(pd.to_numeric, errors="coerce")

    print(f"Dataset loaded: {len(analysis_df):,} candles  "
        f"from {analysis_df.index.min()} to {analysis_df.index.max()}")

    # BTC is 24/7 – keep all hours
    trading_df = analysis_df.copy()

    # 5-minute rolling volatility (% returns)
    trading_df["Returns"] = trading_df["Close"].pct_change() * 100
    trading_df["5min_Volatility"] = trading_df["Returns"].rolling(5).std()

    # Helper columns
    trading_df["Date"] = trading_df.index.date
    trading_df["Time"] = trading_df.index.time

    print("=" * 70)
    print("BTCUSD – INTRADAY VOLATILITY EXPANSION ANALYSIS (24/7)")
    print("=" * 70)
    print(f"Data Range   : {trading_df.index.min()} → {trading_df.index.max()}")
    print(f"Trading Days : {trading_df['Date'].nunique()}")


    # ==================== FIND INTRADAY EXPANSION WINDOWS ====================

    def find_intraday_expansion_windows(data, expansion_threshold=20):
        """
        Identify volatility expansion windows within the same UTC calendar day.
        Uses 15-minute resampling to smooth noise.
        """
        all_windows = []

        for date, day_data in data.groupby("Date"):
            if len(day_data) < 50:
                continue

            day_15min = day_data.resample("15min").agg(
                {"5min_Volatility": "mean", "Close": "last"}
            ).dropna()

            if len(day_15min) < 10:
                continue

            vol_series = day_15min["5min_Volatility"].values

            for i in range(2, len(vol_series) - 2):
                # Local minimum → convergence (potential entry)
                if (vol_series[i] < vol_series[i - 1] and
                        vol_series[i] < vol_series[i - 2] and
                        vol_series[i] < vol_series[i + 1] and
                        vol_series[i] < vol_series[i + 2]):

                    # Next local maximum → peak (potential exit)
                    for j in range(i + 1, len(vol_series) - 2):
                        if (vol_series[j] > vol_series[j - 1] and
                                vol_series[j] > vol_series[j - 2] and
                                vol_series[j] > vol_series[j + 1] and
                                vol_series[j] > vol_series[j + 2]):

                            expansion_pct = (
                                (vol_series[j] - vol_series[i]) / vol_series[i] * 100
                                if vol_series[i] > 0 else 0
                            )

                            if expansion_pct >= expansion_threshold and (j - i) >= 3:
                                start_time = day_15min.index[i].time()
                                end_time   = day_15min.index[j].time()

                                if start_time < end_time:
                                    all_windows.append({
                                        "Date":          date,
                                        "Start_Time":    start_time,
                                        "End_Time":      end_time,
                                        "Start_Vol":     round(vol_series[i], 4),
                                        "End_Vol":       round(vol_series[j], 4),
                                        "Expansion_Pct": round(expansion_pct, 1),
                                        "Duration_Min":  (
                                            (day_15min.index[j] - day_15min.index[i])
                                            .total_seconds() / 60
                                        ),
                                    })
                            break  # only take the first peak after each trough

        return pd.DataFrame(all_windows)


    windows_df = find_intraday_expansion_windows(trading_df, expansion_threshold=30)
    print(f"\nFound {len(windows_df)} intraday expansion windows (same-day only)")


    # ==================== MOST CONSISTENT WINDOWS ====================

    print("\n" + "=" * 70)
    print("MOST CONSISTENT INTRADAY WINDOWS (Top 10 by Frequency)")
    print("=" * 70)

    if not windows_df.empty:
        windows_df["Window"] = (
            windows_df["Start_Time"].apply(lambda x: x.strftime("%H:%M"))
            + " → "
            + windows_df["End_Time"].apply(lambda x: x.strftime("%H:%M"))
        )

        window_stats = windows_df.groupby("Window").agg(
            Avg_Expansion=("Expansion_Pct", "mean"),
            Std_Expansion=("Expansion_Pct", "std"),
            Avg_Duration=("Duration_Min", "mean"),
            Frequency=("Expansion_Pct", "count"),
        ).round(2)

        window_stats = window_stats.sort_values("Frequency", ascending=False)

        print("\nTop 10 Most Consistent Windows (Occurred Most Often):")
        print("-" * 70)
        for idx, (window, stats) in enumerate(window_stats.head(10).iterrows(), 1):
            print(
                f"{idx:2d}. {window:15s} | Freq: {int(stats['Frequency']):3d} days | "
                f"Avg Exp: {stats['Avg_Expansion']:6.1f}% | "
                f"Duration: {stats['Avg_Duration']:3.0f} min"
            )

        # ==================== BEST TIME WINDOWS BY HOUR ====================
        print("\n" + "=" * 70)
        print("BEST ENTRY & EXIT TIMES BY HOUR (UTC)")
        print("=" * 70)

        entry_stats = windows_df.groupby(
            windows_df["Start_Time"].apply(lambda x: x.hour)
        ).agg(Avg_Expansion=("Expansion_Pct", "mean"), Count=("Expansion_Pct", "count"))

        print("\nBest Entry Hours – Volatility Convergence (UTC):")
        print("-" * 50)
        for hour, stats in entry_stats.sort_values("Avg_Expansion", ascending=False).head(5).iterrows():
            print(
                f"  {hour:02d}:00 UTC | Avg Expansion: {stats['Avg_Expansion']:.1f}% | "
                f"Occurred: {stats['Count']} times"
            )

        exit_stats = windows_df.groupby(
            windows_df["End_Time"].apply(lambda x: x.hour)
        ).agg(Avg_Expansion=("Expansion_Pct", "mean"), Count=("Expansion_Pct", "count"))

        print("\nBest Exit Hours – Volatility Peak (UTC):")
        print("-" * 50)
        for hour, stats in exit_stats.sort_values("Avg_Expansion", ascending=False).head(5).iterrows():
            print(
                f"  {hour:02d}:00 UTC | Avg Expansion: {stats['Avg_Expansion']:.1f}% | "
                f"Occurred: {stats['Count']} times"
            )

        # ==================== RELIABLE WINDOWS (≥ 20 % of days) ====================
        print("\n" + "=" * 70)
        print("RECOMMENDED TRADING WINDOWS")
        print("=" * 70)

        total_days = trading_df["Date"].nunique()
        min_frequency = total_days * 0.20

        reliable_windows = window_stats[window_stats["Frequency"] >= min_frequency]

        if not reliable_windows.empty:
            print(f"\nReliable Windows (occurred on ≥20 % of trading days):")
            print("-" * 70)
            for window, stats in reliable_windows.sort_values("Avg_Expansion", ascending=False).iterrows():
                occ_rate = (stats["Frequency"] / total_days) * 100
                print(f"• {window:15s} | Occurrence: {occ_rate:.1f}% of days")
                print(f"  Avg Expansion: {stats['Avg_Expansion']:.1f}%  |  "
                    f"Duration: {stats['Avg_Duration']:.0f} min")
                print()
        else:
            print("No windows met the 20 % frequency threshold.")
            top = window_stats.iloc[0]
            top_name = window_stats.index[0]
            print(
                f"Highest-frequency window: {top_name}  "
                f"({int(top['Frequency'])}/{total_days} days = "
                f"{(top['Frequency'] / total_days * 100):.1f}%)"
            )

        # ==================== VISUALIZATION ====================
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle("BTCUSD – Intraday Volatility Expansion Patterns (UTC)",
                    fontsize=16, fontweight="bold")

        # 1. Heatmap: optimal trading times
        heatmap_data = []
        for hour in range(0, 24):
            for minute in [0, 15, 30, 45]:
                time_str = f"{hour:02d}:{minute:02d}"
                start_count = len(windows_df[
                    windows_df["Start_Time"].apply(lambda x: x.strftime("%H:%M")) == time_str
                ])
                end_count = len(windows_df[
                    windows_df["End_Time"].apply(lambda x: x.strftime("%H:%M")) == time_str
                ])
                heatmap_data.append({
                    "Hour": hour, "Minute": minute,
                    "Start_Count": start_count,
                    "End_Count": end_count,
                    "Total": start_count + end_count,
                })

        heatmap_df = pd.DataFrame(heatmap_data)
        pivot_table = heatmap_df.pivot_table(index="Hour", columns="Minute", values="Total")

        im = axes[0, 0].imshow(pivot_table.values, aspect="auto", cmap="YlOrRd")
        axes[0, 0].set_title("Optimal Trading Times Heatmap (UTC)", fontweight="bold")
        axes[0, 0].set_xlabel("Minute")
        axes[0, 0].set_ylabel("Hour (UTC)")
        axes[0, 0].set_xticks(range(4))
        axes[0, 0].set_xticklabels([0, 15, 30, 45])
        axes[0, 0].set_yticks(range(len(pivot_table.index)))
        axes[0, 0].set_yticklabels([f"{h:02d}:00" for h in pivot_table.index])
        plt.colorbar(im, ax=axes[0, 0], label="Window Count")

        # 2. Entry time distribution (all 24 hours)
        entry_hours = windows_df["Start_Time"].apply(lambda x: x.hour + x.minute / 60)
        axes[0, 1].hist(entry_hours, bins=48, edgecolor="black", color="lightgreen", alpha=0.7)
        axes[0, 1].set_title("Entry Time Distribution (UTC)", fontweight="bold")
        axes[0, 1].set_xlabel("Hour of Day (UTC)")
        axes[0, 1].set_ylabel("Frequency")
        axes[0, 1].set_xticks(range(0, 25, 4))
        axes[0, 1].set_xticklabels([f"{h:02d}:00" for h in range(0, 25, 4)])

        # 3. Expansion strength vs duration
        scatter = axes[1, 0].scatter(
            windows_df["Duration_Min"], windows_df["Expansion_Pct"],
            c=windows_df["Start_Time"].apply(lambda x: x.hour),
            cmap="viridis", alpha=0.6, s=50,
        )
        axes[1, 0].set_title("Expansion Strength vs Duration", fontweight="bold")
        axes[1, 0].set_xlabel("Duration (minutes)")
        axes[1, 0].set_ylabel("Expansion (%)")
        plt.colorbar(scatter, ax=axes[1, 0], label="Entry Hour (UTC)")

        # 4. Most frequent windows (bar chart)
        top_windows = window_stats.head(8)
        y_pos = range(len(top_windows))
        axes[1, 1].barh(y_pos, top_windows["Frequency"], color="steelblue", alpha=0.7)
        axes[1, 1].set_yticks(y_pos)
        axes[1, 1].set_yticklabels(top_windows.index, fontsize=9)
        axes[1, 1].set_title("Most Frequent Trading Windows", fontweight="bold")
        axes[1, 1].set_xlabel("Frequency (days)")

        plt.tight_layout()
        plt.show()

        # ==================== STRATEGY SUMMARY ====================
        print("\n" + "=" * 70)
        print("TRADING STRATEGY RECOMMENDATIONS")
        print("=" * 70)

        if len(window_stats) > 0:
            best_window_name = window_stats.index[0]
            best_window = window_stats.iloc[0]
            start_t, end_t = best_window_name.split(" → ")

            print(f"\nPRIMARY STRATEGY: Trade the {best_window_name} window (UTC)")
            print(f"   Entry ~{start_t} UTC  (volatility convergence)")
            print(f"   Exit  ~{end_t} UTC  (volatility peak)")
            print(f"   Expected expansion : {best_window['Avg_Expansion']:.1f}%")
            print(f"   Duration           : {best_window['Avg_Duration']:.0f} min")
            print(
                f"   Reliability        : {int(best_window['Frequency'])}/{total_days} days "
                f"({(best_window['Frequency'] / total_days * 100):.1f}%)"
            )

        print("\nALTERNATIVE STRATEGIES:")
        for idx, (window, stats) in enumerate(window_stats.head(4).iterrows(), 1):
            if idx == 1:
                continue
            start_t, end_t = window.split(" → ")
            print(
                f"{idx:2d}. {window:15s} | Freq: {int(stats['Frequency']):3d} days | "
                f"Avg Exp: {stats['Avg_Expansion']:6.1f}% | "
                f"Duration: {stats['Avg_Duration']:3.0f} min"
            )

        print("\nRISK MANAGEMENT:")
        print("   • BTC is 24/7 – no forced session close, but respect your risk limits")
        print("   • Use ATR or rolling-vol for position sizing, not fixed lots")
        print("   • Set stops based on the entry volatility level (e.g. 1.5× entry vol)")
        print("   • Be extra cautious around macro events (FOMC, CPI, etc.)")

        # Save results
        os.makedirs("analysis", exist_ok=True)
        out_path = "analysis/btcusd_intraday_expansion_windows.csv"
        windows_df.to_csv(out_path, index=False)
        print(f"\nResults saved to '{out_path}'")

    else:
        print("No intraday expansion windows found with the current parameters.")
        print("Try lowering the expansion_threshold argument.")

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)


    # ==================== VOLATILITY SHORT STRANGLE BACKTEST ====================
    import datetime

    # ── 1. Options Symbol Parser ──────────────────────────────────────────────

    def parse_btc_option_symbol(symbol: str) -> dict:                                                                                                                                                       
        """C-BTC-99000-011224 → {opt_type, strike, expiry_str}"""
        parts      = symbol.split("-")                                                                                                                                                                      
        opt_type   = "CE" if parts[0] == "C" else "PE"                                                                                                                                                    
        strike     = float(parts[2])                                                                                                                                                                        
        raw_expiry = parts[3]                                          # DDMMYY                                                                                                                           
        expiry_str = f"20{raw_expiry[4:6]}-{raw_expiry[2:4]}-{raw_expiry[:2]}"                                                                                                                              
        return {"opt_type": opt_type, "strike": strike, "expiry_str": expiry_str}                                                                                                                           
                                                                                                                                                                                                            
                                                                                                                                                                                                            
    # ── 2. Options Loader ─────────────────────────────────────────────────────                                                                                                                          
                                                                                                                                                                                                            
    def load_btc_options_for_date(date: pd.Timestamp, spot: float,                                                                                                                                          
                                    strike_range: int = 5000,                                                                                                                                              
                                    options_dir: str = "data/BTCUSD/options") -> pd.DataFrame:                                                                                                               
        """                                                                                                                                                                                               
        Load BTC options ticks for a given date, resample to 1-min close,                                                                                                                                   
        filter to strikes within ±strike_range of spot.                                                                                                                                                     
        Returns columns: expiry_str, strike, option_type, time, close                                                                                                                                       
        """                                                                                                                                                                                                 
        ym       = date.strftime("%Y-%m")                                                                                                                                                                   
        filepath = os.path.join(options_dir, f"BTC_{ym}.csv")                                                                                                                                               
        if not os.path.exists(filepath):                                                                                                                                                                    
            return pd.DataFrame()                                                                                                                                                                         
                                                                                                                                                                                                            
        df = pd.read_csv(filepath)                                                                                                                                      
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
        df = df[df["timestamp"].dt.date == date.date()].copy()                                                                                                                                            
        if df.empty:                                                                                                                                                                                        
            return pd.DataFrame()                                                                                                                                                                         
                                                                                                                                                                                                            
        parsed             = df["product_symbol"].apply(parse_btc_option_symbol)                                                                                                                            
        df["option_type"]  = parsed.apply(lambda x: x["opt_type"])
        df["strike"]       = parsed.apply(lambda x: x["strike"])                                                                                                                                            
        df["expiry_str"]   = parsed.apply(lambda x: x["expiry_str"])                                                                                                                                      
                                                                                                                                                                                                            
        df = df[df["strike"].between(spot - strike_range, spot + strike_range)]                                                                                                                           
                                                                                                                                                                                                            
        df["time"] = df["timestamp"].dt.floor("1min").dt.time                                                                                                                                               
        df_1m = (df.groupby(["expiry_str", "strike", "option_type", "time"])["price"]                                                                                                                     
                    .last()                                                                                                                                                                                  
                    .reset_index()                                                                                                                                                                           
                    .rename(columns={"price": "close"}))                                                                                                                                                     
        return df_1m                                                                                                                                                                                        
                                                                                                                                                                                                            
    # ── 3. Nearest Expiry Selector ────────────────────────────────────────────
                                                                                                                                                                                                            
    def get_btc_nearest_expiry(options_df: pd.DataFrame, trade_date: pd.Timestamp) -> str:                                                                                                                
        """Pick the nearest expiry on or after trade_date."""                                                                                                                                             
        expiries = pd.to_datetime(options_df["expiry_str"].unique())                                                                                                                                        
        future   = sorted([e for e in expiries if e >= trade_date])                                                                                                                                         
        return str(future[0].date()) if future else None                                                                                                                                                    
                                                                                                                                                                                                            
                                                                                                                                                                                                            
    # ── 4. Peak Volatility Detector (BTC-scaled) ─────────────────────────────                                                                                                                             
                                                                                                                                                                                                            
    def detect_peak_volatility_btc(spot_df: pd.DataFrame, date,                                                                                                                                           
                                    scan_from=datetime.time(0, 0),                                                                                                                                        
                                    scan_to=datetime.time(23, 59),                                                                                                                                          
                                    min_candles: int = 3) -> dict:                                                                                                                                          
        """                                                                                                                                                                                                 
        Scans 5-min BTC spot candles for a high-volatility window.                                                                                                                                          
        Thresholds scaled for BTC (vs NIFTY pts in KCIM):                                                                                                                                                   
            min_range : $200   (NIFTY: 40 pts)                                                                                                                                                                
            atr       : $100   (NIFTY: 20 pts)                                                                                                                                                                
            body      : $75    (NIFTY: 15 pts)                                                                                                                                                                
        Returns ATM strike rounded to nearest $1000.                                                                                                                                                        
        """                                                                                                                                                                                                 
        min_range_pts  = 200.0                                                                                                                                                                            
        atr_threshold  = 100.0                                                                                                                                                                              
        body_threshold = 75.0                                                                                                                                                                             
                                                                                                                                                                                                            
        day_df = spot_df[                                                                                                                                                                                   
            (spot_df["Date"] == date) &                                                                                                                                                                   
            (spot_df["Time"] >= scan_from) &                                                                                                                                                                
            (spot_df["Time"] <= scan_to)                                                                                                                                                                  
        ].copy()                                                                                                                                                                                          

        if day_df.empty:                                                                                                                                                                                    
            return {"found": False}
                                                                                                                                                                                                            
        day_5m = (day_df.set_index("DateTime")                                                                                                                                                            
                    .resample("5min")                                                                                                                                                                     
                    .agg(open=("Open","first"), high=("High","max"),                                                                                                                                        
                        low=("Low","min"),     close=("Close","last"))
                    .dropna()                                                                                                                                                                               
                    .reset_index())                                                                                                                                                                       
        day_5m["Time"] = day_5m["DateTime"].dt.time                                                                                                                                                         
                                                                                                                                                                                                            
        if len(day_5m) < min_candles:                                                                                                                                                                       
            return {"found": False}
                                                                                                                                                                                                            
        day_5m["prev_close"] = day_5m["close"].shift(1)                                                                                                                                                   
        day_5m["tr"] = day_5m.apply(                                                                                                                                                                      
            lambda r: max(                                                                                                                                                                                  
                r["high"] - r["low"],
                abs(r["high"] - r["prev_close"]) if not pd.isna(r["prev_close"]) else 0,                                                                                                                    
                abs(r["low"]  - r["prev_close"]) if not pd.isna(r["prev_close"]) else 0                                                                                                                     
            ), axis=1                                                                                                                                                                                       
        )                                                                                                                                                                                                   
        day_5m["body"] = (day_5m["close"] - day_5m["open"]).abs()                                                                                                                                           
                                                                                                                                                                                                            
        for i in range(len(day_5m) - min_candles + 1):                                                                                                                                                    
            w = day_5m.iloc[i: i + min_candles]                                                                                                                                                             
            if ((w["high"].max() - w["low"].min()) >= min_range_pts and                                                                                                                                     
                    w["tr"].mean() >= atr_threshold and                                                                                                                                                   
                    w["body"].max() >= body_threshold):                                                                                                                                                     
                signal_candle = w.iloc[-1]                                                                                                                                                                
                spot_price    = signal_candle["close"]                                                                                                                                                      
                atm_strike    = round(spot_price / 1000) * 1000   # nearest $1000                                                                                                                           
                return {                                                                                                                                                                                    
                    "found"       : True,                                                                                                                                                                   
                    "signal_time" : signal_candle["Time"],                                                                                                                                                  
                    "level"       : atm_strike,                                                                                                                                                           
                    "zone_range"  : round(w["high"].max() - w["low"].min(), 2),                                                                                                                             
                    "avg_atr"     : round(w["tr"].mean(), 2),
                    "max_body"    : round(w["body"].max(), 2),                                                                                                                                              
                    "ce_strike"   : atm_strike,           # resolved dynamically in loop
                    "pe_strike"   : atm_strike,           # resolved dynamically in loop                                                                                                                                                             
                }                                                                                                                                                                                           
        return {"found": False}                                                                                                                                                                           
                                                                                                                                                                                                            
                                                                                                                                                                                                            
    # ── 5. Walk-Forward P&L (Short Strangle) ─────────────────────────────────

    def walk_forward_pnl_short_btc(opt_groups: dict, expiry: str,
                                    ce_strike: float, pe_strike: float,
                                    ce_entry_ltp: float, pe_entry_ltp: float,
                                    signal_time,
                                    lot_size: int = 100,
                                    sl_pct: float = 0.80,
                                    tp_pct: float = 999.0,
                                    forced_exit_time=datetime.time(17, 25),
                                    prem_rebuild_n: int = 6) -> dict:
        """
        Walk forward minute by minute after SELLING BTC OTM CE + PE (strangle).
        Seller P&L = (entry_premium - current_premium) x lot_size  [in USD]
        Exit conditions (first hit):
            SL     : loss  >= sl_pct x entry_premium
            TP     : gain  >= tp_pct x entry_premium
            FORCED : forced_exit_time reached (17:25 IST)
        Tracks min_offset and peak_pnl per minute for KCIM-style analysis.
        """                                                                                                                                                                                                       
        prem_consec_up = 0          # consecutive minutes combined premium is rising
        prev_combined  = None       # previous tick combined premium
        entry_premium = (ce_entry_ltp + pe_entry_ltp) * lot_size
        sl_trigger    = entry_premium * sl_pct
        tp_trigger    = entry_premium * tp_pct

        no_data = {"exit_reason": "NO_DATA", "exit_time": None,
                "pnl_usd": 0.0, "pnl_pct": 0.0, "peak_pnl_usd": 0.0,
                "total_capital": round(entry_premium, 2), "pnl_trail": []}

        ce_grp = opt_groups.get((expiry, ce_strike, "CE"))
        pe_grp = opt_groups.get((expiry, pe_strike, "PE"))
        if ce_grp is None or pe_grp is None:
            return no_data

        ce_ticks = ce_grp[ce_grp["time"] > signal_time].set_index("time")["close"]
        pe_ticks = pe_grp[pe_grp["time"] > signal_time].set_index("time")["close"]
        common   = sorted(set(ce_ticks.index) & set(pe_ticks.index))

        if not common:
            return no_data

        entry_dt  = pd.Timestamp(f"2000-01-01 {signal_time}")
        peak_pnl  = float("-inf")
        pnl_trail = []

        for t in common:
            ce_curr = ce_ticks[t]
            pe_curr = pe_ticks[t]
            pnl_usd = ((ce_entry_ltp - ce_curr) + (pe_entry_ltp - pe_curr)) * lot_size
            pnl_pct = (pnl_usd / entry_premium) * 100 if entry_premium > 0 else 0
            mins    = int(round((pd.Timestamp(f"2000-01-01 {t}") - entry_dt).total_seconds() / 60))

            pnl_trail.append({
                "time"       : t,
                "min_offset" : mins,
                "pnl_usd"    : round(pnl_usd, 2),
                "pnl_pct"    : round(pnl_pct, 2),
                "ce_ltp"     : ce_curr,
                "pe_ltp"     : pe_curr,
            })

            if pnl_usd > peak_pnl:
                peak_pnl = pnl_usd

            # ── Premium rebuild tracker ───────────────────────────────
            combined_now = ce_curr + pe_curr
            if prev_combined is not None:
                if combined_now > prev_combined:
                    prem_consec_up += 1
                else:
                    prem_consec_up = 0
            prev_combined = combined_now

            def _result(reason, _t=t, _pnl=pnl_usd, _pct=pnl_pct):
                return {"exit_reason": reason, "exit_time": _t,
                        "pnl_usd": round(_pnl, 2), "pnl_pct": round(_pct, 2),
                        "peak_pnl_usd": round(peak_pnl, 2),
                        "total_capital": round(entry_premium, 2), "pnl_trail": pnl_trail}

            if pnl_usd <= -sl_trigger:              return _result("SL")
            if prem_consec_up >= prem_rebuild_n:    return _result("PREM_REBUILD")
            if t >= forced_exit_time:               return _result("FORCED")

        last = pnl_trail[-1] if pnl_trail else {"time": None, "pnl_usd": 0.0, "pnl_pct": 0.0}
        return {"exit_reason": "FORCED", "exit_time": last["time"],
                "pnl_usd": last["pnl_usd"], "pnl_pct": last["pnl_pct"],
                "peak_pnl_usd": round(peak_pnl, 2) if peak_pnl != float("-inf") else 0.0,
                "total_capital": round(entry_premium, 2), "pnl_trail": pnl_trail}


    # ── 6. Backtest Loop ──────────────────────────────────────────────────────

    BT_START     = pd.Timestamp("2024-12-01")   # earliest available spot data
    BT_END       = pd.Timestamp("2025-11-30")   # last available spot data
    SCAN_FROM_BT = datetime.time(13, 15)        # IST — post-London-open spike
    SCAN_TO_BT   = datetime.time(15, 30)        # IST — buffer before forced exit
    FORCED_EXIT  = datetime.time(17, 25)        # IST — hard close
    LOT_SIZE     = 0.1                          # 0.1 contract → ~$72 capital/trade
    STARTING_BAL = 1500.0                       # starting balance in USD
    SL_PCT       = 0.80                         # stop-loss  : 80% of premium
    TP_PCT       = 999.0                        # take-profit : disabled (max gain ~100%)                                                                                                                         
    PREM_REBUILD_N = 6                          # exit if combined premium rises N consecutive mins
                                                                                                                                                                                                            
    spot_bt = trading_df.reset_index().copy()                                                                                                                                                               
    spot_bt["Date"] = spot_bt["DateTime"].dt.date                                                                                                                                                         
    spot_bt["Time"] = spot_bt["DateTime"].dt.time                                                                                                                                                           
                                                                                                                                                                                                            
    all_dates_bt = sorted(spot_bt[                                                                                                                                                                        
        (spot_bt["Date"] >= BT_START.date()) &
        (spot_bt["Date"] <= BT_END.date())                                                                                                                                                                  
    ]["Date"].unique())
                                                                                                                                                                                                            
    trades_bt, skipped_bt, trails_bt = [], [], []
    running_balance = STARTING_BAL

    print("\n" + "=" * 60)
    print("BTCUSD — VOLATILITY SHORT STRANGLE BACKTEST")
    print("=" * 60)
    print(f"Period        : {BT_START.date()} \u2192 {BT_END.date()}")
    print(f"Scan window   : {SCAN_FROM_BT} \u2192 {SCAN_TO_BT} IST")
    print(f"Forced exit   : {FORCED_EXIT} IST")
    print(f"Lot size      : {LOT_SIZE} contracts")
    print(f"SL / TP       : {SL_PCT*100:.0f}% / {TP_PCT*100:.0f}% of premium")
    print(f"Trading days  : {len(all_dates_bt)}")

    for date in tqdm(all_dates_bt, desc="Vol Short Backtest"):
        trade_date = pd.Timestamp(date)

        day_spot = spot_bt[spot_bt["Date"] == date]
        if day_spot.empty:
            skipped_bt.append({"date": date, "reason": "no_spot"}); continue

        spot_ref = float(day_spot["Close"].median())

        opt_df = load_btc_options_for_date(trade_date, spot_ref)
        if opt_df.empty:
            skipped_bt.append({"date": date, "reason": "no_options"}); continue

        opt_groups = {
            key: grp.sort_values("time").reset_index(drop=True)
            for key, grp in opt_df.groupby(["expiry_str", "strike", "option_type"])
        }

        expiry = get_btc_nearest_expiry(opt_df, trade_date)
        if expiry is None:
            skipped_bt.append({"date": date, "reason": "no_expiry"}); continue

        vol_signal = detect_peak_volatility_btc(spot_bt, date, SCAN_FROM_BT, SCAN_TO_BT)
        if not vol_signal["found"]:
            skipped_bt.append({"date": date, "reason": "no_vol_signal"}); continue

        signal_time = vol_signal["signal_time"]
        signal_hour = pd.Timestamp(f"2000-01-01 {signal_time}").hour
        atm          = vol_signal["level"]
        available    = sorted(opt_df["strike"].unique())
        ce_candidates = [s for s in available if s > atm]
        pe_candidates = [s for s in available if s < atm]
        if not ce_candidates or not pe_candidates:
            skipped_bt.append({"date": date, "reason": "no_otm_strikes"}); continue
        ce_stk = min(ce_candidates)   # nearest OTM call
        pe_stk = max(pe_candidates)   # nearest OTM put

        ce_grp = opt_groups.get((expiry, ce_stk, "CE"))
        pe_grp = opt_groups.get((expiry, pe_stk, "PE"))
        if ce_grp is None or pe_grp is None:
            skipped_bt.append({"date": date, "reason": "no_strike_in_options"}); continue

        ce_rows = ce_grp[ce_grp["time"] >= signal_time]
        pe_rows = pe_grp[pe_grp["time"] >= signal_time]
        if ce_rows.empty or pe_rows.empty:
            skipped_bt.append({"date": date, "reason": "no_entry_ltp"}); continue

        ce_entry = ce_rows["close"].iloc[0]
        pe_entry = pe_rows["close"].iloc[0]

        result = walk_forward_pnl_short_btc(
            opt_groups, expiry, ce_stk, pe_stk,
            ce_entry, pe_entry, signal_time,
            LOT_SIZE, SL_PCT, TP_PCT, FORCED_EXIT, PREM_REBUILD_N
        )

        running_balance += result["pnl_usd"]

        trades_bt.append({
            "date"          : date,
            "signal_time"   : signal_time,
            "signal_hour"   : signal_hour,
            "expiry"        : expiry,
            "ce_strike"     : ce_stk,
            "pe_strike"     : pe_stk,
            "ce_entry"      : ce_entry,
            "pe_entry"      : pe_entry,
            "combined_prem" : round(ce_entry + pe_entry, 2),
            "zone_range"    : vol_signal["zone_range"],
            "avg_atr"       : vol_signal["avg_atr"],
            "exit_time"     : result["exit_time"],
            "exit_reason"   : result["exit_reason"],
            "pnl_usd"       : result["pnl_usd"],
            "pnl_pct"       : result["pnl_pct"],
            "peak_pnl_usd"  : result["peak_pnl_usd"],
            "total_capital" : result["total_capital"],
            "balance"       : round(running_balance, 2),
        })

        # ── Per-minute trail log ──────────────────────────────────────────
        for tick in result.get("pnl_trail", []):
            trails_bt.append({
                "date"        : date,
                "signal_time" : signal_time,
                "signal_hour" : signal_hour,
                "exit_reason" : result["exit_reason"],
                "min_offset"  : tick["min_offset"],
                "time"        : tick["time"],
                "pnl_usd"     : tick["pnl_usd"],
                "pnl_pct"     : tick["pnl_pct"],
                "ce_ltp"      : tick["ce_ltp"],
                "pe_ltp"      : tick["pe_ltp"],
            })

    trades_bt_df  = pd.DataFrame(trades_bt)
    skipped_bt_df = pd.DataFrame(skipped_bt)
    trail_df      = pd.DataFrame(trails_bt)

    print(f"\nTrades entered : {len(trades_bt_df)}")
    print(f"Days skipped   : {len(skipped_bt_df)}")

    if not trades_bt_df.empty:
        wins     = trades_bt_df[trades_bt_df["pnl_usd"] > 0]
        losses   = trades_bt_df[trades_bt_df["pnl_usd"] <= 0]
        win_rate = round(len(wins) / len(trades_bt_df) * 100, 1)
        avg_cap  = trades_bt_df["total_capital"].mean()

        print(f"\n--- PERFORMANCE SUMMARY ---")
        print(f"Win rate          : {win_rate}%")
        print(f"Total P&L         : ${trades_bt_df['pnl_usd'].sum():,.2f}")
        print(f"Avg P&L / trade   : ${trades_bt_df['pnl_usd'].mean():,.2f}")
        print(f"Best trade        : ${trades_bt_df['pnl_usd'].max():,.2f}")
        print(f"Worst trade       : ${trades_bt_df['pnl_usd'].min():,.2f}")
        print(f"Avg capital/trade : ${avg_cap:,.2f}")
        print(f"Avg combined prem : ${trades_bt_df['combined_prem'].mean():,.2f}")
        print(f"Final balance     : ${running_balance:,.2f}  (started ${STARTING_BAL:,.2f})")
        print(f"Total return      : {((running_balance - STARTING_BAL) / STARTING_BAL * 100):.1f}%")

        print(f"\nExit reasons:")
        print(trades_bt_df["exit_reason"].value_counts().to_string())

        print(f"\nEntry time distribution (IST hour):")
        print(trades_bt_df["signal_hour"].value_counts().sort_index().to_string())

        print(f"\nMonthly P&L (wins / losses / net $ / win rate):")
        trades_bt_df["month"] = pd.to_datetime(trades_bt_df["date"]).dt.to_period("M")
        monthly = trades_bt_df.groupby("month").agg(
            trades   = ("pnl_usd", "count"),
            wins     = ("pnl_usd", lambda x: (x > 0).sum()),
            losses   = ("pnl_usd", lambda x: (x <= 0).sum()),
            net_usd  = ("pnl_usd", "sum"),
            avg_usd  = ("pnl_usd", "mean"),
        )
        monthly["win_rate"] = (monthly["wins"] / monthly["trades"] * 100).round(1)
        print(monthly.to_string())

        # ── Peak P&L distribution ─────────────────────────────────────────
        if "peak_pnl_usd" in trades_bt_df.columns:
            peak_pcts = (trades_bt_df["peak_pnl_usd"] / avg_cap * 100)
            print(f"\n--- PEAK P&L DISTRIBUTION ---")
            print(f"  Avg peak     : {peak_pcts.mean():+.2f}%")
            print(f"  Median peak  : {peak_pcts.median():+.2f}%")
            for threshold in [0, 10, 20, 30, 40]:
                print(f"  Trades with peak > {threshold}% : {(peak_pcts > threshold).mean()*100:.1f}%")

        # ── Minute-by-minute P&L profile ─────────────────────────────────
        if not trail_df.empty and "min_offset" in trail_df.columns:
            print(f"\n--- MINUTE-BY-MINUTE P&L PROFILE ---")
            print(f"{'Min':>4}  {'AvgPct':>8}  {'MedPct':>8}  {'Best%':>7}  {'Worst%':>8}  {'n':>5}")
            mprofile = (trail_df.groupby("min_offset")["pnl_pct"]
                        .agg(["mean", "median", "max", "min", "count"])
                        .reset_index())
            for _, row in mprofile.iterrows():
                print(f"  {int(row['min_offset']):3d}  "
                    f"{row['mean']:+8.2f}%  "
                    f"{row['median']:+8.2f}%  "
                    f"{row['max']:+7.2f}%  "
                    f"{row['min']:+8.2f}%  "
                    f"{int(row['count']):5d}")

        # ── Save files ────────────────────────────────────────────────────
        os.makedirs("analysis", exist_ok=True)
        _s = BT_START.strftime("%Y%m%d")
        _e = BT_END.strftime("%Y%m%d")
        trades_path = f"analysis/btcusd_vol_short_{_s}_{_e}_trades.csv"
        trails_path = f"analysis/btcusd_vol_short_{_s}_{_e}_trails.csv"
        trades_bt_df.to_csv(trades_path, index=False)
        trail_df.to_csv(trails_path, index=False)
        print(f"\nTrades saved \u2192 {trades_path}")
        print(f"Trails saved \u2192 {trails_path}")

    if not skipped_bt_df.empty:
        print(f"\nSkip reasons:")
        print(skipped_bt_df["reason"].value_counts().to_string())

    print("\n" + "=" * 60)
    print("BACKTEST COMPLETE")
    print("=" * 60)

    '''
    Found 12 CSV files. Processing...
    Saving 525,600 rows to data/BTCUSD/spot/BTCUSDT_1m_combined.xlsx ...
    Saved.
    Dataset loaded: 525,600 candles  from 2024-12-01 05:30:00+05:30 to 2025-12-01 05:29:00+05:30
    ======================================================================
    BTCUSD – INTRADAY VOLATILITY EXPANSION ANALYSIS (24/7)
    ======================================================================
    Data Range   : 2024-12-01 05:30:00+05:30 → 2025-12-01 05:29:00+05:30
    Trading Days : 366

    Found 2591 intraday expansion windows (same-day only)

    ======================================================================
    MOST CONSISTENT INTRADAY WINDOWS (Top 10 by Frequency)
    ======================================================================

    Top 10 Most Consistent Windows (Occurred Most Often):
    ----------------------------------------------------------------------
    1. 05:15 → 06:00   | Freq:  42 days | Avg Exp:  165.2% | Duration:  45 min
    2. 18:15 → 19:00   | Freq:  37 days | Avg Exp:  290.3% | Duration:  45 min
    3. 02:45 → 03:30   | Freq:  32 days | Avg Exp:  180.4% | Duration:  45 min
    4. 17:15 → 18:00   | Freq:  31 days | Avg Exp:  288.4% | Duration:  45 min
    5. 16:15 → 17:00   | Freq:  23 days | Avg Exp:  134.5% | Duration:  45 min
    6. 00:45 → 01:30   | Freq:  23 days | Avg Exp:  127.9% | Duration:  45 min
    7. 13:15 → 14:00   | Freq:  23 days | Avg Exp:  119.0% | Duration:  45 min
    8. 18:30 → 19:15   | Freq:  21 days | Avg Exp:  200.7% | Duration:  45 min
    9. 12:45 → 13:30   | Freq:  20 days | Avg Exp:  119.5% | Duration:  45 min
    10. 11:15 → 12:00   | Freq:  19 days | Avg Exp:  308.1% | Duration:  45 min

    ======================================================================
    BEST ENTRY & EXIT TIMES BY HOUR (UTC)
    ======================================================================

    Best Entry Hours – Volatility Convergence (UTC):
    --------------------------------------------------
    02:00 UTC | Avg Expansion: 525.4% | Occurred: 120.0 times
    18:00 UTC | Avg Expansion: 261.4% | Occurred: 199.0 times
    17:00 UTC | Avg Expansion: 256.7% | Occurred: 130.0 times
    03:00 UTC | Avg Expansion: 207.2% | Occurred: 93.0 times
    20:00 UTC | Avg Expansion: 196.7% | Occurred: 96.0 times

    Best Exit Hours – Volatility Peak (UTC):
    --------------------------------------------------
    04:00 UTC | Avg Expansion: 580.2% | Occurred: 86.0 times
    19:00 UTC | Avg Expansion: 261.1% | Occurred: 215.0 times
    18:00 UTC | Avg Expansion: 253.2% | Occurred: 106.0 times
    03:00 UTC | Avg Expansion: 220.4% | Occurred: 132.0 times
    02:00 UTC | Avg Expansion: 211.8% | Occurred: 88.0 times

    ======================================================================
    RECOMMENDED TRADING WINDOWS
    ======================================================================
    No windows met the 20 % frequency threshold.
    Highest-frequency window: 05:15 → 06:00  (42/366 days = 11.5%)

    ======================================================================
    TRADING STRATEGY RECOMMENDATIONS
    ======================================================================

    PRIMARY STRATEGY: Trade the 05:15 → 06:00 window (UTC)
    Entry ~05:15 UTC  (volatility convergence)
    Exit  ~06:00 UTC  (volatility peak)
    Expected expansion : 165.2%
    Duration           : 45 min
    Reliability        : 42/366 days (11.5%)

    ALTERNATIVE STRATEGIES:
    2. 18:15 → 19:00   | Freq:  37 days | Avg Exp:  290.3% | Duration:  45 min
    3. 02:45 → 03:30   | Freq:  32 days | Avg Exp:  180.4% | Duration:  45 min
    4. 17:15 → 18:00   | Freq:  31 days | Avg Exp:  288.4% | Duration:  45 min

    RISK MANAGEMENT:
    • BTC is 24/7 – no forced session close, but respect your risk limits
    • Use ATR or rolling-vol for position sizing, not fixed lots
    • Set stops based on the entry volatility level (e.g. 1.5× entry vol)
    • Be extra cautious around macro events (FOMC, CPI, etc.)

    Results saved to 'analysis/btcusd_intraday_expansion_windows.csv'

    ======================================================================
    ANALYSIS COMPLETE
    ======================================================================

    ============================================================
    BTCUSD — VOLATILITY SHORT STRANGLE BACKTEST
    ============================================================
    Period        : 2024-12-01 → 2025-11-30
    Scan window   : 13:15:00 → 15:30:00 IST
    Forced exit   : 17:25:00 IST
    Lot size      : 0.1 contracts
    SL / TP       : 150% / 40% of premium
    Trading days  : 365
    Vol Short Backtest: 100%|██████████| 365/365 [09:26<00:00,  1.55s/it]
    Trades entered : 316
    Days skipped   : 49

    --- PERFORMANCE SUMMARY ---
    Win rate          : 63.0%
    Total P&L         : $1,048.94
    Avg P&L / trade   : $3.32
    Best trade        : $154.85
    Worst trade       : $-215.69
    Avg capital/trade : $44.29
    Avg combined prem : $442.91
    Final balance     : $2,548.94  (started $1,500.00)
    Total return      : 69.9%

    Exit reasons:
    exit_reason
    FORCED    316

    Entry time distribution (IST hour):
    signal_hour
    13    265
    14     39
    15     12

    Monthly P&L (wins / losses / net $ / win rate):
            trades  wins  losses  net_usd    avg_usd  win_rate
    month                                                      
    2024-12      28    11      17  -523.78 -18.706429      39.3
    2025-01      28    16      12   -98.44  -3.515714      57.1
    2025-02      23    17       6   485.78  21.120870      73.9
    2025-03      27    15      12  -153.70  -5.692593      55.6
    2025-04      24    14      10  -219.33  -9.138750      58.3
    2025-05      28    19       9   332.17  11.863214      67.9
    2025-06      26    16      10    34.66   1.333077      61.5
    2025-07      20    14       6   344.43  17.221500      70.0
    2025-08      30    22       8   180.10   6.003333      73.3
    2025-09      25    17       8   254.08  10.163200      68.0
    2025-10      30    16      14    58.06   1.935333      53.3
    2025-11      27    22       5   354.91  13.144815      81.5

    --- PEAK P&L DISTRIBUTION ---
    Avg peak     : +61.78%
    Median peak  : +59.87%
    Trades with peak > 0% : 93.4%
    Trades with peak > 10% : 88.6%
    Trades with peak > 20% : 80.1%
    Trades with peak > 30% : 74.4%
    Trades with peak > 40% : 65.2%

    --- MINUTE-BY-MINUTE P&L PROFILE ---
    Min    AvgPct    MedPct    Best%    Worst%      n
        1     +0.08%     +0.00%   +43.10%    -50.36%    129
        2     -0.78%     +0.00%   +35.69%    -76.75%    143
        3     -2.52%     +1.56%   +23.76%   -153.85%    147
        4     -2.49%     -0.18%   +57.95%    -70.00%    134
        5     -2.55%     +1.50%   +43.38%   -133.21%    159
        6     -3.21%     +1.83%   +52.98%   -147.14%    135
        7     -3.99%     +2.64%   +32.14%   -110.89%    143
        8     -5.44%     +1.66%   +33.93%   -231.32%    129
        9     -4.26%     +1.76%   +32.71%   -207.69%    142
    10     -5.60%     +2.85%   +47.17%   -206.70%    127
    11     -4.60%     +2.03%   +37.18%   -143.78%    134
    12     -4.06%     +2.00%   +48.01%   -155.64%    130
    13     -6.66%     +2.49%   +45.36%   -186.53%    121
    14     -4.22%     +3.04%   +42.31%   -188.81%    128
    15     -1.92%     +4.81%   +51.42%   -167.88%    136
    16     -4.19%     +5.08%   +43.55%   -343.09%    134
    17     -5.27%     +5.68%   +44.70%   -394.20%    133
    18     -5.38%     +2.38%   +45.32%   -306.40%    122
    19     -2.75%     +3.93%   +37.62%   -211.41%    130
    20     -0.67%     +8.11%   +47.08%   -130.91%    127
    21     -5.07%     +5.00%   +52.51%   -175.65%    126
    22     -1.84%     +4.35%   +52.37%   -135.85%    113
    23     -2.17%     +4.86%   +46.36%   -149.15%    112
    24     -4.61%     +7.13%   +46.03%   -264.69%    125
    25     -4.75%     +5.29%   +46.65%   -288.89%    127
    26     -4.87%     +3.25%   +49.45%   -234.91%    129
    27     -3.59%     +6.29%   +51.02%   -312.75%    117
    28     -9.16%     +4.41%   +50.88%   -288.34%    120
    29     -5.33%     +8.16%   +52.49%   -314.27%    133
    30     -7.90%     +5.71%   +54.84%   -320.94%    109
    31     -3.57%     +9.90%   +54.93%   -368.65%    124
    32     -4.22%     +7.50%   +51.58%   -268.87%    123
    33     -2.70%     +9.78%   +56.58%   -225.78%    120
    34     -1.12%     +8.96%   +58.48%   -190.00%    119
    35     -4.96%     +7.59%   +54.41%   -327.36%    124
    36     -0.35%    +10.09%   +51.57%   -246.23%    112
    37     -3.45%     +9.68%   +48.69%   -249.07%    121
    38     -0.11%    +11.96%   +58.34%   -226.40%    125
    39     +3.33%    +11.59%   +58.21%   -141.19%    112
    40     -2.63%    +10.74%   +58.59%   -192.86%    104
    41     +3.08%    +12.59%   +52.65%   -223.58%    113
    42     -3.76%    +12.94%   +52.80%   -459.90%    117
    43     +3.21%    +14.32%   +49.70%   -300.94%    124
    44     -1.53%    +11.55%   +55.45%   -200.92%    114
    45     -1.11%    +14.34%   +51.93%   -400.57%    117
    46     +5.89%    +17.88%   +59.02%   -178.07%    117
    47     +0.82%    +11.64%   +51.22%   -177.82%    113
    48     +3.95%    +16.62%   +54.84%   -194.43%    113
    49    +10.08%    +16.41%   +50.39%    -98.44%    124
    50     +1.35%    +12.70%   +52.32%   -291.04%    131
    51     +1.69%    +16.14%   +45.09%   -288.77%    131
    52     +3.67%    +15.82%   +55.63%   -263.49%    106
    53     +2.01%    +13.86%   +56.90%   -267.19%    116
    54     +5.17%    +15.63%   +51.98%   -304.91%    126
    55     +4.60%    +15.74%   +55.72%   -264.22%    132
    56     +3.58%    +16.88%   +54.97%   -363.20%    126
    57     +1.43%    +12.99%   +69.02%   -357.06%    109
    58     +5.01%    +17.99%   +61.62%   -259.91%    104
    59     +0.19%    +16.08%   +59.90%   -333.29%    112
    60     +8.17%    +20.02%   +62.12%   -196.70%    111
    61     +4.71%    +13.46%   +56.23%   -203.83%    105
    62     +7.57%    +17.73%   +62.29%   -156.83%    119
    63     +9.36%    +18.44%   +65.15%   -141.50%    121
    64     +1.90%    +14.89%   +62.63%   -267.92%    111
    65     +6.98%    +18.82%   +61.82%   -279.53%    126
    66     +7.72%    +20.58%   +58.25%   -230.24%    132
    67     +8.43%    +17.85%   +62.29%   -252.51%    125
    68     +9.87%    +20.84%   +61.52%   -158.00%    126
    69     +9.15%    +19.95%   +59.67%   -166.15%    131
    70     +4.20%    +18.62%   +62.83%   -237.76%    121
    71     +7.86%    +17.82%   +59.60%   -174.57%    131
    72    +11.23%    +24.35%   +63.93%   -249.30%    136
    73    +10.15%    +21.74%   +67.02%   -180.95%    117
    74     +8.06%    +21.99%   +64.79%   -306.08%    113
    75    +11.34%    +26.66%   +57.46%   -289.45%    115
    76     +2.26%    +24.00%   +72.38%   -392.26%    121
    77     +5.26%    +23.14%   +66.23%   -349.06%    123
    78    +12.11%    +25.80%   +72.93%   -279.43%    114
    79     +6.71%    +23.95%   +76.24%   -361.86%    107
    80     +3.98%    +25.54%   +67.62%   -463.59%    118
    81    +13.46%    +26.97%   +54.41%   -146.07%    120
    82     +7.85%    +27.59%   +80.66%   -328.15%    121
    83     +3.70%    +23.97%   +66.23%   -466.18%    121
    84     +0.92%    +23.59%   +82.87%   -445.65%    134
    85     +9.54%    +25.72%   +63.91%   -335.57%    128
    86     +4.54%    +22.84%   +82.32%   -353.43%    128
    87     +7.89%    +23.78%   +87.07%   -324.21%    120
    88    +12.94%    +22.92%   +87.85%   -208.93%    115
    89    +15.97%    +27.71%   +88.95%   -215.00%    125
    90    +12.09%    +25.26%   +88.95%   -346.96%    131
    91     +8.09%    +23.54%   +82.32%   -276.82%    128
    92     +2.97%    +25.06%   +82.87%   -404.91%    108
    93     +4.42%    +28.76%   +90.06%   -385.06%    119
    94     +8.75%    +25.24%   +83.43%   -262.11%    115
    95    +11.56%    +28.19%   +84.53%   -270.44%    140
    96     +6.10%    +25.99%   +77.78%   -293.52%    134
    97     -0.19%    +28.77%   +84.13%   -390.43%    121
    98    +11.02%    +24.79%   +84.13%   -227.90%    112
    99     +7.99%    +29.03%   +88.01%   -454.32%    123
    100     +9.03%    +27.49%   +87.94%   -328.67%    122
    101     +5.98%    +26.70%   +87.30%   -432.38%    121
    102     +7.91%    +29.72%   +90.11%   -429.66%    121
    103    +10.00%    +29.41%   +90.06%   -536.23%    118
    104     +3.48%    +30.62%   +94.03%   -516.93%    115
    105    +13.85%    +30.90%   +93.48%   -611.31%    117
    106     +5.33%    +30.70%   +92.93%   -535.78%    116
    107    +15.46%    +33.75%   +93.48%   -463.90%    119
    108     +5.90%    +33.14%   +94.03%   -531.81%    110
    109    +15.45%    +34.62%   +95.87%   -447.81%    112
    110    +14.51%    +31.56%   +96.76%   -572.48%    127
    111     +5.82%    +33.21%   +97.52%   -662.36%    131
    112    +17.14%    +36.11%   +97.71%   -853.24%    126
    113    +17.90%    +36.94%   +97.21%   -757.90%    122
    114    +19.75%    +37.46%   +98.16%   -330.00%    118
    115    +19.23%    +34.11%   +98.10%   -836.38%    128
    116    +13.07%    +35.98%   +98.34%   -892.86%    135
    117    +15.21%    +36.56%   +98.62%   -891.81%    125
    118    +17.36%    +35.41%   +98.29%   -884.86%    119
    119    +19.81%    +36.37%   +99.17%   -290.41%    120
    120    +24.82%    +37.60%   +98.67%   -277.80%    129
    121    +21.08%    +40.16%   +98.86%   -753.52%    124
    122    +22.54%    +39.73%   +99.49%   -707.09%    124
    123    +20.89%    +42.19%   +99.17%   -822.10%    116
    124    +18.83%    +41.81%   +98.40%   -823.90%    119
    125    +24.05%    +42.37%   +99.68%   -325.45%    131
    126    +15.63%    +37.03%   +98.54%   -734.77%    135
    127    +17.61%    +39.83%   +99.68%   -964.95%    136
    128    +19.74%    +39.55%   +99.61%   -303.90%    119
    129    +24.13%    +42.06%   +87.74%   -257.04%    123
    130    +18.86%    +37.95%   +99.61%   -297.26%    136
    131    +25.54%    +40.20%   +99.67%   -255.49%    130
    132    +12.76%    +41.89%   +99.45%  -1064.57%    122
    133    +30.04%    +41.88%   +99.72%   -199.27%    118
    134    +24.52%    +41.61%   +99.67%   -277.83%    119
    135    +16.00%    +40.52%   +99.23%   -700.55%    133
    136    +14.62%    +41.12%   +99.39%  -1144.86%    139
    137    +32.75%    +45.28%   +93.87%   -254.55%    119
    138    +32.30%    +48.38%   +99.39%   -389.11%    120
    139    +38.19%    +47.48%   +99.83%   -206.84%    110
    140    +30.66%    +46.05%   +99.45%   -323.74%    137
    141    +28.02%    +45.76%   +96.13%   -316.48%    131
    142    +28.45%    +47.64%   +94.97%   -405.00%    119
    143    +29.04%    +46.11%   +95.23%   -441.81%    138
    144    +33.52%    +49.48%   +97.35%   -449.51%    137
    145    +26.20%    +49.58%   +98.58%  -1092.19%    132
    146    +33.57%    +46.38%   +97.48%   -200.62%    146
    147    +34.72%    +46.58%   +98.26%   -443.46%    120
    148    +44.19%    +50.71%   +98.90%   -168.93%    116
    149    +26.14%    +51.47%   +98.84%  -1087.71%    116
    150    +37.81%    +52.51%   +98.90%   -225.97%    132
    151    +30.94%    +51.50%   +98.90%   -457.61%    136
    152    +32.64%    +52.43%   +99.23%  -1091.33%    131
    153    +39.71%    +53.74%   +99.28%   -164.81%    119
    154    +39.61%    +55.70%   +99.35%   -234.29%    130
    155    +42.68%    +53.35%   +99.43%   -154.06%    145
    156    +43.46%    +55.96%   +99.48%   -232.29%    134
    157    +46.65%    +56.39%   +99.78%   -285.93%    142
    158    +44.45%    +56.04%   +99.42%   -167.16%    128
    159    +28.62%    +55.93%   +99.87%   -403.16%    123
    160    +46.84%    +56.66%   +99.71%   -154.20%    137
    161    +45.71%    +57.80%   +99.44%   -239.74%    133
    162    +49.51%    +59.25%   +99.74%    -96.43%    126
    163    +46.39%    +60.88%   +99.91%   -145.13%    118
    164    +44.99%    +61.01%   +99.91%   -212.98%    107
    165    +47.03%    +60.23%   +99.91%   -233.49%    127
    166    +49.20%    +61.70%   +99.92%   -249.37%    117
    167    +42.06%    +59.90%   +99.91%   -250.19%    131
    168    +52.52%    +61.41%   +99.88%   -427.81%    123
    169    +52.02%    +62.97%   +99.92%   -146.10%    133
    170    +49.75%    +62.34%   +99.84%   -230.14%    130
    171    +40.44%    +61.24%   +99.89%   -247.04%    137
    172    +47.30%    +62.14%   +99.40%   -478.05%    121
    173    +45.27%    +60.00%   +99.84%   -277.78%    108
    174    +48.03%    +61.76%   +97.49%   -285.52%    125
    175    +43.99%    +61.39%   +99.58%   -374.05%    134
    176    +43.43%    +65.08%   +99.90%   -316.17%    122
    177    +50.45%    +66.03%   +99.86%   -261.27%    128
    178    +48.61%    +63.63%   +98.74%   -287.82%    125
    179    +54.99%    +66.22%   +99.75%   -139.25%    130
    180    +51.22%    +64.34%   +99.86%   -335.62%    142
    181    +57.00%    +65.90%   +98.58%   -289.36%    121
    182    +45.96%    +65.56%   +99.45%   -407.18%    131
    183    +57.50%    +68.50%   +99.76%    -92.38%    127
    184    +57.06%    +68.51%   +99.62%   -241.31%    120
    185    +52.55%    +65.93%   +99.67%   -325.95%    141
    186    +49.93%    +67.63%   +99.83%   -305.88%    116
    187    +56.91%    +69.62%   +99.83%   -147.83%    133
    188    +55.07%    +66.32%   +99.83%   -112.41%    128
    189    +53.53%    +67.51%   +99.83%   -143.45%    137
    190    +56.05%    +70.96%   +99.29%   -296.55%    135
    191    +56.06%    +69.25%   +99.13%   -540.51%    131
    192    +55.68%    +69.34%   +99.88%   -158.34%    116
    193    +58.89%    +72.38%   +99.76%   -591.44%    122
    194    +54.52%    +75.41%   +99.93%   -592.60%    117
    195    +65.55%    +72.19%   +99.86%    -88.21%    128
    196    +54.24%    +74.58%   +99.67%   -627.02%    129
    197    +57.69%    +74.64%   +99.95%   -374.79%    135
    198    +51.26%    +72.93%   +99.93%   -634.79%    134
    199    +59.39%    +76.05%   +99.93%   -271.63%    132
    200    +59.28%    +73.62%   +99.95%   -165.52%    143
    201    +61.03%    +75.15%   +99.68%   -134.31%    134
    202    +56.75%    +74.74%   +99.82%   -288.46%    129
    203    +56.78%    +75.59%   +99.78%   -194.25%    136
    204    +69.75%    +79.09%   +99.73%    -67.62%    120
    205    +62.80%    +77.27%   +99.89%   -107.40%    133
    206    +62.18%    +75.30%   +99.73%   -160.12%    135
    207    +67.31%    +79.04%   +99.93%   -157.18%    123
    208    +66.47%    +78.49%   +99.92%   -261.67%    133
    209    +69.72%    +77.88%   +99.86%   -163.93%    119
    210    +61.30%    +81.53%   +99.88%   -160.08%    126
    211    +65.09%    +79.36%   +99.90%   -109.57%    132
    212    +67.89%    +84.65%   +99.91%   -252.01%    119
    213    +67.42%    +82.55%   +99.92%    -76.96%    117
    214    +70.06%    +85.19%   +99.85%   -124.13%    116
    215    +62.56%    +77.40%   +99.92%   -203.88%    130
    216    +62.24%    +79.67%   +99.90%   -153.93%    122
    217    +71.78%    +82.84%   +99.93%   -112.99%    115
    218    +65.84%    +83.19%   +99.88%   -288.94%    116
    219    +69.43%    +82.20%   +99.93%    -90.67%    114
    220    +59.36%    +83.05%   +99.90%   -380.85%    120
    221    +70.38%    +83.65%   +99.90%   -174.44%     96
    222    +66.10%    +87.19%   +99.89%   -203.16%    111
    223    +70.62%    +86.72%   +99.93%   -160.25%    101
    224    +64.98%    +87.45%   +99.93%   -292.54%    100
    225    +66.39%    +87.72%   +99.93%   -304.84%     90
    226    +68.27%    +88.46%   +99.90%   -218.33%     93
    227    +69.59%    +90.11%   +99.93%   -190.63%     88
    228    +60.93%    +90.13%   +99.96%   -568.65%     93
    229    +63.31%    +91.50%   +99.93%   -236.13%    101
    230    +55.06%    +87.10%   +99.94%   -294.79%    105
    231    +66.32%    +88.87%   +99.93%   -175.84%     83
    232    +69.30%    +90.01%   +99.89%   -132.54%     79
    233    +68.94%    +94.43%   +99.91%   -251.46%     71
    234    +66.61%    +87.54%   +99.93%    -86.03%     76
    235    +67.77%    +92.77%   +99.96%   -154.17%     84
    236    +61.53%    +88.00%   +99.87%   -254.32%     54
    237    +64.41%    +89.50%   +99.91%   -152.71%     52
    238    +67.05%    +88.58%   +99.93%    -96.96%     56
    239    +74.03%    +96.84%   +99.96%    -37.52%     50
    240    +42.10%    +80.28%   +99.96%   -421.01%     64
    241    +34.69%    +96.43%   +99.94%   -441.08%     13
    242    -94.40%    -77.61%   +99.88%   -320.02%      7
    243     -9.20%    +13.49%   +73.24%   -217.52%     12
    244    -47.30%    -38.36%    -1.94%   -104.28%      5

    Trades saved → analysis/btcusd_vol_short_20241201_20251130_trades.csv
    Trails saved → analysis/btcusd_vol_short_20241201_20251130_trails.csv

    Skip reasons:
    reason
    no_vol_signal    47
    no_entry_ltp      1
    no_options        1

    ============================================================
    BACKTEST COMPLETE
    ============================================================
    '''