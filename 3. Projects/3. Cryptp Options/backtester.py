
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time
import os
import re

class StrangleBacktester:
    def __init__(self, spot_data_path, options_dir, lot_size=1):
        """
        Initialize backtester with data paths
        
        Args:
            spot_data_path: Path to spot 5m Excel file
            options_dir: Directory containing options CSV files
            lot_size: Number of contracts per lot (default=1)
        """
        self.spot_data = pd.read_excel(spot_data_path)
        self.options_dir = options_dir
        self.lot_size = lot_size
        
        # Ensure spot data has proper datetime
        self.spot_data['datetime'] = pd.to_datetime(self.spot_data['datetime'])
        self.spot_data.sort_values('datetime', inplace=True)
        
        # Storage for trades
        self.trades_summary = []  # Will become backtest_summary.xlsx
        self.trades_detailed = []  # Will become backtest_detailed.xlsx
        self.trade_counter = 0
        
        # Current position tracking
        self.current_position = None
        self.position_tracker = []
        
    def extract_strike_from_symbol(self, symbol):
        """Extract strike price from option symbol like 'C-BTC-65600-250226'"""
        match = re.search(r'BTC-(\d+)-\d{6}', symbol)
        return int(match.group(1)) if match else None
    
    def extract_expiry_from_symbol(self, symbol):
        """Extract expiry date from option symbol like 'C-BTC-65600-250226'"""
        match = re.search(r'BTC-\d+-(\d{6})', symbol)
        if match:
            exp_str = match.group(1)  # 250226
            return datetime.strptime(exp_str, '%y%m%d').date()
        return None
    
    def get_option_price_at_time(self, expiry_date, strike, option_type, target_time, lookback_minutes=1):
        """
        Get option price at specific time from the relevant options file
        
        Args:
            expiry_date: date of expiry
            strike: strike price
            option_type: 'C' or 'P'
            target_time: datetime to get price for
            lookback_minutes: minutes to look back if exact time not found
        """
        # Format expiry for filename (YYYY-MM)
        filename = f"BTC_{expiry_date.strftime('%Y-%m')}.csv"
        filepath = os.path.join(self.options_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"Warning: Options file not found: {filepath}")
            return None
        
        # Load relevant options data
        df = pd.read_csv(filepath)
        
        # Construct symbol pattern to filter
        symbol_pattern = f"{option_type}-BTC-{strike}-{expiry_date.strftime('%y%m%d')}"
        
        # Filter for our specific option
        option_df = df[df['product_symbol'] == symbol_pattern].copy()
        
        if option_df.empty:
            print(f"Warning: No data for {symbol_pattern}")
            return None
        
        # Convert timestamp to full datetime
        # Assuming timestamp format is "HH:MM:SS.ms" and date is from target_time
        option_df['datetime'] = option_df['timestamp'].apply(
            lambda x: datetime.combine(
                target_time.date(),
                datetime.strptime(x.split('.')[0], '%H:%M:%S').time()
            ) if '.' in x else datetime.combine(
                target_time.date(),
                datetime.strptime(x, '%H:%M:%S').time()
            )
        )
        
        # Find closest price to target_time
        time_diff = abs(option_df['datetime'] - target_time)
        closest_idx = time_diff.idxmin()
        closest_time = option_df.loc[closest_idx, 'datetime']
        
        # If closest time is within lookback_minutes, return price
        if abs(closest_time - target_time) <= timedelta(minutes=lookback_minutes):
            return option_df.loc[closest_idx, 'price']
        else:
            print(f"Warning: No price within {lookback_minutes} minutes of {target_time}")
            return None
    
    def check_spot_consolidation(self, spot_idx, lookback=3, max_range=300, max_atr=100):
        """
        Check if spot is consolidating (condition 1)
        
        Args:
            spot_idx: current index in spot_data
            lookback: number of candles to check
            max_range: max price range in points
            max_atr: max ATR value
        """
        if spot_idx < lookback - 1:
            return False
        
        # Get last 'lookback' candles
        candles = self.spot_data.iloc[spot_idx - lookback + 1:spot_idx + 1]
        
        # Calculate price range
        price_range = candles['high'].max() - candles['low'].min()
        
        # Calculate ATR (simplified)
        atr = (candles['high'] - candles['low']).mean()
        
        return price_range <= max_range and atr <= max_atr
    
    def get_otm_strikes(self, spot_price, step=100):
        """Get 1-step OTM strikes (condition 2)"""
        # Round to nearest 100
        base_strike = round(spot_price / step) * step
        
        ce_strike = base_strike + step
        pe_strike = base_strike - step
        
        return ce_strike, pe_strike
    
    def check_option_consolidation(self, ce_prices, pe_prices, lookback=3, max_range=30):
        """
        Check if options are consolidating (condition 3)
        
        Args:
            ce_prices: list of recent CE prices
            pe_prices: list of recent PE prices
            lookback: number of candles to check
            max_range: max price range in points
        """
        if len(ce_prices) < lookback or len(pe_prices) < lookback:
            return False
        
        # Check CE consolidation
        ce_range = max(ce_prices[-lookback:]) - min(ce_prices[-lookback:])
        
        # Check PE consolidation
        pe_range = max(pe_prices[-lookback:]) - min(pe_prices[-lookback:])
        
        return ce_range <= max_range and pe_range <= max_range
    
    def check_exit_conditions(self, current_time, ce_price, pe_price, entry_ce, entry_pe):
        """Check if SL, TP, or forced exit triggered"""
        combined_entry = entry_ce + entry_pe
        combined_current = ce_price + pe_price
        
        pnl_pct = ((combined_current - combined_entry) / combined_entry) * 100
        
        # Check SL (7% loss)
        if pnl_pct <= -7:
            return "SL", pnl_pct
        
        # Check TP (21% gain)
        if pnl_pct >= 21:
            return "TP", pnl_pct
        
        # Check forced exit at 4:30 PM
        if current_time.time() >= time(16, 30):
            return "forced", pnl_pct
        
        return None, pnl_pct
    
    def run_backtest(self, start_date=None, end_date=None):
        """
        Run the complete backtest
        
        Args:
            start_date: datetime to start backtest
            end_date: datetime to end backtest
        """
        # Filter spot data to date range
        spot_data = self.spot_data.copy()
        if start_date:
            spot_data = spot_data[spot_data['datetime'] >= start_date]
        if end_date:
            spot_data = spot_data[spot_data['datetime'] <= end_date]
        
        print(f"Running backtest on {len(spot_data)} spot candles...")
        
        i = 0
        while i < len(spot_data):
            current_spot = spot_data.iloc[i]
            current_time = current_spot['datetime']
            
            # Check if we have an open position
            if self.current_position is not None:
                # Track position minute-by-minute
                self.track_open_position(current_time)
                
                # If position closed, continue to next iteration
                if self.current_position is None:
                    i += 1
                    continue
            
            # Condition 1: Spot consolidation
            if not self.check_spot_consolidation(spot_data.index.get_loc(current_spot.name)):
                i += 1
                continue
            
            # Get strikes
            ce_strike, pe_strike = self.get_otm_strikes(current_spot['close'])
            
            # Determine expiry based on time
            if current_time.time() >= time(16, 30):
                # After 4:30 PM, use next day's expiry
                expiry_date = (current_time + timedelta(days=1)).date()
                # Find next trading day expiry (assuming daily expiries exist)
                while expiry_date.weekday() >= 5:  # Skip weekends if crypto follows traditional
                    expiry_date += timedelta(days=1)
            else:
                # Use today's expiry
                expiry_date = current_time.date()
            
            # Get option prices for consolidation check (need at least 3 minutes of data)
            ce_prices = []
            pe_prices = []
            
            for minutes_ago in [2, 1, 0]:  # Check current and last 2 minutes
                check_time = current_time - timedelta(minutes=minutes_ago)
                
                ce_price = self.get_option_price_at_time(
                    expiry_date, ce_strike, 'C', check_time
                )
                pe_price = self.get_option_price_at_time(
                    expiry_date, pe_strike, 'P', check_time
                )
                
                if ce_price is not None:
                    ce_prices.append(ce_price)
                if pe_price is not None:
                    pe_prices.append(pe_price)
            
            # Condition 3: Option consolidation
            if not self.check_option_consolidation(ce_prices, pe_prices):
                i += 1
                continue
            
            # All conditions met - ENTER POSITION
            entry_ce_price = ce_prices[-1]  # Most recent price
            entry_pe_price = pe_prices[-1]
            
            self.enter_position(
                current_time, ce_strike, pe_strike, expiry_date,
                entry_ce_price, entry_pe_price
            )
            
            i += 1
        
        # Export results
        self.export_results()
    
    def enter_position(self, entry_time, ce_strike, pe_strike, expiry_date, ce_price, pe_price):
        """Enter a new strangle position"""
        self.trade_counter += 1
        trade_id = f"TRADE_{self.trade_counter:04d}"
        
        self.current_position = {
            'trade_id': trade_id,
            'entry_time': entry_time,
            'ce_strike': ce_strike,
            'pe_strike': pe_strike,
            'expiry_date': expiry_date,
            'entry_ce': ce_price,
            'entry_pe': pe_price,
            'combined_entry': ce_price + pe_price
        }
        
        # First entry in position tracker
        self.position_tracker.append({
            'trade_id': trade_id,
            'datetime': entry_time,
            'ce_price': ce_price,
            'pe_price': pe_price,
            'combined_value': ce_price + pe_price,
            'pnl': 0,
            'pnl_pct': 0,
            'minutes_in_trade': 0,
            'status': 'open'
        })
        
        print(f"\n[{entry_time}] ENTRY: {trade_id} - CE:{ce_strike}@{ce_price} PE:{pe_strike}@{pe_price}")
    
    def track_open_position(self, current_time):
        """Track open position at current minute"""
        if self.current_position is None:
            return
        
        # Calculate minutes in trade
        minutes_in_trade = int((current_time - self.current_position['entry_time']).total_seconds() / 60)
        
        # Get current option prices
        ce_price = self.get_option_price_at_time(
            self.current_position['expiry_date'],
            self.current_position['ce_strike'],
            'C',
            current_time
        )
        
        pe_price = self.get_option_price_at_time(
            self.current_position['expiry_date'],
            self.current_position['pe_strike'],
            'P',
            current_time
        )
        
        if ce_price is None or pe_price is None:
            # Skip if prices not available
            return
        
        # Calculate PnL
        combined_current = ce_price + pe_price
        combined_entry = self.current_position['combined_entry']
        pnl = combined_current - combined_entry
        pnl_pct = (pnl / combined_entry) * 100
        
        # Check exit conditions
        exit_reason, final_pnl_pct = self.check_exit_conditions(
            current_time, ce_price, pe_price,
            self.current_position['entry_ce'],
            self.current_position['entry_pe']
        )
        
        # Add to tracker
        tracker_entry = {
            'trade_id': self.current_position['trade_id'],
            'datetime': current_time,
            'ce_price': ce_price,
            'pe_price': pe_price,
            'combined_value': combined_current,
            'pnl': pnl,
            'pnl_pct': pnl_pct,
            'minutes_in_trade': minutes_in_trade,
            'status': 'open' if exit_reason is None else exit_reason
        }
        
        self.position_tracker.append(tracker_entry)
        
        # Exit if conditions met
        if exit_reason is not None:
            self.exit_position(current_time, ce_price, pe_price, exit_reason, final_pnl_pct)
    
    def exit_position(self, exit_time, ce_price, pe_price, exit_reason, final_pnl_pct):
        """Exit current position and record trade"""
        # Add to trades summary
        trade_summary = {
            'trade_id': self.current_position['trade_id'],
            'entry_time': self.current_position['entry_time'],
            'exit_time': exit_time,
            'ce_strike': self.current_position['ce_strike'],
            'pe_strike': self.current_position['pe_strike'],
            'expiry_date': self.current_position['expiry_date'],
            'ce_entry': self.current_position['entry_ce'],
            'pe_entry': self.current_position['entry_pe'],
            'ce_exit': ce_price,
            'pe_exit': pe_price,
            'total_pnl': (ce_price + pe_price) - self.current_position['combined_entry'],
            'pnl_pct': final_pnl_pct,
            'exit_reason': exit_reason,
            'hold_minutes': int((exit_time - self.current_position['entry_time']).total_seconds() / 60)
        }
        
        self.trades_summary.append(trade_summary)
        
        # Update last tracker entry with exit price (in case it was just added)
        if self.position_tracker and self.position_tracker[-1]['trade_id'] == self.current_position['trade_id']:
            self.position_tracker[-1]['status'] = exit_reason
            self.position_tracker[-1]['ce_price'] = ce_price
            self.position_tracker[-1]['pe_price'] = pe_price
            self.position_tracker[-1]['combined_value'] = ce_price + pe_price
            self.position_tracker[-1]['pnl'] = (ce_price + pe_price) - self.current_position['combined_entry']
            self.position_tracker[-1]['pnl_pct'] = final_pnl_pct
        
        print(f"[{exit_time}] EXIT: {self.current_position['trade_id']} - {exit_reason} @ {final_pnl_pct:.2f}%")
        
        # Clear current position
        self.current_position = None
    
    def export_results(self):
        """Export backtest results to Excel files"""
        if self.trades_summary:
            df_summary = pd.DataFrame(self.trades_summary)
            df_summary.to_excel('backtest_summary.xlsx', index=False)
            print(f"\nExported {len(df_summary)} trades to backtest_summary.xlsx")
        else:
            print("\nNo trades generated in backtest")
        
        if self.position_tracker:
            df_detailed = pd.DataFrame(self.position_tracker)
            df_detailed.to_excel('backtest_detailed.xlsx', index=False)
            print(f"Exported {len(df_detailed)} minute-by-minute entries to backtest_detailed.xlsx")
            
            # Print summary statistics
            self.print_summary_stats(df_summary, df_detailed)
    
    def print_summary_stats(self, df_summary, df_detailed):
        """Print basic backtest statistics"""
        print("\n" + "="*50)
        print("BACKTEST RESULTS SUMMARY")
        print("="*50)
        
        if len(df_summary) == 0:
            print("No trades executed")
            return
        
        total_trades = len(df_summary)
        winning_trades = len(df_summary[df_summary['total_pnl'] > 0])
        losing_trades = len(df_summary[df_summary['total_pnl'] < 0])
        
        print(f"Total Trades: {total_trades}")
        print(f"Winning Trades: {winning_trades} ({winning_trades/total_trades*100:.1f}%)")
        print(f"Losing Trades: {losing_trades} ({losing_trades/total_trades*100:.1f}%)")
        print(f"Total PnL: ${df_summary['total_pnl'].sum():.2f}")
        print(f"Average PnL per Trade: ${df_summary['total_pnl'].mean():.2f}")
        print(f"Average Hold Time: {df_summary['hold_minutes'].mean():.1f} minutes")
        
        print("\nExit Reasons:")
        for reason in df_summary['exit_reason'].unique():
            count = len(df_summary[df_summary['exit_reason'] == reason])
            print(f"  {reason}: {count} trades")


# Run the backtest
if __name__ == "__main__":
    # Initialize backtester
    backtester = StrangleBacktester(
        spot_data_path="BTCUSDT_1m_5y.xlsx",  # Your spot data file
        options_dir="options_data",
        lot_size=1
    )
    
    # Run backtest (optional: specify date range)
    backtester.run_backtest(
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31)
    )