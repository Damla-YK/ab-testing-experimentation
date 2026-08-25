# Portfolio 1 — A/B Testing & Experimentation

## Does a new game-discovery experience increase 7-day conversion?

**This is a synthetic portfolio project.** The product scenario, data and results are fictional.

### The business question

A gaming platform is testing a new game-discovery experience.

The question is:

> **Does the new experience cause more users to start a game within 7 days?**

I designed a simple A/B test:

- **Control:** existing experience
- **Treatment:** new experience
- **20,000 users total**
- 10,000 users per group

### Main result

| Metric | Control | Treatment |
|---|---:|---:|
| Users | 10,000 | 10,000 |
| Conversions | 1,261 | 1,415 |
| Conversion rate | 12.61% | 14.15% |

The treatment produced:

- **+1.54 percentage points absolute lift**
- **+12.2% relative lift**
- **p = 0.00138**
- **95% CI: +0.60 to +2.48 percentage points**

### What does that mean?

In simple terms:

The old experience converted about 13 out of every 100 users.

The new experience converted about 14 out of every 100 users.

So we observed approximately **1.54 additional conversions per 100 users**.

The 12.2% figure is a **relative** increase. It does not mean 12 additional people converted out of every 100.

This distinction is important when communicating experiment results in a workplace.

---

## What I analysed

I worked through the experiment in this order:

1. Loaded and inspected the data
2. Checked the Control/Treatment split
3. Checked whether the groups looked balanced
4. Compared raw conversion counts
5. Calculated conversion rates
6. Calculated absolute and relative lift
7. Ran a two-proportion statistical test
8. Calculated a 95% confidence interval
9. Looked at secondary metrics
10. Explored results by device
11. Considered MDE and statistical power
12. Made a business recommendation

---

## Key concepts in plain English

### Absolute lift

**14.15% - 12.61% = +1.54 percentage points**

This is the actual difference between the two conversion rates.

### Relative lift

**1.54 / 12.61 = +12.2%**

This tells us how much larger the treatment conversion rate is relative to the control rate.

### P-value

The p-value was **0.00138**.

Assuming there were genuinely no treatment effect, a difference this large would be very unusual under the assumptions of the statistical test.

The p-value is **not** the probability that the treatment is wrong.

### Confidence interval

Our observed lift was **+1.54 percentage points**.

The 95% confidence interval was:

**+0.60 to +2.48 percentage points**

The simple mental model I use is:

> **1.54 pp = what we observed.**

> **0.60–2.48 pp = the uncertainty around that estimate.**

### MDE and power

Power should be considered **before running an experiment**.

For this project I assumed:

- baseline conversion: 12.61%
- MDE: 1.5 percentage points
- power: 80%
- significance level: 5%

The calculation required approximately **8,075 users per group**.

We actually had **10,000 users per group**, so the experiment had enough users for the planned MDE under these assumptions.

The MDE should come from the business question:

> "What is the smallest improvement that would make this change worthwhile?"

It should not be chosen after seeing the result.

---

## Recommendation

I would recommend **moving to a rollout/business review**.

The treatment increased conversion, the observed effect is statistically significant, and the confidence interval is entirely above zero.

However, I would not make the decision based on the p-value alone.

A real product decision would also consider:

- implementation cost
- expected commercial value
- experiment duration
- data quality
- guardrail metrics
- whether the effect persists
- important user segments

---

## Files

```text
Portfolio_1_AB_Testing/
├── data/
│   └── mock_experiment_data.csv
├── analysis.py
├── README.md
└── requirements.txt
```

### Running the project

Open the project folder in Spyder and run `analysis.py`.

If required, install the packages with:

```bash
pip install pandas numpy scipy statsmodels
```

---

## What this project demonstrates

This project is intended to demonstrate that I can:

- translate a product question into an experiment
- define and interpret an outcome metric
- check treatment/control balance
- calculate and explain effect size
- perform a statistical test
- interpret p-values without overstating them
- calculate and explain confidence intervals
- understand MDE and statistical power
- consider secondary metrics
- translate statistical findings into a business recommendation

The emphasis is on **understanding and communicating the analysis**, rather than using advanced statistical techniques for their own sake.
