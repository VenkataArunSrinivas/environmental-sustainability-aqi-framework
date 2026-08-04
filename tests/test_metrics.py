import pytest

from aqi_framework.evaluate import jaccard_top_k, regression_metrics
from aqi_framework.sample_size import RegressionPowerPlan, minimum_regression_n, regression_power


def test_regression_metrics():
    result = regression_metrics([1, 2, 3], [1, 2, 4])
    assert result["mae"] == pytest.approx(1 / 3)
    assert result["rmse"] == pytest.approx((1 / 3) ** 0.5)


def test_jaccard_top_k():
    assert jaccard_top_k(["a", "b", "c"], ["b", "c", "d"], k=3) == pytest.approx(0.5)


def test_regression_power_plan_reproduces_145():
    plan = RegressionPowerPlan()
    assert minimum_regression_n(plan) == 145
    assert regression_power(145, plan) >= 0.80
