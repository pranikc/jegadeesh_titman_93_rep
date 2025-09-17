# Comprehensive Analysis of Jegadeesh and Titman (1993): "Returns to Buying Winners and Selling Losers"

## 1. **Paper Overview & Key Findings**

### Main Hypothesis and Motivation
- **Core Hypothesis**: Stock prices exhibit medium-term momentum - past winners continue to outperform and past losers continue to underperform over 3-12 month horizons
- **Motivation**: Reconcile conflicting evidence between:
  - Academic literature supporting contrarian strategies (De Bondt & Thaler, 1985)
  - Practitioner use of relative strength/momentum strategies (Value Line, mutual funds)
- **Time horizon gap**: Previous contrarian evidence focused on very short (1 week/month) or very long (3-5 years) horizons, while practitioners use 3-12 month horizons

### Key Empirical Findings
- **Most successful strategy**: Buy stocks based on past 12-month returns, hold for 3 months
  - Returns: 1.31% per month without skip week
  - Returns: 1.49% per month with 1-week skip between formation and holding
- **6-month/6-month strategy** (primary focus):
  - Returns: 0.95% per month (11.4% annually)
  - Compounded excess return: 12.01% per year
- **Statistical significance**: All 32 strategies examined show positive returns, 31 are statistically significant
- **Economic significance**: Returns remain profitable after transaction costs (9.29% annually after 0.5% one-way costs)

### Time Period and Data Sources
- **Primary sample**: January 1965 - December 1989 (25 years)
- **Back-testing periods**:
  - 1927-1940 (high volatility, mean reversion period)
  - 1941-1964 (similar characteristics to main sample)
- **Data source**: CRSP daily returns file

## 2. **Data Requirements & Sample Construction**

### Exact Data Sources
- **CRSP daily returns file**: Primary source for all return calculations
- **Monthly returns**: Obtained by compounding daily returns
- **COMPUSTAT quarterly industrial database**: For earnings announcement dates (1980-1989 subsample)

### Sample Period Considerations
- **Start date rationale**: 1965 chosen because 12-month/12-month strategy requires 23 months of lagged data
- **Market characteristics matter**: 1927-1940 period shows different results due to extreme volatility and mean reversion

### Stock Universe
- **Exchanges**: NYSE and AMEX stocks only
- **NASDAQ**: Not included (typical for this era due to data quality concerns)
- **Coverage**: All stocks with available returns data in formation period

### Critical Filters
- **Price filters**: No explicit price screens mentioned (unlike later momentum studies)
- **Size filters**: No ex-ante size filters, but ex-post analysis shows winners/losers tend to be smaller stocks
- **Data availability**: Must have returns data for entire J-month formation period
- **Delisted securities**: Included if returns available during formation period

### Data Frequency Requirements
- **Daily data**: Used to compute monthly returns via compounding
- **Monthly frequency**: All portfolio formation and return calculations at monthly level

## 3. **Core Methodology - Portfolio Formation**

### Formation Period Lengths
- **J = 3, 6, 9, 12 months**: Four different lookback periods tested
- **Ranking basis**: Cumulative returns over J months (not risk-adjusted)

### Ranking Methodology
- **Sort type**: Ascending order based on J-month cumulative returns
- **Return calculation**: Simple cumulative returns (not log returns)
- **No industry adjustment**: Pure return-based sorting

### Portfolio Construction
- **Number of portfolios**: 10 deciles
- **Portfolio weighting**: Equal-weighted within each decile
- **Naming convention**:
  - P1 (bottom decile) = "Losers"
  - P10 (top decile) = "Winners"
- **Zero-cost portfolio**: Long P10, Short P1

### The Critical Skip Month
- **Two versions tested**:
  - No skip between formation and holding
  - 1-week skip between periods
- **Rationale for skip**: Avoid bid-ask bounce, price pressure, and short-term reversal effects
- **Impact**: Skip week strategies generally show slightly higher returns

### Treatment of Delisted Securities
- **During formation**: Included if data available
- **During holding**: Returns incorporated until delisting date
- **No survivorship bias**: Delisted returns included when available

## 4. **Portfolio Holding & Return Calculation**

### Holding Period Lengths
- **K = 3, 6, 9, 12 months**: Four holding periods tested
- **Creates 16 base strategies**: 4 formation × 4 holding periods
- **Total 32 strategies**: Including skip-week variants

### Overlapping Portfolio Problem and Solution
- **Challenge**: Monthly portfolio formation creates overlapping holding periods
- **Solution**: Hold K overlapping portfolios simultaneously
- **Mechanics**: Each month:
  - Form new portfolio based on past J months
  - Hold portfolios formed in previous K-1 months
  - Close position from month t-K

### Monthly Rebalancing Mechanics
- **Portfolio revision**: 1/K of securities revised each month
- **Two approaches tested**:
  - Buy-and-hold within each vintage
  - Monthly rebalancing to equal weights
- **Finding**: Results very similar; paper reports rebalanced returns
- **Rebalancing frequency**: Beginning of each month for equal weighting

### Return Calculation Methodology
- **Portfolio returns**: Equal-weighted average of constituent returns
- **Zero-cost returns**: Long portfolio return minus short portfolio return
- **Reported as**: Returns per dollar long (not levered returns)
- **No market adjustment**: Raw returns reported in main tables

### Winner minus Loser (WML) Portfolio Construction
- **Construction**: P10 return - P1 return each month
- **Interpretation**: Return to $1 long winners, $1 short losers
- **Self-financing**: Proceeds from short sales fund long positions

## 5. **Critical Implementation Details**

### The 16 Different Strategies (J,K Combinations)
- **Matrix approach**: 4 formation periods × 4 holding periods
- **Each combination tested independently**
- **Correlation across strategies**: High due to overlapping periods and similar selection

### Calendar Time Portfolio Approach
- **Method**: Track actual calendar month returns
- **Not event time initially**: Main results in calendar time
- **Advantage**: Reflects real investable strategy
- **Handles overlaps**: Multiple vintages held simultaneously

### Risk Adjustments
- **Market model**: rpt - rft = αp + βp(rmt - rft) + eit
- **Factor models**: Paper predates Fama-French three-factor model
- **Beta estimation**: Post-ranking betas using full holding period
- **Finding**: Negative beta for zero-cost portfolio (-0.08)

### Transaction Cost Considerations
- **Assumed cost**: 0.5% one-way (conservative for institutional investors)
- **Turnover**: 84.8% semiannually (86.6% buy side, 83.1% sell side)
- **Net returns**: 9.29% annually after transaction costs
- **Still profitable**: All size subsamples profitable after costs

## 6. **Robustness Tests & Variations**

### Subperiod Analyses
- **Five 5-year periods**: 1965-69, 70-74, 75-79, 80-84, 85-89
- **Finding**: Positive in 4 of 5 periods (negative only in 75-79)
- **75-79 anomaly**: Driven entirely by January effects in small stocks

### January Effect Considerations
- **January returns**: -6.86% average for zero-cost portfolio
- **Other months**: +1.66% average (February-December)
- **Size interaction**: January effect strongest for small stocks
- **Strategy modification**: Could reverse positions in January for 25% annual return

### Industry Momentum vs Individual Stock Momentum
- **Not explicitly tested**: Pure individual stock momentum
- **No industry adjustment**: Rankings based on total returns only

### Size-Based Subsample Results
- **Three groups**: Small, medium, large (tertiles by market cap)
- **Small stocks**: 0.99% monthly return
- **Medium stocks**: 1.26% monthly return
- **Large stocks**: 0.75% monthly return
- **All profitable**: Strategy works across size spectrum

### Longer-Term Reversals
- **Key finding**: Returns partially reverse in months 13-36
- **Cumulative return pattern**:
  - Month 12: +9.5%
  - Month 24: +5.6%
  - Month 36: +4.1%
- **Interpretation**: About half of year 1 profits dissipate

## 7. **Common Pitfalls & "Where Bodies Are Buried"**

### Survivorship Bias Concerns
- **Addressed**: Delisted firms included when data available
- **CRSP advantage**: Includes delisted returns
- **No forward-looking selection**: All stocks with formation period data included

### Look-Ahead Bias in Implementation
- **Formation date**: Use only information available at month-end
- **Price data**: Month-end prices, not forward-looking
- **Compounding**: Daily returns compounded to get monthly returns

### Proper Handling of Missing Returns
- **Formation period**: Stock excluded if missing data
- **Holding period**: Use available returns until delisting/missing
- **No backfilling**: Missing data not imputed

### Microstructure Issues
- **Bid-ask bounce**: Motivation for skip-week variant
- **Finding**: Skip week increases returns slightly (about 0.15% monthly)
- **Price pressure**: Potentially affects extreme deciles

### Why the Skip Month is Absolutely Critical
- **Avoids short-term reversal**: One-month reversal well documented
- **Reduces microstructure noise**: Bid-ask bounce effects
- **Month 1 returns**: Often negative without skip (-0.25% in main sample)
- **Practical implementation**: Allows time for portfolio formation

### Common Mistakes in Overlapping Portfolio Calculations
- **Error 1**: Not maintaining K separate vintage portfolios
- **Error 2**: Full rebalancing each month instead of 1/K revision
- **Error 3**: Incorrect averaging across overlapping periods
- **Correct approach**: Track each vintage separately, combine for aggregate portfolio

## 8. **Practical Implementation Guidance**

### Step-by-Step Process Flow
1. **Month t formation**:
   - Calculate J-month returns for all eligible stocks (t-J to t-1)
   - Rank stocks in ascending order
   - Assign to deciles (equal number of stocks)
   - Form equal-weighted P1 through P10 portfolios

2. **Holding period management**:
   - Hold new portfolio for K months
   - Maintain K-1 existing vintage portfolios
   - Calculate returns for each vintage
   - Aggregate across vintages for strategy return

3. **Monthly maintenance**:
   - Close K-month old position
   - Rebalance continuing positions to equal weight
   - Form new portfolio for current month

### Key Decision Points Where Researchers Often Go Wrong

1. **Return calculation period**:
   - ERROR: Using overlapping returns in formation period
   - CORRECT: Use non-overlapping monthly returns, compound for J months

2. **Portfolio weighting**:
   - ERROR: Value-weighting (biases toward large stocks)
   - CORRECT: Equal-weighting within deciles

3. **Decile assignment**:
   - ERROR: Fixed number of stocks per decile
   - CORRECT: NYSE breakpoints or equal number of stocks

4. **Skip period implementation**:
   - ERROR: Skip full month
   - CORRECT: Skip one week only

### Data Quality Checks
- **Return magnitudes**: Winners ~17% annual, Losers ~8% annual
- **Number of stocks**: Roughly equal across deciles (~100-200 per decile)
- **Turnover**: Should be less than 100% (finding: 84.8%)
- **Beta signs**: Zero-cost portfolio should have negative beta

### Expected Magnitudes of Returns to Validate Implementation

**Monthly Returns (6-month/6-month strategy)**:
- Winners portfolio (P10): 1.74%
- Losers portfolio (P1): 0.79%
- Zero-cost (P10-P1): 0.95%

**Key patterns to verify**:
- Monotonic increase from P1 to P10
- January effect (large negative returns in January)
- April especially strong (96% positive across years)
- Returns decline after month 12 in event time

**Risk-adjusted returns**:
- Alpha should exceed raw returns (due to negative beta)
- Market model alpha: ~1.00% monthly
- Statistical significance: t-statistics above 3.0

This comprehensive blueprint provides all necessary details for accurate replication of the Jegadeesh and Titman (1993) momentum strategy. The critical insights are: (1) the intermediate 3-12 month horizon captures momentum unlike shorter or longer periods, (2) the skip week materially improves results, (3) returns partially reverse after year one suggesting temporary price pressure, and (4) the strategy remains profitable after reasonable transaction costs across all size groups.