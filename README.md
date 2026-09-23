# Taxi Fare & Price Prediction

## Dependencies:

```
python
uv
```

## Project Setup:

Install dependencies:
```
uv sync
```

## Pulling the data

Download the [NYC TLC yellow taxi trip records](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) for a range of months (both ends included) and save them as CSV files:

```sh
uv run pull_trip_data --from 2022-02 --to 2023-03
```

Files are saved to `data/raw/` as `yellow_tripdata_YYYY-MM.csv`. Use `--out-dir` to save them somewhere else:

```sh
uv run pull_trip_data --from 2022-02 --to 2023-03 --out-dir path/to/dir
```

If a month can't be downloaded (network error, month not published yet, ...) the error is logged and the script continues with the next month.
