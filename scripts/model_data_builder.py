"""Build a leakage-safe modeling dataset from cleaned taxi trips."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class TaxiModelDataBuilder:
    """Select prediction features and retain the fare target."""

    cleaned_data: pd.DataFrame

    REQUIRED_COLUMNS = (
        "fare_amount",
        "PULocationID",
        "DOLocationID",
        "trip_distance",
        "tpep_pickup_datetime",
        "passenger_count",
        "RatecodeID",
        "VendorID",
        "store_and_fwd_flag",
    )

    def build(self) -> pd.DataFrame:
        """Return a modeling table without post-trip information leakage."""
        self._validate_columns()
        model_data = self.cleaned_data.copy()

        pickup_datetime = pd.to_datetime(model_data["tpep_pickup_datetime"])
        model_data["pickup_hour"] = pickup_datetime.dt.hour
        model_data["pickup_day_of_week"] = pickup_datetime.dt.dayofweek
        model_data["pickup_month"] = pickup_datetime.dt.month
        pickup_minutes = (
            pickup_datetime.dt.hour * 60
            + pickup_datetime.dt.minute
            + pickup_datetime.dt.second / 60
        )
        model_data["is_morning_rush"] = pickup_minutes.between(
            6 * 60 + 30, 9 * 60 + 30, inclusive="both"
        ).astype("int8")
        model_data["is_evening_rush"] = pickup_minutes.between(
            15 * 60 + 30, 20 * 60, inclusive="both"
        ).astype("int8")
        model_data["is_weekend"] = pickup_datetime.dt.dayofweek.isin([5, 6]).astype(
            "int8"
        )

        # Missingness can contain operational information, so preserve it as a
        # feature instead of deleting every row with a missing input value.
        model_data["passenger_count_missing"] = model_data["passenger_count"].isna()
        model_data["RatecodeID_missing"] = model_data["RatecodeID"].isna()

        # These columns are known before or at pickup and can be used as inputs:
        # locations describe the route, distance describes the planned trip,
        # pickup time captures demand patterns, and vendor/passenger/rate code
        # describe the ride context.
        feature_columns = [
            "PULocationID",
            "DOLocationID",
            "trip_distance",
            "passenger_count",
            "RatecodeID",
            "VendorID",
            "store_and_fwd_flag",
            "pickup_hour",
            "pickup_day_of_week",
            "pickup_month",
            "is_morning_rush",
            "is_evening_rush",
            "is_weekend",
            "passenger_count_missing",
            "RatecodeID_missing",
        ]

        # Keep fare_amount as the supervised-learning target.
        model_columns = feature_columns + ["fare_amount"]

        # Dropoff time, tips, tolls, total amount, payment type, taxes, and
        # surcharges are known only after the ride or include the target. Keeping
        # them would let the model see the answer and create data leakage.
        # duration, average speed, and fare_per_mile also depend on dropoff time
        # or fare, so they are excluded for the same reason.
        # review_distance_fare is only an EDA flag and is not a model feature.
        return model_data.loc[:, model_columns].copy()

    def _validate_columns(self) -> None:
        missing_columns = [
            column for column in self.REQUIRED_COLUMNS if column not in self.cleaned_data.columns
        ]
        if missing_columns:
            raise ValueError(
                "Cleaned dataset is missing required columns: "
                + ", ".join(missing_columns)
            )