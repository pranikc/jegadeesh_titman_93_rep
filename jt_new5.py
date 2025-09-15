# jt93_panelA_replication_strict_FINAL.py
# Final version to match paper's methodology by compounding daily returns.

import os
import numpy as np
import pandas as pd
from pandas.tseries.offsets import MonthEnd

# Optional: Newey–West t-stats
try:
    import statsmodels.api as sm
except ImportError:
    sm = None

# ==============================
# Config
# ==============================
# The paper's sample period is 1965-1989. We pull data starting earlier
# to ensure the longest lookback (J=12) is available for the first portfolio.
START_PULL = "1962-07-01"
END_PULL   = "1989-12-31"
PORT_START = "1965-01-01"
PORT_END   = "1989-12-31"

J_LIST = [3, 6, 9, 12]
K_LIST = [3, 6, 9, 12]

EXCHCD_KEEP = [1, 2]      # NYSE, AMEX
SHRCD_KEEP  = [10, 11]    # Common shares

# --- IMPORTANT: Set to True if you have a WRDS connection ---
USE_WRDS = True

# ==============================
# Data Pull (NEW: Switched to Daily)
# ==============================
def pull_crsp_data_via_wrds(start_date, end_date):
    """
    Pulls daily returns and delisting returns from WRDS.
    Daily data is required to match the paper's methodology.
    """
    print("Connecting to WRDS to pull CRSP daily data...")
    import wrds
    db = wrds.Connection()

    # Query for DAILY stock returns, filtered by exchange and share code
    dret = db.raw_sql(f"""
        SELECT d.permno, d.date, d.ret
        FROM crsp.dsf AS d
        INNER JOIN crsp.msenames AS n
            ON d.permno = n.permno
            AND d.date >= n.namedt
            AND d.date <= COALESCE(n.nameendt, '9999-12-31')
        WHERE d.date BETWEEN '{start_date}' AND '{end_date}'
          AND n.shrcd IN ({', '.join(map(str, SHRCD_KEEP))})
          AND n.exchcd IN ({', '.join(map(str, EXCHCD_KEEP))})
    """, date_cols=['date'])

    # Query for delisting returns remains the same
    dl = db.raw_sql(f"""
        SELECT permno, dlstdt AS date, dlret
        FROM crsp.msedelist
        WHERE dlstdt BETWEEN '{start_date}' AND '{end_date}'
    """, date_cols=['date'])
    dl['dlret'] = pd.to_numeric(dl['dlret'], errors='coerce')

    db.close()
    print("WRDS pull complete.")
    return dret, dl

# ==============================
# Data Prep (NEW: Compounding Function)
# ==============================
def compound_daily_to_monthly(daily_returns):
    """
    Converts a dataframe of daily returns into monthly returns
    by geometrically compounding them, as done in the paper.
    """
    print("Compounding daily returns to monthly...")
    df = daily_returns.copy()
    df['ret'] = pd.to_numeric(df['ret'], errors='coerce')
    df = df.dropna(subset=['ret'])
    
    # Add 1 to returns for compounding
    df['retplus1'] = 1 + df['ret']
    
    # Set date as index and create a month-period column for grouping
    df = df.set_index('date')
    df['month_period'] = df.index.to_period('M')

    # Group by stock and month, then calculate the product of (1+ret)
    # This is the geometric mean, which is the correct way to compound
    mret = df.groupby(['permno', 'month_period'])['retplus1'].prod()
    
    # Subtract 1 to get the final monthly return
    mret = mret - 1
    mret = mret.rename('ret').reset_index()
    
    # Convert the month period back to a month-end timestamp for merging
    mret['date'] = mret['month_period'].dt.to_timestamp('M')
    print("Compounding complete.")
    return mret[['permno', 'date', 'ret']]

def prepare_monthly_universe(daily_returns, delist_returns):
    """
    Takes daily and delist data, compounds to monthly, and merges
    to create the final analysis universe.
    """
    # 1. Compound daily returns to get monthly returns
    mret = compound_daily_to_monthly(daily_returns)
    
    # 2. Merge with delisting returns
    # Standardize delist dates to month-end to match compounded returns
    delist_returns['date'] = delist_returns['date'] + MonthEnd(0)
    
    # Merge, keeping all monthly returns
    m = pd.merge(mret, delist_returns, on=['permno', 'date'], how='left', validate='1:1')
    
    # 3. Calculate the final adjusted monthly return
    m['ret_adj'] = (1.0 + m['ret'].fillna(0.0)) * (1.0 + m['dlret'].fillna(0.0)) - 1.0

    return m[['permno', 'date', 'ret_adj']].sort_values(['permno', 'date']).reset_index(drop=True)

# ==============================
# Signal, Portfolio, and Stats Functions
# (These functions remain the same as the previous version)
# ==============================

def formation_signal(monthly_df, J):
    df = monthly_df.sort_values(['permno', 'date']).copy()
    df['logret'] = np.log1p(df['ret_adj'].where(df['ret_adj'] > -1.0))
    cum_logret = df.groupby('permno')['logret'].rolling(J, min_periods=J).sum()
    cum_logret = cum_logret.reset_index(level=0, drop=True)
    df['formation_ret'] = np.expm1(cum_logret.shift(1))
    df = df.dropna(subset=['formation_ret']).reset_index(drop=True)
    return df[['permno', 'date', 'ret_adj', 'formation_ret']]

def assign_deciles(x):
    return pd.qcut(x, 10, labels=False, duplicates='drop') + 1

def build_panel_A(monthly_df, J_list, K_list, port_start, port_end):
    full_results = {}
    returns_pivoted = monthly_df.pivot_table(index='date', columns='permno', values='ret_adj')
    eval_dates = pd.date_range(port_start, port_end, freq='M')
    returns_pivoted = returns_pivoted.reindex(eval_dates)

    for J in J_list:
        print(f"Processing J={J}...")
        formed = formation_signal(monthly_df, J)
        formed['decile'] = formed.groupby('date')['formation_ret'].transform(assign_deciles)
        deciles = formed.pivot_table(index='date', columns='permno', values='decile')

        for K in K_list:
            portfolio_returns_ts = pd.DataFrame(index=eval_dates, columns=range(1, 11))
            for t in eval_dates:
                active_positions = []
                for h in range(K):
                    form_date = t - pd.DateOffset(months=h)
                    if form_date in deciles.index:
                        cohort_deciles = deciles.loc[form_date].dropna()
                        active_positions.append(cohort_deciles)
                if not active_positions:
                    continue
                
                all_cohorts = pd.concat(active_positions)
                current_returns = returns_pivoted.loc[t, all_cohorts.index]
                monthly_decile_returns = current_returns.groupby(all_cohorts).mean()
                portfolio_returns_ts.loc[t] = monthly_decile_returns
            
            full_results[(J, K)] = portfolio_returns_ts.astype(float)
    return full_results

def nw_tstat(x, lag=0):
    x = x.dropna()
    n = len(x)
    if n < 5 or sm is None:
        mean = x.mean()
        std_err = x.std(ddof=1) / np.sqrt(n)
        return mean / std_err if std_err != 0 else np.nan
    X = sm.add_constant(x)
    model = sm.OLS(x, X.iloc[:,0]).fit(cov_type='HAC', cov_kwds={'maxlags': int(lag)})
    return model.tvalues[0]

def summarize_and_print_panel(results):
    print("\n" + "="*70)
    print("Replication of Jegadeesh & Titman (1993) — Panel A (No Skip Week)")
    print("Method: Daily Compounded Returns, NYSE/AMEX Common Shares")
    print("="*70)
    print(f"{' ':>3} {'K =':<2} {'3':>12} {'6':>12} {'9':>12} {'12':>11}")
    print("-"*60)
    
    for J in J_LIST:
        row_data = {'Sell': [J], 'Buy': [''], 'Buy-sell': ['']}
        t_stat_data = {'Sell': [''], 'Buy': [''], 'Buy-sell': ['']}

        for K in K_LIST:
            df = results.get((J, K))
            if df is None or df.empty or 1 not in df.columns or 10 not in df.columns:
                for key in row_data:
                    row_data[key].append(np.nan)
                    t_stat_data[key].append(np.nan)
                continue

            sell_ts, buy_ts = df[1], df[10]
            ls_ts = buy_ts - sell_ts
            lag = K - 1

            row_data['Sell'].append(sell_ts.mean())
            row_data['Buy'].append(buy_ts.mean())
            row_data['Buy-sell'].append(ls_ts.mean())
            t_stat_data['Sell'].append(nw_tstat(sell_ts, lag=lag))
            t_stat_data['Buy'].append(nw_tstat(buy_ts, lag=lag))
            t_stat_data['Buy-sell'].append(nw_tstat(ls_ts, lag=lag))
            
        print(f"{row_data['Sell'][0]:<3} Sell", end="")
        for val in row_data['Sell'][1:]: print(f"{val:>9.4f}   ", end="")
        print("\n     ", end="")
        for t in t_stat_data['Sell'][1:]: print(f"({t:>4.2f})    ", end="")
        
        print(f"\n{row_data['Buy'][0]:<3} Buy ", end="")
        for val in row_data['Buy'][1:]: print(f"{val:>9.4f}   ", end="")
        print("\n     ", end="")
        for t in t_stat_data['Buy'][1:]: print(f"({t:>4.2f})    ", end="")
        
        print(f"\n{row_data['Buy-sell'][0]:<3} Buy-sell", end="")
        for val in row_data['Buy-sell'][1:]: print(f"{val:>9.4f}   ", end="")
        print("\n     ", end="")
        for t in t_stat_data['Buy-sell'][1:]: print(f"({t:>4.2f})    ", end="")
        print("\n" + "-"*60)

# ==============================
# Main Execution
# ==============================
def main():
    if not USE_WRDS:
        raise ConnectionError("This script requires a WRDS connection to pull daily data.")
    
    # New data pipeline
    daily_returns, delist_returns = pull_crsp_data_via_wrds(START_PULL, END_PULL)
    monthly_universe = prepare_monthly_universe(daily_returns, delist_returns)
    
    results = build_panel_A(
        monthly_df=monthly_universe,
        J_list=J_LIST,
        K_list=K_LIST,
        port_start=PORT_START,
        port_end=PORT_END
    )
    
    summarize_and_print_panel(results)

if __name__ == "__main__":
    main()
