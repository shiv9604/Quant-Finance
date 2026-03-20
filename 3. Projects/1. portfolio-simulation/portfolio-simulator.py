import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==============================
# CONFIG
# ==============================
EXCEL_FILE = "MTEA/MTEA-V18-V1.xlsx"
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
