import pandas as pd

from aqi_framework.cleaning import clean_air_quality, station_date_duplicate_count


def sample_frame():
    return pd.DataFrame(
        {
            "From Date": ["01-08-2021", "01-08-2021"],
            "To Date": ["01-08-2021", "01-08-2021"],
            "Ozone": [10, 10], "CO": [1, 1], "SO2": [2, 2], "NO2": [3, 3], "PM10": [4, 4], "PM2.5": [5, 5],
            "State": ["Maharasthra", "Maharasthra"], "City": [" Pune ", " Pune "], "Station": ["A", "A"],
        }
    )


def test_cleaning_normalizes_state_and_date():
    cleaned = clean_air_quality(sample_frame())
    assert cleaned.loc[0, "state"] == "Maharashtra"
    assert cleaned.loc[0, "city"] == "Pune"
    assert cleaned.loc[0, "date"] == pd.Timestamp("2021-08-01")


def test_station_date_duplicates_are_detected():
    cleaned = clean_air_quality(sample_frame())
    assert station_date_duplicate_count(cleaned) == 1
