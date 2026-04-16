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
                atm_strike    = spot_price   # actual spot at signal candle close                                                                                                                           
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
    oading combined data from cache: data/BTCUSD/spot/BTCUSDT_1m_combined.xlsx
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

     
    Important
    Figures are displayed in the Plots pane by default. To make them also appear inline in the console, you need to uncheck "Mute inline plotting" under the options menu of Plots.
     
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
    SL / TP       : 80% / 99900% of premium
    Trading days  : 365
    Vol Short Backtest: 100%|██████████| 365/365 [09:42<00:00,  1.60s/it]
    Trades entered : 316
    Days skipped   : 49

    --- PERFORMANCE SUMMARY ---
    Win rate          : 56.6%
    Total P&L         : $1,787.94
    Avg P&L / trade   : $5.66
    Best trade        : $154.85
    Worst trade       : $-87.21
    Avg capital/trade : $44.29
    Avg combined prem : $442.91
    Final balance     : $3,287.94  (started $1,500.00)
    Total return      : 119.2%

    Exit reasons:
    exit_reason
    FORCED          188
    SL               73
    PREM_REBUILD     55

    Entry time distribution (IST hour):
    signal_hour
    13    265
    14     39
    15     12

    Monthly P&L (wins / losses / net $ / win rate):
             trades  wins  losses  net_usd    avg_usd  win_rate
    month                                                      
    2024-12      28    10      18  -155.87  -5.566786      35.7
    2025-01      28    15      13   110.39   3.942500      53.6
    2025-02      23    14       9   358.98  15.607826      60.9
    2025-03      27    15      12    53.14   1.968148      55.6
    2025-04      24    13      11   -27.18  -1.132500      54.2
    2025-05      28    17      11   243.06   8.680714      60.7
    2025-06      26    15      11   265.18  10.199231      57.7
    2025-07      20    13       7   308.07  15.403500      65.0
    2025-08      30    20      10   227.02   7.567333      66.7
    2025-09      25    16       9   235.92   9.436800      64.0
    2025-10      30    13      17  -170.71  -5.690333      43.3
    2025-11      27    18       9   339.94  12.590370      66.7

    --- PEAK P&L DISTRIBUTION ---
      Avg peak     : +56.01%
      Median peak  : +51.04%
      Trades with peak > 0% : 90.8%
      Trades with peak > 10% : 83.9%
      Trades with peak > 20% : 75.0%
      Trades with peak > 30% : 68.7%
      Trades with peak > 40% : 58.2%

    --- MINUTE-BY-MINUTE P&L PROFILE ---
     Min    AvgPct    MedPct    Best%    Worst%      n
        1     +0.08%     +0.00%   +43.10%    -50.36%    129
        2     -0.78%     +0.00%   +35.69%    -76.75%    143
        3     -2.52%     +1.56%   +23.76%   -153.85%    147
        4     -1.99%     -0.17%   +57.95%    -68.34%    133
        5     -2.15%     +1.53%   +43.38%   -133.21%    158
        6     -1.27%     +2.09%   +52.98%    -88.42%    132
        7     -1.98%     +2.75%   +32.14%   -104.40%    139
        8     -2.00%     +2.37%   +33.93%    -91.75%    125
        9     -0.66%     +3.34%   +32.71%    -65.10%    136
       10     -2.08%     +3.15%   +47.17%   -103.63%    123
       11     -0.98%     +2.97%   +37.18%    -56.75%    128
       12     -1.15%     +2.76%   +48.01%    -96.58%    125
       13     +0.14%     +3.08%   +45.36%    -78.57%    114
       14     +0.07%     +3.44%   +42.31%    -71.70%    123
       15     +2.55%     +5.16%   +51.42%    -80.19%    129
       16     +2.50%     +5.51%   +43.55%    -67.53%    126
       17     +2.37%     +6.62%   +44.70%    -71.65%    124
       18     +0.66%     +3.74%   +45.32%    -92.21%    114
       19     +2.32%     +6.17%   +37.62%    -61.56%    121
       20     +2.36%     +8.39%   +47.08%    -88.24%    119
       21     +0.98%     +7.54%   +52.51%   -111.95%    114
       22     +3.42%     +6.63%   +52.37%    -86.57%    104
       23     +4.27%     +7.52%   +46.36%    -67.54%    103
       24     +4.66%     +9.20%   +46.03%    -94.81%    114
       25     +1.69%     +8.28%   +46.65%    -79.42%    118
       26     +3.51%     +6.33%   +49.45%    -65.51%    115
       27     +3.33%     +7.97%   +51.02%    -95.36%    107
       28     +2.34%     +7.70%   +50.88%   -145.34%    108
       29     +8.01%    +10.53%   +52.49%    -72.62%    113
       30     +4.97%     +9.43%   +54.84%    -81.75%     95
       31     +7.75%    +13.09%   +54.93%    -78.19%    110
       32     +5.59%    +10.14%   +51.58%    -63.03%    112
       33     +7.06%    +11.77%   +56.58%    -67.39%    110
       34     +7.11%    +12.29%   +58.48%    -82.61%    107
       35     +6.45%    +10.46%   +54.41%    -52.41%    110
       36    +11.20%    +14.33%   +51.57%    -51.99%     97
       37     +9.91%    +13.21%   +48.69%    -76.72%    108
       38    +11.80%    +15.04%   +58.34%    -76.83%    109
       39    +10.43%    +12.68%   +58.21%    -69.69%    103
       40    +10.24%    +12.70%   +58.59%   -106.77%     93
       41    +10.29%    +13.80%   +52.65%    -43.91%    105
       42    +12.65%    +14.89%   +52.80%    -60.14%    103
       43    +12.62%    +16.92%   +49.70%    -68.70%    110
       44     +8.70%    +14.73%   +55.45%    -69.92%    102
       45    +12.59%    +17.53%   +51.93%    -98.42%    105
       46    +14.44%    +18.57%   +59.02%    -26.81%    105
       47    +10.91%    +15.62%   +51.22%    -64.79%     97
       48    +12.27%    +17.91%   +54.84%    -75.17%    102
       49    +12.87%    +18.06%   +50.39%    -81.78%    117
       50    +12.35%    +14.02%   +52.32%   -140.14%    119
       51    +13.05%    +17.53%   +45.09%    -56.21%    119
       52    +13.71%    +17.17%   +55.63%    -52.03%     97
       53    +13.74%    +14.99%   +56.90%    -50.00%    105
       54    +14.61%    +17.32%   +51.98%    -58.29%    113
       55    +13.20%    +17.11%   +55.72%    -53.14%    120
       56    +15.58%    +18.49%   +54.97%    -47.40%    112
       57    +14.73%    +16.39%   +69.02%    -45.36%     96
       58    +15.35%    +20.34%   +61.62%    -72.44%     92
       59    +17.06%    +19.71%   +59.90%    -60.19%     99
       60    +18.71%    +22.58%   +62.12%    -42.09%     99
       61    +14.95%    +18.31%   +56.23%    -58.42%     95
       62    +15.85%    +21.14%   +62.29%    -67.05%    108
       63    +13.85%    +19.33%   +65.15%    -63.86%    114
       64    +12.39%    +18.21%   +62.63%    -89.88%    100
       65    +17.76%    +22.56%   +61.82%    -89.90%    112
       66    +17.52%    +22.37%   +58.25%    -91.54%    118
       67    +15.19%    +21.79%   +62.29%    -71.81%    113
       68    +18.81%    +23.32%   +61.52%    -59.66%    111
       69    +17.69%    +22.94%   +59.67%    -57.22%    116
       70    +18.97%    +23.33%   +62.83%    -49.92%    100
       71    +15.82%    +20.80%   +59.60%    -70.10%    112
       72    +20.46%    +26.51%   +63.93%    -59.11%    118
       73    +19.27%    +23.20%   +67.02%    -56.44%     98
       74    +20.37%    +25.27%   +64.79%    -52.71%     99
       75    +22.19%    +28.77%   +57.46%    -70.48%     98
       76    +22.80%    +27.27%   +72.38%    -80.15%     97
       77    +18.95%    +25.57%   +66.23%    -96.53%    108
       78    +22.51%    +28.31%   +72.93%    -78.89%    102
       79    +21.96%    +28.70%   +76.24%    -84.66%     89
       80    +19.32%    +29.68%   +67.62%    -89.24%    105
       81    +23.50%    +29.55%   +54.41%   -127.78%    105
       82    +21.93%    +30.56%   +80.66%    -78.63%    104
       83    +21.50%    +29.65%   +61.90%    -93.50%     97
       84    +22.45%    +27.92%   +82.87%    -69.73%    111
       85    +22.27%    +28.77%   +63.91%    -70.17%    110
       86    +21.10%    +26.88%   +82.32%    -72.51%    109
       87    +25.19%    +28.77%   +87.07%    -77.56%     99
       88    +20.91%    +24.38%   +87.85%    -93.92%    100
       89    +25.14%    +29.23%   +88.95%   -174.48%    109
       90    +24.10%    +28.08%   +88.95%    -76.24%    112
       91    +21.28%    +25.61%   +82.32%    -86.91%    110
       92    +24.63%    +27.91%   +82.87%    -70.15%     86
       93    +23.19%    +30.88%   +90.06%    -86.10%    103
       94    +23.37%    +29.88%   +83.43%    -55.35%    102
       95    +23.79%    +29.81%   +84.53%   -121.13%    124
       96    +25.49%    +29.77%   +77.78%   -121.33%    111
       97    +25.75%    +31.25%   +84.13%    -61.82%    101
       98    +24.83%    +27.38%   +84.13%    -77.14%     94
       99    +25.38%    +31.69%   +88.01%    -98.26%    107
      100    +30.11%    +33.10%   +87.94%    -52.90%    102
      101    +24.80%    +29.39%   +87.30%    -79.83%    107
      102    +27.79%    +34.30%   +90.11%   -121.91%    101
      103    +29.43%    +34.39%   +90.06%    -94.10%     97
      104    +32.01%    +34.67%   +94.03%    -33.62%     88
      105    +32.34%    +33.47%   +93.48%    -41.59%    101
      106    +29.51%    +32.69%   +92.93%    -73.64%    100
      107    +32.35%    +36.11%   +93.48%    -57.96%    104
      108    +29.50%    +35.67%   +94.03%    -57.83%     90
      109    +32.72%    +36.59%   +95.87%    -29.88%     94
      110    +31.11%    +33.81%   +96.76%    -35.07%    104
      111    +28.79%    +34.80%   +97.52%    -72.57%    110
      112    +33.65%    +39.07%   +97.71%    -88.76%    111
      113    +34.20%    +41.88%   +97.21%    -53.43%    102
      114    +33.52%    +39.31%   +98.16%    -95.13%    101
      115    +35.92%    +38.46%   +98.10%    -36.03%    105
      116    +31.47%    +39.01%   +98.34%    -65.10%    112
      117    +36.43%    +41.51%   +98.62%    -46.29%    101
      118    +33.84%    +37.89%   +98.29%    -39.82%    101
      119    +33.69%    +39.43%   +99.17%    -50.86%    101
      120    +35.39%    +41.74%   +98.67%    -47.35%    109
      121    +35.63%    +41.52%   +98.86%   -107.79%    104
      122    +35.91%    +42.29%   +99.49%    -67.46%    105
      123    +39.97%    +44.68%   +99.17%    -62.84%     97
      124    +37.69%    +43.99%   +98.40%    -53.02%    104
      125    +40.12%    +43.35%   +99.68%    -49.14%    111
      126    +35.89%    +40.70%   +98.54%    -87.87%    112
      127    +37.05%    +42.73%   +99.68%   -101.81%    114
      128    +38.04%    +42.18%   +99.61%   -130.23%     95
      129    +39.61%    +43.65%   +87.74%    -61.33%     99
      130    +36.32%    +43.04%   +99.61%    -63.42%    106
      131    +39.81%    +42.43%   +99.67%    -36.26%    105
      132    +41.39%    +44.75%   +99.45%    -41.84%     97
      133    +40.50%    +42.78%   +99.72%    -33.37%     96
      134    +39.86%    +44.19%   +99.67%    -55.22%    101
      135    +40.26%    +44.69%   +99.23%    -74.37%    104
      136    +39.58%    +44.96%   +99.39%    -75.27%    114
      137    +45.22%    +48.59%   +93.87%    -26.47%     98
      138    +48.41%    +50.35%   +99.39%    -43.03%     99
      139    +45.18%    +49.16%   +99.83%    -43.51%     99
      140    +44.74%    +50.27%   +99.45%    -61.75%    111
      141    +40.32%    +47.68%   +96.13%    -80.73%    111
      142    +44.72%    +49.65%   +94.97%    -56.56%     98
      143    +45.17%    +51.55%   +95.23%    -23.45%    112
      144    +45.36%    +51.61%   +97.35%    -67.36%    116
      145    +47.24%    +50.85%   +98.58%    -50.08%    106
      146    +39.72%    +51.08%   +97.48%    -84.33%    125
      147    +43.77%    +49.28%   +98.26%   -141.12%    100
      148    +48.89%    +51.29%   +98.90%    -66.58%     99
      149    +50.81%    +53.25%   +98.84%    -55.86%     97
      150    +51.16%    +55.35%   +98.90%    -75.55%    107
      151    +49.91%    +54.61%   +98.90%   -117.43%    109
      152    +50.37%    +54.31%   +99.23%    -66.04%    110
      153    +51.58%    +54.95%   +99.28%    -64.41%     99
      154    +52.50%    +58.30%   +99.35%    -66.56%    104
      155    +51.29%    +56.52%   +99.43%    -64.59%    123
      156    +51.49%    +58.56%   +99.48%    -69.70%    113
      157    +54.08%    +58.33%   +99.78%    -70.93%    117
      158    +52.51%    +58.07%   +99.42%    -46.23%    102
      159    +50.64%    +59.39%   +99.87%    -84.91%     98
      160    +55.41%    +58.70%   +99.71%    -52.17%    111
      161    +54.21%    +59.25%   +99.44%    -61.84%    110
      162    +57.18%    +61.15%   +99.74%    -45.73%    101
      163    +53.50%    +62.30%   +99.91%    -55.90%     98
      164    +56.06%    +63.24%   +99.91%    -58.03%     85
      165    +56.15%    +63.30%   +99.91%   -104.10%    107
      166    +57.26%    +62.64%   +99.92%    -58.53%     95
      167    +57.15%    +62.96%   +99.91%    -62.30%    102
      168    +60.29%    +61.99%   +99.88%    -32.23%    103
      169    +57.84%    +63.97%   +99.92%    -66.89%    115
      170    +55.08%    +63.89%   +99.62%    -58.15%    106
      171    +55.93%    +62.86%   +99.27%    -66.23%    105
      172    +58.71%    +63.79%   +98.72%    -48.77%     98
      173    +56.13%    +60.52%   +99.65%    -35.38%     88
      174    +58.52%    +63.88%   +97.49%    -86.53%     98
      175    +59.33%    +64.96%   +99.58%    -29.13%    101
      176    +57.82%    +66.21%   +99.90%    -68.83%     98
      177    +58.62%    +67.79%   +99.86%    -91.11%    102
      178    +59.39%    +66.78%   +98.74%    -71.87%     99
      179    +63.32%    +69.17%   +99.75%    -56.14%    105
      180    +61.95%    +67.49%   +99.86%    -68.66%    113
      181    +63.54%    +70.74%   +98.58%    -18.57%     98
      182    +58.33%    +67.70%   +99.45%    -82.25%    107
      183    +65.13%    +70.57%   +99.76%    -27.97%    104
      184    +64.41%    +70.48%   +99.62%    -17.40%     98
      185    +59.17%    +68.48%   +99.67%    -68.26%    116
      186    +57.19%    +67.91%   +99.83%    -92.49%     98
      187    +63.96%    +71.32%   +99.83%    -50.39%    107
      188    +60.06%    +68.87%   +99.83%    -69.29%    109
      189    +62.49%    +70.61%   +99.83%    -77.87%    108
      190    +61.02%    +73.05%   +99.29%    -66.22%    114
      191    +64.03%    +73.09%   +99.13%    -47.53%    106
      192    +64.47%    +73.68%   +99.88%    -22.65%     89
      193    +66.98%    +73.58%   +99.76%    -28.70%     98
      194    +67.16%    +76.98%   +99.93%    -58.07%     92
      195    +69.31%    +75.58%   +99.86%     -5.41%    103
      196    +67.15%    +75.97%   +99.67%    -78.21%    106
      197    +67.51%    +76.15%   +99.95%    -89.49%    111
      198    +66.47%    +76.10%   +99.93%    -64.43%    105
      199    +71.19%    +78.19%   +99.93%    -27.28%    102
      200    +67.64%    +77.81%   +99.95%    -63.34%    111
      201    +66.49%    +76.37%   +99.63%    -78.91%    105
      202    +66.85%    +74.96%   +99.40%    -16.60%    102
      203    +68.24%    +77.80%   +99.71%    -61.67%    108
      204    +72.38%    +80.11%   +99.73%    -28.27%    103
      205    +69.81%    +79.50%   +99.82%    -74.70%    106
      206    +68.87%    +76.14%   +99.73%    -36.76%    108
      207    +73.77%    +79.19%   +99.76%    -25.94%    100
      208    +73.33%    +80.84%   +99.92%    -25.89%    108
      209    +72.52%    +77.64%   +99.66%    -66.92%     96
      210    +71.44%    +82.71%   +99.81%    -91.97%    101
      211    +69.77%    +79.52%   +99.90%    -48.62%    107
      212    +75.85%    +84.82%   +99.91%    -44.85%     96
      213    +70.59%    +83.29%   +99.92%    -76.96%     95
      214    +72.37%    +85.19%   +99.75%    -96.08%     94
      215    +69.84%    +78.12%   +99.92%    -75.55%    103
      216    +71.07%    +84.06%   +99.90%    -77.50%     96
      217    +74.42%    +84.81%   +99.93%    -23.33%     94
      218    +76.87%    +84.96%   +99.88%    -37.10%     89
      219    +72.65%    +85.90%   +99.93%    -90.67%     90
      220    +72.26%    +86.79%   +99.90%    -59.19%     90
      221    +80.28%    +88.06%   +99.90%     +6.76%     71
      222    +72.34%    +88.62%   +99.84%    -51.01%     88
      223    +73.88%    +88.84%   +99.93%   -105.20%     77
      224    +78.95%    +90.91%   +99.87%    -17.63%     73
      225    +77.55%    +87.94%   +99.93%    -34.30%     68
      226    +77.97%    +90.80%   +99.90%    -70.76%     71
      227    +79.59%    +91.93%   +99.93%    -42.43%     68
      228    +75.49%    +92.66%   +99.93%    -64.35%     69
      229    +73.47%    +92.43%   +99.88%    -96.96%     77
      230    +75.52%    +92.84%   +99.94%    -33.30%     74
      231    +75.91%    +94.55%   +99.93%    -30.90%     63
      232    +78.64%    +95.88%   +99.89%    -37.68%     56
      233    +74.11%    +97.65%   +99.91%    -71.09%     58
      234    +75.25%    +95.72%   +99.93%    -57.53%     53
      235    +78.96%    +98.86%   +99.96%    -48.33%     61
      236    +75.30%    +97.47%   +99.82%    -81.69%     37
      237    +81.82%    +99.11%   +99.91%     +6.12%     33
      238    +72.81%    +97.72%   +99.93%     -3.81%     38
      239    +77.15%    +98.57%   +99.96%    -32.89%     37
      240    +70.35%    +91.19%   +99.96%    -18.19%     40
      241    +83.46%    +99.77%   +99.94%     +6.80%      9
      242    +11.13%    +11.13%   +99.88%    -77.61%      2
      243    +27.47%    +28.82%   +73.24%    -30.86%      8
      244     -1.94%     -1.94%    -1.94%     -1.94%      1

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