"""Utilities for cleaning the NYC yellow taxi dataset."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class TaxiDataCleaner:
    """Clean taxi trips while preserving the input DataFrame."""

    dataset: pd.DataFrame
    dataset_month: str | None = None
    max_duration_minutes: float = 180.0
    max_speed_mph: float = 80.0
    max_trip_distance_miles: float = 1000.0
    remove_duplicates: bool = True

    REQUIRED_COLUMNS = (
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "trip_distance",
        "fare_amount",
    )

    def clean(self) -> pd.DataFrame:
        """Return a cleaned copy suitable for downstream storage or modeling."""
        self._validate_columns()
        cleaned = self.dataset.copy()

        pickup_datetime = pd.to_datetime(cleaned["tpep_pickup_datetime"])
        dropoff_datetime = pd.to_datetime(cleaned["tpep_dropoff_datetime"])
        duration_minutes = (
            dropoff_datetime - pickup_datetime
        ).dt.total_seconds() / 60
        average_speed_mph = (
            cleaned["trip_distance"] / (duration_minutes / 60)
        ).where(duration_minutes > 0)

        if self.dataset_month is None:
            # Without a configured month, the cleaner supports datasets that
            # contain any month or multiple months and does not filter dates.
            date_valid = pd.Series(True, index=cleaned.index)
        else:
            # A monthly file can opt into a date check with values such as
            # "2022-05" or "2025-11". The year is part of the Period, so May
            # 2022 and May 2025 are treated as different datasets.
            dataset_period = pd.Period(self.dataset_month, freq="M")
            date_valid = (
                pickup_datetime.dt.to_period("M").eq(dataset_period)
                & dropoff_datetime.dt.to_period("M").eq(dataset_period)
            )

        # The remaining rules remove physically impossible or unusable trips:
        # negative/zero duration, excessive duration, non-positive distance,
        # physically implausible distance, non-positive target fare, and speeds
        # above the configured limit. These rules target data errors, not normal
        # statistical outliers that may represent valid taxi rides.
        valid_rows = (
            date_valid
            # A trip must have a real forward duration.
            & duration_minutes.gt(0)
            # Trips over three hours are treated as invalid by default because
            # they are unlikely to represent a standard taxi trip in this data.
            & duration_minutes.le(self.max_duration_minutes)
            # Zero or negative distance cannot describe a valid paid trip.
            & cleaned["trip_distance"].gt(0)
            # Extremely large distances are treated as corrupted measurements.
            & cleaned["trip_distance"].le(self.max_trip_distance_miles)
            # A positive fare is required when fare_amount is the prediction target.
            & cleaned["fare_amount"].gt(0)
            # Very high implied speeds indicate inconsistent timestamps or distance.
            & average_speed_mph.le(self.max_speed_mph)
        )

        cleaned["duration_minutes"] = duration_minutes
        cleaned["average_speed_mph"] = average_speed_mph
        cleaned["fare_per_mile"] = (
            cleaned["fare_amount"] / cleaned["trip_distance"]
        )
        cleaned = cleaned.loc[valid_rows].copy()

        if self.remove_duplicates:
            # Exact duplicate rows do not add independent observations and can
            # give duplicated trips too much influence during model training.
            cleaned = cleaned.drop_duplicates().copy()

        return cleaned.reset_index(drop=True)

    def _validate_columns(self) -> None:
        missing_columns = [
            column for column in self.REQUIRED_COLUMNS if column not in self.dataset.columns
        ]
        if missing_columns:
            raise ValueError(
                "Dataset is missing required columns: "
                + ", ".join(missing_columns)
            )