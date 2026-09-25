# EDA - Cami's Exploratory Data Analysis

## Overview
This directory contains Cami's exploratory data analysis for the NYC Taxi Fare Prediction project using May 2022 data.

## Files
- `002_eda_cami.ipynb` - Jupyter notebook with comprehensive EDA analysis
- `run_eda.py` - Python script version of the EDA analysis (can run without Jupyter)

## Dataset
- **Source**: NYC TLC Yellow Taxi Trip Records
- **Period**: May 2022
- **Size**: 3,588,295 trips, 19 features (523MB)
- **Format**: Parquet

## Key Findings

### Data Quality Issues
- **20,506 negative fare amounts** (min: -$1,311)
- **46,438 zero/negative distances** 
- **1,268 negative trip durations**
- **4,933 very long durations** (>4 hours, max: 113 hours)
- **73,587 zero passenger count**
- **3.6% missing values** in 5 columns (passenger_count, RatecodeID, store_and_fwd_flag, congestion_surcharge, airport_fee)

### Target Variables
- **Fare Amount**: Mean $15.17, range -$1,311 to $6,966
- **Trip Duration**: Mean 18.2 min, range -14 min to 6,823 min

### Correlations
- **Trip duration ↔ Fare**: 0.20 (moderate correlation)
- **Distance ↔ Fare**: 0.009 (very low correlation - needs investigation)
- **Passenger count ↔ Fare**: 0.03 (very low correlation)

## Proposed Cleaning Steps
1. Remove negative fare amounts (data errors)
2. Filter invalid distances (must be > 0)
3. Fix unrealistic durations (negative or > 4 hours)
4. Handle missing values (impute or remove 3.6%)
5. Address zero passenger count (keep or remove?)
6. Investigate low distance-fare correlation

## Feature Engineering Ideas
1. **Temporal features**: Hour, day of week, month (already extracted)
2. **Speed calculation**: distance/duration (handle division by zero)
3. **Location features**: Pickup/dropoff borough or zones
4. **Rush hour indicator**: Based on hour and day
5. **Weekend indicator**: Based on day of week

## How to Run
### Using Jupyter Notebook
```bash
uv run jupyter lab
# Open 002_eda_cami.ipynb in the browser
```

### Using Python Script
```bash
uv run python notebooks/run_eda.py
```

## Next Steps
- [ ] Implement data cleaning pipeline
- [ ] Create feature engineering functions
- [ ] Save cleaned dataset for model training
- [ ] Compare results with team members on Friday

## Team Notes
This EDA will be consolidated with team findings on Friday before the presentation to Mariano on Wednesday.