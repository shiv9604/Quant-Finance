#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 05:54:27 2026

@author: shivprasadkounsalye
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==============================
# CONFIG
# ==============================
EXCEL_FILE = "MREA-MFT/MREA-MFT-Robust-V1.xlsx"
SHEET_NAME = "Consolidated Trades"
START_CAPITAL = 100000

print("Working directory:", os.getcwd())

# ==============================
# LOAD DATA
# ==============================
df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
print("Columns found:", df.columns.tolist())

# ==============================
# CLEAN & STANDARDIZE DATA
# ==============================

# 1. Rename columns to stable names
df = df.rename(columns={
    "Time": "datetime",
    "Profit": "pnl",
    "Symbol": "symbol",
    "Type": "type"
})

# 2. Drop balance rows (non-trade rows)
df = df[df["type"].str.lower() != "balance"]

# 3. Convert datetime
df["datetime"] = pd.to_datetime(df["datetime"], format="%Y.%m.%d %H:%M:%S")

# 4. Clean PnL (remove spaces like '100 000.00')
df["pnl"] = (
    df["pnl"]
    .astype(str)
    .str.replace(" ", "", regex=False)
    .astype(float)
)

# 5. Sort chronologically
df = df.sort_values("datetime").reset_index(drop=True)

print("✅ Data cleaned successfully")
print("Total trades:", len(df))
print("Date range:", df["datetime"].min(), "→", df["datetime"].max())

# ==============================
# TRADE-LEVEL EQUITY CURVE
# ==============================
df["cum_pnl"] = df["pnl"].cumsum()
df["equity"] = START_CAPITAL + df["cum_pnl"]

# ==============================
# PLOT PORTFOLIO EQUITY CURVE
# ==============================
plt.figure(figsize=(12,5))
plt.plot(df["datetime"], df["equity"], linewidth=2)
plt.title("Kosashi Capital – Portfolio Equity Curve (Trade-Level)")
plt.xlabel("Time")
plt.ylabel("Equity")
plt.grid(True)
plt.tight_layout()
plt.show()

# ==============================
# DAILY NAV (INDUSTRY STANDARD)
# ==============================
df["date"] = df["datetime"].dt.date

daily = (
    df.groupby("date")["pnl"]
    .sum()
    .reset_index()
)

daily["equity"] = START_CAPITAL + daily["pnl"].cumsum()
daily["returns"] = daily["equity"].pct_change().fillna(0)

# ==============================
# PORTFOLIO METRICS
# ==============================
total_trades = len(df)
trading_days = len(daily)

win_rate = (df["pnl"] > 0).mean()

gross_profit = df.loc[df["pnl"] > 0, "pnl"].sum()
gross_loss = abs(df.loc[df["pnl"] < 0, "pnl"].sum())
profit_factor = gross_profit / gross_loss if gross_loss != 0 else np.nan

# CAGR
years = (pd.to_datetime(daily["date"].iloc[-1]) -
         pd.to_datetime(daily["date"].iloc[0])).days / 365.25

final_equity = daily["equity"].iloc[-1]
cagr = (final_equity / START_CAPITAL) ** (1 / years) - 1

# Drawdown
daily["peak"] = daily["equity"].cummax()
daily["drawdown"] = (daily["equity"] - daily["peak"]) / daily["peak"]
max_dd = daily["drawdown"].min()

# Sharpe & Sortino (Daily NAV)
mean_ret = daily["returns"].mean()
std_ret = daily["returns"].std()
sharpe = (mean_ret / std_ret) * np.sqrt(252) if std_ret != 0 else np.nan

downside_std = daily.loc[daily["returns"] < 0, "returns"].std()
sortino = (mean_ret / downside_std) * np.sqrt(252) if downside_std != 0 else np.nan

# ==============================
# METRICS TABLE (PRESENTATION READY)
# ==============================
metrics = pd.DataFrame({
    "Performance Metric": [
        "Initial Capital",
        "Final Equity",
        "Gain",
        "CAGR",
        "Profit Factor",
        "Win Rate",
        "Max Drawdown",
        "Total Trades",
        "Trading Days",
        "Sharpe Ratio (Daily NAV)",
        "Sortino Ratio (Daily NAV)"
    ],
    "Value": [
        START_CAPITAL,
        round(final_equity, 2),
        f"{((final_equity / START_CAPITAL) - 1) * 100:.2f}%",
        f"{cagr * 100:.2f}%",
        round(profit_factor, 2),
        f"{win_rate * 100:.2f}%",
        f"{max_dd * 100:.2f}%",
        total_trades,
        trading_days,
        round(sharpe, 2),
        round(sortino, 2)
    ]
})

print("\nMREA – PORTFOLIO METRICS\n")
print(metrics.to_string(index=False))


# ==============================
# SYMBOL-LEVEL ANALYSIS
# ==============================

print("\n==============================")
print("SYMBOL CONTRIBUTION ANALYSIS")
print("==============================")

# 1️⃣ Per-symbol PnL summary
symbol_summary = (
    df.groupby("symbol")["pnl"]
    .agg(["sum", "count"])
    .rename(columns={"sum": "total_pnl", "count": "trades"})
)

symbol_summary["avg_pnl"] = symbol_summary["total_pnl"] / symbol_summary["trades"]

# Profit factor per symbol
def symbol_pf(x):
    gp = x[x > 0].sum()
    gl = abs(x[x < 0].sum())
    return gp / gl if gl != 0 else np.nan

symbol_pf_series = df.groupby("symbol")["pnl"].apply(symbol_pf)
symbol_summary["profit_factor"] = symbol_pf_series

symbol_summary = symbol_summary.sort_values("total_pnl", ascending=False)

print(symbol_summary)


# ==============================
# 2️⃣ DRAWdown Contribution (Who hurts portfolio most?)
# ==============================

print("\n==============================")
print("DRAWDOWN IMPACT ANALYSIS")
print("==============================")

# Tag portfolio drawdown periods
daily["in_drawdown"] = daily["drawdown"] < 0

# Merge back daily drawdown flag
df = df.merge(daily[["date", "in_drawdown"]], on="date", how="left")

# Sum losses during portfolio drawdown periods
dd_impact = (
    df[df["in_drawdown"]]
    .groupby("symbol")["pnl"]
    .sum()
    .sort_values()
)

print("\nSymbols contributing MOST to drawdowns:")
print(dd_impact.head(10))


# ==============================
# 3️⃣ CORRELATION MATRIX (Hedging / Offset Detection)
# ==============================

print("\n==============================")
print("SYMBOL CORRELATION ANALYSIS")
print("==============================")

# Create daily pnl per symbol
daily_symbol = (
    df.groupby(["date", "symbol"])["pnl"]
    .sum()
    .unstack()
    .fillna(0)
)

correlation_matrix = daily_symbol.corr()

print("\nCorrelation Matrix (Daily PnL):")
print(correlation_matrix.round(2))

# ==========================================================
# PROFESSIONAL SYMBOL CONTRIBUTION & LOT SIZE RECOMMENDER
# ==========================================================

print("\n==================================================")
print("SYMBOL CONTRIBUTION & CAPITAL ALLOCATION ANALYSIS")
print("==================================================")

# 1️⃣ SYMBOL TOTAL CONTRIBUTION
symbol_stats = df.groupby("symbol")["pnl"].agg(
    total_pnl="sum",
    avg_pnl="mean",
    trades="count"
)

# Profit factor per symbol
def compute_pf(x):
    gross_profit = x[x > 0].sum()
    gross_loss = abs(x[x < 0].sum())
    return gross_profit / gross_loss if gross_loss != 0 else np.nan

symbol_stats["profit_factor"] = df.groupby("symbol")["pnl"].apply(compute_pf)

# 2️⃣ VOLATILITY (Risk) PER SYMBOL
symbol_stats["pnl_std"] = df.groupby("symbol")["pnl"].std()

# 3️⃣ RISK-EFFICIENCY SCORE (Institutional Style)
symbol_stats["risk_efficiency"] = (
    symbol_stats["total_pnl"] / symbol_stats["pnl_std"]
)

# 4️⃣ DRAWdown CONTRIBUTION
daily["in_dd"] = daily["drawdown"] < 0
df = df.merge(daily[["date", "in_dd"]], on="date", how="left")

dd_contribution = (
    df[df["in_dd"]]
    .groupby("symbol")["pnl"]
    .sum()
)

symbol_stats["drawdown_contribution"] = dd_contribution
symbol_stats["drawdown_contribution"] = symbol_stats["drawdown_contribution"].fillna(0)

# 5️⃣ NORMALISE SCORES
symbol_stats["alpha_score"] = (
    symbol_stats["risk_efficiency"] *
    symbol_stats["profit_factor"]
)

# ==========================================================
# INSTITUTIONAL SYMBOL RISK & ALLOCATION ANALYSIS
# ==========================================================

print("\n==================================================")
print("ADVANCED SYMBOL ALLOCATION ANALYSIS (DD FOCUSED)")
print("==================================================")

symbol_metrics = []

for sym in df["symbol"].unique():
    
    sym_df = df[df["symbol"] == sym].copy()
    sym_df["cum"] = sym_df["pnl"].cumsum()
    sym_df["equity"] = START_CAPITAL + sym_df["cum"]
    
    # --- Symbol Max Drawdown ---
    peak = sym_df["equity"].cummax()
    dd = (sym_df["equity"] - peak) / peak
    max_dd = dd.min()
    
    # --- Daily Series ---
    daily_sym = (
        sym_df.groupby("date")["pnl"]
        .sum()
        .reset_index()
    )
    
    daily_sym["equity"] = START_CAPITAL + daily_sym["pnl"].cumsum()
    daily_sym["returns"] = daily_sym["equity"].pct_change().fillna(0)
    
    mean_r = daily_sym["returns"].mean()
    std_r = daily_sym["returns"].std()
    sharpe = (mean_r / std_r) * np.sqrt(252) if std_r != 0 else 0
    
    total_return = sym_df["pnl"].sum()
    recovery = total_return / abs(max_dd * START_CAPITAL) if max_dd != 0 else 0
    
    ulcer = np.sqrt(np.mean(dd**2))
    
    # Stabilised risk penalty (avoid tiny denominator explosion)
    risk_penalty = max(ulcer + abs(max_dd), 0.02)
    
    allocation_score = (sharpe * recovery) / risk_penalty
    
    symbol_metrics.append([
        sym,
        total_return,
        max_dd,
        sharpe,
        recovery,
        ulcer,
        allocation_score
    ])

symbol_df = pd.DataFrame(symbol_metrics, columns=[
    "symbol",
    "total_return",
    "max_dd",
    "sharpe",
    "recovery_factor",
    "ulcer_index",
    "allocation_score"
])

# ==============================
# REMOVE LOW CAPITAL EFFICIENCY
# ==============================

total_portfolio_return = symbol_df["total_return"].sum()

symbol_df["return_share"] = (
    symbol_df["total_return"] / total_portfolio_return
)

symbol_df["force_remove"] = symbol_df["return_share"] < 0.02

# ==============================
# DRAWdown PENALTY FLAG
# ==============================

symbol_df["dd_flag"] = abs(symbol_df["max_dd"]) > 0.25

symbol_df = symbol_df.sort_values("allocation_score", ascending=False)

print(symbol_df.round(3))

# ==============================
# FINAL WEIGHT RECOMMENDATION
# ==============================

def recommend_weight(row):
    
    if row["force_remove"]:
        return 0.0
    
    # Penalize deep drawdown assets
    if row["dd_flag"]:
        return 0.6
    
    # Top quartile but capped (DD mandate)
    if row["allocation_score"] > symbol_df["allocation_score"].quantile(0.75):
        return 1.2
    
    # Middle tier
    if row["allocation_score"] > symbol_df["allocation_score"].median():
        return 1.0
    
    # Lower tier
    return 0.7

symbol_df["recommended_weight"] = symbol_df.apply(recommend_weight, axis=1)

# ==============================
# PORTFOLIO ADJUSTMENT SUMMARY
# ==============================

print("\n==============================")
print("PORTFOLIO ADJUSTMENT SUMMARY")
print("==============================")

print("\nIncrease Weight:")
print(symbol_df[symbol_df["recommended_weight"] > 1.0]["symbol"].tolist())

print("\nReduce Weight:")
print(symbol_df[
    (symbol_df["recommended_weight"] < 1.0) &
    (symbol_df["recommended_weight"] > 0)
]["symbol"].tolist())

print("\nRemove:")
print(symbol_df[symbol_df["recommended_weight"] == 0]["symbol"].tolist())

print("\nFinal Recommended Weights:")
print(symbol_df[["symbol", "recommended_weight"]])

# ==========================================================
# GLOBAL RISK SCALING FOR 15% DD TARGET
# ==========================================================

print("\n==============================")
print("GLOBAL RISK SCALING SUGGESTION")
print("==============================")

target_dd = 0.15
try:
    current_dd = abs(max_drawdown)
except NameError:
    # Fallback if variable named differently
    current_dd = abs(daily["drawdown"].min())

scaling_factor = target_dd / current_dd if current_dd != 0 else 1

print(f"Current Portfolio DD: {round(current_dd*100,2)}%")
print(f"Target DD: {target_dd*100}%")
print(f"Suggested Global Risk Multiplier: {round(scaling_factor,2)}")