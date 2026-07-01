# Velocity Forecasting Guide: Monte Carlo Methods & Probabilistic Estimation

Probabilistic forecasting replaces single-point estimates with a range of outcomes and confidence levels, so
stakeholders manage expectations against real uncertainty rather than false precision. This is the manual fallback for
the forecasting the `velocity_analyzer.py` script performs — reach here when `uv` is unavailable and you must compute a
forecast by hand.

---

## Monte Carlo simulation

Monte Carlo uses random sampling to model outcomes that can't be predicted directly. Applied to velocity:

```text
For each of N iterations (use N = 10000):
1. For each of the sprints ahead, sample a velocity from the historical distribution
2. Sum the sampled velocities into a projected total
3. Record the total
Then read confidence intervals off the sorted distribution of totals.
```

Most teams' velocity is roughly normal after stabilization, characterized by its **mean (μ)** and **standard deviation
(σ)**. Teams with frequent disruptions skew positive.

---

## Core formulas

**Coefficient of variation (predictability):**

```text
CV = σ / μ
```

| CV     | Volatility | Reading              |
| ------ | ---------- | -------------------- |
| ≤15%   | Low        | Predictable          |
| 15-25% | Moderate   | Usable with a buffer |
| 25-40% | High       | Wide ranges only     |
| >40%   | Very high  | Not yet forecastable |

**Single-sprint confidence interval:**

```text
Interval = μ ± (Z-score × σ)
```

**Multi-sprint total** (sum of per-sprint samples):

```text
Total = Σ sampled_velocity_i  for i = 1..n sprints
```

### Confidence-level Z-scores

| Confidence | Z-score | Interpretation            |
| ---------- | ------- | ------------------------- |
| 50%        | 0.67    | Median outcome            |
| 70%        | 1.04    | Moderate confidence       |
| 85%        | 1.44    | High confidence           |
| 95%        | 1.96    | Very high confidence      |
| 99%        | 2.58    | Extremely high confidence |

---

## Reading the simulation

Sort the recorded totals ascending; the value at index `confidence × N` is that confidence level's forecast.

```python
def calculate_confidence_intervals(results, confidence_levels=(0.5, 0.7, 0.85, 0.95)):
    sorted_results = sorted(results)
    return {
        f"{int(c * 100)}%": sorted_results[int(c * len(sorted_results))]
        for c in confidence_levels
    }
```

Example 6-sprint forecast: 50% → 120 pts (median), 70% → 135, 85% → 150, 95% → 170.

### Delivery probability and risk

```text
P(completion ≤ target) = (# simulations ≤ target) / N
```

| Probability | Risk level | Recommendation                  |
| ----------- | ---------- | ------------------------------- |
| >85%        | Low        | Proceed with confidence         |
| 70-85%      | Moderate   | Add buffer, monitor closely     |
| 50-70%      | High       | Reduce scope or extend timeline |
| <50%        | Very high  | Significant replanning required |

Use the **70% confidence interval** as the recommended commitment ceiling for a sprint backlog — it balances ambition
against reliability.

---

## Sampling methods

Pick the method that fits the data:

1. **Historical sampling** — sample actual past velocities with replacement. Simple; ignores trend and assumes a
   stationary distribution.
2. **Normal distribution** — sample from `normal(μ, σ)`, clamping negatives to 0. Mathematically clean; assumes
   normality. This is what the script uses.
3. **Bootstrap** — resample the history to re-estimate μ and σ each iteration, then sample from `normal`. Robust to
   distribution assumptions and accounts for sampling uncertainty; needs enough history.

**Trend adjustment:** when velocity is clearly improving or declining, fit a linear regression to the history and
forecast future sprints from the trend line rather than the flat mean, then simulate around those adjusted values.

---

## Practical use

- **Sprint planning:** set realistic goals, communicate uncertainty to the Product Owner, plan capacity buffers.
- **Release planning:** estimate completion dates, assess schedule risk, make go/no-go decisions.
- **Stakeholder communication:** present ranges and probability statements ("70% confident we deliver X by date Y"),
  never single points.

---

## Common pitfalls

- **Too little data** — use a minimum of 6-8 sprints; below that, widen intervals and note the limitation.
- **Non-stationary data** — exclude sprints from a different team composition or process; look for structural breaks in
  the time series.
- **False precision** — round and say "approximately"; never report "23.7 points" as if certain.
- **Ignoring external factors** — adjust for holidays, team changes, and known dependencies.
- **Overconfidence** — calibrate against actual outcomes; a well-calibrated 70% interval contains the actual result
  about 70% of the time.

The goal is not perfect prediction but honest understanding of uncertainty for better planning decisions.
