"""Transparent sample-size planning utilities."""
from __future__ import annotations

from dataclasses import dataclass

from scipy.optimize import brentq
from scipy.stats import f, ncf


@dataclass(frozen=True)
class RegressionPowerPlan:
    alpha: float = 0.05
    power: float = 0.80
    effect_size_f2: float = 0.12
    predictors: int = 10


def regression_power(n: int, plan: RegressionPowerPlan) -> float:
    """Power of the overall multiple-regression F test using a noncentral F distribution."""
    denominator_df = n - plan.predictors - 1
    if denominator_df <= 0:
        return 0.0
    critical = f.ppf(1 - plan.alpha, plan.predictors, denominator_df)
    noncentrality = plan.effect_size_f2 * n
    return float(ncf.sf(critical, plan.predictors, denominator_df, noncentrality))


def minimum_regression_n(plan: RegressionPowerPlan = RegressionPowerPlan(), upper: int = 10000) -> int:
    """Find the smallest integer N meeting the requested power."""
    lower = plan.predictors + 2
    if regression_power(upper, plan) < plan.power:
        raise ValueError("Upper search bound is insufficient for the requested power.")
    root = brentq(lambda n: regression_power(int(n), plan) - plan.power, lower, upper)
    candidate = max(lower, int(root) - 2)
    while regression_power(candidate, plan) < plan.power:
        candidate += 1
    return candidate


def planning_table() -> list[dict[str, object]]:
    plan = RegressionPowerPlan()
    rq1 = minimum_regression_n(plan)
    return [
        {
            "research_question": "RQ1",
            "method": "A priori overall multiple-regression F test",
            "parameters": "alpha=.05; power=.80; f2=.12; 10 effective predictors",
            "parameter_reasoning": "Conventional Type I error and power; conservative small-to-medium effect for aggregate observational data; ten predictors reflects two focal drivers plus parsimonious controls.",
            "minimum_n": rq1,
            "decision": 150,
        },
        {
            "research_question": "RQ2",
            "method": "Conservative extension of RQ1 for restricted lag/interaction terms",
            "parameters": "Pre-specified 1- and 2-month lags; limited interactions",
            "parameter_reasoning": "Lagged terms consume degrees of freedom and require consecutive months; model complexity will be reduced if unique exposure periods are insufficient.",
            "minimum_n": 150,
            "decision": 150,
        },
        {
            "research_question": "RQ3",
            "method": "Stability-oriented planning heuristic",
            "parameters": "15 observations per effective predictor x 10 predictors",
            "parameter_reasoning": "Provides a conservative buffer for regularization, tree-based comparisons, and repeated explanation-stability checks; it is a planning heuristic, not a formal power proof.",
            "minimum_n": 150,
            "decision": 150,
        },
        {
            "research_question": "RQ4",
            "method": "Blocked chronological validation planning",
            "parameters": "Five time blocks with approximately 30 validation observations per block",
            "parameter_reasoning": "Supports repeated held-out error estimates while preserving temporal order and keeping all stations from a state-month in one fold.",
            "minimum_n": 150,
            "decision": 150,
        },
    ]
