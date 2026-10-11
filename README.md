# Did Late Deliveries Drive the Early-2018 Dip in Review Scores?

A simulated analyst project using the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). It shows the full workflow, from a vague stakeholder ask to a scoped question, careful data prep, and testing.

**Status:** scoping and data prep are done. Hypothesis testing is in progress, so there is no conclusion yet.

## The scenario
I play a new analyst on a marketplace's Customer Experience team (~April 2018). The VP of Ops says:

> "Our review scores have been softer lately, and we're getting more delivery-related complaints. Before we make any big calls on logistics spend, can you dig into what's actually going on?"

## The question
> Did delivery performance (actual vs. estimated delivery date) decline in Jan-Mar 2018 compared to 2017, and does that decline explain a meaningful share of the drop in average review score?

The VP's claim ("it's delivery") is treated as a hypothesis to test, not a fact. Competing explanations are product quality and problems concentrated in specific regions, sellers or categories.

## The data
Olist is a Brazilian online marketplace. The dataset has about 99,000 orders from 2016 to 2018, spread across linked tables.

| Table | Used for |
|---|---|
| `orders` | Order status and dates (the delivery-delay variable) |
| `reviews` | Review scores (the outcome) |

Other tables (customers, order items, etc.) are loaded or reserved for later checks. Raw files are not included in this repo.

## Progress
- [x] `00_scoping`: questions, assumptions, hypothesis, final scoped question
- [x] `01_exploration`: joining tables, data-quality checks, delay distribution
- [ ] Define "late" and review extreme values
- [ ] Compare delivery performance, Jan-Mar 2018 vs. 2017
- [ ] Re-check the score dip and seasonality
- [ ] Link delay to review score
- [ ] Measure how much of the score gap delay explains
- [ ] Conclusions and recommendation

## Findings so far
**Data prep**
- **Duplicate reviews.** 551 orders have more than one review, and 789 review IDs are shared across orders. A plain join would duplicate orders, so I averaged scores to one row per order. The joined table has exactly 99,441 rows, matching the orders table.
- **Missing delivery dates.** 2,965 orders (3.0%) have none, mostly canceled or unshipped orders. The rate in Jan-Mar 2018 is no higher than in 2017, so dropping them should not bias the comparison.
- **Analysis set.** 96,470 delivered orders remain after exclusions.

**Delivery delay** (delivered minus estimated; positive = late)
- Most orders arrive early: the median is about 12 days before the estimate. Late orders form a thin tail.
- Extremes range from about -146 to +189 days. I will report medians and the share of late orders alongside means.

**Early signal, not yet verified:** monthly review scores were lowest in March 2018 (3.73) and softer in Jan-Apr 2018 than most of 2017. This used review dates, so I still need to confirm it using order dates and rule out seasonality.

## Analysis plan
1. Confirm the dip using order dates, and compare Jan-Mar 2017 for seasonality.
2. Compare delay between periods (median delay, late share, shipping time) with confidence intervals.
3. Check how review score changes with delay.
4. Measure how much of the score gap delay explains, with a regression comparison and a counterfactual.
5. If delay explains only part, look at comment themes and regional or seller segments.

## Limitations
- Observational data: this shows association, not causation.
- Only customers who left reviews are observed.
- Scores are 1-5 ratings, so I will check that results don't depend on using the average.

## Repo structure
```
notebooks/   00_scoping, 01_exploration
src/         helpers.py (loads CSVs into SQLite, runs queries)
requirements.txt
```

## Reproduce
1. Download the dataset from Kaggle and place the CSVs in `data/raw/`.
2. Install Python 3.11+ and run `pip install -r requirements.txt`.
3. Run the notebooks in order.

**Tools:** Python (pandas, seaborn, statsmodels, scipy), SQL (SQLite)