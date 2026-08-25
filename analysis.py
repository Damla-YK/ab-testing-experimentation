"""
Portfolio 1: A/B Testing & Experimentation

Question:
Does a new game-discovery experience increase the percentage of
users who convert within 7 days?

The data is synthetic/mock data created for this portfolio project.
"""

import numpy as np
import pandas as pd
from scipy import stats


# ---------------------------------------------------------
# 1. Load the data
# ---------------------------------------------------------

df = pd.read_csv("data/mock_experiment_data.csv")

print("First 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)


# ---------------------------------------------------------
# 2. Check the experiment groups
# ---------------------------------------------------------

print("\nUsers in each group:")
print(df["variant"].value_counts())

print("\nPercentage in each group:")
print(df["variant"].value_counts(normalize=True))


# ---------------------------------------------------------
# 3. Check whether the groups look balanced
# ---------------------------------------------------------

print("\nDevice mix:")
print(
    pd.crosstab(
        df["variant"],
        df["device"],
        normalize="index"
    ).round(3)
)

print("\nPrevious 30-day sessions:")
print(
    df.groupby("variant")["prior_30d_sessions"].describe().round(2)
)


# ---------------------------------------------------------
# 4. Look at the raw conversion numbers
# ---------------------------------------------------------

print("\nConversion counts:")
print(
    pd.crosstab(
        df["variant"],
        df["converted_7d"]
    )
)


# ---------------------------------------------------------
# 5. Calculate conversion rates
# ---------------------------------------------------------

conversion_rates = (
    df.groupby("variant")["converted_7d"].mean()
)

control_rate = conversion_rates["control"]
treatment_rate = conversion_rates["treatment"]

print("\nConversion rates:")
print(conversion_rates)


# ---------------------------------------------------------
# 6. Calculate the size of the improvement
# ---------------------------------------------------------

# Absolute lift tells us the difference in percentage points.
absolute_lift = treatment_rate - control_rate

# Relative lift tells us how much larger treatment is
# compared with the original control rate.
relative_lift = absolute_lift / control_rate

print("\nEffect size:")
print(f"Absolute lift: {absolute_lift * 100:.2f} percentage points")
print(f"Relative lift: {relative_lift * 100:.1f}%")

# ---------------------------------------------------------
# Prepare Control and Treatment groups
# ---------------------------------------------------------

control = df[df["variant"] == "control"]
treatment = df[df["variant"] == "treatment"]

control_conversions = control["converted_7d"].sum()
treatment_conversions = treatment["converted_7d"].sum()

control_users = len(control)
treatment_users = len(treatment)

# ---------------------------------------------------------
# 7. Statistical test
# ---------------------------------------------------------
#
# PREFERRED METHOD: Statsmodels
#
# If Statsmodels is installed, use the library below.
# This is the approach I would normally use in a real
# Python analysis because it is concise and reproducible.
#
# If Statsmodels is NOT installed, the manual calculation
# underneath shows how the z-score and p-value are obtained.
# I worked through this manually while learning the test,
# so the underlying calculation is still clear.
# 
# Note:
# Statsmodels calculates Control - Treatment here,
# so the z-score is negative because Treatment converted more.
# The two-sided p-value is unchanged by the sign.
# ---------------------------------------------------------

try:
    from statsmodels.stats.proportion import proportions_ztest

    z_score, p_value = proportions_ztest(
        [control_conversions, treatment_conversions],
        [control_users, treatment_users]
    )

    print("Using Statsmodels:")
    print(f"Z-score (Control - Treatment): {z_score:.2f}")
    print(f"P-value (two-sided): {p_value:.6f}")

except ImportError:

    print("Statsmodels is not installed.")
    print("Using the manual two-proportion z-test instead.")

    pooled_rate = (
        control_conversions + treatment_conversions
    ) / (control_users + treatment_users)

    standard_error = np.sqrt(
        pooled_rate
        * (1 - pooled_rate)
        * (1 / control_users + 1 / treatment_users)
    )

    z_score = (
        treatment_rate - control_rate
    ) / standard_error

    p_value = 2 * stats.norm.sf(abs(z_score))

    print(f"Z-score: {z_score:.2f}")
    print(f"P-value: {p_value:.6f}")
    
    
# ---------------------------------------------------------
# 8. 95% confidence interval
# ---------------------------------------------------------

# This tells us the uncertainty around the observed
# difference between the two conversion rates.

ci_standard_error = np.sqrt(
    control_rate * (1 - control_rate) / control_users
    + treatment_rate * (1 - treatment_rate) / treatment_users
)

ci_lower = absolute_lift - 1.96 * ci_standard_error
ci_upper = absolute_lift + 1.96 * ci_standard_error

print("\n95% confidence interval:")
print(
    f"{ci_lower * 100:.2f} to {ci_upper * 100:.2f} "
    "percentage points"
)


# ---------------------------------------------------------
# 9. Look at secondary metrics
# ---------------------------------------------------------

print("\nSecondary metrics:")
print(
    df.groupby("variant")[["sessions_7d", "revenue_7d"]].mean().round(2)
)


# ---------------------------------------------------------
# 10. Look at the result by device
# ---------------------------------------------------------

print("\nConversion by device:")
print(
    pd.crosstab(
        df["device"],
        df["variant"],
        values=df["converted_7d"],
        aggfunc="mean"
    ).round(4)
)


# ---------------------------------------------------------
# 11. Simple power / sample-size planning
# ---------------------------------------------------------

# In a real experiment, this would be done BEFORE
# collecting the data.
#
# We assume the business considers a 1.5 percentage-point
# improvement to be the smallest worthwhile effect (MDE).
#
# We want:
# - 80% power
# - 5% significance level

baseline = control_rate
mde = 0.015
target_rate = baseline + mde

z_alpha = stats.norm.ppf(1 - 0.05 / 2)
z_beta = stats.norm.ppf(0.80)

average_rate = (baseline + target_rate) / 2

required_users = (
    (
        z_alpha * np.sqrt(
            2 * average_rate * (1 - average_rate)
        )
        + z_beta * np.sqrt(
            baseline * (1 - baseline)
            + target_rate * (1 - target_rate)
        )
    ) ** 2
    / (target_rate - baseline) ** 2
)

required_users = int(np.ceil(required_users))

print("\nSample-size planning:")
print(f"Minimum detectable effect: {mde * 100:.1f} percentage points")
print(f"Required users per group: {required_users:,}")
print(f"Actual users per group: {control_users:,}")


# ---------------------------------------------------------
# 12. Final recommendation
# ---------------------------------------------------------

print("\nFINAL RECOMMENDATION")

if p_value < 0.05 and ci_lower > 0:
    print(
        "The treatment shows strong evidence of improving conversion."
    )
    print(
        "I would recommend moving to a rollout/business review, "
        "while also considering implementation cost and business value."
    )
else:
    print(
        "There is not enough evidence to recommend the treatment yet."
    )


# ---------------------------------------------------------
# 13. Visualise conversion rates
# ---------------------------------------------------------

variants = ["Control", "Treatment"]
rates = [control_rate, treatment_rate]

plt.figure(figsize=(7, 5))

plt.bar(variants, rates)

plt.ylabel("Conversion rate")
plt.title("7-Day Conversion: Control vs Treatment")

# Show percentages on top of the bars
for i, rate in enumerate(rates):
    plt.text(
        i,
        rate + 0.002,
        f"{rate:.2%}",
        ha="center"
    )

plt.ylim(0, max(rates) + 0.03)
plt.tight_layout()
plt.show()
