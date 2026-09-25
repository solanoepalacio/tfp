import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("=== Starting EDA Analysis ===\n")

# Load the data
data_path = Path("data/raw/yellow_tripdata_2022-05.parquet")
if not data_path.exists():
    data_path = Path("../data/raw/yellow_tripdata_2022-05.parquet")
print(f"Loading data from {data_path.absolute()}...")
df = pd.read_parquet(data_path)

print(f"✓ Data loaded successfully")
print(f"Shape: {df.shape}")
print(f"Number of samples: {df.shape[0]:,}")
print(f"Number of features: {df.shape[1]}")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n")

# Display first few rows
print("=== First 5 rows ===")
print(df.head())
print()

# Column information
print("=== Column Information ===")
print(df.info())
print()

# Check for missing values
print("=== Missing Values ===")
missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100
missing_df = pd.DataFrame({
    'Missing Count': missing_values,
    'Missing Percentage': missing_percentage
})
print(missing_df[missing_df['Missing Count'] > 0])
print()

# Statistical summary
print("=== Statistical Summary ===")
print(df.describe())
print()

# Check data types
print("=== Data Types ===")
print(df.dtypes)
print()

# Check for duplicates
duplicates = df.duplicated().sum()
print(f"=== Duplicates ===")
print(f"Number of duplicate rows: {duplicates:,}")
print(f"Percentage of duplicates: {(duplicates/len(df))*100:.2f}%\n")

# Calculate trip duration
print("=== Target Variables Analysis ===")
df['trip_duration'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60  # in minutes

print("Fare Amount Statistics:")
print(df['fare_amount'].describe())
print("\nTrip Duration (minutes) Statistics:")
print(df['trip_duration'].describe())
print()

# Extract temporal features
print("=== Temporal Features ===")
df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour
df['pickup_day'] = df['tpep_pickup_datetime'].dt.dayofweek
df['pickup_month'] = df['tpep_pickup_datetime'].dt.month
print(df[['pickup_hour', 'pickup_day', 'pickup_month']].head())
print()

# Passenger count analysis
print("=== Passenger Count Statistics ===")
print(df['passenger_count'].describe())
print(f"Unique passenger counts: {sorted(df['passenger_count'].unique())}")
print()

# Distance analysis
print("=== Trip Distance Statistics ===")
print(df['trip_distance'].describe())
print()

# Data quality checks
print("=== Data Quality Checks ===")
negative_fares = (df['fare_amount'] < 0).sum()
print(f"Negative fare amounts: {negative_fares:,}")

invalid_distances = (df['trip_distance'] <= 0).sum()
print(f"Zero or negative distances: {invalid_distances:,}")

negative_durations = (df['trip_duration'] < 0).sum()
print(f"Negative trip durations: {negative_durations:,}")

long_durations = (df['trip_duration'] > 240).sum()
print(f"Very long durations (>4 hours): {long_durations:,}")

zero_passengers = (df['passenger_count'] == 0).sum()
print(f"Zero passenger count: {zero_passengers:,}")
print()

# Correlation analysis
print("=== Correlation Analysis ===")
numeric_cols = ['fare_amount', 'trip_distance', 'passenger_count', 
                'trip_duration', 'pickup_hour', 'pickup_day']
correlation_matrix = df[numeric_cols].corr()
print(correlation_matrix)
print()

print("=== EDA Analysis Complete ===")
print("Key findings saved for your review.")