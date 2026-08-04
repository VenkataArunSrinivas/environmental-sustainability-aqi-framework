import math

import pandas as pd
import pytest

from aqi_framework.aqi import add_provisional_aqi, subindex


def test_pm25_subindex_at_breakpoints():
    assert subindex(30, "PM2.5") == pytest.approx(50)
    assert subindex(60, "PM2.5") == pytest.approx(100)
    assert subindex(90, "PM2.5") == pytest.approx(200)


def test_provisional_aqi_requires_explicit_opt_in():
    frame = pd.DataFrame({"Ozone": [40], "CO": [0.5], "SO2": [20], "NO2": [30], "PM10": [80], "PM2.5": [45]})
    with pytest.raises(RuntimeError):
        add_provisional_aqi(frame)


def test_readiness_requires_three_pollutants_and_particulate():
    frame = pd.DataFrame({"Ozone": [40, 40], "CO": [0.5, 0.5], "SO2": [None, 20], "NO2": [None, None], "PM10": [None, 80], "PM2.5": [None, None]})
    result = add_provisional_aqi(frame, allow_provisional=True)
    assert not bool(result.loc[0, "aqi_ready_provisional"])
    assert bool(result.loc[1, "aqi_ready_provisional"])
